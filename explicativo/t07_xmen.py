"""Comics Store · Serie "Camino a Doomsday" Cap. 6 — Los X-Men: su historia y cronología.
Uso: FORMATO=horizontal python3 t07_xmen.py yt salida.mp4  |  python3 t07_xmen.py s1..s4 salida.mp4
Imágenes en IMG_DIR: 01 mansión, 02 hangar con jet, 03 sala de entrenamiento, 04 robots gigantes en ruinas, 05 ave de fuego cósmica, 06 multitud protestando."""
import os, sys
os.environ.setdefault("SEMILLA", "xmen")
os.environ.setdefault("IMG_DIR", "/home/claude/xmen/img")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import clima
from t03_asi_nacio_doom import *
from t03_asi_nacio_doom import _tramo, _lista, L
from t02_si_dejaste_marvel import e_centinelas
from t05_incursiones import e_revela
from motor import render

# Voz permanente (28-nov): los nombres en inglés vienen de PRON_BASE; aquí solo los que faltan, también en inglés.
PRON = {w.lower(): ("en", w) for w in ["Xavier", "Jean", "Grey", "Rogue", "Kitty", "Pryde", "Claremont", "Len", "Wein", "Dave", "Cockrum", "Jim",
        "Lee", "Stan", "Jack", "Kirby", "Hugh", "Jackman", "Patrick", "Stewart", "Ian", "McKellen", "James", "Marsden", "Rebecca", "Romijn",
        "Alan", "Cumming", "Kelsey", "Grammer", "Channing", "Tatum", "Fox", "Giant-Size", "Thunderbird", "Ororo", "Guinness", "Kelly", "Jennifer",
        "Lawrence", "Marvels", "Krakoa", "Scott", "Summers", "Carol", "Danvers", "Logan", "Oscar", "Dark", "Phoenix", "Jonathan", "Hickman", "BAMF", "John", "Byrne", "Russo", "Infinity", "War", "Endgame"]}
PRON.update({"x-men": ("es", "équis men"), "x2": ("es", "équis dos"), "x-men,": ("es", "équis men")})
AMX = (255, 200, 30)
COLORES = (AMX, (90, 160, 255))

def e_estrellas_x(titulo, nota=5):
    def f(t, d):
        c = cosmos(t, "azul"); figura(c, "wolverine_garras", P(W / 2, W * .82), PISO, P(560, 560), t, "der", alpha=P(.35, 1), reflejo=False)
        texto(c, titulo, P(W / 2, W * .4), P(620, 300), P(64, 64), (255, 255, 255), glow_col=AMX)
        estrellas(c, t, nota, P(W / 2, W * .4), P(900, 520)); texto(c, f"{nota} / 5", P(W / 2, W * .4), P(1120, 700), P(90, 84), ORO, alpha=eo(pr(t, 1.5, .3)), glow_col=ORO)
        return zoom(c, t, d, 1.0, 1.05)
    return S("estrellas", f)

def e_continuara_x():
    def f(t, d):
        c = cosmos(t, "doom", velocidad=.5); figura(c, "loki_casco", W / 2, PISO, FH * .9, t, "pop", alpha=.6)
        c.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 90)))
        texto(c, "CONTINUARÁ…", W / 2, P(860, 470), P(130, 140), (255, 255, 255), alpha=eo(pr(t, .5, .6)), glow_col=VERDE, stroke=8)
        chip(c, "CAP. 7 · LOKI", W / 2, P(1100, 650), ORO, P(40, 40), eo(pr(t, 1.2, .4)))
        return c
    return S("continuara", f)

