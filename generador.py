#!/usr/bin/env python3
"""Generador de videos Guerra de Peludos.
Uso:  python3 generador.py guion.json salida.mp4
Lee el guion (ver README.md), genera la voz latina, la música, los efectos,
anima al Bulldog y al gato y entrega un MP4 vertical 1080x1920 listo para Reels/TikTok.
"""
import json, math, os, subprocess, sys, tempfile, wave
from functools import lru_cache
import numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFont, ImageFilter

KIT = os.path.dirname(os.path.abspath(__file__))
A = lambda f: os.path.join(KIT, "assets", f)
W, H, FPS = 1080, 1920, 30
SR = 22050
VOICE = os.environ.get("VOICE", os.path.join(KIT, "voz", "es_MX-claude-high.onnx"))

def font_path(name):
    for p in [f"/usr/share/fonts/truetype/google-fonts/{name}.ttf", os.path.join(KIT, "fonts", f"{name}.ttf")]:
        if os.path.exists(p): return p
    return "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FB, FM = font_path("Poppins-Bold"), font_path("Poppins-Medium")
F = lambda s: ImageFont.truetype(FB, s)
FR = lambda s: ImageFont.truetype(FM if os.path.exists(FM) else FB, s)

TEAM = {
    "perro": dict(kind="dog", colors=((232, 36, 36), (165, 12, 22)), stroke=(110, 10, 10)),
    "gato":  dict(kind="cat", colors=((35, 100, 235), (18, 52, 170)), stroke=(10, 30, 110)),
}
WHITE, DARK = (255, 255, 255), (18, 16, 28)

# ------------------------------------------------------------------ helpers
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def ease_out(t): t = clamp(t); return 1 - (1 - t) ** 3
def ease_back(t):
    t = clamp(t); c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (t - 1) ** 3 + c1 * (t - 1) ** 2
def prog(t, s, d): return clamp((t - s) / d)

def gradient(c1, c2, w=W, h=H):
    g = Image.new("RGB", (1, h))
    for y in range(h):
        k = y / (h - 1); g.putpixel((0, y), tuple(int(c1[i] * (1 - k) + c2[i] * k) for i in range(3)))
    return g.resize((w, h))

def paw(size, color, alpha=255):
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0)); d = ImageDraw.Draw(im); c = tuple(color) + (alpha,); s = size
    d.ellipse((s*.22, s*.45, s*.78, s*.95), fill=c)
    for (x, y) in [(.12, .30), (.34, .10), (.58, .10), (.80, .30)]:
        d.ellipse((s*(x-.1), s*(y-.11), s*(x+.1), s*(y+.13)), fill=c)
    return im

def wrap(text, font, maxw):
    d = ImageDraw.Draw(Image.new("RGBA", (1, 1))); lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw: cur = t
        else: lines.append(cur); cur = w
    lines.append(cur); return lines

@lru_cache(maxsize=4096)
def text_layer(text, size, fill=WHITE, stroke=0, stroke_fill=(0, 0, 0), medium=False):
    font = FR(size) if medium else F(size)
    tmp = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    l, t, r, b = tmp.textbbox((0, 0), text, font=font, stroke_width=stroke)
    asc, desc = font.getmetrics()
    im = Image.new("RGBA", (r - l + 20, asc + desc + 2 * stroke + 20), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((10 - l, 10 + stroke), text, font=font, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill)
    return im

def fit_size(text, size, maxw):
    while size > 30 and ImageDraw.Draw(Image.new("RGBA", (1, 1))).textlength(text, font=F(size)) > maxw: size -= 4
    return size

def put(canvas, layer, cx, cy, scale=1.0, alpha=1.0, rot=0):
    if alpha <= 0 or scale <= 0.01: return
    L = layer
    if scale != 1.0: L = L.resize((max(1, int(L.width * scale)), max(1, int(L.height * scale))), Image.LANCZOS)
    if rot: L = L.rotate(rot, resample=Image.BICUBIC, expand=True)
    if alpha < 1:
        L = L.copy(); L.putalpha(L.getchannel("A").point(lambda v: int(v * alpha)))
    canvas.alpha_composite(L, (int(cx - L.width / 2), int(cy - L.height / 2)))

@lru_cache(maxsize=64)
def pill(w, h, c1, c2, r=None):
    r = r or h // 2; g = gradient(c1, c2, w, h).convert("RGBA")
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w-1, h-1), r, fill=255)
    g.putalpha(m); return g

