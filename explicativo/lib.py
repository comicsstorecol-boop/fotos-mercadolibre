import os
"""Biblioteca del estilo EXPLICATIVO (escenas ilustradas en vector, una por frase).
Todo se dibuja a 2x y se reduce (antialias). Coordenadas siempre en el lienzo final 1080x1920."""
import math, random
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HORIZONTAL = os.environ.get("FORMATO") == "horizontal"
W, H, SS = (1920, 1080, 2) if HORIZONTAL else (1080, 1920, 2)
def Y(v): return 180 + (v - 500) * .74 if HORIZONTAL else v       # mapea coordenadas pensadas en vertical
def X(v): return 960 + (v - 540) * 1.35 if HORIZONTAL else v
KS = .74 if HORIZONTAL else 1.
FB = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
FM = "/usr/share/fonts/truetype/google-fonts/Poppins-Medium.ttf"
def F(s): return ImageFont.truetype(FB, s)
def FMd(s): return ImageFont.truetype(FM, s)

def clamp(x, a=0., b=1.): return max(a, min(b, x))
def eo(t): t = clamp(t); return 1 - (1 - t) ** 3
def eio(t): t = clamp(t); return 3 * t * t - 2 * t * t * t
def eb(t):
    t = clamp(t); c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (t - 1) ** 3 + c1 * (t - 1) ** 2
def pr(t, s, d): return clamp((t - s) / d)
def mix(a, b, k): return tuple(int(a[i] * (1 - k) + b[i] * k) for i in range(len(a)))

# ---------------------------------------------------------------- lienzos
class Hi:
    """Lienzo 2x con helpers en coordenadas finales."""
    def __init__(self, w=W, h=H):
        self.w, self.h = w, h; self.im = Image.new("RGBA", (w * SS, h * SS), (0, 0, 0, 0)); self.d = ImageDraw.Draw(self.im)
    def s(self, v): return v * SS
    def pts(self, p): return [(x * SS, y * SS) for x, y in p]
    def box(self, b): return tuple(v * SS for v in b)
    def ellipse(self, b, **k): self.d.ellipse(self.box(b), **self._k(k))
    def rect(self, b, r=0, **k):
        if r: self.d.rounded_rectangle(self.box(b), int(r * SS), **self._k(k))
        else: self.d.rectangle(self.box(b), **self._k(k))
    def poly(self, p, **k): self.d.polygon(self.pts(p), **self._k(k))
    def line(self, p, **k): self.d.line(self.pts(p), **self._k(k))
    def arc(self, b, a0, a1, **k): self.d.arc(self.box(b), a0, a1, **self._k(k))
    def _k(self, k):
        if "width" in k: k = dict(k, width=int(k["width"] * SS))
        return k
    def paste(self, img, x, y): self.im.alpha_composite(img.resize((img.width * SS, img.height * SS), Image.LANCZOS), (int(x * SS), int(y * SS)))
    def done(self): return self.im.resize((self.w, self.h), Image.LANCZOS)

def vgrad(w, h, stops):
    """stops: [(pos 0..1, (r,g,b)), ...]"""
    g = Image.new("RGB", (1, h))
    for y in range(h):
        k = y / max(1, h - 1)
        for i in range(len(stops) - 1):
            if stops[i][0] <= k <= stops[i + 1][0]:
                kk = (k - stops[i][0]) / max(1e-6, stops[i + 1][0] - stops[i][0]); g.putpixel((0, y), mix(stops[i][1], stops[i + 1][1], kk)); break
    return g.resize((w, h)).convert("RGBA")

def glow(c, x, y, r, color, a=160, blur=None):
    L = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(L).ellipse((x - r, y - r, x + r, y + r), fill=tuple(color) + (a,))
    c.alpha_composite(L.filter(ImageFilter.GaussianBlur(blur or r * .6)))

def shadow_of(img, blur=18, off=(0, 20), a=.5):
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0)); sh.putalpha(img.getchannel("A").point(lambda v: int(v * a)))
    out = Image.new("RGBA", (img.width + 80, img.height + 80), (0, 0, 0, 0))
    out.alpha_composite(sh.filter(ImageFilter.GaussianBlur(blur)), (40 + off[0], 40 + off[1])); out.alpha_composite(img, (40, 40)); return out

def place(c, img, cx, cy, scale=1., rot=0., alpha=1.):
    if alpha <= 0 or scale <= .01: return
    L = img
    if scale != 1: L = L.resize((max(1, int(L.width * scale)), max(1, int(L.height * scale))), Image.LANCZOS)
    if rot: L = L.rotate(rot, resample=Image.BICUBIC, expand=True)
    if alpha < 1: L = L.copy(); L.putalpha(L.getchannel("A").point(lambda v: int(v * alpha)))
    c.alpha_composite(L, (int(cx - L.width / 2), int(cy - L.height / 2)))

