"""Guía de regalos navideños: fans de Dragon Ball. Uso:
python3 explicativo/regalos/rg01_dragon_ball.py fb|tt salida.mp4"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); EXP = os.path.dirname(HERE); sys.path.insert(0, EXP); sys.path.insert(0, os.path.dirname(EXP))
from regalos import armar
from motor import render

IMG = os.path.join(os.path.dirname(EXP), "productos", "dragon-ball")
NARANJA, AZUL = (255, 150, 20), (60, 150, 255)
PRON = {"dragon": ("en", "Dragon"), "ball": ("en", "Ball"), "capsule": ("en", "Capsule"), "corp": ("en", "Corp"), "trucker": ("en", "trucker"),
        "hoodie": ("es", "júdi"), "roshi": ("es", "róshi"), "kanji": ("es", "kanyi"), "shenlong": ("es", "shen long"), "saiyajin": ("es", "saiyayín"), "comics-store": ("es", "cómics estor")}

G = {"productos": [
    dict(img=f"{IMG}/c1.png", nombre="TULA SPORT NARANJA", precio="$26.999", nota="EL SÍMBOLO DE LA TORTUGA"),
    dict(img=f"{IMG}/c2.png", nombre="GORRA CAPSULE CORP", precio="$29.999", nota="LA EMPRESA DE BULMA"),
    dict(img=f"{IMG}/c3.png", nombre="HOODIE GOKU", precio="$84.999", nota="DESDE 1984"),
    dict(img=f"{IMG}/c4.png", nombre="MUG 3D ESFERA DEL DRAGÓN", precio="$99.999", nota="LA ESFERA DE 4 ESTRELLAS"),
    dict(img=f"{IMG}/c5.png", nombre="DIORAMA GOKU VS VEGETA", precio="$249.999", nota="¡ÚLTIMA UNIDAD!")]}

G["fb"] = [
    ("host", "¿Tienes un fan de Dragon Ball en tu vida y no sabes qué regalarle esta Navidad? Aquí van cinco ideas de Comics Store… para todos los bolsillos.", {"navidad", "bolsillos"}),
    ("host", "Y quédate hasta el final, porque el número cinco es el regalo soñado de cualquier fan.", {"cinco"}),
    ("p", 1, 0, "Número uno: la tula sport naranja de Dragon Ball, por menos de veintisiete mil pesos. Perfecta para el gimnasio, el colegio… o el amigo secreto.", {"naranja", "veintisiete"}),
    ("host", "¿Sabes qué significa ese símbolo? Es el kanji de la tortuga: el emblema de la escuela del Maestro Roshi, el que Goku llevaba en su uniforme de entrenamiento.", {"tortuga", "roshi"}, 1),
    ("p", 2, 0, "Número dos: la gorra trucker de Capsule Corp, por menos de treinta mil pesos.", {"capsule", "treinta"}),
    ("p", 2, 1, "Capsule Corp es la empresa del doctor Brief, el papá de Bulma: el genio que inventó las cápsulas que guardan casas, motos y aviones en el bolsillo. Un guiño que solo los verdaderos fans reconocen.", {"bulma", "cápsulas"}),
    ("host", "Hasta aquí, detalles económicos. Pero espera… porque ahora subimos de nivel.", {"nivel"}),
    ("p", 3, 0, "Número tres: el hoodie de Goku, por ochenta y cinco mil pesos. Ideal para las noches frías de diciembre.", {"goku", "diciembre"}),
    ("host", "Goku apareció por primera vez en mil novecientos ochenta y cuatro. Akira Toriyama lo creó inspirado en el Rey Mono de la novela china Viaje al Oeste.", {"toriyama", "mono"}, 3),
    ("p", 4, 0, "Número cuatro: el mug en tres de de la esfera del dragón, por menos de cien mil pesos. Café con poder Saiyajin todas las mañanas.", {"esfera", "saiyajin"}),
    ("p", 4, 1, "Dato para fans: la esfera de cuatro estrellas era el tesoro de Goku, el recuerdo de su abuelo Gohan. Con ella empieza toda la aventura.", {"cuatro", "gohan"}),
    ("host", "Y ahora sí… el regalo para el fan de verdad.", {"verdad"}),
    ("p", 5, 0, "Número cinco: el diorama de Goku contra Vegeta, por menos de doscientos cincuenta mil pesos. Una pieza de colección para la repisa.", {"diorama", "colección"}),
    ("host", "Vegeta, el príncipe de los Saiyajin, llegó a la Tierra como villano y terminó siendo el rival eterno de Goku. Y ojo: de este diorama queda una sola unidad.", {"príncipe", "unidad"}, 5),
    ("cierre", "Todos están en comics-store punto com punto co. ¿Cuál de los cinco le regalarías a tu fan de Dragon Ball? Déjalo en los comentarios y síguenos en Comics Store.", {"comentarios"}, "¿CUÁL REGALARÍAS?")]

G["tt"] = [
    ("host", "¿Qué le regalas a un fan de Dragon Ball esta Navidad? Cinco ideas, de menor a mayor precio. Y el último… es el regalo soñado.", {"navidad", "soñado"}),
    ("p", 1, 0, "Uno: la tula sport naranja, por menos de veintisiete mil pesos.", {"naranja", "veintisiete"}),
    ("host", "Ese símbolo es el kanji de la tortuga, el emblema de la escuela del Maestro Roshi que Goku llevaba en su uniforme.", {"tortuga"}, 1),
    ("p", 2, 0, "Dos: la gorra de Capsule Corp, la empresa del papá de Bulma. Menos de treinta mil.", {"capsule", "bulma"}),
    ("p", 3, 0, "Tres: el hoodie de Goku, ochenta y cinco mil, para el frío de diciembre.", {"goku", "diciembre"}),
    ("host", "Goku nació en mil novecientos ochenta y cuatro, inspirado en el Rey Mono de la novela china Viaje al Oeste.", {"mono"}, 3),
    ("p", 4, 0, "Cuatro: el mug en tres de de la esfera del dragón. Menos de cien mil. Café con poder Saiyajin.", {"esfera", "saiyajin"}),
    ("host", "Y el número cinco… es para el fan de verdad.", {"verdad"}),
    ("p", 5, 0, "Cinco: el diorama de Goku contra Vegeta, por menos de doscientos cincuenta mil.", {"diorama"}),
    ("host", "El príncipe de los Saiyajin contra Goku: la rivalidad más legendaria del anime. Y queda una sola unidad.", {"unidad"}, 5),
    ("cierre", "Todos están en comics-store punto com punto co. ¿Cuál regalarías tú? Comenta y síguenos en Comics Store.", {"comenta"}, "¿CUÁL REGALARÍAS?")]

if __name__ == "__main__":
    ver = sys.argv[1]; out = sys.argv[2] if len(sys.argv) > 2 else f"/home/claude/salidas/regalos_dragon_ball/{ver}.mp4"
    os.makedirs(os.path.dirname(out), exist_ok=True)
    esc, ganchos = armar(G, ver)
    render(esc, out, musica="alegre", pron=PRON, estilo="neon", y_sub=330, regancho_idx=ganchos, colores=(NARANJA, AZUL))
