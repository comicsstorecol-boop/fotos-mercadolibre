"""Regalos: fans de Superman. python3 rg11_superman.py fb|tt salida.mp4"""
from _tema import *
S = "superman"
G = {"productos": [
    dict(img=img(S, 1), nombre="TULA SPORT SUPERMAN", precio="$24.999", nota="DESDE 1938"),
    dict(img=img(S, 2), nombre="CAMISETA ESCUDO SUPERMAN", precio="$44.999", nota="AL PRINCIPIO NO VOLABA"),
    dict(img=img(S, 3), nombre="HOODIE SUPERMAN BLACK", precio="$89.999", nota="SÍMBOLO DE ESPERANZA"),
    dict(img=img(S, 4), nombre="SUPERMAN THE MOVIE 1978", precio="$194.999", nota="CHRISTOPHER REEVE"),
    dict(img=img(S, 5), nombre="SUPERMAN PAGE PUNCHERS", precio="$219.999", nota="¡TRAE SU CÓMIC!")]}
G["fb"] = [
    ("host", "¿Tienes un fan de Superman en tu vida y no sabes qué regalarle esta Navidad? Aquí van cinco ideas de Comics Store, para todos los presupuestos.", {"navidad", "superman"}),
    ("host", "Y quédate, porque hay un dato del hombre de acero que casi nadie sabe.", {"acero", "dato"}),
    ("p", 1, 0, "Número uno: la tula sport de Superman, por menos de veinticinco mil pesos.", {"tula", "veinticinco"}),
    ("host", "Superman nació en mil novecientos treinta y ocho, en Action Comics número uno, creado por Jerry Siegel y Joe Shuster.", {"treinta", "action"}, 1),
    ("p", 2, 0, "Número dos: la camiseta con el escudo de Superman, por menos de cuarenta y cinco mil pesos.", {"escudo", "cuarenta"}),
    ("p", 2, 1, "Y aquí va el dato: al principio Superman no volaba. Solo saltaba, tan alto como un edificio.", {"volaba", "saltaba"}),
    NIVEL,
    ("p", 3, 0, "Número tres: el hoodie negro de Superman, por menos de noventa mil pesos.", {"hoodie", "noventa"}),
    ("host", "En las películas modernas, la S del escudo es el símbolo de su familia… y significa esperanza.", {"esperanza"}, 3),
    ("p", 4, 0, "Número cuatro: Superman de la película de mil novecientos setenta y ocho, de McFarlane, por menos de ciento noventa y cinco mil pesos.", {"setenta", "ciento"}),
    ("p", 4, 1, "El Superman de Christopher Reeve: la película que convenció al mundo de que un hombre podía volar.", {"reeve", "volar"}),
    VERDAD,
    ("p", 5, 0, "Número cinco: Superman de Page Punchers, de McFarlane, por menos de doscientos veinte mil pesos.", {"punchers", "doscientos"}),
    ("host", "Y lo mejor: la figura viene con su propio cómic. Regalo doble para el fan de Superman.", {"cómic", "doble"}, 5),
    CIERRE_FB("Superman")]
G["tt"] = [
    ("host", "¿Qué le regalas a un fan de Superman esta Navidad? Cinco ideas, de menor a mayor precio.", {"navidad", "cinco"}),
    ("p", 1, 0, "Uno: la tula sport de Superman, menos de veinticinco mil.", {"tula", "veinticinco"}),
    ("host", "Dato: Superman debutó en mil novecientos treinta y ocho, en Action Comics número uno.", {"treinta"}, 1),
    ("p", 2, 0, "Dos: la camiseta del escudo, menos de cuarenta y cinco mil.", {"escudo", "cuarenta"}),
    ("host", "¿Sabías que al principio Superman no volaba? Solo saltaba edificios.", {"volaba"}, 2),
    ("p", 3, 0, "Tres: el hoodie negro de Superman, menos de noventa mil.", {"hoodie", "noventa"}),
    ("host", "Y en las películas modernas, su S significa esperanza.", {"esperanza"}, 3),
    ("p", 4, 0, "Cuatro: el Superman de Christopher Reeve, de la película de mil novecientos setenta y ocho.", {"reeve", "setenta"}),
    VERDAD_TT,
    ("p", 5, 0, "Cinco: Superman de Page Punchers, menos de doscientos veinte mil. ¡Y trae su propio cómic!", {"punchers", "cómic"}),
    ("host", "¿Cuál de los cinco escoges?", {"escoges"}, 5),
    CIERRE_TT]
if __name__ == "__main__":
    correr(S, G, ((235, 40, 40), (60, 130, 255)), {"superman": ("en", "Superman"), "action": ("en", "Action"), "comics": ("en", "Comics"), "jerry": ("en", "Jerry"),
           "siegel": ("en", "Siegel"), "joe": ("en", "Joe"), "shuster": ("en", "Shuster"), "christopher": ("en", "Christopher"), "reeve": ("en", "Reeve"),
           "page": ("en", "Page"), "punchers": ("en", "Punchers")})
