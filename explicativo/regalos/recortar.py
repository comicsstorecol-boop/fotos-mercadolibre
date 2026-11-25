"""Recorta los productos (fondo blanco) de una tira descargada de Shopify (N imágenes de 1200x1200 lado a lado).
Uso: python3 recortar.py tira.jpg carpeta_salida tipo1 tipo2 ...   (tipo: 'solido' rellena huecos internos —tulas, mugs, gorras,
camisetas, hoodies, termos, mouse pads—; 'figura' conserva los huecos reales entre brazos y piernas)"""
import sys, os
import numpy as np
from PIL import Image
from scipy import ndimage
from rembg import remove, new_session
tira, out, tipos = sys.argv[1], sys.argv[2], sys.argv[3:]
os.makedirs(out, exist_ok=True); s = new_session("isnet-general-use"); T = Image.open(tira).convert("RGB"); n = len(tipos)
for i, tipo in enumerate(tipos):
    im = T.crop((i * 1200, 0, (i + 1) * 1200, 1200))
    a = np.array(remove(im, session=s, only_mask=True)); a = np.where(a < 40, 0, a)
    if tipo == "solido":
        m = ndimage.binary_closing(a > 100, iterations=3); f = ndimage.binary_erosion(ndimage.binary_fill_holes(m), iterations=3)
        a = np.maximum(a, f * 255)
    o = im.convert("RGBA"); o.putalpha(Image.fromarray(a.astype("uint8"))); o = o.crop(o.getchannel("A").getbbox())
    o.save(f"{out}/c{i + 1}.png"); print(i + 1, tipo, o.size)
