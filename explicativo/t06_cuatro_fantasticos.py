"""Comics Store · Serie "Camino a Doomsday" Cap. 5 — Los 4 Fantásticos: su historia completa.
Uso: FORMATO=horizontal python3 t06_cuatro_fantasticos.py yt salida.mp4  |  python3 t06_cuatro_fantasticos.py s1..s4 salida.mp4
Imágenes en IMG_DIR: 01 cohete retro, 02 nave con rayos cósmicos, 03 edificio con el 4, 04 planeta devorado, 05 laboratorio retro."""
import os, sys
os.environ.setdefault("SEMILLA", "cuatro")
os.environ.setdefault("IMG_DIR", "/home/claude/cuatro/img")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import clima
from t03_asi_nacio_doom import *
from t03_asi_nacio_doom import PRON as PRON3, _tramo, _lista, L
from t05_incursiones import e_revela
from motor import render

PRON = dict(PRON3); PRON.update({"stan": ("es", "stan"), "lee": ("es", "li"), "jack": ("es", "yac"), "kirby": ("es", "kérbi"), "martin": ("es", "mártin"),
    "goodman": ("es", "gúdman"), "sue": ("es", "su"), "storm": ("es", "storm"), "johnny": ("es", "yóni"), "ben": ("es", "ben"), "grimm": ("es", "grim"),
    "it's": ("es", "its"), "clobberin'": ("es", "clóberin"), "time": ("es", "taim"), "moloides": ("es", "moloides"), "galactus": ("es", "galáctus"),
    "silver": ("es", "sílver"), "surfer": ("es", "sérfer"), "annihilus": ("es", "aníjilus"), "franklin": ("es", "fránklin"), "valeria": ("es", "valéria"),
    "hickman": ("es", "jícman"), "jonathan": ("es", "yónatan"), "tim": ("es", "tim"), "story": ("es", "estóri"), "chris": ("es", "cris"), "evans": ("es", "évans"),
    "pedro": ("es", "pédro"), "pascal": ("es", "pascál"), "vanessa": ("es", "vanésa"), "joseph": ("es", "yósef"), "quinn": ("es", "cuin"),
    "ebon": ("es", "ébon"), "moss-bachrach": ("es", "mos bácrac"), "corman": ("es", "córman"), "roger": ("es", "róyer"), "herbie": ("es", "jérbi"),
    "baxter": ("es", "báxter"), "universal": ("es", "universal"), "alicia": ("es", "alísia"), "masters": ("es", "másters"), "ioan": ("es", "yóan"), "gruffudd": ("es", "grífid"), "jessica": ("es", "yésica"), "alba": ("es", "alba"), "michael": ("es", "máikol"), "chiklis": ("es", "chíclis"), "rise": ("es", "ráis"), "josh": ("es", "yosh"), "trank": ("es", "trank"), "miles": ("es", "máils"), "teller": ("es", "téler"), "kate": ("es", "keit"), "mara": ("es", "mára"), "jordan": ("es", "yórdan"), "jamie": ("es", "yéimi"), "bell": ("es", "bel"), "ralph": ("es", "ralf"), "ineson": ("es", "ínesun"), "shalla-bal": ("es", "shála bal"), "julia": ("es", "yúlia"), "garner": ("es", "gárner"), "spider-man": ("es", "espáider man"), "krasinski": ("es", "crasínski"), "john": ("es", "yon"), "killmonger": ("es", "kílmonguer"), "matt": ("es", "mat"), "shakman": ("es", "shákman"), "wandavision": ("es", "uandavíshon")})
AZ4 = (60, 170, 255)
COLORES = (AZ4, (255, 255, 255))

def e_estrellas_f(titulo, nota=5):
    def f(t, d):
        c = cosmos(t, "azul"); figura(c, "cuatro_grupo", P(W / 2, W * .82), PISO, P(560, 560), t, "der", alpha=P(.35, 1), reflejo=False)
        texto(c, titulo, P(W / 2, W * .4), P(620, 300), P(64, 64), (255, 255, 255), glow_col=AZ4)
        estrellas(c, t, nota, P(W / 2, W * .4), P(900, 520)); texto(c, f"{nota} / 5", P(W / 2, W * .4), P(1120, 700), P(90, 84), ORO, alpha=eo(pr(t, 1.5, .3)), glow_col=ORO)
        return zoom(c, t, d, 1.0, 1.05)
    return S("estrellas", f)