def camera(img, t, dur, z0=1.0, z1=1.08, dx=0, dy=0):
    """Movimiento de cámara suave (push-in + paneo)."""
    k = eio(t / max(.01, dur)); z = z0 + (z1 - z0) * k
    big = img.resize((int(W * z), int(H * z)), Image.BILINEAR)
    ox = (big.width - W) / 2 + dx * k; oy = (big.height - H) / 2 + dy * k
    return big.crop((int(ox), int(oy), int(ox) + W, int(oy) + H))

# ---------------------------------------------------------------- paletas
ATARDECER = [(0, (52, 28, 92)), (.45, (196, 82, 120)), (.62, (252, 160, 96)), (.7, (255, 205, 140)), (1, (60, 30, 70))]
NOCHE = [(0, (10, 12, 34)), (.6, (38, 30, 80)), (1, (14, 12, 30))]
DIA = [(0, (90, 160, 235)), (.6, (170, 215, 250)), (1, (230, 240, 250))]
ESTUDIO = [(0, (24, 22, 44)), (1, (10, 10, 20))]

# ---------------------------------------------------------------- escenarios (estáticos, cacheados)
@lru_cache(maxsize=32)
def paisaje(paleta="ATARDECER", sol=True, seed=1):
    pal = globals()[paleta]; c = vgrad(W, H, pal)
    if sol: glow(c, W * .5, H * .58, 260, (255, 210, 140), 210); glow(c, W * .5, H * .58, 120, (255, 240, 200), 255, 40)
    h = Hi(); rnd = random.Random(seed)
    for layer, (base, col) in enumerate([(H * .62, (110, 60, 120)), (H * .66, (80, 44, 96)), (H * .7, (54, 30, 70))]):
        ph = [rnd.uniform(0, 6) for _ in range(3)]; pts = [(0, H)]
        for x in range(0, W + 20, 20):
            y = base - 40 * math.sin(x / 210 + ph[0]) - 22 * math.sin(x / 90 + ph[1]) - 12 * math.sin(x / 41 + ph[2])
            pts.append((x, y))
        pts.append((W, H)); h.poly(pts, fill=col)
    h.rect((0, H * .74, W, H), fill=(40, 24, 52))
    c.alpha_composite(h.done()); return c

@lru_cache(maxsize=8)
def sala(atardecer=True):
    """Sala con ventana al atardecer, sofá y lámpara."""
    c = vgrad(W, H, [(0, (46, 34, 66)), (.7, (70, 48, 82)), (1, (40, 28, 50))])
    h = Hi()
    # ventana
    win = (140, 330, 940, 980)
    sky = vgrad(win[2] - win[0], win[3] - win[1], ATARDECER if atardecer else NOCHE)
    m = Image.new("L", sky.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, sky.width - 1, sky.height - 1), 18, fill=255); sky.putalpha(m)
    c.alpha_composite(sky, (win[0], win[1]))
    glow(c, W * .5, 760, 170, (255, 200, 140), 200)
    h.rect(win, r=18, outline=(30, 20, 40), width=18); h.line([(540, 330), (540, 980)], fill=(30, 20, 40), width=14); h.line([(140, 640), (940, 640)], fill=(30, 20, 40), width=14)
    # piso
    h.poly([(0, 1300), (W, 1300), (W, H), (0, H)], fill=(58, 38, 52))
    for i in range(9): h.line([(i * 140 - 200, H), (W / 2 + (i - 4) * 40, 1300)], fill=(66, 44, 60), width=4)
    # sofá
    h.rect((60, 1060, 640, 1330), r=40, fill=(92, 52, 96)); h.rect((40, 1150, 660, 1360), r=40, fill=(110, 62, 112))
    h.rect((90, 1170, 340, 1250), r=24, fill=(126, 74, 128)); h.rect((360, 1170, 610, 1250), r=24, fill=(126, 74, 128))
    # lámpara
    h.line([(900, 1300), (900, 860)], fill=(40, 30, 40), width=10); h.poly([(830, 860), (970, 860), (940, 760), (860, 760)], fill=(250, 210, 150))
    c.alpha_composite(h.done()); glow(c, 900, 840, 160, (255, 210, 150), 120)
    return c

