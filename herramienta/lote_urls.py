"""Lote con URLs del Gestor de fotos de Mercado Libre.
Uso: python3 lote_urls.py <tipo> lote.json salida.xlsx
  tipo = una clave de tipos.json (camiseta-adulto, camiseta-nino, ...)
  lote.json = [{"nombre": "Porky", "url": "https://http2.mlstatic.com/...-F.jpg"}, ...]  (en orden)
Cada tipo tiene su propia planilla (tallas, guía de tallas, etc.) en plantillas/.
Asigna CsXXXX desde contador.txt, genera el Excel y avanza el contador."""
import json, os, re, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__))
tipos = json.load(open(os.path.join(H, 'tipos.json')))
if len(sys.argv) != 4 or sys.argv[1] not in tipos:
    sys.exit("Uso: python3 lote_urls.py <tipo> lote.json salida.xlsx\nTipos: " + ", ".join(tipos))
T = tipos[sys.argv[1]]; lote = json.load(open(sys.argv[2])); out = sys.argv[3]
def clean(s): return re.sub(r'^camiseta\s+', '', re.sub(r'\s+', ' ', s).strip(), flags=re.I)
n = int(open(os.path.join(H, 'contador.txt')).read().strip()); prods = []
for it in lote:
    c = f"Cs{n:04d}"; nm = clean(it["nombre"])
    sobra = len(T["titulo"].format(nombre="", codigo=c))
    nm_t = nm[:60 - sobra].strip()
    prods.append({"codigo": c, "titulo": T["titulo"].format(nombre=nm_t, codigo=c), "marca": nm, "modelo": nm, "fotos": it["url"].strip()}); n += 1
json.dump(prods, open(os.path.join(H, "_productos.json"), "w"), ensure_ascii=False, indent=1)
json.dump(T["fijos"], open(os.path.join(H, "_fijos.json"), "w"), ensure_ascii=False)
subprocess.run(["node", os.path.join(H, "gen.js"), os.path.join(H, "_productos.json"), out,
                os.path.join(H, T["plantilla"]), os.path.join(H, "_fijos.json")], check=True)
open(os.path.join(H, 'contador.txt'), 'w').write(f"{n}\n")
for p in prods: print(p["codigo"], "|", p["titulo"], "|", p["fotos"])