def e_continuara_f():
    def f(t, d):
        c = cosmos(t, "mistico", velocidad=.5); figura(c, "wolverine_pie", W / 2, PISO, FH * .9, t, "pop", alpha=.6)
        c.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 90)))
        texto(c, "CONTINUARÁ…", W / 2, P(860, 470), P(130, 140), (255, 255, 255), alpha=eo(pr(t, .5, .6)), glow_col=(255, 210, 40), stroke=8)
        chip(c, "CAP. 6 · LOS X-MEN", W / 2, P(1100, 650), ORO, P(40, 40), eo(pr(t, 1.2, .4)))
        return c
    return S("continuara", f)

def e_cta_f(youtube=False):
    def f(t, d):
        c = cosmos(t, "azul")
        figura(c, "cosa_pie", P(W / 2, W * .24), P(1180, 880), P(760, 700), t, "pop", reflejo=False)
        caja_comentario(c, t, "FANTÁSTICOS", x=P(W / 2, W * .68), y=P(1320, 400), col=AZ4)
        if youtube: chip(c, "HISTORIA COMPLETA EN YOUTUBE", W / 2, P(1560, 900), ROJO, P(40, 38), eo(pr(t, 1.6, .3)), (40, 6, 10))
        barra_suscribir(c, t, x=P(W / 2, W * .68), y=P(1740, 600), inicio=2.0 if youtube else 1.4)
        return c
    return S("cta", f)

FOUR = ["reed_legends", "sue_poder", "antorcha_vuelo", "cosa_pie"]