@lru_cache(maxsize=4)
def laboratorio():
    c = vgrad(W, H, [(0, (16, 30, 54)), (.7, (24, 46, 78)), (1, (10, 18, 34))]); h = Hi()
    for x in range(0, W, 90): h.line([(x, 0), (x, H)], fill=(30, 56, 92), width=2)
    for y in range(0, H, 90): h.line([(0, y), (W, y)], fill=(30, 56, 92), width=2)
    h.rect((0, 1350, W, H), fill=(18, 30, 52)); h.rect((0, 1340, W, 1360), fill=(70, 120, 180))
    c.alpha_composite(h.done()); glow(c, W / 2, 700, 420, (60, 140, 255), 90); return c

# ---------------------------------------------------------------- personajes y objetos
@lru_cache(maxsize=16)
def persona(pose="sentado", piel=(30, 22, 40), rim=(255, 170, 120), s=1.0):
    """Silueta plana con luz de borde."""
    h = Hi(420, 760); k = 1
    def body(col, off=0):
        h.ellipse((150 + off, 40, 270 + off, 165), fill=col)
        h.rect((110 + off, 170, 310 + off, 470), r=70, fill=col)
        if pose == "sentado":
            h.rect((120 + off, 420, 380 + off, 520), r=50, fill=col); h.rect((300 + off, 450, 380 + off, 740), r=36, fill=col)
            h.rect((120 + off, 420, 220 + off, 520), r=50, fill=col)
        else:
            h.rect((130 + off, 440, 200 + off, 750), r=34, fill=col); h.rect((220 + off, 440, 290 + off, 750), r=34, fill=col)
        h.rect((80 + off, 190, 140 + off, 440), r=30, fill=col); h.rect((280 + off, 190, 340 + off, 440), r=30, fill=col)
    body(rim, 6); body(piel, 0)
    im = h.done()
    return im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)

@lru_cache(maxsize=8)
def cara_humana(sonrisa=True):
    h = Hi(420, 480)
    h.ellipse((40, 30, 380, 450), fill=(232, 176, 140)); h.ellipse((40, 10, 380, 200), fill=(60, 40, 40)); h.rect((40, 100, 380, 160), fill=(232, 176, 140))
    for x in (140, 280): h.ellipse((x - 26, 210, x + 26, 262), fill=(255, 255, 255)); h.ellipse((x - 13, 222, x + 13, 250), fill=(40, 30, 30))
    for x in (140, 280): h.line([(x - 34, 186), (x + 30, 178)], fill=(60, 40, 40), width=10)
    h.poly([(210, 250), (186, 320), (232, 320)], fill=(210, 150, 116))
    if sonrisa: h.arc((130, 300, 290, 400), 15, 165, fill=(150, 50, 60), width=14)
    else: h.line([(150, 360), (270, 360)], fill=(150, 50, 60), width=12)
    return h.done()

@lru_cache(maxsize=8)
def perro_perfil(col=(210, 130, 60)):
    """Perro de perfil plano (genérico) para diagramas."""
    h = Hi(560, 420); dk = mix(col, (0, 0, 0), .35)
    h.ellipse((40, 170, 380, 360), fill=col)                           # cuerpo
    for x in (80, 150, 270, 330): h.rect((x, 300, x + 40, 410), r=18, fill=dk)  # patas
    h.ellipse((300, 60, 470, 230), fill=col)                           # cabeza
    h.rect((420, 130, 545, 200), r=30, fill=col)                       # hocico
    h.ellipse((520, 128, 552, 158), fill=(30, 20, 20))                 # nariz
    h.ellipse((310, 70, 380, 200), fill=dk)                            # oreja
    h.ellipse((418, 104, 442, 128), fill=(30, 20, 20))                 # ojo
    h.poly([(40, 230), (0, 150), (60, 210)], fill=col)                 # cola
    return h.done()

@lru_cache(maxsize=8)
def bulldog():
    import os
    p = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "marcas", "guerra-de-peludos", "dog.png")
    im = Image.open(p).convert("RGBA"); return im.crop(im.getchannel("A").getbbox())

@lru_cache(maxsize=8)
def hueso(col=(245, 238, 225)):
    h = Hi(300, 120)
    for x in (40, 260):
        h.ellipse((x - 40, 0, x + 10 if x == 40 else x + 40, 60), fill=col); h.ellipse((x - 40, 60, x + 10 if x == 40 else x + 40, 120), fill=col)
    h.rect((30, 34, 270, 86), r=26, fill=col)
    return h.done()

@lru_cache(maxsize=8)
def aro(col=(90, 170, 255)):
    h = Hi(220, 220); h.ellipse((10, 10, 210, 210), outline=col, width=36); return h.done()

