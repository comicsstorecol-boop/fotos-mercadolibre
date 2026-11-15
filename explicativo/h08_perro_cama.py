"""Comics Store · Terror: El perro bajo la cama (leyenda urbana)"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
from compositor import historia
from motor import render
AMB = (255, 200, 120); AZ = (150, 190, 255); ROJO = (220, 40, 50)
H = [
 ({"fondo": "habitacion", "el": [("lengua_mano", 300, 1500, .5, {"anim": "aparecer", "rot": 15})], "vineta": .9, "pulso": .5, "bpm": 70, "cam": (1, 1.15, -100, 60)}, "Esta es una de las leyendas urbanas más contadas del mundo. Y después de escucharla… no vas a querer sacar la mano de la cama.", {"mano"}),
 ({"fondo": "casa", "fx": ["lluvia"], "cam": (1, 1.1, 0, 40)}, "Una joven llamada Laura se queda sola en casa por primera vez. Sus padres viajaron por el fin de semana.", {"sola"}),
 ({"fondo": "cuarto", "el": [("mujer", 380, 1250, .8), ("perro", 700, 1300, .5)], "velas": [(900, 1000, 90, AMB)], "cam": (1, 1.06, 0, 0)}, "Pero no está completamente sola: la acompaña su perro, Max, que la cuida a todas partes.", {"max"}),
 ({"fondo": "estudio", "el": [("telefono", 540, 1080, 1.0, {"anim": "aparecer"})], "tag": "ÚLTIMA HORA", "tag_y": 620, "tag_col": ROJO, "cam": (1, 1.08, 0, 0)}, "Esa noche, en las noticias, anuncian que un peligroso criminal escapó de una cárcel cercana.", {"criminal"}),
 ({"fondo": "casa", "fx": ["lluvia", "rayo"], "vineta": .8, "cam": (1, 1.08, 0, 0)}, "Laura revisa que todas las puertas y ventanas estén cerradas. Todo parece en orden.", {"cerradas"}),
 ({"fondo": "habitacion", "el": [("perro", 540, 1400, .4)], "vineta": .85, "cam": (1, 1.08, 0, 30)}, "Se va a dormir. Como siempre, Max se acuesta debajo de su cama.", {"debajo"}),
 ({"fondo": "habitacion", "el": [("sonido", 820, 700, .5, {"anim": "temblar"})], "vineta": .9, "cam": (1, 1.1, 0, 0)}, "A medianoche, la despierta un sonido: gotas. Ploc… ploc… ploc. Viene del baño.", {"gotas"}),
 ({"fondo": "habitacion", "el": [("lengua_mano", 300, 1460, .5, {"anim": "aparecer", "rot": 15})], "vineta": .9, "cam": (1, 1.12, -80, 40)}, "Tiene miedo. Entonces estira la mano hacia abajo de la cama… y siente una lengua que se la lame. Es Max. Se tranquiliza.", {"lengua", "max"}),
 ({"fondo": "habitacion", "el": [("sonido", 820, 700, .5, {"anim": "temblar"})], "pulso": .5, "bpm": 70, "cam": (1, 1.1, 0, 0)}, "El goteo sigue. Ploc… ploc. Cada vez que se asusta, baja la mano… y Max se la vuelve a lamer.", {"goteo"}),
 ({"fondo": "habitacion", "el": [("lengua_mano", 300, 1460, .5, {"rot": 15})], "vineta": .9, "cam": (1, 1.06, 0, 0)}, "Así pasa toda la noche, hasta que por fin se queda dormida.", {"dormida"}),
 ({"fondo": "habitacion", "glows": [(540, 660, 300, (255, 240, 200), 120)], "flash": True, "cam": (1.12, 1.0, 0, 0)}, "A la mañana siguiente, el goteo sigue sonando.", {"mañana"}),
 ({"fondo": "pasillo", "el": [("mujer", 540, 1350, .5, {"anim": "caminar_der", "dist": 0})], "pulso": .9, "bpm": 110, "cam": (1, 1.25, 0, 0)}, "Laura camina hasta el baño para cerrar la llave… y abre la puerta.", {"baño"}),
 ({"fondo": "negro", "el": [("perro", 540, 1250, .6, {"anim": "aparecer"})], "pulso": 1.2, "bpm": 140, "flash": True, "cam": (1, 1.15, 0, 0)}, "Allí está Max. Sin vida. Lo que goteaba toda la noche… era él.", {"max"}),
 ({"fondo": "habitacion", "el": [("espejo", 540, 1000, 1.2)], "tag": "LOS HUMANOS TAMBIÉN PUEDEN LAMER", "tag_y": 1000, "tag_col": ROJO, "tag_size": 40, "pulso": 1.0, "bpm": 130, "cam": (1, 1.15, 0, 0)}, "Y en el espejo, alguien había escrito: los humanos también pueden lamer.", {"lamer"}),
 ({"fondo": "habitacion", "el": [("sombra", 540, 1400, .5, {"anim": "aparecer", "t0": .5})], "vineta": .95, "pulso": .8, "bpm": 90, "cam": (1, 1.2, 0, 60)}, "Toda la noche… lo que estaba debajo de su cama no era su perro.", {"perro"}),
 ({"fondo": "estudio", "el": [("libro", 540, 1050, .9, {"var": "Leyendas|urbanas"})], "cam": (1, 1.06, 0, 0)}, "Esta leyenda circula desde hace décadas en todo el mundo, con distintos nombres y finales. Nadie sabe dónde empezó… pero todos la cuentan igual.", {"décadas"}),
 ({"fondo": "habitacion", "el": [("lengua_mano", 300, 1500, .5, {"anim": "aparecer", "rot": 15})], "vineta": .9, "pulso": .6, "bpm": 70, "cam": (1, 1.2, -100, 60)}, "Esta noche, antes de bajar la mano de la cama… asegúrate de saber quién está ahí abajo.", {"abajo"}),
]
esc, cierre = historia(H, "comics-store", "¿DUERMES CON LA MANO AFUERA?")
esc.append((cierre, "¿Tú duermes con la mano afuera de la cama? Comenta y síguenos en Comics Store.", {"mano"}))
if __name__ == "__main__":
    render(esc, sys.argv[1] if len(sys.argv) > 1 else "/home/claude/terror_08_perro_cama.mp4", regancho_idx=10, musica="terror")
