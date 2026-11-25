"""Plantilla común: cada tema define PRODUCTOS, FB, TT, COLORES y PRON extra."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); EXP = os.path.dirname(HERE); sys.path.insert(0, EXP); sys.path.insert(0, os.path.dirname(EXP))
PRON_BASE = {"comics-store": ("es", "cómics estor"), "marvel": ("en", "Marvel"), "legends": ("en", "Legends"), "stan": ("en", "Stan"), "lee": ("en", "Lee"),
             "jack": ("en", "Jack"), "kirby": ("en", "Kirby"), "hoodie": ("es", "júdi"), "trucker": ("en", "trucker"), "mcfarlane": ("en", "McFarlane")}
def correr(slug, G, colores, pron=None):
    from regalos import armar
    from motor import render
    ver = sys.argv[1]; out = sys.argv[2] if len(sys.argv) > 2 else f"/home/claude/salidas/regalos_{slug}/{ver}.mp4"
    os.makedirs(os.path.dirname(out), exist_ok=True)
    esc, ganchos = armar(G, ver)
    render(esc, out, musica="alegre", pron={**PRON_BASE, **(pron or {})}, estilo="neon", y_sub=195, regancho_idx=ganchos, colores=colores)
def img(slug, i): return os.path.join(os.path.dirname(EXP), "productos", slug, f"c{i}.png")
CIERRE_FB = lambda fan: ("cierre", f"Todos están en comics-store punto com punto co. ¿Cuál de los cinco le regalarías a tu fan de {fan}? Déjalo en los comentarios y síguenos en Comics Store.", {"comentarios"}, "¿CUÁL REGALARÍAS?")
CIERRE_TT = ("cierre", "Todos están en comics-store punto com punto co. ¿Cuál regalarías tú? Comenta y síguenos en Comics Store.", {"comenta"}, "¿CUÁL REGALARÍAS?")
NIVEL = ("host", "Hasta aquí, detalles económicos. Pero espera… porque ahora subimos de nivel.", {"nivel"})
VERDAD = ("host", "Y ahora sí… el regalo para el coleccionista de verdad.", {"verdad"})
VERDAD_TT = ("host", "Y el número cinco… es para el coleccionista de verdad.", {"verdad"})
