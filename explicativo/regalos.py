"""Formato GUÍA DE REGALOS (Comics Store, Navidad): el encapuchado en el set gamer navideño presenta
productos reales de la tienda sobre un pedestal neón, con nombre, precio y un dato del personaje.
Uso: ver explicativo/regalos/rg01_dragon_ball.py"""
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE); sys.path.insert(0, ROOT)
from PIL import Image, ImageDraw, ImageFilter, ImageChops
from lib import *
import lib as _lib
from resena import Anfitrion, neon
from compositor import fx_nieve
import motor

INTROS = os.path.join(ROOT, "marcas", "comics-store", "intros")
FONDOS = os.path.join(ROOT, "biblioteca", "fondos", "v")
M = marca("comics-store")

def _cover(path, size=(W, H)):
    im = Image.open(path).convert("RGB"); sw, sh = im.size; tw, th = size
    k = max(tw / sw, th / sh); im = im.resize((int(sw * k + .5), int(sh * k + .5)), Image.LANCZOS)
    x0 = (im.width - tw) // 2; y0 = (im.height - th) // 2
    return im.crop((x0, y0, x0 + tw, y0 + th)).convert("RGBA")

# ---------------------------------------------------------------- presentador (set navideño)
def _dof(src_path, out_path):
    """Profundidad de campo: estanterías laterales desenfocadas, presentador y escritorio nítidos."""
    if os.path.exists(out_path) and os.path.getmtime(out_path) > os.path.getmtime(src_path): return out_path
    im = Image.open(src_path).convert("RGB"); w, h = im.size
    m = Image.new("L", im.size, 0); d = ImageDraw.Draw(m)
    d.ellipse((w * .5 - 330, 380, w * .5 + 330, 1500), fill=255); d.rectangle((0, 1180, w, h), fill=255)
    m = m.filter(ImageFilter.GaussianBlur(70))
    bl = im.filter(ImageFilter.GaussianBlur(7))
    Image.composite(im, bl, m).save(out_path); return out_path

class Presentador(Anfitrion):
    LUCES = [(60, 40), (180, 150), (250, 230), (720, 180), (820, 110), (900, 60), (40, 760), (130, 750), (790, 590), (760, 700), (830, 700)]
    def __init__(self):
        p = _dof(os.path.join(INTROS, "navidad_narrador_v.png"), os.path.join(INTROS, "navidad_narrador_v_dof.png"))
        super().__init__(p, cabeza=(475, 640, 175, 215), boca=(476, 691, 62, 762, 14), vela=(790, 600), lampara=(472, 330), ventana=(330, 0, 615, 185))
    def escena(self, z0=1.0, z1=1.12, cy=.44, nombre="host", mini=None):
        def f(t, d):
            im = self._frame(t, motor.NIVEL); SW, SH = self.SW, self.SH
            z = (z0 + (z1 - z0) * eio(min(1, t / d))) * (1 + .005 * math.sin(t * 1.65)); h = min(SH, SW * H / W) / z; w = h * W / H
            jx = (math.sin(t * 1.1) + .6 * math.sin(t * 2.7 + 1)) * SW * .0016; jy = (math.sin(t * .8 + 2) + .5 * math.sin(t * 2.1)) * SH * .0013
            x0 = min(max((SW - w) / 2 + jx, 0), SW - w); y0 = min(max(cy * SH - h / 2 + jy, 0), SH - h); k = W / w
            c = im.resize((W, H), Image.BICUBIC, box=(x0, y0, x0 + w, y0 + h))
            P = lambda x, y: ((x - x0) * k, (y - y0) * k)
            for i, (lx, ly) in enumerate(self.LUCES):   # luces navideñas titilando
                a = int(40 + 50 * (.5 + .5 * math.sin(t * (2.1 + i * .37) + i * 1.7)))
                px, py = P(lx, ly); glow(c, px, py, 46 * k, (255, 200, 110), a)
            px, py = P(472, 330); glow(c, px, py, 230 * k, (60, 255, 120), int(28 + 18 * math.sin(t * 3.1) ** 2))   # neón del control
            px, py = P(472, 95); glow(c, px, py, 200 * k, (150, 180, 255), 30)   # ventana nevada
            fx_nieve_suave(c, t)
            if mini: mini(c, t)
            if t < .35 and nombre == "intro": c.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, int(255 * (1 - t / .35)))))
            vineta(c, .45); return c
        f.__name__ = nombre; return f