def ondas(c, x, y, t, col=(255, 230, 160), n=4, direction=0, spread=55, maxr=260):
    """Ondas de sonido que se expanden hacia 'direction' (grados)."""
    h = Hi()
    for i in range(n):
        r = ((t * 140 + i * maxr / n) % maxr) + 30; a = 1 - r / (maxr + 30)
        h.arc((x - r, y - r, x + r, y + r), direction - spread, direction + spread, fill=tuple(col) + (int(255 * a),), width=10)
    c.alpha_composite(h.done())

def cono(c, x, y, ang, largo, abertura, col=(255, 240, 160), a=90):
    L = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    p1 = (x + largo * math.cos(math.radians(ang - abertura)), y + largo * math.sin(math.radians(ang - abertura)))
    p2 = (x + largo * math.cos(math.radians(ang + abertura)), y + largo * math.sin(math.radians(ang + abertura)))
    d.polygon([(x, y), p1, p2], fill=tuple(col) + (a,)); c.alpha_composite(L.filter(ImageFilter.GaussianBlur(6)))

def burbuja(c, x, y, w, h, t, contenido=None):
    k = eb(pr(t, 0, .5)); L = Hi()
    for i, (dx, dy, r) in enumerate([(-w * .55, h * .62, 16), (-w * .42, h * .5, 26)]):
        if pr(t, i * .1, .2) > 0: L.ellipse((x + dx - r, y + dy - r, x + dx + r, y + dy + r), fill=(255, 255, 255, 235))
    L.ellipse((x - w / 2 * k, y - h / 2 * k, x + w / 2 * k, y + h / 2 * k), fill=(255, 255, 255, 240))
    c.alpha_composite(L.done())
    if contenido is not None and k > .6: place(c, contenido, x, y, scale=k * .9)

def etiqueta(c, txt, x, y, col=(255, 255, 255), bg=(20, 18, 34), size=46, alpha=1., borde=None):
    f = F(size); tw = ImageDraw.Draw(Image.new("RGBA", (1, 1))).textlength(txt, font=f)
    L = Image.new("RGBA", (int(tw + 60), size + 44), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rounded_rectangle((0, 0, L.width - 1, L.height - 1), 18, fill=tuple(bg) + (230,), outline=tuple(borde) + (255,) if borde else None, width=4 if borde else 0)
    d.text((30, 14), txt, font=f, fill=col); place(c, L, x, y, alpha=alpha)

def contador(c, valor, t, x, y, col, size=200, sufijo="%", start=.2, dur=1.2):
    v = valor * eo(pr(t, start, dur)); txt = f"{v:.0f}{sufijo}"
    f = F(size); L = Image.new("RGBA", (size * 4, int(size * 1.4)), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.text((L.width / 2, L.height / 2), txt, font=f, fill=col, anchor="mm", stroke_width=8, stroke_fill=(10, 8, 20))
    place(c, L, x, y, scale=.9 + .1 * eb(pr(t, start + dur, .3)))

# ---------------------------------------------------------------- subtítulos karaoke
ESTILO_SUB = "clasico"
NEON = (57, 255, 20); NEON2 = (255, 46, 166)

def karaoke(c, palabras, t, y=250, clave=(), size=60, max_chars=26):
    if ESTILO_SUB == "neon": size, max_chars = 74, 20
    if c.size[0] > c.size[1]: size, max_chars = 70, 34
    """palabras: [(t0, t1, 'texto')]. Muestra la línea actual; la palabra dicha en blanco, el resto atenuado; 'clave' enmarcadas."""
    if not palabras: return
    # partir en líneas por cantidad de caracteres
    lines, cur, n = [], [], 0
    for w in palabras:
        if cur and n + len(w[2]) > max_chars: lines.append(cur); cur, n = [], 0
        cur.append(w); n += len(w[2]) + 1
    if cur: lines.append(cur)
    act = None
    for ln in lines:
        if ln[0][0] - .05 <= t <= ln[-1][1] + .15: act = ln; break
    if act is None:
        prev = [ln for ln in lines if ln[-1][1] < t]
        if not prev or t - prev[-1][-1][1] > .6: return
        act = prev[-1]
    f = F(size); d0 = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    widths = [d0.textlength(w[2], font=f) for w in act]; sp = size * .28
    total = sum(widths) + sp * (len(act) - 1)
    if total > c.size[0] - 80:   # dos renglones
        half = len(act) // 2
        karaoke_line(c, act[:half], t, y - size * .62, clave, size); karaoke_line(c, act[half:], t, y + size * .62, clave, size); return
    karaoke_line(c, act, t, y, clave, size)

def karaoke_line(c, act, t, y, clave, size):
    if ESTILO_SUB == "neon": return karaoke_neon(c, act, t, y, clave, size)
    f = F(size); d0 = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    widths = [d0.textlength(w[2], font=f) for w in act]; sp = size * .28; total = sum(widths) + sp * (len(act) - 1)
    CW, CH = c.size; L = Image.new("RGBA", (CW, CH), (0, 0, 0, 0)); d = ImageDraw.Draw(L); x = (CW - total) / 2
    for (t0, t1, txt), w in zip(act, widths):
        said = t >= t0; now = t0 <= t < t1 + .05
        limpio = txt.strip(".,;:!?¡¿").lower()
        if limpio in clave and said:
            d.rectangle((x - 10, y - size * .66, x + w + 10, y + size * .62), outline=(120, 170, 255), width=4)
            for (px, py) in ((x - 10, y - size * .66), (x + w + 10, y - size * .66), (x - 10, y + size * .62), (x + w + 10, y + size * .62)):
                d.rectangle((px - 6, py - 6, px + 6, py + 6), fill=(255, 255, 255), outline=(120, 170, 255), width=3)
        col = (255, 255, 255, 255) if said else (255, 255, 255, 110)
        d.text((x, y), txt, font=f, fill=col, anchor="lm", stroke_width=5 if said else 0, stroke_fill=(0, 0, 0, 160))
        x += w + sp
    sh = Image.new("RGBA", (CW, CH), (0, 0, 0, 0)); sh.putalpha(L.getchannel("A").point(lambda v: int(v * .45)))
    c.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)), (0, 6)); c.alpha_composite(L)