def e_cta_x(youtube=False):
    def f(t, d):
        c = cosmos(t, "azul")
        figura(c, "wolverine_pie", P(W / 2, W * .24), P(1180, 880), P(760, 700), t, "pop", reflejo=False)
        caja_comentario(c, t, "MUTANTE", x=P(W / 2, W * .68), y=P(1320, 400), col=AMX)
        if youtube: chip(c, "HISTORIA COMPLETA EN YOUTUBE", W / 2, P(1560, 900), ROJO, P(40, 38), eo(pr(t, 1.6, .3)), (40, 6, 10))
        barra_suscribir(c, t, x=P(W / 2, W * .68), y=P(1740, 600), inicio=2.0 if youtube else 1.4)
        return c
    return S("cta", f)

ORIG = ["ciclope_pie", "jean_salto", "bestia_clasico"]

def bloques():
    B = {}
    B["intro"] = [
        L(e_narrador(), INTRO_GAMER[0], *INTRO_GAMER[1]),
        L(e_foto(6, chip_txt="EL MUNDO LOS ODIA", mov=1), "Nacieron con poderes. El mundo los odió por eso. Y aun así, decidieron protegerlo.", "poderes", "odió"),
        L(e_impacto("LOS\nX-MEN", AMX, "azul", fig="wolverine_garras"), "Ellos son los X-Men.", "x-men"),
        L(e_grupo(["ciclope_pie", "jean_salto", "tormenta_pie", "wolverine_pie"], "CAMINO A DOOMSDAY · CAP. 6", "azul", AMX), "Bienvenido al capítulo seis de Camino a Doomsday: los X-Men, su historia y su cronología.", "x-men", "historia"),
        L(e_dos("nightcrawler_pie", "rogue_vuelo", "FIGURAS DE COMICS STORE", "mistico", chip_col=ORO), "Y como siempre, todas las figuras que vas a ver son de nuestra tienda, Comics Store.", "figuras", "comics", "store"),
        L(e_narrador(), "Quédate hasta el final, porque te cuento qué X-Men vuelven en Avengers Doomsday. Y es la reunión más grande en la historia del cine de Marvel.", "final", "doomsday"),
    ]
    B["cap1"] = [
        L(e_capitulo(1, "1963: LOS HIJOS DEL ÁTOMO", AMX, "azul"), "Capítulo uno. Mil novecientos sesenta y tres: los hijos del átomo.", "átomo"),
        L(e_comic("1963", "#1", fig="xavier_silla", titulo="THE X-MEN"), "Los X-Men aparecieron en septiembre de mil novecientos sesenta y tres, creados por Stan Lee y Jack Kirby.", "sesenta", "kirby"),
        L(e_narrador(), "¿Y por qué mutantes? Porque Stan no quería inventar otro accidente con radiación para explicar los poderes. Así que decidió que estos héroes nacieran con ellos.", "mutantes", "nacieran"),
        L(e_foto(1, chip_txt="LA ESCUELA DE XAVIER", mov=1), "El profesor Charles Xavier, el telépata más poderoso del mundo, abrió una escuela para jóvenes con dones.", "xavier", "escuela"),
        L(e_fig("xavier_silla", "PROFESOR X", "mistico"), "Ahí los entrenaba para controlar sus poderes… y para proteger a una humanidad que les tenía miedo.", "miedo"),
        L(e_foto(3, chip_txt="LA SALA DE PELIGRO", mov=2), "Para entrenar tenían la Sala de Peligro, un cuarto lleno de trampas que ya aparecía en ese primer número.", "sala", "peligro"),
        L(e_foto(2, chip_txt="EL PÁJARO NEGRO", mov=1), "Y para viajar por el mundo, su famoso avión supersónico: el Pájaro Negro.", "avión", "negro"),
        L(e_grupo(ORIG, "LOS 5 ORIGINALES", "azul", AMX), "Los primeros alumnos fueron cinco: Cíclope, Jean Grey, Bestia, el Ángel y el Hombre de Hielo.", "cinco", "originales"),
        L(e_fig("bestia_clasico", "BESTIA", "azul"), "Bestia, un genio con la fuerza y la agilidad de un gorila. El Ángel, un joven millonario con alas. Y el Hombre de Hielo, el bromista del grupo, que congela todo lo que toca.", "bestia", "hielo"),
        L(e_fig("ciclope_pie", "CÍCLOPE", "rojo"), "Cíclope dispara rayos por los ojos y no puede apagarlos. Por eso siempre lleva su visor.", "rayos", "visor"),
        L(e_fig("xavier_silla", "CEREBRO", "mistico"), "Xavier además usa Cerebro, una máquina que amplifica su mente para encontrar mutantes en cualquier parte del planeta.", "cerebro", "planeta"),
        L(e_fig("jean_salto", "JEAN GREY", "mistico"), "Jean Grey, telépata y telequinética. Guarda su nombre, porque más adelante se convertiría en una de las fuerzas más poderosas del universo.", "jean", "poderosas"),
        L(e_fig("magneto_pie", "MAGNETO · #1", "rojo"), "Y en ese mismo número uno apareció su gran enemigo: Magneto, el amo del magnetismo.", "magneto"),
    ]
    B["cap2"] = [
        L(e_capitulo(2, "XAVIER VS MAGNETO", (200, 60, 200), "mistico"), "Capítulo dos. Xavier contra Magneto.", "xavier", "magneto"),
        L(e_dos("xavier_silla", "magneto_mckellen", "DOS SUEÑOS", "mistico", vs=True), "Xavier soñaba con que humanos y mutantes vivieran en paz.", "paz"),
        L(e_fig("magneto_vuelo", "EL OTRO CAMINO", "rojo"), "Magneto pensaba lo contrario: que los humanos nunca los iban a aceptar, y que los mutantes debían defenderse… o gobernar.", "defenderse", "gobernar"),
        L(e_narrador(), "Y con el tiempo se reveló algo que cambió al personaje: Magneto es un sobreviviente del Holocausto. Ya había visto lo que pasa cuando un pueblo es perseguido.", "sobreviviente", "perseguido"),
        L(e_foto(6, chip_txt="MIEDO A LO DIFERENTE", mov=3), "Por eso los X-Men siempre fueron más que superhéroes: hablaban de discriminación y de miedo a lo diferente. Muchos lectores se sentían identificados.", "discriminación", "identificados"),
        L(e_impacto("PROTEGER UN MUNDO\nQUE LOS ODIA", AMX, "azul"), "Protegían a un mundo que les temía y los odiaba. Esa frase define a los X-Men.", "temía", "odiaba"),
        L(e_fig("magneto_cerca", "MAGNETO AL MANDO", "rojo"), "Y aunque parezca increíble, en mil novecientos ochenta y cinco Xavier dejó a Magneto como director de su escuela. El villano se volvió maestro de los X-Men.", "director", "maestro"),
    ]
    B["cap3"] = [
        L(e_capitulo(3, "CANCELADOS… Y RESUCITADOS", (255, 140, 40), "rojo"), "Capítulo tres. Cancelados… y resucitados.", "cancelados"),
        L(e_impacto("1970\nCANCELADOS", ROJO, "rojo", fig="ciclope_pie"), "Pero al principio los X-Men no vendían. En mil novecientos setenta dejaron de salir historias nuevas, y la serie solo publicaba reimpresiones.", "vendían", "reimpresiones"),
        L(e_comic("1975", "#1", fig="tormenta_rayo", titulo="GIANT-SIZE X-MEN"), "Hasta que en mayo de mil novecientos setenta y cinco, Len Wein y Dave Cockrum crearon Giant-Size X-Men número uno, con un equipo nuevo e internacional.", "setenta", "internacional"),
        L(e_fig("tormenta_vuelo", "TORMENTA", "azul"), "Tormenta, que controla el clima y era venerada como una diosa en África.", "tormenta", "clima"),
        L(e_fig("tormenta_pie", "LÍDER DE LOS X-MEN", "azul"), "Años después se convirtió en líder del equipo. Y llegó a ganarle un duelo a Cíclope… sin usar sus poderes.", "líder", "poderes"),
        L(e_fig("nightcrawler_salto", "RONDADOR NOCTURNO", "mistico"), "Rondador Nocturno, de Alemania: se teletransporta y parece un demonio… pero es uno de los más bondadosos del grupo.", "teletransporta", "bondadosos"),
        L(e_fig("nightcrawler_agacha", "¡BAMF!", "mistico"), "Cada vez que se teletransporta, en los cómics suena un ruido muy famoso: BAMF.", "bamf"),
        L(e_fig("wolverine_garras", "WOLVERINE", "rojo", sacude=True), "Y Wolverine, de Canadá, con garras y un factor de curación. Había aparecido un año antes, peleando contra Hulk.", "wolverine", "hulk"),
        L(e_fig("wolverine_pie", "ADAMANTIUM", "rojo"), "Su esqueleto está cubierto de adamantium, el metal más resistente de Marvel. Por eso sus garras cortan casi cualquier cosa.", "adamantium", "garras"),
        L(e_grupo(["tormenta_pie", "nightcrawler_pie", "wolverine_pie"], "LOS NUEVOS X-MEN", "azul", AMX), "También llegaron Coloso, de Rusia, y Banshee, de Irlanda. Un equipo de todo el mundo.", "coloso", "mundo"),
        L(e_fig("ciclope_pie", "CHRIS CLAREMONT", "azul"), "Luego llegó el guionista Chris Claremont, que escribió a los X-Men durante dieciséis años y los convirtió en un fenómeno.", "claremont", "dieciséis"),
        L(e_narrador(), "Y con Claremont llegaron las historias más famosas de los X-Men. Empezando por la más trágica de todas.", "trágica"),
    ]
    B["cap4"] = [
        L(e_capitulo(4, "FÉNIX OSCURA", (255, 100, 30), "rojo"), "Capítulo cuatro. Fénix Oscura.", "fénix"),
        L(e_foto(5, chip_txt="EL FÉNIX", mov=1), "Jean Grey se sacrificó para salvar a sus amigos en el espacio… y renació como el Fénix.", "renació", "fénix"),
        L(e_fig("fenix_alas", "UN PODER CÓSMICO", "rojo"), "Un poder cósmico casi infinito.", "cósmico"),
        L(e_impacto("FÉNIX\nOSCURA", (255, 100, 30), "rojo", fig="fenix_llama"), "Pero ese poder la corrompió. Se convirtió en Fénix Oscura… y llegó a consumir una estrella entera, con todo un planeta habitado.", "corrompió", "estrella"),
        L(e_comic("1980", "#129-137", fig="fenix_llama", titulo="LA SAGA DE FÉNIX OSCURA"), "Esa saga va del número ciento veintinueve al ciento treinta y siete, escrita por Chris Claremont y dibujada por John Byrne. Muchos la consideran la mejor historia de los X-Men.", "byrne", "mejor"),
        L(e_dos("jean_estatua", "ciclope_pie", "EL SACRIFICIO", "rojo", chip_col=(255, 100, 30)), "Al final, para no volver a perder el control, Jean se sacrificó frente a Cíclope. Fue en el número ciento treinta y siete, de mil novecientos ochenta.", "sacrificó", "ochenta"),
        L(e_narrador(), "Una muerte que cambió los cómics para siempre. Aunque claro… esto es Marvel, y Jean volvió.", "cambió", "volvió"),
    ]
    B["cap5"] = [
        L(e_capitulo(5, "DÍAS DEL FUTURO PASADO", ROJO, "rojo"), "Capítulo cinco. Días del futuro pasado.", "futuro"),
        L(e_foto(4, chip_txt="LOS CENTINELAS", mov=1, sacude=True), "En mil novecientos ochenta y uno llegó otra historia legendaria: un futuro donde robots gigantes, los Centinelas, cazan a los mutantes.", "centinelas", "cazan"),
        L(e_centinelas(), "Para evitarlo, Kitty Pryde envía su mente al pasado. Tiene que impedir el asesinato que desató todo.", "kitty", "asesinato"),
        L(e_impacto("SOLO 2\nNÚMEROS", ROJO, "rojo", fig="mistica_pie"), "Lo increíble es que Días del futuro pasado ocupó solo dos números, el ciento cuarenta y uno y el ciento cuarenta y dos. Y aun así inspiró una película y una de las mejores sagas de la serie animada.", "dos", "inspiró"),
        L(e_fig("mistica_pie", "MÍSTICA", "azul"), "¿Y quién iba a cometer ese asesinato? Mística, la mutante que puede tomar la forma de cualquiera, con su Hermandad de Mutantes.", "mística", "hermandad"),
        L(e_fig("nightcrawler_agacha", "SU HIJO", "mistico"), "Dato loco: Mística es la madre biológica del Rondador Nocturno.", "madre", "rondador"),
        L(e_fig("rogue_estatua", "ROGUE", "doom"), "Y también fue la madre adoptiva de Rogue, que empezó como villana… y terminó uniéndose a los X-Men.", "rogue", "villana"),
        L(e_fig("rogue_vuelo", "ABSORBE PODERES", "doom"), "Rogue absorbe los poderes y los recuerdos de quien toca. Por eso no puede tocar a nadie.", "absorbe", "nadie"),
        L(e_fig("rogue_busto", "SUPERFUERZA Y VUELO", "doom"), "Y una vez absorbió para siempre los poderes de Carol Danvers, la futura Capitana Marvel. Por eso Rogue vuela y tiene superfuerza.", "danvers", "vuela"),
    ]
    B["extra"] = [
        L(e_capitulo(6, "KRAKOA", (60, 220, 120), "doom"), "Capítulo seis. Krakoa: la nación mutante.", "krakoa"),
        L(e_impacto("UNA ISLA\nVIVA", (60, 220, 120), "doom"), "¿Recuerdas Giant-Size X-Men? En ese número, el enemigo era Krakoa: una isla viva.", "isla", "viva"),
        L(e_foto(1, chip_txt="LA ERA DE KRAKOA · 2019", mov=3), "En dos mil diecinueve, Jonathan Hickman, el mismo de las incursiones, convirtió esa isla en una nación para todos los mutantes.", "hickman", "nación"),
        L(e_dos("xavier_silla", "magneto_mckellen", "JUNTOS", "doom", chip_col=(60, 220, 120)), "Y lo más loco: Xavier y Magneto la gobernaron juntos. Héroes y villanos mutantes, en el mismo bando.", "juntos", "bando"),
        L(e_narrador(), "Hickman vuelve a aparecer en esta serie. Si viste los capítulos anteriores, ya sabes que ese guionista está detrás de casi todo lo que lleva a Doomsday.", "hickman", "doomsday"),
    ]
    B["cap6"] = [
        L(e_capitulo(7, "LOS AÑOS 90", (255, 70, 170), "mistico"), "Capítulo siete. Los años noventa.", "noventa"),
        L(e_comic("1991", "#1", fig="ciclope_pie", titulo="X-MEN"), "En mil novecientos noventa y uno, X-Men número uno, de Chris Claremont y Jim Lee, vendió unos ocho millones cien mil ejemplares.", "ocho", "millones"),
        L(e_impacto("RÉCORD\nGUINNESS", ORO, "azul"), "Todavía hoy es el cómic más vendido de la historia, según el récord Guinness.", "guinness"),
        L(e_grupo(["gambit_pie", "rogue_busto", "wolverine_pie", "tormenta_pie"], "LA SERIE ANIMADA", "mistico", (255, 70, 170)), "Y en mil novecientos noventa y dos llegó la serie animada, que muchos vimos de niños por televisión.", "animada", "televisión"),
        L(e_fig("gambit_pie", "GAMBITO", "mistico"), "Ahí se hicieron famosos personajes como Gambito, que lanza cartas cargadas de energía. Gambito había nacido en los cómics apenas en mil novecientos noventa.", "gambito", "cartas"),
        L(e_dos("ciclope_pie", "jean_salto", "LA BODA", "azul", chip_col=(255, 70, 170)), "Y en mil novecientos noventa y cuatro, Cíclope y Jean Grey por fin se casaron, en uno de los números más vendidos de la década.", "casaron"),
        L(e_narrador(), "Y en dos mil veinticuatro volvió con X-Men noventa y siete. Para muchos fans, una de las mejores series que ha hecho Marvel.", "noventa", "mejores"),
    ]
    B["cap7"] = [
        L(e_capitulo(8, "EN EL CINE", ORO, "azul"), "Capítulo ocho. En el cine.", "cine"),
        L(e_dos("xavier_silla", "magneto_mckellen", "STEWART Y McKELLEN", "mistico", chip_col=ORO), "En el cine todo empezó en el año dos mil, con Patrick Stewart como Xavier e Ian McKellen como Magneto.", "stewart", "mckellen"),
        L(e_fig("wolverine_garras", "HUGH JACKMAN", "rojo"), "Y un actor casi desconocido como Wolverine: Hugh Jackman. Lo interpretó durante más de veinte años.", "jackman", "veinte"),
        L(e_fig("wolverine_garras", "LOGAN · 2017", "rojo"), "Su despedida, Logan, de dos mil diecisiete, fue nominada al Oscar a mejor guion adaptado. Algo histórico para una película de superhéroes.", "logan", "oscar"),
        L(e_foto(4, chip_txt="DÍAS DEL FUTURO PASADO · 2014", mov=2), "Y Días del futuro pasado, de dos mil catorce, juntó a los X-Men clásicos con los jóvenes, y recaudó unos setecientos cuarenta y siete millones de dólares.", "setecientos", "millones"),
        L(e_fig("fenix_llama", "FÉNIX EN EL CINE", "rojo"), "La saga de Fénix Oscura se llevó dos veces al cine: en La Batalla Final, de dos mil seis, y en Dark Phoenix, de dos mil diecinueve. Ninguna convenció a los fans.", "dos", "fans"),
        L(e_fig("mistica_estatua", "REBECCA ROMIJN", "azul"), "Rebecca Romijn fue Mística, antes de que Jennifer Lawrence tomara el papel.", "romijn", "mística"),
        L(e_fig("nightcrawler_espadas", "ALAN CUMMING", "mistico"), "Alan Cumming fue el Rondador Nocturno en X2, de dos mil tres.", "cumming", "rondador"),
        L(e_fig("bestia_mcu", "KELSEY GRAMMER", "azul"), "Y Kelsey Grammer fue Bestia en La Batalla Final… y reapareció en la escena post créditos de The Marvels.", "grammer", "marvels"),
        L(e_impacto("DISNEY\nCOMPRA FOX", (120, 170, 255), "azul"), "En marzo de dos mil diecinueve, Disney completó la compra de Fox, y los X-Men volvieron a casa.", "disney", "casa"),
        L(e_dos("wolverine_garras", "gambit_pie", "DEADPOOL & WOLVERINE", "rojo", chip_col=ROJO), "Deadpool y Wolverine, en dos mil veinticuatro, recaudó más de mil trescientos millones de dólares… y nos mostró por fin al Gambito de Channing Tatum.", "mil", "tatum"),
    ]
    B["cap8"] = [
        L(e_capitulo(9, "RUMBO A DOOMSDAY", VERDE, "doom"), "Capítulo nueve. Rumbo a Doomsday.", "doomsday"),
        L(e_foto(1, chip_txt="REGRESAN", mov=4, oscuro=.3), "Y ahora, en Avengers Doomsday, regresan los X-Men de Fox.", "regresan"),
        L(_lista(["PATRICK STEWART", "IAN McKELLEN", "JAMES MARSDEN", "REBECCA ROMIJN", "ALAN CUMMING", "KELSEY GRAMMER", "CHANNING TATUM"], "xavier_silla", AMX, "azul"),
          "Patrick Stewart, Ian McKellen, James Marsden como Cíclope, Rebecca Romijn, Alan Cumming, Kelsey Grammer y Channing Tatum como Gambito.", "marsden", "tatum"),
        L(e_universos(("X-MEN", "VENGADORES", "4 FANTÁSTICOS"), ("wolverine_pie", "cap_sincasco", "reed_legends")), "Tres universos distintos en una sola historia, contra Doctor Doom.", "tres", "doom"),
        L(e_impacto("18 DE\nDICIEMBRE", VERDE, "doom", fig="doom_pie3"), "Avengers Doomsday llega a los cines el dieciocho de diciembre de dos mil veintiséis, dirigida por los hermanos Russo, los mismos de Infinity War y Endgame.", "dieciocho", "russo"),
        L(e_dos("xavier_silla", "doom_pie3", "XAVIER VS DOOM", "doom", vs=True), "La mente más poderosa del mundo mutante… frente al hombre que quiere ser Dios.", "mente", "dios"),
        L(e_narrador(), "¿Y Wolverine? Hugh Jackman no fue anunciado en el elenco… pero en Marvel nunca se sabe. Lo descubriremos el dieciocho de diciembre.", "wolverine", "dieciocho"),
    ]
    B["cierre"] = [
        L(e_narrador(), "¿Mi opinión? Los X-Men son el grupo con más corazón de Marvel. Son una familia de marginados que decidió proteger al mismo mundo que los rechaza.", "opinión", "familia"),
        L(e_dos("xavier_silla", "magneto_vuelo", "¿QUIÉN TENÍA RAZÓN?", "mistico", vs=True), "Y la gran pregunta sigue abierta: ¿quién tenía razón, Xavier o Magneto? Te leo en los comentarios.", "razón", "comentarios"),
        L(e_estrellas_x("¿EL MEJOR EQUIPO DE MARVEL?", 5), "¿Mi nota? Cinco de cinco.", "cinco"),
        L(e_grupo(["nightcrawler_espadas", "fenix_alas", "rogue_vuelo"], "COMICS-STORE.COM.CO", "azul", ORO), "Y si quieres estas figuras, como el Rondador Nocturno, el Fénix o Rogue, las encuentras en Comics Store: comics store punto com punto co.", "fénix", "rogue"),
        L(e_continuara_x(), "En el próximo capítulo: Loki, el dios que sostiene el multiverso. Continuará…", "loki", "continuará"),
        L(e_cta_x(), "Comenta MUTANTE si quieres el capítulo siete, suscríbete y activa la campanita. ¡Nos vemos en el próximo video!", "mutante"),
    ]
    return B

