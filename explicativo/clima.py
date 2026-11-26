"""Efectos visuales de clima que acompañan el ambiente sonoro de cada escena (fn.amb).
lluvia+relámpagos (tormenta/trueno), nieve, viento, parpadeo de noche, brasas y parpadeo de fuego, destello de explosión."""
import math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

def _rng(semilla, n, k):
    r = random.Random(semilla); return [[r.random() for _ in range(k)] for _ in range(n)]

_LLUVIA = _rng(11, 170, 4); _NIEVE = _rng(22, 140, 4); _VIENTO = _rng(33, 40, 4); _BRASAS = _rng(44, 70, 4)

def _capa(c):
    return Image.new("RGBA", c.size, (0, 0, 0, 0))

def lluvia(c, t, fuerte=1.0):
    W, H = c.size; L = _capa(c); d = ImageDraw.Draw(L); lg = H * .06
    for x0, y0, v, a in _LLUVIA[:int(170 * fuerte)]:
        sp = H * (1.6 + v * 1.2); y = (y0 * H + t * sp) % (H + lg) - lg; x = (x0 * W * 1.2 + t * sp * .18) % (W * 1.2) - W * .1
        d.line((x, y, x - lg * .18, y - lg * (.6 + v * .5)), fill=(200, 215, 255, int(70 + 80 * a)), width=2)
    c.alpha_composite(L)

def relampago(c, t, semilla=0):
    """Destellos irregulares cada ~3-4 s (doble parpadeo, como un rayo real)."""
    ciclo = 3.3 + (semilla % 3) * .4; f = (t + semilla * .7) % ciclo
    k = 0.
    for ini, dur, amp in ((0., .07, .55), (.13, .05, .35), (.22, .12, .25)):
        if ini <= f < ini + dur: k = max(k, amp * (1 - (f - ini) / dur))
    if k > 0: c.alpha_composite(Image.new("RGBA", c.size, (220, 230, 255, int(255 * k))))

def nieve(c, t):
    W, H = c.size; L = _capa(c); d = ImageDraw.Draw(L)
    for x0, y0, v, a in _NIEVE:
        r = 2 + v * 5; y = (y0 * H + t * H * (.08 + v * .12)) % (H + 20) - 10
        x = (x0 * W + math.sin(t * (.8 + a) + x0 * 9) * 40 + t * 30) % W
        d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 255, 255, int(120 + 110 * a)))
    c.alpha_composite(L.filter(ImageFilter.GaussianBlur(1.2)))

def viento(c, t):
    W, H = c.size; L = _capa(c); d = ImageDraw.Draw(L)
    for x0, y0, v, a in _VIENTO:
        ln = W * (.08 + v * .15); x = (x0 * W + t * W * (.9 + v)) % (W + ln) - ln; y = y0 * H + math.sin(t * 2 + x0 * 7) * 25
        d.line((x, y, x + ln, y - ln * .05), fill=(230, 235, 255, int(25 + 45 * a)), width=2)
        if a > .6: d.ellipse((x + ln, y - 3, x + ln + 5, y + 2), fill=(200, 190, 170, 120))   # hojita / polvo
    c.alpha_composite(L.filter(ImageFilter.GaussianBlur(1.5)))

def _brillo(c, k, tinte=None):
    """k<1 oscurece, tinte suma color. Rápido con numpy."""
    a = np.asarray(c).astype(np.float32); a[..., :3] *= k
    if tinte: a[..., :3] += np.array(tinte, np.float32)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), c.mode)

def parpadeo_noche(c, t):
    """Luz que titila: caídas cortas e irregulares de brillo + viñeta fría."""
    caida = 0.
    for per, fase in ((2.7, .0), (4.1, 1.3), (6.3, 2.2)):
        f = (t + fase) % per
        if f < .09: caida = max(caida, .35 * (1 - f / .09))
    k = .9 - caida + .03 * math.sin(t * 9)
    return _brillo(c, k, (0, 2, 10))

def brasas(c, t):
    W, H = c.size; L = _capa(c); d = ImageDraw.Draw(L)
    for x0, y0, v, a in _BRASAS:
        y = H - (y0 * H + t * H * (.12 + v * .15)) % (H * 1.05); x = x0 * W + math.sin(t * 2.5 + x0 * 11) * 30
        r = 1.5 + v * 3.5; al = int(140 + 110 * a) * (y / H)
        d.ellipse((x - r, y - r, x + r, y + r), fill=(255, int(120 + 80 * a), 40, int(al)))
    c.alpha_composite(L.filter(ImageFilter.GaussianBlur(1)))

def parpadeo_fuego(c, t):
    k = 1 + .05 * math.sin(t * 13) + .04 * math.sin(t * 21.7 + 1)
    return _brillo(c, k, (6, 2, 0))

def destello(c, t):
    if t < .35: c.alpha_composite(Image.new("RGBA", c.size, (255, 240, 210, int(200 * (1 - t / .35)))))

FUEGO = ("fogata", "chimenea", "antorchas", "forja", "infierno", "fuego")

def aplicar(c, t, amb, semilla=0):
    if not amb: return c
    a = amb.split("+"); c = c.convert("RGBA")
    if "noche" in a: c = parpadeo_noche(c, t)
    if "velas" in a: c = parpadeo_fuego(c, t)
    if any(x in a for x in FUEGO): c = parpadeo_fuego(c, t); brasas(c, t)
    if "nieve" in a: nieve(c, t)
    if "viento" in a: viento(c, t)
    if "lluvia" in a: lluvia(c, t, .45)
    if "tormenta" in a: lluvia(c, t, 1.0); relampago(c, t, semilla)
    if "trueno" in a: relampago(c, t, semilla)
    if "explosion" in a: destello(c, t)
    return c

def envolver(esc):
    """Envuelve cada escena para dibujar el clima de su ambiente (fn.amb o fn.clima)."""
    out = []
    for i, (fn, txt, *resto) in enumerate(esc):
        amb = getattr(fn, "clima", None) or getattr(fn, "amb", None)
        if amb and not getattr(fn, "_clima", False):
            def g(t, d, _f=fn, _a=amb, _s=i): return aplicar(_f(t, d), t, _a, _s)
            g.__dict__.update(fn.__dict__); g.__name__ = fn.__name__; g._clima = True; fn = g
        out.append((fn, txt, *resto))
    return out
