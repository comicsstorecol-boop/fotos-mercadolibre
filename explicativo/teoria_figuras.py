"""Comics Store · Teorías con FIGURAS REALES de la tienda + animaciones (estilo dinámico).
Las figuras son fotos de Fernando (recortadas). Todo lo demás se dibuja en código: sin personajes dibujados."""
import os, sys, math, random
from functools import lru_cache
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops
import numpy as np
import lib
from lib import W, H, F, eo, eio, eb, pr, mix, clamp
import motor

HZ = lib.HORIZONTAL
FIG_DIR = os.environ.get("FIG_DIR", "/home/claude/strange/fig2")
KIT = os.path.dirname(HERE)
VERDE = (60, 255, 120); NARANJA = (255, 150, 40); MORADO = (150, 90, 255); ROJO = (255, 60, 70); AZUL = (80, 150, 255); ORO = (255, 200, 70)

def P(v, h):  # elige coordenadas según formato
    return h if HZ else v

# ------------------------------------------------------------------ utilidades rápidas
@lru_cache(maxsize=64)
def _glow_sprite(r, col, a):
    s = int(r * 2.6); L = Image.new("RGBA", (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    c = s / 2; d.ellipse((c - r, c - r, c + r, c + r), fill=tuple(col) + (a,))
    return L.filter(ImageFilter.GaussianBlur(r * .55))

def glow(c, x, y, r, col, a=150):
    r = max(4, int(r)); sp = _glow_sprite(r, tuple(col), int(a)); c.alpha_composite(sp, (int(x - sp.width / 2), int(y - sp.height / 2))) if -sp.width < x < W + sp.width else None

def place(c, img, cx, cy, scale=1., rot=0., alpha=1.):
    if alpha <= .01 or scale <= .01: return
    L = img
    if abs(scale - 1) > .002: L = L.resize((max(1, int(L.width * scale)), max(1, int(L.height * scale))), Image.BILINEAR)
    if rot: L = L.rotate(rot, resample=Image.BICUBIC, expand=True)
    if alpha < .99: L = L.copy(); L.putalpha(L.getchannel("A").point(lambda v: int(v * alpha)))
    x, y = int(cx - L.width / 2), int(cy - L.height / 2)
    if x > W or y > H or x + L.width < 0 or y + L.height < 0: return
    c.alpha_composite(L, (x, y)) if x >= 0 and y >= 0 and x + L.width <= W and y + L.height <= H else _paste_clip(c, L, x, y)

def _paste_clip(c, L, x, y):
    x0, y0 = max(0, -x), max(0, -y); x1, y1 = min(L.width, W - x), min(L.height, H - y)
    if x1 <= x0 or y1 <= y0: return
    c.alpha_composite(L.crop((x0, y0, x1, y1)), (x + x0, y + y0))

def texto(c, txt, x, y, size, col=(255, 255, 255), alpha=1., stroke=6, anchor="mm", glow_col=None):
    f = F(size); d0 = ImageDraw.Draw(Image.new("RGBA", (1, 1))); bb = d0.textbbox((0, 0), txt, font=f, stroke_width=stroke)
    L = Image.new("RGBA", (bb[2] - bb[0] + 60, bb[3] - bb[1] + 60), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    if glow_col:
        G_ = Image.new("RGBA", L.size, (0, 0, 0, 0)); ImageDraw.Draw(G_).text((30 - bb[0], 30 - bb[1]), txt, font=f, fill=tuple(glow_col) + (255,), stroke_width=stroke + 6, stroke_fill=tuple(glow_col) + (255,))
        L.alpha_composite(G_.filter(ImageFilter.GaussianBlur(12)))
    d.text((30 - bb[0], 30 - bb[1]), txt, font=f, fill=tuple(col) + (255,), stroke_width=stroke, stroke_fill=(8, 6, 16, 255))
    ox = {"mm": L.width / 2, "lm": 30, "rm": L.width - 30}[anchor]
    place(c, L, x - ox + L.width / 2, y, alpha=alpha)

def chip(c, txt, x, y, col=VERDE, size=44, alpha=1., fondo=(12, 10, 26)):
    if HZ and y > 860: y = 105   # en horizontal los subtítulos van abajo: chips arriba
    f = F(size); w = ImageDraw.Draw(Image.new("RGBA", (1, 1))).textlength(txt, font=f)
    L = Image.new("RGBA", (int(w + size * 1.4), int(size * 1.9)), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rounded_rectangle((3, 3, L.width - 4, L.height - 4), L.height // 2, fill=tuple(fondo) + (230,), outline=tuple(col) + (255,), width=4)
    d.text((L.width / 2, L.height / 2), txt, font=f, fill=tuple(col) + (255,), anchor="mm")
    glow(c, x, y, L.width * .45, col, int(60 * alpha)); place(c, L, x, y, scale=.85 + .15 * eb(min(1, alpha * 1.2)), alpha=alpha)

def flash(c, t, dur=.18, col=(255, 255, 255), fuerza=180):
    if t < dur:
        c.alpha_composite(Image.new("RGBA", (W, H), tuple(col) + (int(fuerza * (1 - t / dur)),)))

def shake(img, t, fuerza=14, dur=.45):
    if t > dur: return img
    k = (1 - t / dur) * fuerza; dx = int(math.sin(t * 90) * k); dy = int(math.cos(t * 73) * k)
    return ImageChops.offset(img, dx, dy)

def glitch(img, t, dur=.35, fuerza=18):
    if t > dur: return img
    k = int((1 - t / dur) * fuerza); r, g, b, a = img.split()
    r = ImageChops.offset(r, k, 0); b = ImageChops.offset(b, -k, 0)
    out = Image.merge("RGBA", (r, g, b, a))
    if int(t * 30) % 2 == 0:
        y = random.Random(int(t * 30)).randint(0, H - 120); band = out.crop((0, y, W, y + 90)); out.paste(ImageChops.offset(band, k * 3, 0), (0, y))
    return out

def zoom(img, t, d, z0=1.0, z1=1.1, dx=0, dy=0):
    return lib.camera(img, t, d, z0, z1, dx, dy)

def vineta(c, fuerza=170):
    v = _vineta_cache(fuerza); c.alpha_composite(v)

@lru_cache(maxsize=4)
def _vineta_cache(fuerza):
    m = Image.new("L", (W // 4, H // 4), 0); ImageDraw.Draw(m).ellipse((-W * .08, -H * .05, W * .33, H * .3), fill=255)
    m = m.filter(ImageFilter.GaussianBlur(min(W, H) // 10)).resize((W, H), Image.BILINEAR).point(lambda v: int((255 - v) * fuerza / 255))
    L = Image.new("RGBA", (W, H), (0, 0, 0, 0)); L.putalpha(m); return L

# ------------------------------------------------------------------ fondo cósmico (cacheado + estrellas vivas)
PALETAS = {
    "mistico": [(0, (14, 8, 40)), (.5, (52, 22, 96)), (1, (10, 6, 28))],
    "doom": [(0, (4, 18, 14)), (.55, (14, 60, 40)), (1, (4, 10, 10))],
    "thanos": [(0, (20, 8, 40)), (.5, (70, 30, 90)), (1, (16, 6, 24))],
    "azul": [(0, (6, 12, 40)), (.55, (20, 40, 110)), (1, (6, 8, 24))],
    "rojo": [(0, (30, 4, 10)), (.55, (90, 16, 30)), (1, (16, 4, 8))],
}
NEB = {"mistico": [MORADO, NARANJA, AZUL], "doom": [VERDE, (20, 120, 90), (40, 200, 160)], "thanos": [MORADO, ORO, (200, 60, 160)],
       "azul": [AZUL, (120, 200, 255), MORADO], "rojo": [ROJO, NARANJA, MORADO]}

@lru_cache(maxsize=8)
def _base(pal):
    bw, bh = int(W * 1.25), int(H * 1.25)
    c = lib.vgrad(bw, bh, PALETAS[pal]).copy(); rng = random.Random(hash(pal) % 999)
    lay = Image.new("RGBA", (bw // 4, bh // 4), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for i in range(9):
        col = NEB[pal][i % 3]; x, y, r = rng.uniform(0, bw / 4), rng.uniform(0, bh / 4), rng.uniform(40, 130)
        d.ellipse((x - r, y - r * .7, x + r, y + r * .7), fill=col + (rng.randint(30, 70),))
    c.alpha_composite(lay.filter(ImageFilter.GaussianBlur(40)).resize((bw, bh), Image.BILINEAR))
    d = ImageDraw.Draw(c)
    for i in range(500):
        x, y = rng.uniform(0, bw), rng.uniform(0, bh); s = rng.choice([1, 1, 1, 2]); a = rng.randint(60, 200)
        d.ellipse((x - s, y - s, x + s, y + s), fill=(255, 255, 255, a))
    return c

STARS = [(random.Random(i).uniform(0, 1), random.Random(i + 99).uniform(0, 1), random.Random(i + 7).uniform(0, 6.3), random.Random(i + 3).uniform(1.5, 3.5)) for i in range(60)]

def cosmos(t, pal="mistico", drift=(1, -.5), velocidad=1.):
    b = _base(pal); mx, my = b.width - W, b.height - H
    ox = mx / 2 + math.sin(t * .12 * velocidad) * mx * .45 * drift[0]; oy = my / 2 + math.cos(t * .1 * velocidad) * my * .45 * drift[1]
    c = b.crop((int(ox), int(oy), int(ox) + W, int(oy) + H)).copy(); d = ImageDraw.Draw(c)
    for x, y, ph, s in STARS:
        a = int(140 + 115 * math.sin(t * 3 + ph)); X, Y = x * W, ((y + t * .01 * velocidad) % 1) * H
        d.ellipse((X - s, Y - s, X + s, Y + s), fill=(255, 255, 255, max(0, a)))
    return c

PARTS = [(random.Random(i).uniform(0, 1), random.Random(i + 5).uniform(0, 1), random.Random(i + 9).uniform(.3, 1.2), random.Random(i + 1).uniform(2, 6)) for i in range(45)]
def particulas(c, t, col=NARANJA, sube=True, n=45, a=200):
    d = ImageDraw.Draw(c)
    for x, y, v, s in PARTS[:n]:
        X = x * W + math.sin(t * v * 2 + y * 9) * 30; Y = ((y - t * .08 * v) % 1 if sube else (y + t * .08 * v) % 1) * H
        al = int(a * (.5 + .5 * math.sin(t * 4 * v + x * 20)))
        d.ellipse((X - s, Y - s, X + s, Y + s), fill=tuple(col) + (al,))

# ------------------------------------------------------------------ figuras (fotos de Fernando)
@lru_cache(maxsize=32)
def _fig(nombre, h):
    im = Image.open(os.path.join(FIG_DIR, nombre + ".png")).convert("RGBA")
    return im.resize((int(im.width * h / im.height), h), Image.LANCZOS)

COLOR_FIG = {"doom": VERDE, "strange": (255, 165, 40), "thanos": (180, 90, 255), "iron": ORO, "cap": (70, 140, 255), "loki": (170, 255, 60),
             "thor": (120, 200, 255), "wolverine": (255, 220, 40), "magneto": (235, 60, 200), "xavier": (170, 120, 255), "reed": (60, 210, 255),
             "cuatro": (60, 210, 255), "cosa": (255, 140, 40), "hulk": (110, 255, 70), "wanda": (255, 50, 90)}
def color_de(nombre, defecto=VERDE):
    return COLOR_FIG.get(nombre.split("_")[0], defecto)

@lru_cache(maxsize=32)
def _neon(nombre, h, flip=False):
    """Figura recortada con contorno neón del color del personaje (sigue la silueta, sin marco)."""
    from scipy import ndimage
    col = color_de(nombre); im = _fig(nombre, h)
    if flip: im = im.transpose(Image.FLIP_LEFT_RIGHT)
    pad = max(20, int(h * .05)); A = Image.new("L", (im.width + 2 * pad, im.height + 2 * pad), 0); A.paste(im.getchannel("A"), (pad, pad))
    lleno = Image.fromarray((ndimage.binary_fill_holes(np.array(A) > 110) * 255).astype("uint8"))
    g = max(9, int(h * .011) | 1)
    borde = ImageChops.subtract(lleno.filter(ImageFilter.MaxFilter(g)), lleno.filter(ImageFilter.MinFilter(3)))
    C = Image.new("RGBA", A.size, (0, 0, 0, 0))
    for r, m in ((pad * .5, 3.), (pad * .25, 3.5), (pad * .1, 3.)):
        L = Image.new("RGBA", A.size, col + (0,)); L.putalpha(borde.filter(ImageFilter.GaussianBlur(r)).point(lambda v: min(255, int(v * m)))); C.alpha_composite(L)
    L = Image.new("RGBA", A.size, mix(col, (255, 255, 255), .55) + (0,)); L.putalpha(borde.filter(ImageFilter.MinFilter(5)).filter(ImageFilter.GaussianBlur(1.2))); C.alpha_composite(L)
    C.alpha_composite(im, (pad, pad)); return C

def figura(c, nombre, x, pie, h, t, entra="pop", col=VERDE, flota=True, retraso=0., alpha=1., flip=False, reflejo=True):
    """Pone la figura con entrada animada, aura del color del tema, flotación suave y reflejo en el piso."""
    h = int(h); k = eo(pr(t, retraso, .55)); im = _fig(nombre, h); col = color_de(nombre, col)
    if flip: im = im.transpose(Image.FLIP_LEFT_RIGHT)
    dx = dy = 0; sc = 1.
    if entra == "pop": sc = .6 + .4 * eb(pr(t, retraso, .5))
    elif entra == "izq": dx = -(1 - k) * W * .7
    elif entra == "der": dx = (1 - k) * W * .7
    elif entra == "sube": dy = (1 - k) * H * .5
    elif entra == "baja": dy = -(1 - k) * H * .5
    b = math.sin(t * 1.6 + x) * 10 if flota else 0
    cx, cy = x + dx, pie - h / 2 * sc + dy + b
    a = alpha * clamp(k * 1.5)
    if a <= 0: return
    glow(c, cx, cy + h * .05, h * .42, col, int(70 * a))
    if reflejo:   # sombra-elipse en el piso
        sh = Image.new("RGBA", (int(h * .7), 60), (0, 0, 0, 0)); ImageDraw.Draw(sh).ellipse((0, 0, sh.width, 60), fill=(0, 0, 0, 150))
        place(c, sh.filter(ImageFilter.GaussianBlur(14)), cx, pie + dy + 10, alpha=a * (1 - abs(b) / 40))
        glow(c, cx, pie + dy + 6, h * .22, col, int(60 * a))
    place(c, _neon(nombre, h, flip), cx, cy, sc, alpha=a)

# ------------------------------------------------------------------ gráficos animados
@lru_cache(maxsize=8)
def _anillo(r, col, runas=True):
    s = int(r * 2 + 40); L = Image.new("RGBA", (s * 2, s * 2), (0, 0, 0, 0)); d = ImageDraw.Draw(L); c = s; R = r * 2
    for rr, w in ((R, 6), (R * .86, 3), (R * .62, 4)): d.ellipse((c - rr, c - rr, c + rr, c + rr), outline=tuple(col) + (255,), width=w)
    for i in range(72):
        a = math.radians(i * 5); l = 22 if i % 6 == 0 else 10
        d.line([(c + math.cos(a) * (R - 4), c + math.sin(a) * (R - 4)), (c + math.cos(a) * (R - 4 - l), c + math.sin(a) * (R - 4 - l))], fill=tuple(col) + (255,), width=3)
    if runas:
        for i in range(12):
            a = math.radians(i * 30 + 15); x, y = c + math.cos(a) * R * .74, c + math.sin(a) * R * .74
            pts = [(x + math.cos(a + k * 2.1) * 16, y + math.sin(a + k * 2.1) * 16) for k in range(3)]; d.polygon(pts, outline=tuple(col) + (255,))
    pts = [(c + math.cos(math.radians(90 * k + 45)) * R * .62, c + math.sin(math.radians(90 * k + 45)) * R * .62) for k in range(4)]
    d.polygon(pts, outline=tuple(col) + (255,)); d.polygon([(p[1] - c + c, c - (p[0] - c)) for p in pts], outline=tuple(col) + (255,))
    L = L.resize((s, s), Image.LANCZOS)
    G_ = L.filter(ImageFilter.GaussianBlur(8)); out = Image.new("RGBA", L.size, (0, 0, 0, 0)); out.alpha_composite(G_); out.alpha_composite(G_); out.alpha_composite(L); return out

def mandala(c, x, y, r, t, col=NARANJA, alpha=1., retraso=0.):
    k = eb(pr(t, retraso, .6));
    if k <= 0: return
    a = _anillo(int(r), tuple(col)); place(c, a, x, y, scale=k * (1 + .03 * math.sin(t * 5)), rot=t * 40, alpha=alpha * clamp(k))
    place(c, _anillo(int(r * .55), tuple(col), False), x, y, scale=k, rot=-t * 70, alpha=alpha * .9 * clamp(k))

def hilos(c, x, y, t, col=VERDE, n=34, largo=None, abanico=(200, 340), a=200, seed=3):
    """Hilos del tiempo: líneas curvas que salen de un punto con chispas que viajan."""
    rng = random.Random(seed); largo = largo or max(W, H); L = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L); grow = eo(pr(t, 0, 1.2))
    dots = []
    for i in range(n):
        ang = math.radians(rng.uniform(*abanico)); curva = rng.uniform(-.5, .5); ln = largo * rng.uniform(.6, 1.1) * grow
        pts = []
        for s in range(0, 21):
            u = s / 20; aa = ang + curva * u; pts.append((x + math.cos(aa) * ln * u, y + math.sin(aa) * ln * u))
        d.line(pts, fill=tuple(col) + (int(a * .55),), width=2)
        u = (t * rng.uniform(.25, .6) + rng.random()) % 1; idx = int(u * 20); dots.append(pts[idx])
    G_ = L.resize((W // 3, H // 3), Image.BILINEAR).filter(ImageFilter.GaussianBlur(2)).resize((W, H), Image.BILINEAR); c.alpha_composite(G_); c.alpha_composite(L); d = ImageDraw.Draw(c)
    for px, py in dots: d.ellipse((px - 5, py - 5, px + 5, py + 5), fill=(255, 255, 255, 230)); glow(c, px, py, 14, col, 160)

def contador_futuros(c, t, x, y, valor=14000605, size=None, col=VERDE, etiqueta="FUTUROS", start=.15, dur=1.6):
    size = size or P(118, 130); v = int(valor * eo(pr(t, start, dur)))
    if pr(t, start, dur) >= 1: v = valor
    txt = f"{v:,}".replace(",", ".")
    f = F(size); w = ImageDraw.Draw(Image.new("RGBA", (1, 1))).textlength("14.000.605", font=f); fe = F(int(size * .3))
    L = Image.new("RGBA", (int(w + size * 2.6), int(size * 1.9)), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rounded_rectangle((4, 4, L.width - 5, L.height - 5), L.height // 2, fill=(10, 14, 22, 225), outline=tuple(col) + (255,), width=5)
    d.text((size * .55, L.height / 2), txt, font=f, fill=(255, 255, 255, 255), anchor="lm")
    d.text((L.width - size * .45, L.height / 2 + size * .2), etiqueta.lower(), font=fe, fill=tuple(col) + (255,), anchor="rm")
    glow(c, x, y, L.width * .45, col, 90); place(c, L, x, y, scale=.7 + .3 * eb(pr(t, 0, .45)) + .04 * eb(pr(t, start + dur, .3)) * (1 - pr(t, start + dur + .3, .3)))

def gema(c, x, y, r, t, col=VERDE):
    glow(c, x, y, r * 2.2, col, 120 + int(40 * math.sin(t * 4)))
    L = Image.new("RGBA", (int(r * 2.4), int(r * 2.4)), (0, 0, 0, 0)); d = ImageDraw.Draw(L); m = L.width / 2
    d.ellipse((m - r, m - r * .62, m + r, m + r * .62), fill=(20, 60, 30, 255), outline=tuple(col) + (255,), width=6)
    pr_ = r * .42 * (1 + .1 * math.sin(t * 6)); d.ellipse((m - pr_, m - pr_, m + pr_, m + pr_), fill=tuple(col) + (255,))
    d.ellipse((m - pr_ * .4, m - pr_ * .4, m + pr_ * .4, m + pr_ * .4), fill=(10, 30, 15, 255))
    d.ellipse((m - pr_ * .6, m - pr_ * .75, m - pr_ * .2, m - pr_ * .35), fill=(255, 255, 255, 220))
    place(c, L, x, y, scale=.5 + .5 * eb(pr(t, 0, .5)))

def _iso(cx, cy, s, i, j): return (cx + (i - j) * s, cy + (i + j) * s * .55)

def ajedrez(c, t, cx, cy, s, piezas, c1=(120, 100, 220), c2=(60, 44, 130), n=6, alpha=1.):
    """Tablero isométrico. piezas: [(tipo, color, (i0,j0), (i1,j1), t_mov)]"""
    k = eo(pr(t, 0, .6)); d = ImageDraw.Draw(c); oy = (1 - k) * 200
    top = _iso(cx, cy + oy, s, 0, 0); r_ = _iso(cx, cy + oy, s, n, 0); b_ = _iso(cx, cy + oy, s, n, n); l_ = _iso(cx, cy + oy, s, 0, n)
    d.polygon([l_, b_, (b_[0], b_[1] + s * .5), (l_[0], l_[1] + s * .5)], fill=(30, 22, 70, 255)); d.polygon([b_, r_, (r_[0], r_[1] + s * .5), (b_[0], b_[1] + s * .5)], fill=(20, 14, 50, 255))
    for i in range(n):
        for j in range(n):
            p = [_iso(cx, cy + oy, s, i, j), _iso(cx, cy + oy, s, i + 1, j), _iso(cx, cy + oy, s, i + 1, j + 1), _iso(cx, cy + oy, s, i, j + 1)]
            d.polygon(p, fill=(c1 if (i + j) % 2 == 0 else c2) + (255,))
    orden = sorted(piezas, key=lambda p: sum(p[2]))
    for tipo, col, a0, a1, tm in orden:
        u = eio(pr(t, tm, .6)); i = a0[0] + (a1[0] - a0[0]) * u + .5; j = a0[1] + (a1[1] - a0[1]) * u + .5
        px, py = _iso(cx, cy + oy, s, i, j); salto = math.sin(u * math.pi) * s * .8
        pieza(c, tipo, px, py - salto, s * .9, col)

def pieza(c, tipo, x, y, s, col):
    d = ImageDraw.Draw(c); osc = mix(col, (0, 0, 0), .45)
    d.ellipse((x - s * .45, y - s * .18, x + s * .45, y + s * .18), fill=osc + (255,))
    hgt = {"peon": 1.1, "rey": 1.9, "reina": 1.7, "torre": 1.3}[tipo]
    d.polygon([(x - s * .38, y), (x + s * .38, y), (x + s * .2, y - s * hgt * .7), (x - s * .2, y - s * hgt * .7)], fill=col + (255,))
    d.ellipse((x - s * .26, y - s * hgt - s * .1, x + s * .26, y - s * hgt * .62), fill=col + (255,))
    if tipo == "rey": d.rectangle((x - s * .05, y - s * hgt - s * .45, x + s * .05, y - s * hgt - s * .05), fill=col + (255,)); d.rectangle((x - s * .17, y - s * hgt - s * .33, x + s * .17, y - s * hgt - s * .23), fill=col + (255,))
    if tipo == "reina":
        for q in (-1, 0, 1): d.ellipse((x + q * s * .18 - s * .07, y - s * hgt - s * .3, x + q * s * .18 + s * .07, y - s * hgt - s * .16), fill=col + (255,))
    d.ellipse((x - s * .2, y - s * hgt * .55, x - s * .06, y - s * hgt * .3), fill=(255, 255, 255, 90))

def dominos(c, t, x0, y0, n=9, paso=None, col=(240, 240, 248), retraso=.2, vel=.16):
    paso = paso or P(95, 110); d = ImageDraw.Draw(c)
    for i in range(n):
        u = eio(pr(t, retraso + i * vel, .25)); ang = u * 72
        x = x0 + i * paso; w, h = P(34, 40), P(110, 125)
        L = Image.new("RGBA", (w + 8, h + 8), (0, 0, 0, 0)); dd = ImageDraw.Draw(L)
        dd.rounded_rectangle((4, 4, w + 4, h + 4), 8, fill=col + (255,), outline=(40, 40, 60, 255), width=3); dd.line([(8, h / 2 + 4), (w, h / 2 + 4)], fill=(40, 40, 60, 255), width=3)
        for yy in (h * .25, h * .75): dd.ellipse((w / 2 - 1, yy - 1, w / 2 + 9, yy + 9), fill=(30, 30, 40, 255))
        Lr = L.rotate(-ang, resample=Image.BICUBIC, expand=True)
        c.alpha_composite(Lr, (int(x - Lr.width / 2 + math.sin(math.radians(ang)) * h / 2), int(y0 - Lr.height + 4)))
        if 0 < pr(t, retraso + i * vel + .2, .2) < 1: glow(c, x + h * .6, y0, 40, ORO, 120)

@lru_cache(maxsize=2)
def _textura_parches(r):
    rng = random.Random(7); w, h = r * 4, r * 2; L = Image.new("RGBA", (w, h)); px = L.load()
    cols = [(70, 90, 200), (190, 60, 110), (60, 170, 120), (220, 150, 60), (120, 70, 190), (40, 140, 190), (200, 200, 80), (160, 60, 60)]
    seeds = [(rng.uniform(0, w), rng.uniform(0, h), rng.choice(cols)) for _ in range(26)]
    small = Image.new("RGB", (w // 4, h // 4)); sp = small.load()
    for yy in range(h // 4):
        for xx in range(w // 4):
            X, Y = xx * 4, yy * 4; best = None; bd = 1e18; sec = 1e18
            for sx, sy, cc in seeds:
                dx = min(abs(X - sx), w - abs(X - sx)); dd = dx * dx + (Y - sy) ** 2
                if dd < bd: sec = bd; bd = dd; best = cc
                elif dd < sec: sec = dd
            sp[xx, yy] = (120, 255, 160) if math.sqrt(sec) - math.sqrt(bd) < 7 else best
    return small.resize((w, h), Image.NEAREST).convert("RGBA")

def planeta(c, x, y, r, t, col=VERDE, alpha=1.):
    r = int(r); tex = _textura_parches(r); off = int(t * 40) % tex.width
    strip = Image.new("RGBA", (r * 2, r * 2)); strip.paste(tex.crop((off, 0, min(tex.width, off + r * 2), r * 2)), (0, 0))
    if off + r * 2 > tex.width: strip.paste(tex.crop((0, 0, off + r * 2 - tex.width, r * 2)), (tex.width - off, 0))
    m = Image.new("L", (r * 2, r * 2), 0); ImageDraw.Draw(m).ellipse((0, 0, r * 2 - 1, r * 2 - 1), fill=255)
    sh = Image.new("RGBA", (r * 2, r * 2), (0, 0, 0, 0)); ImageDraw.Draw(sh).ellipse((r * .5, -r * .3, r * 2.6, r * 1.9), fill=(0, 0, 0, 0));
    shade = Image.radial_gradient("L").resize((r * 3, r * 3)).crop((r * .2, r * .2, r * 2.2, r * 2.2)).point(lambda v: int(min(200, v * .9)))
    strip.alpha_composite(Image.merge("RGBA", (Image.new("L", strip.size, 0),) * 3 + (shade,)))
    strip.putalpha(m); k = eb(pr(t, 0, .6))
    glow(c, x, y, r * 1.25, col, int(110 * alpha)); place(c, strip, x, y, scale=k, alpha=alpha)
    ImageDraw.Draw(c).ellipse((x - r * k, y - r * k, x + r * k, y + r * k), outline=tuple(col) + (int(220 * alpha),), width=4)

def comic(c, x, y, t, titulo="SECRET WARS", sub="2015", num="#1", col=VERDE, ancho=None, rot0=-8):
    ancho = int(ancho or P(520, 440)); alto = int(ancho * 1.45); L = Image.new("RGBA", (ancho, alto), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rectangle((0, 0, ancho - 1, alto - 1), fill=(245, 240, 225, 255)); d.rectangle((14, 14, ancho - 15, alto - 15), fill=(40, 20, 80, 255))
    for yy in range(int(alto * .3), alto - 20, 22):
        for xx in range(20, ancho - 20, 22): rr = 2 + 5 * (yy / alto); d.ellipse((xx - rr, yy - rr, xx + rr, yy + rr), fill=(90, 50, 150, 255))
    d.rectangle((14, 14, ancho - 15, int(alto * .26)), fill=(255, 220, 40, 255))
    ft = F(int(ancho * .15)); d.text((ancho / 2, alto * .13), titulo, font=ft, fill=(210, 20, 40, 255), anchor="mm", stroke_width=3, stroke_fill=(60, 0, 10, 255))
    cx, cy, rr = ancho / 2, alto * .6, ancho * .3
    for i, cc in enumerate([(70, 90, 200), (190, 60, 110), (60, 170, 120), (220, 150, 60)]): d.pieslice((cx - rr, cy - rr, cx + rr, cy + rr), i * 90 + 20, i * 90 + 110, fill=cc + (255,))
    d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), outline=tuple(col) + (255,), width=6)
    d.rectangle((24, alto - 90, 130, alto - 30), fill=(255, 255, 255, 255)); d.text((77, alto - 60), num, font=F(36), fill=(20, 20, 20, 255), anchor="mm")
    d.text((ancho - 30, alto - 60), sub, font=F(40), fill=(255, 255, 255, 255), anchor="rm")
    k = eb(pr(t, 0, .6)); glow(c, x, y, ancho * .7, col, 80)
    place(c, L, x, y + (1 - eo(pr(t, 0, .6))) * 300, scale=k * (1 + .02 * math.sin(t * 2)), rot=rot0 * (1 - eo(pr(t, 0, .8))) + math.sin(t * 1.3) * 2)

def linea_tiempo(c, t, items, y=None, col=NARANJA, x0=None, x1=None):
    """items: [(titulo, fecha, color_opcional)] — nodos que se encienden uno a uno."""
    y = y or P(1000, 600); x0 = x0 or P(130, 260); x1 = x1 or P(W - 130, W - 260); n = len(items); d = ImageDraw.Draw(c)
    k = eo(pr(t, .1, 1.2)); d.line([(x0, y), (x0 + (x1 - x0) * k, y)], fill=(255, 255, 255, 120), width=6)
    for i, it in enumerate(items):
        tit, fecha = it[0], it[1]; cc = it[2] if len(it) > 2 else col; x = x0 + (x1 - x0) * i / max(1, n - 1); u = pr(t, .3 + i * .45, .4)
        if u <= 0: continue
        glow(c, x, y, 40, cc, int(180 * u)); d.ellipse((x - 18, y - 18, x + 18, y + 18), fill=cc + (255,), outline=(255, 255, 255, 255), width=4)
        arriba = (i % 2 == 0) if not HZ else True
        sz = P(40, 36)
        for li, part in enumerate(tit.split("\n")): texto(c, part, x, y - (130 if arriba else -110) + li * (sz + 8) - (0 if arriba else 0), sz, alpha=eo(u))
        texto(c, fecha, x, y + (70 if arriba else -60) if not HZ else y + 70, P(36, 32), cc, alpha=eo(u), stroke=4)

def lupa(c, x, y, t, r=None, col=(240, 240, 255)):
    r = r or P(110, 110); d = ImageDraw.Draw(c); dx = math.sin(t * 2) * 30; dy = math.cos(t * 1.6) * 20; k = eb(pr(t, 0, .5)); r *= k
    if r < 5: return
    glow(c, x + dx, y + dy, r * 1.3, col, 50)
    d.ellipse((x + dx - r, y + dy - r, x + dx + r, y + dy + r), outline=col + (255,), width=12)
    a = math.radians(45); d.line([(x + dx + math.cos(a) * r, y + dy + math.sin(a) * r), (x + dx + math.cos(a) * r * 1.9, y + dy + math.sin(a) * r * 1.9)], fill=col + (255,), width=22)

def balsa(c, x, y, t, s=None, col=AZUL, abierta=0.):
    s = s or P(300, 380); L = Image.new("RGBA", (int(s * 2.4), int(s * 1.4)), (0, 0, 0, 0)); d = ImageDraw.Draw(L); w, h = L.size
    d.rounded_rectangle((10, h * .18, w - 10, h * .82), h * .32, fill=(70, 80, 110, 255), outline=(200, 220, 255, 255), width=6)
    d.rounded_rectangle((w * .2, h * .3, w * .8, h * .7), h * .2, fill=tuple(mix(col, (255, 255, 255), .3 + .3 * abierta)) + (255,))
    for i in range(5): d.ellipse((w * .12 + i * w * .19 - 8, h * .82 - 26, w * .12 + i * w * .19 + 8, h * .82 - 10), fill=tuple(col) + (255,))
    glow(c, x, y, s * (1 + abierta), col, 90 + int(40 * math.sin(t * 3)))
    place(c, L, x, y + math.sin(t * 1.5) * 12, scale=.7 + .3 * eb(pr(t, 0, .5)), rot=math.sin(t) * 3)

def estrellas(c, t, nota, x, y, s=None, col=ORO):
    s = s or P(70, 70)
    for i in range(5):
        u = eb(pr(t, .3 + i * .22, .35)); xx = x + (i - 2) * s * 2.3
        lleno = clamp(nota - i)
        pts = [(xx + math.cos(math.radians(-90 + k * 36)) * (s if k % 2 == 0 else s * .45), y + math.sin(math.radians(-90 + k * 36)) * (s if k % 2 == 0 else s * .45)) for k in range(10)]
        L = Image.new("RGBA", (int(s * 2.4), int(s * 2.4)), (0, 0, 0, 0)); d = ImageDraw.Draw(L); o = s * 1.2
        pp = [(px - xx + o, py - y + o) for px, py in pts]; d.polygon(pp, fill=(60, 50, 70, 255), outline=col + (255,))
        if lleno > 0:
            m = Image.new("L", L.size, 0); ImageDraw.Draw(m).rectangle((0, 0, o - s + 2 * s * lleno, L.height), fill=255)
            F_ = Image.new("RGBA", L.size, (0, 0, 0, 0)); ImageDraw.Draw(F_).polygon(pp, fill=col + (255,)); L.paste(F_, (0, 0), ImageChops.multiply(m, F_.getchannel("A")))
            glow(c, xx, y, s, col, int(90 * u))
        place(c, L, xx, y, scale=u)

def caja_comentario(c, t, palabra="DOOM", x=None, y=None, col=VERDE):
    x = x or W / 2; y = y or P(1500, 820); w, h = P(760, 700), P(120, 110)
    L = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rounded_rectangle((3, 3, w - 4, h - 4), 30, fill=(12, 14, 24, 240), outline=tuple(col) + (255,), width=5)
    d.ellipse((22, h / 2 - 34, 90, h / 2 + 34), fill=tuple(col) + (255,))
    n = int(len(palabra) * pr(t, .5, .9)); txt = palabra[:n] + ("|" if int(t * 3) % 2 == 0 else "")
    d.text((120, h / 2), txt, font=F(int(h * .48)), fill=(255, 255, 255, 255), anchor="lm")
    d.ellipse((w - 100, h / 2 - 36, w - 28, h / 2 + 36), fill=tuple(col) + (255,)); d.polygon([(w - 80, h / 2 - 16), (w - 46, h / 2), (w - 80, h / 2 + 16)], fill=(10, 30, 15, 255))
    glow(c, x, y, w * .4, col, 70); place(c, L, x, y + (1 - eo(pr(t, 0, .5))) * 200, alpha=eo(pr(t, 0, .4)))

@lru_cache(maxsize=1)
def _logo():
    return Image.open(os.path.join(KIT, "marcas", "comics-store", "logo.png")).convert("RGBA")

def barra_suscribir(c, t, x=None, y=None, inicio=.3):
    x = x or W / 2; y = y or P(1650, 960); w, h = P(820, 760), P(130, 120); L = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rounded_rectangle((2, 2, w - 3, h - 3), 24, fill=(14, 12, 20, 245))
    lg = _logo().resize((h - 24, h - 24), Image.LANCZOS); L.alpha_composite(lg, (14, 12))
    d.text((h + 10, h * .36), "@ComicsStoreCol", font=F(int(h * .26)), fill=(255, 255, 255, 255), anchor="lm")
    d.text((h + 10, h * .68), "El paraíso del coleccionista", font=F(int(h * .18)), fill=(180, 180, 200, 255), anchor="lm")
    hecho = t > inicio + 1.0
    bx0 = w - 250; d.rounded_rectangle((bx0, h * .25, w - 70, h * .75), h * .25, fill=(70, 70, 80, 255) if hecho else (230, 30, 50, 255))
    d.text(((bx0 + w - 70) / 2, h / 2), "¡SUSCRITO!" if hecho else "SUSCRIBIRME", font=F(int(h * .17)), fill=(255, 255, 255, 255), anchor="mm")
    d.text((w - 38, h / 2), "🔔" if False else "•", font=F(40), fill=ORO + (255,), anchor="mm")
    place(c, L, x, y + (1 - eo(pr(t, inicio, .5))) * 250, alpha=eo(pr(t, inicio, .4)))
    # cursor que hace clic
    u = eio(pr(t, inicio + .4, .5)); cx = x + w / 2 - 160 + (1 - u) * 200; cy = y + 30 + (1 - u) * 120
    if t > inicio + .3:
        d2 = ImageDraw.Draw(c); s = 1 - .2 * math.sin(clamp((t - inicio - .95) / .2) * math.pi)
        d2.polygon([(cx, cy), (cx + 38 * s, cy + 52 * s), (cx + 18 * s, cy + 52 * s), (cx + 26 * s, cy + 76 * s), (cx + 14 * s, cy + 80 * s), (cx + 6 * s, cy + 56 * s), (cx - 6 * s, cy + 70 * s)], fill=(255, 255, 255, 255), outline=(0, 0, 0, 255))

def rayos_velocidad(c, t, col=(255, 255, 255), dur=.5, cx=None, cy=None):
    if t > dur: return
    cx = cx or W / 2; cy = cy or H / 2; d = ImageDraw.Draw(c); rng = random.Random(int(t * 30)); a = int(150 * (1 - t / dur))
    for i in range(40):
        ang = rng.uniform(0, 6.28); r0 = rng.uniform(.35, .6) * max(W, H); r1 = r0 + rng.uniform(150, 400)
        d.line([(cx + math.cos(ang) * r0, cy + math.sin(ang) * r0), (cx + math.cos(ang) * r1, cy + math.sin(ang) * r1)], fill=col + (a,), width=rng.choice([2, 3, 5]))

# ------------------------------------------------------------------ narrador (presentador encapuchado, set neón)
_TOMAS = {}
def _tomas():
    """Clips reales del narrador (Higgsfield, sin voz) → cuadros a 30 fps del tamaño del video."""
    import glob, subprocess
    if "t" not in _TOMAS:
        clips = sorted(glob.glob(os.path.join(KIT, "marcas", "comics-store", "intros", "clips", "gamer_hablando_h*.mp4" if HZ else "gamer_hablando_v*.mp4")))
        out = []
        for clip in clips:
            cache = f"/home/claude/frames/{os.path.splitext(os.path.basename(clip))[0]}_{W}x{H}"
            if not glob.glob(f"{cache}/f*.jpg"):
                os.makedirs(cache, exist_ok=True)
                subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", clip, "-vf", f"fps=30,scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H}", "-q:v", "2", f"{cache}/f%04d.jpg"], check=True)
            out.extend(_partir_cortes(sorted(glob.glob(f"{cache}/f*.jpg"))))
        _TOMAS["t"] = out; _TOMAS["k"] = 0
    return _TOMAS["t"]

def _actividad(files):
    """Movimiento de boca/cabeza por cuadro (diferencia en la zona de la cara). Devuelve índices de cuadros 'hablando'."""
    import numpy as np
    x0, x1, y0, y1 = (.40, .60, .22, .50) if HZ else (.36, .64, .22, .42)
    g = []
    for fp in files:
        im = Image.open(fp).convert("L"); w, h = im.size
        g.append(np.asarray(im.crop((int(w * x0), int(h * y0), int(w * x1), int(h * y1))).resize((96, 96)), dtype=np.float32))
    n = len(g); a = np.zeros(n)
    for k in range(3, n): a[k] = np.abs(g[k] - g[k - 3]).mean()
    a[:3] = a[3] if n > 3 else 0
    a = np.convolve(a, np.ones(9) / 9, "same")
    thr = np.percentile(a, 40); act = a > thr
    # tramos hablando de al menos 0,8 s
    idx = []; k = 0
    while k < n:
        if act[k]:
            e = k
            while e < n and act[e]: e += 1
            if e - k >= 24: idx.extend(range(k, e))
            k = e
        else: k += 1
    return idx or list(range(n))

def _partir_cortes(files, minimo=45):
    """Parte un clip donde hay un corte de cámara (cambio brusco de plano): cada plano queda como toma aparte."""
    import numpy as np
    g = [np.asarray(Image.open(p).convert("L").resize((64, 36)), dtype=np.float32) for p in files]
    cortes = [k for k in range(1, len(g)) if np.abs(g[k] - g[k - 1]).mean() > 18]
    trozos, a = [], 0
    for c in cortes + [len(files)]:
        if c - a >= minimo: trozos.append(files[a:c])
        a = c
    return trozos or [files]

_NV = {}
def _narrador_gamer():
    """Narrador en video sincronizado por BOCA: apertura medida cuadro a cuadro (insightface, biblioteca/narrador/gamer/boca.json),
    normalizada con TODAS las tomas juntas (una toma quieta no se infla), y cada escena se edita con trozos de 0,3 s cuya boca sigue la voz."""
    if "nv" not in _NV:
        import json, numpy as np
        from narrador_video import NarradorVideo
        nv = NarradorVideo("gamer")
        import types
        nv.planificar = types.MethodType(_planificar_suave, nv)
        data = json.load(open(os.path.join(KIT, "biblioteca", "narrador", "gamer", "boca.json")))
        noms = sorted(os.path.basename(p_)[:-4] for p_ in __import__("glob").glob(os.path.join(KIT, "biblioteca", "narrador", "gamer", nv.ori, "*.mp4")))
        crudos = []
        for nom, cl in zip(noms, nv.clips):
            v = np.array([np.nan if x is None else x for x in data[f"{nv.ori}/{nom}"]["boca"]], float)
            k = np.arange(len(v)); ok = ~np.isnan(v); v = np.interp(k, k[ok], v[ok]); v = np.convolve(v, [.25, .5, .25], "same"); crudos.append(v[:len(cl["frames"])])
        todo = np.concatenate(crudos); lo, hi = np.percentile(todo, 10), np.percentile(todo, 97)
        for cl, v in zip(nv.clips, crudos): cl["m"] = np.clip((v - lo) / max(1e-6, hi - lo), 0, 1)
        _NV["nv"] = nv
    return _NV["nv"]

def _planificar_suave(self, lv, lead, nf, K=12, salto=.75):
    """Como NarradorVideo.planificar pero con trozos de 0,4 s y saltos mucho más caros (menos fundidos/imagen doble)."""
    import numpy as np
    RATES = (.64, .72, .8, .88, .96)
    T_ = np.zeros(nf); off = int(round(lead * 30)) - 1
    for f in range(nf):
        k = f - off
        if 0 <= k < len(lv): T_[f] = lv[k]
    T_ = np.clip(T_ / max(.35, np.percentile(T_[T_ > 0], 85) if (T_ > 0).any() else 1), 0, 1)
    plan = []; cur = None
    for f0 in range(0, nf, K):
        n = min(K, nf - f0); tgt = T_[f0:f0 + n]; idx = np.arange(n); best = None
        if cur is not None:
            c, st = cur
            for r in RATES:
                pos = st + r * (idx + 1)
                if pos[-1] >= len(self.clips[c]["m"]) - 1: continue
                cost = np.abs(self._M(c, pos) - tgt).mean() + .5 * abs(r - .8) ** 2
                if best is None or cost < best[0]: best = (cost, c, pos, False)
        for c, cl in enumerate(self.clips):
            m = cl["m"]; L = len(m); starts = np.arange(0, L - int(n * .8) - 2, 2)
            if not len(starts): continue
            Pm = starts[:, None] + .8 * idx[None, :]; Mv = self._M(c, Pm)
            cost = np.abs(Mv - tgt[None, :]).mean(1) + .05 * self.uso[c][starts] + (salto if cur is not None else 0)
            j = int(np.argmin(cost))
            if best is None or cost[j] < best[0]: best = (float(cost[j]), c, Pm[j], cur is not None)
        _, c, pos, sal = best
        for i, p_ in enumerate(pos):
            fade = None
            if sal and i < 3 and cur is not None and cur[0] == c:   # entre tomas distintas: corte limpio (cambio de cámara)
                pc, ps = cur; fade = (pc, min(ps + .8 * (i + 1), len(self.clips[pc]["frames"]) - 1), (i + 1) / 4)
            plan.append((c, float(p_), fade))
        cur = (c, float(pos[-1]))
        u = self.uso[c]; a, b = int(pos[0]), int(pos[-1]) + 1; u *= .97; u[max(0, a - 12):b + 12] += 1
    return plan

def narrador_escena(titulo=None, col=VERDE, sub=None, z0=1.0, z1=1.05):
    """Escena del narrador: clip real cuya boca se abre y se cierra con la voz de Fernando (desde el primer cuadro)."""
    import numpy as np
    nv = _narrador_gamer(); st = {}
    def f(t, d):
        nf = int(round(d * 30))
        if st.get("nf") != nf:
            voz = getattr(f, "voz", None); lead = getattr(f, "lead", .15)
            st["plan"] = nv.planificar(voz if voz is not None else np.zeros(nf), lead, nf); st["nf"] = nf
        plan = st["plan"]; c_, p_, fade = plan[min(len(plan) - 1, max(0, int(round(t * 30))))]
        im = nv._img(c_, p_)
        if fade: im = Image.blend(nv._img(fade[0], fade[1]), im, fade[2])
        c = im.resize((W, H), Image.LANCZOS).convert("RGBA"); c = zoom(c, t, d, z0, z1)
        if titulo:
            u = eb(pr(t, .2, .5)); texto(c, titulo, W / 2, P(1560, 860), P(84, 96), col, alpha=clamp(u * 1.5), glow_col=col)
            if sub: texto(c, sub, W / 2, P(1660, 950), P(44, 46), (255, 255, 255), alpha=eo(pr(t, .6, .4)), stroke=5)
        vineta(c, 120); return c
    return f

# ------------------------------------------------------------------ fábrica de escenas
def S(nombre, f):
    f.__name__ = nombre; return f

def fx_final(c, t, d, pal):
    vineta(c, 160); return c
