"""Comics Store · Serie "Camino a Doomsday" Cap. 3 — Los Illuminati: la sociedad secreta de Marvel.
Uso: FORMATO=horizontal python3 t04_illuminati.py yt salida.mp4
     python3 t04_illuminati.py s1|s2|s3|s4 salida.mp4      (shorts verticales)
Imágenes HD de Fernando en IMG_DIR: 01 sala secreta, 02 planeta Skrull, 03 bóveda de gemas, 04 cápsula espacial, 05 ciudad en ruinas."""
import os, sys
os.environ.setdefault("SEMILLA", "illuminati")
os.environ.setdefault("IMG_DIR", "/home/claude/illuminati/img")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import clima
from t03_asi_nacio_doom import *          # e_foto, e_fig, e_dos, e_grupo, e_impacto, e_capitulo, e_comic, e_narrador, _lista, ...
from t03_asi_nacio_doom import PRON as PRON3
from t02_si_dejaste_marvel import e_incursion
from t03_asi_nacio_doom import _tramo, _lista, L
from motor import render

PRON = dict(PRON3); PRON.update({"illuminati": ("es", "iluminati"), "skrull": ("es", "escrul"), "skrulls": ("es", "escruls"), "kree": ("es", "cri"),
    "bolt": ("es", "bolt"), "new": ("es", "niu"), "brian": ("es", "bráian"), "michael": ("es", "máikol"), "bendis": ("es", "béndis"),
    "uatu": ("es", "uátu"), "hood": ("es", "jud"), "world": ("es", "uorld"), "war": ("es", "uor"), "civil": ("es", "sívil"),
    "manhattan": ("es", "manjátan"), "vegas": ("es", "végas"), "elektra": ("es", "eléctra"), "original": ("es", "oriyinal"), "sin": ("es", "sin"),
    "mordo": ("es", "mórdo"), "carter": ("es", "cárter"), "rambeau": ("es", "rambó"), "krasinski": ("es", "crasínski"), "john": ("es", "yon"),
    "darkhold": ("es", "dárjold"), "ragnarok": ("es", "ráñarok"), "dorrek": ("es", "dórec"), "medusa": ("es", "medúsa"), "hayley": ("es", "jéili"), "atwell": ("es", "átuel"), "mount": ("es", "maunt"), "anson": ("es", "ánson"), "sakaar": ("es", "sacár"), "banner": ("es", "báner"), "madison": ("es", "mádison"), "square": ("es", "escuer"), "garden": ("es", "gárden"), "beyonder": ("es", "biyónder"), "invasion": ("es", "inveishon"), "atlántida": ("es", "atlántida"), "inhumanos": ("es", "inhumanos")})
AZ = (120, 170, 255)
COLORES = (AZ, ORO)

# ---------------------------------------------------------------- escenas propias de este capítulo
def e_voz():
    """Black Bolt: un susurro que derrumba una ciudad (ondas que salen de su boca)."""
    def f(t, d):
        c = cosmos(t, "mistico"); col = color_de("blackbolt")
        figura(c, "blackbolt_pie", W / 2, PISO, FH, t, "pop")
        cx, cy = W / 2, PISO - FH * .86; dd = ImageDraw.Draw(c)
        for k in range(5):
            u = ((t * .9 + k * .3) % 1.5) / 1.5
            if t < .6: break
            r = P(60, 50) + u * P(900, 1000); a = int(230 * (1 - u))
            dd.ellipse((cx - r, cy - r * .55, cx + r, cy + r * .55), outline=col + (a,), width=max(3, int(10 * (1 - u))))
        chip(c, "UN SUSURRO", W / 2, P(1840, 1010), col, P(46, 44), eo(pr(t, .5, .3)))
        flash(c, t, .15, col); c = zoom(c, t, d, 1.0, 1.08)
        return shake(c, t - .6, 18, .6) if t > .6 else c
    return S("voz", f)

