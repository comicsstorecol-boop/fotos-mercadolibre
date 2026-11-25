"""Regalos: fans de Guardianes de la Galaxia. python3 rg09_guardianes.py fb|tt salida.mp4"""
from _tema import *
S = "guardianes"
G = {"productos": [
    dict(img=img(S, 1), nombre="CAMISETA GROOT WANTED", precio="$54.999", nota="ERA UN MONSTRUO"),
    dict(img=img(S, 2), nombre="GROOT BAILARÍN", precio="$149.999", nota="¡BAILA Y SUENA!"),
    dict(img=img(S, 3), nombre="STAR-LORD MARVEL LEGENDS", precio="$164.999", nota="DESDE 1976"),
    dict(img=img(S, 4), nombre="ROCKET MARVEL LEGENDS", precio="$164.999", nota="NOMBRE DE UNA CANCIÓN"),
    dict(img=img(S, 5), nombre="NEBULA MARVEL LEGENDS", precio="$174.999", nota="HIJA DE THANOS")]}
G["fb"] = [
    ("host", "¿Tienes un fan de los Guardianes de la Galaxia en tu vida y no sabes qué regalarle esta Navidad? Aquí van cinco ideas de Comics Store.", {"navidad", "guardianes"}),
    ("host", "Y quédate hasta el final, porque hay un dato de Rocket que casi nadie conoce.", {"rocket"}),
    ("p", 1, 0, "Número uno: la camiseta de Groot buscado, por menos de cincuenta y cinco mil pesos.", {"groot", "cincuenta"}),
    ("host", "Groot apareció en mil novecientos sesenta… como un monstruo del Planeta X que quería capturar humanos. Y en ese entonces decía mucho más que yo soy Groot.", {"monstruo", "groot"}, 1),
    ("p", 2, 0, "Número dos: el Groot bailarín, por menos de ciento cincuenta mil pesos. Baila al ritmo de la música, como en la película.", {"bailarín", "ciento"}),
    ("p", 2, 1, "El regalo perfecto para el escritorio: cada vez que suena, todo el mundo voltea a mirar.", {"escritorio"}),
    ("host", "Y ahora vamos con el equipo completo.", {"equipo"}),
    ("p", 3, 0, "Número tres: Star-Lord de Marvel Legends, por menos de ciento sesenta y cinco mil pesos.", {"star-lord", "ciento"}),
    ("host", "Star-Lord debutó en mil novecientos setenta y seis, en la revista Marvel Preview. Tres números después… llegó Rocket.", {"setenta", "rocket"}, 3),
    ("p", 4, 0, "Número cuatro: Rocket de Marvel Legends, por menos de ciento sesenta y cinco mil pesos.", {"rocket", "ciento"}),
    ("p", 4, 1, "Aquí va el dato: su nombre viene de una canción de los Beatles, Rocky Raccoon, del Álbum Blanco de mil novecientos sesenta y ocho.", {"beatles", "rocky"}),
    ("host", "Y para cerrar… la villana que se volvió heroína.", {"heroína"}),
    ("p", 5, 0, "Número cinco: Nebula de Marvel Legends, por menos de ciento setenta y cinco mil pesos.", {"nebula", "ciento"}),
    ("host", "La hija de Thanos que terminó del lado de los Guardianes. ¿Cuál es tu favorito del equipo?", {"thanos", "favorito"}, 5),
    CIERRE_FB("los Guardianes de la Galaxia")]
G["tt"] = [
    ("host", "¿Qué le regalas a un fan de los Guardianes de la Galaxia esta Navidad? Cinco ideas, de menor a mayor precio.", {"navidad", "cinco"}),
    ("p", 1, 0, "Uno: la camiseta de Groot buscado, menos de cincuenta y cinco mil.", {"groot", "cincuenta"}),
    ("host", "Dato: Groot empezó en mil novecientos sesenta como un monstruo del Planeta X.", {"monstruo"}, 1),
    ("p", 2, 0, "Dos: el Groot bailarín, menos de ciento cincuenta mil.", {"bailarín", "ciento"}),
    ("p", 3, 0, "Tres: Star-Lord de Marvel Legends, menos de ciento sesenta y cinco mil.", {"star-lord", "ciento"}),
    ("p", 4, 0, "Cuatro: Rocket. Su nombre viene de la canción Rocky Raccoon, de los Beatles.", {"rocket", "beatles"}),
    ("host", "Y el número cinco… la villana que se volvió heroína.", {"heroína"}),
    ("p", 5, 0, "Cinco: Nebula, la hija de Thanos, menos de ciento setenta y cinco mil.", {"nebula", "thanos"}),
    ("host", "¿Cuál es tu favorito de los Guardianes?", {"favorito"}, 5),
    CIERRE_TT]
if __name__ == "__main__":
    correr(S, G, ((255, 120, 40), (190, 80, 255)), {"groot": ("es", "grut"), "star-lord": ("en", "Star-Lord"), "rocket": ("en", "Rocket"), "rocky": ("en", "Rocky"), "raccoon": ("en", "Raccoon"), "beatles": ("en", "Beatles"), "nebula": ("en", "Nebula"), "thanos": ("es", "tanos"), "preview": ("en", "Preview")})