def bloques():
    B = {}
    B["intro"] = [
        L(e_narrador(), INTRO_GAMER[0], *INTRO_GAMER[1]),
        L(e_foto(3, chip_txt="NUEVA YORK", mov=1), "Antes de los Vengadores. Antes de Spider-Man. Antes de los X-Men… hubo una familia.", "antes", "familia"),
        L(e_impacto("LA PRIMERA\nFAMILIA", AZ4, "azul", fig="cuatro_grupo"), "Una familia que creó todo el Universo Marvel.", "creó", "marvel"),
        L(e_grupo(FOUR, "CAMINO A DOOMSDAY · CAP. 5", "azul", AZ4), "Bienvenido al capítulo cinco de Camino a Doomsday: Los Cuatro Fantásticos, su historia completa.", "cuatro", "fantásticos"),
        L(e_dos("topo_moloides", "annihilus_pie", "FIGURAS DE COMICS STORE", "azul", chip_col=ORO), "Y como siempre, todas las figuras que vas a ver son de nuestra tienda, Comics Store.", "figuras", "comics", "store"),
        L(e_narrador(), "Quédate hasta el final, porque te voy a contar por qué Doctor Doom está obsesionado con un niño de esta familia.", "obsesionado", "niño"),
    ]
    B["cap1"] = [
        L(e_capitulo(1, "1961: NACE MARVEL", AZ4, "azul"), "Capítulo uno. Mil novecientos sesenta y uno: nace Marvel.", "nace"),
        L(e_comic("1961", "#1", fig="cuatro_grupo", titulo="FANTASTIC FOUR"), "Los Cuatro Fantásticos aparecieron en noviembre de mil novecientos sesenta y uno, creados por Stan Lee y Jack Kirby.", "sesenta", "kirby"),
        L(e_narrador(), "Según contaba Stan Lee, su jefe le pidió un equipo de superhéroes porque la competencia estaba vendiendo muy bien con la Liga de la Justicia.", "equipo", "justicia"),
        L(e_fig("reed_pie", "HÉROES DIFERENTES", "azul"), "Pero Stan y Jack hicieron algo distinto: héroes sin identidades secretas, que discutían, peleaban… y se querían como una familia de verdad.", "familia"),
        L(e_fig("antorcha_pie", "NO FUE LA PRIMERA ANTORCHA", "rojo"), "Dato curioso: Johnny no fue la primera Antorcha Humana. En mil novecientos treinta y nueve ya existía otra: un androide que ardía en llamas.", "primera", "androide"),
        L(e_impacto("NACE EL\nUNIVERSO MARVEL", ROJO, "rojo"), "Fue tal el éxito, que ese cómic es considerado el inicio del Universo Marvel moderno.", "éxito", "inicio"),
        L(e_impacto("LA MEJOR REVISTA\nDE CÓMICS DEL MUNDO", ORO, "azul", fig="cuatro_grupo"), "Por algo sus portadas decían, con todo el orgullo: la mejor revista de cómics del mundo.", "mejor", "mundo"),
        L(e_comic("1961", "10¢", fig="cosa_pie", titulo="FANTASTIC FOUR"), "Y ese primer número costaba apenas diez centavos de dólar. Hoy, una copia en buen estado vale una verdadera fortuna.", "diez", "fortuna"),
        L(e_foto(3, chip_txt="EL EDIFICIO BAXTER · #3", mov=3), "Un dato más: en el número uno ni siquiera tenían trajes. Los uniformes azules y su cuartel en Nueva York, el Edificio Baxter, llegaron en el número tres.", "trajes", "baxter"),
        L(e_comic("1961-1970", "102", fig="reed_legends", titulo="LEE & KIRBY"), "Stan Lee y Jack Kirby hicieron juntos ciento dos números seguidos de la serie. Una de las etapas más importantes de la historia del cómic.", "ciento", "historia"),
    ]
    B["cap2"] = [
        L(e_capitulo(2, "EL VUELO", (255, 140, 40), "rojo"), "Capítulo dos. El vuelo.", "vuelo"),
        L(e_foto(1, chip_txt="LA CARRERA ESPACIAL", mov=1), "Reed Richards, un científico brillante, quería llegar al espacio antes que nadie.", "espacio"),
        L(e_fig("cosa_mcu", "BEN NO QUERÍA IR", "rojo"), "Ben, el piloto, no quería ir. Advirtió que la nave no estaba protegida contra los rayos cósmicos. Pero Sue lo convenció.", "advirtió", "convenció"),
        L(e_grupo(FOUR, "LA TRIPULACIÓN", "azul", AZ4), "Lo acompañaron su novia, Sue Storm; el hermano de ella, Johnny; y su mejor amigo, el piloto Ben Grimm.", "sue", "ben"),
        L(e_foto(2, chip_txt="RAYOS CÓSMICOS", mov=3, sacude=True), "Pero la nave no tenía suficiente protección… y los rayos cósmicos los atravesaron.", "rayos", "cósmicos"),
        L(e_impacto("YA NO ERAN\nLOS MISMOS", AZ4, "azul"), "Cuando volvieron a la Tierra, ya no eran los mismos.", "mismos"),
        L(e_narrador(), "Y aquí viene lo bueno: cada uno recibió un poder que de alguna forma reflejaba quién era.", "poder"),
    ]
    B["cap3"] = [
        L(e_capitulo(3, "LOS PODERES", AZ4, "azul"), "Capítulo tres. Los poderes.", "poderes"),
        L(e_fig("reed_legends", "MR. FANTÁSTICO", "azul"), "Reed se volvió elástico: puede estirarse y tomar casi cualquier forma. Pero su verdadero poder es su mente. Es uno de los hombres más inteligentes del universo.", "elástico", "mente"),
        L(e_fig("sue_poder", "LA MUJER INVISIBLE", "azul"), "Sue puede volverse invisible y crear campos de fuerza. Al principio la llamaban la Chica Invisible; en mil novecientos ochenta y cinco pasó a ser la Mujer Invisible. Hoy muchos la consideran la más poderosa del equipo.", "invisible", "poderosa"),
        L(e_dos("reed_pie2", "sue_pie", "LA BODA", "azul", chip_col=AZ4), "Reed y Sue se casaron en el Anual número tres, de mil novecientos sesenta y cinco. A la boda llegaron casi todos los héroes y villanos de Marvel.", "casaron", "boda"),
        L(e_fig("antorcha_vuelo", "LA ANTORCHA HUMANA", "rojo"), "Johnny puede envolverse en llamas y volar. Es el joven impulsivo del grupo, siempre buscando problemas.", "llamas", "volar"),
        L(e_fig("cosa_pie", "LA COSA", "rojo", sacude=True), "Y Ben se convirtió en un gigante de roca naranja. Es el más fuerte… pero también el más triste, porque él no puede volver a ser humano.", "roca", "triste"),
        L(e_fig("cosa_pie", "ALICIA MASTERS", "rojo"), "Pero Ben encontró el amor en Alicia Masters, una escultora ciega que lo quiso por quien era, no por cómo se veía.", "alicia", "ciega"),
        L(e_fig("cosa_mcu", "IT'S CLOBBERIN' TIME", "rojo"), "Aun así, es el corazón del equipo. Y su grito de batalla es legendario: It's clobberin' time. ¡Es hora de los golpes!", "corazón", "golpes"),
        L(e_fig("reed_herbie", "H.E.R.B.I.E.", "azul"), "Un dato curioso: en la serie animada de mil novecientos setenta y ocho, la Antorcha no pudo aparecer por temas de derechos… y la reemplazaron con un robot llamado Herbie.", "herbie", "robot"),
        L(e_narrador(), "Ahora, un equipo así necesitaba villanos a su altura. Y vaya que los tuvo.", "villanos"),
    ]
    B["cap4"] = [
        L(e_capitulo(4, "SUS VILLANOS", VERDE, "doom"), "Capítulo cuatro. Sus villanos.", "villanos"),
        L(e_fig("topo_moloides", "EL HOMBRE TOPO", "doom"), "El primero fue el Hombre Topo, en el número uno, con su ejército de Moloides que vive bajo la tierra.", "topo", "moloides"),
        L(e_fig("topo_pie", "EL PRIMER VILLANO", "doom"), "Sí: el primer villano de toda la era moderna de Marvel fue este señor.", "primer"),
        L(e_foto(2, chip_txt="LOS SKRULLS · #2", mov=4, oscuro=.35), "En el número dos aparecieron los Skrulls, los alienígenas que cambian de forma. Sí, los mismos de Invasión Secreta.", "skrulls", "invasión"),
        L(e_doom("doom_pie3", "DOCTOR DOOM · #5", "sube"), "En el número cinco llegó el más grande: Doctor Doom, el antiguo compañero de universidad de Reed. Su historia completa la contamos en el capítulo dos.", "cinco", "doom"),
        L(e_foto(4, chip_txt="EL DEVORADOR DE MUNDOS", mov=1, sacude=True), "En mil novecientos sesenta y seis llegó una de las historias más famosas del cómic: la Trilogía de Galactus, en los números cuarenta y ocho al cincuenta.", "galactus", "cincuenta"),
        L(e_fig("galactus_brazos", "GALACTUS", "thanos"), "Galactus, el Devorador de Mundos, un ser cósmico que se alimenta de planetas.", "galactus", "planetas"),
        L(e_fig("surfer_tabla", "SILVER SURFER", "azul"), "Y su heraldo, Silver Surfer, que terminó traicionando a su amo para salvar la Tierra.", "surfer", "traicionando"),
        L(e_fig("blackbolt_pie", "LOS INHUMANOS", "mistico"), "Y en sus páginas también nacieron los Inhumanos, con Black Bolt, en el número cuarenta y cinco. Las páginas de los Cuatro Fantásticos crearon medio Universo Marvel.", "inhumanos", "medio"),
        L(e_fig("annihilus_alas", "ANNIHILUS", "doom"), "Y desde la Zona Negativa, Annihilus: un tirano con forma de insecto, obsesionado con vivir para siempre.", "annihilus", "siempre"),
        L(e_comic("1968", "ANUAL #6", fig="annihilus_pie", titulo="FANTASTIC FOUR"), "Annihilus apareció en el Anual número seis de mil novecientos sesenta y ocho… el mismo cómic donde nació alguien muy especial.", "anual", "especial"),
    ]
    B["cap5"] = [
        L(e_capitulo(5, "FRANKLIN Y VALERIA", AZ4, "mistico"), "Capítulo cinco. Franklin y Valeria.", "franklin", "valeria"),
        L(e_fig("franklin_pie", "FRANKLIN RICHARDS", "azul"), "Franklin Benjamin Richards, el hijo de Reed y Sue. Benjamin, por su padrino, Ben Grimm. Para salvar a Sue en el parto, el equipo tuvo que robarle a Annihilus su Vara de Control Cósmico.", "franklin", "vara"),
        L(e_impacto("EL MUTANTE\nMÁS PODEROSO", AZ4, "mistico", fig="franklin_pie"), "Franklin es considerado uno de los mutantes más poderosos del Universo Marvel. De niño llegó a crear universos enteros.", "poderosos", "universos"),
        L(e_fig("futuro_pareja", "VALERIA RICHARDS", "azul"), "Después llegó Valeria, su hermana menor, una genio incluso más inteligente que su papá.", "valeria", "genio"),
        L(e_doom("doom_magia", "DOOM LA NOMBRÓ", "sube"), "Y aquí viene algo increíble: fue Doctor Doom quien ayudó a que Valeria naciera… y fue él quien le puso el nombre.", "doom", "nombre"),
        L(e_narrador(), "El peor enemigo de la familia, con un lazo especial con su hija. Guarda ese detalle, porque Doom y los niños Richards siempre terminan conectados.", "lazo", "conectados"),
    ]
    B["cap6"] = [
        L(e_capitulo(6, "LA ERA HICKMAN", (170, 90, 255), "mistico"), "Capítulo seis. La era Hickman.", "hickman"),
        L(e_comic("2009", "#570", fig="reed_pie2", titulo="FANTASTIC FOUR"), "En dos mil nueve llegó a la serie el guionista Jonathan Hickman. Y lo cambió todo.", "hickman"),
        L(e_grupo(["reed_pie", "reed_legends", "reed_pie2"], "EL CONSEJO DE REEDS", "azul", AZ4), "Reed descubrió el Consejo de Reeds: versiones de sí mismo de otros universos, trabajando juntas para resolver todos los problemas.", "consejo", "versiones"),
        L(e_foto(5, chip_txt="EL LABORATORIO", mov=1), "Le ofrecieron unirse… pero para eso tenía que abandonar a su familia. Y Reed dijo que no.", "familia"),
        L(e_impacto("JOHNNY\nMUERE", ROJO, "rojo", fig="antorcha_pie"), "En dos mil once pasó lo impensable: Johnny Storm murió defendiendo un portal a la Zona Negativa.", "murió", "zona"),
        L(e_fig("futuro_trio", "LA FUNDACIÓN FUTURO", "azul"), "Reed transformó al equipo en la Fundación Futuro: una escuela para los niños más brillantes del mundo.", "fundación", "futuro"),
        L(e_impacto("SPIDER-MAN\nSE UNE", ROJO, "rojo"), "Y en el lugar de Johnny entró alguien inesperado: Spider-Man, como Johnny lo había pedido.", "spider-man"),
        L(e_fig("antorcha_mcu", "JOHNNY REGRESA", "rojo"), "Tranquilo: Johnny regresó poco después. Esto es Marvel.", "regresó"),
        L(e_narrador(), "Y sí: Hickman es el mismo que después escribió las incursiones y Secret Wars. Todo está conectado.", "incursiones", "conectado"),
    ]
    B["cap7"] = [
        L(e_capitulo(7, "EN EL CINE", ORO, "azul"), "Capítulo siete. En el cine.", "cine"),
        L(e_impacto("1994: NUNCA\nSE ESTRENÓ", ROJO, "rojo"), "La primera película se hizo en mil novecientos noventa y cuatro, con apenas un millón de dólares… y nunca se estrenó.", "millón", "estrenó"),
        L(e_fig("reed_pie", "SOLO POR LOS DERECHOS", "rojo"), "Se hizo con el productor Roger Corman para que una compañía alemana no perdiera los derechos. Hoy es una película de culto.", "derechos", "culto"),
        L(e_grupo(FOUR, "2005 · 2007", "azul", AZ4), "En dos mil cinco llegó la versión de Tim Story, con Ioan Gruffudd, Jessica Alba, Michael Chiklis y Chris Evans como la Antorcha, años antes de ser el Capitán América.", "evans", "antorcha"),
        L(e_fig("surfer_surf", "2007 · SILVER SURFER", "azul"), "En dos mil siete llegó la secuela, Rise of the Silver Surfer, con Galactus convertido en una nube cósmica… algo que a muchos fans no les gustó.", "secuela", "nube"),
        L(e_impacto("2015", (120, 120, 140), "azul", fig="cosa_pie"), "En dos mil quince hubo otro intento, mucho más oscuro, dirigido por Josh Trank, con Miles Teller, Kate Mara, Michael B. Jordan y Jamie Bell. Fue un fracaso de crítica y taquilla.", "fracaso"),
        L(e_dos("antorcha_vuelo", "cap_sincasco", "DATO LOCO", "rojo", chip_col=ORO), "Dato loco: dos de los actores que hicieron de la Antorcha Humana terminaron siendo otros héroes. Chris Evans fue el Capitán América, y Michael B. Jordan fue Killmonger.", "evans", "killmonger"),
        L(e_foto(3, chip_txt="TIERRA-828", mov=2), "Hasta que en julio de dos mil veinticinco llegó Los Cuatro Fantásticos: Primeros Pasos, ya dentro del MCU, en un mundo retro de los años sesenta: la Tierra ochocientos veintiocho.", "veinticinco", "ochocientos"),
        L(_lista(["PEDRO PASCAL", "VANESSA KIRBY", "JOSEPH QUINN", "EBON MOSS-BACHRACH"], "reed_legends", AZ4, "azul"), "Con Pedro Pascal, Vanessa Kirby, Joseph Quinn y Ebon Moss-Bachrach.", "pascal", "kirby"),
        L(e_fig("sue_mcu", "UN HOMENAJE", "azul"), "La dirigió Matt Shakman, el mismo de WandaVision. Y fíjate en la coincidencia: Sue la interpreta Vanessa Kirby, con el mismo apellido que el creador del equipo, Jack Kirby.", "shakman", "kirby"),
        L(e_fig("galactus_pie", "GALACTUS QUIERE A FRANKLIN", "thanos"), "Ahí enfrentaron a Galactus, con la voz de Ralph Ineson, que quería quedarse con el bebé de Sue: Franklin.", "galactus", "franklin"),
        L(e_fig("surfer_tabla", "SILVER SURFER · JULIA GARNER", "azul"), "Y esta vez Silver Surfer fue una mujer: Shalla-Bal, interpretada por Julia Garner.", "shalla-bal", "garner"),
        L(e_impacto("521\nMILLONES", ORO, "azul"), "Abrió con doscientos dieciocho millones en todo el mundo, y terminó con unos quinientos veintiún millones de dólares. Bien… pero menos de lo que Marvel esperaba.", "quinientos", "esperaba"),
    ]
    B["cap8"] = [
        L(e_capitulo(8, "RUMBO A DOOMSDAY", VERDE, "doom"), "Capítulo ocho. Rumbo a Doomsday.", "doomsday"),
        L(e_foto(3, chip_txt="CUATRO AÑOS DESPUÉS", mov=4, oscuro=.35), "En la escena a mitad de los créditos, pasan cuatro años. Sue le lee un cuento a Franklin…", "cuatro", "franklin"),
        L(e_revela("doom_pie4", "ALGUIEN LLEGA…", "DOCTOR DOOM"), "…y aparece Doctor Doom.", "doom"),
        L(e_dos("doom_magia", "franklin_pie", "¿POR QUÉ FRANKLIN?", "doom", chip_col=VERDE), "¿Por qué le interesa Franklin? Porque su poder puede alterar la realidad misma. Y eso es justo lo que Doom necesita.", "franklin", "realidad"),
        L(e_universos(("4 FANTÁSTICOS", "VENGADORES", "X-MEN"), ("reed_legends", "cap_sincasco", "wolverine_pie")), "Ahora, en Avengers Doomsday, la familia salta a la historia principal, junto a los Vengadores y los X-Men.", "familia", "x-men"),
        L(e_dos("reed_legends", "doom_pie3", "REED VS DOOM", "doom", vs=True), "Y por fin vamos a ver en el cine la rivalidad más antigua de Marvel: Reed Richards contra Doctor Doom.", "rivalidad", "doom"),
        L(e_dos("reed_pie", "xavier_silla", "OTRO REED", "mistico", chip_col=ORO), "Ojo, que no es la primera vez que vemos a un Reed en el MCU: John Krasinski fue el Reed de los Illuminati en Multiverso de la Locura. Te lo contamos en el capítulo tres.", "krasinski", "tres"),
        L(e_narrador(), "¿Qué quiere Doom con Franklin? ¿Y qué hará Reed para proteger a su hijo? El dieciocho de diciembre lo descubriremos.", "franklin", "dieciocho"),
    ]
    B["cierre"] = [
        L(e_narrador(), "¿Mi opinión? Los Cuatro Fantásticos son el corazón de Marvel. No son solo un equipo: son una familia que pelea, se perdona y siempre vuelve a estar junta.", "opinión", "familia"),
        L(e_dos("cosa_pie", "antorcha_vuelo", "¿TU FAVORITO?", "rojo", vs=True), "¿Cuál es tu favorito: Reed, Sue, Johnny o Ben? Te leo en los comentarios.", "favorito", "comentarios"),
        L(e_fig("cosa_mcu", "MI FAVORITO", "rojo"), "El mío es la Cosa. Un hombre convertido en monstruo, que aun así es el más humano de todos.", "cosa", "humano"),
        L(e_foto(3, chip_txt="UNA FAMILIA", mov=4), "Y lo que más me gusta de Primeros Pasos es que por fin entendió eso: que esta historia no es sobre poderes, es sobre una familia.", "familia"),
        L(e_estrellas_f("¿LA MEJOR FAMILIA DE MARVEL?", 5), "¿Mi nota? Cinco de cinco. Sin ellos no existiría nada de lo que vemos hoy.", "cinco"),
        L(e_grupo(["topo_moloides", "annihilus_alas", "franklin_pie"], "COMICS-STORE.COM.CO", "azul", ORO), "Y si quieres estas figuras, como el Hombre Topo, Annihilus o Franklin Richards, las encuentras en Comics Store: comics store punto com punto co.", "topo", "franklin"),
        L(e_continuara_f(), "En el próximo capítulo: los X-Men. Su historia y cronología, antes de Doomsday. Continuará…", "x-men", "continuará"),
        L(e_cta_f(), "Comenta FANTÁSTICOS si quieres el capítulo seis, suscríbete y activa la campanita. ¡Nos vemos en el próximo video!", "fantásticos"),
    ]
    return B