GEMAS = [(170, 90, 255), (80, 150, 255), (255, 60, 70), (255, 150, 40), (60, 255, 120), (255, 220, 40)]
def e_gemas(nombres=("IRON MAN", "REED", "XAVIER", "STRANGE", "NAMOR", "BLACK BOLT")):
    def f(t, d):
        c = cosmos(t, "thanos")
        texto(c, "UNA GEMA PARA CADA UNO", W / 2, P(330, 150), P(70, 62), (255, 255, 255), alpha=eo(pr(t, .1, .4)), glow_col=ORO)
        for i, (col, nm) in enumerate(zip(GEMAS, nombres)):
            if HZ: x, y = W * (.12 + i * .152), 470
            else: x, y = W * (.2 + (i % 3) * .3), 760 + (i // 3) * 520
            u = pr(t, .3 + i * .22, .4)
            if u <= 0: continue
            gema(c, x, y, P(95, 72), t - (.3 + i * .22), col)
            chip(c, nm, x, y + P(200, 160), col, P(36, 30), eo(u))
        return zoom(c, t, d, 1.0, 1.05)
    return S("gemas", f)

def e_memoria():
    """Strange borra la memoria del Capitán América: el Capi se desvanece con interferencia."""
    def f(t, d):
        c = cosmos(t, "azul"); mw = P(W * .5, W * .4)
        hc = min(h_fit("cap_sincasco", FH * .9, mw), h_fit("strange_magia", FH * .9, mw))
        mandala(c, P(W * .73, W * .7), P(950, 520), P(360, 300), t, color_de("strange"), .5)
        hilos(c, P(W * .73, W * .7), P(900, 450), t, color_de("strange"), n=24, abanico=(150, 210))
        k = eo(pr(t, 1.0, 1.4))
        figura(c, "cap_sincasco", P(W * .28, W * .3), PISO, hc, t, "izq", alpha=1 - .75 * k)
        figura(c, "strange_magia", P(W * .73, W * .7), PISO, hc, t, "der", retraso=.15)
        chip(c, "MEMORIA BORRADA", W / 2, P(1840, 1010), color_de("strange"), P(44, 42), eo(pr(t, 1.2, .3)))
        c = zoom(c, t, d, 1.0, 1.06)
        return glitch(c, (t - 1.0) % .9, .35, 22) if t > 1.0 else c
    return S("memoria", f)

def e_lupa_fig(fig, chip_txt, pal="doom"):
    def f(t, d):
        c = cosmos(t, pal); figura(c, fig, W / 2, PISO, FH, t, "pop")
        c = c.filter(ImageFilter.GaussianBlur(int(4 + 10 * eo(pr(t, .1, .5)))))
        lupa(c, P(W * .58, W * .56), P(800, 420), t)
        chip(c, chip_txt, W / 2, P(1500, 880), (255, 255, 255), P(50, 48), eo(pr(t, .3, .3)))
        return zoom(c, t, d, 1.0, 1.1)
    return S("lupa", f)

def e_estrellas_i(titulo, nota=4):
    def f(t, d):
        c = cosmos(t, "mistico"); figura(c, "blackbolt_pie", P(W / 2, W * .85), PISO, P(560, 520), t, "der", alpha=P(.35, 1), reflejo=False)
        texto(c, titulo, P(W / 2, W * .42), P(620, 300), P(64, 66), (255, 255, 255), glow_col=ORO)
        estrellas(c, t, nota, P(W / 2, W * .42), P(900, 520)); texto(c, f"{nota} / 5", P(W / 2, W * .42), P(1120, 700), P(90, 84), ORO, alpha=eo(pr(t, 1.5, .3)), glow_col=ORO)
        return zoom(c, t, d, 1.0, 1.05)
    return S("estrellas", f)

def e_continuara_i():
    def f(t, d):
        c = cosmos(t, "mistico", velocidad=.5); figura(c, "blackbolt_pie", W / 2, PISO, FH * .9, t, "pop", alpha=.6)
        c.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 90)))
        texto(c, "CONTINUARÁ…", W / 2, P(860, 470), P(130, 140), (255, 255, 255), alpha=eo(pr(t, .5, .6)), glow_col=AZ, stroke=8)
        chip(c, "CAP. 4 · LAS INCURSIONES", W / 2, P(1100, 650), ORO, P(40, 40), eo(pr(t, 1.2, .4)))
        return c
    return S("continuara", f)

def e_cta_i(youtube=False):
    def f(t, d):
        c = cosmos(t, "mistico")
        figura(c, "blackbolt_mano", P(W / 2, W * .24), P(1180, 880), P(760, 700), t, "pop", reflejo=False)
        caja_comentario(c, t, "ILLUMINATI", x=P(W / 2, W * .68), y=P(1320, 400), col=ORO)
        if youtube: chip(c, "HISTORIA COMPLETA EN YOUTUBE", W / 2, P(1560, 900), ROJO, P(40, 38), eo(pr(t, 1.6, .3)), (40, 6, 10))
        barra_suscribir(c, t, x=P(W / 2, W * .68), y=P(1740, 600), inicio=2.0 if youtube else 1.4)
        return c
    return S("cta", f)

