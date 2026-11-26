"""Comics Store · Serie "Camino a Doomsday" Cap. 4 — Las incursiones: la destrucción del multiverso.
Uso: FORMATO=horizontal python3 t05_incursiones.py yt salida.mp4  |  python3 t05_incursiones.py s1..s4 salida.mp4
Imágenes en IMG_DIR: 01 dos Tierras chocando, 02 ciudad mirando otra Tierra, 03 biblioteca infinita, 04 templo del cisne negro, 05 Wakanda, 06 universo rompiéndose."""
import os, sys
os.environ.setdefault("SEMILLA", "incursiones")
os.environ.setdefault("IMG_DIR", "/home/claude/incursiones/img")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import clima
from t03_asi_nacio_doom import *
from t03_asi_nacio_doom import PRON as PRON3, _tramo, _lista, L
from t02_si_dejaste_marvel import e_incursion
from t01_strange_doom import e_battleworld
from t04_illuminati import e_memoria
from motor import render

PRON = dict(PRON3); PRON.update({"illuminati": ("es", "iluminati"), "skrull": ("es", "escrul"), "rabum": ("es", "rábum"), "alal": ("es", "alál"),
    "black": ("es", "blac"), "swan": ("es", "suán"), "swans": ("es", "suáns"), "bolt": ("es", "bolt"), "panther": ("es", "pánter"), "new": ("es", "niu"),
    "hickman": ("es", "jícman"), "jonathan": ("es", "yónatan"), "beyonders": ("es", "biyónders"), "beyonder": ("es", "biyónder"),
    "proxima": ("es", "próxima"), "midnight": ("es", "mídnait"), "corvus": ("es", "córvus"), "glaive": ("es", "gleiv"), "terrax": ("es", "térrax"),
    "maximus": ("es", "máximus"), "ultimate": ("es", "últimeit"), "time": ("es", "taim"), "runs": ("es", "rans"), "out": ("es", "aut"),
    "darkhold": ("es", "dárjold"), "clea": ("es", "clía"),
    "namor": ("es", "námor"), "wakanda": ("es", "uakánda"), "kang": ("es", "cang"), "invasion": ("es", "inveishon"), "owen": ("es", "ouen"), "reece": ("es", "ris"), "yabbat": ("es", "yábat"), "ummon": ("es", "úmon"), "tarru": ("es", "tárru"), "thane": ("es", "zein"), "infinity": ("es", "infíniti"), "dynasty": ("es", "dáinasti"), "comic-con": ("es", "cómic con"), "shuri": ("es", "shúri"), "t'challa": ("es", "chála"), "latveria": ("es", "latvéria"), "marfil": ("es", "marfíl")})
ROJ = (255, 60, 70)
COLORES = (ROJ, (120, 180, 255))

# ---------------------------------------------------------------- escenas propias
def e_reloj(chip_txt="8 HORAS", desde=8 * 3600):
    """Cuenta regresiva de 8 horas que corre rápido."""
    def f(t, d):
        c = cosmos(t, "rojo", velocidad=1.5)
        planeta(c, P(W * .22, W * .2), P(560, 260), P(150, 130), t, AZUL, .8); planeta(c, P(W * .78, W * .8), P(560, 260), P(150, 130), t + 2, ROJO, .8)
        s = max(0, int(desde - t * 1777)); hh, mm, ss = s // 3600, (s // 60) % 60, s % 60
        glow(c, W / 2, P(1000, 560), P(520, 520), ROJ, 70 + int(40 * (math.sin(t * 7) > 0)))
        texto(c, f"{hh:02d}:{mm:02d}:{ss:02d}", W / 2, P(1000, 560), P(170, 190), (255, 255, 255), glow_col=ROJ, stroke=8)
        chip(c, chip_txt, W / 2, P(1300, 800), ROJ, P(46, 44), eo(pr(t, .3, .3)))
        return shake(c, (t % 1.0), 6, .15)
    return S("reloj", f)

def e_dilema():
    """Dos Tierras: la tuya o la otra."""
    def f(t, d):
        c = cosmos(t, "rojo"); r = P(260, 210)
        x1, x2 = P(W * .26, W * .27), P(W * .74, W * .73); y = P(980, 520)
        planeta(c, x1, y, r, t, AZUL); planeta(c, x2, y, r, t * 1.2 + 3, ROJO)
        chip(c, "TU MUNDO", x1, y + r + P(80, 70), AZUL, P(40, 38), eo(pr(t, .4, .3)))
        chip(c, "EL OTRO", x2, y + r + P(80, 70), ROJ, P(40, 38), eo(pr(t, .7, .3)))
        texto(c, "¿CUÁL DESTRUYES?", W / 2, P(560, 170), P(80, 74), (255, 255, 255), alpha=eo(pr(t, 1.0, .4)), glow_col=ROJ)
        return zoom(c, t, d, 1.0, 1.05)
    return S("dilema", f)