FOTO_AMB_F = {1: "explosion+viento", 2: "cosmos+trueno", 3: "noche", 4: "cosmos+explosion", 5: "maquina"}
FOTO_CLIMA_F = {1: "fuego", 2: None, 3: "noche", 4: "explosion", 5: None}
CLAVE_AMB_F = [("rayos", "trueno"), ("galactus", "cosmos+trueno"), ("annihilus", "maquina"), ("doom", "magia"), ("murió", "explosion"), ("topo", "viento")]

def preparar(esc):
    for fn, txt, _ in esc:
        low = txt.lower(); a = None
        if getattr(fn, "foto", None): a = FOTO_AMB_F.get(fn.foto); fn.clima = FOTO_CLIMA_F.get(fn.foto)
        else:
            a = next((v for k, v in CLAVE_AMB_F if k in low), None)
            if not a: a = {"impacto": "impacto+magia", "capitulo": "cosmos", "continuara": "cosmos+magia", "revela": "trueno+magia",
                           "estrellas": "magia"}.get(fn.__name__)
        if a: fn.amb = a
    return clima.envolver(esc)

def guion_yt():
    B = bloques(); esc = []
    for k in ("intro", "cap1", "cap2", "cap3", "cap4", "cap5", "cap6", "cap7", "cap8", "cierre"): esc += B[k]
    esc = preparar(esc)
    re_ = [i for i, e in enumerate(esc) if e[0].__name__ == "narrador" and i > 0]
    return esc, re_

