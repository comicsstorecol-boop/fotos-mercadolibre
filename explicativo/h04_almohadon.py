"""Comics Store · Terror: El almohadón de plumas (Horacio Quiroga, 1907)"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
from compositor import historia
from motor import render
AMB = (255, 200, 120); AZ = (160, 190, 255); ROJO = (200, 30, 50)
H = [
 ({"fondo": "habitacion", "el": [("almohadon", 360, 1170, .45, {"anim": "latir"})], "vineta": .85, "cam": (1, 1.15, -80, 40)}, "Este es uno de los cuentos más perturbadores de América Latina. Y todo ocurre… en una almohada.", {"almohada"}),
 ({"fondo": "fiesta", "el": [("hombre", 420, 1250, .8), ("dama", 660, 1250, .75)], "velas": [(270, 380, 120, AMB), (810, 380, 120, AMB)], "cam": (1, 1.08, 0, 0)}, "Alicia y Jordán acababan de casarse. Ella era dulce y tímida. Él, serio y frío.", {"alicia", "jordán"}),
 ({"fondo": "casa", "fx": ["niebla"], "vineta": .7, "cam": (1, 1.1, 0, 60)}, "Se fueron a vivir a una casa enorme, blanca y silenciosa. Sus pisos de mármol hacían que todo se sintiera helado.", {"helado"}),
 ({"fondo": "pasillo", "el": [("dama", 540, 1300, .45, {"anim": "caminar_der", "dist": 60})], "vineta": .8, "cam": (1, 1.1, 0, 0)}, "Alicia pasaba los días sola, caminando por los pasillos. Esperando un cariño que no llegaba.", {"sola"}),
 ({"fondo": "habitacion", "el": [("dama", 540, 1140, .6, {"anim": "aparecer"})], "pulso": .4, "bpm": 70, "cam": (1, 1.08, 0, 0)}, "Muy pronto empezó a adelgazar. Se veía pálida, cansada… cada día más débil.", {"pálida", "débil"}),
 ({"fondo": "habitacion", "vineta": .85, "cam": (1, 1.08, 0, 30)}, "Una tarde se desmayó, y desde ese día ya no pudo levantarse de la cama.", {"cama"}),
 ({"fondo": "habitacion", "el": [("anciano", 300, 1250, .8), ("libro", 760, 1050, .5, {"var": "Diagnóstico|?"})], "cam": (1, 1.06, 0, 0)}, "Llamaron al médico. La examinó y no encontró nada… solo una anemia que avanzaba sin explicación.", {"anemia"}),
 ({"fondo": "habitacion", "el": [("sombra", 820, 1300, .5, {"anim": "aparecer"})], "pulso": .8, "bpm": 100, "vineta": .9, "cam": (1, 1.15, 100, 40)}, "En las noches, Alicia deliraba. Decía ver una criatura en la alfombra… con los ojos fijos en ella.", {"criatura", "ojos"}),
 ({"fondo": "habitacion", "el": [("hombre", 760, 1250, .8, {"anim": "temblar"})], "vineta": .8, "cam": (1, 1.08, 0, 0)}, "Jordán no se separaba de ella. Por primera vez, tenía miedo de perderla.", {"miedo"}),
 ({"fondo": "habitacion", "pulso": .7, "bpm": 80, "cam": (1, 1.1, 0, 40)}, "Lo extraño era esto: en las mañanas, Alicia parecía mejorar… pero cada noche volvía a empeorar.", {"noche", "empeorar"}),
 ({"fondo": "estudio", "el": [("anciano", 300, 1250, .8), ("hombre", 760, 1250, .8)], "vineta": .8, "cam": (1, 1.06, 0, 0)}, "Los médicos se rindieron. No había nada que hacer.", {"rindieron"}),
 ({"fondo": "habitacion", "flash": True, "pulso": 1.0, "bpm": 60, "cam": (1.15, 1.0, 0, 0)}, "Y una noche, Alicia murió.", {"murió"}),
 ({"fondo": "habitacion", "el": [("mujer", 300, 1260, .7), ("almohadon", 640, 1170, .55, {"var": "manchas"})], "cam": (1, 1.12, 120, 40)}, "Al día siguiente, la sirvienta deshacía la cama… y se quedó mirando el almohadón de plumas.", {"almohadón"}),
 ({"fondo": "estudio", "el": [("almohadon", 540, 1050, 1.3, {"var": "manchas", "anim": "aparecer"})], "pulso": .6, "bpm": 90, "cam": (1, 1.15, 0, 0)}, "Tenía pequeñas manchas oscuras. Y era extraño: pesaba demasiado.", {"manchas", "pesaba"}),
 ({"fondo": "habitacion", "el": [("hombre", 760, 1250, .8, {"anim": "temblar"}), ("almohadon", 440, 1170, .55, {"var": "manchas"})], "vineta": .85, "cam": (1, 1.1, 0, 0)}, "Jordán lo puso sobre la mesa y lo abrió de un corte.", {"abrió"}),
 ({"fondo": "estudio", "el": [("almohadon", 540, 1150, 1.2, {"var": "manchas"}), ("criatura", 540, 1050, 1.6, {"anim": "aparecer", "t0": .8})], "pulso": 1.2, "bpm": 140, "flash": True, "cam": (1, 1.2, 0, 0)}, "Adentro, entre las plumas, había un animal monstruoso: una bola viva, hinchada… del tamaño de un puño.", {"monstruoso"}),
 ({"fondo": "negro", "el": [("criatura", 540, 1050, 1.4, {"anim": "latir"})], "glows": [(540, 1050, 300, ROJO, 90)], "pulso": .9, "bpm": 110, "cam": (1, 1.12, 0, 0)}, "Cada noche, mientras Alicia dormía, esa criatura le había ido chupando la sangre… poco a poco.", {"sangre"}),
 ({"fondo": "habitacion", "vineta": .9, "cam": (1, 1.08, 0, 0)}, "Por eso de día mejoraba. Y por eso cada noche se apagaba un poco más.", {"noche"}),
 ({"fondo": "estudio", "el": [("libro", 540, 1050, .9, {"var": "Parásitos|de aves"})], "cam": (1, 1.06, 0, 0)}, "Quiroga cerró el cuento con un dato escalofriante: esos parásitos existen en las aves… y en almohadas de plumas pueden crecer más de lo normal.", {"existen"}),
 ({"fondo": "habitacion", "el": [("almohadon", 360, 1170, .45, {"anim": "latir"})], "pulso": .7, "bpm": 70, "cam": (1, 1.2, -100, 40)}, "Así que esta noche, antes de dormir… revisa bien tu almohada.", {"almohada"}),
 ({"fondo": "biblioteca", "el": [("libro", 540, 1150, 1.0, {"anim": "entrar", "var": "El almohadón|de plumas"})], "tag": "HORACIO QUIROGA · 1907", "tag_y": 700, "cam": (1, 1.06, 0, 0)}, "El almohadón de plumas fue publicado por el uruguayo Horacio Quiroga en mil novecientos siete. Más de un siglo después, sigue quitando el sueño.", {"quiroga"}),
]
esc, cierre = historia(H, "comics-store", "¿REVISASTE TU ALMOHADA?")
esc.append((cierre, "¿Ya revisaste tu almohada? Comenta y síguenos en Comics Store.", {"almohada"}))
if __name__ == "__main__":
    render(esc, sys.argv[1] if len(sys.argv) > 1 else "/home/claude/terror_04_almohadon.mp4", regancho_idx=11, musica="terror")
