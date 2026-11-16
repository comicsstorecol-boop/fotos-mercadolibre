#!/usr/bin/env python3
"""FÁBRICA DE VIDEOS — Comics Store y demás páginas.

Un tema = un archivo en temas/<slug>.py que define:
    SLUG, TITULO, PRON (pronunciación), COLORES ((r,g,b) principal, (r,g,b) acento)
    largo()      -> (escenas, ganchos)   versión YouTube 5–10 min
    corto(red)   -> (escenas, ganchos)   red = "fb" (Facebook/Instagram ~2 min) o "tt" (TikTok 60–90 s)

Uso:
    python3 fabrica.py temas/psicosis.py            # las 3 versiones
    python3 fabrica.py temas/psicosis.py yt tt      # solo algunas
Salida: /home/claude/salidas/<slug>/{youtube_horizontal,fbig_vertical,tiktok_vertical}.mp4
YouTube sale en HORIZONTAL 1920x1080 nativo; Facebook/Instagram y TikTok en VERTICAL 1080x1920.
"""
import os, sys, subprocess, json, time, importlib.util
RAIZ = os.path.dirname(os.path.abspath(__file__))
VERSIONES = {"yt": ("youtube_horizontal", "horizontal"), "fb": ("fbig_vertical", "vertical"), "tt": ("tiktok_vertical", "vertical")}

def _cargar(path):
    sys.path[:0] = [os.path.join(RAIZ, "explicativo"), os.path.join(RAIZ, "explicativo", "resenas"), RAIZ]
    s = importlib.util.spec_from_file_location("tema", path); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

def render_una(path, red, out):
    """Se ejecuta en un proceso aparte (el formato se fija al importar)."""
    m = _cargar(path)
    from motor import render
    esc, g = m.largo() if red == "yt" else m.corto(red)
    render(esc, out, musica=getattr(m, "MUSICA", "terror"), pron=m.PRON, estilo="neon", y_sub=330, regancho_idx=g, colores=getattr(m, "COLORES", None),
           formato=VERSIONES[red][1])

def main():
    if len(sys.argv) > 2 and sys.argv[1] == "--una": return render_una(sys.argv[2], sys.argv[3], sys.argv[4])
    path = sys.argv[1]; redes = sys.argv[2:] or ["yt", "fb", "tt"]
    slug = os.path.splitext(os.path.basename(path))[0]; dest = f"/home/claude/salidas/{slug}"; os.makedirs(dest, exist_ok=True)
    for red in redes:
        nombre, fmt = VERSIONES[red]; out = f"{dest}/{nombre}.mp4"
        env = dict(os.environ, FORMATO=fmt); t0 = time.time()
        with open(f"{dest}/{red}.log", "w") as lg:
            r = subprocess.run([sys.executable, __file__, "--una", path, red, out], env=env, stdout=lg, stderr=subprocess.STDOUT)
        estado = "LISTO" if r.returncode == 0 and os.path.exists(out) else "ERROR"
        print(f"{estado} {red} {out} ({(time.time() - t0) / 60:.0f} min)", flush=True)
        cat = os.path.join(RAIZ, "catalogo.json"); data = json.load(open(cat)) if os.path.exists(cat) else {}
        data.setdefault(slug, {})[red] = {"estado": estado, "fecha": time.strftime("%Y-%m-%d")}
        json.dump(data, open(cat, "w"), indent=1, ensure_ascii=False)

if __name__ == "__main__": main()