def fx_nieve_suave(c, t, n=55):
    L = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L); rnd = random.Random(9)
    for i in range(n):
        x0, y0, sp, r = rnd.uniform(0, W), rnd.uniform(0, H), rnd.uniform(35, 90), rnd.uniform(1.5, 4.5)
        y = (y0 + t * sp) % H; x = x0 + 25 * math.sin(t * .8 + i); d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 255, 255, int(110 + 25 * r)))
    c.alpha_composite(L.filter(ImageFilter.GaussianBlur(1.2)))

# ---------------------------------------------------------------- tarjeta del producto
def _redondear(im, r):
    m = Image.new("L", im.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, im.width - 1, im.height - 1), r, fill=255)
    im = im.convert("RGBA"); im.putalpha(ImageChops.multiply(im.getchannel("A"), m)); return im

_CARD = {}
def tarjeta(path, lado=620, col=None):
    """Foto del producto en un marco neón con brillo (cacheada por tamaño)."""
    key = (path, lado, col)
    if key in _CARD: return _CARD[key]
    col = col or _lib.NEON
    src = Image.open(path).convert("RGB"); s = min(src.size)
    src = src.crop(((src.width - s) // 2, (src.height - s) // 2, (src.width + s) // 2, (src.height + s) // 2)).resize((lado, lado), Image.LANCZOS)
    pad = int(lado * .12); r = int(lado * .07); C = Image.new("RGBA", (lado + 2 * pad, lado + 2 * pad), (0, 0, 0, 0))
    g = Image.new("RGBA", C.size, (0, 0, 0, 0)); ImageDraw.Draw(g).rounded_rectangle((pad - 6, pad - 6, pad + lado + 6, pad + lado + 6), r + 6, outline=col + (255,), width=14)
    C.alpha_composite(g.filter(ImageFilter.GaussianBlur(pad * .45))); C.alpha_composite(g.filter(ImageFilter.GaussianBlur(pad * .2)))
    C.alpha_composite(_redondear(src, r), (pad, pad))
    _CARD[key] = (C, pad); return C, pad

def _brillo(card, pad, k):
    """Destello diagonal que cruza la foto (k de 0 a 1)."""
    if not 0 < k < 1: return card
    w, h = card.size; L = Image.new("L", (w, h), 0); d = ImageDraw.Draw(L); x = -w * .4 + k * w * 1.8
    d.polygon([(x, 0), (x + w * .16, 0), (x - h * .5 + w * .16, h), (x - h * .5, h)], fill=120)
    L = L.filter(ImageFilter.GaussianBlur(18)); L = ImageChops.multiply(L, card.getchannel("A"))
    S = Image.new("RGBA", (w, h), (255, 255, 255, 0)); S.putalpha(L); out = card.copy(); out.alpha_composite(S); return out

_BG = {}
def _pedestal():
    if "p" not in _BG: _BG["p"] = _cover(os.path.join(FONDOS, "navidad_pedestal.png"))
    return _BG["p"]

def producto(img, n, nombre, precio, fase=0, nota=None):
    """Escena del producto. fase 0 = presentación (entra la tarjeta, nombre y precio); fase 1 = acercamiento con dato (nota)."""
    def f(t, d):
        bg = _pedestal(); c = camera(bg, t, d, 1.04 + .03 * fase, 1.1 + .03 * fase, dx=-20 if fase else 20)
        glow(c, W / 2, 1240, 470, _lib.NEON, int(55 + 25 * math.sin(t * 2.4) ** 2))   # luz del pedestal
        glow(c, W * .85, 760, 160, (255, 200, 110), int(40 + 30 * math.sin(t * 3.3) ** 2))  # árbol
        card, pad = tarjeta(img, 600 if fase == 0 else 640)
        ent = eb(pr(t, .05, .65)) if fase == 0 else 1.
        bob = math.sin(t * 1.8) * 12; rot = math.sin(t * 1.1) * 1.6 + (1 - ent) * -10
        cy = 905 + bob + (1 - ent) * 260
        glow(c, W / 2, 1230, 300 * ent, _lib.NEON, int(120 * ent))   # reflejo sobre el pedestal
        place(c, _brillo(card, pad, (t - .7) / .8 if fase == 0 else (t - .3) / .9), W / 2, cy, scale=(.55 + .45 * ent) * (1 + .03 * fase), rot=rot, alpha=min(1, ent * 1.5))
        neon(c, f"REGALO #{n}", W / 2, 540, 74, _lib.NEON2, eo(pr(t, .15, .4)))
        if fase == 0:
            etiqueta(c, nombre, W / 2, 1405, (255, 255, 255), size=50, alpha=eo(pr(t, .55, .4)), borde=_lib.NEON2)
            a = eo(pr(t, .85, .4)); neon(c, precio, W / 2, 1565 + (1 - a) * 40, 112, _lib.NEON, a)
        else:
            etiqueta(c, precio, W / 2, 1405, (20, 18, 34), bg=(255, 255, 255), size=54, alpha=eo(pr(t, .1, .3)))
            if nota: etiqueta(c, nota, W / 2, 1540, (255, 255, 255), size=44, alpha=eo(pr(t, .4, .4)), borde=_lib.NEON)
        etiqueta(c, M["cta"].lower(), W / 2, 1790, (255, 255, 255), size=34, alpha=.85)
        fx_nieve_suave(c, t, 45); vineta(c, .45)
        if t < .2: c.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(120 * (1 - t / .2)))))   # flash de entrada
        return c
    f.__name__ = f"p{n}{'ab'[fase]}"; return f

