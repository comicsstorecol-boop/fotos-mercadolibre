"""Formato RESEÑA de películas (Comics Store): portada, capítulos neón, escenas ilustradas,
opinión con el narrador hablando y calificación con estrellas."""
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
from PIL import Image, ImageDraw, ImageFilter
from lib import *
from compositor import escena, objeto
import generador as G
import motor

import lib as _lib
class _C:
    @property
    def v(self): return _lib.NEON
    @property
    def r(self): return _lib.NEON2
_c = _C()
M = marca("comics-store")
G.load_brand("comics-store"); _K = next(iter(G.CHAR)); G.CHAR[_K]["drop"] = int(G.CHAR[_K]["drop"] * 1.9)

def neon(c, txt, x, y, size, col, alpha=1., anchor="mm"):
    f = F(size); L = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.text((x, y), txt, font=f, fill=col + (255,), anchor=anchor, stroke_width=max(4, size // 10), stroke_fill=col + (255,))
    g = L.filter(ImageFilter.GaussianBlur(size // 3))
    T = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(T).text((x, y), txt, font=f, fill=(255, 255, 255, 255), anchor=anchor, stroke_width=max(2, size // 22), stroke_fill=col + (255,))
    for lay in (g, g, T):
        if alpha < 1: lay = lay.copy(); lay.putalpha(lay.getchannel("A").point(lambda v: int(v * alpha)))
        c.alpha_composite(lay)

def _grano(c, t):
    rnd = random.Random(int(t * 30)); L = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    for _ in range(3):
        x = rnd.randint(0, W); d.line([(x, 0), (x + rnd.randint(-20, 20), H)], fill=(255, 255, 255, 18), width=2)
    c.alpha_composite(L)

def _fondo_marca(t):
    c = vgrad(W, H, [(0, (14, 6, 22)), (.5, (8, 10, 18)), (1, (4, 14, 8))]).copy()
    glow(c, W * .3 + math.sin(t * .8) * 80, Y(600), 420, _c.r, 70); glow(c, W * .7 + math.cos(t * .7) * 80, Y(1400), 420, _c.v, 55)
    return c

def logo_mini(c, a=1.):
    if M["logo"] is not None:
        lg = M["logo"].resize((190, int(190 * M["logo"].height / M["logo"].width)), Image.LANCZOS)
        place(c, lg, 130, 150, alpha=a)

def portada(titulo, linea2, sub, obj=None):
    def f(t, d):
        c = _fondo_marca(t)
        if obj: place(c, objeto(obj), W / 2, Y(1380), scale=.9 * KS * eb(pr(t, .3, .6)), alpha=.9)
        neon(c, "RESEÑA", W / 2, Y(640), 70, _c.r, eo(pr(t, .1, .4)))
        neon(c, titulo, W / 2, Y(800), 118, _c.v, eo(pr(t, .3, .5)))
        if linea2: neon(c, linea2, W / 2, Y(940), 118, _c.v, eo(pr(t, .4, .5)))
        etiqueta(c, sub, W / 2, Y(1080), (255, 255, 255), size=46, alpha=eo(pr(t, .7, .4)), borde=_c.r)
        logo_mini(c); _grano(c, t); vineta(c, .6)
        return camera(c, t, d, 1.0, 1.06)
    f.__name__ = "portada"; return f

def capitulo(n, titulo, obj=None):
    def f(t, d):
        c = _fondo_marca(t + n)
        if obj: place(c, objeto(obj), W / 2, Y(1300), scale=.8 * KS * eb(pr(t, .2, .6)), alpha=.85)
        neon(c, f"CAPÍTULO {n}", W / 2, Y(760), 64, _c.r, eo(pr(t, .05, .35)))
        for i, ln in enumerate(titulo.split("|")): neon(c, ln, W / 2, Y(900 + i * 120) if not HORIZONTAL else 470 + i * 110, 104, _c.v, eo(pr(t, .2 + i * .1, .4)))
        logo_mini(c); _grano(c, t)
        return camera(c, t, d, 1.08, 1.0)
    f.__name__ = f"cap{n}"; return f

def calificacion(nota, total=5):
    est = objeto("estrella")
    def f(t, d):
        c = _fondo_marca(t); neon(c, "MI CALIFICACIÓN", W / 2, Y(760), 72, _c.r)
        for i in range(total):
            x = W / 2 + (i - (total - 1) / 2) * 190; a = eb(pr(t, .3 + i * .25, .4))
            if a <= 0: continue
            frac = max(0, min(1, nota - i))
            gris = est.copy(); gris.putalpha(gris.getchannel("A").point(lambda v: int(v * .25))); place(c, gris, x, Y(1000), scale=.6 * a)
            if frac > 0:
                s = est.crop((0, 0, int(est.width * frac), est.height)); L = Image.new("RGBA", est.size, (0, 0, 0, 0)); L.paste(s, (0, 0))
                place(c, L, x, Y(1000), scale=.6 * a)
        neon(c, f"{str(nota).replace('.', ',')} / {total}", W / 2, Y(1210), 110, _c.v, eo(pr(t, 1.6, .5)))
        logo_mini(c); return camera(c, t, d, 1.0, 1.05)
    f.__name__ = "nota"; return f

def intro_imagen(path, z0=1.0, z1=1.25, cy=.42):
    """Escena de apertura con una imagen a pantalla completa, acercamiento lento y vela/luz parpadeando."""
    src = Image.open(path).convert("RGB"); SW, SH = src.size
    def f(t, d):
        z = z0 + (z1 - z0) * eio(min(1, t / d)); h = min(SH, SW * H / W) / z; w = h * W / H
        x0 = (SW - w) / 2; y0 = min(max(cy * SH - h / 2, 0), SH - h)
        c = src.resize((W, H), Image.BICUBIC, box=(x0, y0, x0 + w, y0 + h)).convert("RGBA")
        if t < .6: c.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, int(255 * (1 - t / .6)))))
        vineta(c, .55); return c
    f.__name__ = "intro"; return f

def con_narrador(fn, px=470):
    """Superpone al narrador hablando (abajo a la derecha)."""
    def f(t, d):
        c = fn(t, d); n = G.character(_K, px, min(1., motor.NIVEL * 1.4), (t % 3.7) < .12)
        c.alpha_composite(n, (W - px + 20, int(H - px + 30 + math.sin(t * 2.4) * 5)))
        return c
    f.__name__ = fn.__name__ + "_n"; return f

def armar(items, cierre_txt=None, cierre_preg="¿QUÉ PELÍCULA SIGUE?"):
    """items: lista de (spec_dict o función, frase, claves, narrador?)"""
    out = []
    for i, it in enumerate(items):
        sp, frase, clave = it[:3]; nar = it[3] if len(it) > 3 else False
        fn = sp if callable(sp) else escena(dict(sp, id=sp.get("id", f"e{i + 1:02d}")))
        out.append((con_narrador(fn) if nar else fn, frase, clave))
    def cierre(t, d): return escena_cierre(M, t, d, cierre_preg)
    out.append((cierre, cierre_txt or "¿Qué película quieres que reseñemos ahora? Déjala en los comentarios y síguenos en Comics Store.", {"comentarios", "youtube"}))
    return out

# ================================================================ ANFITRIÓN (imagen con vida: cabeza, boca, luces, humo)
def _humo_tex():
    rnd = random.Random(4); L = Image.new("L", (W, H * 2), 0); d = ImageDraw.Draw(L)
    for _ in range(70):
        x, y, r = rnd.uniform(0, W), rnd.uniform(0, H * 2), rnd.uniform(60, 200); d.ellipse((x - r, y - r * 1.4, x + r, y + r * 1.4), fill=rnd.randint(20, 60))
    return L.filter(ImageFilter.GaussianBlur(50))

class Anfitrion:
    """Imagen del presentador con movimientos sutiles. Coordenadas de la imagen original (1024x1536)."""
    def __init__(self, path, cabeza=(520, 420, 300, 330), boca=(522, 522), vela=(930, 880), lampara=(422, 70), ventana=(700, 0, 1024, 720)):
        self.src = Image.open(path).convert("RGBA"); self.SW, self.SH = self.src.size
        self.cab, self.boca, self.vela, self.lamp, self.ven = cabeza, boca, vela, lampara, ventana
        cx, cy, rx, ry = cabeza; m = Image.new("L", self.src.size, 0); ImageDraw.Draw(m).ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=255)
        self.mcab = m.filter(ImageFilter.GaussianBlur(40)); self.humo = _humo_tex()
    def _frame(self, t, nivel):
        im = self.src.copy(); cx, cy, rx, ry = self.cab
        dx, dy, rot = math.sin(t * .9) * 5, math.sin(t * .7 + 1) * 4 + nivel * 2, math.sin(t * .5) * .8
        head = self.src.rotate(rot, center=(cx, cy + ry * .6), resample=Image.BICUBIC, translate=(dx, dy))
        im.paste(head, (0, 0), self.mcab)
        if nivel > .05:  # boca: se abre con la voz
            bx, by = self.boca[0] + dx, self.boca[1] + dy; op = 1 + 7 * nivel
            jaw = im.crop((int(bx - 55), int(by - 2), int(bx + 55), int(by + 42)))
            mk = Image.new("L", jaw.size, 0); ImageDraw.Draw(mk).ellipse((10, 6, jaw.width - 10, jaw.height * 2), fill=255); mk = mk.filter(ImageFilter.GaussianBlur(8))
            hole = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(hole).ellipse((bx - 18, by - 3, bx + 18, by + op + 3), fill=(20, 8, 8, 230))
            im.alpha_composite(hole.filter(ImageFilter.GaussianBlur(3)))
            im.paste(jaw, (int(bx - 55), int(by - 2 + op)), mk)
        return im
    def escena(self, z0=1.0, z1=1.15, cy=.42, nombre="anf"):
        def f(t, d):
            im = self._frame(t, motor.NIVEL); SW, SH = self.SW, self.SH
            z = z0 + (z1 - z0) * eio(min(1, t / d)); h = min(SH, SW * H / W) / z; w = h * W / H
            x0 = (SW - w) / 2; y0 = min(max(cy * SH - h / 2, 0), SH - h); k = W / w
            c = im.resize((W, H), Image.BICUBIC, box=(x0, y0, x0 + w, y0 + h))
            P = lambda x, y: ((x - x0) * k, (y - y0) * k)
            fl = .55 + .45 * math.sin(t * 13) * math.sin(t * 5.1 + 2)
            vx, vy = P(*self.vela); glow(c, vx, vy - 40 * k, 150 * k, (255, 150, 60), int(70 + 60 * fl)); glow(c, vx - 300 * k, vy + 100 * k, 380 * k, (255, 110, 40), int(25 * fl))
            lx, ly = P(*self.lamp); glow(c, lx, ly, 120 * k, (255, 50, 40), int(60 + 40 * math.sin(t * 9) ** 2))
            if (t % 6.3) < .18:  # relámpago en la ventana
                a0, b0 = P(self.ven[0], self.ven[1]); a1, b1 = P(self.ven[2], self.ven[3])
                L = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(L).rectangle((a0, b0, a1, b1), fill=(200, 210, 255, 70)); c.alpha_composite(L.filter(ImageFilter.GaussianBlur(30)))
            off = int(t * 60) % H; hm = self.humo.crop((0, H - off, W, 2 * H - off)).point(lambda v: int(v * .55))
            sm = Image.new("RGBA", (W, H), (200, 190, 190, 0)); sm.putalpha(hm); c.alpha_composite(sm)
            if t < .4: c.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, int(255 * (1 - t / .4)))))
            vineta(c, .5); return c
        f.__name__ = nombre; return f