def karaoke_neon(c, act, t, y, clave, size):
    f = F(size); d0 = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    widths = [d0.textlength(w[2].upper(), font=f) for w in act]; sp = size * .3; total = sum(widths) + sp * (len(act) - 1)
    CW, CH = c.size; G_ = Image.new("RGBA", (CW, CH), (0, 0, 0, 0)); L = Image.new("RGBA", (CW, CH), (0, 0, 0, 0)); dg, d = ImageDraw.Draw(G_), ImageDraw.Draw(L); x = (CW - total) / 2
    for (t0, t1, txt), w in zip(act, widths):
        said = t >= t0; now = t0 <= t < t1 + .05; txt = txt.upper()
        clave_w = txt.strip(".,;:!?¡¿…").lower() in clave
        col = (NEON2 if clave_w else NEON) if said else (255, 255, 255)
        yy = y - (8 if now else 0)
        if said: dg.text((x, yy), txt, font=f, fill=col + (255,), anchor="lm", stroke_width=10, stroke_fill=col + (255,))
        d.text((x, yy), txt, font=f, fill=(255, 255, 255, 255) if now else (col + (255,)), anchor="lm", stroke_width=6, stroke_fill=(0, 0, 0, 255))
        x += w + sp
    c.alpha_composite(G_.filter(ImageFilter.GaussianBlur(16)))
    c.alpha_composite(L)

def tiempos_palabras(texto, audio, sr, lead):
    """Estima el tiempo de cada palabra: reparte la duración hablada según longitud + pausas en puntuación."""
    import numpy as np
    words = texto.split()
    if not words: return []
    a = np.abs(audio); thr = max(1e-4, np.percentile(a, 60) * .15)
    idx = np.where(a > thr)[0]; s0 = idx[0] / sr if len(idx) else 0; s1 = idx[-1] / sr if len(idx) else len(audio) / sr
    wts = []
    for w in words:
        base = sum(1 for ch in w if ch.isalnum()) + 1.5
        pausa = 5 if w[-1] in ".!?" else (3 if w[-1] in ",;:" else 0)
        wts.append((base, pausa))
    tot = sum(b + p for b, p in wts); t = lead + s0; span = s1 - s0; out = []
    for w, (b, p) in zip(words, wts):
        d = span * b / tot; out.append((t, t + d, w)); t += d + span * p / tot
    return out

# ---------------------------------------------------------------- marca (cualquier página)
@lru_cache(maxsize=16)
def marca(nombre):
    """Datos de la página: logo, nombre y colores, desde marcas/<nombre>/marca.json."""
    import os, json
    base = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "marcas", nombre)
    b = json.load(open(os.path.join(base, "marca.json"), encoding="utf-8"))
    lp = os.path.join(base, "logo.png")
    logo = Image.open(lp).convert("RGBA") if os.path.exists(lp) else None
    g1, g2 = [tuple(x) for x in b.get("glow", [[255, 200, 60], [120, 80, 220]])]
    return dict(nombre=b["nombre"], logo=logo, c1=g1, c2=g2, cta=b.get("cta", "COMENTA · SÍGUENOS"), disclaimer=b.get("disclaimer"))

