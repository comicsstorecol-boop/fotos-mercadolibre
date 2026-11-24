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


# ---------------------------------------------------------------- overlays en video (Fernando, fondo negro) y recortes con borde neón
EFXV = os.path.join(ROOT, "biblioteca", "efectos", "video")
class Overlay:
    def __init__(self, nombre):
        import glob, subprocess
        self.cache = f"/home/claude/frames/ov_{nombre}_{W}x{H}"
        if not glob.glob(f"{self.cache}/f*.jpg"):
            os.makedirs(self.cache, exist_ok=True)
            subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", os.path.join(EFXV, nombre + ".mp4"), "-vf",
                            f"fps=30,scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}", "-q:v", "3", f"{self.cache}/f%04d.jpg"], check=True)
        self.files = sorted(glob.glob(f"{self.cache}/f*.jpg")); self.n = len(self.files)
    def frame(self, t, loop=True):
        i = int(t * 30); i = i % self.n if loop else min(i, self.n - 1)
        return Image.open(self.files[i]).convert("RGB")
_OV = {}
def ov(nombre):
    if nombre not in _OV: _OV[nombre] = Overlay(nombre)
    return _OV[nombre]
_NEGRO = {}
def pantalla(c, nombre, t, a=1., loop=True):
    """Mezcla 'screen' del overlay sobre el cuadro (solo suma luz)."""
    if a <= .01: return c
    o = ov(nombre).frame(t, loop)
    if a < 1:
        if "n" not in _NEGRO: _NEGRO["n"] = Image.new("RGB", (W, H), (0, 0, 0))
        o = Image.blend(_NEGRO["n"], o, a)
    out = ImageChops.screen(c.convert("RGB"), o).convert("RGBA"); return out

_REC = {}
def recorte(path, lado=620, col=None):
    """Producto sin fondo con borde neón que sigue su silueta (sin marco). Los anchos (dioramas) crecen hasta 1,45x."""
    col = col or (57, 235, 30); key = (path, lado, col)   # verde del logo Comics Store
    if key in _REC: return _REC[key]
    import numpy as np
    from scipy import ndimage
    im = Image.open(path).convert("RGBA"); k = min(lado / im.height, lado * 1.45 / im.width); im = im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS)
    pad = int(lado * .12); A = Image.new("L", (im.width + 2 * pad, im.height + 2 * pad), 0); A.paste(im.getchannel("A"), (pad, pad))
    lleno = Image.fromarray((ndimage.binary_fill_holes(np.array(A) > 110) * 255).astype("uint8"))
    borde = ImageChops.subtract(lleno.filter(ImageFilter.MaxFilter(15)), lleno.filter(ImageFilter.MinFilter(3)))
    C = Image.new("RGBA", A.size, (0, 0, 0, 0))
    for r, m in ((pad * .5, 4.), (pad * .5, 4.), (pad * .2, 3.5), (pad * .08, 3.)):
        L = Image.new("RGBA", A.size, col + (0,)); L.putalpha(borde.filter(ImageFilter.GaussianBlur(r)).point(lambda v: min(255, int(v * m)))); C.alpha_composite(L)
    L = Image.new("RGBA", A.size, mix(col, (255, 255, 255), .55) + (0,)); L.putalpha(borde.filter(ImageFilter.MinFilter(5)).filter(ImageFilter.GaussianBlur(1.5))); C.alpha_composite(L)
    C.alpha_composite(im, (pad, pad)); _REC[key] = (C, pad); return C, pad

_BG = {}
def _letrero():
    """Letrero neón 'El Paraíso del Coleccionista' (Fernando) separado en tubos verdes y rosados para que parpadeen por separado."""
    if "l" not in _BG:
        import numpy as np
        L = Image.open(os.path.join(ROOT, "biblioteca", "efectos", "letrero_paraiso.png")).convert("RGB")
        ancho = 800; L = L.resize((ancho, int(L.height * ancho / L.width)), Image.LANCZOS)
        a = np.asarray(L).astype(np.int16); verde = (a[..., 1] > a[..., 0]) & (a[..., 1] > a[..., 2])
        _BG["l"] = [Image.fromarray(np.where(mk[..., None], a, 0).astype("uint8")) for mk in (verde, ~verde)]
    return _BG["l"]
