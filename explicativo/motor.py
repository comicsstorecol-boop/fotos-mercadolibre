"""Motor de render del estilo explicativo: voz, karaoke, música (alegre o terror), transiciones y video final."""
import os, sys, subprocess, tempfile
import numpy as np, soundfile as sf
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE)); sys.path.insert(0, HERE)
import generador as G
from lib import W, H, karaoke, tiempos_palabras, eio

def musica_terror(total, N, SR):
    t = np.arange(N) / SR; rng = np.random.default_rng(13)
    drone = (np.sin(2 * np.pi * 55 * t) + .6 * np.sin(2 * np.pi * 55.7 * t) + .4 * np.sin(2 * np.pi * 82.4 * t)) * .18
    drone *= .7 + .3 * np.sin(2 * np.pi * .07 * t)
    n = rng.standard_normal(N); wind = np.zeros(N); a = 0.
    for i in range(0, N, 1):  # paso bajo simple (viento)
        a += .004 * (n[i] - a); wind[i] = a
    wind = wind / (np.abs(wind).max() + 1e-6) * .25 * (.6 + .4 * np.sin(2 * np.pi * .05 * t + 1))
    eerie = np.sin(2 * np.pi * (880 + 6 * np.sin(2 * np.pi * 5 * t)) * t) * .03 * (np.sin(2 * np.pi * .03 * t) > .6)
    return (drone + wind + eerie).astype(np.float32)

# Palabras que siempre se dicen en inglés (o con su pronunciación usual) en todos los videos
PRON_BASE = {"store": ("en", "Store"), "steve": ("en", "Steve"), "rogers": ("en", "Rogers"), "avengers": ("es", "avényers"),
             "doomsday": ("es", "dúmsdei"), "thor": ("es", "tor"), "tva": ("es", "te ve a")}
NIVEL = 0.0  # apertura de boca del narrador en el cuadro actual (0..1)

