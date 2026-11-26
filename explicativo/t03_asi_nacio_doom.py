"""Comics Store · "Así nació Doom" (Parte 1) — YouTube 12-14 min + 4 shorts sacados del mismo guion.
Uso: FORMATO=horizontal python3 t03_asi_nacio_doom.py yt salida.mp4
     python3 t03_asi_nacio_doom.py s1|s2|s3|s4 salida.mp4      (shorts verticales)
     FORMATO=horizontal python3 t03_asi_nacio_doom.py final salida.mp4
Imágenes HD de Fernando (ChatGPT) en IMG_DIR: 01..14.(png|jpg|webp)."""
import os, sys, math, glob
os.environ.setdefault("SEMILLA", "asi_nacio_doom")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from t02_si_dejaste_marvel import *          # escenas genéricas (e_fig, e_dos, e_grupo, e_doom, ...)
from t02_si_dejaste_marvel import PRON as PRON2
from motor import render
from t01_strange_doom import e_lupa, e_comic, e_battleworld

IMG_DIR = os.environ.get("IMG_DIR", "/home/claude/doom/img")
PRON = dict(PRON2); PRON.update({"capcom": ("es", "cápcom"), "rivals": ("es", "ráivals"), "doomwar": ("es", "dumuor"), "russo": ("es", "ruso"), "víctor": ("es", "víctor"), "cynthia": ("es", "síntia"), "werner": ("es", "uérner"), "mefisto": ("es", "mefísto"),
    "latveria": ("es", "latvéria"), "doomstadt": ("es", "dúmstat"), "grimm": ("es", "grim"), "ben": ("es", "ben"), "johnny": ("es", "yóni"),
    "doombots": ("es", "dúmbots"), "galactus": ("es", "galáctus"), "surfer": ("es", "súrfer"), "silver": ("es", "sílver"), "namor": ("es", "namór"),
    "panther": ("es", "pánter"), "black": ("es", "blac"), "julian": ("es", "yúlian"), "mcmahon": ("es", "macmájon"), "toby": ("es", "tóbi"),
    "kebbell": ("es", "kébel"), "comic-con": ("es", "cómic con"), "stan": ("es", "estan"), "lee": ("es", "li"), "jack": ("es", "yac"),
    "kirby": ("es", "kérbi"), "peggy": ("es", "pégui"), "kristoff": ("es", "krístof"), "valeria": ("es", "valéria")})
COLORES = (VERDE, ORO)

# ---------------------------------------------------------------- imágenes HD
def _img_path(n):
    for ext in ("png", "jpg", "jpeg", "webp"):
        p_ = os.path.join(IMG_DIR, f"{n:02d}.{ext}")
        if os.path.exists(p_): return p_
    return None

from functools import lru_cache
@lru_cache(maxsize=16)
def _foto(n):
    p_ = _img_path(n)
    if not p_: return None
    im = Image.open(p_).convert("RGB"); k = max(W * 1.18 / im.width, H * 1.18 / im.height)
    return im.resize((int(im.width * k) + 1, int(im.height * k) + 1), Image.LANCZOS).convert("RGBA")

def fondo_foto(n, t, d, pal="mistico", mov=0):
    """Foto HD con movimiento de cámara suave (acercar / paneo). Si aún no llega la foto: fondo cósmico con aviso."""
    im = _foto(n)
    if im is None:
        c = cosmos(t, pal); chip(c, f"FOTO {n}", W / 2, P(1000, 540), (255, 255, 255), 40); return c
    u = eio(clamp(t / max(.1, d))); mx, my = im.width - W, im.height - H
    modos = [(.5, .5, 0, 1), (0, .5, 1, .5), (1, .5, 0, .5), (.5, 1, .5, 0), (.5, 0, .5, 1)]
    x0, y0, x1, y1 = modos[mov % len(modos)]
    ox = mx * (x0 + (x1 - x0) * u) if mov else mx / 2; oy = my * (y0 + (y1 - y0) * u) if mov else my / 2
    c = im.crop((int(ox), int(oy), int(ox) + W, int(oy) + H)).copy()
    if not mov: c = zoom(c, t, d, 1.0, 1.1)
    return c

def e_foto(n, fig=None, chip_txt=None, mov=0, lado="c", pal="mistico", sacude=False, oscuro=.25, alto=None, particula=None):
    def f(t, d):
        c = fondo_foto(n, t, d, pal, mov)
        if oscuro: c.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, int(255 * oscuro))))
        if particula: particulas(c, t, particula, n=35)
        if fig:
            x = {"c": W / 2, "i": P(W * .3, W * .26), "d": P(W * .7, W * .74)}[lado]
            figura(c, fig, x, PISO, alto or h_fit(fig, FH * .92, P(W * .8, W * .45)), t, {"c": "sube", "i": "izq", "d": "der"}[lado])
        if chip_txt: chip(c, chip_txt, W / 2, P(1840, 1010), color_de(fig) if fig else ORO, P(44, 42), eo(pr(t, .5, .3)))
        flash(c, t, .12); vineta(c, 140)
        return shake(c, t, 14) if sacude else c
    f = S("foto", f); f.foto = n; return f