def escena_cierre(m, t, d, pregunta=None):
    """Cierre genérico con logo y colores de la página (sin personaje)."""
    c = vgrad(W, H, [(0, mix(m["c2"], (10, 8, 20), .7)), (1, (8, 6, 14))]).copy()
    if HORIZONTAL:
        glow(c, 620, 540, 420, m["c1"], 90); glow(c, 1300, 540, 340, m["c2"], 70)
        if m["logo"] is not None:
            lg = m["logo"].resize((560, int(560 * m["logo"].height / m["logo"].width)), Image.LANCZOS)
            place(c, lg, 620, 540, scale=eb(pr(t, .1, .5)), rot=math.sin(t * 2) * 2)
        if pregunta: etiqueta(c, pregunta, 1300, 470, (255, 255, 255), size=52, alpha=eo(pr(t, .5, .4)), borde=m["c1"])
        etiqueta(c, m["cta"], 1300, 600, (20, 18, 34), bg=(255, 255, 255), size=46, alpha=eo(pr(t, .9, .4)))
        if m.get("disclaimer"): etiqueta(c, m["disclaimer"], W / 2, H - 60, (255, 255, 255), size=30)
        return camera(c, t, d, 1.0, 1.05)
    glow(c, W / 2, 820, 420, m["c1"], 90); glow(c, W / 2, 1300, 300, m["c2"], 70)
    if m["logo"] is not None:
        lg = m["logo"].resize((620, int(620 * m["logo"].height / m["logo"].width)), Image.LANCZOS)
        place(c, lg, W / 2, 860, scale=eb(pr(t, .1, .5)), rot=math.sin(t * 2) * 2)
    if pregunta: etiqueta(c, pregunta, W / 2, 1320, (255, 255, 255), size=52, alpha=eo(pr(t, .5, .4)), borde=m["c1"])
    etiqueta(c, m["cta"], W / 2, 1480, (20, 18, 34), bg=(255, 255, 255), size=46, alpha=eo(pr(t, .9, .4)))
    if m.get("disclaimer"): etiqueta(c, m["disclaimer"], W / 2, H - 80, (255, 255, 255), size=30)
    return camera(c, t, d, 1.0, 1.05)

# ================================================================ PAQUETE TERROR / NOCHE
def vineta(c, fuerza=.75, col=(0, 0, 0)):
    m = Image.new("L", (W, H), 0); ImageDraw.Draw(m).ellipse((-W * .25, -H * .1, W * 1.25, H * 1.1), fill=255)
    m = m.filter(ImageFilter.GaussianBlur(220)).point(lambda v: int((255 - v) * fuerza))
    L = Image.new("RGBA", (W, H), tuple(col) + (255,)); L.putalpha(m); c.alpha_composite(L)

def niebla(c, t, y=1400, col=(150, 160, 200), a=70):
    L = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    for i in range(7):
        x = (i * 260 + t * 40 * (1 + i % 3)) % (W + 600) - 300
        d.ellipse((x - 260, y - 70 + i * 18, x + 260, y + 70 + i * 18), fill=tuple(col) + (a,))
    c.alpha_composite(L.filter(ImageFilter.GaussianBlur(40)))

@lru_cache(maxsize=4)
def noche_casa():
    c = vgrad(W, H, [(0, (6, 8, 22)), (.6, (22, 24, 52)), (1, (8, 8, 16))]); rnd = random.Random(3); h = Hi()
    for _ in range(90):
        x, y, r = rnd.uniform(0, W), rnd.uniform(0, H * .55), rnd.uniform(1, 3); h.ellipse((x - r, y - r, x + r, y + r), fill=(230, 230, 255, rnd.randint(90, 230)))
    c.alpha_composite(h.done())
    glow(c, 820, 500, 190, (200, 210, 255), 90); h = Hi(); h.ellipse((740, 420, 900, 580), fill=(236, 236, 220))
    h.ellipse((780, 455, 815, 490), fill=(214, 214, 200)); h.ellipse((845, 520, 872, 547), fill=(214, 214, 200))
    # casa
    h.poly([(170, 1500), (170, 900), (520, 620), (870, 900), (870, 1500)], fill=(18, 16, 28))
    h.rect((640, 640, 720, 820), fill=(18, 16, 28))
    for (x, y) in ((260, 1000), (620, 1000), (260, 1220), (620, 1220)):
        h.rect((x, y, x + 140, y + 150), fill=(30, 26, 40))
    h.rect((450, 1260, 590, 1500), fill=(28, 22, 34))
    h.rect((0, 1500, W, H), fill=(10, 10, 16))
    c.alpha_composite(h.done())
    glow(c, 690, 1075, 110, (255, 190, 90), 140); h = Hi(); h.rect((620, 1000, 760, 1150), fill=(255, 196, 110)); h.line([(690, 1000), (690, 1150)], fill=(30, 26, 40), width=8); h.line([(620, 1075), (760, 1075)], fill=(30, 26, 40), width=8)
    # árbol seco
    for (p, w) in [([(80, 1500), (110, 1100), (60, 900)], 26), ([(110, 1100), (220, 980)], 14), ([(95, 1250), (20, 1150)], 12), ([(60, 900), (20, 820)], 10), ([(60, 900), (130, 800)], 10)]:
        h.line(p, fill=(8, 8, 12), width=w)
    c.alpha_composite(h.done()); return c

