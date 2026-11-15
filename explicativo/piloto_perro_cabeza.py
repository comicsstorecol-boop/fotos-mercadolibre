"""Piloto estilo explicativo: ¿Por qué los perros inclinan la cabeza? (Guerra de Peludos)"""
import os, sys, math, subprocess, tempfile
import numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__)); KIT = os.path.dirname(HERE)
sys.path.insert(0, KIT); sys.path.insert(0, HERE)
import generador as G
import visuales as V
from lib import *

OUT = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/explicativo_piloto.mp4"
PREVIEW = os.environ.get("PREVIEW")
ROJO, AZUL, ORO = (232, 36, 36), (35, 100, 235), (255, 200, 60)
LOGO = Image.open(os.path.join(KIT, "marcas", "guerra-de-peludos", "logo.png")).convert("RGBA")
DOG = bulldog()

def dog(c, x, y, size, tilt=0., alpha=1.):
    im = DOG.resize((size, int(size * DOG.height / DOG.width)), Image.LANCZOS)
    place(c, im, x, y, rot=tilt, alpha=alpha)

def tilt_wave(t, amp=14, speed=1.6):
    return amp * math.sin(t * speed * math.pi) if t > .3 else 0

# ------------------------------------------------------------------ escenas
def s1(t, d):
    c = sala().copy()
    place(c, persona("sentado"), 330, 1050, scale=1.05)
    ondas(c, 470, 820, t, (255, 230, 170), direction=10, spread=35, maxr=300)
    dog(c, 790, 1330, 420, tilt=tilt_wave(t, 16, 1.2))
    return camera(c, t, d, 1.0, 1.1, 0, 80)

def s2(t, d):
    c = vgrad(W, H, ESTUDIO).copy(); glow(c, W / 2, 1000, 480, (120, 60, 200), 80)
    cards = [("1", "sonido", "OÍR"), ("2", "ojo", "VER"), ("3", "lupa", "¿?")]
    for i, (n, ic, lab) in enumerate(cards):
        k = eb(pr(t, .2 + i * .35, .5)); y = 640 + i * 360
        hi = i == 2 and t > d * .62
        L = Hi(900, 300); L.rect((0, 0, 900, 300), r=40, fill=(30, 26, 56, 240), outline=ORO if hi else (90, 80, 140), width=6 if hi else 3)
        card = L.done(); card.alpha_composite(V.icono(ic).resize((230, 230)), (40, 30))
        dd = ImageDraw.Draw(card); dd.text((330, 150), lab, font=F(120), fill=ORO if hi else (255, 255, 255), anchor="lm")
        dd.text((860, 60), n, font=F(70), fill=(140, 130, 190), anchor="rm")
        if hi: glow(c, W / 2, y, 300, ORO, 70)
        place(c, card, W / 2 + (1 - k) * 900, y, scale=1 + (.04 * math.sin(t * 8) if hi else 0))
    return camera(c, t, d, 1.0, 1.05)

def s3(t, d):
    c = laboratorio().copy()
    tl = -18 * eio(pr(t, .6, .6)) + (6 * math.sin(t * 3) if t > 1.2 else 0)
    ondas(c, 120, 900, t, (120, 220, 255), n=5, direction=0, spread=40, maxr=380)
    dog(c, 620, 1050, 640, tilt=tl)
    if t > .9: glow(c, 410, 760, 110, (120, 220, 255), int(160 * (.6 + .4 * math.sin(t * 6))))
    etiqueta(c, "UBICA EL SONIDO", W / 2, 1560, (120, 220, 255), alpha=eo(pr(t, 1.2, .4)), borde=(120, 220, 255))
    return camera(c, t, d, 1.04, 1.12, -40, 0)

