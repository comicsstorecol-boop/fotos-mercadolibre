"""Regalos: fans de Batman. python3 rg10_batman.py fb|tt salida.mp4"""
from _tema import *
S = "batman"
G = {"productos": [
    dict(img=img(S, 1), nombre="MOUSE PAD BATMAN", precio="$19.999", nota="DESDE 1939"),
    dict(img=img(S, 2), nombre="TERMO BATMAN", precio="$39.999", nota="EL MEJOR DETECTIVE"),
    dict(img=img(S, 3), nombre="HOODIE BATMAN", precio="$84.999", nota="BOB KANE Y BILL FINGER"),
    dict(img=img(S, 4), nombre="SPACE BATMAN '66 RETRO", precio="$144.999", nota="ALAS Y CASCO REMOVIBLES"),
    dict(img=img(S, 5), nombre="NIGHTWING VS TALON & OWL", precio="$320.000", nota="LA CORTE DE LOS BÚHOS")]}
G["fb"] = [
    ("host", "¿Tienes un fan de Batman en tu vida y no sabes qué regalarle esta Navidad? Aquí van cinco ideas de Comics Store, para todos los presupuestos.", {"navidad", "batman"}),
    ("host", "Y quédate hasta el final, porque el último regalo trae a los villanos más secretos de Ciudad Gótica.", {"secretos", "gótica"}),
    ("p", 1, 0, "Número uno: el mouse pad de Batman, por menos de veinte mil pesos.", {"mouse", "veinte"}),
    ("host", "Batman apareció por primera vez en mil novecientos treinta y nueve, en Detective Comics número veintisiete.", {"treinta", "detective"}, 1),
    ("p", 2, 0, "Número dos: el termo de Batman, por menos de cuarenta mil pesos.", {"termo", "cuarenta"}),
    ("p", 2, 1, "Y no es casualidad que su primera revista se llamara Detective: a Batman le dicen el mejor detective del mundo.", {"detective", "mundo"}),
    NIVEL,
    ("p", 3, 0, "Número tres: el hoodie de Batman, por menos de ochenta y cinco mil pesos.", {"hoodie", "ochenta"}),
    ("host", "Lo crearon Bob Kane y Bill Finger. Y Finger fue el que le dio la capa oscura y la máscara que hoy todos conocen.", {"finger", "capa"}, 3),
    ("p", 4, 0, "Número cuatro: Space Batman, de la línea retro de McFarlane, por menos de ciento cuarenta y cinco mil pesos.", {"space", "ciento"}),
    ("p", 4, 1, "Viene del cómic de Batman sesenta y seis, el de la serie de Adam West, y trae alas y casco removibles.", {"sesenta", "alas"}),
    VERDAD,
    ("p", 5, 0, "Número cinco: Nightwing contra Talon y el Búho, Etiqueta de Oro de McFarlane, por trescientos veinte mil pesos.", {"nightwing", "trescientos"}),
    ("host", "Tres figuras de siete pulgadas, de la saga La Corte de los Búhos: una sociedad secreta que controla Ciudad Gótica desde las sombras.", {"búhos", "sombras"}, 5),
    CIERRE_FB("Batman")]
G["tt"] = [
    ("host", "¿Qué le regalas a un fan de Batman esta Navidad? Cinco ideas, de menor a mayor precio.", {"navidad", "cinco"}),
    ("p", 1, 0, "Uno: el mouse pad de Batman, menos de veinte mil. Perfecto para el gamer de la casa.", {"mouse", "gamer"}),
    ("host", "Dato: Batman debutó en mil novecientos treinta y nueve, en Detective Comics número veintisiete.", {"treinta"}, 1),
    ("p", 2, 0, "Dos: el termo de Batman, menos de cuarenta mil.", {"termo", "cuarenta"}),
    ("host", "Por algo le dicen el mejor detective del mundo.", {"detective"}, 2),
    ("p", 3, 0, "Tres: el hoodie de Batman, menos de ochenta y cinco mil.", {"hoodie", "ochenta"}),
    ("host", "Lo crearon Bob Kane y Bill Finger. Y Finger le dio la capa oscura.", {"finger"}, 3),
    ("p", 4, 0, "Cuatro: Space Batman retro, del cómic de Batman sesenta y seis, menos de ciento cuarenta y cinco mil.", {"space", "sesenta"}),
    ("host", "Trae alas y casco removibles. Puro estilo de la serie de Adam West.", {"alas", "casco"}, 4),
    VERDAD_TT,
    ("p", 5, 0, "Cinco: Nightwing contra Talon y el Búho, Etiqueta de Oro, trescientos veinte mil.", {"nightwing", "trescientos"}),
    ("host", "La Corte de los Búhos: la sociedad secreta que controla Ciudad Gótica. ¿Cuál escoges?", {"búhos"}, 5),
    CIERRE_TT]
if __name__ == "__main__":
    correr(S, G, ((255, 214, 0), (170, 185, 210)), {"batman": ("en", "Batman"), "mouse": ("en", "mouse"), "pad": ("en", "pad"), "detective": ("es", "detectiv"),
           "comics": ("en", "Comics"), "bob": ("en", "Bob"), "kane": ("en", "Kane"), "bill": ("en", "Bill"), "finger": ("en", "Finger"), "space": ("en", "Space"),
           "adam": ("en", "Adam"), "west": ("en", "West"), "nightwing": ("en", "Nightwing"), "talon": ("en", "Talon")})