# ---------------------------------------------------------------- guion completo (YouTube)
def bloques():
    B = {}
    B["intro"] = [
        L(e_narrador(), INTRO_GAMER[0], *INTRO_GAMER[1]),
        L(e_foto(1, chip_txt="UNA REUNIÓN SECRETA", mov=1), "Imagina una sala secreta. Seis sillas. Y sentados en ellas, seis de los héroes más poderosos de Marvel.", "secreta", "seis"),
        L(e_impacto("LOS\nILLUMINATI", ORO, "mistico", fig="blackbolt_pie"), "Decidiendo el destino del planeta… sin que nadie lo supiera. Ni siquiera los Vengadores.", "nadie", "vengadores"),
        L(e_grupo(["iron_mk42", "reed_legends", "strange_magia"], "CAMINO A DOOMSDAY · CAP. 3", "mistico", ORO), "Bienvenido al capítulo tres de nuestra serie Camino a Doomsday: los Illuminati, la sociedad secreta de Marvel.", "illuminati", "secreta"),
        L(e_dos("blackbolt_mano", "bestia_clasico", "FIGURAS DE COMICS STORE", "azul", chip_col=ORO), "Y como siempre, todas las figuras que vas a ver son de nuestra tienda, Comics Store.", "figuras", "comics", "store"),
        L(e_foto(1, chip_txt="EL CAMINO A DOOMSDAY", mov=2, oscuro=.35), "Y ojo, porque lo que decidieron en esa sala secreta lleva directo a Avengers Doomsday.", "directo", "doomsday"),
        L(e_narrador(), "Quédate hasta el final, porque uno de ellos resultó ser un impostor… y otro le borró la memoria al Capitán América.", "impostor", "memoria"),
    ]
    B["cap1"] = [
        L(e_capitulo(1, "LA IDEA DE TONY STARK", ORO, "mistico"), "Capítulo uno. La idea de Tony Stark.", "tony", "stark"),
        L(e_comic("2005", "#7", fig="iron_mk42", titulo="NEW AVENGERS"), "Los Illuminati aparecieron por primera vez en dos mil cinco, en New Avengers número siete, del guionista Brian Michael Bendis.", "cinco", "bendis"),
        L(e_comic("2006", "#1", fig="reed_pie", titulo="ILLUMINATI"), "Y en dos mil seis, un especial contó toda su historia secreta. Una historia que, según los cómics, venía de muchos años atrás.", "seis", "secreta"),
        L(e_foto(2, chip_txt="LA GUERRA KREE-SKRULL", mov=2), "Todo empezó después de la guerra Kree-Skrull, cuando dos imperios alienígenas convirtieron la Tierra en su campo de batalla.", "guerra", "alienígenas"),
        L(e_comic("1971", "#89", fig="iron_clasico", titulo="AVENGERS"), "Esa guerra es una de las sagas más famosas de Los Vengadores: salió entre mil novecientos setenta y uno y setenta y dos, del número ochenta y nueve al noventa y siete.", "setenta", "vengadores"),
        L(e_narrador(), "Y después de ver lo cerca que estuvo la Tierra de caer, alguien pensó que los héroes necesitaban organizarse. Pero en secreto.", "organizarse", "secreto"),
        L(e_fig("iron_tony", "UNA IDEA DE TONY STARK", "mistico"), "Tony Stark tuvo una idea: reunir a los líderes de cada rincón del mundo de los héroes. Una especie de Naciones Unidas de superhéroes.", "idea", "naciones"),
        L(e_foto(1, chip_txt="SEIS MIEMBROS", mov=3), "Así nació el grupo. Seis miembros, y cada uno representaba algo distinto.", "seis", "distinto"),
        L(e_narrador(), "Bendis, su creador, lo explicó así: cada miembro representa algo muy especial del Universo Marvel. Mira.", "especial"),
        L(e_fig("iron_mk42", "IRON MAN · TECNOLOGÍA", "mistico"), "Iron Man: la tecnología, y el hombre común sin superpoderes que trabaja con el gobierno.", "tecnología"),
        L(e_fig("reed_legends", "REED RICHARDS · CIENCIA", "azul"), "Reed Richards, el líder de Los Cuatro Fantásticos: la ciencia.", "ciencia"),
        L(e_fig("xavier_silla", "CHARLES XAVIER · MUTANTES", "mistico"), "Charles Xavier, el líder de los X-Men: los mutantes.", "mutantes"),
        L(e_fig("strange_magia", "DOCTOR STRANGE · MAGIA", "mistico", efecto="hilos"), "Doctor Strange, el Hechicero Supremo: la magia.", "magia"),
        L(e_fig("namor_tridente", "NAMOR · EL ANTIHÉROE", "azul"), "Namor, el rey de la Atlántida: el antihéroe del grupo.", "antihéroe"),
        L(e_fig("blackbolt_pie", "BLACK BOLT · LOS INHUMANOS", "mistico"), "Y Black Bolt, el rey de los Inhumanos. Un rey que casi nunca habla…", "rey", "habla"),
        L(e_voz(), "…porque un simple susurro suyo puede derrumbar una ciudad entera.", "susurro", "ciudad"),
        L(e_fig("panther_pie", "BLACK PANTHER DIJO QUE NO", "mistico"), "Pero hubo uno que dijo que no: Black Panther. Se reunieron con él en Wakanda, y se negó a participar.", "no", "wakanda"),
        L(e_narrador(), "¿Por qué? Porque sintió que un grupo así, tarde o temprano, iba a terminar haciendo cosas nada heroicas. Y tenía toda la razón.", "razón"),
        L(e_foto(1, chip_txt="SOLO COMPARTIR INFORMACIÓN", mov=4, oscuro=.4), "Los demás tampoco aceptaron gobernar a los héroes. Pero acordaron reunirse en secreto para compartir información.", "secreto", "información"),
        L(e_dos("xavier_silla", "reed_pie2", "CONTRA EL BEYONDER", "mistico", chip_col=ORO), "Y no se quedaron quietos. Cuando empezaron las primeras Secret Wars, Xavier y Reed intentaron dejar inconscientes a todos los combatientes, para que el Beyonder no tuviera su espectáculo.", "beyonder", "espectáculo"),
        L(e_impacto("FALLÓ", ROJO, "mistico"), "No funcionó. Y de esa guerra te hablo en el capítulo nueve de esta serie.", "nueve"),
    ]
    B["cap2"] = [
        L(e_capitulo(2, "LA MISIÓN SKRULL", VERDE, "doom"), "Capítulo dos. La misión Skrull.", "skrull"),
        L(e_foto(2, chip_txt="EL IMPERIO SKRULL", mov=1, particula=VERDE), "Su primera misión fue una locura: viajar hasta el imperio de los Skrulls.", "locura", "skrulls"),
        L(e_grupo(["iron_mk42", "namor_vortice", "strange_portal"], "UNA ADVERTENCIA", "doom", VERDE), "Se presentaron ante el emperador Skrull, Dorrek séptimo, para advertirle que no volvieran a atacar la Tierra nunca más.", "emperador", "nunca"),
        L(e_impacto("CAPTURADOS", ROJO, "rojo"), "Pero los Skrulls los capturaron.", "capturaron"),
        L(e_foto(2, chip_txt="LOS ESTUDIARON", mov=3, oscuro=.45, particula=VERDE), "Y mientras estaban prisioneros, los estudiaron por dentro y por fuera.", "estudiaron"),
        L(e_fig("iron_rayos", "EL ESCAPE", "rojo", sacude=True), "Al final escaparon, con Iron Man al frente de la fuga.", "escaparon"),
        L(e_lupa_fig("iron_tony", "UN DETALLE", "doom"), "Pero había un problema: con todo lo que aprendieron de ellos, los Skrulls descubrieron cómo pasar desapercibidos en la Tierra.", "problema", "desapercibidos"),
        L(e_narrador(), "Los Illuminati lo sabían: tarde o temprano iba a llegar otra invasión. Y llegó. Pero eso te lo cuento más adelante.", "invasión"),
    ]
    B["cap3"] = [
        L(e_capitulo(3, "LAS GEMAS DEL INFINITO", MORADO, "thanos"), "Capítulo tres. Las Gemas del Infinito.", "gemas", "infinito"),
        L(e_fig("reed_pie2", "REED TENÍA UN SECRETO", "thanos"), "Años después, Reed Richards volvió a reunirlos. Tenía un secreto enorme.", "secreto"),
        L(e_foto(3, chip_txt="LAS SEIS GEMAS", mov=1), "Había estado buscando las Gemas del Infinito. Con ayuda del grupo, consiguieron las seis.", "seis"),
        L(e_dos("thanos_guante", "reed_legends", "NUNCA MÁS", "thanos", vs=True), "La idea era que nadie, nunca más, pudiera hacer lo que hizo Thanos con el Guantelete.", "thanos", "guantelete"),
        L(e_impacto("NO SE PUEDEN\nDESTRUIR", MORADO, "thanos"), "Reed intentó hacerlas desaparecer con su voluntad. No funcionó.", "desaparecer"),
        L(e_foto(3, chip_txt="UATU · EL VIGILANTE", mov=3, oscuro=.4), "Hasta Uatu, el Vigilante, apareció para regañarlos por jugar con ese poder.", "uatu", "vigilante"),
        L(e_gemas(), "Así que tomaron una decisión: cada uno se llevaría una gema, y no le diría a nadie dónde la escondió.", "gema", "nadie"),
        L(e_narrador(), "Seis héroes. Seis gemas. Seis secretos. ¿Qué podría salir mal?", "seis", "mal"),
        L(e_foto(3, chip_txt="ROBADAS UNA A UNA", mov=4, sacude=True, oscuro=.35), "Mucho después, un villano llamado The Hood descubrió que las tenían… y empezó a robarlas una por una. El grupo tuvo que volver a reunirse para recuperarlas.", "hood", "robarlas"),
    ]
    B["cap4"] = [
        L(e_capitulo(4, "EL EXILIO DE HULK", (110, 255, 70), "doom"), "Capítulo cuatro. El exilio de Hulk.", "hulk"),
        L(e_fig("hulk_puno", "DEMASIADO PELIGROSO", "doom", sacude=True), "Después de que Hulk perdiera el control en Las Vegas, los Illuminati se reunieron otra vez.", "control", "vegas"),
        L(e_fig("iron_tony", "LA PROPUESTA", "mistico"), "Iron Man propuso algo extremo: mandar a Hulk al espacio.", "espacio"),
        L(e_foto(4, chip_txt="EXILIADO AL ESPACIO", mov=1), "Lo engañaron, lo subieron a una nave y lo lanzaron lejos de la Tierra.", "engañaron", "lanzaron"),
        L(e_dos("namor_tridente", "iron_mk42", "NAMOR SE OPUSO", "azul", vs=True), "Namor fue el único que se opuso. Les advirtió que Hulk iba a volver… y que iba a querer venganza.", "opuso", "venganza"),
        L(e_fig("namor_vortice", "NAMOR SE VA", "azul"), "Y se fue del grupo.", "fue"),
        L(e_foto(4, chip_txt="PLANETA HULK", mov=3, oscuro=.35), "La nave terminó en un planeta llamado Sakaar. Allí Hulk fue esclavo, luego gladiador… y al final, rey. Sí: Sakaar es el mismo planeta que viste en Thor Ragnarok.", "sakaar", "ragnarok"),
        L(e_impacto("LA NAVE\nEXPLOTÓ", (255, 120, 30), "rojo", fig="hulk_pie"), "Pero la nave en la que lo mandaron explotó, y mató a su esposa y a miles de personas. Hulk culpó a los Illuminati.", "explotó", "culpó"),
        L(e_impacto("HULK\nREGRESÓ", (110, 255, 70), "doom", fig="hulk_roca"), "Namor tenía razón. En World War Hulk, de dos mil siete, Hulk regresó.", "razón", "regresó"),
        L(e_fig("hulk_roca", "TOMÓ MANHATTAN", "doom", sacude=True), "Tomó Manhattan y destruyó la Torre Stark en su pelea contra Iron Man.", "manhattan", "stark"),
        L(e_grupo(["iron_mk42", "reed_legends", "strange_magia", "blackbolt_pie"], "GLADIADORES", "doom", (110, 255, 70)), "Capturó a Iron Man, Reed, Strange y Black Bolt… y los obligó a pelear como gladiadores en el Madison Square Garden.", "gladiadores", "madison"),
        L(e_dos("namor_tridente", "xavier_silla", "LOS PERDONÓ", "azul", chip_col=(40, 230, 190)), "A Namor lo perdonó, porque fue el único que votó en contra. Y a Xavier también, porque ni siquiera estaba en esa reunión.", "perdonó"),
        L(e_fig("iron_rayos", "LOS SATÉLITES", "rojo", sacude=True), "Al final, Tony Stark usó unos satélites armados para derribarlo, y Hulk volvió a ser Bruce Banner.", "satélites", "banner"),
        L(e_narrador(), "No los mató. Pero el mensaje quedó claro: sus decisiones secretas tenían consecuencias.", "consecuencias"),
    ]
    B["cap5"] = [
        L(e_capitulo(5, "EL IMPOSTOR", ROJO, "rojo"), "Capítulo cinco. El impostor.", "impostor"),
        L(e_foto(5, chip_txt="CIVIL WAR", mov=1), "Luego llegó Civil War: la guerra entre héroes.", "guerra"),
        L(e_dos("iron_mk42", "reed_pie", "A FAVOR DEL REGISTRO", "rojo", chip_col=ORO), "Iron Man y Reed Richards lideraron el bando a favor del registro de superhéroes.", "registro"),
        L(e_grupo(["strange_magia", "blackbolt_pie", "namor_tridente"], "CADA UNO POR SU LADO", "rojo", ROJO), "Strange no se metió. Black Bolt y los Inhumanos tampoco. Namor solo pensó en lo suyo. Y Xavier ni siquiera estaba en el planeta.", "planeta"),
        L(e_foto(1, chip_txt="LA ÚLTIMA REUNIÓN", mov=2, oscuro=.4), "Después, Iron Man llamó a una última reunión. Tenía algo que mostrarles.", "última"),
        L(e_impacto("UN SKRULL", VERDE, "doom"), "El cuerpo de un Skrull que se había hecho pasar por Elektra.", "skrull", "elektra"),
        L(e_fig("blackbolt_mano", "¿BLACK BOLT?", "doom", sacude=True), "Y en plena reunión descubrieron algo peor: Black Bolt… no era Black Bolt.", "peor"),
        L(e_impacto("ERA UN\nSKRULL", VERDE, "doom", fig="blackbolt_pie"), "Era un Skrull disfrazado. Todo lo que les estudiaron en aquella misión, lo usaron contra ellos.", "disfrazado", "contra"),
        L(e_fig("namor_vortice", "NAMOR LO ACABA", "doom", sacude=True), "El impostor atacó al grupo, y fue Namor quien acabó con él.", "impostor", "namor"),
        L(e_fig("blackbolt_pie", "EL VERDADERO BLACK BOLT", "mistico"), "¿Y el verdadero Black Bolt? Estaba prisionero de los Skrulls. Su esposa, Medusa, terminó rescatándolo.", "prisionero", "medusa"),
        L(e_foto(2, chip_txt="SECRET INVASION · 2008", mov=4, particula=VERDE), "Ese fue el comienzo de Secret Invasion, de dos mil ocho: los Skrulls habían reemplazado a héroes por todo el planeta. Ya nadie sabía quién era quién.", "invasion", "quién"),
        L(e_narrador(), "Nadie confiaba en nadie, y el grupo se rompió. Pero esto no termina aquí…", "rompió"),
    ]
    B["cap6"] = [
        L(e_capitulo(6, "EL REGRESO", (170, 90, 255), "mistico"), "Capítulo seis. El regreso.", "regreso"),
        L(e_comic("2013", "#1", fig="panther_lanza", titulo="NEW AVENGERS"), "En dos mil trece, en la nueva serie de New Avengers, alguien volvió a reunirlos. Y esta vez fue… Black Panther.", "trece", "panther"),
        L(e_fig("panther_lanza", "EL QUE DIJO QUE NO", "mistico"), "Sí, el mismo que al principio dijo que no. Había descubierto una amenaza contra todo el universo.", "amenaza"),
        L(e_fig("bestia_clasico", "BESTIA · NUEVO MIEMBRO", "azul"), "Xavier había muerto, y en su lugar entró Bestia, el científico de los X-Men. Y uno de los cinco X-Men originales de mil novecientos sesenta y tres.", "bestia", "originales"),
        L(e_grupo(["panther_pie", "bestia_ruge", "blackbolt_pie", "reed_pie2"], "LOS NUEVOS ILLUMINATI", "mistico", (170, 90, 255)), "Black Panther, Bestia, Black Bolt, Reed, Iron Man, Strange y Namor. Y un invitado nuevo: el Capitán América.", "capitán"),
        L(e_foto(3, chip_txt="LAS GEMAS SE DESTRUYEN", mov=2, sacude=True), "Primero usaron el Guantelete del Infinito para detener un choque entre mundos. Funcionó… pero las gemas se destruyeron. Solo la del Tiempo desapareció.", "guantelete", "destruyeron"),
        L(e_dos("cap_sincasco", "iron_tony", "EL CAPITÁN SE OPUSO", "azul", vs=True), "Cuando el grupo empezó a hablar de armas capaces de destruir mundos enteros, el Capitán se opuso.", "armas", "opuso"),
        L(e_memoria(), "Y entonces Doctor Strange hizo algo terrible: con un hechizo preparado de antemano, le borró la memoria.", "hechizo", "memoria"),
        L(e_fig("cap_saludo", "SU MEMORIA VOLVIÓ", "azul"), "El Capitán no recordó nada… hasta un año después, en Original Sin. Y cuando recordó, se sintió traicionado.", "traicionado"),
        L(e_incursion("INCURSIONES"), "¿Y cuál era esa amenaza? Mundos enteros chocando contra la Tierra: las incursiones. Pero eso es el próximo capítulo.", "incursiones"),
        L(e_fig("namor_vortice", "DESTRUYÓ UN MUNDO", "rojo", sacude=True), "En esa lucha, Namor hizo lo que nadie se atrevía: destruyó un planeta entero. Y lo expulsaron del grupo.", "planeta", "expulsaron"),
        L(e_battleworld(chip_txt="EL FINAL · SECRET WARS"), "Y así llegó el final: la última incursión, la muerte del multiverso… y Secret Wars, de dos mil quince.", "final", "quince"),
        L(e_dos("panther_lanza", "reed_pie", "EL ÚLTIMO PLAN", "thanos", chip_col=ORO), "Black Panther y Namor volvieron a armar el Guantelete para enfrentar a Doom. Y Reed terminó reconstruyendo todo el multiverso.", "guantelete", "multiverso"),
        L(e_narrador(), "Esa historia, la de Doom convertido en Dios, la vemos completa en el capítulo ocho. No te la pierdas.", "dios", "ocho"),
    ]
    B["cap7"] = [
        L(e_capitulo(7, "EN EL CINE", ORO, "mistico"), "Capítulo siete. En el cine.", "cine"),
        L(e_grupo(["xavier_silla", "reed_legends", "blackbolt_pie"], "TIERRA-838", "mistico", ORO), "En el cine los vimos en dos mil veintidós, en Doctor Strange en el Multiverso de la Locura.", "veintidós", "locura"),
        L(_lista(["MORDO", "CAPITANA CARTER", "BLACK BOLT", "CAPITANA MARVEL", "REED RICHARDS", "CHARLES XAVIER"], "strange_portal", ORO, "mistico"),
          "En la Tierra ochocientos treinta y ocho, los Illuminati eran Mordo, la Capitana Carter, Black Bolt, María Rambeau como Capitana Marvel, Reed Richards y Charles Xavier.", "ochocientos"),
        L(e_dos("xavier_silla", "reed_pie", "STEWART Y KRASINSKI", "mistico", chip_col=ORO), "Patrick Stewart regresó como Xavier. Y John Krasinski fue Reed Richards, el actor que muchos fans pedían.", "stewart", "krasinski"),
        L(e_fig("blackbolt_pie", "ANSON MOUNT · BLACK BOLT", "mistico"), "Y la gran sorpresa: Anson Mount volvió como Black Bolt, el mismo papel que hizo en la serie Inhumanos de dos mil diecisiete. Esta vez, con su traje de los cómics.", "mount", "traje"),
        L(e_impacto("CAPITANA\nCARTER", (70, 140, 255), "azul"), "Hayley Atwell fue la Capitana Carter: en ese mundo, la que recibió el suero de súper soldado fue Peggy Carter, no Steve Rogers.", "suero", "peggy"),
        L(e_fig("strange_portal", "JUZGAN A STRANGE", "mistico"), "Ahí juzgaron a nuestro Doctor Strange, porque el Strange de su mundo había usado el Darkhold… y casi lo destruye.", "darkhold"),
        L(e_impacto("WANDA LOS\nDESTRUYE", (255, 50, 90), "rojo", fig="wanda_pie"), "Pero llegó Wanda. Y en pocos minutos acabó con casi todos. Solo sobrevivió Mordo.", "wanda", "mordo"),
        L(e_fig("blackbolt_mano", "SU PROPIA VOZ", "rojo", sacude=True), "A Black Bolt le hizo lo peor: su propia voz terminó destruyéndolo.", "voz"),
        L(e_dos("reed_pie2", "blackbolt_pie", "¿VOLVERÁN EN DOOMSDAY?", "azul", chip_col=ORO), "Ahora, con el Reed Richards de Pedro Pascal y los X-Men en Doomsday, muchos fans sueñan con ver una nueva versión de los Illuminati.", "doomsday", "illuminati"),
    ]
    B["cierre"] = [
        L(e_narrador(), "¿Mi opinión? Los Illuminati son de lo mejor de Marvel, porque muestran a los héroes tomando decisiones que no son blancas ni negras.", "opinión"),
        L(e_narrador(), "Querían proteger al mundo. Pero cada secreto que guardaron terminó volviéndose en su contra: los Skrulls, Hulk, el Capitán…", "secreto", "contra"),
        L(e_dos("panther_pie", "iron_mk42", "¿QUIÉN TENÍA RAZÓN?", "mistico", vs=True), "Al final, el único que tuvo razón desde el principio fue Black Panther.", "panther"),
        L(e_dos("cap_sincasco", "strange_magia", "¿DE QUÉ LADO ESTÁS?", "azul", vs=True), "Y tú, ¿de qué lado estarías: del Capitán América o de los Illuminati? Te leo en los comentarios.", "lado", "comentarios"),
        L(e_narrador(), "Y piensa en esto: sin los Illuminati no habría World War Hulk, ni Secret Invasion, ni las incursiones. Casi todo lo que lleva a Doomsday pasa por esa sala secreta.", "doomsday", "sala"),
        L(e_estrellas_i("¿LOS MEJORES DE MARVEL?", 4), "¿Mi nota? Cuatro de cinco. Geniales… pero no los quisiera guardando mis secretos.", "cuatro", "secretos"),
        L(e_grupo(["blackbolt_pie", "bestia_clasico", "namor_tridente"], "COMICS-STORE.COM.CO", "mistico", ORO), "Y si quieres armar tu propio consejo secreto, en Comics Store tenemos estas figuras. Las encuentras en comics store punto com punto co.", "consejo"),
        L(e_continuara_i(), "En el próximo capítulo: las incursiones. Mundos chocando… y un villano escondido detrás de todo. Continuará…", "incursiones", "continuará"),
        L(e_cta_i(), "Comenta ILLUMINATI si quieres el capítulo cuatro, suscríbete y activa la campanita. ¡Nos vemos en el próximo video!", "illuminati"),
    ]
    return B

