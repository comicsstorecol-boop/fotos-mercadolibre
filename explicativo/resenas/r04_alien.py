"""Reseña: Alien, el octavo pasajero (1979). Resumen propio; ilustraciones originales; la criatura nunca se dibuja (solo sombras)."""
from _base import *
PRON = en("Ridley", "Scott", "Dan", "O'Bannon", "Ronald", "Shusett", "Nostromo", "Ripley", "Dallas", "Kane", "Ash", "Lambert", "Parker", "Brett", "Jones",
          "Sigourney", "Weaver", "John", "Hurt", "Giger", "Fox", "Alien", "Jaws", "Star", "Wars")
PRON.update({"h.r.": ("en", "H. R.")})
TEAL = (120, 255, 200)
H = [
 ({"fondo": "espacio", "cam": (1, 1.15, 0, 60)}, "En el espacio profundo, la nave de carga Nostromo regresa a la Tierra. Lleva millones de toneladas de mineral… y siete tripulantes dormidos en cápsulas.", {"nostromo", "siete"}),
 ({"fondo": "nave", "el": [("computadora", 540, 1100, 1.0, {"anim": "aparecer"})], "cam": (1, 1.1, 0, 0)}, "Pero la computadora de la nave, a la que llaman Madre, los despierta antes de tiempo. Detectó una señal que viene de un planeta desconocido.", {"madre", "señal"}),
 ({"fondo": "nave", "el": [("hombre", 300, 1290, .65), ("mujer", 540, 1300, .62), ("hombre", 780, 1290, .65)], "cam": (1, 1.06, 0, 0)}, "El contrato con la compañía es claro: si detectan una señal, están obligados a investigar. Así que bajan al planeta, aunque nadie quiere hacerlo.", {"compañía"}),
 ({"fondo": "desierto", "el": [("hombre", 380, 1400, .45), ("hombre", 540, 1405, .45), ("mujer", 690, 1410, .43)], "fx": ["niebla"], "vineta": .8, "cam": (1, 1.1, 0, 0)}, "Tres de ellos salen a explorar, en medio de tormentas y oscuridad. Encuentran una nave gigantesca, abandonada, que no fue construida por humanos.", {"nave", "humanos"}),
 ({"fondo": "abismo", "el": [("huevo", 380, 1300, .7), ("huevo", 560, 1350, .8, {"anim": "latir"}), ("huevo", 740, 1300, .7)], "fx": ["niebla_verde"], "cam": (1, 1.15, 0, 0)}, "Adentro, Kane baja a una cámara llena de huevos enormes. Se acerca a uno… el huevo se abre, y algo salta directo a su cara.", {"huevos", "kane"}),
 ({"fondo": "nave", "el": [("mujer", 540, 1280, .9, {"anim": "temblar"})], "pulso": .8, "bpm": 100, "cam": (1, 1.1, 0, 0)}, "Ripley, que está al mando en ese momento, se niega a dejarlos entrar: las reglas de cuarentena lo prohíben. Pero Ash, el oficial científico, les abre la puerta.", {"ripley", "ash"}),
 ({"fondo": "nave", "el": [("criatura", 540, 1100, .9, {"anim": "latir"})], "glows": [(540, 1100, 240, TEAL, 60)], "cam": (1, 1.15, 0, 0)}, "La criatura está pegada a la cara de Kane y no pueden quitársela. Cuando intentan cortarla, su sangre es un ácido que perfora el metal de la nave.", {"ácido"}),
 ({"fondo": "nave", "el": [("hombre", 540, 1300, .8)], "cam": (1, 1.06, 0, 0)}, "Días después, la criatura se suelta sola y muere. Kane despierta, tiene hambre… y parece estar bien. Todos se relajan.", {"bien"}),
 ("H", "Error. Durante una cena tranquila, Kane empieza a convulsionar. Y de su pecho sale una pequeña criatura que escapa por los pasillos. Fue una de las escenas más impactantes del cine de su época.", {"pecho"}),
 ({"fondo": "nave", "el": [("sombra", 540, 1250, .7, {"anim": "aparecer"})], "pulso": 1.0, "bpm": 120, "cam": (1, 1.15, 0, 0)}, "Ahora hay un octavo pasajero a bordo. Y crece muy rápido. Mata a Brett, y luego al capitán Dallas, que lo buscaba en los ductos de ventilación.", {"octavo", "dallas"}),
 ({"fondo": "nave", "el": [("computadora", 540, 1100, 1.0, {"anim": "temblar"})], "tag": "TRIPULACIÓN PRESCINDIBLE", "tag_y": 1420, "tag_col": ROJO, "tag_size": 44, "cam": (1, 1.15, 0, 0)}, "Ripley consulta a Madre y descubre la verdad: la compañía sabía de la criatura. La orden era llevarla a la Tierra para estudiarla. La tripulación era prescindible.", {"prescindible"}),
 ({"fondo": "nave", "el": [("hombre", 540, 1280, .9, {"anim": "temblar", "var": "frio"})], "flash": True, "pulso": 1.1, "bpm": 140, "cam": (1, 1.2, 0, 0)}, "Y el giro: Ash ataca a Ripley. Cuando lo detienen, descubren que no es humano. Es un androide, puesto ahí por la compañía para cumplir esa misión.", {"androide"}),
 ({"fondo": "nave", "el": [("sombra", 540, 1250, .8, {"anim": "acercar"})], "pulso": 1.2, "bpm": 150, "cam": (1, 1.2, 0, 0)}, "Los sobrevivientes deciden volar la nave y escapar en la cápsula. Pero la criatura atrapa a Parker y a Lambert. Ripley queda completamente sola.", {"sola"}),
 ({"fondo": "nave", "el": [("gato", 540, 1300, .8, {"anim": "aparecer"})], "cam": (1, 1.1, 0, 0)}, "Bueno, casi sola: también rescata a Jones, el gato de la nave. Activa la autodestrucción y corre hacia la cápsula de escape.", {"jones", "autodestrucción"}),
 ({"fondo": "espacio", "glows": [(540, 1000, 520, (255, 200, 120), 230)], "flash": True, "cam": (1.2, 1.0, 0, 0)}, "La Nostromo explota en el espacio. Ripley respira tranquila…", {"explota"}),
 ({"fondo": "nave", "el": [("sombra", 760, 1250, .7, {"anim": "aparecer", "t0": .6}), ("mujer", 340, 1300, .7, {"anim": "temblar"})], "pulso": 1.3, "bpm": 160, "cam": (1, 1.2, 0, 0)}, "Hasta que descubre que la criatura se escondió en la cápsula con ella. Se pone el traje espacial, abre la compuerta… y la expulsa al vacío.", {"cápsula", "vacío"}),
 ({"fondo": "espacio", "el": [("gato", 540, 1150, .6)], "cam": (1, 1.1, 0, 0)}, "Ripley graba el último informe de la nave y se duerme junto a Jones, rumbo a casa. Única sobreviviente.", {"sobreviviente"}),
]
D = [
 ({"fondo": "estudio", "el": [("maquina", 540, 1100, 1.0, {"anim": "entrar"})], "cam": (1, 1.06, 0, 0)}, "La historia nació de los guionistas Dan O'Bannon y Ronald Shusett. Y la dirigió Ridley Scott, que en ese momento tenía una sola película en su carrera.", {"scott"}),
 ({"fondo": "abismo", "el": [("estatua_alada", 540, 1150, .9, {"anim": "aparecer"})], "fx": ["niebla_verde"], "cam": (1, 1.1, 0, 0)}, "El diseño de la criatura y del planeta es del artista suizo H. R. Giger, que mezclaba lo biológico con lo mecánico. Por eso todo se ve tan extraño… y tan perturbador.", {"giger"}),
 ("H", "Dato curioso: Ripley, en el guion, no tenía género definido. Ese papel convirtió a Sigourney Weaver en estrella, y a Ripley en una de las heroínas más importantes del cine.", {"weaver", "heroínas"}),
 ({"fondo": "dinero" if False else "estudio", "el": [("dinero", 540, 1080, .9, {"anim": "entrar"})], "tag": "30.000 USD", "tag_y": 1380, "tag_col": VERDE_T, "cam": (1, 1.08, 0, 0)}, "Y como en ese momento era desconocida, se dice que le pagaron apenas unos treinta mil dólares por el papel.", {"treinta"}),
 ({"fondo": "nave", "el": [("camara_cine", 540, 1100, .9, {"anim": "entrar"})], "cam": (1, 1.08, 0, 0)}, "Los pasillos de la Nostromo se construyeron como sets enormes y estrechos, llenos de cables, vapor y luces parpadeantes. La idea era que la nave se sintiera sucia, vieja y real, como un camión de carga en el espacio.", {"camión"}),
 ("H", "La escena de la cena tiene leyenda propia: los actores sabían que algo iba a pasar, pero no exactamente cómo se iba a ver. Muchas de sus reacciones de asco y sorpresa son reales.", {"reales"}),
 ({"fondo": "cine", "el": [("dinero", 540, 1060, .9, {"anim": "entrar"})], "tag": "+100 MILLONES USD", "tag_y": 1380, "tag_col": VERDE_T, "cam": (1, 1.08, 0, 0)}, "Costó unos once millones de dólares y recaudó más de cien millones en todo el mundo, compitiendo en cines con gigantes de esa época.", {"once", "cien"}),
 ({"fondo": "estudio", "el": [("trofeo", 540, 1060, .9, {"anim": "entrar"})], "tag": "ÓSCAR · EFECTOS VISUALES", "tag_y": 1380, "tag_col": ORO, "cam": (1, 1.08, 0, 0)}, "Las primeras críticas fueron mixtas, pero ganó el Óscar a mejores efectos visuales. Y dio inicio a una saga que sigue viva más de cuarenta años después.", {"óscar"}),
]
O = [
 ("H", "Para mí, Alien es la prueba de que menos es más. Casi nunca ves a la criatura completa, y justo por eso da tanto miedo: tu imaginación hace el resto.", {"imaginación"}),
 ("H", "Es una película de terror disfrazada de ciencia ficción. Una casa embrujada… pero en el espacio, donde no hay a dónde correr.", {"espacio"}),
 ({"fondo": "nave", "el": [("computadora", 540, 1100, .9)]}, "¿Lo malo? El primer tramo es lento, y algunos efectos se notan de su época. Pero el diseño de la nave sigue viéndose increíble.", {"lento"}),
 ("H", "Y Ripley es una protagonista enorme: no es una víctima, es la más inteligente de la nave. Mientras los demás discuten, ella piensa. Por algo sigue siendo un ícono del cine.", {"ripley"}),
]
esc, g = resena_completa("ALIEN", "", "1979 · RIDLEY SCOTT", "huevo", GANCHO,
    "Hoy reseñamos Alien, el octavo pasajero, de Ridley Scott. Siete tripulantes, una nave en medio de la nada… y algo que no debería estar a bordo.", H, D, O, 5,
    "Mi calificación: cinco de cinco. Un clásico absoluto del terror y la ciencia ficción, que no ha envejecido.", obj1="computadora",
    gancho_detras="Y lo que pasó detrás de cámaras es igual de interesante. Empezando por un dato: Ripley ni siquiera estaba pensada como mujer.")
if __name__ == "__main__": correr(esc, g, "alien", PRON)