FOTO_AMB_X = {1: "viento", 2: "maquina", 3: "maquina+magia", 4: "explosion+fuego", 5: "fuego+cosmos", 6: "noche+viento"}
FOTO_CLIMA_X = {1: "viento", 2: None, 3: None, 4: "fuego", 5: "fuego", 6: "fuego"}
CLAVE_AMB_X = [("centinelas", "maquina"), ("fénix", "fuego"), ("magneto", "magia"), ("tormenta", "tormenta"), ("doom", "magia"), ("wolverine", "impacto")]
CLAVE_CLIMA_X = [("tormenta, que controla", "tormenta"), ("consumir una estrella", "explosion")]

def preparar(esc):
    for fn, txt, _ in esc:
        low = txt.lower(); a = None
        if getattr(fn, "foto", None): a = FOTO_AMB_X.get(fn.foto); fn.clima = FOTO_CLIMA_X.get(fn.foto)
        else:
            if fn.__name__ != "narrador": fn.clima = next((v for k, v in CLAVE_CLIMA_X if k in low), None)
            a = next((v for k, v in CLAVE_AMB_X if k in low), None)
            if not a: a = {"impacto": "impacto+magia", "capitulo": "cosmos", "continuara": "cosmos+magia", "estrellas": "magia"}.get(fn.__name__)
        if a: fn.amb = a
    return clima.envolver(esc)

