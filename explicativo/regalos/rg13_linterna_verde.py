"""Regalos: fans de Linterna Verde. python3 rg13_linterna_verde.py fb|tt salida.mp4"""
from _tema import *
S = "linterna_verde"
G = {"productos": [
    dict(img=img(S, 1), nombre="CAMISETA GREEN LANTERN BLACK", precio="$54.999", nota="DESDE 1940"),
    dict(img=img(S, 2), nombre="HOODIE CAPOTA GREEN LANTERN", precio="$89.999", nota="HAL JORDAN · 1959"),
    dict(img=img(S, 3), nombre="HAL JORDAN PAGE PUNCHERS", precio="$99.999", nota="¡TRAE SU CÓMIC!"),
    dict(img=img(S, 4), nombre="ALCANCÍA GREEN LANTERN", precio="$174.999", nota="AHORRA CON EL ANILLO"),
    dict(img=img(S, 5), nombre="ISAMOT KOL MOVIE MASTERS", precio="$174.999", nota="PELÍCULA DE 2011")]}
G["fb"] = [
    ("host", "¿Tienes un fan de Linterna Verde en tu vida y no sabes qué regalarle esta Navidad? Aquí van cinco ideas de Comics Store.", {"navidad", "linterna"}),
    ("host", "Y quédate, porque el último es un Linterna que muy pocos conocen.", {"pocos"}),
    ("p", 1, 0, "Número uno: la camiseta negra de Green Lantern, por menos de cincuenta y cinco mil pesos.", {"camiseta", "cincuenta"}),
    ("host", "El primer Linterna Verde, Alan Scott, apareció en mil novecientos cuarenta. Su anillo era mágico.", {"cuarenta", "mágico"}, 1),
    ("p", 2, 0, "Número dos: el hoodie verde de Green Lantern, por menos de noventa mil pesos.", {"hoodie", "noventa"}),
    ("p", 2, 1, "Y en mil novecientos cincuenta y nueve llegó Hal Jordan, un piloto de pruebas que recibió su anillo de un alienígena.", {"hal", "piloto"}),
    NIVEL,
    ("p", 3, 0, "Número tres: Hal Jordan de Page Punchers, de McFarlane, por menos de cien mil pesos.", {"punchers", "cien"}),
    ("host", "Y lo mejor: viene con su propio cómic, Green Lantern Rebirth.", {"cómic", "rebirth"}, 3),
    ("p", 4, 0, "Número cuatro: la alcancía de Green Lantern, por menos de ciento setenta y cinco mil pesos.", {"alcancía", "ciento"}),
    ("p", 4, 1, "Un busto de Hal Jordan para el escritorio… que además guarda los ahorros para el próximo regalo.", {"busto", "ahorros"}),
    VERDAD,
    ("p", 5, 0, "Número cinco: Isamot Kol, de la línea Movie Masters, por menos de ciento setenta y cinco mil pesos.", {"isamot", "ciento"}),
    ("host", "Un miembro de la Tropa de los Linternas Verdes, de la película de dos mil once. Una pieza rara para el coleccionista.", {"tropa", "rara"}, 5),
    CIERRE_FB("Linterna Verde")]
G["tt"] = [
    ("host", "¿Qué le regalas a un fan de Linterna Verde esta Navidad? Cinco ideas, de menor a mayor precio.", {"navidad", "cinco"}),
    ("p", 1, 0, "Uno: la camiseta negra de Green Lantern, menos de cincuenta y cinco mil.", {"camiseta", "cincuenta"}),
    ("host", "Dato: el primer Linterna Verde apareció en mil novecientos cuarenta… y su anillo era mágico.", {"mágico"}, 1),
    ("p", 2, 0, "Dos: el hoodie verde, menos de noventa mil.", {"hoodie", "noventa"}),
    ("host", "Hal Jordan llegó en mil novecientos cincuenta y nueve: un piloto de pruebas.", {"hal", "piloto"}, 2),
    ("p", 3, 0, "Tres: Hal Jordan de Page Punchers, menos de cien mil. ¡Y trae su cómic!", {"punchers", "cómic"}),
    ("p", 4, 0, "Cuatro: la alcancía de Green Lantern, menos de ciento setenta y cinco mil.", {"alcancía", "ciento"}),
    ("host", "Un busto de Hal Jordan que además guarda tus ahorros.", {"busto", "ahorros"}, 4),
    VERDAD_TT,
    ("p", 5, 0, "Cinco: Isamot Kol, de la Tropa de los Linternas Verdes, menos de ciento setenta y cinco mil.", {"isamot", "tropa"}),
    ("host", "Sale en la película de dos mil once. Una pieza rara. ¿Cuál escoges?", {"rara"}, 5),
    TT_EXTRA,
    CIERRE_TT]
if __name__ == "__main__":
    correr(S, G, ((40, 230, 80), (230, 230, 240)), {"green": ("en", "Green"), "lantern": ("en", "Lantern"), "alan": ("en", "Alan"), "scott": ("en", "Scott"),
           "hal": ("en", "Hal"), "jordan": ("en", "Jordan"), "page": ("en", "Page"), "punchers": ("en", "Punchers"), "rebirth": ("en", "Rebirth"),
           "isamot": ("en", "Isamot"), "kol": ("en", "Kol"), "movie": ("en", "Movie"), "masters": ("en", "Masters")})