# ================================================================ PLANTILLA COMPLETA DE RESEÑA (aprobada con El exorcista)
_ANF = None
_PRESETS = [(1.3, 1.1, .36), (1.1, 1.35, .38), (1.4, 1.15, .4), (1.0, 1.25, .45), (1.15, 1.4, .36), (1.4, 1.1, .45), (1.0, 1.3, .4)]
def anfitrion():
    global _ANF
    if _ANF is None:
        d = os.path.join(os.path.dirname(HERE), "marcas", "comics-store", "intros")
        if HORIZONTAL:
            _ANF = Anfitrion(os.path.join(d, "terror_narrador_h.png"), cabeza=(840, 250, 250, 260), boca=(840, 312), vela=(1226, 525), lampara=(615, 55), ventana=(1100, 0, 1672, 560))
        else: _ANF = Anfitrion(os.path.join(d, "terror_narrador.png"))
    return _ANF

def resena_completa(titulo, linea2, sub, obj_portada, gancho, presentacion, historia, detras, opinion, nota, cierre_nota,
                    obj1="amuleto", gancho_detras=None, gancho_opinion=None):
    """Arma la reseña con el orden aprobado y ganchos de retención. En las listas, usar "H" como escena para que hable el presentador."""
    A = anfitrion(); n = [0]
    def host():
        z0, z1, cy = _PRESETS[n[0] % len(_PRESETS)]; n[0] += 1; return A.escena(z0, z1, cy, f"h{n[0]:02d}")
    def conv(lst): return [((host() if it[0] == "H" else it[0]),) + tuple(it[1:]) for it in lst]
    I = [(A.escena(1.0, 1.22, .42, "intro"), gancho, {"enterradas", "despertar", "miedo", "terror"}),
         (portada(titulo, linea2, sub, obj_portada), presentacion, {"reseña"}),
         (host(), "Aviso: voy a contar la historia completa, incluido el final. Si no la has visto, guarda este video y vuelve después. Y quédate hasta el final, porque te doy mi calificación… y un dato que casi nadie conoce.", {"final", "calificación"}),
         (capitulo(1, "LA|HISTORIA", obj1), "Capítulo uno: la historia.", {"historia"})]
    I += conv(historia)
    I.append((host(), gancho_detras or "Y si la historia te pareció perturbadora… espera a saber lo que pasó detrás de cámaras.", {"cámaras"}))
    I.append((capitulo(2, "DETRÁS DE|CÁMARAS", "claqueta"), "Capítulo dos: detrás de cámaras.", {"cámaras"}))
    I += conv(detras)
    I.append((host(), gancho_opinion or "Ahora sí, la pregunta importante: ¿vale la pena verla hoy? Te doy mi opinión sin filtro.", {"opinión"}))
    I.append((capitulo(3, "MI|OPINIÓN", "estrella"), "Capítulo tres: mi opinión.", {"opinión"}))
    I += conv(opinion)
    I.append((calificacion(nota), cierre_nota, {"calificación", "cinco"}))
    esc = armar(I)
    ganchos = [2, 4 + len(historia), 6 + len(historia) + len(detras)]
    return esc, ganchos


# ================================================================ VERSIONES CORTAS (Facebook/Instagram ~2 min, TikTok 60-90 s)
CTA_YT = "La reseña completa, con todos los secretos del rodaje, está en nuestro canal de YouTube. Síguenos en Comics Store."
def resena_corta(gancho, lista, nota, cierre_nota, cta=CTA_YT):
    """Sin portada ni capítulos: gancho del presentador, historia en ritmo rápido, calificación y llamado a YouTube."""
    A = anfitrion(); n = [0]
    def host():
        z0, z1, cy = _PRESETS[(n[0] + 2) % len(_PRESETS)]; n[0] += 1; return A.escena(z0, z1, cy, f"h{n[0]:02d}")
    I = [(A.escena(1.15, 1.35, .42, "intro"), gancho, {"miedo", "terror"})]
    I += [((host() if it[0] == "H" else it[0]),) + tuple(it[1:]) for it in lista]
    if nota is not None: I.append((calificacion(nota), cierre_nota, {"cinco", "calificación"}))
    return armar(I, cierre_txt=cta, cierre_preg="RESEÑA COMPLETA EN YOUTUBE"), [len(I) // 2]
