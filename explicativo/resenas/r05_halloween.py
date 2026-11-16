"""Reseña: Halloween (1978). Resumen propio; ilustraciones originales; el villano solo como sombra (no se dibuja su máscara)."""
from _base import *
PRON = en("John", "Carpenter", "Debra", "Hill", "Michael", "Myers", "Judith", "Haddonfield", "Illinois", "Smith's", "Grove", "Sam", "Loomis", "Laurie", "Strode",
          "Tommy", "Annie", "Lynda", "Bob", "Jamie", "Lee", "Curtis", "Janet", "Leigh", "Donald", "Pleasence", "Halloween", "Kirk", "Captain", "Star", "Trek", "Panaglide", "Babysitter", "Murders")
NAR = (255, 140, 40)
H = [
 ({"fondo": "suburbio", "el": [("calabaza", 300, 1420, .5, {"anim": "aparecer"})], "cam": (1, 1.12, 0, 60)}, "Noche de Halloween, mil novecientos sesenta y tres. En Haddonfield, un pueblito tranquilo de Illinois, todo parece normal.", {"haddonfield"}),
 ({"fondo": "suburbio", "el": [("nino", 540, 1440, .45, {"anim": "aparecer"})], "pulso": .9, "bpm": 110, "vineta": .9, "cam": (1, 1.15, 0, 0)}, "Hasta que un niño de seis años, Michael Myers, entra a su casa disfrazado y ataca a su hermana mayor, Judith. Ella no sobrevive.", {"michael"}),
 ({"fondo": "estudio", "el": [("nino", 540, 1300, .7)], "vineta": .9, "cam": (1, 1.1, 0, 0)}, "Cuando sus padres llegan, lo encuentran parado en la calle, inmóvil, sin ninguna expresión en la cara. Lo internan en un sanatorio mental.", {"sanatorio"}),
 ({"fondo": "carretera", "fx": ["lluvia"], "el": [("auto", 540, 1300, .9, {"anim": "temblar"})], "cam": (1, 1.12, 0, 0)}, "Quince años después, en mil novecientos setenta y ocho, la noche antes de Halloween, Michael escapa del sanatorio y roba un carro.", {"escapa"}),
 ({"fondo": "estudio", "el": [("anciano", 540, 1280, .9, {"anim": "aparecer"})], "cam": (1, 1.08, 0, 0)}, "Su psiquiatra, el doctor Loomis, sabe exactamente a dónde va. Lleva años estudiándolo y está convencido de algo: detrás de esos ojos no hay nada humano.", {"loomis"}),
 ({"fondo": "suburbio", "el": [("sombra", 760, 1380, .55, {"anim": "aparecer"}), ("mujer", 340, 1420, .5)], "cam": (1, 1.1, 0, 0)}, "En Haddonfield, Laurie Strode, una estudiante tímida y responsable, camina al colegio. No sabe que alguien la observa desde lejos.", {"laurie", "observa"}),
 ({"fondo": "suburbio", "el": [("sombra", 540, 1400, .5, {"anim": "desvanecer", "t0": 1.2})], "pulso": .7, "bpm": 90, "cam": (1, 1.15, 0, 0)}, "Una figura con overol oscuro y una máscara blanca, sin expresión. Aparece detrás de un arbusto… y cuando Laurie vuelve a mirar, ya no está.", {"máscara"}),
 ({"fondo": "cementerio", "el": [("anciano", 380, 1400, .55), ("lapida", 700, 1420, .6, {"anim": "desvanecer", "t0": .8})], "fx": ["niebla"], "cam": (1, 1.1, 0, 0)}, "Loomis llega al pueblo y va al cementerio. La lápida de Judith, la hermana de Michael, desapareció. Alguien se la llevó. Ahí confirma que Michael volvió a casa.", {"lápida"}),
 ({"fondo": "casa", "el": [("anciano", 380, 1430, .5), ("policia", 640, 1430, .5)], "fx": ["niebla"], "cam": (1, 1.08, 0, 0)}, "Le pide ayuda al sheriff, que es el papá de Annie, la amiga de Laurie. Pero nadie le cree del todo. Loomis decide esperar toda la noche frente a la vieja casa de los Myers.", {"sheriff"}),
 ("H", "Y esa es la genialidad de Halloween: el asesino casi no corre, casi no habla. Solo camina, observa… y espera.", {"espera"}),
 ({"fondo": "cuarto", "el": [("mujer", 380, 1280, .8), ("nino", 680, 1320, .55)], "velas": [(860, 1000, 90, AMB)], "cam": (1, 1.06, 0, 0)}, "Esa noche de Halloween, Laurie cuida a un niño, Tommy. Sus amigas Annie y Lynda también cuidan niños en casas cercanas.", {"tommy"}),
 ({"fondo": "suburbio", "el": [("calabaza", 260, 1430, .45), ("sombra", 780, 1380, .5, {"anim": "aparecer"})], "pulso": .8, "bpm": 100, "cam": (1, 1.12, 0, 0)}, "Tommy le dice que vio al hombre del saco en la casa del frente. Laurie no le cree. Pero el niño tiene razón.", {"razón"}),
 ({"fondo": "suburbio", "vineta": .95, "pulso": 1.1, "bpm": 140, "cam": (1, 1.2, 0, 0)}, "Uno por uno, Michael ataca a Annie, a Lynda y a su novio Bob, en la casa del frente. Todo en silencio, mientras el pueblo celebra.", {"silencio"}),
 ({"fondo": "pasillo", "el": [("mujer", 540, 1350, .5, {"anim": "caminar_der", "dist": 0})], "pulso": 1.2, "bpm": 150, "cam": (1, 1.25, 0, 0)}, "Laurie va a ver por qué nadie contesta el teléfono. Entra a esa casa oscura… y encuentra a sus amigas. Entonces, Michael aparece detrás de ella.", {"aparece"}),
 ({"fondo": "cuarto", "el": [("mujer", 380, 1290, .8, {"anim": "temblar"}), ("sombra", 720, 1280, .8, {"anim": "acercar"})], "flash": True, "pulso": 1.3, "bpm": 160, "cam": (1, 1.2, 0, 0)}, "Escapa herida y se encierra con los niños. Michael entra. Laurie se defiende con lo que encuentra: una aguja de tejer, un gancho de ropa… y lo derriba varias veces.", {"defiende"}),
 ("H", "Pero cada vez que Laurie cree que ya terminó… Michael se vuelve a levantar.", {"levantar"}),
 ({"fondo": "suburbio", "el": [("anciano", 540, 1380, .6, {"anim": "aparecer"})], "flash": True, "pulso": 1.0, "bpm": 120, "cam": (1, 1.12, 0, 0)}, "En el último segundo llega el doctor Loomis, le dispara seis veces, y Michael cae por el balcón al jardín.", {"seis"}),
 ({"fondo": "suburbio", "pulso": .9, "bpm": 80, "vineta": .95, "cam": (1, 1.25, 0, 0)}, "Loomis se asoma para ver el cuerpo… y el jardín está vacío. Michael desapareció. La película termina con su respiración sonando por todo el pueblo.", {"vacío"}),
]
D = [
 ({"fondo": "estudio", "el": [("maquina", 540, 1100, 1.0, {"anim": "entrar"})], "cam": (1, 1.06, 0, 0)}, "La escribieron John Carpenter y la productora Debra Hill. Su primer título era muy distinto: Los asesinatos de la niñera. Luego decidieron ambientarla en Halloween… y le cambiaron el nombre.", {"carpenter", "niñera"}),
 ({"fondo": "estudio", "el": [("dinero", 540, 1080, .9, {"anim": "entrar"})], "tag": "300.000 USD", "tag_y": 1380, "tag_col": VERDE_T, "cam": (1, 1.08, 0, 0)}, "El presupuesto era ridículo: unos trescientos mil dólares. La grabaron en unas tres semanas… y en primavera, en California, aunque la historia pasa en otoño.", {"trescientos", "primavera"}),
 ("H", "Y aquí el dato que casi nadie conoce: la máscara de Michael era una máscara barata de un personaje de televisión, el capitán Kirk de Star Trek. Costó menos de dos dólares. La pintaron de blanco, le agrandaron los ojos… y nació un ícono.", {"kirk", "dos"}),
 ({"fondo": "estudio", "el": [("sonido", 540, 1050, 1.0, {"anim": "latir"})], "cam": (1, 1.08, 0, 0)}, "La música también la compuso John Carpenter. Esa melodía de piano, simple y repetitiva, es una de las más reconocidas del terror.", {"música"}),
 ({"fondo": "estudio", "el": [("mujer", 540, 1290, .9, {"anim": "aparecer"})], "cam": (1, 1.06, 0, 0)}, "Fue la primera película de Jamie Lee Curtis, hija de Janet Leigh… la actriz de Psicosis. Y el nombre del doctor Loomis es un guiño a otro personaje de Psicosis.", {"curtis", "psicosis"}),
 ({"fondo": "estudio", "el": [("camara_cine", 540, 1100, .9, {"anim": "entrar"})], "cam": (1, 1.08, 0, 0)}, "Gran parte del presupuesto se fue en cámaras. Usaron un estabilizador nuevo, el Panaglide, para esos planos que siguen a los personajes como si fueran los ojos del asesino.", {"panaglide"}),
 ({"fondo": "cine", "el": [("dinero", 540, 1060, .9, {"anim": "entrar"})], "tag": "70 MILLONES USD", "tag_y": 1380, "tag_col": VERDE_T, "cam": (1, 1.08, 0, 0)}, "El resultado: recaudó unos setenta millones de dólares en el mundo. Una de las películas independientes más rentables de la historia.", {"setenta"}),
]
O = [
 ("H", "Para mí, Halloween es la película que inventó las reglas del cine de asesinos de los años ochenta: la chica que sobrevive, el villano que no muere, la noche especial.", {"reglas"}),
 ("H", "Lo que más me gusta es su paciencia. Casi no hay sangre. El miedo viene de ver a Michael parado al fondo del plano, mientras los personajes no se dan cuenta.", {"paciencia"}),
 ({"fondo": "suburbio", "el": [("calabaza", 540, 1300, .7)]}, "¿Lo malo? Algunos personajes toman decisiones absurdas, y hoy el ritmo puede parecer lento para quien busca sustos cada minuto.", {"absurdas"}),
 ("H", "Pero con trescientos mil dólares crearon un monstruo que sigue vivo más de cuarenta años después. Eso, para mí, es genialidad pura.", {"genialidad"}),
]
esc, g = resena_completa("HALLOWEEN", "", "1978 · JOHN CARPENTER", "calabaza", GANCHO,
    "Hoy reseñamos Halloween, de John Carpenter. La noche en la que un asesino silencioso volvió a casa… y cambió el cine de terror para siempre.", H, D, O, 4.5,
    "Mi calificación: cuatro punto cinco de cinco. Un clásico que hay que ver… idealmente, una noche de Halloween.", obj1="calabaza",
    gancho_detras="Y lo más loco es cómo la hicieron. Porque el villano más famoso del terror… nació de una máscara de dos dólares.")
if __name__ == "__main__": correr(esc, g, "halloween", PRON)