FOTO_AMB_I = {1: "noche", 2: "viento+cosmos", 3: "maquina+magia", 4: "cosmos", 5: "fuego+trueno"}
CLAVE_AMB_I = [("hulk", "impacto"), ("susurro", "trueno"), ("capturaron", "impacto"), ("incursi", "explosion+cosmos"), ("wanda", "magia"), ("hechizo", "magia")]
FOTO_CLIMA_I = {1: "noche", 2: "viento", 3: None, 4: None, 5: "lluvia+fuego"}
CLAVE_CLIMA_I = [("destruyó un planeta", "explosion"), ("manhattan", "explosion")]

def preparar(esc):
    for fn, txt, _ in esc:
        low = txt.lower(); a = None
        if getattr(fn, "foto", None): a = FOTO_AMB_I.get(fn.foto); fn.clima = FOTO_CLIMA_I.get(fn.foto)
        else:
            if fn.__name__ != "narrador": fn.clima = next((v for k, v in CLAVE_CLIMA_I if k in low), None)
            a = next((v for k, v in CLAVE_AMB_I if k in low), None)
            if not a: a = {"impacto": "impacto+magia", "capitulo": "cosmos", "continuara": "cosmos+magia", "voz": "trueno", "gemas": "magia",
                           "memoria": "magia", "estrellas": "magia"}.get(fn.__name__)
        if a: fn.amb = a
    return clima.envolver(esc)

