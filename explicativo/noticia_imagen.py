"""Formato NOTICIA (Comics Store): imagen de fondo + narración + narrador abajo a la derecha + karaoke.
Uso: escenas = [(foco, frase, {claves})], foco = None (imagen completa) o fracción vertical 0..1 de la imagen donde acercar."""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
from PIL import Image, ImageFilter, ImageEnhance
from lib import W, H, marca, escena_cierre, eio
ROOT = os.path.dirname(HERE)

def armar(img_path, lista, marca_nombre="comics-store", pregunta="¿QUÉ OPINAS?", top=360, bottom=1540):
    src = Image.open(img_path).convert("RGB")
    # fondo: imagen difuminada y oscurecida a pantalla completa
    s = max(W / src.width, H / src.height); bg = src.resize((int(src.width * s), int(src.height * s)), Image.LANCZOS)
    bg = bg.crop(((bg.width - W) // 2, (bg.height - H) // 2, (bg.width - W) // 2 + W, (bg.height - H) // 2 + H))
    bg = ImageEnhance.Brightness(bg.filter(ImageFilter.GaussianBlur(40))).enhance(.35).convert("RGBA")
    # imagen principal centrada en la zona libre
    s = min(W / src.width, (bottom - top) / src.height); fg = src.resize((int(src.width * s), int(src.height * s)), Image.LANCZOS)
    fx0, fy0 = (W - fg.width) // 2, top + ((bottom - top) - fg.height) // 2
    base = bg.copy()
    from PIL import ImageDraw
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((fx0 - 6, fy0 - 6, fx0 + fg.width + 6, fy0 + fg.height + 6), 18, fill=(0, 0, 0, 200))
    base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14)))
    nar = Image.open(os.path.join(ROOT, "marcas", marca_nombre, "narrador.png")).convert("RGBA")
    nar = nar.resize((420, int(480 * nar.height / nar.width)), Image.LANCZOS)
    def zoom(z, foco):
        if z <= 1.001: return fg
        w, h = fg.width / z, fg.height / z; x0 = (fg.width - w) / 2; y0 = min(max(fg.height * foco - h / 2, 0), fg.height - h)
        return fg.crop((int(x0), int(y0), int(x0 + w), int(y0 + h))).resize(fg.size, Image.BICUBIC)
    def esc(foco, i):
        fo = foco if foco is not None else .5; z1 = 1.45 if foco is not None else 1.06
        def f(t, d):
            c = base.copy(); c.paste(zoom(1 + (z1 - 1) * eio(min(1, t / d)), fo), (fx0, fy0))
            ent = eio(min(1, t / .5)) if i == 0 else 1
            bob = math.sin(t * 9) * 6 * abs(math.sin(t * 2.3))
            c.alpha_composite(nar, (W - nar.width + 10, int(H - nar.height + 30 + bob + (1 - ent) * 400)))
            return c
        f.__name__ = f"n{i + 1:02d}"; return f
    out = [(esc(foco, i), frase, clave) for i, (foco, frase, clave) in enumerate(lista)]
    m = marca(marca_nombre)
    def cierre(t, d): return escena_cierre(m, t, d, pregunta)
    return out, cierre