def e_pizarra(error=False):
    def f(t, d):
        c = cosmos(t, "azul"); bw, bh = P(900, 1200), P(620, 640); x0, y0 = (W - bw) / 2, P(520, 150)
        L = Image.new("RGBA", (bw, bh), (0, 0, 0, 0)); dd = ImageDraw.Draw(L)
        dd.rounded_rectangle((0, 0, bw - 1, bh - 1), 18, fill=(28, 52, 40, 255), outline=(150, 110, 60, 255), width=14)
        ec = ["E = mc²", "F = m · a", "t · x > h", "p = h / L", "x² + y² = r²", "V = I · R"]
        for i, e in enumerate(ec):
            u = pr(t, .1 + i * .18, .3)
            if u > 0: dd.text((60 + (i % 2) * bw * .5, 70 + (i // 2) * bh * .27), e[:max(1, int(len(e) * u))], font=F(P(54, 52)), fill=(235, 240, 230, 255))
        place(c, L, W / 2, y0 + bh / 2, scale=.85 + .15 * eo(pr(t, 0, .4)))
        if error:
            k = eo(pr(t, .9, .5)); cx, cy = x0 + 60 + 170, y0 + 70 + bh * .27 + 30
            ImageDraw.Draw(c).ellipse((cx - 210 * k, cy - 70 * k, cx + 210 * k, cy + 70 * k), outline=(255, 50, 50, 255), width=9)
            texto(c, "ERROR", cx, cy + P(115, 105), P(64, 64), ROJO, alpha=eo(pr(t, 1.2, .3)), glow_col=ROJO)
        figura(c, "reed_estira" if error else "doom_pie3", P(W * .5, W * .86), PISO, P(560, 520), t, "der", retraso=.3, alpha=P(.9, 1), reflejo=False)
        return zoom(c, t, d, 1.0, 1.08)
    return S("pizarra", f)

def e_continuara():
    def f(t, d):
        c = cosmos(t, "doom", velocidad=.5); figura(c, "doom_libro", W / 2, PISO, FH * .9, t, "pop", alpha=.6)
        c.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 90)))
        texto(c, "CONTINUARÁ…", W / 2, P(860, 470), P(130, 140), (255, 255, 255), alpha=eo(pr(t, .5, .6)), glow_col=VERDE, stroke=8)
        chip(c, "PARTE 2 · DESPUÉS DEL 18 DE DICIEMBRE", W / 2, P(1100, 650), VERDE, P(36, 38), eo(pr(t, 1.2, .4)))
        return c
    return S("continuara", f)

def e_cta_doom(youtube=False):
    def f(t, d):
        c = cosmos(t, "doom")
        figura(c, "doom_magia", P(W / 2, W * .24), P(1180, 880), P(760, 700), t, "pop", reflejo=False)
        caja_comentario(c, t, "DOOM", x=P(W / 2, W * .68), y=P(1320, 400))
        if youtube: chip(c, "HISTORIA COMPLETA EN YOUTUBE", W / 2, P(1560, 900), ROJO, P(40, 38), eo(pr(t, 1.6, .3)), (40, 6, 10))
        barra_suscribir(c, t, x=P(W / 2, W * .68), y=P(1740, 600), inicio=2.0 if youtube else 1.4)
        return c
    return S("cta", f)

def e_estrellas_t(titulo, nota=5):
    def f(t, d):
        c = cosmos(t, "doom"); figura(c, "doom_libro", P(W / 2, W * .85), PISO, P(560, 520), t, "der", alpha=P(.35, 1), reflejo=False)
        texto(c, titulo, P(W / 2, W * .42), P(620, 300), P(64, 66), (255, 255, 255), glow_col=VERDE)
        estrellas(c, t, nota, P(W / 2, W * .42), P(900, 520)); texto(c, f"{nota} / 5", P(W / 2, W * .42), P(1120, 700), P(90, 84), ORO, alpha=eo(pr(t, 1.5, .3)), glow_col=ORO)
        return zoom(c, t, d, 1.0, 1.05)
    return S("estrellas", f)

def e_detalle():
    def f(t, d):
        c = cosmos(t, "rojo"); figura(c, "doom_pie2", W / 2, PISO, FH, t, "pop")
        c = c.filter(ImageFilter.GaussianBlur(int(4 + 10 * eo(pr(t, .1, .5)))))
        lupa(c, P(W * .58, W * .56), P(800, 420), t)
        chip(c, "UN DETALLE", W / 2, P(1500, 880), (255, 255, 255), P(54, 50), eo(pr(t, .3, .3)))
        return zoom(c, t, d, 1.0, 1.1)
    return S("lupa", f)

def e_cine(items):
    def f(t, d):
        c = cosmos(t, "mistico"); linea_tiempo(c, t, items)
        if not HZ: figura(c, "iron_tony", W / 2, 1880, 620, t, "sube", alpha=.6, reflejo=False)
        return zoom(c, t, d, 1.0, 1.05)
    return S("cine", f)

def _lista(items, fig, col, pal):
    def f(t, d):
        c = cosmos(t, pal); figura(c, fig, P(W / 2, W * .25), PISO, P(820, 880), t, "pop", alpha=P(.45, 1.))
        paso = max(.6, (d - .6) / len(items))
        for i, it in enumerate(items):
            chip(c, it, P(W / 2, W * .66), P(700 + i * 210, 330 + i * 190), col, P(42, 42), eo(pr(t, .2 + i * paso, .35)))
        return zoom(c, t, d, 1.0, 1.05)
    return S("lista", f)

# ---------------------------------------------------------------- guion completo (YouTube)
def L(esc, txt, *clave): return (esc, txt, set(clave))