def fade(c, t, dur, d=.25, col=DARK):
    a = ease_out(prog(t, dur - d, d))
    if a > 0: c.alpha_composite(Image.new("RGBA", (W, H), col + (int(255 * a),)))

# ------------------------------------------------------------------ characters (talking + blink)
CHAR = {
    "dog": dict(src="dog.png", jaw=(500, 600, 800, 850), cut=636, drop=46, mouth=(528, 618, 772, 646),
                mouth_col=(70, 14, 20), tongue=(224, 96, 110), eyes=[(425, 405, 70, 46), (845, 397, 70, 46)], line=(25, 15, 10)),
    "cat": dict(src="cat.png", jaw=(540, 590, 740, 770), cut=628, drop=34, mouth=(560, 612, 720, 636),
                mouth_col=(70, 18, 30), tongue=(228, 110, 130), eyes=[(442, 445, 92, 58), (820, 445, 92, 58)], line=(20, 20, 24)),
}
@lru_cache(maxsize=None)
def _src(kind): return Image.open(A(CHAR[kind]["src"])).convert("RGBA")

@lru_cache(maxsize=None)
def _frame(kind, level, blink):
    c = CHAR[kind]; base = _src(kind).copy(); Wd, Hd = base.size
    if level > 0:
        d = int(c["drop"] * level); x0, y0, x1, y1 = c["jaw"]
        m = Image.new("L", (Wd, Hd), 0); md = ImageDraw.Draw(m)
        md.ellipse((x0, y0, x1, y1), fill=255); md.rectangle((0, 0, Wd, c["cut"]), fill=0)
        jaw = Image.new("RGBA", (Wd, Hd), (0, 0, 0, 0)); jaw.paste(base, (0, 0), m.filter(ImageFilter.GaussianBlur(7)))
        mx0, my0, mx1, my1 = c["mouth"]; dr = ImageDraw.Draw(base)
        dr.ellipse((mx0, my0, mx1, my1 + d + 18), fill=c["mouth_col"], outline=c["line"], width=6)
        if level > .35:
            tw = (mx1 - mx0) * .32; cx = (mx0 + mx1) / 2
            dr.ellipse((cx - tw, my1 + d * .4, cx + tw, my1 + d + 14), fill=c["tongue"])
        base.alpha_composite(jaw, (0, d))
    if blink:
        src = base.copy()
        for (ex, ey, rx, ry) in c["eyes"]:
            bx0, by0, bx1, by1 = int(ex - rx * 1.3), int(ey - ry * 1.4), int(ex + rx * 1.3), int(ey + ry * 1.35)
            up = int(ry * 2.5); patch = src.crop((bx0, by0 - up, bx1, by1 - up))
            m = Image.new("L", patch.size, 0)
            ImageDraw.Draw(m).ellipse((rx * .18, ry * .2, patch.width - rx * .18, patch.height - ry * .15), fill=255)
            base.paste(patch, (bx0, by0), m.filter(ImageFilter.GaussianBlur(9)))
            ImageDraw.Draw(base).arc((ex - rx, ey - ry * 1.1, ex + rx, ey + ry * .9), 18, 162, fill=c["line"], width=10)
    return base

@lru_cache(maxsize=None)
def character(kind, size, level=0.0, blink=False):
    return _frame(kind, round(level * 5) / 5, bool(blink)).resize((size, size), Image.LANCZOS)