def render(ESCENAS, OUT, regancho_idx=None, musica="alegre", lead=.15, y_sub=250, pron=None, estilo=None, formato="vertical", colores=None, pelicula=False):
    global NIVEL
    import lib; lib.ESTILO_SUB = estilo or "clasico"
    if colores: lib.NEON, lib.NEON2 = colores
    if lib.HORIZONTAL: y_sub = 960
    HORIZ = lib.HORIZONTAL
    if formato == "horizontal" and not HORIZ: raise SystemExit("Para horizontal ejecutar con la variable de entorno FORMATO=horizontal")
    if False:
        def _h(fn):
            fit = fn.__name__ in ("cierre",)
            def g(t, d): return lib.horizontal(fn(t, d), fit=fit)
            g.__name__ = fn.__name__; return g
        pass
    pron = {**PRON_BASE, **(pron or {})}
    SR = G.SR; speak = G.tts_engine(); plan = []
    for fn, txt, clave in ESCENAS:
        a = speak(txt, pron) if pron else speak(txt); dur = round((lead + len(a) / SR + .35) * 30) / 30
        env = np.abs(a); hop = SR // 30; lv = np.array([env[i:i + hop].mean() if i < len(env) else 0 for i in range(0, len(env), hop)])
        lv = np.clip(lv / (np.percentile(lv, 90) + 1e-6), 0, 1)
        sm = np.zeros_like(lv); v = 0.   # boca natural: abre rápido, cierra suave; silencios cerrados
        for i, x in enumerate(lv):
            x = 0. if x < .1 else x ** .85; v += (x - v) * (.6 if x > v else .3); sm[i] = v
        lv = sm
        fn.voz, fn.lead = lv, lead   # actividad de la voz por cuadro: la usan los narradores en video para sincronizar la boca
        plan.append(dict(lv=lv, fn=fn, txt=txt, clave={c.lower() for c in clave}, audio=a, dur=dur, words=tiempos_palabras(txt, a, SR, lead)))
        print(f"{fn.__name__}: {dur:.1f}s", flush=True)
    total = sum(p["dur"] for p in plan); N = int(total * SR) + SR
    if os.environ.get("PREVIEW"):
        tiles = []
        for p in plan:
            t = p["dur"] * .7; fr = p["fn"](t, p["dur"]); karaoke(fr, p["words"], t, y_sub, p["clave"]); tiles.append(fr.convert("RGB").resize((480, 270) if HORIZ else (270, 480)))
        tw, th = tiles[0].size; cols = 8 if not HORIZ else 5; rows = (len(tiles) + cols - 1) // cols; sh = Image.new("RGB", (tw * cols, th * rows))
        for i, im in enumerate(tiles): sh.paste(im, ((i % cols) * tw, (i // cols) * th))
        sh.save(OUT.replace(".mp4", "_preview.jpg")); print("preview", round(total, 1), "s"); return
    vo = np.zeros(N, np.float32); fx = np.zeros(N, np.float32); POP, WH, ST = G.sfx(); off = 0
    for i, p in enumerate(plan):
        G._add(vo, p["audio"], off + lead); G._add(fx, WH * .4, max(0, off - .12))
        if regancho_idx is not None and (i == regancho_idx if isinstance(regancho_idx, int) else i in regancho_idx): G._add(fx, ST * .9, off)
        off += p["dur"]
    am = np.zeros(N, np.float32); off2 = 0
    import sonido as SN
    for p in plan:   # ambientes por escena (atributo fn.amb, uno o varios separados por '+')
        amb = getattr(p["fn"], "amb", None)
        if amb:
            for a_ in amb.split("+"): G._add(am, SN.ambiente(a_, p["dur"] + .4, SR) * .55, max(0, off2 - .2))
        off2 += p["dur"]
    if musica == "terror": m = musica_terror(total, N, SR)
    elif musica == "epica": m = SN.musica_epica(total, N, SR)
    else: m = G.music(total, N)
    env = np.convolve(np.abs(vo), np.ones(int(.25 * SR)) / int(.25 * SR), "same")
    fade = np.ones(N); fe = int(total * SR); fl = int(1.2 * SR); fade[fe - fl:fe] = np.linspace(1, 0, fl); fade[fe:] = 0
    duck = .6 if musica != "terror" else .35
    mix_ = (m * fade * (1 - duck * np.clip(env / .03, 0, 1)) * (.45 if musica != "terror" else .7) + vo + fx * .45 + am * (1 - .45 * np.clip(env / .03, 0, 1)) * .5)[:int(total * SR)]
    mix_ = mix_ / max(1e-6, np.abs(mix_).max()) * .92
    with tempfile.TemporaryDirectory() as td:
        sf.write(f"{td}/a.wav", mix_, SR)
        pr_ = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{lib.W}x{lib.H}", "-r", "30", "-i", "-",
                                "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p", f"{td}/v.mp4"], stdin=subprocess.PIPE)
        prev = None
        t_ini = 0.
        for p in plan:
            nf = int(round(p["dur"] * 30))
            for f in range(nf):
                t = f / 30; k = int((t - lead) * 30); NIVEL = float(p["lv"][k]) if 0 <= k < len(p["lv"]) else 0.
                fr = p["fn"](t, p["dur"])
                if prev is not None and t < .25: fr = Image.blend(prev, fr, eio(t / .25))
                if pelicula:
                    import compositor as _C; fr = fr.convert("RGBA"); _C.fx_pelicula(fr, (t_ini + t))
                karaoke(fr, p["words"], t, y_sub, p["clave"]); pr_.stdin.write(fr.convert("RGB").tobytes())
            t_ini += p["dur"]; prev = p["fn"](p["dur"], p["dur"]); print("ok", p["fn"].__name__, flush=True)
        pr_.stdin.close(); pr_.wait()
        tmp = OUT + ".tmp.mp4"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{td}/v.mp4", "-i", f"{td}/a.wav", "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                        "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", "-c:a", "aac", "-b:a", "192k", "-shortest", tmp], check=True)
        os.replace(tmp, OUT)
    print("LISTO", OUT, round(total, 1), "s")
