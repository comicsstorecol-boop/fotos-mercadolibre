"""Formato NOTICIA (Comics Store): la imagen llena toda la pantalla con acercamientos/alejamientos,
narrador hablando abajo a la derecha y subtítulos karaoke neón.
Cada escena: (mov, frase, {claves}); mov = (z0, z1, (x0, y0), (x1, y1)) con x,y en fracción de la imagen (0..1)."""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
from PIL import Image
from lib import W, H, marca, escena_cierre, eio
import generador as G
import motor

def armar(img_path, lista, marca_nombre="comics-store", pregunta="¿QUÉ OPINAS?", narrador_px=470):
    src = Image.open(img_path).convert("RGB"); SW, SH = src.size
    G.load_brand(marca_nombre); kind = next(iter(G.CHAR)); G.CHAR[kind]["drop"] = int(G.CHAR[kind]["drop"] * 1.9)
    def encuadre(z, cx, cy):
        h = min(SH, SW * H / W) / z; w = h * W / H          # recorte 9:16 que cubre la pantalla
        x0 = min(max(cx * SW - w / 2, 0), SW - w); y0 = min(max(cy * SH - h / 2, 0), SH - h)
        return src.resize((W, H), Image.BICUBIC, box=(x0, y0, x0 + w, y0 + h))
    def esc(mov, i):
        z0, z1, (ax, ay), (bx, by) = mov
        def f(t, d):
            k = eio(min(1, t / d)); c = encuadre(z0 + (z1 - z0) * k, ax + (bx - ax) * k, ay + (by - ay) * k).convert("RGBA")
            # sombra suave abajo para que resalte el narrador
            blink = (t % 3.7) < .12
            n = G.character(kind, narrador_px, min(1., motor.NIVEL * 1.4), blink)
            ent = eio(min(1, t / .45)) if i == 0 else 1
            bob = math.sin(t * 2.4) * 5 + motor.NIVEL * -6
            c.alpha_composite(n, (W - narrador_px + 20, int(H - narrador_px + 30 + bob + (1 - ent) * 500)))
            return c
        f.__name__ = f"n{i + 1:02d}"; return f
    out = [(esc(mov, i), frase, clave) for i, (mov, frase, clave) in enumerate(lista)]
    m = marca(marca_nombre)
    def cierre(t, d): return escena_cierre(m, t, d, pregunta)
    return out, cierre
