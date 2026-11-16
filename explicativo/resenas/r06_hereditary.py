"""Reseña: Hereditary / El legado del diablo (2018). Resumen propio, sin violencia gráfica; ilustraciones originales."""
from _base import *
PRON = en("Ari", "Aster", "Annie", "Graham", "Ellen", "Steve", "Peter", "Charlie", "Joan", "Paimon", "Toni", "Collette", "Gabriel", "Byrne", "Alex", "Wolff",
          "Milly", "Shapiro", "Ann", "Dowd", "Sundance", "Utah", "Hereditary", "Everything", "Everywhere", "All", "at", "Once", "Colin", "Stetson")
PRON.update({"a24": ("en", "A twenty four")})
H = [
 ({"fondo": "cementerio", "el": [("lapida", 540, 1350, .8)], "fx": ["niebla"], "cam": (1, 1.1, 0, 40)}, "La historia empieza con un funeral. Muere Ellen, la abuela de la familia Graham: una mujer reservada, llena de secretos, con la que nadie se llevaba del todo bien.", {"ellen", "secretos"}),
 ({"fondo": "estudio", "el": [("casa_munecas", 540, 1100, 1.0, {"anim": "aparecer"})], "velas": [(860, 1300, 90, AMB)], "cam": (1, 1.1, 0, 0)}, "Su hija, Annie, es artista: construye casas en miniatura, réplicas perfectas de su propia vida. Vive con su esposo Steve y sus dos hijos, Peter y Charlie.", {"annie", "miniatura"}),
 ({"fondo": "cuarto", "el": [("nino", 540, 1300, .7, {"anim": "balancear"})], "vineta": .9, "cam": (1, 1.1, 0, 0)}, "Charlie, de trece años, era la nieta favorita de la abuela. Es callada, extraña, hace muñecos con objetos raros y tiene una costumbre inquietante: chasquea la lengua.", {"charlie", "chasquea"}),
 ({"fondo": "estudio", "el": [("libro", 540, 1100, .9, {"anim": "aparecer", "var": "Diario|Ellen"})], "cam": (1, 1.08, 0, 0)}, "Después del funeral empiezan a pasar cosas raras. Annie siente la presencia de su madre en el taller. Y encuentra notas y libros de ella que no entiende.", {"presencia"}),
 ({"fondo": "fiesta", "el": [("hombre", 380, 1270, .7), ("nino", 680, 1300, .55)], "velas": [(540, 380, 140, AMB)], "cam": (1, 1.06, 0, 0)}, "Una noche, Annie obliga a Peter a llevar a Charlie a una fiesta. Allí, Charlie come un pastel con nueces… y ella es alérgica. Empieza a ahogarse.", {"alérgica"}),
 ({"fondo": "carretera", "el": [("auto", 540, 1300, .9, {"anim": "temblar"})], "pulso": 1.2, "bpm": 150, "cam": (1, 1.15, 0, 0)}, "Peter maneja a toda velocidad hacia el hospital. Charlie saca la cabeza por la ventana para respirar… y ocurre un accidente terrible en la carretera. Charlie no sobrevive.", {"accidente"}),
 ("H", "Y esto pasa en los primeros treinta minutos. Lo que parecía la historia de una niña extraña… se convierte en algo mucho peor.", {"treinta"}),
 ({"fondo": "cuarto", "el": [("hombre", 540, 1300, .8)], "vineta": .95, "cam": (1, 1.1, 0, 0)}, "Peter, en shock, llega a casa y no dice nada. Se acuesta como si nada hubiera pasado. A la mañana siguiente, es Annie quien encuentra lo ocurrido.", {"shock"}),
 ({"fondo": "estudio", "el": [("mujer", 380, 1270, .8, {"anim": "temblar"}), ("hombre", 700, 1270, .8)], "pulso": .8, "bpm": 100, "cam": (1, 1.1, 0, 0)}, "La familia se rompe. El duelo se vuelve rabia, culpa y reproches. Hay una cena en la que Annie le dice a Peter todo lo que lleva guardado. Es tan incómoda como cualquier escena de terror.", {"duelo", "culpa"}),
 ({"fondo": "estudio", "el": [("mujer", 380, 1270, .8), ("anciano", 700, 1270, .8)], "velas": [(540, 1000, 90, AMB)], "cam": (1, 1.06, 0, 0)}, "En un grupo de apoyo, Annie conoce a Joan, una señora amable que también perdió a alguien. Joan le enseña un ritual para comunicarse con los muertos.", {"joan", "ritual"}),
 ({"fondo": "cuarto", "el": [("vela", 540, 1150, 1.0)], "velas": [(540, 1000, 120, AMB)], "fx": ["particulas"], "pulso": 1.0, "bpm": 110, "cam": (1, 1.15, 0, 0)}, "Annie lo intenta en casa con Steve y Peter. Y funciona… demasiado bien. Algo responde. Algo entra a la casa.", {"funciona"}),
 ({"fondo": "biblioteca", "el": [("libro", 540, 1100, 1.0, {"anim": "entrar", "var": "Paimon|Rey del infierno"})], "fx": ["particulas"], "cam": (1, 1.1, 0, 0)}, "Revisando las cosas de su madre, Annie descubre la verdad: Ellen lideraba una secta que adoraba a Paimon, uno de los reyes del infierno.", {"secta", "paimon"}),
 ("H", "El plan de la secta llevaba años en marcha. Paimon necesitaba un cuerpo para vivir en la tierra. Y no cualquier cuerpo: el de un joven. Charlie fue solo el primer paso. El verdadero objetivo era Peter.", {"peter", "objetivo"}),
 ({"fondo": "casa", "fx": ["niebla"], "pulso": 1.0, "bpm": 120, "vineta": .95, "cam": (1, 1.15, 0, 0)}, "Joan también era parte de la secta. Todo el dolor de la familia había sido preparado, paso a paso, desde mucho antes.", {"joan"}),
 ({"fondo": "estudio", "el": [("fuego", 540, 1150, 1.0, {"anim": "latir"})], "glows": [(540, 1100, 300, (255, 120, 40), 120)], "flash": True, "cam": (1, 1.15, 0, 0)}, "Annie intenta romper el vínculo con el fuego, pero el ritual se vuelve contra ella. Steve muere envuelto en llamas, y Annie queda poseída.", {"fuego", "poseída"}),
 ({"fondo": "casa", "el": [("hombre", 540, 1430, .5, {"anim": "caer"})], "pulso": 1.3, "bpm": 160, "cam": (1, 1.2, 0, 0)}, "Peter, aterrado, huye por la casa… hasta que salta por una ventana. Cae inconsciente en el jardín. Y en ese momento, el plan se cumple.", {"ventana"}),
 ({"fondo": "bosque", "el": [("hombre", 540, 1350, .6, {"anim": "aparecer"}), ("sombra", 300, 1400, .45), ("sombra", 780, 1400, .45)], "glows": [(540, 1100, 260, ORO, 90)], "fx": ["particulas"], "cam": (1, 1.15, 0, 0)}, "Peter se levanta, pero ya no es él. Camina hasta la casa del árbol, donde los miembros de la secta lo esperan arrodillados. Le ponen una corona. Paimon ha llegado.", {"corona", "paimon"}),
]
D = [
 ({"fondo": "estudio", "el": [("camara_cine", 540, 1100, 1.0, {"anim": "entrar"})], "cam": (1, 1.08, 0, 0)}, "Hereditary fue la primera película de Ari Aster como director. Él mismo la presentó como una tragedia familiar, sin decir que era de terror.", {"aster", "tragedia"}),
 ({"fondo": "estudio", "el": [("casa_munecas", 540, 1100, 1.0, {"anim": "aparecer"})], "cam": (1, 1.08, 0, 0)}, "Se filmó en Utah. Casi toda la casa se construyó como un set en un estudio, para que la cámara pudiera moverse como si mirara dentro de una casa de muñecas.", {"utah", "muñecas"}),
 ("H", "En Latinoamérica la estrenaron como El legado del diablo. Un título que a muchos críticos no les gustó, porque sonaba a película de serie B… cuando en realidad es todo lo contrario.", {"legado"}),
 ({"fondo": "biblioteca", "el": [("libro", 540, 1100, .9, {"var": "Paimon|Grimorio"})], "cam": (1, 1.06, 0, 0)}, "Paimon no es un invento de la película. Aparece en antiguos libros de demonología como uno de los reyes del infierno.", {"paimon"}),
 ({"fondo": "cine", "el": [("dinero", 540, 1060, .9, {"anim": "entrar"})], "tag": "10 MILLONES USD", "tag_y": 1380, "tag_col": VERDE_T, "cam": (1, 1.08, 0, 0)}, "Se estrenó en el festival de Sundance en dos mil dieciocho y los críticos la compararon con El exorcista. Costó unos diez millones de dólares y recaudó más de ochenta.", {"sundance", "ochenta"}),
 ({"fondo": "estudio", "el": [("trofeo", 540, 1060, .9, {"anim": "entrar"})], "cam": (1, 1.08, 0, 0)}, "Durante años fue la película más taquillera del estudio A24, hasta que la superó Everything Everywhere All at Once en dos mil veintidós.", {"a24"}),
 ("H", "Y muchos fans siguen indignados porque Toni Collette no fue nominada al Óscar. Su actuación como Annie es considerada una de las mejores del cine de terror moderno.", {"collette"}),
]
O = [
 ("H", "Para mí, Hereditary es una de las películas más perturbadoras de este siglo. No te asusta con sustos fáciles: te deja una incomodidad que dura días.", {"perturbadoras"}),
 ("H", "Lo más fuerte es que primero es un drama sobre el duelo, y es tan real que duele. Cuando llega lo sobrenatural, ya estás destrozado.", {"duelo"}),
 ({"fondo": "estudio", "el": [("casa_munecas", 540, 1100, .9)]}, "¿Lo malo? Es lenta, y el final es tan extraño que divide al público: a unos les encanta, y a otros los saca de la película.", {"final"}),
 ("H", "No es para todo el mundo. Pero si te gusta el terror que se queda contigo… es obligatoria.", {"obligatoria"}),
]
esc, g = resena_completa("EL LEGADO", "DEL DIABLO", "HEREDITARY · 2018 · ARI ASTER", "casa_munecas", GANCHO,
    "Hoy reseñamos Hereditary, conocida en Latinoamérica como El legado del diablo. La película de Ari Aster que muchos llaman la más perturbadora del siglo veintiuno.", H, D, O, 4.5,
    "Mi calificación: cuatro punto cinco de cinco. Una pesadilla familiar brillante… que no vas a querer ver dos veces seguidas.", obj1="casa_munecas",
    gancho_detras="Y detrás de cámaras hay detalles que hacen la película todavía más inquietante. Empezando por cómo la vendieron.")
if __name__ == "__main__": correr(esc, g, "hereditary", PRON)
