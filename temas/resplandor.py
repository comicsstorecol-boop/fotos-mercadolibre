"""Tema: El resplandor (1980) — reseña. Escenas clave resplandor_r01..r14 en biblioteca."""
import sys
SLUG, TITULO = "resplandor", "El resplandor (1980)"
PELICULA = True
COLORES = ((255, 140, 40), (255, 255, 255))        # naranja alfombra/hotel + blanco nieve
PRON = None
def largo():
    sys.modules.pop("r03_resplandor", None); import r03_resplandor as L
    globals()["PRON"] = L.PRON; return L.esc, [2, 4 + len(L.H), 6 + len(L.H) + len(L.D)]
def corto(red):
    saved = sys.argv[:]; sys.argv = ["cortos", "resplandor", red]
    try:
        sys.modules.pop("cortos", None); import cortos as C
    finally: sys.argv = saved
    globals()["PRON"] = C.L.PRON; return C.esc, C.g