def e_revela(fig="doom_magia", chip_txt="RABUM ALAL ES…", nombre="DOCTOR DOOM", col=VERDE, t0=1.6):
    """Silueta misteriosa que se revela con un destello."""
    def f(t, d):
        c = cosmos(t, "doom"); k = eo(pr(t, t0, .25))
        if t < t0:
            figura(c, fig, W / 2, PISO, FH, t, "pop", alpha=.25)
            c.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 110)))
        else:
            mandala(c, W / 2, P(950, 520), P(430, 360), t, col, .45); figura(c, fig, W / 2, PISO, FH, 2.0, "pop"); particulas(c, t, col, n=35)
            texto(c, nombre, W / 2, P(560, 160), P(110, 100), (255, 255, 255), alpha=k, glow_col=col, stroke=8)
            flash(c, t - t0, .35, col, 230)
        chip(c, chip_txt, W / 2, P(1840, 1010), col, P(46, 44), eo(pr(t, .3, .3)))
        c = zoom(c, t, d, 1.0, 1.08)
        return shake(c, t - t0, 18, .5) if t > t0 else c
    return S("revela", f)

def e_moleculas(n=5, chip_txt="UN HOMBRE MOLÉCULA EN CADA UNIVERSO"):
    """Varios universos, cada uno con su Hombre Molécula: la bomba."""
    def f(t, d):
        c = cosmos(t, "mistico"); col = color_de("molecula")
        for i in range(n):
            x = W * (.12 + .76 * i / (n - 1)); y = P(1150 + (i % 2) * 160, 620 + (i % 2) * 60)
            u = pr(t, .2 + i * .18, .4)
            if u <= 0: continue
            glow(c, x, y - P(200, 160), P(260, 200), col, int(80 * eo(u)))
            figura(c, "molecula_pie", x, y, P(520, 380), t, "sube", retraso=.2 + i * .18, reflejo=False)
        chip(c, chip_txt, W / 2, P(1840, 1010), col, P(38, 38), eo(pr(t, 1.0, .3)))
        return zoom(c, t, d, 1.0, 1.05)
    return S("moleculas", f)

def e_trio_m(chip_txt="DOOM · STRANGE · HOMBRE MOLÉCULA"):
    def f(t, d):
        c = cosmos(t, "mistico"); glow(c, W / 2, P(700, 260), P(300, 260), (255, 255, 255), 90)
        figs = ["doom_brazos", "molecula_pie", "strange_portal"]; mw = P(W * .34, W * .3)
        hc = min(h_fit(fg, FH * .82, mw) for fg in figs)
        for i, fg in enumerate(figs):
            figura(c, fg, W * (.2 + .3 * i) if HZ else W * (.18 + .32 * i), PISO, hc, t, "sube", retraso=i * .15)
        chip(c, chip_txt, W / 2, P(560, 1010), MORADO, P(36, 38), eo(pr(t, .5, .3)))
        return zoom(c, t, d, 1.0, 1.06)
    return S("trio", f)

def e_estrellas_c(titulo, nota=5):
    def f(t, d):
        c = cosmos(t, "rojo"); figura(c, "molecula_pie", P(W / 2, W * .85), PISO, P(560, 520), t, "der", alpha=P(.35, 1), reflejo=False)
        texto(c, titulo, P(W / 2, W * .42), P(620, 300), P(64, 66), (255, 255, 255), glow_col=ROJ)
        estrellas(c, t, nota, P(W / 2, W * .42), P(900, 520)); texto(c, f"{nota} / 5", P(W / 2, W * .42), P(1120, 700), P(90, 84), ORO, alpha=eo(pr(t, 1.5, .3)), glow_col=ORO)
        return zoom(c, t, d, 1.0, 1.05)
    return S("estrellas", f)

def e_continuara_c():
    def f(t, d):
        c = cosmos(t, "azul", velocidad=.5); figura(c, "reed_legends", W / 2, PISO, FH * .9, t, "pop", alpha=.6)
        c.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 90)))
        texto(c, "CONTINUARÁ…", W / 2, P(860, 470), P(130, 140), (255, 255, 255), alpha=eo(pr(t, .5, .6)), glow_col=(60, 210, 255), stroke=8)
        chip(c, "CAP. 5 · LOS 4 FANTÁSTICOS", W / 2, P(1100, 650), ORO, P(40, 40), eo(pr(t, 1.2, .4)))
        return c
    return S("continuara", f)

