"""Regalos: fans de los Cuatro Fantásticos. python3 rg08_fantastic_four.py fb|tt salida.mp4"""
from _tema import *
S = "fantastic_four"
G = {"productos": [
    dict(img=img(S, 1), nombre="CAMISETA FANTASTIC FOUR", precio="$54.999", nota="NOVIEMBRE DE 1961"),
    dict(img=img(S, 2), nombre="ANTORCHA HUMANA RETRO", precio="$174.999", nota="¡LLAMAS ENCENDIDAS!"),
    dict(img=img(S, 3), nombre="JOHNNY STORM FIRST STEPS", precio="$194.999", nota="DE LA PELÍCULA"),
    dict(img=img(S, 4), nombre="GALACTUS TITAN HERO", precio="$199.999", nota="EL DEVORADOR DE MUNDOS"),
    dict(img=img(S, 5), nombre="LA COSA Y MUJER INVISIBLE", precio="$319.999", nota="SET DE DOS FIGURAS")]}
G["fb"] = [
    ("host", "¿Tienes un fan de los Cuatro Fantásticos en tu vida y no sabes qué regalarle esta Navidad? Aquí van cinco ideas de Comics Store.", {"navidad", "fantásticos"}),
    ("host", "Y quédate hasta el final, porque el número cinco trae a dos héroes en la misma caja.", {"dos"}),
    ("p", 1, 0, "Número uno: la camiseta de los Cuatro Fantásticos, por menos de cincuenta y cinco mil pesos.", {"camiseta", "cincuenta"}),
    ("host", "Los Cuatro Fantásticos nacieron en noviembre de mil novecientos sesenta y uno, creados por Stan Lee y Jack Kirby. Con ellos arrancó la era Marvel.", {"sesenta", "era"}, 1),
    ("p", 2, 0, "Número dos: la Antorcha Humana retro de Marvel Legends, por menos de ciento setenta y cinco mil pesos.", {"antorcha", "ciento"}),
    ("p", 2, 1, "Johnny Storm obtuvo sus poderes con los rayos cósmicos, igual que su hermana Sue, su cuñado Reed y su amigo Ben.", {"cósmicos"}),
    ("host", "Y ahora vamos con la película.", {"película"}),
    ("p", 3, 0, "Número tres: Johnny Storm de la película Los Cuatro Fantásticos: Primeros Pasos, por menos de ciento noventa y cinco mil pesos.", {"johnny", "ciento"}),
    ("host", "Y su villano más temido llegó en mil novecientos sesenta y seis: un ser cósmico que se alimenta de planetas.", {"planetas"}, 3),
    ("p", 4, 0, "Número cuatro: Galactus, el devorador de mundos, por menos de doscientos mil pesos. Una figura enorme.", {"galactus", "doscientos"}),
    ("p", 4, 1, "Galactus apareció en Fantastic Four número cuarenta y ocho, junto a su heraldo, Silver Surfer. Es una de las historias más famosas de Marvel.", {"surfer", "famosas"}),
    VERDAD,
    ("p", 5, 0, "Número cinco: La Cosa y la Mujer Invisible de Marvel Legends, por menos de trescientos veinte mil pesos. Dos figuras en una sola caja.", {"cosa", "trescientos"}),
    ("host", "Ben Grimm, el corazón del equipo, y Sue Storm, la más poderosa de los cuatro. ¿Cuál es tu favorito?", {"favorito"}, 5),
    CIERRE_FB("los Cuatro Fantásticos")]
G["tt"] = [
    ("host", "¿Qué le regalas a un fan de los Cuatro Fantásticos esta Navidad? Cinco ideas, de menor a mayor precio.", {"navidad", "cinco"}),
    ("p", 1, 0, "Uno: la camiseta de los Cuatro Fantásticos, menos de cincuenta y cinco mil.", {"camiseta", "cincuenta"}),
    ("host", "Dato: nacieron en mil novecientos sesenta y uno, y con ellos arrancó la era Marvel.", {"era"}, 1),
    ("p", 2, 0, "Dos: la Antorcha Humana retro, menos de ciento setenta y cinco mil.", {"antorcha", "ciento"}),
    ("p", 3, 0, "Tres: Johnny Storm de la película Primeros Pasos, menos de ciento noventa y cinco mil.", {"johnny", "ciento"}),
    ("p", 4, 0, "Cuatro: Galactus, el devorador de mundos, menos de doscientos mil.", {"galactus", "doscientos"}),
    VERDAD_TT,
    ("p", 5, 0, "Cinco: La Cosa y la Mujer Invisible, dos figuras en una caja, menos de trescientos veinte mil.", {"cosa", "trescientos"}),
    ("host", "Ben y Sue juntos… ¿cuál es tu favorito de los cuatro?", {"favorito"}, 5),
    CIERRE_TT]
if __name__ == "__main__":
    correr(S, G, ((40, 140, 255), (255, 255, 255)), {"johnny": ("en", "Johnny"), "storm": ("en", "Storm"), "sue": ("en", "Sue"), "reed": ("en", "Reed"), "ben": ("en", "Ben"), "grimm": ("en", "Grimm"), "galactus": ("es", "galactus"), "surfer": ("en", "Surfer"), "silver": ("en", "Silver"), "fantastic": ("en", "Fantastic"), "four": ("en", "Four")})
