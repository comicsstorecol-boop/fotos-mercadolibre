"""Procesa un lote de camisetas.
Uso: python3 lote.py lote.json salida.xlsx
lote.json = [{"archivo": "/ruta/foto.jpg", "nombre": "Iron Maiden"}, ...]  (en orden)
- Asigna consecutivos CsXXXX desde contador.txt
- Guarda cada foto optimizada en camisetas/CsXXXX-nombre.jpg
- Genera el Excel con Título, Marca, Modelo y URL de foto
- Actualiza contador.txt (el commit/push se hace aparte)"""
import json, os, re, subprocess, sys, unicodedata
from PIL import Image, ImageOps
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(H)
BASE = "https://raw.githubusercontent.com/comicsstorecol-boop/fotos-mercadolibre/main/camisetas/"
def slug(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')[:40] or 'camiseta'
def clean(s): return re.sub(r'^camiseta\s+', '', re.sub(r'\s+', ' ', s).strip(), flags=re.I)
lote = json.load(open(sys.argv[1])); out = sys.argv[2]
n = int(open(os.path.join(H, 'contador.txt')).read().strip())
prods = []
for item in lote:
    code = f"Cs{n:04d}"; name = clean(item["nombre"])
    maxn = 60 - len("Camiseta  ") - len(code)
    titulo = f"Camiseta {name[:maxn].strip()} {code}"
    fn = f"{code}-{slug(name)}.jpg"
    im = ImageOps.exif_transpose(Image.open(item["archivo"])).convert("RGB")
    if max(im.size) > 1600: im.thumbnail((1600, 1600))
    if min(im.size) < 500: print("AVISO: foto pequeña (<500px):", item["archivo"])
    im.save(os.path.join(REPO, "camisetas", fn), "JPEG", quality=88, optimize=True)
    prods.append({"codigo": code, "titulo": titulo, "marca": name, "modelo": name, "fotos": BASE + fn})
    n += 1
json.dump(prods, open(os.path.join(H, "_productos.json"), "w"), ensure_ascii=False, indent=1)
subprocess.run(["node", os.path.join(H, "gen.js"), os.path.join(H, "_productos.json"), out], check=True)
open(os.path.join(H, 'contador.txt'), 'w').write(f"{n}\n")
for p in prods: print(p["codigo"], "|", p["titulo"], "|", p["fotos"])
