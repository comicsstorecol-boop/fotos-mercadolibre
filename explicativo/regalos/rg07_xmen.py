"""Regalos: fans de X-Men. python3 rg07_xmen.py fb|tt salida.mp4"""
from _tema import *
S = "xmen"
G = {"productos": [
    dict(img=img(S, 1), nombre="CAMISETA WOLVERINE", precio="$54.999", nota="DEBUTÓ CONTRA HULK"),
    dict(img=img(S, 2), nombre="POLARIS X-MEN '97", precio="$174.999", nota="LA SERIE DE LOS 90 VOLVIÓ"),
    dict(img=img(S, 3), nombre="CYCLOPS X-MEN '97", precio="$189.999", nota="ÚLTIMA UNIDAD"),
    dict(img=img(S, 4), nombre="COLOSSUS MARVEL LEGENDS", precio="$299.999", nota="DESDE 1975"),
    dict(img=img(S, 5), nombre="WOLVERINE X-MEN '97", precio="$349.999", nota="LA JOYA DE LA COLECCIÓN")]}
G["fb"] = [
    ("host", "¿Tienes un fan de los X-Men en tu vida y no sabes qué regalarle esta Navidad? Aquí van cinco ideas de Comics Store… para el fan y para el coleccionista.", {"navidad", "coleccionista"}),
    ("host", "Y quédate hasta el final, porque el número cinco es el mutante más famoso de todos.", {"mutante"}),
    ("p", 1, 0, "Número uno: la camiseta de Wolverine, por menos de cincuenta y cinco mil pesos.", {"wolverine", "cincuenta"}),
    ("host", "¿Sabías que Wolverine no debutó con los X-Men? Apareció en mil novecientos setenta y cuatro… peleando contra Hulk.", {"setenta", "hulk"}, 1),
    ("p", 2, 0, "Número dos: Polaris de X-Men noventa y siete, por menos de ciento setenta y cinco mil pesos.", {"polaris", "ciento"}),
    ("p", 2, 1, "X-Men noventa y siete es la continuación de la serie animada de mil novecientos noventa y dos, con las mismas voces de siempre. Y estas figuras vienen en su caja estilo retro.", {"noventa", "retro"}),
    ("host", "Y ahora vamos con los clásicos del equipo.", {"clásicos"}),
    ("p", 3, 0, "Número tres: Cyclops de X-Men noventa y siete, por menos de ciento noventa mil pesos.", {"cyclops", "ciento"}),
    ("host", "Cyclops es uno de los X-Men originales: el equipo nació en mil novecientos sesenta y tres, creado por Stan Lee y Jack Kirby.", {"originales", "sesenta"}, 3),
    ("p", 4, 0, "Número cuatro: Colossus de Marvel Legends, por menos de trescientos mil pesos. Un gigante de acero para la vitrina.", {"colossus", "trescientos"}),
    ("p", 4, 1, "Colossus llegó en mil novecientos setenta y cinco, en el famoso Giant-Size X-Men número uno, el mismo cómic donde Wolverine se unió al equipo.", {"setenta", "wolverine"}),
    VERDAD,
    ("p", 5, 0, "Número cinco: Wolverine de X-Men noventa y siete, por menos de trescientos cincuenta mil pesos.", {"wolverine", "trescientos"}),
    ("host", "Más de cincuenta años después de aquella pelea con Hulk, sigue siendo el mejor en lo que hace. ¿Ya lo tienes?", {"mejor"}, 5),
    CIERRE_FB("los X-Men")]
G["tt"] = [
    ("host", "¿Qué le regalas a un fan de los X-Men esta Navidad? Cinco ideas, de menor a mayor precio.", {"navidad", "cinco"}),
    ("p", 1, 0, "Uno: la camiseta de Wolverine, menos de cincuenta y cinco mil.", {"wolverine", "cincuenta"}),
    ("host", "Dato: Wolverine debutó en mil novecientos setenta y cuatro… peleando contra Hulk.", {"hulk"}, 1),
    ("p", 2, 0, "Dos: Polaris de X-Men noventa y siete, menos de ciento setenta y cinco mil.", {"polaris", "ciento"}),
    ("p", 3, 0, "Tres: Cyclops, uno de los X-Men originales de mil novecientos sesenta y tres. Menos de ciento noventa mil.", {"cyclops", "originales"}),
    ("p", 4, 0, "Cuatro: Colossus de Marvel Legends, menos de trescientos mil.", {"colossus", "trescientos"}),
    VERDAD_TT,
    ("p", 5, 0, "Cinco: Wolverine de X-Men noventa y siete, menos de trescientos cincuenta mil.", {"wolverine", "trescientos"}),
    ("host", "El mejor en lo que hace… ¿ya lo tienes en tu colección?", {"colección"}, 5),
    CIERRE_TT]
if __name__ == "__main__":
    correr(S, G, ((255, 210, 0), (40, 110, 255)), {"x-men": ("en", "X-Men"), "wolverine": ("en", "Wolverine"), "polaris": ("en", "Polaris"), "cyclops": ("en", "Cyclops"), "colossus": ("en", "Colossus"), "hulk": ("es", "jolk"), "giant-size": ("en", "Giant-Size")})
