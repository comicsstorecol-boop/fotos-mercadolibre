"""Guía de regalos navideños: fans de Marvel. Uso:
python3 explicativo/regalos/rg02_marvel.py fb|tt salida.mp4"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); EXP = os.path.dirname(HERE); sys.path.insert(0, EXP); sys.path.insert(0, os.path.dirname(EXP))
from regalos import armar
from motor import render

IMG = os.path.join(os.path.dirname(EXP), "productos", "marvel")
ROJO, DORADO = (235, 40, 45), (255, 200, 40)
PRON = {"marvel": ("en", "Marvel"), "groot": ("es", "grut"), "hulk": ("es", "jolk"), "iron": ("en", "Iron"), "man": ("en", "Man"),
        "spider-man": ("en", "Spider-Man"), "mcfarlane": ("en", "McFarlane"), "stan": ("en", "Stan"), "lee": ("en", "Lee"),
        "jack": ("en", "Jack"), "kirby": ("en", "Kirby"), "tony": ("en", "Tony"), "stark": ("en", "Stark"), "comics-store": ("es", "cómics estor")}

G = {"productos": [
    dict(img=f"{IMG}/c1.png", nombre="MOUSE PAD SPIDER-MAN", precio="$19.999", nota="NACIÓ EN 1962"),
    dict(img=f"{IMG}/c2.png", nombre="TERMO CAPITÁN AMÉRICA", precio="$44.999", nota="DESDE 1941"),
    dict(img=f"{IMG}/c3.png", nombre="MUG 3D HULK", precio="$84.999", nota="¡NACIÓ GRIS!"),
    dict(img=f"{IMG}/c4.png", nombre="FIGURA GROOT BAILARÍN", precio="$149.999", nota="ERA UN MONSTRUO"),
    dict(img=f"{IMG}/c5.png", nombre="IRON MAN MCFARLANE 1:6", precio="$299.999", nota="¡ÚLTIMA UNIDAD!")]}

G["fb"] = [
    ("host", "¿Tienes un fan de Marvel en tu vida y no sabes qué regalarle esta Navidad? Aquí van cinco ideas de Comics Store… para todos los bolsillos.", {"navidad", "bolsillos"}),
    ("host", "Y quédate hasta el final, porque el número cinco es una pieza de colección que pocos tienen.", {"cinco"}),
    ("p", 1, 0, "Número uno: el mouse pad de Spider-Man, por menos de veinte mil pesos. Perfecto para el gamer o para el amigo secreto.", {"spider-man", "veinte"}),
    ("host", "Spider-Man apareció por primera vez en mil novecientos sesenta y dos, en Amazing Fantasy número quince. Y hoy es el héroe más querido de Marvel.", {"sesenta"}, 1),
    ("p", 2, 0, "Número dos: el termo con pitillo del Capitán América, por menos de cuarenta y cinco mil pesos.", {"capitán", "cuarenta"}),
    ("p", 2, 1, "El Capitán América nació en marzo de mil novecientos cuarenta y uno, creado por Joe Simon y Jack Kirby. En su primera portada… le estaba dando un puño a Hitler.", {"cuarenta", "hitler"}),
    ("host", "Hasta aquí, detalles económicos. Pero espera… porque ahora subimos de nivel.", {"nivel"}),
    ("p", 3, 0, "Número tres: el mug en tres de de Hulk, por menos de ochenta y cinco mil pesos. Café con fuerza de gigante esmeralda.", {"hulk", "ochenta"}),
    ("host", "¿Sabías que Hulk no nació verde? En su primer cómic, en mil novecientos sesenta y dos, era gris. La imprenta no lograba un gris parejo… y Stan Lee lo cambió a verde.", {"gris", "verde"}, 3),
    ("p", 4, 0, "Número cuatro: la figura de Groot bailarín, por menos de ciento cincuenta mil pesos. Para el fan de los Guardianes de la Galaxia.", {"groot", "ciento"}),
    ("p", 4, 1, "Dato para fans: Groot apareció en mil novecientos sesenta como un monstruo del Planeta X que quería capturar humanos. Y en ese entonces… decía mucho más que yo soy Groot.", {"monstruo", "groot"}),
    ("host", "Y ahora sí… el regalo para el coleccionista de verdad.", {"verdad"}),
    ("p", 5, 0, "Número cinco: Iron Man de McFarlane, escala uno a seis, por menos de trescientos mil pesos. Una figura enorme para la vitrina.", {"iron", "trescientos"}),
    ("host", "Iron Man debutó en mil novecientos sesenta y tres con una armadura gris, enorme y pesada. El rojo y dorado llegó después. Y ojo: de esta figura queda una sola unidad.", {"gris", "unidad"}, 5),
    ("cierre", "Todos están en comics-store punto com punto co. ¿Cuál de los cinco le regalarías a tu fan de Marvel? Déjalo en los comentarios y síguenos en Comics Store.", {"comentarios"}, "¿CUÁL REGALARÍAS?")]

G["tt"] = [
    ("host", "¿Qué le regalas a un fan de Marvel esta Navidad? Cinco ideas, de menor a mayor precio. Y el último… es de colección.", {"navidad", "colección"}),
    ("p", 1, 0, "Uno: el mouse pad de Spider-Man, por menos de veinte mil pesos.", {"spider-man", "veinte"}),
    ("p", 2, 0, "Dos: el termo del Capitán América, el héroe que nació en mil novecientos cuarenta y uno. Menos de cuarenta y cinco mil.", {"capitán", "cuarenta"}),
    ("p", 3, 0, "Tres: el mug en tres de de Hulk, menos de ochenta y cinco mil.", {"hulk", "ochenta"}),
    ("host", "Dato: Hulk nació gris en su primer cómic. Por un problema de impresión, Stan Lee lo cambió a verde.", {"gris", "verde"}, 3),
    ("p", 4, 0, "Cuatro: Groot bailarín, menos de ciento cincuenta mil. Y sí: Groot empezó como un monstruo del Planeta X.", {"groot", "monstruo"}),
    ("host", "Y el número cinco… es para el coleccionista de verdad.", {"verdad"}),
    ("p", 5, 0, "Cinco: Iron Man de McFarlane, escala uno a seis, por menos de trescientos mil.", {"iron", "trescientos"}),
    ("host", "Una figura enorme para la vitrina… y queda una sola unidad.", {"unidad"}, 5),
    ("cierre", "Todos están en comics-store punto com punto co. ¿Cuál regalarías tú? Comenta y síguenos en Comics Store.", {"comenta"}, "¿CUÁL REGALARÍAS?")]

if __name__ == "__main__":
    ver = sys.argv[1]; out = sys.argv[2] if len(sys.argv) > 2 else f"/home/claude/salidas/regalos_marvel/{ver}.mp4"
    os.makedirs(os.path.dirname(out), exist_ok=True)
    esc, ganchos = armar(G, ver)
    render(esc, out, musica="alegre", pron=PRON, estilo="neon", y_sub=195, regancho_idx=ganchos, colores=(ROJO, DORADO))