def e_cta_c(youtube=False):
    def f(t, d):
        c = cosmos(t, "rojo")
        figura(c, "molecula_pie", P(W / 2, W * .24), P(1180, 880), P(760, 700), t, "pop", reflejo=False)
        caja_comentario(c, t, "INCURSIÓN", x=P(W / 2, W * .68), y=P(1320, 400), col=ROJ)
        if youtube: chip(c, "HISTORIA COMPLETA EN YOUTUBE", W / 2, P(1560, 900), ROJO, P(40, 38), eo(pr(t, 1.6, .3)), (40, 6, 10))
        barra_suscribir(c, t, x=P(W / 2, W * .68), y=P(1740, 600), inicio=2.0 if youtube else 1.4)
        return c
    return S("cta", f)

# ---------------------------------------------------------------- guion completo
def bloques():
    B = {}
    B["intro"] = [
        L(e_narrador(), INTRO_GAMER[0], *INTRO_GAMER[1]),
        L(e_foto(2, chip_txt="OTRA TIERRA EN EL CIELO", mov=1), "Imagina que miras al cielo… y ves otra Tierra. Igual a la tuya. Acercándose.", "cielo", "tierra"),
        L(e_impacto("TIENES\n8 HORAS", ROJ, "rojo"), "Tienes ocho horas. Si no destruyes ese planeta… los dos universos desaparecen.", "ocho", "desaparecen"),
        L(e_grupo(["molecula_pie", "doom_brazos", "namor_vortice"], "CAMINO A DOOMSDAY · CAP. 4", "rojo", ROJ), "Bienvenido al capítulo cuatro de Camino a Doomsday: las incursiones, la destrucción del multiverso.", "incursiones", "multiverso"),
        L(e_dos("molecula_pie", "panther_lanza", "FIGURAS DE COMICS STORE", "mistico", chip_col=ORO), "Y como siempre, todas las figuras que vas a ver son de nuestra tienda, Comics Store.", "figuras", "comics", "store"),
        L(e_narrador(), "Quédate hasta el final, porque detrás de todo esto había alguien… y es un villano que ya conoces muy bien.", "final", "villano"),
    ]
    B["cap1"] = [
        L(e_capitulo(1, "¿QUÉ ES UNA INCURSIÓN?", ROJ, "rojo"), "Capítulo uno. ¿Qué es una incursión?", "incursión"),
        L(e_incursion("DOS UNIVERSOS CHOCAN"), "Una incursión es el choque de dos universos. Y el punto exacto donde se tocan… es siempre la Tierra.", "choque", "tierra"),
        L(e_universos(("UNIVERSO A", "PUNTO DE CHOQUE", "UNIVERSO B"), ("iron_mk42", "molecula_pie", "doom_brazos")), "No es que choquen en el espacio como dos asteroides. Son dos realidades distintas que intentan ocupar el mismo lugar.", "realidades", "lugar"),
        L(e_foto(1, chip_txt="LA INCURSIÓN", mov=1, sacude=True), "Las dos Tierras aparecen una frente a la otra. Y empieza la cuenta regresiva.", "regresiva"),
        L(e_reloj(), "Después de ocho horas, las dos Tierras chocan y se destruyen. Y detrás de ellas, sus universos completos también colapsan.", "ocho", "colapsan"),
        L(e_dilema(), "Solo hay una forma de salvar los dos universos: que una de las Tierras sea destruida antes de tiempo.", "una", "destruida"),
        L(e_foto(2, chip_txt="UNA Y OTRA VEZ", mov=4, oscuro=.3), "Y eso no es lo peor. Lo peor es que no pasó una sola vez: las incursiones empezaron a repetirse una y otra vez.", "peor", "otra"),
        L(e_narrador(), "Piénsalo bien: para salvar tu mundo, tienes que destruir otro planeta con miles de millones de personas inocentes. ¿Tú qué harías?", "inocentes", "harías"),
        L(e_comic("2012", "#1", fig="iron_mk42", titulo="AVENGERS"), "Esta historia la escribió Jonathan Hickman. Empezó en dos mil doce con la serie Avengers…", "hickman", "doce"),
        L(e_comic("2013", "#1", fig="panther_pie", titulo="NEW AVENGERS"), "…y siguió en dos mil trece con New Avengers, donde los Illuminati vuelven a reunirse.", "trece", "illuminati"),
    ]
    B["cap2"] = [
        L(e_capitulo(2, "EL CISNE NEGRO", (200, 60, 60), "rojo"), "Capítulo dos. El Cisne Negro.", "cisne", "negro"),
        L(e_foto(5, chip_txt="WAKANDA", mov=1), "Todo empezó en Wakanda. Black Panther vio algo imposible en el cielo de su país.", "wakanda", "imposible"),
        L(e_foto(2, chip_txt="UNA TIERRA EN EL CIELO", mov=3, oscuro=.3), "Otra Tierra, a punto de chocar con la nuestra.", "chocar"),
        L(e_foto(4, chip_txt="BLACK SWAN", mov=1), "Y de ella bajó una mujer misteriosa con un grupo de aliados: la Black Swan. Activaron un aparato… y destruyeron ese planeta por completo.", "black", "swan", "destruyeron"),
        L(e_fig("panther_lanza", "LA CAPTURAN", "mistico"), "Black Panther la capturó y la encerró en la Necrópolis de Wakanda.", "necrópolis"),
        L(e_fig("reed_pie2", "EL INTERROGATORIO", "azul"), "Reed Richards la interrogó dentro de un cubo transparente, sin cama y sin asiento. Y lo que ella contó era aterrador.", "cubo", "aterrador"),
        L(e_foto(4, chip_txt="EL CULTO DE RABUM ALAL", mov=3, oscuro=.3), "Ella venía de otro universo que ya había muerto. Y servía a un culto que adoraba a alguien llamado Rabum Alal.", "rabum", "alal"),
        L(e_impacto("RABUM ALAL\nEL GRAN DESTRUCTOR", ROJ, "rojo"), "Rabum Alal. El Gran Destructor.", "destructor"),
        L(e_foto(4, chip_txt="VE EL FUTURO", mov=2, oscuro=.35), "Pero Black Swan tenía un poder muy útil: podía predecir dónde iba a ocurrir la siguiente incursión.", "predecir"),
        L(e_doom("doom_brazos", "LATVERIA", "sube"), "Y la siguiente iba a ser en Latveria… el país de Doctor Doom. Los Illuminati tuvieron que meterse en su territorio.", "latveria", "doom"),
        L(e_narrador(), "Guarda ese nombre, porque al final de este video vas a saber quién es. Y te aseguro que no te lo esperas.", "nombre"),
    ]
    B["cap3"] = [
        L(e_capitulo(3, "EL DILEMA", (170, 90, 255), "mistico"), "Capítulo tres. El dilema.", "dilema"),
        L(e_grupo(["panther_pie", "reed_legends", "iron_mk42", "strange_magia"], "LOS ILLUMINATI", "mistico", (170, 90, 255)), "Los Illuminati se volvieron a reunir para enfrentar las incursiones en secreto.", "secreto"),
        L(e_memoria(), "Y como viste en el capítulo anterior, cuando el Capitán América se opuso… Strange le borró la memoria.", "memoria"),
        L(e_foto(3, chip_txt="BUSCANDO RESPUESTAS", mov=1), "Buscaron soluciones por todos lados. En la ciencia, en la magia, en otros mundos.", "soluciones"),
        L(e_fig("iron_rayos", "BOMBAS DE ANTIMATERIA", "rojo", sacude=True), "Al final construyeron armas capaces de destruir un planeta entero. Pero había un problema…", "armas", "problema"),
        L(e_fig("panther_lanza", "NO PUEDO HACERLO", "mistico"), "Cuando llegó el momento de usarlas, ninguno se atrevió. Black Panther fue el primero en advertir: matar a otros héroes era una línea que no se podía cruzar.", "línea"),
        L(e_fig("namor_tridente", "NAMOR SÍ LO HIZO", "rojo", sacude=True), "Todos dudaron. Todos… menos Namor.", "namor"),
        L(e_foto(1, chip_txt="UN MUNDO DESTRUIDO", mov=4, sacude=True), "Namor activó la bomba y destruyó la otra Tierra. Salvó nuestro universo… pero mató a un planeta entero.", "destruyó", "planeta"),
        L(e_dos("panther_lanza", "namor_vortice", "PANTHER VS NAMOR", "rojo", vs=True), "Y Black Panther, que ya odiaba a Namor por la guerra entre Wakanda y Atlantis, lo atacó.", "atacó", "atlantis"),
        L(e_foto(5, chip_txt="PANTHER DESTERRADO", mov=4, oscuro=.4), "Esa guerra le costó caro: su hermana Shuri llegó a creer que T'Challa conspiraba con Namor, y lo desterró a la Necrópolis.", "shuri", "necrópolis"),
        L(e_narrador(), "Héroes contra héroes, mientras el multiverso se moría. Y lo peor apenas empezaba.", "peor"),
    ]
    B["cap4"] = [
        L(e_capitulo(4, "LA CÁBALA", (255, 140, 40), "rojo"), "Capítulo cuatro. La Cábala.", "cábala"),
        L(e_fig("namor_vortice", "NAMOR SE VA", "azul"), "Cuando los Illuminati decidieron rendirse, Namor no aceptó. Si los héroes no querían ensuciarse las manos… él buscaría a otros.", "manos", "otros"),
        L(e_dos("namor_tridente", "thanos_frente", "LA CÁBALA", "thanos", chip_col=(255, 140, 40)), "Formó la Cábala. Y el primero en unirse fue nada menos que Thanos.", "cábala", "thanos"),
        L(_lista(["THANOS", "PROXIMA MIDNIGHT", "CORVUS GLAIVE", "TERRAX", "MAXIMUS", "BLACK SWAN"], "namor_vortice", (255, 140, 40), "thanos"),
          "Con él llegaron Proxima Midnight y Corvus Glaive, de la Orden Negra; Terrax; Máximus, el Inhumano loco; y la propia Black Swan.", "proxima", "corvus"),
        L(e_foto(6, chip_txt="TIERRA-9004", mov=1, sacude=True), "Su primera víctima fue la Tierra nueve mil cuatro. Y después vinieron muchas más.", "primera", "víctima"),
        L(e_impacto("SIN\nESCONDERSE", (255, 140, 40), "rojo", fig="thanos_frente"), "Y a diferencia de los Illuminati, la Cábala no se escondía: lo hacían a la vista de todo el mundo, como si fueran los salvadores de la Tierra.", "vista", "salvadores"),
        L(e_fig("thanos_guante", "DISFRUTABAN DESTRUIR", "thanos"), "La diferencia es que los Illuminati querían destruir mundos sin dolor. La Cábala acababa con sus héroes y sus habitantes antes de volarlos.", "diferencia", "habitantes"),
        L(e_fig("namor_tridente", "EL ARREPENTIMIENTO", "azul"), "Con el tiempo, hasta Namor sintió asco de lo que hacían sus aliados. Pero ya era demasiado tarde.", "asco", "tarde"),
        L(e_doom("doom_metal", "DOOM LOS OBSERVA", "sube"), "Incluso Doctor Doom, que tampoco era un santo, despreciaba trabajar con ellos. Para él, la Cábala solo disfrutaba destruir.", "despreciaba"),
        L(e_narrador(), "Ahora viene lo más loco. Porque los Illuminati no sabían que alguien más estaba trabajando en secreto… para salvarlo todo.", "secreto"),
    ]
    B["cap5"] = [
        L(e_capitulo(5, "SE ACABA EL TIEMPO", ROJ, "rojo"), "Capítulo cinco. Se acaba el tiempo.", "tiempo"),
        L(e_reloj("OCHO MESES DESPUÉS", desde=8 * 3600 - 60), "A finales de dos mil catorce, Hickman saltó la historia ocho meses hacia el futuro, en la saga Time Runs Out.", "ocho", "meses"),
        L(e_comic("2014", "#35", fig="cap_sincasco", titulo="TIME RUNS OUT"), "Esa saga se contó en Avengers, del número treinta y cinco al cuarenta y cuatro, y en New Avengers, del veinticuatro al treinta y tres.", "treinta", "cuatro"),
        L(e_grupo(["cap_sincasco", "iron_tony", "namor_tridente"], "LOS HÉROES DIVIDIDOS", "rojo", ROJ), "Para entonces, todo se había roto. Los Vengadores estaban divididos en tres bandos. El Capitán ya había recordado todo… y quería que Tony pagara.", "divididos", "recordado"),
        L(e_dos("cap_sincasco", "iron_tony", "CAPITÁN VS IRON MAN", "rojo", vs=True), "Amigos que se enfrentaban mientras el multiverso se moría.", "multiverso"),
        L(e_foto(6, chip_txt="EL MULTIVERSO MUERE", mov=3), "Y las incursiones seguían. Cada vez más rápido. Cada vez más universos desaparecían.", "rápido"),
        L(e_fig("strange_portal", "STRANGE SIGUE LA PISTA", "mistico", efecto="hilos"), "Doctor Strange decidió seguir la pista de las Black Swans hasta el final. Quería saber, de una vez, quién era Rabum Alal.", "strange", "rabum"),
    ]
    B["cap6"] = [
        L(e_capitulo(6, "EL GRAN DESTRUCTOR", VERDE, "doom"), "Capítulo seis. El Gran Destructor.", "destructor"),
        L(e_foto(4, chip_txt="CAPTURADO", mov=4, oscuro=.4), "Las Black Swans lo atraparon. Su líder, Rabum Alal, lo quería vivo.", "vivo"),
        L(e_revela("doom_magia", "RABUM ALAL ES…", "DOCTOR DOOM"), "Y entonces, en New Avengers número treinta y uno, por fin vimos su rostro. Rabum Alal era… Doctor Doom.", "treinta", "doom"),
        L(e_doom("doom_libro", "LO SABÍA TODO", "sube"), "Doom había viajado al origen de todo. Llevaba años, quizás siglos, luchando contra las incursiones a su manera.", "origen", "manera"),
        L(e_narrador(), "Y fíjate en la ironía: el Gran Destructor, al que todos temían, era el único que estaba peleando contra los verdaderos culpables.", "ironía", "culpables"),
        L(e_foto(3, chip_txt="LOS BEYONDERS", mov=2, oscuro=.3), "Y descubrió la verdad: los culpables eran los Beyonders, unos seres todopoderosos que estaban destruyendo el multiverso.", "beyonders", "todopoderosos"),
        L(e_impacto("LOS REYES\nDE MARFIL", (240, 230, 210), "mistico"), "Los mismos misteriosos Reyes de Marfil de los que hablaban las Black Swans. Siempre fueron los Beyonders.", "marfil"),
        L(e_fig("molecula_pie", "EL HOMBRE MOLÉCULA", "mistico"), "¿Y cómo lo hacían? Con el Hombre Molécula. Un personaje que muchos veían como un villano de segunda… y que terminó siendo la pieza más importante del multiverso.", "molécula", "importante"),
        L(e_moleculas(), "Cada universo tiene su propio Hombre Molécula, y todos son pedazos de un mismo ser. Los Beyonders los hacían estallar como bombas… y así acababan con cada realidad.", "pedazos", "bombas"),
        L(e_trio_m(), "Doom, Strange y el Hombre Molécula de nuestro universo hicieron lo impensable: reunieron a los Hombres Molécula de todo el multiverso…", "impensable", "multiverso"),
        L(e_impacto("UNA BOMBA\nCONTRA DIOSES", (220, 60, 230), "mistico", fig="molecula_pie"), "…y los usaron como una gran bomba contra los Beyonders. Y los mataron.", "bomba", "mataron"),
        L(e_incursion("616 VS 1610"), "Pero ya era tarde. Llegó la última incursión: nuestro universo contra el Universo Ultimate. Los dos se destruyeron.", "última", "ultimate"),
        L(e_dos("reed_legends", "thanos_frente", "DOS BALSAS", "azul", chip_col=ORO), "Solo sobrevivieron dos balsas: una con Reed Richards y un grupo de héroes… y otra con la Cábala, Thanos incluido.", "balsas", "cábala"),
        L(e_battleworld(chip_txt="BATTLEWORLD"), "El Hombre Molécula le pasó a Doom el poder de los Beyonders. Y con los pedazos que sobrevivieron, Doom creó un nuevo planeta: Battleworld.", "poder", "battleworld"),
        L(e_comic("2015", "#1", fig="doom_trono", titulo="SECRET WARS"), "Así empezó Secret Wars, que salió el seis de mayo de dos mil quince. Pero esa historia es el capítulo ocho.", "mayo", "ocho"),
    ]
    B["extra"] = [
        L(e_capitulo(7, "LO QUE NO TE CONTARON", (220, 60, 230), "mistico"), "Capítulo siete. Lo que no te contaron.", "contaron"),
        L(e_comic("1963", "#20", fig="molecula_pie", titulo="FANTASTIC FOUR"), "El Hombre Molécula no es nuevo: apareció por primera vez en Los Cuatro Fantásticos número veinte, en mil novecientos sesenta y tres. Su nombre real es Owen Reece.", "veinte", "reece"),
        L(e_foto(4, chip_txt="YABBAT UMMON TARRU", mov=4), "Black Swan también tiene nombre: Yabbat Ummon Tarru. Y era la última sobreviviente de su gente.", "nombre", "sobreviviente"),
        L(e_fig("thanos_guante", "INFINITY · 2013", "thanos"), "En medio de las incursiones, Thanos invadió la Tierra buscando a su hijo perdido, Thane. Esa saga se llamó Infinity.", "thanos", "infinity"),
        L(e_grupo(["reed_pie2", "panther_pie", "blackbolt_pie"], "LOS CONSTRUCTORES", "azul", ORO), "Y los Illuminati también se enfrentaron a los Constructores, una raza alienígena antiquísima con planes para la Tierra.", "constructores"),
        L(e_narrador(), "Todas estas historias corrían al mismo tiempo. Y todas terminaban en el mismo lugar: Secret Wars.", "secret", "wars"),
    ]
    B["cap7"] = [
        L(e_capitulo(8, "LAS INCURSIONES EN EL MCU", ORO, "mistico"), "Capítulo ocho. Las incursiones en el MCU.", "mcu"),
        L(e_fig("strange_portal", "MULTIVERSO DE LA LOCURA", "mistico"), "En el cine la palabra apareció en Doctor Strange en el Multiverso de la Locura, de dos mil veintidós.", "veintidós"),
        L(e_dos("reed_pie", "xavier_silla", "LA EXPLICACIÓN", "mistico", chip_col=ORO), "Ahí, el Reed Richards de la Tierra ochocientos treinta y ocho le explicó a Strange qué es una incursión: dos universos que chocan.", "explicó", "chocan"),
        L(e_fig("strange_magia", "EL STRANGE CULPABLE", "rojo"), "Y le contó que el Strange de su mundo causó una, usando el Darkhold. Por eso lo ejecutaron.", "darkhold", "ejecutaron"),
        L(e_foto(6, chip_txt="UN MUNDO DESTRUIDO", mov=1), "Incluso vimos un universo en pleno choque, un mundo que ya estaba siendo destruido por una incursión.", "choque"),
        L(e_foto(1, chip_txt="CLEA LO ADVIERTE", mov=2), "Y al final de la película, Clea le dice a nuestro Strange que él también causó una incursión.", "clea", "incursión"),
        L(e_comic("2024", "SDCC", fig="doom_brazos", titulo="COMIC-CON"), "Al principio, Marvel tenía planeada una película llamada The Kang Dynasty. Pero el plan cambió, y en la Comic-Con de dos mil veinticuatro anunciaron Avengers Doomsday.", "kang", "comic-con"),
        L(e_doom("doom_pie4", "AVENGERS: DOOMSDAY", "sube"), "Ahora llega Avengers Doomsday, con Robert Downey Junior como Doctor Doom, y los Vengadores, los Cuatro Fantásticos y los X-Men de Fox en la misma historia.", "downey", "doom"),
        L(e_universos(("VENGADORES", "4 FANTÁSTICOS", "X-MEN"), ("cap_sincasco", "reed_legends", "wolverine_pie")), "Tres universos distintos, juntos. Y en los cómics… eso siempre termina en incursiones.", "tres", "incursiones"),
        L(e_narrador(), "Muchos fans creen que la película seguirá este camino hacia Secret Wars. Lo sabremos el dieciocho de diciembre.", "fans", "dieciocho"),
    ]
    B["cierre"] = [
        L(e_narrador(), "¿Mi opinión? Las incursiones son de las mejores historias que ha hecho Marvel, porque convierten a los héroes en algo que nunca habíamos visto: personas desesperadas.", "opinión", "desesperadas"),
        L(e_dilema(), "No hay un villano al que golpear. Solo una pregunta imposible: ¿destruirías otro mundo para salvar el tuyo?", "imposible"),
        L(e_grupo(["namor_vortice", "doom_magia", "reed_legends"], "TODOS FALLARON", "rojo", ROJ), "Y lo mejor es cómo todo encaja: los Illuminati, la Cábala, Doom… todos tratando de salvar el multiverso a su manera. Y casi todos fallando.", "encaja", "fallando"),
        L(e_doom("doom_trono2", "¿LLEGARÁ AL CINE?", "sube"), "Por eso tantos fans quieren ver esto en el cine. Porque si Doomsday toma aunque sea una parte de esta historia, va a ser enorme.", "enorme"),
        L(e_dos("namor_tridente", "panther_lanza", "¿NAMOR O PANTHER?", "rojo", vs=True), "Namor dijo que sí, y lo perdió todo. Black Panther dijo que no, y casi pierde su mundo. ¿Y tú? ¿Con quién estás? Te leo en los comentarios.", "comentarios"),
        L(e_estrellas_c("¿LA MEJOR SAGA DE MARVEL?", 5), "¿Mi nota? Cinco de cinco. Una de las mejores sagas de la historia del cómic.", "cinco"),
        L(e_grupo(["molecula_pie", "namor_vortice", "panther_lanza"], "COMICS-STORE.COM.CO", "mistico", ORO), "Y si quieres estas figuras, como el Hombre Molécula, las encuentras en Comics Store: comics store punto com punto co.", "molécula"),
        L(e_continuara_c(), "En el próximo capítulo: los Cuatro Fantásticos. La familia que creó el Universo Marvel. Continuará…", "fantásticos", "continuará"),
        L(e_cta_c(), "Y si te perdiste el capítulo anterior, los Illuminati, lo encuentras en nuestro canal. Comenta INCURSIÓN si quieres el capítulo cinco, suscríbete y activa la campanita. ¡Nos vemos en el próximo video!", "incursión"),
    ]
    return B