def mini_card(img, precio):
    """Producto pequeño abajo a la izquierda mientras habla el presentador."""
    def m(c, t):
        card, pad = tarjeta(img, 300); a = eb(pr(t, .15, .5)); x, y = 245, 1560 + math.sin(t * 1.8) * 8
        place(c, card, x, y + (1 - a) * 200, scale=a, rot=math.sin(t * 1.2) * 2)
        etiqueta(c, precio, x, y + 245, (20, 18, 34), bg=(255, 255, 255), size=40, alpha=eo(pr(t, .5, .3)))
    return m

def cierre(pregunta):
    def f(t, d): return escena_cierre(M, t, d, pregunta)
    f.__name__ = "cierre"; return f

def armar(guion, version):
    """guion: dict con 'productos' (img, nombre, precio, nota) y textos por versión ('fb' o 'tt').
    Cada item de la versión: ("host", frase, claves[, n_producto]) | ("p", n, fase, frase, claves) | ("cierre", frase, claves, pregunta)."""
    A = PresentadorVideo(); P = guion["productos"]; out = []; ganchos = []; vistas = [(1.0, 1.06, .5), (1.08, 1.0, .5), (1.0, 1.1, .5), (1.12, 1.04, .5)]
    for i, it in enumerate(guion[version]):
        if it[0] == "host":
            _, frase, clave = it[:3]; prod = it[3] if len(it) > 3 else None; z0, z1, cy = vistas[i % len(vistas)]
            mini = mini_card(P[prod - 1]["img"], P[prod - 1]["precio"]) if prod else None
            out.append((A.escena(z0, z1, cy, "intro" if i == 0 else f"h{i:02d}", mini), frase, clave))
            if 0 < i and not prod: ganchos.append(len(out) - 1)
        elif it[0] == "p":
            _, n, fase, frase, clave = it; p = P[n - 1]
            out.append((producto(p["img"], n, p["nombre"], p["precio"], fase, p.get("nota")), frase, clave))
        elif it[0] == "cierre":
            _, frase, clave, preg = it; out.append((cierre(preg), frase, clave))
    return out, ganchos

# ---------------------------------------------------------------- presentador en VIDEO (clip de Higgsfield, sin voz, en bucle)
class PresentadorVideo:
    """Usa un clip real del encapuchado hablando. Bucle de ida y vuelta (sin saltos) y cada escena arranca en otro punto."""
    def __init__(self, clip=os.path.join(INTROS, "clips", "navidad_hablando_h.mp4"), cache="/home/claude/frames_navidad_v"):
        import glob, subprocess
        if not glob.glob(f"{cache}/f*.jpg"):
            os.makedirs(cache, exist_ok=True)
            vf = "fps=30,crop=608:1080:656:0,scale=1080:1920:flags=lanczos" if not HORIZONTAL else "fps=30,scale=1920:1080"
            subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", clip, "-vf", vf, "-q:v", "2", f"{cache}/f%04d.jpg"], check=True)
        self.files = sorted(glob.glob(f"{cache}/f*.jpg")); self.n = len(self.files); self.k = 0
    def _cuadro(self, i):
        p = 2 * (self.n - 1); i %= p; i = i if i < self.n else p - i   # ida y vuelta
        return Image.open(self.files[i]).convert("RGBA")
    def escena(self, z0=1.0, z1=1.06, cy=.5, nombre="host", mini=None):
        off = (self.k * 97) % (2 * self.n); self.k += 1
        def f(t, d):
            fr = self._cuadro(off + int(t * 30)); c = camera(fr, t, d, z0, z1)
            fx_nieve_suave(c, t, 35)
            if mini: mini(c, t)
            if t < .35 and nombre == "intro": c.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, int(255 * (1 - t / .35)))))
            vineta(c, .4); return c
        f.__name__ = nombre; return f