def ojo_grande(c, x, y, ancho, apertura=1., pupila=(0, 0), mirada_film=True, t=0):
    """Ojo enorme estilo 'ojo de buitre': azul pálido con velo."""
    h = Hi(); a = max(.02, apertura); ww = ancho; hh = ancho * .48 * a
    h.ellipse((x - ww / 2 - 40, y - hh / 2 - 60, x + ww / 2 + 40, y + hh / 2 + 60), fill=(150, 110, 100))
    h.ellipse((x - ww / 2, y - hh / 2, x + ww / 2, y + hh / 2), fill=(236, 230, 222))
    c.alpha_composite(h.done())
    if a > .15:
        m = Image.new("L", (W, H), 0); ImageDraw.Draw(m).ellipse((x - ww / 2, y - hh / 2, x + ww / 2, y + hh / 2), fill=255)
        I = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(I); r = ancho * .2
        px, py = x + pupila[0], y + pupila[1]
        d.ellipse((px - r, py - r, px + r, py + r), fill=(150, 185, 210)); d.ellipse((px - r * .45, py - r * .45, px + r * .45, py + r * .45), fill=(30, 40, 50))
        if mirada_film:
            d.ellipse((px - r * 1.02, py - r * 1.02, px + r * 1.02, py + r * 1.02), fill=(220, 230, 236, 120))
        d.ellipse((px + r * .2, py - r * .6, px + r * .5, py - r * .3), fill=(255, 255, 255, 220))
        I.putalpha(Image.composite(I.getchannel("A"), Image.new("L", (W, H), 0), m)); c.alpha_composite(I)
    h = Hi(); h.arc((x - ww / 2, y - hh / 2, x + ww / 2, y + hh / 2), 180, 360, fill=(40, 24, 24), width=10)
    if a <= .15: h.line([(x - ww / 2, y), (x + ww / 2, y)], fill=(40, 24, 24), width=12)
    for i in range(9):
        ang = math.pi + i * math.pi / 8; h.line([(x + ww / 2 * math.cos(ang), y + hh / 2 * math.sin(ang)), (x + (ww / 2 + 30) * math.cos(ang), y + (hh / 2 + 34) * math.sin(ang) - 6)], fill=(40, 24, 24), width=6)
    c.alpha_composite(h.done())

def haz_linterna(c, x, y, ang, largo=1200, abertura=9, a=110, col=(255, 220, 140)):
    cono(c, x, y, ang, largo, abertura, col, a); glow(c, x, y, 40, col, 230, 20)

@lru_cache(maxsize=4)
def cuarto_oscuro():
    c = vgrad(W, H, [(0, (14, 10, 18)), (1, (6, 4, 8))]); h = Hi()
    h.rect((0, 1350, W, H), fill=(26, 18, 16))
    for i in range(10): h.line([(i * 120 - 60, H), (W / 2 + (i - 5) * 30, 1350)], fill=(36, 24, 20), width=4)
    h.rect((520, 900, 1020, 1240), r=20, fill=(30, 22, 30)); h.rect((500, 1180, 1040, 1400), r=20, fill=(40, 30, 40))
    h.rect((540, 1150, 720, 1210), r=30, fill=(70, 64, 76)); h.rect((560, 1240, 1020, 1300), fill=(30, 22, 30))
    c.alpha_composite(h.done()); return c