FOTO_AMB_C = {1: "explosion+trueno", 2: "noche+viento", 3: "magia+campanas", 4: "antorchas+magia", 5: "noche", 6: "cosmos+explosion"}
FOTO_CLIMA_C = {1: "explosion", 2: "noche", 3: "velas", 4: "antorchas", 5: "noche", 6: "explosion"}
CLAVE_AMB_C = [("bomba", "explosion"), ("ocho horas", "maquina"), ("destruy", "explosion"), ("thanos", "trueno"), ("doom", "magia"), ("beyonders", "cosmos")]

def preparar(esc):
    for fn, txt, _ in esc:
        low = txt.lower(); a = None
        if getattr(fn, "foto", None): a = FOTO_AMB_C.get(fn.foto); fn.clima = FOTO_CLIMA_C.get(fn.foto)
        else:
            a = next((v for k, v in CLAVE_AMB_C if k in low), None)
            if not a: a = {"impacto": "impacto+magia", "capitulo": "cosmos", "continuara": "cosmos+magia", "reloj": "maquina", "incursion": "explosion+cosmos",
                           "revela": "trueno+magia", "moleculas": "magia", "dilema": "cosmos", "estrellas": "magia", "battleworld": "cosmos"}.get(fn.__name__)
        if a: fn.amb = a
    return clima.envolver(esc)

