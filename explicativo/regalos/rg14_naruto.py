"""Regalos: fans de Naruto. python3 rg14_naruto.py fb|tt salida.mp4"""
from _tema import *
S = "naruto"
G = {"productos": [
    dict(img=img(S, 1), nombre="GORRA TRUCKER AKATSUKI", precio="$29.999", nota="NUBES ROJAS"),
    dict(img=img(S, 2), nombre="TERMO PITILLO NARUTO", precio="$44.999", nota="DESDE 1999"),
    dict(img=img(S, 3), nombre="FIGURA NARUTO", precio="$69.999", nota="EL NINJA NÚMERO UNO"),
    dict(img=img(S, 4), nombre="PELUCHE ZORRO KURAMA", precio="$84.999", nota="EL ZORRO DE NUEVE COLAS"),
    dict(img=img(S, 5), nombre="MORRAL ESPALDA NARUTO", precio="$139.999", nota="PARA TODA LA ALDEA")]}
G["fb"] = [
    ("host", "¿Tienes un fan de Naruto en tu vida y no sabes qué regalarle esta Navidad? Aquí van cinco ideas de Comics Store, para todos los presupuestos.", {"navidad", "naruto"}),
    ("host", "Y quédate, porque hay un regalo que lleva por dentro… al zorro de nueve colas.", {"zorro", "colas"}),
    ("p", 1, 0, "Número uno: la gorra trucker de Akatsuki, por menos de treinta mil pesos.", {"akatsuki", "treinta"}),
    ("host", "Las nubes rojas de Akatsuki: la organización de ninjas renegados más temida de toda la serie.", {"nubes", "renegados"}, 1),
    ("p", 2, 0, "Número dos: el termo con pitillo de Naruto, por menos de cuarenta y cinco mil pesos.", {"termo", "cuarenta"}),
    ("p", 2, 1, "Naruto nació en mil novecientos noventa y nueve, en la revista Shonen Jump, de la mano de Masashi Kishimoto.", {"noventa", "kishimoto"}),
    NIVEL,
    ("p", 3, 0, "Número tres: la figura de Naruto, por menos de setenta mil pesos.", {"figura", "setenta"}),
    ("host", "El niño que todos rechazaban… y que soñaba con ser Hokage, el líder de su aldea. ¡Y lo logró!", {"hokage", "logró"}, 3),
    ("p", 4, 0, "Número cuatro: el peluche del zorro Kurama, por menos de ochenta y cinco mil pesos.", {"kurama", "ochenta"}),
    ("p", 4, 1, "El zorro de nueve colas que estaba sellado dentro de Naruto… y que terminó siendo su mejor aliado.", {"sellado", "aliado"}),
    VERDAD,
    ("p", 5, 0, "Número cinco: el morral de espalda de Naruto, por menos de ciento cuarenta mil pesos.", {"morral", "ciento"}),
    ("host", "Para el colegio, la universidad o las misiones ninja. ¿A quién se lo regalarías?", {"misiones", "regalarías"}, 5),
    CIERRE_FB("Naruto")]
G["tt"] = [
    ("host", "¿Qué le regalas a un fan de Naruto esta Navidad? Cinco ideas, de menor a mayor precio.", {"navidad", "cinco"}),
    ("p", 1, 0, "Uno: la gorra trucker de Akatsuki, menos de treinta mil.", {"akatsuki", "treinta"}),
    ("host", "Las nubes rojas de los ninjas renegados más temidos de la serie.", {"nubes"}, 1),
    ("p", 2, 0, "Dos: el termo con pitillo de Naruto, menos de cuarenta y cinco mil.", {"termo", "cuarenta"}),
    ("host", "Dato: Naruto nació en mil novecientos noventa y nueve, creado por Masashi Kishimoto.", {"kishimoto"}, 2),
    ("p", 3, 0, "Tres: la figura de Naruto, menos de setenta mil.", {"figura", "setenta"}),
    ("host", "El niño que soñaba con ser Hokage… y lo logró.", {"hokage"}, 3),
    ("p", 4, 0, "Cuatro: el peluche de Kurama, el zorro de nueve colas, menos de ochenta y cinco mil.", {"kurama", "colas"}),
    ("host", "El zorro que vivía sellado dentro de Naruto… y terminó siendo su mejor aliado.", {"aliado"}, 4),
    VERDAD_TT,
    ("p", 5, 0, "Cinco: el morral de espalda de Naruto, menos de ciento cuarenta mil.", {"morral", "ciento"}),
    ("host", "Para las misiones ninja de todos los días. ¿Cuál escoges?", {"misiones"}, 5),
    TT_EXTRA,
    CIERRE_TT]
if __name__ == "__main__":
    correr(S, G, ((255, 140, 0), (60, 140, 255)), {"naruto": ("es", "naruto"), "akatsuki": ("es", "akatsuki"), "shonen": ("es", "shónen"), "jump": ("en", "Jump"),
           "masashi": ("es", "masashi"), "kishimoto": ("es", "kishimoto"), "hokage": ("es", "jokague"), "kurama": ("es", "kurama")})