def guion_yt():
    B = bloques(); esc = []
    for k in ("intro", "cap1", "cap2", "cap3", "cap4", "cap5", "extra", "cap6", "cap7", "cap8", "cierre"): esc += B[k]
    esc = preparar(esc)
    re_ = [i for i, e in enumerate(esc) if e[0].__name__ == "narrador" and i > 0]
    return esc, re_

def _short(gancho, tramo):
    gancho[0].amb = "impacto+magia"
    return [gancho] + tramo + [L(e_cta_x(youtube=True), "Comenta MUTANTE, y mira la historia completa en nuestro canal de YouTube.", "mutante", "youtube")]

def guion_short(n):
    esc, _ = guion_yt()
    if n == 1: return _short(L(e_impacto("¿POR QUÉ\nMUTANTES?", AMX, "azul", fig="xavier_silla"), "¿Sabes por qué los X-Men nacieron con sus poderes?", "poderes"),
                             _tramo(esc, "Los X-Men aparecieron en septiembre", "Cíclope dispara") + _tramo(esc, "Xavier soñaba", "Protegían a un mundo"))
    if n == 2: return _short(L(e_impacto("8 MILLONES\nDE COPIAS", ORO, "azul", fig="ciclope_pie"), "El cómic más vendido de la historia es de los X-Men.", "vendido"),
                             _tramo(esc, "En mil novecientos noventa y uno, X-Men", "Y en mil novecientos noventa y cuatro"))
    if n == 3: return _short(L(e_impacto("FÉNIX\nOSCURA", (255, 100, 30), "rojo", fig="fenix_alas"), "La heroína que destruyó una estrella entera.", "estrella"),
                             _tramo(esc, "Jean Grey, telépata", "Y en ese mismo número") + _tramo(esc, "Jean Grey se sacrificó para salvar", "Una muerte que cambió") + _tramo(esc, "La saga de Fénix Oscura se llevó", "En marzo de dos mil"))
    if n == 4: return _short(L(e_impacto("LOS X-MEN\nVUELVEN", VERDE, "doom", fig="wolverine_garras"), "Los X-Men originales del cine vuelven en Avengers Doomsday.", "vuelven"),
                             _tramo(esc, "En el cine todo empezó", "Rebecca Romijn fue") + _tramo(esc, "Y ahora, en Avengers Doomsday", "¿Y Wolverine?"))

if __name__ == "__main__":
    v = sys.argv[1]; out = sys.argv[2]
    if v == "yt": esc, re_ = guion_yt()
    else: esc, re_ = guion_short(int(v[1])), None
    if os.environ.get("CONTAR"):
        print(v, len(esc), "escenas", sum(len(e[1].split()) for e in esc), "palabras"); sys.exit()
    if os.environ.get("HOJA"):
        tiles = []
        for fn, txt, cl in esc:
            fr = fn(1.8, 4.0).convert("RGB"); tiles.append(fr.resize((fr.width // 5, fr.height // 5)))
        tw, th = tiles[0].size; cols = 8 if tw < th else 6; rows = (len(tiles) + cols - 1) // cols; sh = Image.new("RGB", (tw * cols, th * rows))
        for i, im in enumerate(tiles): sh.paste(im, ((i % cols) * tw, (i // cols) * th))
        sh.save(out); print("hoja", len(tiles)); sys.exit()
    render(esc, out, regancho_idx=re_, musica="epica", pron=PRON, estilo="neon", colores=COLORES,
           formato="horizontal" if lib.HORIZONTAL else "vertical", y_sub=250)