def _tubo(t, semilla):
    """Brillo de un tubo neón: pulso suave + apagones cortos al azar (reproducibles)."""
    k = int(t * 8); r = random.Random(k * 7919 + semilla).random()
    if r < .06: return .12
    if r < .10: return .55
    return .88 + .12 * math.sin(t * 5.3 + semilla)
def _pedestal(t=0.):
    if "p" not in _BG: _BG["p"] = _cover(os.path.join(FONDOS, "navidad_pedestal_limpio.png")).convert("RGB")
    c = _BG["p"]; neg = Image.new("RGB", (W, H), (0, 0, 0))
    for i, capa in enumerate(_letrero()):
        b = _tubo(t, i * 31 + 3); L = neg.copy(); L.paste(capa, ((W - capa.width) // 2, 455 - capa.height // 2))
        c = ImageChops.screen(c, Image.blend(neg, L, b))
    return c.convert("RGBA")

def producto(img, n, nombre, precio, fase=0, nota=None):
    """Escena del producto. fase 0 = presentación (entra la tarjeta, nombre y precio); fase 1 = acercamiento con dato (nota)."""
    def f(t, d):
        bg = _pedestal(t + n * 2.7); c = camera(bg, t, d, 1.04 + .03 * fase, 1.1 + .03 * fase, dx=-20 if fase else 20)
        glow(c, W / 2, 1240, 470, _lib.NEON, int(55 + 25 * math.sin(t * 2.4) ** 2))   # luz del pedestal
        glow(c, W * .85, 760, 160, (255, 200, 110), int(40 + 30 * math.sin(t * 3.3) ** 2))  # árbol
        card, pad = recorte(img, 560 if fase == 0 else 600)
        ent = eb(pr(t, .05, .65)) if fase == 0 else 1.
        bob = math.sin(t * 1.8) * 12; rot = math.sin(t * 1.1) * 1.6 + (1 - ent) * -10
        esc = (.55 + .45 * ent) * (1 + .03 * fase)
        cy = 1185 - (card.height / 2 - pad) * esc + bob * .4 + (1 - ent) * 260   # la base del producto se apoya en el centro del pedestal
        glow(c, W / 2, 1230, 300 * ent, _lib.NEON, int(120 * ent))   # reflejo sobre el pedestal
        place(c, _brillo(card, pad, (t - .7) / .8 if fase == 0 else (t - .3) / .9), W / 2, cy, scale=esc, rot=rot * .5, alpha=min(1, ent * 1.5))
        neon(c, f"REGALO #{n}", W / 2, 1312, 66, _lib.NEON2, eo(pr(t, .15, .4)))
        if fase == 0:
            etiqueta(c, nombre, W / 2, 1425, (255, 255, 255), size=50, alpha=eo(pr(t, .55, .4)), borde=_lib.NEON2)
            a = eo(pr(t, .85, .4)); neon(c, precio, W / 2, 1580 + (1 - a) * 40, 112, _lib.NEON, a)
        else:
            etiqueta(c, precio, W / 2, 1425, (20, 18, 34), bg=(255, 255, 255), size=54, alpha=eo(pr(t, .1, .3)))
            if nota: etiqueta(c, nota, W / 2, 1560, (255, 255, 255), size=44, alpha=eo(pr(t, .4, .4)), borde=_lib.NEON)
        etiqueta(c, M["cta"].lower(), W / 2, 1790, (255, 255, 255), size=34, alpha=.85)
        c = pantalla(c, "neon_parpadeo" if fase == 0 else "neon_escenario", t + n, .9)
        c = pantalla(c, "bokeh_navidad", t + n * 1.3, .28)
        if fase == 0: c = pantalla(c, "destello", t * .9, max(0, 1 - t / 1.6), loop=False)
        if fase == 0 and t < .7: c = pantalla(c, "light_leak", t + n, 1 - t / .7)
        fx_nieve_suave(c, t, 45); vineta(c, .45)
        return c
    f.__name__ = f"p{n}{'ab'[fase]}"; return f

def mini_card(img, precio):
    """Producto pequeño abajo a la izquierda mientras habla el presentador."""
    def m(c, t):
        card, pad = recorte(img, 300); a = eb(pr(t, .15, .5)); x, y = 245, 1560 + math.sin(t * 1.8) * 8
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
    """Clips reales del encapuchado (Higgsfield, con su audio). Sincroniza la boca con la voz de Fernando:
    se mide cuándo habla el narrador en el clip y cuándo habla la voz, y se re-cronometra el video (DTW) para que
    cada aparición arranca justo donde él empieza a hablar, para que entre hablando a la vez que la voz; luego sigue a velocidad normal."""
    def __init__(self, clips=None):
        import glob, subprocess
        import numpy as np
        if clips is None:
            pat = "navidad_*_h*.mp4" if HORIZONTAL else "navidad_*_v*.mp4"
            clips = sorted(glob.glob(os.path.join(INTROS, "clips", pat)))
        self.files, act = [], []
        for clip in clips:
            nom = os.path.splitext(os.path.basename(clip))[0]; cache = f"/home/claude/frames/{nom}_{W}x{H}"
            if not glob.glob(f"{cache}/f*.jpg"):
                os.makedirs(cache, exist_ok=True)
                subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", clip, "-vf", f"fps=30,scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}",
                                "-q:v", "2", f"{cache}/f%04d.jpg"], check=True)
            fr = sorted(glob.glob(f"{cache}/f*.jpg"))
            raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", clip, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"], capture_output=True).stdout
            a = np.frombuffer(raw, np.int16).astype(np.float32) if raw else np.zeros(16000)
            hop = 16000 // 30; e = np.array([np.sqrt((a[i * hop:(i + 1) * hop] ** 2).mean()) if i * hop < len(a) else 0 for i in range(len(fr))])
            e = np.clip(e / (np.percentile(e, 90) + 1e-6), 0, 1); e = np.convolve(e, np.ones(3) / 3, "same")
            # ida y vuelta para tener material largo sin saltos
            idx = list(range(len(fr))) + list(range(len(fr) - 2, 0, -1))
            self.files += [fr[i] for i in idx]; act += [float(e[i]) for i in idx]
        self.act = np.array(act); self.k = 0
    def _inicio(self, lead, kk):
        """Cuadro donde el narrador EMPIEZA a hablar, menos el 'lead', para que hable justo cuando entra la voz."""
        import numpy as np
        c = self.act; hab = c > .2
        on = [i for i in range(1, len(c) - 30) if hab[i] and not hab[i - 1] and hab[i:i + 12].mean() > .8]
        if not on: on = [int(np.argmax(c))]
        j = on[(kk * 3) % len(on)]
        return max(0, j - int(round(lead * 30)))
    def escena(self, z0=1.0, z1=1.06, cy=.5, nombre="host", mini=None):
        st = {}; kk = self.k
        def f(t, d):
            if "i0" not in st: st["i0"] = self._inicio(getattr(f, "lead", .15), kk)
            i = (st["i0"] + int(round(t * 30))) % len(self.files)
            c = camera(Image.open(self.files[i]).convert("RGBA"), t, d, z0, z1)
            c = pantalla(c, "bokeh_navidad", t + self.k, .22)
            if mini is None and t < .7: c = pantalla(c, "light_leak", t + self.k, .8 * (1 - t / .7))
            fx_nieve_suave(c, t, 30)
            if mini: mini(c, t)
            if t < .35 and nombre == "intro": c.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, int(255 * (1 - t / .35)))))
            vineta(c, .4); return c
        self.k += 1; f.__name__ = nombre; return f
