"""Regalos: fans de Iron Man y Thor (Avengers). python3 rg06_avengers.py fb|tt salida.mp4"""
from _tema import *
S = "avengers"
G = {"productos": [
    dict(img=img(S, 1), nombre="CAMISETA IRON MAN VS THANOS", precio="$54.999", nota="NACIÓ EN 1963"),
    dict(img=img(S, 2), nombre="MUG 3D MARTILLO DE THOR", precio="$99.999", nota="SOLO PARA LOS DIGNOS"),
    dict(img=img(S, 3), nombre="MIGHTY THOR LOVE AND THUNDER", precio="$159.999", nota="JANE FOSTER"),
    dict(img=img(S, 4), nombre="TONY STARK (A.I.) MARVEL LEGENDS", precio="$184.999", nota="ARMADURA CLÁSICA"),
    dict(img=img(S, 5), nombre="IRON MAN MCFARLANE 1:6", precio="$299.999", nota="¡ÚLTIMA UNIDAD!")]}
G["fb"] = [
    ("host", "¿Tienes un fan de los Vengadores en tu vida y no sabes qué regalarle esta Navidad? Hoy: Iron Man y Thor. Cinco ideas de Comics Store… para todos los bolsillos.", {"navidad", "thor"}),
    ("host", "Y quédate hasta el final, porque el número cinco es un Iron Man gigante de colección.", {"cinco"}),
    ("p", 1, 0, "Número uno: la camiseta de Iron Man contra Thanos, por menos de cincuenta y cinco mil pesos.", {"iron", "cincuenta"}),
    ("host", "Iron Man debutó en mil novecientos sesenta y tres… con una armadura gris, enorme y pesada. El rojo y dorado llegó después.", {"gris", "dorado"}, 1),
    ("p", 2, 0, "Número dos: el mug en tres de con forma del martillo de Thor, por menos de cien mil pesos.", {"martillo", "cien"}),
    ("p", 2, 1, "Mira la inscripción: quien sostenga este martillo, si es digno, poseerá el poder de Thor. Ahora tu café también tiene que ser digno.", {"digno", "thor"}),
    NIVEL,
    ("p", 3, 0, "Número tres: la Poderosa Thor de Amor y Trueno, Marvel Legends, por menos de ciento sesenta mil pesos.", {"thor", "ciento"}),
    ("host", "Thor apareció por primera vez en agosto de mil novecientos sesenta y dos, creado por Stan Lee, Larry Lieber y Jack Kirby. En esta versión, quien levanta el martillo es Jane Foster.", {"sesenta", "jane"}, 3),
    ("p", 4, 0, "Número cuatro: Tony Stark, Iron Man de Marvel Legends, por menos de ciento ochenta y cinco mil pesos.", {"stark", "ciento"}),
    ("p", 4, 1, "Con la armadura clásica roja y dorada, la que convirtió al genio millonario en un ícono de los cómics.", {"clásica", "ícono"}),
    VERDAD,
    ("p", 5, 0, "Número cinco: Iron Man de McFarlane, escala uno a seis, por menos de trescientos mil pesos. Una figura enorme para la vitrina.", {"iron", "trescientos"}),
    ("host", "Y ojo: de esta figura queda una sola unidad. El que la vea primero… se la lleva.", {"unidad"}, 5),
    CIERRE_FB("los Vengadores")]
G["tt"] = [
    ("host", "¿Qué le regalas a un fan de Iron Man y Thor esta Navidad? Cinco ideas, de menor a mayor precio.", {"navidad", "thor"}),
    ("p", 1, 0, "Uno: la camiseta de Iron Man contra Thanos, menos de cincuenta y cinco mil.", {"iron", "cincuenta"}),
    ("host", "Dato: la primera armadura de Iron Man, en mil novecientos sesenta y tres, era gris.", {"gris"}, 1),
    ("p", 2, 0, "Dos: el mug del martillo de Thor, menos de cien mil. Solo para los dignos.", {"martillo", "dignos"}),
    ("p", 3, 0, "Tres: la Poderosa Thor de Amor y Trueno, menos de ciento sesenta mil.", {"thor", "ciento"}),
    ("host", "Thor nació en mil novecientos sesenta y dos, creado por Stan Lee y Jack Kirby.", {"sesenta"}, 3),
    ("p", 4, 0, "Cuatro: Tony Stark de Marvel Legends, menos de ciento ochenta y cinco mil.", {"stark", "ciento"}),
    VERDAD_TT,
    ("p", 5, 0, "Cinco: Iron Man de McFarlane, escala uno a seis, menos de trescientos mil.", {"iron", "trescientos"}),
    ("host", "Y queda una sola unidad. ¿Para quién sería?", {"unidad"}, 5),
    CIERRE_TT]
if __name__ == "__main__":
    correr(S, G, ((235, 40, 45), (255, 200, 40)), {"iron": ("en", "Iron"), "man": ("en", "Man"), "thor": ("es", "tor"), "thanos": ("es", "tanos"), "tony": ("en", "Tony"), "stark": ("en", "Stark"), "larry": ("en", "Larry"), "lieber": ("en", "Lieber"), "jane": ("en", "Jane"), "foster": ("en", "Foster")})
