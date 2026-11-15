"""Comics Store · Terror: La cita en el cementerio (leyenda de la chica de la curva / el baile)"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
from compositor import historia
from motor import render
AMB = (255, 200, 120); AZ = (160, 200, 255); ROJO = (220, 40, 50)
H = [
 ({"fondo": "cementerio", "el": [("lapida", 540, 1300, .8), ("chaqueta", 540, 1120, .6, {"anim": "aparecer"})], "fx": ["niebla"], "pulso": .5, "bpm": 70, "cam": (1, 1.15, 0, 40)}, "Una chaqueta olvidada sobre una tumba. Así termina una de las leyendas más contadas de América Latina. Pero empieza en una fiesta.", {"chaqueta", "fiesta"}),
 ({"fondo": "fiesta", "el": [("hombre", 540, 1260, .85, {"anim": "aparecer"})], "velas": [(270, 380, 140, AMB), (810, 380, 140, AMB)], "cam": (1, 1.06, 0, 0)}, "Era un sábado por la noche. Andrés, un joven del pueblo, fue al baile de la plaza con sus amigos.", {"andrés", "baile"}),
 ({"fondo": "fiesta", "el": [("dama", 760, 1260, .8, {"anim": "aparecer"}), ("hombre", 340, 1260, .8)], "velas": [(540, 380, 140, AMB)], "glows": [(760, 1000, 220, AZ, 60)], "cam": (1, 1.08, 0, 0)}, "Esa noche vio a una muchacha que nunca había visto. Vestido blanco, piel pálida… y una mirada triste.", {"blanco", "triste"}),
 ({"fondo": "fiesta", "el": [("hombre", 440, 1260, .8, {"anim": "balancear"}), ("dama", 640, 1260, .8, {"anim": "balancear"})], "velas": [(270, 380, 140, AMB), (810, 380, 140, AMB)], "cam": (1, 1.08, 0, 0)}, "La invitó a bailar. Ella aceptó. Bailaron toda la noche. Le dijo que se llamaba Elena.", {"elena"}),
 ({"fondo": "fiesta", "el": [("dama", 540, 1260, .8, {"anim": "balancear"})], "velas": [(270, 380, 140, AMB)], "cam": (1, 1.08, 0, 0)}, "Andrés le preguntó dónde vivía y quiénes eran sus papás. Ella solo sonreía… y cambiaba de tema.", {"sonreía"}),
 ({"fondo": "fiesta", "el": [("dama", 540, 1260, .8)], "glows": [(540, 1000, 240, AZ, 70)], "cam": (1, 1.1, 0, 0)}, "Lo raro era su mano: helada, como si estuviera tocando hielo. Y casi no hablaba de sí misma.", {"helada"}),
 ({"fondo": "calle", "el": [("hombre", 440, 1440, .55), ("dama", 600, 1440, .5)], "fx": ["niebla"], "cam": (1, 1.08, 0, 0)}, "A la medianoche, ella dijo que debía irse. Hacía frío, así que Andrés le prestó su chaqueta.", {"chaqueta"}),
 ({"fondo": "calle", "el": [("hombre", 440, 1440, .55, {"anim": "caminar_der", "dist": 120}), ("dama", 600, 1440, .5, {"anim": "caminar_der", "dist": 120})], "fx": ["niebla"], "vineta": .8, "cam": (1, 1.1, 0, 0)}, "La acompañó hasta la entrada del cementerio. Ella le dijo: aquí cerca vivo. No sigas.", {"cementerio"}),
 ({"fondo": "cementerio", "el": [("dama", 540, 1300, .6, {"anim": "desvanecer", "t0": 1})], "fx": ["niebla"], "pulso": .8, "bpm": 90, "cam": (1, 1.12, 0, 0)}, "Se despidieron. Andrés la vio caminar entre la neblina… hasta perderla de vista.", {"neblina"}),
 ({"fondo": "cuarto", "el": [("hombre", 540, 1250, .8)], "velas": [(820, 1000, 90, AMB)], "vineta": .85, "cam": (1, 1.06, 0, 0)}, "Esa noche Andrés no pudo dormir. No dejaba de pensar en esa mano helada.", {"helada"}),
 ({"fondo": "casa", "glows": [(540, 660, 300, (255, 240, 200), 110)], "cam": (1, 1.08, 0, 0)}, "Al día siguiente, fue a buscarla para recuperar su chaqueta. Preguntó por Elena en las casas cercanas.", {"elena"}),
 ({"fondo": "casa", "el": [("anciano", 420, 1300, .8), ("hombre", 720, 1300, .8)], "cam": (1, 1.06, 0, 0)}, "Una señora mayor le abrió la puerta. Andrés le describió a la muchacha del vestido blanco.", {"señora"}),
 ({"fondo": "casa", "el": [("retrato", 540, 1050, .9, {"anim": "aparecer"})], "pulso": 1.0, "bpm": 120, "flash": True, "cam": (1, 1.15, 0, 0)}, "La señora palideció. Le mostró un retrato viejo. Era ella… era Elena.", {"retrato", "elena"}),
 ({"fondo": "casa", "el": [("anciano", 540, 1300, .9, {"anim": "temblar"})], "vineta": .9, "cam": (1, 1.1, 0, 0)}, "Es mi hija, le dijo. Pero murió hace veinte años… la noche de un baile, como el de ayer.", {"veinte", "murió"}),
 ({"fondo": "calle", "el": [("dama", 540, 1300, .7, {"anim": "desvanecer", "t0": 1})], "fx": ["niebla", "lluvia"], "cam": (1, 1.1, 0, 0)}, "Le contó que Elena salió a un baile con un vestido blanco. Y que en el camino de regreso tuvo un accidente. Nunca llegó a casa.", {"accidente"}),
 ({"fondo": "cementerio", "el": [("hombre", 540, 1430, .45, {"anim": "caminar_der", "dist": 0})], "fx": ["niebla"], "pulso": .9, "bpm": 110, "cam": (1, 1.15, 0, 0)}, "Andrés no lo creyó. Corrió al cementerio, buscando su tumba.", {"tumba"}),
 ({"fondo": "cementerio", "el": [("lapida", 540, 1300, .9), ("chaqueta", 540, 1120, .65, {"anim": "aparecer", "t0": .6})], "fx": ["niebla"], "pulso": 1.2, "bpm": 140, "flash": True, "cam": (1, 1.25, 0, 0)}, "Y allí, sobre la lápida con el nombre de Elena… estaba su chaqueta. Doblada.", {"chaqueta"}),
 ({"fondo": "cementerio", "el": [("chaqueta", 540, 1150, .8, {"anim": "temblar"})], "fx": ["niebla"], "cam": (1, 1.1, 0, 0)}, "Andrés tomó la chaqueta. Estaba helada… y todavía olía a flores.", {"flores"}),
 ({"fondo": "cementerio", "el": [("rosa", 540, 1250, .7, {"anim": "aparecer"})], "fx": ["niebla"], "vineta": .9, "cam": (1, 1.12, 0, 0)}, "Dicen que Elena vuelve cada año, la noche del baile, buscando la última pieza que no pudo terminar.", {"baile"}),
 ({"fondo": "estudio", "el": [("libro", 540, 1050, .9, {"var": "Leyendas|de América"})], "cam": (1, 1.06, 0, 0)}, "Esta historia se cuenta en Colombia, México, Perú, Chile y Estados Unidos, con distintos nombres. Algunos juran conocer al muchacho… o al menos a alguien que lo conoció.", {"colombia"}),
 ({"fondo": "fiesta", "el": [("dama", 540, 1260, .8, {"anim": "acercar"})], "glows": [(540, 1000, 260, AZ, 80)], "pulso": .8, "bpm": 90, "cam": (1, 1.15, 0, 0)}, "Así que la próxima vez que bailes con alguien que no conoces, y su mano esté helada… pregúntale dónde vive.", {"helada"}),
]
esc, cierre = historia(H, "comics-store", "¿LE PRESTARÍAS TU CHAQUETA?")
esc.append((cierre, "¿Conoces otra versión de esta leyenda? Comenta y síguenos en Comics Store.", {"leyenda"}))
if __name__ == "__main__":
    render(esc, sys.argv[1] if len(sys.argv) > 1 else "/home/claude/terror_10_cita_cementerio.mp4", regancho_idx=9, musica="terror")
