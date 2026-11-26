"""Regalos: fans de Demon Slayer. python3 rg16_demon_slayer.py fb|tt salida.mp4"""
from _tema import *
S = "demon_slayer"
G = {"productos": [
    dict(img=img(S, 1), nombre="CAMISETA TANJIRO", precio="$54.999", nota="DESDE 2016"),
    dict(img=img(S, 2), nombre="CAMISETA ZENITSU", precio="$54.999", nota="RESPIRACIÓN DEL TRUENO"),
    dict(img=img(S, 3), nombre="FIGURA ZENITSU AGATSUMA", precio="$99.999", nota="¡FUERTE DORMIDO!"),
    dict(img=img(S, 4), nombre="JUEGO DE 6 FIGURAS", precio="$124.999", nota="TODO EL EQUIPO"),
    dict(img=img(S, 5), nombre="FIGURA MUZAN KIBUTSUJI", precio="$144.999", nota="EL REY DE LOS DEMONIOS")]}
G["fb"] = [
    ("host", "¿Tienes un fan de Demon Slayer en tu vida y no sabes qué regalarle esta Navidad? Aquí van cinco ideas de Comics Store, para todos los presupuestos.", {"navidad", "slayer"}),
    ("host", "Y quédate hasta el final, porque ahí aparece el villano más temido de la serie.", {"villano", "temido"}),
    ("p", 1, 0, "Número uno: la camiseta de Tanjiro, por menos de cincuenta y cinco mil pesos.", {"tanjiro", "cincuenta"}),
    ("host", "Demon Slayer, o Kimetsu no Yaiba, nació en dos mil dieciséis, creado por Koyoharu Gotouge.", {"dieciséis", "gotouge"}, 1),
    ("p", 2, 0, "Número dos: la camiseta de Zenitsu, también por menos de cincuenta y cinco mil pesos.", {"zenitsu", "cincuenta"}),
    ("p", 2, 1, "Y aquí va el dato: la película del Tren Infinito sigue siendo la más taquillera de la historia en Japón.", {"tren", "japón"}),
    NIVEL,
    ("p", 3, 0, "Número tres: la figura de Zenitsu Agatsuma, por menos de cien mil pesos.", {"figura", "cien"}),
    ("host", "El más miedoso del grupo… que se vuelve imparable cuando se queda dormido.", {"miedoso", "dormido"}, 3),
    ("p", 4, 0, "Número cuatro: el juego de seis figuras de Demon Slayer, por menos de ciento veinticinco mil pesos.", {"seis", "ciento"}),
    ("p", 4, 1, "Tanjiro, Nezuko, Zenitsu, Inosuke, Giyu y Shinobu: el equipo completo en una sola caja.", {"nezuko", "equipo"}),
    VERDAD,
    ("p", 5, 0, "Número cinco: la figura de Muzan Kibutsuji, por menos de ciento cuarenta y cinco mil pesos.", {"muzan", "ciento"}),
    ("host", "El primer demonio y el rey de todos ellos. El villano que todo fan ama odiar.", {"rey", "odiar"}, 5),
    CIERRE_FB("Demon Slayer")]
G["tt"] = [
    ("host", "¿Qué le regalas a un fan de Demon Slayer esta Navidad? Cinco ideas, de menor a mayor precio.", {"navidad", "cinco"}),
    ("p", 1, 0, "Uno: la camiseta de Tanjiro, menos de cincuenta y cinco mil.", {"tanjiro", "cincuenta"}),
    ("host", "Dato: Demon Slayer nació en dos mil dieciséis, creado por Koyoharu Gotouge.", {"gotouge"}, 1),
    ("p", 2, 0, "Dos: la camiseta de Zenitsu, menos de cincuenta y cinco mil.", {"zenitsu", "cincuenta"}),
    ("host", "Su película del Tren Infinito sigue siendo la más taquillera de Japón.", {"tren"}, 2),
    ("p", 3, 0, "Tres: la figura de Zenitsu, que pelea mejor dormido, menos de cien mil.", {"dormido", "cien"}),
    ("p", 4, 0, "Cuatro: el juego de seis figuras, con todo el equipo, menos de ciento veinticinco mil.", {"seis", "equipo"}),
    ("host", "Tanjiro, Nezuko, Zenitsu, Inosuke, Giyu y Shinobu, en una sola caja.", {"nezuko"}, 4),
    VERDAD_TT,
    ("p", 5, 0, "Cinco: Muzan Kibutsuji, el rey de los demonios, menos de ciento cuarenta y cinco mil.", {"muzan", "demonios"}),
    ("host", "El villano que todo fan ama odiar. ¿Cuál escoges?", {"odiar"}, 5),
    TT_EXTRA,
    CIERRE_TT]
if __name__ == "__main__":
    correr(S, G, ((40, 210, 160), (255, 100, 150)), {"demon": ("en", "Demon"), "slayer": ("en", "Slayer"), "kimetsu": ("es", "kimetsu"), "yaiba": ("es", "yaiba"),
           "koyoharu": ("es", "koyojaru"), "gotouge": ("es", "gotóge"), "tanjiro": ("es", "tanyiro"), "zenitsu": ("es", "zenitsu"), "agatsuma": ("es", "agatsuma"),
           "nezuko": ("es", "nezuko"), "inosuke": ("es", "inosuke"), "giyu": ("es", "guiyu"), "shinobu": ("es", "shinobu"), "muzan": ("es", "muzan"), "kibutsuji": ("es", "kibutsuyi")})
