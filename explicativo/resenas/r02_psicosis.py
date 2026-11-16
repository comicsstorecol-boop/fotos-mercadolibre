"""Reseña: Psicosis (1960). Resumen propio; ilustraciones originales, sin imágenes de la película."""
from _base import *
PRON = en("Hitchcock", "Alfred", "Marion", "Crane", "Phoenix", "Sam", "Loomis", "Norman", "Bates", "Arbogast", "Lila", "Anthony", "Perkins", "Janet", "Leigh",
          "Vera", "Miles", "John", "Gavin", "Robert", "Bloch", "Ed", "Paramount", "Bernard", "Herrmann", "Joseph", "Stefano", "Wisconsin")
PRON.update({"gein": ("en", "Geen")})
H = [
 ({"fondo": "estudio", "el": [("dinero", 540, 1080, 1.0, {"anim": "entrar"})], "cam": (1, 1.08, 0, 0)}, "Marion Crane es secretaria en Phoenix, Arizona. Un viernes, su jefe le pide depositar en el banco cuarenta mil dólares en efectivo de un cliente.", {"marion", "dólares"}),
 ({"fondo": "estudio", "el": [("mujer", 540, 1280, .9, {"anim": "temblar"})], "vineta": .85, "cam": (1, 1.08, 0, 0)}, "Pero Marion no va al banco. Quiere casarse con su novio, Sam Loomis, que está lleno de deudas. Así que toma el dinero… y huye.", {"huye"}),
 ({"fondo": "carretera", "el": [("auto", 540, 1300, 1.0, {"anim": "temblar"})], "cam": (1, 1.12, 0, 0)}, "Maneja horas por la carretera, nerviosa. Un policía la detiene y la mira con sospecha. Ella cambia de carro para no dejar rastro.", {"policía"}),
 ({"fondo": "carretera", "fx": ["lluvia"], "vineta": .9, "cam": (1, 1.15, 0, 0)}, "Cae la noche y empieza una tormenta. Marion se desvía de la autopista principal… y llega a un lugar casi abandonado.", {"tormenta"}),
 ({"fondo": "motel", "fx": ["lluvia"], "cam": (1, 1.1, 0, 0)}, "El Motel Bates. Doce habitaciones, cero huéspedes. Desde que cambiaron la carretera, ya nadie pasa por ahí.", {"bates"}),
 ({"fondo": "motel", "el": [("hombre", 540, 1300, .7, {"anim": "aparecer"})], "fx": ["lluvia"], "cam": (1, 1.1, 0, 0)}, "La atiende Norman Bates, un joven tímido, amable… y un poco raro. Le entrega la llave de la habitación número uno.", {"norman", "llave"}),
 ({"fondo": "casa", "fx": ["lluvia"], "glows": [(560, 900, 120, AMB, 120)], "cam": (1, 1.12, 0, 0)}, "Detrás del motel, en lo alto de una colina, hay una casa vieja. Ahí vive la madre de Norman. Marion escucha cómo ella le grita y lo humilla.", {"madre"}),
 ({"fondo": "estudio", "el": [("pajaro", 400, 1050, .9, {"anim": "aparecer"}), ("pajaro", 780, 950, .7, {"anim": "aparecer", "t0": .6})], "velas": [(540, 1300, 90, AMB)], "cam": (1, 1.1, 0, 0)}, "Norman la invita a cenar en una salita llena de aves disecadas. Su pasatiempo es la taxidermia. Le dice algo que da escalofríos: todos enloquecemos un poco a veces.", {"aves", "enloquecemos"}),
 ("H", "Esa conversación hace que Marion se dé cuenta de su error. Decide volver a Phoenix al día siguiente… y devolver el dinero.", {"devolver"}),
 ({"fondo": "negro", "el": [("sombra", 540, 1250, .8, {"anim": "acercar"})], "pulso": 1.3, "bpm": 160, "flash": True, "cam": (1, 1.25, 0, 0)}, "Pero esa noche, mientras se ducha, una figura aparece detrás de la cortina. Es una silueta de mujer. Y Marion nunca sale de esa habitación.", {"silueta"}),
 ({"fondo": "casa", "el": [("auto", 540, 1450, .7, {"anim": "caer"})], "fx": ["niebla"], "vineta": .9, "cam": (1, 1.1, 0, 0)}, "Norman, aterrado, culpa a su madre. Limpia todo y hunde el carro de Marion en un pantano, con el dinero adentro.", {"pantano"}),
 ("H", "Y aquí está lo que nadie esperaba en mil novecientos sesenta: la protagonista muere antes de la mitad de la película. El público quedó sin saber a quién seguir.", {"protagonista"}),
 ({"fondo": "calle", "el": [("hombre", 540, 1300, .8, {"anim": "caminar_der", "dist": 120})], "cam": (1, 1.08, 0, 0)}, "Días después, un detective privado, Arbogast, busca a Marion y el dinero. Las pistas lo llevan directo al Motel Bates.", {"arbogast"}),
 ({"fondo": "casa", "el": [("hombre", 540, 1430, .5, {"anim": "acercar"})], "fx": ["niebla"], "pulso": 1.0, "bpm": 120, "cam": (1, 1.2, 0, 0)}, "Arbogast sospecha de Norman y entra a la casa para hablar con la madre. Sube las escaleras… y desaparece.", {"desaparece"}),
 ({"fondo": "estudio", "el": [("mujer", 380, 1280, .8), ("hombre", 700, 1270, .85)], "cam": (1, 1.06, 0, 0)}, "Entonces Lila, la hermana de Marion, y Sam van a buscarla ellos mismos. El sheriff del pueblo les cuenta algo imposible: la señora Bates murió hace diez años.", {"lila", "murió"}),
 ("H", "Entonces… ¿quién es la mujer de la casa?", {"quién"}),
 ({"fondo": "cuarto", "el": [("mujer", 400, 1300, .7, {"anim": "caminar_der", "dist": 80}), ("mecedora", 760, 1200, .8, {"anim": "aparecer"})], "vineta": .95, "pulso": 1.2, "bpm": 150, "cam": (1, 1.2, 0, 0)}, "Lila se mete a la casa y baja al sótano. Ve a una anciana sentada en una silla, de espaldas. La toca… y descubre que es un cadáver momificado.", {"sótano", "momificado"}),
 ({"fondo": "cuarto", "el": [("sombra", 540, 1280, .9, {"anim": "acercar"})], "flash": True, "pulso": 1.3, "bpm": 160, "cam": (1, 1.25, 0, 0)}, "En ese momento entra Norman, vestido con la ropa de su madre y una peluca. Sam llega justo a tiempo y lo detiene.", {"norman"}),
 ({"fondo": "estudio", "el": [("libro", 540, 1100, .9, {"var": "Diagnóstico|Norman Bates"})], "cam": (1, 1.06, 0, 0)}, "Un psiquiatra lo explica todo: años atrás, Norman envenenó a su madre y a su amante por celos. No soportó la culpa, guardó el cuerpo… y empezó a ser ella.", {"psiquiatra", "ella"}),
 ({"fondo": "negro", "el": [("hombre", 540, 1280, .9, {"anim": "acercar"})], "vineta": .95, "pulso": .6, "bpm": 60, "cam": (1, 1.2, 0, 0)}, "La última escena es Norman, solo en una celda, mientras escuchamos la voz de la madre en su cabeza. Ya no queda nada de él.", {"madre"}),
]
D = [
 ({"fondo": "biblioteca", "el": [("libro", 540, 1100, 1.0, {"anim": "entrar", "var": "Psicosis|Robert Bloch"})], "cam": (1, 1.06, 0, 0)}, "La película adapta la novela de Robert Bloch, de mil novecientos cincuenta y nueve. Y Bloch se inspiró en un caso real: Ed Gein, un asesino de Wisconsin que también vivía obsesionado con su madre muerta.", {"gein", "real"}),
 ({"fondo": "estudio", "el": [("camara_cine", 540, 1100, 1.0, {"anim": "entrar"})], "tag": "806.947 USD", "tag_y": 1380, "tag_col": VERDE_T, "cam": (1, 1.08, 0, 0)}, "Al estudio Paramount no le gustó la historia y le dio a Hitchcock un presupuesto mínimo: unos ochocientos mil dólares. Él la filmó en blanco y negro, con el equipo de su programa de televisión.", {"paramount", "televisión"}),
 ("H", "Hitchcock protegió el final como un tesoro. Y cuando se estrenó, exigió algo que nunca se había visto: nadie podía entrar a la sala después de empezar la película.", {"final", "nadie"}),
 ({"fondo": "negro", "el": [("cronometro", 540, 1050, 1.0, {"anim": "entrar"})], "tag": "7 DÍAS · 78 TOMAS", "tag_y": 1380, "tag_col": ROJO, "cam": (1, 1.1, 0, 0)}, "La escena de la ducha dura unos cuarenta y cinco segundos en pantalla… pero tomó siete días de rodaje y setenta y ocho posiciones de cámara.", {"siete", "ducha"}),
 ({"fondo": "estudio", "el": [("lupa", 540, 1080, .9, {"anim": "entrar"})], "cam": (1, 1.06, 0, 0)}, "Y la sangre era jarabe de chocolate: en blanco y negro se veía más real que la sangre falsa.", {"chocolate"}),
 ({"fondo": "estudio", "el": [("sonido", 540, 1050, 1.0, {"anim": "latir"})], "cam": (1, 1.08, 0, 0)}, "Hitchcock quería esa escena sin música. El compositor Bernard Herrmann lo convenció de lo contrario, con esos violines agudos que hoy todos reconocemos.", {"violines"}),
 ({"fondo": "estudio", "el": [("dinero", 540, 1060, .9, {"anim": "entrar"})], "cam": (1, 1.06, 0, 0)}, "Dato curioso: a Anthony Perkins le pagaron cuarenta mil dólares por ser Norman. Exactamente la misma cantidad que roba Marion en la película.", {"cuarenta"}),
 ({"fondo": "cine", "el": [("trofeo", 540, 1060, .9, {"anim": "entrar"})], "tag": "50 MILLONES USD", "tag_y": 1380, "tag_col": VERDE_T, "cam": (1, 1.08, 0, 0)}, "Las críticas al principio fueron mixtas, pero el público hizo filas enormes. Recaudó unos cincuenta millones de dólares y tuvo cuatro nominaciones al Óscar, aunque no ganó ninguno.", {"cincuenta", "óscar"}),
]
O = [
 ("H", "Para mí, Psicosis es la madre de todo el cine de asesinos que vino después. Sin Norman Bates no existirían muchos de los villanos que hoy amamos odiar.", {"madre"}),
 ("H", "Lo más genial es cómo te engaña: te hace seguir a una ladrona, y de repente te cambia la película por completo. Ese giro sigue funcionando más de sesenta años después.", {"giro"}),
 ("H", "Anthony Perkins está perfecto: tierno, nervioso… y aterrador. Te da lástima y miedo al mismo tiempo.", {"perkins"}),
 ({"fondo": "cine", "el": [("ojo", 540, 900, .6)]}, "¿Lo malo? Para el público de hoy, el inicio puede sentirse lento, y el final explica demasiado. Pero son detalles frente a lo que logró.", {"lento"}),
]
esc, g = resena_completa("PSICOSIS", "", "1960 · ALFRED HITCHCOCK", "llave", GANCHO,
    "Hoy reseñamos Psicosis, de Alfred Hitchcock. La película que cambió las reglas del terror… y que hizo que medio mundo le tuviera miedo a la ducha.", H, D, O, 5,
    "Mi calificación: cinco de cinco. Una obra maestra que hay que ver al menos una vez. Y después de verla… vas a cerrar la cortina del baño con cuidado.",
    obj1="pajaro", gancho_detras="Y lo que pasó detrás de cámaras es casi tan increíble como la película. Hitchcock tuvo que pelear contra su propio estudio para hacerla.")
if __name__ == "__main__": correr(esc, g, "psicosis", PRON)