def guion_yt():
    B = bloques(); esc = []
    for k in ("intro", "cap1", "cap2", "cap3", "cap4", "cap5", "cap6", "cap7", "cierre"): esc += B[k]
    esc = preparar(esc)
    re_ = [i for i, e in enumerate(esc) if e[0].__name__ == "narrador" and i > 0]
    return esc, re_

# ---------------------------------------------------------------- shorts (salen del mismo guion)
def _short(gancho, tramo):
    gancho[0].amb = "impacto+magia"
    return [gancho] + tramo + [L(e_cta_i(youtube=True), "Comenta ILLUMINATI, y mira la historia completa en nuestro canal de YouTube.", "illuminati", "youtube")]

def guion_short(n):
    esc, _ = guion_yt()
    if n == 1: return _short(L(e_impacto("LE BORRARON\nLA MEMORIA", (80, 140, 255), "azul", fig="cap_sincasco"), "Doctor Strange le borró la memoria al Capitán América. Y casi nadie lo sabe.", "memoria"),
                             _tramo(esc, "En dos mil trece, en la nueva serie", "El Capitán no recordó nada"))
    if n == 2: return _short(L(e_impacto("BLACK BOLT\nERA UN SKRULL", VERDE, "doom", fig="blackbolt_pie"), "Uno de los héroes más poderosos de Marvel… era un impostor.", "impostor"),
                             _tramo(esc, "Su primera misión fue una locura", "Pero había un problema") + _tramo(esc, "Después, Iron Man llamó", "¿Y el verdadero Black Bolt?"))
    if n == 3: return _short(L(e_impacto("MANDARON A HULK\nAL ESPACIO", (110, 255, 70), "doom", fig="hulk_puno"), "Seis héroes decidieron mandar a Hulk al espacio… y fue un error.", "error"),
                             _tramo(esc, "Después de que Hulk perdiera", "Al final, Tony Stark usó"))
    if n == 4: return _short(L(e_impacto("6 HÉROES\n6 GEMAS", MORADO, "thanos"), "Seis héroes escondieron las seis Gemas del Infinito… y no se lo dijeron a nadie.", "gemas"),
                             _tramo(esc, "Imagina una sala secreta", "Decidiendo el destino") + _tramo(esc, "Años después, Reed Richards", "Mucho después, un villano"))

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