def tablas(c, t, levantar=0., x0=0, y0=1150, n=7, alto=110):
    h = Hi(); cols = [(92, 60, 40), (102, 66, 44), (86, 56, 36)]
    for i in range(n):
        y = y0 + i * alto; dy = -levantar * 220 if i == 3 else 0; rot = levantar * 12 if i == 3 else 0
        h.rect((x0 - 20, y + dy, W + 20, y + alto - 8 + dy), r=8, fill=cols[i % 3])
        for k in range(3): h.line([(80 + k * 320 + (i * 60) % 200, y + 20 + dy), (240 + k * 320 + (i * 60) % 200, y + 30 + dy)], fill=(70, 44, 30), width=3)
        for xx in (60, W - 60): h.ellipse((xx - 7, y + alto / 2 - 7 + dy, xx + 7, y + alto / 2 + 7 + dy), fill=(40, 30, 26))
    c.alpha_composite(h.done())

def reloj(c, x, y, r, horas=12, minutos=0):
    h = Hi(); h.ellipse((x - r - 14, y - r - 14, x + r + 14, y + r + 14), fill=(60, 44, 30)); h.ellipse((x - r, y - r, x + r, y + r), fill=(236, 226, 200))
    for i in range(12):
        a = i * math.pi / 6; h.line([(x + math.sin(a) * r * .82, y - math.cos(a) * r * .82), (x + math.sin(a) * r * .95, y - math.cos(a) * r * .95)], fill=(40, 30, 20), width=6)
    ah = (horas % 12 + minutos / 60) * math.pi / 6; am = minutos * math.pi / 30
    h.line([(x, y), (x + math.sin(ah) * r * .5, y - math.cos(ah) * r * .5)], fill=(30, 20, 14), width=14)
    h.line([(x, y), (x + math.sin(am) * r * .78, y - math.cos(am) * r * .78)], fill=(30, 20, 14), width=8)
    h.ellipse((x - 14, y - 14, x + 14, y + 14), fill=(30, 20, 14)); c.alpha_composite(h.done())

@lru_cache(maxsize=4)
def libro_antiguo(titulo="", sub=""):
    h = Hi(900, 620); h.rect((20, 40, 880, 600), r=24, fill=(70, 36, 24)); h.rect((40, 20, 860, 580), r=18, fill=(236, 222, 186))
    h.line([(450, 20), (450, 580)], fill=(170, 150, 120), width=6)
    for y in range(120, 560, 40):
        h.line([(500, y), (820, y)], fill=(170, 150, 120), width=3)
    im = h.done(); d = ImageDraw.Draw(im)
    if titulo:
        f = F(54); ws = titulo.split(); lines = [titulo] if d.textlength(titulo, font=f) < 360 else [" ".join(ws[:len(ws) // 2 + len(ws) % 2]), " ".join(ws[len(ws) // 2 + len(ws) % 2:])]
        for i, ln in enumerate(lines): d.text((245, 230 + i * 70), ln, font=f, fill=(60, 30, 20), anchor="mm")
        if sub: d.text((245, 420), sub, font=F(40), fill=(120, 60, 40), anchor="mm")
    return im

def pulso(c, t, bpm=70, col=(200, 20, 30), fuerza=1.):
    """Viñeta roja que late."""
    ph = (t * bpm / 60) % 1; k = max(0, 1 - ph * 5) + .6 * max(0, 1 - abs(ph - .25) * 6)
    vineta(c, .35 + .45 * k * fuerza, col)
    return k


# ================================================================ FORMATO HORIZONTAL (YouTube 1920x1080)
HW, HH = 1920, 1080
_MASK = None
def horizontal(fr, fit=False, y0=420):
    """Convierte un cuadro vertical 1080x1920 en 1920x1080: la franja central va al centro y los lados se
    rellenan con la misma escena ampliada, difuminada y oscurecida (fundido suave en los bordes)."""
    global _MASK
    fr = fr.convert("RGBA")
    if fit:
        band = fr.resize((int(1080 * 1080 / 1920), 1080), Image.LANCZOS); bx = (HW - band.width) // 2
    else:
        band = fr.crop((0, y0, 1080, y0 + 1080)); bx = (HW - 1080) // 2
    bg = band.resize((HW, int(band.height * HW / band.width)), Image.BILINEAR)
    bg = bg.crop((0, (bg.height - HH) // 2, HW, (bg.height - HH) // 2 + HH)).filter(ImageFilter.GaussianBlur(28))
    bg = Image.blend(Image.new("RGBA", (HW, HH), (0, 0, 0, 255)), bg, .38)
    if _MASK is None or _MASK.size != band.size:
        m = Image.new("L", band.size, 255); d = ImageDraw.Draw(m)
        for i in range(90): v = int(255 * i / 90); d.line([(i, 0), (i, band.height)], fill=v); d.line([(band.width - 1 - i, 0), (band.width - 1 - i, band.height)], fill=v)
        _MASK = m
    bg.paste(band, (bx, 0), _MASK); return bg
