"""Lote con URLs del Gestor de fotos de Mercado Libre.
Uso: python3 lote_urls.py lote.json salida.xlsx
lote.json = [{"nombre": "Porky", "url": "https://http2.mlstatic.com/...-F.jpg"}, ...]  (en orden)
Asigna CsXXXX desde contador.txt, genera el Excel (4 tallas S-M-L-XL por camiseta) y avanza el contador."""
import json, os, re, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__))
def clean(s): return re.sub(r'^camiseta\s+', '', re.sub(r'\s+', ' ', s).strip(), flags=re.I)
lote = json.load(open(sys.argv[1])); out = sys.argv[2]
n = int(open(os.path.join(H, 'contador.txt')).read().strip()); prods = []
for it in lote:
    c = f"Cs{n:04d}"; nm = clean(it["nombre"]); maxn = 60 - len("Camiseta  ") - len(c)
    prods.append({"codigo": c, "titulo": f"Camiseta {nm[:maxn].strip()} {c}", "marca": nm, "modelo": nm, "fotos": it["url"].strip()}); n += 1
json.dump(prods, open(os.path.join(H, "_productos.json"), "w"), ensure_ascii=False, indent=1)
subprocess.run(["node", os.path.join(H, "gen.js"), os.path.join(H, "_productos.json"), out], check=True)
open(os.path.join(H, 'contador.txt'), 'w').write(f"{n}\n")
for p in prods: print(p["codigo"], "|", p["titulo"], "|", p["fotos"])
