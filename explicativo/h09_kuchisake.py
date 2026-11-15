"""Comics Store · Terror: Kuchisake-onna (leyenda japonesa) — sin violencia gráfica"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
from compositor import historia
from motor import render
AMB = (255, 200, 120); ROJO = (220, 40, 50); AZ = (150, 190, 255)
H = [
 ({"fondo": "japon", "el": [("mujer", 540, 1300, .7, {"anim": "aparecer"}), ("mascarilla", 540, 1045, .35, {"anim": "aparecer"})], "fx": ["niebla"], "pulso": .6, "bpm": 80, "cam": (1, 1.15, 0, 40)}, "Si en Japón una mujer con mascarilla te detiene en la calle y te pregunta: ¿soy bonita?… piensa muy bien tu respuesta.", {"bonita"}),
 ({"fondo": "estudio", "el": [("libro", 540, 1050, .9, {"anim": "aparecer", "var": "Kuchisake-onna|Leyenda japonesa"})], "cam": (1, 1.06, 0, 0)}, "Se llama Kuchisake-onna, que significa: la mujer de la boca cortada. Es una de las leyendas urbanas más temidas de Japón.", {"kuchisake"}),
 ({"fondo": "ciudad_antigua", "el": [("dama", 540, 1250, .8, {"anim": "aparecer"})], "velas": [(860, 1000, 90, AMB)], "cam": (1, 1.06, 0, 0)}, "La historia empieza hace siglos, en el Japón antiguo. Una mujer muy hermosa estaba casada con un samurái celoso.", {"samurái"}),
 ({"fondo": "ciudad_antigua", "el": [("hombre", 380, 1250, .85, {"anim": "temblar"}), ("dama", 720, 1260, .75)], "vineta": .9, "pulso": .8, "bpm": 100, "cam": (1, 1.1, 0, 0)}, "Él creía que ella lo engañaba. Y en un ataque de celos, la castigó dejándole una cicatriz enorme en la cara… de oreja a oreja.", {"celos", "cicatriz"}),
 ({"fondo": "abismo", "el": [("dama", 540, 1250, .75, {"anim": "desvanecer", "t0": 1})], "fx": ["particulas"], "cam": (1, 1.08, 0, 0)}, "Ella murió poco después. Pero su espíritu, lleno de rencor, regresó al mundo de los vivos.", {"rencor"}),
 ({"fondo": "estudio", "el": [("mascarilla", 540, 1050, .8, {"anim": "aparecer"})], "cam": (1, 1.06, 0, 0)}, "Las versiones modernas cambian el origen: dicen que fue una cirugía que salió mal. Por eso esconde su rostro.", {"cirugía"}),
 ({"fondo": "japon", "el": [("mujer", 540, 1300, .7, {"anim": "caminar_der", "dist": 0}), ("mascarilla", 540, 1045, .35)], "fx": ["niebla"], "cam": (1, 1.1, 0, 0)}, "Desde entonces, dicen que camina de noche por las calles, con el rostro cubierto por una mascarilla y un abrigo largo.", {"mascarilla"}),
 ({"fondo": "calle", "el": [("nino", 380, 1440, .45), ("mujer", 680, 1330, .65, {"anim": "acercar"}), ("mascarilla", 680, 1095, .3)], "fx": ["niebla"], "pulso": .8, "bpm": 100, "cam": (1, 1.12, 0, 0)}, "Se acerca a quien camina solo, sobre todo a los niños que vuelven tarde a casa. Y le hace una sola pregunta.", {"pregunta"}),
 ({"fondo": "negro", "tag": "¿SOY BONITA?", "tag_y": 1000, "tag_col": ROJO, "pulso": 1.0, "bpm": 120, "cam": (1, 1.2, 0, 0)}, "¿Soy bonita?", {"bonita"}),
 ({"fondo": "calle", "el": [("nino", 540, 1350, .7, {"anim": "temblar"})], "fx": ["niebla"], "vineta": .9, "cam": (1, 1.1, 0, 0)}, "Si respondes que no… desapareces esa misma noche. Nadie vuelve a saber de ti.", {"no"}),
 ({"fondo": "calle", "el": [("mujer", 540, 1300, .8, {"anim": "acercar"}), ("mascarilla", 540, 1025, .4, {"anim": "desvanecer", "t0": 1.4})], "flash": True, "pulso": 1.2, "bpm": 140, "cam": (1, 1.2, 0, 0)}, "Si respondes que sí… se quita la mascarilla. Y deja ver la cicatriz que le atraviesa la cara.", {"sí", "cicatriz"}),
 ({"fondo": "negro", "el": [("tijeras", 540, 1050, .9, {"anim": "temblar"})], "glows": [(540, 1050, 260, ROJO, 90)], "pulso": 1.2, "bpm": 150, "cam": (1, 1.15, 0, 0)}, "Y vuelve a preguntar: ¿y ahora, soy bonita? Dicen que lleva unas tijeras enormes… y que ninguna respuesta parece correcta.", {"tijeras"}),
 ({"fondo": "japon", "el": [("libro", 540, 1100, .8, {"var": "¿Cómo|escapar?"})], "fx": ["niebla"], "cam": (1, 1.06, 0, 0)}, "Pero la leyenda también dice cómo escapar. Hay tres trucos.", {"escapar", "tres"}),
 ({"fondo": "japon", "el": [("nino", 540, 1350, .7)], "tag": "1 · «ERES NORMAL»", "tag_y": 700, "tag_col": AZ, "cam": (1, 1.06, 0, 0)}, "Uno: responder que es normal, ni bonita ni fea. Eso la confunde, y te da tiempo para huir.", {"normal"}),
 ({"fondo": "japon", "el": [("dulces", 540, 1150, .9, {"anim": "aparecer"})], "tag": "2 · DULCES", "tag_y": 700, "tag_col": AZ, "cam": (1, 1.06, 0, 0)}, "Dos: lanzarle dulces de fruta. Dicen que le encantan, y se detiene a recogerlos.", {"dulces"}),
 ({"fondo": "japon", "el": [("ojo", 540, 1050, .8)], "tag": "3 · «POMADA»", "tag_y": 700, "tag_col": AZ, "cam": (1, 1.06, 0, 0)}, "Y tres: decir tres veces la palabra pomada. Según la historia, al cirujano que la atendió le olía a pomada… y eso la espanta.", {"pomada"}),
 ({"fondo": "calle", "el": [("mujer", 540, 1300, .7, {"anim": "acercar"})], "fx": ["niebla"], "pulso": .9, "bpm": 120, "cam": (1, 1.15, 0, 0)}, "Pero cuidado: correr no sirve. Dicen que es más rápida que cualquier persona… y que siempre aparece delante de ti.", {"correr"}),
 ({"fondo": "ciudad_antigua", "el": [("telefono", 540, 1050, .8, {"anim": "aparecer"})], "tag": "JAPÓN · 1979", "tag_y": 700, "tag_col": ROJO, "cam": (1, 1.08, 0, 0)}, "Lo más inquietante: en mil novecientos setenta y nueve, el rumor se volvió tan real en Japón, que algunas escuelas mandaban a los niños a casa en grupo… acompañados por profesores.", {"escuelas"}),
 ({"fondo": "calle", "el": [("policia", 540, 1250, .8)], "fx": ["niebla"], "cam": (1, 1.06, 0, 0)}, "Hubo reportes de pánico en varias ciudades y hasta la policía aumentó las rondas. Nunca encontraron a nadie.", {"policía"}),
 ({"fondo": "japon", "el": [("mujer", 540, 1300, .75, {"anim": "acercar"}), ("mascarilla", 540, 1045, .35)], "fx": ["niebla"], "pulso": .9, "bpm": 100, "cam": (1, 1.2, 0, 0)}, "Así que si alguna vez, de noche, alguien con mascarilla te pregunta si es bonita… ya sabes qué decir.", {"bonita"}),
]
esc, cierre = historia(H, "comics-store", "¿QUÉ RESPONDERÍAS?")
esc.append((cierre, "¿Qué le responderías tú? Comenta y síguenos en Comics Store.", {"responderías"}))
if __name__ == "__main__":
    render(esc, sys.argv[1] if len(sys.argv) > 1 else "/home/claude/terror_09_kuchisake.mp4", regancho_idx=8, musica="terror")