def bloques():
    B = {}
    B["intro"] = [
        L(e_narrador(), INTRO_GAMER[0], *INTRO_GAMER[1]),
        L(e_doom("doom_magia", "EL VILLANO MÁS PELIGROSO"), "Hoy te traigo al villano más peligroso de Marvel. Más inteligente que Reed Richards, más orgulloso que Thanos… y dentro de poco, con la cara de Tony Stark.", "peligroso", "tony"),
        L(e_impacto("ASÍ NACIÓ\nDOOM", VERDE, "doom", fig="doom_pie3"), "Esta es la historia completa de Víctor von Doom. Así nació Doom.", "doom"),
        L(e_comic("1962", "#5", fig="doom_brazos", titulo="FANTASTIC 4"), "Apareció por primera vez en mil novecientos sesenta y dos, en Los Cuatro Fantásticos número cinco, creado por Stan Lee y Jack Kirby.", "sesenta", "kirby"),
        L(e_dos("reed_estira", "doom_pie2", "EL RIVAL DE REED", "azul", chip_col=VERDE), "Nació para ser el gran rival de Reed Richards. Pero su historia empieza mucho antes… en la nieve.", "rival", "nieve"),
        L(e_grupo(["doom_vuelo", "sue_pie", "surfer_tabla"], "FIGURAS DE COMICS STORE", "mistico", VERDE), "Y ojo: todas las figuras que vas a ver son de nuestra tienda, Comics Store.", "figuras", "comics", "store"),
    ]
    B["cap1"] = [
        L(e_capitulo(1, "UN NIÑO EN LATVERIA", (140, 200, 255), "azul"), "Capítulo uno. Un niño en Latveria.", "latveria"),
        L(e_foto(10, chip_txt="LATVERIA · EUROPA DEL ESTE", mov=1), "Latveria es un pequeño país de Europa del Este, rodeado de montañas. No existe en la vida real, pero en Marvel tiene capital, bandera y hasta embajadas.", "latveria", "marvel"),
        L(e_foto(12, chip_txt="CAPITAL: DOOMSTADT", mov=2), "Su capital, años después, se llamaría Doomstadt. Ya te imaginarás por qué.", "doomstadt"),
        L(e_foto(1, chip_txt="CAMPAMENTO GITANO", mov=3), "Pero antes de todo eso, en un campamento gitano en las montañas, nació Víctor von Doom.", "víctor", "doom"),
        L(e_foto(3, chip_txt="CYNTHIA · HECHICERA", mov=1, particula=MORADO), "Su madre, Cynthia, era una hechicera. Conocía secretos de la magia que nadie más se atrevía a tocar.", "cynthia", "hechicera"),
        L(e_foto(1, chip_txt="UN PUEBLO PERSEGUIDO", mov=4, oscuro=.4), "Su pueblo vivía perseguido por el barón que gobernaba el país y por sus soldados.", "perseguido", "barón"),
        L(e_fig("doom_pie2", "UNA HERIDA PROFUNDA", "azul", mandala_on=False), "Víctor creció viendo cómo los trataban. Esa herida fue tan profunda como la que después tendría en la cara.", "herida"),
        L(e_foto(4, "mefisto_trono", "MEFISTO", lado="d"), "Para proteger a su pueblo, buscó más poder… y terminó haciendo un trato con Mefisto, un demonio.", "mefisto", "demonio"),
        L(e_fig("mefisto_trono", "EL PRECIO", "rojo", sacude=True), "Ese trato le costó la vida. Y su alma quedó atrapada en el infierno.", "vida", "infierno"),
        L(e_foto(1, chip_txt="WERNER · SANADOR", mov=2), "Víctor se quedó solo con su padre, Werner, un sanador respetado por su gente.", "werner", "sanador"),
        L(e_foto(10, chip_txt="EL BARÓN", mov=4), "Un día, la esposa del barón que gobernaba Latveria cayó gravemente enferma.", "barón", "enferma"),
        L(e_impacto("SENTENCIADO", ROJO, "rojo"), "Werner intentó salvarla, pero no pudo. Y el barón lo condenó a muerte.", "condenó"),
        L(e_foto(2, chip_txt="LA HUIDA", mov=1, particula=(220, 235, 255)), "Padre e hijo escaparon a las montañas, en medio de una tormenta de nieve.", "tormenta", "nieve"),
        L(e_foto(2, chip_txt="SU ÚLTIMO ABRAZO", mov=3, particula=(220, 235, 255), oscuro=.4), "Esa noche, Werner cubrió a su hijo con su propio cuerpo para darle calor… y murió congelado.", "congelado"),
        L(e_impacto("SOLO", (140, 200, 255), "azul"), "Víctor sobrevivió. Pero ya no le quedaba nadie en el mundo.", "nadie"),
        L(e_foto(3, chip_txt="LOS LIBROS DE SU MADRE", mov=2, particula=VERDE), "Entre las cosas de su madre encontró sus libros de magia. Y ahí juró dos cosas.", "magia", "juró"),
        L(_lista(["1. VENGARSE", "2. SALVAR A SU MADRE"], "doom_pie2", VERDE, "doom"), "Vengarse de los que le quitaron todo… y sacar a su madre del infierno, cueste lo que cueste.", "vengarse", "infierno"),
        L(e_narrador(), "Y ese juramento lo va a perseguir toda la vida. Quédate, porque aquí empieza lo bueno.", "juramento"),
    ]
    B["cap2"] = [
        L(e_capitulo(2, "EL GENIO Y SU RIVAL", (80, 200, 255), "azul"), "Capítulo dos. El genio y su rival.", "genio", "rival"),
        L(e_fig("doom_pie3", "CIENCIA + MAGIA", "doom", efecto="hilos"), "Víctor creció mezclando dos cosas que nadie había unido: la ciencia y la magia. Era un genio.", "ciencia", "magia"),
        L(e_foto(5, chip_txt="UNIVERSIDAD ESTATAL IMPERIO", mov=1), "Tanto, que una universidad de Estados Unidos le ofreció una beca: la Universidad Estatal Imperio.", "beca", "imperio"),
        L(e_dos("reed_estira", "doom_pie3", "REED RICHARDS", "azul", chip_col=(80, 200, 255)), "Allí conoce a otro estudiante igual de brillante: Reed Richards.", "reed"),
        L(e_fig("cosa_pie", "BEN GRIMM", "azul"), "Y también a su compañero de cuarto, Ben Grimm. Sí: el que después sería la Cosa.", "ben", "cosa"),
        L(e_dos("reed_estira", "doom_pie2", "¿AMIGOS O RIVALES?", "azul", vs=True), "Reed quería ser su amigo. Víctor solo veía a alguien que podía ser mejor que él.", "amigo", "mejor"),
        L(e_fig("doom_pie3", "UN PRODIGIO PELIGROSO", "azul"), "Sus profesores lo veían como un prodigio… pero también como alguien peligroso. Víctor no buscaba amigos: buscaba resultados.", "prodigio", "peligroso"),
        L(e_fig("reed_estira", "HUMILDE Y QUERIDO", "azul"), "Reed, en cambio, era humilde y le caía bien a todo el mundo. Eso a Víctor le molestaba todavía más.", "humilde"),
        L(e_foto(6, chip_txt="LA MÁQUINA", mov=1, particula=VERDE), "En secreto, Víctor construye una máquina para comunicarse con el otro lado.", "máquina"),
        L(e_foto(6, chip_txt="RESCATAR A SU MADRE", mov=4, particula=VERDE), "No era un experimento cualquiera: era su forma de llegar al infierno y rescatar a su madre.", "infierno", "madre"),
        L(e_pizarra(False), "Reed revisa los planos de su compañero…", "planos"),
        L(e_pizarra(True), "…y encuentra un error en los cálculos. Se lo advierte. Pero Víctor es demasiado orgulloso para escucharlo.", "error", "orgulloso"),
        L(e_foto(7, chip_txt="¡BOOM!", sacude=True, oscuro=.1), "Enciende la máquina… y explota.", "explota"),
        L(e_impacto("LA CICATRIZ", ROJO, "rojo", fig="doom_pie2"), "La explosión le deja una cicatriz en la cara. Y lo expulsan de la universidad.", "cicatriz", "expulsan"),
        L(e_dos("doom_pie3", "reed_estira", "LA CULPA ES DE REED", "doom", chip_col=VERDE), "Desde ese día, culpa a Reed de todo. Aunque el error fue suyo.", "culpa", "suyo"),
        L(e_grupo(["reed_estira", "sue_pie", "antorcha_pie", "cosa_pie"], "LOS RAYOS CÓSMICOS", "azul", (80, 200, 255)), "Años después, Reed, Ben, Sue y Johnny viajan al espacio, los alcanzan los rayos cósmicos y ganan sus poderes.", "espacio", "poderes"),
        L(e_dos("reed_estira", "doom_pie2", "HÉROE Y VILLANO", "doom", vs=True), "Víctor ve cómo su rival se convierte en héroe… mientras él se convierte en el villano.", "héroe", "villano"),
        L(e_dos("cosa_pie", "antorcha_pie", "60 AÑOS DE RIVALIDAD", "azul", chip_col=(255, 120, 30)), "Esa rivalidad se volvió el corazón de Los Cuatro Fantásticos por más de sesenta años.", "sesenta"),
        L(e_dos("reed_estira", "doom_libro", "LAS DOS MENTES MÁS BRILLANTES", "azul", chip_col=ORO), "Y aunque se enfrentan una y otra vez, en el fondo se respetan: son las dos mentes más brillantes de Marvel.", "mentes", "brillantes"),
        L(e_detalle(), "Y aquí hay un detalle que muchos no saben: en varias versiones, la cicatriz era pequeña.", "detalle", "pequeña"),
        L(e_narrador(), "Lo que de verdad le destruyó la cara vino después. Y fue decisión suya.", "después", "decisión"),
    ]
    B["cap3"] = [
        L(e_capitulo(3, "LA MÁSCARA", ORO, "rojo"), "Capítulo tres. La máscara.", "máscara"),
        L(e_foto(8, chip_txt="EL TÍBET", mov=1), "Víctor viajó por el mundo hasta llegar a las montañas del Tíbet.", "tíbet"),
        L(e_foto(8, chip_txt="LOS MONJES", mov=3), "Allí lo recibió un grupo de monjes. Con ellos aprendió disciplina, y llevó su magia a otro nivel.", "monjes", "magia"),
        L(e_foto(9, chip_txt="LA ARMADURA", mov=1, particula=NARANJA), "Con su ayuda forjó una armadura completa…", "armadura"),
        L(e_foto(9, "doom_pie3", "LA MÁSCARA DE HIERRO", mov=0, particula=NARANJA), "…y una máscara de hierro.", "máscara", "hierro"),
        L(e_impacto("AL ROJO\nVIVO", (255, 90, 30), "rojo"), "Víctor no esperó a que se enfriara. Se la puso todavía al rojo vivo.", "rojo", "vivo"),
        L(e_foto(9, chip_txt="PARA SIEMPRE", mov=4, particula=NARANJA, oscuro=.45), "El metal le quemó la cara para siempre. Desde ese día, casi nadie lo ha visto sin la máscara.", "siempre", "máscara"),
        L(e_doom("doom_vuelo", "NACE DOCTOR DOOM", "sube"), "Ese día nació Doctor Doom.", "doom"),
        L(e_foto(10, "doom_pie2", "EL REGRESO", mov=0), "Regresó a Latveria con su armadura.", "latveria"),
        L(e_doom("doom_trono2", "MONARCA DE LATVERIA", "baja"), "Derrocó al rey que había perseguido a su familia… y se proclamó monarca.", "monarca"),
        L(e_foto(12, chip_txt="TECNOLOGÍA + MAGIA", mov=1), "Convirtió a Latveria en un país lleno de tecnología, con él como soberano absoluto.", "tecnología", "soberano"),
        L(e_foto(11, "doom_libro", "MANO DE HIERRO", mov=0), "Desde su castillo gobierna con mano de hierro. Y como es rey, tiene inmunidad diplomática: los héroes no pueden simplemente arrestarlo.", "inmunidad"),
        L(e_grupo(["doom_pie2", "doom_pie3", "doom_brazos"], "DOOMBOTS", "doom", VERDE), "Para no arriesgarse, creó los Doombots: robots idénticos a él. Muchas veces los héroes creen que lo vencieron… y era un robot.", "doombots", "robot"),
        L(e_fig("doom_vuelo", "CAMPOS DE FUERZA · RAYOS · VUELO", "doom", efecto="hilos"), "Su armadura tiene campos de fuerza, dispara rayos y le permite volar. Y además es uno de los hechiceros más poderosos de Marvel.", "armadura", "hechiceros"),
        L(e_fig("doom_libro", "SU HEREDERO: KRISTOFF", "doom"), "Incluso adoptó a un niño llamado Kristoff, y lo nombró su heredero.", "kristoff", "heredero"),
        L(e_fig("doom_pie3", "“DOOM NO SE EQUIVOCA”", "doom"), "Su orgullo es tan grande que habla de sí mismo en tercera persona. Para él, Doom nunca se equivoca.", "orgullo", "tercera"),
        L(e_dos("doom_pie2", "reed_estira", "DEMOSTRAR QUE ES MEJOR", "doom", chip_col=VERDE), "Y detrás de todo, siempre la misma obsesión: demostrar que es más inteligente que Reed Richards.", "obsesión", "reed"),
        L(e_fig("doom_magia", "EL PRECIO DEL PODER", "rojo", sacude=True), "Y para conseguir más magia, llegó a sacrificar a Valeria, su primer amor. Así de lejos puede llegar.", "valeria", "sacrificar"),
        L(e_narrador(), "Ahora sí: ¿qué tan poderoso llegó a ser? Te va a sorprender.", "poderoso"),
    ]
    B["cap4"] = [
        L(e_capitulo(4, "DOOM CONTRA TODOS", VERDE, "doom"), "Capítulo cuatro. Doom contra todos.", "todos"),
        L(e_grupo(["reed_estira", "sue_poder", "antorcha_vuelo", "cosa_pie"], "SUS ENEMIGOS DE SIEMPRE", "azul", (80, 200, 255)), "Su primera obsesión: los Cuatro Fantásticos. Reed, Sue, Johnny y Ben.", "cuatro", "fantásticos"),
        L(e_grupo(["cap_pelea", "wolverine_garras", "thor_hacha"], "CONTRA TODOS", "rojo", ROJO), "Pero con los años se enfrentó a casi todos: a los Vengadores, a los X-Men, a Spider-Man… y a veces, a todos al mismo tiempo.", "vengadores", "todos"),
        L(e_foto(6, "doom_brazos", "LA MÁQUINA DEL TIEMPO", mov=2, lado="d", particula=VERDE), "En su primera aparición, obliga a los Cuatro Fantásticos a viajar en el tiempo con su máquina para robar un tesoro.", "tiempo", "tesoro"),
        L(e_dos("namor_vortice", "doom_brazos", "ALIANZA CON NAMOR", "azul", chip_col=(40, 230, 190)), "Ya en Los Cuatro Fantásticos número seis, se alía con Namor, el rey de los mares, para destruirlos.", "namor"),
        L(e_fig("surfer_surf", "EL PODER CÓSMICO", "azul"), "En mil novecientos sesenta y seis, Doom le roba su poder cósmico a Silver Surfer.", "silver", "surfer"),
        L(e_fig("galactus_brazos", "GALACTUS", "thanos"), "El mismo poder que le había dado Galactus, el devorador de mundos.", "galactus"),
        L(e_dos("doom_magia", "surfer_tabla", "CASI GANA", "azul", vs=True), "Con ese poder casi lo consigue todo… hasta que Reed lo engaña y lo hace perderlo.", "reed", "perderlo"),
        L(e_comic("1984", "#1", fig="doom_vuelo", titulo="SECRET WARS"), "En las Guerras Secretas de mil novecientos ochenta y cuatro, un ser llamado el Todopoderoso reúne a héroes y villanos en un planeta lejano.", "todopoderoso"),
        L(e_doom("doom_magia", "UN DIOS"), "Doom le roba su poder… y por un momento se convierte en un dios.", "dios"),
        L(e_fig("doom_trono2", "EL EMPERADOR DOOM", "doom"), "En la novela gráfica Emperador Doom, controla la mente de todo el planeta y gobierna la Tierra entera.", "emperador", "tierra"),
        L(e_dos("panther_lanza", "doom_pie3", "EL VIBRANIO", "mistico", vs=True), "También tiene una vieja guerra con Black Panther: Doom siempre ha querido el vibranio de Wakanda.", "vibranio", "wakanda"),
        L(e_fig("panther_agacha", "DOOMWAR · 2010", "mistico", sacude=True), "En Doomwar, de dos mil diez, llega a invadir Wakanda para quedarse con el vibranio.", "doomwar", "wakanda"),
        L(e_dos("sue_poder", "doom_libro", "EL NOMBRE DE VALERIA", "azul", chip_col=(130, 210, 255)), "Y aunque parezca increíble, ayudó a nacer a la hija de Reed y Sue. Por eso la niña se llama Valeria, como su primer amor.", "valeria", "amor"),
        L(e_narrador(), "Pero su historia más famosa no es una batalla. Es un rescate.", "rescate"),
        L(e_comic("1989", "", fig="strange_portal", titulo="TRIUNFO Y TORMENTO"), "En Triunfo y Tormento, de mil novecientos ochenta y nueve, Doom y Doctor Strange bajan juntos al infierno.", "strange", "infierno"),
        L(e_dos("mefisto_trono", "doom_magia", "CARA A CARA CON MEFISTO", "rojo", vs=True), "Se enfrentan a Mefisto, el mismo demonio de su infancia… y Doom libera por fin el alma de su madre.", "mefisto", "madre"),
        L(e_impacto("LO LOGRÓ", VERDE, "doom", fig="doom_vuelo"), "Cumplió el juramento que hizo de niño en la nieve.", "juramento"),
        L(e_comic("2015", "#1", fig="doom_metal", titulo="SECRET WARS"), "En las Guerras Secretas de dos mil quince, el multiverso se destruye.", "multiverso"),
        L(e_battleworld(chip_txt="BATTLEWORLD"), "Doom salva lo que queda, y crea un solo planeta: Battleworld. Él es su Dios Emperador.", "battleworld", "emperador"),
        L(e_dos("strange_magia", "doom_trono2", "SU MANO DERECHA", "doom", chip_col=NARANJA), "Doctor Strange es su mano derecha… hasta que Doom lo mata.", "strange", "mata"),
        L(e_dos("doom_libro", "reed_estira", "“LO HABRÍAS HECHO MEJOR”", "azul", chip_col=ORO), "Al final, Reed lo derrota. Y Doom admite que Reed lo habría hecho mejor.", "reed", "mejor"),
        L(e_fig("doom_pie3", "SU CARA, CURADA", "mistico"), "Y al terminar esa historia, su cara por fin queda curada.", "curada"),
        L(e_dos("iron_mk42", "doom_pie3", "INFAMOUS IRON MAN", "rojo", chip_col=ORO), "Y lo más loco: en dos mil dieciséis, Doom se pone una armadura de Iron Man e intenta ser un héroe.", "iron", "héroe"),
        L(e_fig("iron_rodilla", "DOOM = IRON MAN", "rojo"), "Con Tony Stark fuera de combate, Víctor toma su lugar.", "tony"),
        L(e_dos("iron_tony", "doom_pie3", "AL REVÉS", "doom", chip_col=VERDE), "Doom fue Iron Man en los cómics. Y ahora, el actor de Iron Man será Doom en el cine.", "cómics", "cine"),
        L(e_fig("doom_magia", "HECHICERO SUPREMO", "mistico", efecto="hilos"), "Y en dos mil veinticinco, en Un Mundo Bajo Doom, se convierte en Hechicero Supremo y gobierna todo el planeta.", "hechicero", "planeta"),
        L(e_narrador(), "Y eso nos lleva al cine. Porque Doom ya había llegado antes… y no salió muy bien.", "cine"),
    ]
    B["cap5"] = [
        L(e_capitulo(5, "DOOM EN EL CINE", ORO, "mistico"), "Capítulo cinco. Doom en el cine.", "cine"),
        L(e_cine([("JULIAN\nMCMAHON", "2005"), ("JULIAN\nMCMAHON", "2007"), ("TOBY\nKEBBELL", "2015"), ("ROBERT\nDOWNEY JR.", "2026", VERDE)]), "Julian McMahon lo interpretó en dos mil cinco y en dos mil siete. Toby Kebbell, en dos mil quince.", "mcmahon", "kebbell"),
        L(e_fig("doom_brazos", "2005 · LA NUBE CÓSMICA", "azul"), "En la de dos mil cinco, Víctor era un empresario que ganaba poderes con la misma tormenta cósmica que los Cuatro Fantásticos.", "empresario", "cósmica"),
        L(e_impacto("NO\nCONVENCIÓ", ROJO, "rojo"), "Ninguna de esas versiones convenció a los fans. Doom merecía algo mejor.", "fans", "mejor"),
        L(e_dos("iron_tony", "doom_pie3", "COMIC-CON 2024", "doom", chip_col=VERDE), "En dos mil veinticuatro, en la Comic-Con, Marvel sorprendió a todos: Robert Downey Junior será Doctor Doom.", "downey", "doom"),
        L(e_fig("iron_tony", "SE QUITÓ LA MÁSCARA", "doom"), "Se quitó la máscara en pleno escenario, frente a miles de fans. Cinco años después de despedirse como Iron Man.", "máscara", "fans"),
        L(e_impacto("DOOM EN LOS\nVIDEOJUEGOS", VERDE, "doom", fig="doom_magia"), "Y fuera del cine, Doom es una leyenda de los videojuegos.", "videojuegos"),
        L(e_fig("doom_vuelo", "MARVEL VS. CAPCOM", "mistico"), "Es uno de los personajes favoritos de los jugadores en Marvel versus Capcom.", "capcom"),
        L(e_fig("doom_magia", "MARVEL RIVALS · 2024", "mistico", efecto="hilos"), "Y en Marvel Rivals, de dos mil veinticuatro, una versión del futuro, Doom dos mil noventa y nueve, es el gran villano de la historia.", "rivals", "villano"),
        L(e_narrador(), "Y ahora sí, lo que todos quieren saber: ¿por qué llega a Doomsday?", "doomsday"),
        L(e_franklin(), "Su primera aparición fue en la escena poscréditos de Los Cuatro Fantásticos: Primeros Pasos, interesado en Franklin, el hijo de Reed y Sue.", "franklin"),
    ]
    B["cap6"] = [
        L(e_capitulo(6, "EL CAMINO AL JUICIO FINAL", VERDE, "doom"), "Capítulo seis. El camino al juicio final.", "juicio"),
        L(e_foto(14, chip_txt="DOOMSDAY = EL DÍA DEL JUICIO", mov=1), "Doomsday significa el día del juicio final. Y el título no es casualidad.", "doomsday", "juicio"),
        L(e_doom("doom_magia", "CIENCIA Y MAGIA"), "La sinopsis oficial dice que Doom es un maestro de la ciencia y de la magia, y que desatará una crisis en todo el multiverso.", "ciencia", "magia"),
        L(e_dos("doom_vuelo", "thor_hacha", "LOS RUSSO · PELÍCULA 39", "doom", chip_col=VERDE), "La dirigen los hermanos Russo, los mismos de Infinity War y Endgame. Y es la película número treinta y nueve de Marvel.", "russo", "treinta"),
        L(e_centinelas(), "En el primer tráiler completo, de julio, Doom lanza a Thor con su magia y levanta un ejército de Centinelas.", "thor", "centinelas"),
        L(e_foto(13, chip_txt="INCURSIONES", mov=0, sacude=True, oscuro=.1), "El tráiler final, del veintitrés de noviembre, confirmó algo enorme: el viaje en el tiempo de Endgame provocó las incursiones.", "endgame", "incursiones"),
        L(e_foto(13, chip_txt="NUEVA YORK", mov=3, oscuro=.2), "Y por primera vez se ve una incursión sobre Nueva York: otra Tierra aparece en el cielo.", "nueva", "tierra"),
        L(e_fig("cap_saludo", "SIN SABERLO", "azul", z=(1.0, 1.08)), "Los Vengadores salvaron el universo… pero sin saberlo, rompieron el multiverso.", "rompieron"),
        L(e_fig("doom_pie3", "“VIDAS ROBADAS”", "doom"), "Por eso Doom les dice que han vivido vidas robadas, y que ahora deben devolverlas.", "robadas", "devolverlas"),
        L(e_fig("sue_poder", "“ANTES ERA DISTINTO”", "azul"), "Sue Storm cuenta que Doom antes era distinto… hasta que le quitaron todo lo que amaba.", "distinto", "amaba"),
        L(e_fig("cap_sincasco", "LAS CONSECUENCIAS", "azul"), "Y Steve Rogers tendrá que enfrentar lo que hizo con las gemas. En el tráiler deja a Peggy y a su hijo para irse con los Cuatro Fantásticos.", "steve", "peggy"),
        L(e_grupo(["cap_martillo", "panther_pie", "reed_estira", "magneto_pie"], "LA MAYOR REUNIÓN", "azul", ORO), "Contra él se juntan los Vengadores, Wakanda, los Nuevos Avengers, los Cuatro Fantásticos y los X-Men originales.", "vengadores", "x-men"),
        L(e_foto(14, "doom_libro", "EL JUEZ", mov=0), "Por primera vez, el villano no llega a destruir a los héroes… llega a juzgarlos.", "juzgarlos"),
        L(e_impacto("TEORÍA", ORO, "mistico"), "Y ojo, esto es teoría: algunos creen que Doom perdió a una hija por culpa de los Vengadores.", "teoría", "hija"),
        L(e_battleworld(chip_txt="¿DIOS EMPERADOR?"), "Otros creen que buscará convertirse en Dios Emperador, como en los cómics.", "emperador"),
        L(e_linea([("DOOMSDAY", "18 DIC 2026", VERDE), ("SECRET WARS", "17 DIC 2027", NARANJA)]), "Doomsday se estrena el dieciocho de diciembre de dos mil veintiséis. Y Secret Wars, el diecisiete de diciembre de dos mil veintisiete.", "doomsday", "secret"),
    ]
    B["cierre"] = [
        L(e_narrador(), "¿Mi opinión? Doom no es un villano cualquiera. Es un hombre que lo perdió todo… y decidió que nadie más le diría qué hacer.", "opinión", "todo"),
        L(e_narrador(), "Lo que más me gusta de Doom es que tiene razones. Perdió a su madre, a su padre, a su pueblo… y su cara.", "razones"),
        L(e_dos("thanos_guante", "doom_magia", "THANOS VS DOOM", "thanos", vs=True), "Thanos quería equilibrio. Doom quiere control. Y eso lo hace todavía más peligroso.", "equilibrio", "control"),
        L(e_narrador(), "Y en vez de rendirse, decidió que el mundo entero tenía que obedecerlo. Para él, eso es salvarlo.", "salvarlo"),
        L(e_narrador(), "Por eso es tan peligroso: él de verdad cree que es el héroe de la historia.", "héroe"),
        L(e_estrellas_t("¿EL MEJOR VILLANO?", 5), "¿Es el mejor villano de Marvel? Para mí, cinco de cinco.", "cinco"),
        L(e_grupo(["doom_libro", "doom_magia", "doom_vuelo"], "COMICS-STORE.COM.CO", "doom", VERDE), "Y si quieres a Doom en tu colección, en Comics Store tenemos varias versiones. Las encuentras en comics store punto com punto co.", "colección"),
        L(e_continuara(), "¿Cómo termina Doom en Doomsday? Eso lo vemos en la parte dos, apenas se estrene. Continuará…", "parte", "continuará"),
        L(e_cta_doom(), "Comenta DOOM si quieres la parte dos, suscríbete y activa la campanita. ¡Nos vemos en el próximo video!", "doom"),
    ]
    return B