def _short(gancho, tramo):
    gancho[0].amb = "impacto+magia"
    return [gancho] + tramo + [L(e_cta_f(youtube=True), "Comenta FANTÁSTICOS, y mira la historia completa en nuestro canal de YouTube.", "fantásticos", "youtube")]

def guion_short(n):
    esc, _ = guion_yt()
    if n == 1: return _short(L(e_impacto("LA FAMILIA QUE\nCREÓ MARVEL", AZ4, "azul", fig="cuatro_grupo"), "Sin esta familia, no existirían los Vengadores, ni Spider-Man, ni los X-Men.", "familia"),
                             _tramo(esc, "Los Cuatro Fantásticos aparecieron en noviembre", "Y ese primer número") + _tramo(esc, "Reed se volvió elástico", "Reed y Sue se casaron"))
    if n == 2: return _short(L(e_impacto("LA PELÍCULA QUE\nNUNCA VISTE", ROJO, "rojo"), "Existe una película de los Cuatro Fantásticos que nunca se estrenó.", "nunca"),
                             _tramo(esc, "La primera película se hizo", "Abrió con doscientos"))
    if n == 3: return _short(L(e_impacto("EL NIÑO MÁS\nPODEROSO", AZ4, "mistico", fig="franklin_pie"), "Este niño puede crear universos… y Doctor Doom lo sabe.", "universos"),
                             _tramo(esc, "Franklin Benjamin Richards", "El peor enemigo de la familia") + _tramo(esc, "En la escena a mitad", "¿Por qué le interesa Franklin?"))
    if n == 4: return _short(L(e_impacto("SUS VILLANOS", VERDE, "doom", fig="annihilus_alas"), "Los villanos de los Cuatro Fantásticos son de los mejores de Marvel.", "villanos"),
                             _tramo(esc, "El primero fue el Hombre Topo", "Annihilus apareció en el Anual"))

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