def s4(t, d):
    c = vgrad(W, H, [(0, (34, 26, 60)), (1, (14, 12, 26))]).copy()
    face = cara_humana(); place(c, face, 720, 700, scale=.95)
    k_tilt = eio(pr(t, d * .55, .7))
    pdog = perro_perfil(); ex, ey = 375, 1185
    cono(c, ex + 60, ey - 40, -52 - 8 * k_tilt, 800, 13, (255, 240, 170), 70)
    place(c, pdog, 370, 1260, scale=1.0, rot=-8 * k_tilt)
    # zona tapada (boca) -> se destapa al inclinar
    a = 1 - k_tilt
    if a > 0:
        L = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(L).rounded_rectangle((560, 790, 880, 930), 30, fill=(20, 18, 30, int(235 * a)))
        c.alpha_composite(L); etiqueta(c, "NO VE TU BOCA", 720, 1000, (255, 120, 120), alpha=a * eo(pr(t, .6, .3)), size=40)
    else:
        glow(c, 720, 860, 120, (255, 230, 120), 80)
    if k_tilt > .6: etiqueta(c, "¡AHORA SÍ!", 720, 1000, (140, 255, 140), alpha=eo(pr(t, d * .55 + .5, .3)), size=40, borde=(140, 255, 140))
    return camera(c, t, d, 1.0, 1.06, 0, -30)

def s5(t, d):
    c = vgrad(W, H, [(0, (40, 22, 60)), (1, (16, 10, 28))]).copy()
    glow(c, 280, 1200, 260, AZUL, 70); glow(c, 800, 1200, 260, ROJO, 70)
    place(c, perro_perfil((200, 170, 130)), 280, 1230, scale=.62)
    dog(c, 800, 1210, 300, tilt=8 * math.sin(t * 2))
    etiqueta(c, "HOCICO LARGO", 280, 1440, (200, 220, 255), size=38)
    etiqueta(c, "CARA CHATA", 800, 1440, (255, 200, 200), size=38)
    for x, val, col, st in ((280, 71, (120, 180, 255), .5), (800, 52, (255, 120, 120), d * .55)):
        k = eo(pr(t, st, 1.2)); bh = 420 * val / 100 * k
        L = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dd = ImageDraw.Draw(L)
        dd.rounded_rectangle((x - 90, 1010 - 420, x + 90, 1010), 30, fill=(255, 255, 255, 30))
        if bh > 20: dd.rounded_rectangle((x - 90, 1010 - bh, x + 90, 1010), 30, fill=col + (235,))
        c.alpha_composite(L); contador(c, val, t, x, 1010 - bh - 90, (255, 255, 255), 110, "%", st, 1.2)
    etiqueta(c, "582 DUEÑOS ENCUESTADOS", W / 2, 470, ORO, size=40, alpha=eo(pr(t, .1, .4)))
    return camera(c, t, d, 1.0, 1.05)

def s6(t, d):
    c = vgrad(W, H, [(0, (60, 10, 30)), (1, (10, 6, 16))]).copy()
    L = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dd = ImageDraw.Draw(L)
    for i in range(-4, 14):
        x = i * 160 + (t * 700) % 160; dd.polygon([(x, 0), (x + 70, 0), (x - 330, H), (x - 400, H)], fill=(255, 60, 90, 30))
    c.alpha_composite(L)
    place(c, V.icono("lupa").resize((520, 520)), W / 2, 980, scale=eb(pr(t, .05, .4)), rot=math.sin(t * 7) * 10)
    if t < .12: c.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(200 * (1 - t / .12)))))
    return camera(c, t, d, 1.08, 1.0)

def s7(t, d):
    c = laboratorio().copy()
    dog(c, W / 2, 1120, 560, tilt=tilt_wave(t, 10, 1))
    toys = [(V.icono("balon").resize((210, 210)), 240, 1380, .4), (hueso(), 850, 1400, .65), (aro(), 870, 860, .9), (V.icono("corazon").resize((150, 150)), 230, 860, 1.1)]
    for im, x, y, st in toys:
        place(c, im, x, y + math.sin(t * 2 + x) * 10, scale=eb(pr(t, st, .4)), rot=math.sin(t * 1.5 + x) * 8)
    etiqueta(c, "BUDAPEST · 2021", W / 2, 520, (120, 220, 255), size=44, alpha=eo(pr(t, .2, .4)), borde=(120, 220, 255))
    return camera(c, t, d, 1.0, 1.08, 0, 40)

