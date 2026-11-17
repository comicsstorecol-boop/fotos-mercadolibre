"""Tema: Psicosis (1960) — reseña. Reutiliza los guiones aprobados."""
import sys
SLUG, TITULO = "psicosis", "Psicosis (1960)"
PELICULA = True    # película clásica: rayones y polvo de cine antiguo
COLORES = ((255, 60, 60), (255, 255, 255))        # rojo sangre + blanco (tema Hitchcock / ducha)
def _largo_mod():
    import r02_psicosis as L; return L
PRON = None
def largo():
    L = _largo_mod(); globals()["PRON"] = L.PRON; return L.esc, [2, 4 + len(L.H), 6 + len(L.H) + len(L.D)]
def corto(red):
    saved = sys.argv[:]; sys.argv = ["c02", red]
    try:
        sys.modules.pop('c02_psicosis', None); import c02_psicosis as C
    finally: sys.argv = saved
    globals()["PRON"] = C.L.PRON; return C.esc, C.g
import r02_psicosis as _L; PRON = _L.PRON
