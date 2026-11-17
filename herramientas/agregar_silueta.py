"""Recorta una silueta negra sobre fondo blanco -> PNG transparente en biblioteca/siluetas/<nombre>.png
Uso: python3 herramientas/agregar_silueta.py <nombre> <imagen>"""
import sys, os
from PIL import Image, ImageFilter, ImageOps
n, src = sys.argv[1], sys.argv[2]
g = Image.open(src).convert("L")
a = ImageOps.invert(g).point(lambda v: 0 if v < 40 else (255 if v > 200 else int((v - 40) * 255 / 160)))
a = a.filter(ImageFilter.MedianFilter(3))
if "--rellenar" in sys.argv:   # tapa los huecos blancos internos (caras, camisas) dejando solo el contorno
    from PIL import ImageDraw
    m = a.point(lambda v: 255 if v > 100 else 0); f = m.copy()
    ImageDraw.floodfill(f, (0, 0), 128)
    holes = f.point(lambda v: 255 if v == 0 else 0)
    from PIL import ImageChops
    a = ImageChops.lighter(a, holes.filter(ImageFilter.MaxFilter(3)))
bb = a.point(lambda v: 255 if v > 60 else 0).getbbox(); a = a.crop(bb)
out = Image.new("RGBA", a.size, (0, 0, 0, 255)); out.putalpha(a)
dst = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "biblioteca", "siluetas", f"{n}.png")
out.save(dst); print(n, out.size)