# ------------------------------------------------------------------ audio
def tts_engine():
    from piper import PiperVoice, SynthesisConfig
    v = PiperVoice.load(VOICE, config_path=VOICE + ".json")
    cfg = SynthesisConfig(length_scale=0.8, noise_scale=0.6, noise_w_scale=0.7)
    def speak(txt):
        x = np.concatenate([ch.audio_float_array for ch in v.synthesize(txt, syn_config=cfg)]).astype(np.float32)
        with tempfile.TemporaryDirectory() as td:
            sf.write(f"{td}/i.wav", x, SR)
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{td}/i.wav", "-af",
                "highpass=f=75,equalizer=f=140:t=q:w=1.2:g=4,equalizer=f=350:t=q:w=1:g=-2,"
                "equalizer=f=3200:t=q:w=1.5:g=3,equalizer=f=9000:t=q:w=1:g=2,"
                "acompressor=threshold=-20dB:ratio=3.5:attack=4:release=90:makeup=4,aecho=0.8:0.5:22:0.12",
                "-ar", str(SR), f"{td}/o.wav"], check=True)
            y, _ = sf.read(f"{td}/o.wav", dtype="float32")
        return y[:len(x) + int(.05 * SR)]
    return speak

def sfx():
    def pop():
        n = int(.12 * SR); tt = np.arange(n) / SR
        return (np.sin(2*np.pi*np.cumsum(900*np.exp(-tt*18)+300)/SR) * np.exp(-tt*30) * .5).astype(np.float32)
    def whoosh():
        n = int(.45 * SR); w = np.random.default_rng(1).standard_normal(n); env = np.sin(np.linspace(0, np.pi, n)) ** 2
        out = np.zeros(n); a = 0
        for i in range(n): c = .02 + .25 * env[i]; a += c * (w[i] - a); out[i] = a
        return (out * env * .9).astype(np.float32)
    def sting():
        n = int(1.6 * SR); tt = np.arange(n) / SR
        boom = np.sin(2*np.pi*np.cumsum(45 + 90*np.exp(-tt*12))/SR) * np.exp(-tt*3.5)
        noise = np.random.default_rng(7).standard_normal(n) * np.exp(-tt*9) * .35
        sh = sum(np.sin(2*np.pi*f*tt) for f in (523.25, 659.25, 783.99, 1046.5)) * np.exp(-tt*2.2) * .12
        return ((boom + noise + sh) * 1.1).astype(np.float32)
    return pop(), whoosh(), sting()

def music(total, N):
    beat = 60 / 118; add = lambda b, c, at: _add(b, c, at)
    def note(f, dur, kind, vol):
        n = int(dur * SR); tt = np.arange(n) / SR
        if kind == "pluck": w = np.sin(2*np.pi*f*tt) + .5*np.sin(4*np.pi*f*tt) + .25*np.sin(6*np.pi*f*tt); env = np.exp(-tt*7)
        else: w = np.tanh(2*np.sin(2*np.pi*f*tt)); env = np.exp(-tt*3)
        return (w * env * vol).astype(np.float32)
    n = int(.3*SR); tt = np.arange(n)/SR
    K = (np.sin(2*np.pi*np.cumsum(50+110*np.exp(-tt*30))/SR)*np.exp(-tt*9)*.9).astype(np.float32)
    n = int(.18*SR); C = (np.random.default_rng(5).standard_normal(n)*np.exp(-np.arange(n)/SR*22)*.25).astype(np.float32)
    def hat(v):
        n = int(.05*SR); x = np.diff(np.random.default_rng(3).standard_normal(n), prepend=0)
        return (x*np.exp(-np.arange(n)/SR*80)*v).astype(np.float32)
    hz = lambda m: 440 * 2 ** ((m - 69) / 12)
    chords = [[60, 64, 67], [55, 59, 62], [57, 60, 64], [53, 57, 60]]; bass = [36, 31, 33, 29]
    m = np.zeros(N, np.float32)
    for b in range(int(total / (4 * beat)) + 2):
        t0 = b * 4 * beat
        if t0 >= total: break
        add(m, note(hz(bass[b % 4]), 4 * beat, "bass", .22), t0)
        for s in range(8):
            ts = t0 + s * beat / 2
            if ts >= total: break
            if s % 2 == 0: add(m, K, ts)
            if s in (2, 6): add(m, C, ts)
            add(m, hat(.1 if s % 2 else .05), ts + (beat / 4 if s % 2 == 0 else 0))
            add(m, note(hz(chords[b % 4][[0, 2, 1, 2, 0, 1, 2, 1][s]] + 12), beat * .9, "pluck", .07), ts)
    return m