def guion_yt():
    B = bloques(); esc = []
    for k in ("intro", "cap1", "cap2", "cap3", "cap4", "cap5", "cap6", "extra", "cap7", "cierre"): esc += B[k]
    esc = preparar(esc)
    re_ = [i for i, e in enumerate(esc) if e[0].__name__ == "narrador" and i > 0]
    return esc, re_

def _short(gancho, tramo):
    gancho[0].amb = "impacto+magia"
    return [gancho] + tramo + [L(e_cta_c(youtube=True), "Comenta INCURSIÓN, y mira la historia completa en nuestro canal de YouTube.", "incursión", "youtube")]

def guion_short(n):
    esc, _ = guion_yt()
    if n == 1: return _short(L(e_impacto("8 HORAS PARA\nDESTRUIR UN MUNDO", ROJ, "rojo"), "Tienes ocho horas para destruir otra Tierra… o mueren dos universos.", "ocho"),
                             _tramo(esc, "Una incursión es el choque", "Esta historia la escribió") + _tramo(esc, "Todos dudaron. Todos", "Y Black Panther, que ya odiaba"))
    if n == 2: return _short(L(e_impacto("EL VILLANO\nDETRÁS DE TODO", VERDE, "doom", fig="doom_magia"), "El villano que estaba detrás de la destrucción del multiverso… era alguien que conoces.", "villano"),
                             _tramo(esc, "Ella venía de otro universo", "Rabum Alal. El Gran") + _tramo(esc, "Las Black Swans lo atraparon", "Doom había viajado") + _tramo(esc, "Y descubrió la verdad", "…y los usaron como"))
    if n == 3: return _short(L(e_impacto("NAMOR DESTRUYÓ\nUN PLANETA", (40, 230, 190), "azul", fig="namor_tridente"), "Namor hizo lo que ningún héroe se atrevía: destruir un planeta entero.", "planeta"),
                             _tramo(esc, "Todos dudaron. Todos", "Y Black Panther, que ya odiaba") + _tramo(esc, "Cuando los Illuminati decidieron rendirse", "Y a diferencia de los Illuminati"))
    if n == 4: return _short(L(e_impacto("ESTO PUEDE PASAR\nEN DOOMSDAY", ORO, "doom", fig="doom_pie4"), "Esto que pasó en los cómics… podría llegar a Avengers Doomsday.", "doomsday"),
                             _tramo(esc, "Una incursión es el choque", "Después de ocho horas") + _tramo(esc, "Ahí, el Reed Richards", "Muchos fans creen"))

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