FOTO_AMB = {1: "fogata+viento", 2: "tormenta", 3: "chimenea", 4: "infierno", 5: "noche", 6: "maquina", 7: "explosion", 8: "campanas",
            9: "forja", 10: "trueno", 11: "antorchas+magia", 12: "viento+magia", 13: "explosion+cosmos", 14: "cosmos+magia"}
CLAVE_AMB = [("mefisto", "infierno"), ("infierno", "infierno"), ("galactus", "cosmos"), ("silver", "cosmos"), ("incursi", "explosion+cosmos"),
             ("centinelas", "trueno"), ("explota", "explosion"), ("rojo vivo", "forja"), ("nieve", "viento")]

def sonorizar(esc):
    """Ambiente por escena: por foto, por palabra clave del texto o por tipo de escena."""
    for fn, txt, _ in esc:
        if getattr(fn, "amb", None): continue
        low = txt.lower(); a = None
        if getattr(fn, "foto", None): a = FOTO_AMB.get(fn.foto)
        if not a: a = next((v for k, v in CLAVE_AMB if k in low), None)
        if not a: a = {"doom": "magia", "impacto": "impacto+magia", "capitulo": "cosmos", "continuara": "cosmos+magia", "battleworld": "cosmos",
                       "franklin": "cosmos", "centinelas": "trueno", "cta": None, "narrador": None, "estrellas": "magia"}.get(fn.__name__, None)
        if a: fn.amb = a
    return esc

