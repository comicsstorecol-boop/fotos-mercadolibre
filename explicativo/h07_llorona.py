"""Comics Store · Terror: La Llorona (folclor hispanoamericano)"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
from compositor import historia
from motor import render
AMB = (255, 200, 120); AZ = (160, 200, 255)
H = [
 ({"fondo": "rio", "el": [("llorona", 540, 1250, .7, {"anim": "flotar"})], "fx": ["niebla"], "cam": (1, 1.15, 0, 60)}, "Si de noche, cerca de un río, escuchas un lamento que dice: ¡Ay, mis hijos!… no te acerques.", {"hijos"}),
 ({"fondo": "estudio", "el": [("libro", 540, 1050, .9, {"anim": "aparecer", "var": "La Llorona|Leyenda"})], "cam": (1, 1.06, 0, 0)}, "La Llorona es la leyenda de terror más famosa de América Latina. Se cuenta desde México hasta Argentina… y también aquí, en Colombia.", {"latina", "colombia"}),
 ({"fondo": "fiesta", "el": [("mujer", 540, 1260, .8, {"anim": "aparecer"})], "velas": [(270, 380, 120, AMB), (810, 380, 120, AMB)], "cam": (1, 1.06, 0, 0)}, "Hace mucho tiempo, en un pueblo, vivía una mujer joven y muy hermosa. Muchos la llamaban María.", {"maría"}),
 ({"fondo": "fiesta", "el": [("mujer", 420, 1260, .8), ("hombre", 660, 1250, .85)], "velas": [(270, 380, 120, AMB)], "cam": (1, 1.08, 0, 0)}, "Un día conoció a un hombre rico y elegante. Se enamoraron, y tuvieron dos hijos.", {"hijos"}),
 ({"fondo": "casa", "el": [("anciano", 380, 1300, .8), ("mujer", 720, 1300, .8, {"anim": "temblar"})], "vineta": .8, "cam": (1, 1.06, 0, 0)}, "Ella soñaba con casarse. Pero la familia de él nunca iba a aceptar a una mujer humilde.", {"humilde"}),
 ({"fondo": "casa", "el": [("hombre", 760, 1420, .5, {"anim": "caminar_der", "dist": 260})], "fx": ["niebla"], "cam": (1, 1.08, 0, 0)}, "Pero con el tiempo, él empezó a alejarse. Pasaba días sin volver… hasta que un día los abandonó.", {"abandonó"}),
 ({"fondo": "calle", "el": [("hombre", 420, 1440, .55), ("mujer", 560, 1450, .52)], "vineta": .8, "cam": (1, 1.1, 0, 0)}, "Poco después, María lo vio pasar con otra mujer, de su misma clase social.", {"otra"}),
 ({"fondo": "rio", "el": [("mujer", 540, 1250, .65, {"anim": "temblar"})], "pulso": .9, "bpm": 110, "cam": (1, 1.12, 0, 0)}, "Cegada por la rabia y el dolor, llevó a sus hijos al río… y en un momento de locura, los perdió en el agua.", {"locura", "río"}),
 ({"fondo": "rio", "flash": True, "pulso": 1.0, "bpm": 60, "cam": (1.15, 1.0, 0, 0)}, "Cuando entendió lo que había hecho, ya era tarde.", {"tarde"}),
 ({"fondo": "rio", "el": [("mujer", 540, 1250, .6, {"anim": "desvanecer", "t0": .8})], "fx": ["niebla"], "cam": (1, 1.1, 0, 40)}, "Los buscó por toda la orilla, gritando sus nombres. Días después, la encontraron sin vida junto al río.", {"orilla"}),
 ({"fondo": "cementerio", "el": [("llorona", 540, 1250, .7, {"anim": "aparecer"})], "fx": ["niebla"], "glows": [(540, 1000, 300, AZ, 80)], "cam": (1, 1.1, 0, 0)}, "Dicen que su alma no pudo descansar. Fue condenada a vagar para siempre, buscando a sus hijos.", {"vagar"}),
 ({"fondo": "rio", "el": [("llorona", 540, 1200, .8, {"anim": "flotar"})], "fx": ["niebla"], "glows": [(540, 1000, 340, AZ, 90)], "cam": (1, 1.12, 0, 0)}, "La describen con un vestido blanco, el cabello largo y negro tapándole la cara… y flotando sobre el agua.", {"blanco", "flotando"}),
 ({"fondo": "rio", "el": [("sonido", 540, 900, 1.0, {"anim": "temblar"})], "fx": ["niebla"], "pulso": .8, "bpm": 80, "cam": (1, 1.12, 0, 0)}, "Su grito es inconfundible: ¡Ay, mis hijos! Y hay una regla que todos los abuelos conocen.", {"regla"}),
 ({"fondo": "negro", "el": [("sonido", 540, 1000, 1.2, {"anim": "latir"})], "pulso": 1.0, "bpm": 120, "flash": True, "cam": (1.15, 1.0, 0, 0)}, "Si escuchas el llanto lejos… es porque está cerca. Y si lo escuchas cerca… es porque está lejos.", {"lejos", "cerca"}),
 ({"fondo": "bosque", "el": [("nino", 540, 1430, .45, {"anim": "caminar_der", "dist": 80}), ("llorona", 860, 1300, .5, {"anim": "aparecer", "t0": 1.0})], "fx": ["niebla"], "cam": (1, 1.12, 0, 40)}, "Dicen que se lleva a los niños que encuentra solos cerca del agua por la noche… confundiéndolos con los suyos.", {"niños"}),
 ({"fondo": "casa", "fx": ["niebla"], "vineta": .8, "cam": (1, 1.08, 0, 0)}, "Por eso, durante generaciones, las mamás advirtieron: no salgas de noche… porque te lleva la Llorona.", {"generaciones"}),
 ({"fondo": "calle", "el": [("hombre", 540, 1440, .55, {"anim": "temblar"}), ("llorona", 860, 1350, .45, {"anim": "aparecer", "t0": 1})], "fx": ["niebla"], "cam": (1, 1.1, 0, 0)}, "Hay quienes juran haberla visto: conductores de madrugada, pescadores, campesinos… todos cuentan lo mismo.", {"visto"}),
 ({"fondo": "bosque", "el": [("perro", 540, 1400, .5, {"anim": "temblar"})], "fx": ["niebla"], "cam": (1, 1.1, 0, 30)}, "En Colombia dicen que su grito se escucha en las quebradas… y que los perros aúllan cuando ella pasa.", {"quebradas", "aúllan"}),
 ({"fondo": "abismo", "el": [("libro", 540, 1050, .8, {"var": "Cihuacóatl|Mito azteca"})], "fx": ["particulas"], "cam": (1, 1.08, 0, 0)}, "Algunos historiadores creen que la leyenda es todavía más antigua: que viene de una diosa azteca que lloraba por sus hijos antes de la llegada de los españoles.", {"azteca"}),
 ({"fondo": "rio", "el": [("llorona", 540, 1220, .75, {"anim": "acercar"})], "fx": ["niebla"], "pulso": .9, "bpm": 90, "cam": (1, 1.2, 0, 0)}, "Así que esta noche, si pasas cerca de un río y escuchas un lamento… no mires atrás.", {"atrás"}),
]
esc, cierre = historia(H, "comics-store", "¿LA HAS ESCUCHADO?")
esc.append((cierre, "¿Alguien de tu familia escuchó a la Llorona? Cuéntanos en los comentarios y síguenos en Comics Store.", {"llorona"}))
if __name__ == "__main__":
    render(esc, sys.argv[1] if len(sys.argv) > 1 else "/home/claude/terror_07_llorona.mp4", regancho_idx=7, musica="terror")