def _add(buf, clip, at):
    i = int(at * SR)
    if i < len(buf): buf[i:i + len(clip)] += clip[:len(buf) - i]

# ------------------------------------------------------------------ build plan from guion
def build(guion, out):
    teams = [dict(TEAM[e["equipo"]], **e) for e in guion["equipos"]]
    vs = len(teams) == 2
    speak = tts_engine()
    LEAD = .35
    scenes = [dict(id="logo", kind="logo", voz="", min=2.6, tail=0)]
    scenes.append(dict(id="intro", kind="intro", voz=guion["intro_voz"], min=3.5, tail=.6))
    for ti, tm in enumerate(teams):
        if tm.get("seccion_voz"):
            scenes.append(dict(id=f"sec{ti}", kind="section", team=ti, voz=tm["seccion_voz"], min=2.2, tail=.5))
        n = len(tm["datos"])
        for i, dato in enumerate(tm["datos"]):
            scenes.append(dict(id=f"t{ti}d{i}", kind="fact", team=ti, idx=i + 1, n=n, titulo=dato["titulo"],
                               texto=dato["texto"], voz=dato.get("voz") or f"Número {i+1}. {dato['titulo']}. {dato['texto']}",
                               min=4.5, tail=.7))
    scenes.append(dict(id="outro", kind="outro", voz=guion["outro_voz"], min=4.0, tail=1.6))

    print("Generando voz…", flush=True)
    for s in scenes:
        s["audio"] = speak(s["voz"]) if s["voz"] else np.zeros(1, np.float32)
        s["dur"] = round(max(s["min"], LEAD + len(s["audio"]) / SR + s["tail"]) * FPS) / FPS
        nf = int(round(s["dur"] * FPS)); env = []
        for f in range(nf):
            a = int((f / FPS - LEAD) * SR); b = a + SR // FPS
            seg = s["audio"][max(0, a):max(0, b)] if b > 0 else s["audio"][:0]
            env.append(float(np.sqrt(np.mean(seg ** 2))) if len(seg) else 0.0)
        env = np.array(env); ref = np.percentile(env[env > 0], 90) if (env > 0).any() else 1
        s["mouth"] = np.clip(env / ref, 0, 1)
    total = sum(s["dur"] for s in scenes); N = int(total * SR) + SR
    print(f"Duración: {total:.1f} s", flush=True)

    # ---- audio mix
    vo = np.zeros(N, np.float32); fx = np.zeros(N, np.float32)
    POP, WH, ST = sfx(); off = 0.0
    for s in scenes:
        _add(vo, s["audio"], off + LEAD); _add(fx, WH * .6, max(0, off - .15))
        if s["kind"] == "fact": _add(fx, POP, off + .15)
        if s["kind"] == "section": _add(fx, POP, off + .45)
        if s["kind"] == "logo": _add(fx, ST, off + .15)
        off += s["dur"]
    m = music(total, N)
    fadev = np.ones(N); fe = int(total * SR); fl = int(1.5 * SR); fadev[fe - fl:fe] = np.linspace(1, 0, fl); fadev[fe:] = 0
    st = np.zeros(N); a0 = int(2.3 * SR); st[a0:] = 1; st[a0:a0 + 12000] = np.linspace(0, 1, 12000)
    env = np.convolve(np.abs(vo), np.ones(int(.25 * SR)) / int(.25 * SR), "same")
    mix = (m * fadev * st * (1 - .55 * np.clip(env / .03, 0, 1)) * .55 + vo + fx * .5)[:int(total * SR)]
    mix = mix / max(1e-6, np.abs(mix).max()) * .92

    # ---- visuals
    LOGO = Image.open(A("logo.png")).convert("RGBA")
    logo = lambda w: LOGO.resize((w, int(w * LOGO.height / LOGO.width)), Image.LANCZOS)
    LOGO_BIG, LOGO_SM = logo(860), logo(110)
    BRAND = text_layer("GUERRA DE PELUDOS", 44, fill=(255, 255, 255, 235))
    def darkbg(acc):
        base = gradient((26, 20, 34), (8, 8, 16)).convert("RGBA")
        mk = Image.new("L", (W, H), 0); ImageDraw.Draw(mk).ellipse((-300, -400, W + 300, 900), fill=110)
        base.paste(Image.new("RGBA", (W, H), acc + (255,)), (0, 0), mk.filter(ImageFilter.GaussianBlur(220))); return base
    BG = [darkbg(tm["colors"][0]) for tm in teams]
    PAWS = {}
    def paws(c, t, color, seed):
        for i in range(6):
            k = (seed * 37 + i * 53) % 100 / 100; x = (i * 173 + seed * 61) % W
            y = (H + 200) - ((t * (40 + 30 * k) + i * 330 + seed * 90) % (H + 400)); sz = int(90 + 80 * k)
            key = (sz, color); PAWS.setdefault(key, paw(sz, color, 38))
            put(c, PAWS[key], x, y, rot=(i * 40 + t * 15) % 360)
    def header(c, t):
        a = ease_out(prog(t, 0, .4)); put(c, LOGO_SM, W/2 - 270, 110, alpha=a); put(c, BRAND, W/2 + 60, 112, alpha=a)
    def ch(kind, size, s, t, gain=1.0, phase=0.0):
        mo = s["mouth"]; lv = clamp(mo[min(len(mo) - 1, int(t * FPS))] * gain)
        return character(kind, size, round(lv * 5) / 5, ((t + phase) % 3.1) < .13)
    def split_bg(c, angle_vertical=False, t=0):
        c1 = teams[0]["colors"]; c2 = teams[1]["colors"] if vs else teams[0]["colors"]
        c.alpha_composite(gradient(*c1).convert("RGBA"))
        if vs:
            mk = Image.new("L", (W, H), 0); off = (1 - ease_out(prog(t, 0, .6))) * W
            pts = ([(W/2 + 120, 0), (W, 0), (W, H), (W/2 - 120, H)] if angle_vertical
                   else [(off, 1080), (W + off, 840), (W + off, H), (off, H)])
            ImageDraw.Draw(mk).polygon(pts, fill=255); c.paste(gradient(c2[1], c2[0]).convert("RGBA"), (0, 0), mk)

    titulo = guion.get("titulo", "5 COSAS QUE NO SABÍAS").upper()
    def f_logo(s, t, dur):
        c = Image.new("RGBA", (W, H), (8, 8, 14, 255)); p = ease_out(prog(t, 0, .8))
        g = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(g)
        d.ellipse((-200, 500, W/2 + 200, 1500), fill=TEAM["perro"]["colors"][0] + (int(150 * p),))
        d.ellipse((W/2 - 200, 500, W + 200, 1500), fill=TEAM["gato"]["colors"][0] + (int(150 * p),))
        c.alpha_composite(g.filter(ImageFilter.GaussianBlur(160)))
        rays = Image.new("RGBA", (W, H), (0, 0, 0, 0)); rd = ImageDraw.Draw(rays)
        for i in range(12):
            a = math.radians(i * 30 + t * 25)
            rd.polygon([(W/2, 900), (W/2 + math.cos(a) * 1400, 900 + math.sin(a) * 1400),
                        (W/2 + math.cos(a + .12) * 1400, 900 + math.sin(a + .12) * 1400)], fill=(255, 255, 255, int(22 * p)))
        c.alpha_composite(rays)
        put(c, LOGO_BIG, W/2, 900, scale=ease_back(prog(t, .15, .7)) * (1 + .02 * math.sin(t * 4)), rot=(1 - ease_out(prog(t, .15, .8))) * -25)
        if t > .5:
            fl = 1 - ease_out(prog(t, .5, .4))
            if fl > 0: c.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(160 * fl))))
        q = ease_out(prog(t, .9, .5))
        put(c, text_layer("GUERRA DE PELUDOS", 96, stroke=6, stroke_fill=(10, 10, 20)), W/2, 1480 + (1 - q) * 60, alpha=q)
        sub = guion.get("subtitulo_logo", "PERROS  VS  GATOS")
        put(c, text_layer(sub, fit_size(sub, 52, 980), fill=(255, 255, 255, 210)), W/2, 1590 + (1 - q) * 60, alpha=q)
        fade(c, t, dur, .2); return c

    def f_intro(s, t, dur):
        c = Image.new("RGBA", (W, H)); split_bg(c, False, t)
        paws(c, t, WHITE, 1)
        q = ease_out(prog(t, 1.3, .5)); ts = fit_size(titulo, 60, 800)
        put(c, pill(900, 120, DARK, (40, 36, 60)), W/2, 170 - (1 - q) * 200, alpha=q)
        put(c, text_layer(titulo, ts), W/2, 170 - (1 - q) * 200, alpha=q)
        if vs:
            for k, tm in enumerate(teams):
                y0 = 520 if k == 0 else 1420; sgn = -1 if k == 0 else 1
                dx = (1 - ease_back(prog(t, .2 + .2 * k, .6))) * 900 * sgn
                put(c, ch(tm["kind"], 560, s, t, phase=.4 + 1.3 * k), W/2 + dx, y0 + math.sin(t * 5 + k) * 8, rot=sgn * -math.sin(t * 2.5) * 3)
                lab = tm.get("plural", tm["nombre"] + "S").upper()
                put(c, text_layer(lab, fit_size(lab, 120, 900), stroke=7, stroke_fill=tm["stroke"]), W/2, 860 if k == 0 else 1760,
                    scale=ease_back(prog(t, .45 + .2 * k, .45)))
            vsl = Image.new("RGBA", (260, 260), (0, 0, 0, 0)); d = ImageDraw.Draw(vsl)
            d.ellipse((10, 10, 250, 250), fill=DARK, outline=WHITE, width=10); vsl.alpha_composite(text_layer("VS", 100), (52, 50))
            put(c, vsl, W/2 + 390, 1000, scale=ease_back(prog(t, .9, .45)), rot=math.sin(t * 6) * 5)
        else:
            tm = teams[0]
            put(c, ch(tm["kind"], 820, s, t, gain=1.2), W/2, 900 + math.sin(t * 5) * 10, scale=ease_back(prog(t, .2, .6)), rot=math.sin(t * 2.5) * 3)
            lab = guion.get("subtitulo_intro", tm.get("plural", tm["nombre"] + "S")).upper()
            put(c, text_layer(lab, fit_size(lab, 120, 960), stroke=7, stroke_fill=tm["stroke"]), W/2, 1450, scale=ease_back(prog(t, .5, .45)))
        fade(c, t, dur); return c

    def f_section(s, t, dur):
        tm = teams[s["team"]]; col = tm["colors"]; c = BG[s["team"]].copy(); paws(c, t, col[0], 2 + s["team"] * 2); header(c, t)
        burst = Image.new("RGBA", (W, H), (0, 0, 0, 0)); bd = ImageDraw.Draw(burst)
        for i in range(16):
            a = math.radians(i * 22.5 + t * 40)
            bd.polygon([(W/2, 780), (W/2 + math.cos(a) * 900, 780 + math.sin(a) * 900),
                        (W/2 + math.cos(a + .14) * 900, 780 + math.sin(a + .14) * 900)], fill=col[0] + (40,))
        c.alpha_composite(burst)
        put(c, ch(tm["kind"], 720, s, t, gain=1.2), W/2, 780 + math.sin(t * 6) * 10, scale=ease_back(prog(t, .05, .55)), rot=math.sin(t * 3) * 4)
        put(c, text_layer("TEAM", 90, fill=(255, 255, 255, 210)), W/2, 1230, alpha=ease_out(prog(t, .35, .4)))
        lab = tm["nombre"].upper()
        put(c, text_layer(lab, fit_size(lab, 190, 980), fill=col[0], stroke=6, stroke_fill=WHITE), W/2, 1390, scale=ease_back(prog(t, .45, .5)))
        fade(c, t, dur); return c

    def f_fact(s, t, dur):
        tm = teams[s["team"]]; col = tm["colors"]; idx, n = s["idx"], s["n"]
        c = BG[s["team"]].copy(); paws(c, t, col[0], idx + 3 + 8 * s["team"]); header(c, t); d = ImageDraw.Draw(c)
        tag = f"{tm.get('plural', tm['nombre'] + 'S').upper()}  ·  DATO {idx}/{n}"
        a0 = ease_out(prog(t, 0, .35)); put(c, pill(620, 84, *col), W/2, 245, alpha=a0)
        put(c, text_layer(tag, fit_size(tag, 38, 580)), W/2, 245, alpha=a0)
        for k in range(n):
            x = W/2 + (k - (n - 1) / 2) * 60; on = k < idx; r = 16 if k == idx - 1 else 11
            d.ellipse((x - r, 335 - r, x + r, 335 + r), fill=col[0] if on else (80, 78, 95))
        put(c, text_layer(str(idx), 300, fill=col[0], stroke=5, stroke_fill=WHITE), W/2, 530, scale=ease_back(prog(t, .1, .55)))
        tl = wrap(s["titulo"], F(92), 900); bl = wrap(s["texto"], FR(56), 860)
        tsz = 92 if len(tl) <= 2 else 76; bsz = 56 if len(bl) <= 5 else 48
        tl = wrap(s["titulo"], F(tsz), 900); bl = wrap(s["texto"], FR(bsz), 860)
        card_h = 70 + len(tl) * int(tsz * 1.2) + 30 + len(bl) * int(bsz * 1.4) + 60; cy0 = 700
        q = ease_out(prog(t, .35, .45))
        card = Image.new("RGBA", (980, card_h), (0, 0, 0, 0))
        ImageDraw.Draw(card).rounded_rectangle((0, 0, 979, card_h - 1), 56, fill=(255, 255, 255, 24), outline=col[0] + (200,), width=5)
        put(c, card, W/2, cy0 + card_h/2 + (1 - q) * 120, alpha=q)
        y = cy0 + 70
        for i, ln in enumerate(tl):
            p = ease_out(prog(t, .9 + i * .12, .4)); put(c, text_layer(ln, tsz), W/2, y + 40 + (1 - p) * 60, alpha=p); y += int(tsz * 1.2)
        y += 30
        for i, ln in enumerate(bl):
            p = ease_out(prog(t, 1.9 + i * .15, .4))
            put(c, text_layer(ln, bsz, fill=(232, 232, 242), medium=True), W/2, y + 28 + (1 - p) * 40, alpha=p); y += int(bsz * 1.4)
        side = -1 if idx % 2 else 1; rise = ease_back(prog(t, .2, .6))
        put(c, ch(tm["kind"], 700, s, t, gain=1.1, phase=idx * .7), W/2 + side * 230,
            H - 210 + max(0, cy0 + card_h - 1320) + (1 - rise) * 560 + math.sin(t * 6) * 8, rot=side * -6 + math.sin(t * 2.2) * 3)
        put(c, paw(120, col[0], 200), W/2 - side * 250, H - 230 + math.sin(t * 4) * 10, scale=ease_back(prog(t, .6, .4)), rot=side * 20)
        ImageDraw.Draw(c).rectangle((0, H - 14, int(W * clamp(t / dur)), H), fill=col[0])
        fade(c, t, dur); return c

    def f_outro(s, t, dur):
        c = Image.new("RGBA", (W, H)); split_bg(c, True, 9); paws(c, t, WHITE, 9)
        q = ease_back(prog(t, .1, .5))
        l1, l2 = guion.get("outro_texto", ["¿Y TÚ DE QUÉ", "EQUIPO ERES?"])
        put(c, pill(940, 330, DARK, (40, 36, 60), r=60), W/2, 360, scale=q)
        put(c, text_layer(l1.upper(), fit_size(l1.upper(), 92, 860)), W/2, 305, scale=q)
        put(c, text_layer(l2.upper(), fit_size(l2.upper(), 92, 860)), W/2, 420, scale=q)
        if vs:
            for k, tm in enumerate(teams):
                x = 280 if k == 0 else W - 280; sgn = 1 if k == 0 else -1
                put(c, ch(tm["kind"], 500, s, t, phase=.3 + 1.2 * k), x, 860 + math.sin(t * 5 + 2 * k) * 10,
                    scale=ease_back(prog(t, .3 + .15 * k, .5)), rot=sgn * (5 + math.sin(t * 3) * 3))
                lab = tm["nombre"].upper()
                put(c, text_layer(lab, fit_size(lab, 110, 460), stroke=7, stroke_fill=tm["stroke"]), x, 1160,
                    scale=ease_back(prog(t, .6 + .15 * k, .4)), rot=sgn * 4)
        else:
            tm = teams[0]
            put(c, ch(tm["kind"], 700, s, t, gain=1.1), W/2, 900 + math.sin(t * 5) * 10, scale=ease_back(prog(t, .3, .5)), rot=math.sin(t * 3) * 3)
        p = ease_out(prog(t, 1.1, .5)); bob = math.sin(t * 6) * 10
        put(c, pill(820, 124, (255, 255, 255), (235, 235, 245)), W/2, 1370 + bob, alpha=p)
        put(c, text_layer("COMENTA  ·  SÍGUENOS", 54, fill=DARK), W/2, 1370 + bob, alpha=p)
        put(c, logo(300), W/2, 1650, alpha=p, scale=.9 + .1 * ease_back(prog(t, 1.2, .5)))
        fade(c, t, dur, .6, (0, 0, 0)); return c

    FN = dict(logo=f_logo, intro=f_intro, section=f_section, fact=f_fact, outro=f_outro)
    with tempfile.TemporaryDirectory() as td:
        if os.environ.get("PREVIEW"):
            ims = [FN[s["kind"]](s, s["dur"] * .6, s["dur"]).convert("RGB").resize((360, 640)) for s in scenes]
            sheet = Image.new("RGB", (360 * min(6, len(ims)), 640 * math.ceil(len(ims) / 6)))
            for i, im in enumerate(ims): sheet.paste(im, ((i % 6) * 360, (i // 6) * 640))
            sheet.save(out.replace(".mp4", "_preview.jpg"), quality=85); print("preview listo"); return
        lst = open(f"{td}/list.txt", "w")
        for s in scenes:
            p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                                  "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19",
                                  "-pix_fmt", "yuv420p", f"{td}/{s['id']}.mp4"], stdin=subprocess.PIPE)
            for i in range(int(round(s["dur"] * FPS))):
                p.stdin.write(FN[s["kind"]](s, i / FPS, s["dur"]).convert("RGB").tobytes())
            p.stdin.close()
            if p.wait() != 0: sys.exit("ffmpeg falló en " + s["id"])
            lst.write(f"file '{s['id']}.mp4'\n"); print("escena", s["id"], "ok", flush=True)
        lst.close(); sf.write(f"{td}/mix.wav", mix, SR)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", f"{td}/list.txt", "-c", "copy", f"{td}/v.mp4"], check=True)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{td}/v.mp4", "-i", f"{td}/mix.wav", "-map", "0:v", "-map", "1:a",
                        "-c:v", "copy", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", "-c:a", "aac", "-b:a", "192k",
                        "-shortest", out + ".tmp.mp4"], check=True)
        os.replace(out + ".tmp.mp4", out)
    print("LISTO:", out)

if __name__ == "__main__":
    build(json.load(open(sys.argv[1], encoding="utf-8")), sys.argv[2])