def guion_yt():
    B = bloques(); esc = []
    for k in ("intro", "cap1", "cap2", "cap3", "cap4", "cap5", "cap6", "cierre"): esc += B[k]
    sonorizar(esc)
    re_ = [i for i, e in enumerate(esc) if e[0].__name__ == "narrador" and i > 0]
    return esc, re_

# ---------------------------------------------------------------- shorts (salen del mismo guion)
def _short(gancho, tramo):
    gancho[0].amb = "impacto+magia"
    return [gancho] + tramo + [L(e_cta_doom(youtube=True), "Comenta DOOM, y mira la historia completa en nuestro canal de YouTube.", "doom", "youtube")]

def _tramo(esc, desde, hasta):
    i0 = next(i for i, e in enumerate(esc) if e[1].startswith(desde)); i1 = next(i for i, e in enumerate(esc) if e[1].startswith(hasta))
    return esc[i0:i1 + 1]

def guion_short(n):
    esc, _ = guion_yt()
    if n == 1: return _short(L(e_impacto("UN PACTO CON\nEL DIABLO", ROJO, "rojo", fig="mefisto_trono"), "La madre de Doctor Doom hizo un pacto con el diablo… y así empezó todo.", "diablo"),
                             _tramo(esc, "Pero antes de todo eso", "Vengarse de los que"))
    if n == 2: return _short(L(e_impacto("EL ERROR\nQUE REED VIO", (80, 200, 255), "azul", fig="reed_estira"), "Reed Richards vio el error que creó a Doctor Doom… y nadie lo escuchó.", "error"),
                             _tramo(esc, "Tanto, que una universidad", "La explosión le deja") + _tramo(esc, "Desde ese día, culpa", "Desde ese día, culpa"))
    if n == 3: return _short(L(e_impacto("SE LA PUSO\nAL ROJO VIVO", (255, 90, 30), "rojo", fig="doom_pie3"), "Doctor Doom se puso su máscara todavía al rojo vivo. Esta es la razón.", "rojo"),
                             _tramo(esc, "Y aquí hay un detalle", "Lo que de verdad") + _tramo(esc, "Víctor viajó por el mundo", "Derrocó al rey"))
    if n == 4: return _short(L(e_impacto("DOOM FUE\nIRON MAN", ORO, "rojo", fig="iron_mk42"), "¿Sabías que Doctor Doom fue Iron Man?", "iron"),
                             _tramo(esc, "Y lo más loco", "Doom fue Iron Man en los cómics") + _tramo(esc, "En dos mil veinticuatro, en la Comic-Con", "Su primera aparición fue en la escena"))

if __name__ == "__main__":
    v = sys.argv[1]; out = sys.argv[2]
    if v == "final": esc, re_ = [(e_pantalla_final(), "Te dejo aquí otro video que te va a encantar. Y si todavía no lo has hecho, suscríbete. ¡Nos vemos en el próximo video!", {"suscríbete"})], None
    elif v == "yt": esc, re_ = guion_yt()
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