def s8(t, d):
    c = vgrad(W, H, [(0, (18, 30, 54)), (1, (8, 12, 24))]).copy(); glow(c, 300, 1000, 300, ORO, 80)
    for x, val, col, st, lab in ((300, 43, ORO, .5, "PERROS GENIO"), (790, 2, (170, 170, 190), d * .6, "PERROS COMUNES")):
        k = eo(pr(t, st, 1.2)); bh = 700 * val / 43 * k
        L = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dd = ImageDraw.Draw(L)
        if bh > 4: dd.rounded_rectangle((x - 120, 1420 - max(bh, 24), x + 120, 1420), 30, fill=col + (240,))
        c.alpha_composite(L); contador(c, val, t, x, 1420 - max(bh, 24) - 110, (255, 255, 255), 150, "%", st, 1.2)
        etiqueta(c, lab, x, 1510, col, size=38)
    if t > .5 + 1.4: place(c, V.icono("trofeo").resize((200, 200)), 300, 400, scale=eb(pr(t, 1.9, .4)))
    return camera(c, t, d, 1.0, 1.05)

def s9(t, d):
    c = sala(False).copy()
    dog(c, 560, 1330, 520, tilt=-14 * eio(pr(t, .3, .5)))
    burbuja(c, 760, 760, 380, 300, max(0, t - .6), V.icono("balon").resize((190, 190)))
    for i in range(10):
        a = t * 1.3 + i; glow(c, 760 + 230 * math.cos(a), 760 + 180 * math.sin(a * 1.2), 10, (255, 240, 160), int(200 * (.5 + .5 * math.sin(t * 4 + i))))
    return camera(c, t, d, 1.0, 1.1, 60, 0)

def s10(t, d):
    c = vgrad(W, H, [(0, (40, 30, 20)), (1, (14, 10, 8))]).copy(); glow(c, W / 2, 800, 380, (255, 190, 40), 90)
    place(c, V.icono("alerta").resize((420, 420)), W / 2, 760, scale=eb(pr(t, .1, .4)), rot=math.sin(t * 5) * 4)
    dog(c, W / 2, 1450, 460, tilt=-10)
    etiqueta(c, "¿CONSTANTE? AL VETERINARIO", W / 2, 1110, (255, 210, 90), size=38, alpha=eo(pr(t, .8, .4)), borde=(255, 210, 90))
    return camera(c, t, d, 1.0, 1.06)

def s11(t, d):
    c = paisaje("ATARDECER").copy()
    place(c, LOGO.resize((560, int(560 * LOGO.height / LOGO.width))), W / 2, 820, scale=eb(pr(t, .1, .5)), rot=math.sin(t * 2) * 3)
    dog(c, W / 2, 1500, 430, tilt=tilt_wave(t, 12, 1.4))
    etiqueta(c, "COMENTA · SÍGUENOS", W / 2, 1190, (20, 18, 34), bg=(255, 255, 255), size=48, alpha=eo(pr(t, 1, .4)))
    return camera(c, t, d, 1.0, 1.05)

ESCENAS = [
    (s1, "¿Por qué tu perro inclina la cabeza cuando le hablas?", {"cabeza"}),
    (s2, "La ciencia tiene tres explicaciones… y la última es la más sorprendente.", {"tres", "sorprendente"}),
    (s3, "Primera: para oír mejor. Al inclinar la cabeza, ubica de dónde viene el sonido.", {"oír", "sonido"}),
    (s4, "Segunda: para verte mejor. Su hocico le tapa la parte de abajo de tu cara.", {"verte", "hocico"}),
    (s5, "En una encuesta a quinientos ochenta y dos dueños, el setenta y uno por ciento de los perros de hocico largo lo hacía seguido. Los de cara chata, como los bulldogs, solo el cincuenta y dos.", {"setenta", "cincuenta"}),
    (s6, "Pero la tercera explicación es la más loca.", {"loca"}),
    (s7, "En dos mil veintiuno, científicos de Hungría estudiaron perros genios que se saben los nombres de sus juguetes.", {"genios", "juguetes"}),
    (s8, "Al oír el nombre de un juguete, los genios inclinaban la cabeza el cuarenta y tres por ciento de las veces. Los demás, solo el dos por ciento.", {"cuarenta", "dos"}),
    (s9, "Inclinar la cabeza sería su forma de pensar: está buscando la imagen del juguete en su memoria.", {"pensar", "memoria"}),
    (s10, "Eso sí: si tu perro inclina la cabeza todo el tiempo, sin motivo, llévalo al veterinario.", {"veterinario"}),
    (s11, "¿Tu perro lo hace? Cuéntanos en los comentarios y síguenos en Guerra de Peludos.", {"comentarios"}),
]

# ------------------------------------------------------------------ audio + render
def main():
    SR = G.SR; LEAD = .15
    speak = G.tts_engine()
    plan = []
    for fn, txt, clave in ESCENAS:
        a = speak(txt); dur = round((LEAD + len(a) / SR + .35) * 30) / 30
        plan.append(dict(fn=fn, txt=txt, clave=clave, audio=a, dur=dur, words=tiempos_palabras(txt, a, SR, LEAD)))
        print(f"{fn.__name__}: {dur:.1f}s", flush=True)
    total = sum(p["dur"] for p in plan); N = int(total * SR) + SR
    if PREVIEW:
        tiles = []
        for p in plan:
            t = p["dur"] * .7; fr = p["fn"](t, p["dur"]); karaoke(fr, p["words"], t, 250, p["clave"]); tiles.append(fr.convert("RGB").resize((270, 480)))
        sh = Image.new("RGB", (270 * 6, 480 * 2))
        for i, im in enumerate(tiles): sh.paste(im, ((i % 6) * 270, (i // 6) * 480))
        sh.save(OUT.replace(".mp4", "_preview.jpg")); print("preview"); return
    vo = np.zeros(N, np.float32); fx = np.zeros(N, np.float32); POP, WH, ST = G.sfx(); off = 0
    for i, p in enumerate(plan):
        G._add(vo, p["audio"], off + LEAD); G._add(fx, WH * .45, max(0, off - .12))
        if i == 5: G._add(fx, ST * .8, off)
        off += p["dur"]
    m = G.music(total, N)
    env = np.convolve(np.abs(vo), np.ones(int(.25 * SR)) / int(.25 * SR), "same")
    fade = np.ones(N); fe = int(total * SR); fl = int(1.2 * SR); fade[fe - fl:fe] = np.linspace(1, 0, fl); fade[fe:] = 0
    mix_ = (m * fade * (1 - .6 * np.clip(env / .03, 0, 1)) * .45 + vo + fx * .45)[:int(total * SR)]
    mix_ = mix_ / max(1e-6, np.abs(mix_).max()) * .92
    with tempfile.TemporaryDirectory() as td:
        sf.write(f"{td}/a.wav", mix_, SR)
        pr_ = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                                "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p", f"{td}/v.mp4"], stdin=subprocess.PIPE)
        prev = None
        for p in plan:
            nf = int(round(p["dur"] * 30)); last = None
            for f in range(nf):
                t = f / 30; fr = p["fn"](t, p["dur"])
                if prev is not None and t < .25: fr = Image.blend(prev, fr, eio(t / .25))
                karaoke(fr, p["words"], t, 250, p["clave"])
                last = fr; pr_.stdin.write(fr.convert("RGB").tobytes())
            prev = p["fn"](p["dur"], p["dur"]); print("ok", p["fn"].__name__, flush=True)
        pr_.stdin.close(); pr_.wait()
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{td}/v.mp4", "-i", f"{td}/a.wav", "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                        "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", "-c:a", "aac", "-b:a", "192k", "-shortest", OUT], check=True)
    print("LISTO", OUT)

if __name__ == "__main__":
    main()
