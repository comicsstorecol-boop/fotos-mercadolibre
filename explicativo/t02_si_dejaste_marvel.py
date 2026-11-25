"""Comics Store · "Si dejaste Marvel después de Endgame, te lo explico" — tt / fb / yt / final.
Uso: python3 t02_si_dejaste_marvel.py tt|fb|yt|final salida.mp4   (yt y final con FORMATO=horizontal)"""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from teoria_figuras import *
from motor import render

PRON = {"strange": ("en", "Strange"), "doom": ("en", "Doom"), "thanos": ("es", "tános"), "endgame": ("es", "éndgueim"), "tony": ("es", "tóni"),
        "stark": ("es", "estárk"), "steve": ("es", "estív"), "rogers": ("es", "róyers"), "loki": ("es", "lóqui"), "thor": ("es", "tor"),
        "hulk": ("es", "jalk"), "wanda": ("es", "uánda"), "reed": ("es", "rid"), "richards": ("es", "ríchards"), "sue": ("es", "sú"),
        "franklin": ("es", "fránklin"), "robert": ("es", "róbert"), "downey": ("es", "dáuni"), "junior": ("es", "yúnior"), "wolverine": ("es", "guolverín"),
        "magneto": ("es", "magnéto"), "xavier": ("es", "xávier"), "deadpool": ("es", "dédpul"), "thunderbolts": ("es", "tánderbolts"),
        "doomsday": ("es", "dúmsdei"), "secret": ("es", "sícret"), "wars": ("es", "uors"), "love": ("es", "lov"), "sam": ("es", "sam"),
        "wilson": ("es", "uílson"), "avengers": ("es", "avényers"), "x-men": ("es", "équis men"), "comics": ("en", "Comics"), "youtube": ("es", "yutub"),
        "mckellen": ("es", "mackélen"), "patrick": ("es", "pátrik"), "stewart": ("es", "estiúart"), "pedro": ("es", "pedro"), "pascal": ("es", "pascál"),
        "tesseract": ("es", "téseract"), "wakanda": ("es", "uakánda"), "vormir": ("es", "vórmir"), "natasha": ("es", "natasha"), "sylvie": ("es", "sílvi"), "romijn": ("es", "romín"), "rebecca": ("es", "rebeca"), "mystique": ("es", "místic"), "latveria": ("es", "latvéria"), "evans": ("es", "évans"), "chris": ("es", "cris"), "battleworld": ("es", "bátoluorld")}
COLORES = (VERDE, (80, 200, 255))   # subtítulos: verde Doom + azul multiverso
FH = P(1180, 760); PISO = P(1760, 890)

# ---------------------------------------------------------------- escenas genéricas
def h_fit(fig, h, maxw):
    """Alto de la figura sin pasarse del ancho disponible (poses abiertas)."""
    im = Image.open(os.path.join(FIG_DIR, fig + ".png")); return min(h, maxw * im.height / im.width)

def e_narrador(titulo=None, sub=None, col=VERDE):
    return S("narrador", narrador_escena(titulo, col, sub))

def e_fig(fig, chip_txt=None, pal="mistico", entra="pop", mandala_on=True, z=(1.1, 1.0), sacude=False, efecto=None):
    def f(t, d):
        col = color_de(fig); c = cosmos(t, pal)
        if mandala_on: mandala(c, W / 2, P(950, 520), P(430, 360), t, col, .4)
        if efecto == "hilos": hilos(c, W / 2, P(700, 300), t, col, n=30, abanico=(200, 340))
        figura(c, fig, W / 2, PISO, FH, t, entra)
        particulas(c, t, col, n=30)
        if chip_txt: chip(c, chip_txt, W / 2, P(1840, 1010), col, P(46, 44), eo(pr(t, .5, .3)))
        flash(c, t, .15); c = zoom(c, t, d, *z)
        return shake(c, t, 14) if sacude else c
    return S("fig", f)

def e_dos(a, b, chip_txt=None, pal="mistico", vs=False, chip_col=None):
    def f(t, d):
        c = cosmos(t, pal)
        mw = P(W * .5, W * .4)
        figura(c, a, P(W * .28, W * .3), PISO, h_fit(a, FH * .9, mw), t, "izq")
        figura(c, b, P(W * .73, W * .7), PISO, h_fit(b, FH * .9, mw), t, "der", retraso=.15)
        if vs: texto(c, "VS", W / 2, P(760, 450), P(150, 150), (255, 255, 255), alpha=eo(pr(t, .3, .3)), glow_col=color_de(b)); rayos_velocidad(c, t, color_de(a))
        if chip_txt: chip(c, chip_txt, W / 2, P(1840, 1010), chip_col or color_de(a), P(44, 42), eo(pr(t, .6, .3)))
        return zoom(c, t, d, 1.0, 1.07)
    return S("dos", f)

def e_grupo(figs, chip_txt=None, pal="azul", chip_col=VERDE, alto=None):
    def f(t, d):
        c = cosmos(t, pal); n = len(figs); h = alto or P(700 if n <= 2 else 620, 620)
        m = P(.2, .2) if n > 2 else P(.27, .3); mw = W * (1 - 2 * m) / max(1, n - 1) * 1.15 if n > 1 else W * .8
        for i, fg in enumerate(figs):
            x = W * (m + (1 - 2 * m) * i / max(1, n - 1)) if n > 1 else W / 2
            hh = h_fit(fg, h * (1 if i % 2 == 0 else .92), mw)
            figura(c, fg, x, PISO - (0 if i % 2 == 0 else P(60, 40)), hh, t, "sube", retraso=i * .12)
        if chip_txt: chip(c, chip_txt, W / 2, P(560, 1010), chip_col, P(44, 42), eo(pr(t, .7, .3)))
        return zoom(c, t, d, 1.0, 1.06)
    return S("grupo", f)

def e_loki_hilos(fig="loki_brazos", chip_txt="SOSTIENE EL MULTIVERSO"):
    def f(t, d):
        c = cosmos(t, "mistico"); col = color_de(fig)
        cx = W / 2; manos_y = P(1050, 520)
        hilos(c, cx - P(300, 260), manos_y, t, col, n=22, abanico=(200, 290), seed=4)
        hilos(c, cx + P(300, 260), manos_y, t, col, n=22, abanico=(250, 340), seed=9)
        figura(c, fig, cx, PISO, FH, t, "pop", flota=False)
        chip(c, chip_txt, W / 2, P(1840, 1010), col, P(44, 42), eo(pr(t, .6, .3)))
        return zoom(c, t, d, 1.06, 1.0)
    return S("loki_hilos", f)

def e_universos(etiquetas=("TIERRA 616", "TIERRA 828", "X-MEN"), figs=("cap_sincasco", "reed_estira", "wolverine_pie")):
    def f(t, d):
        c = cosmos(t, "azul"); n = len(etiquetas)
        for i, (et, fg) in enumerate(zip(etiquetas, figs)):
            x = P(W * (.22 + .28 * i), W * (.2 + .3 * i)); y = P(1250 + (i % 2) * 200, 680); r = P(170, 160)
            u = pr(t, .2 + i * .35, .5)
            if u <= 0: continue
            planeta(c, x, y, r, t + i * 3, color_de(fg), eo(u))
            figura(c, fg, x, y - r * .7, P(420, 360), t, "baja", retraso=.3 + i * .35, reflejo=False)
            chip(c, et, x, y + r + P(70, 60), color_de(fg), P(34, 32), eo(pr(t, .5 + i * .35, .3)))
        return zoom(c, t, d, 1.0, 1.05)
    return S("universos", f)

def e_incursion(chip_txt="INCURSIÓN"):
    def f(t, d):
        c = cosmos(t, "rojo"); u = eio(pr(t, .2, max(.5, d - .8)))
        x1 = P(W * .2, W * .25) + u * P(W * .22, W * .2); x2 = P(W * .8, W * .75) - u * P(W * .22, W * .2)
        planeta(c, x1, P(900, 500), P(220, 200), t, AZUL); planeta(c, x2, P(950, 520), P(220, 200), t * 1.3 + 2, ROJO)
        if u > .95: flash(c, t - (.2 + .95 * max(.5, d - .8)), .3, (255, 240, 220), 230)
        chip(c, chip_txt, W / 2, P(1500, 900), ROJO, alpha=eo(pr(t, .4, .3)))
        return shake(c, max(0, t - d + .6), 18, .6)
    return S("incursion", f)

def e_doom(fig="doom_brazos", chip_txt=None, entra="sube", pal="doom"):
    def f(t, d):
        c = cosmos(t, pal); glow(c, W / 2, P(900, 500), P(520, 420), VERDE, 110 + int(40 * math.sin(t * 5)))
        mandala(c, W / 2, P(950, 500), P(470, 380), t, VERDE, .55)
        figura(c, fig, W / 2, PISO, FH, t, entra); particulas(c, t, VERDE, n=40)
        if chip_txt: chip(c, chip_txt, W / 2, P(1840, 1010), VERDE, alpha=eo(pr(t, .6, .3)))
        return glitch(shake(zoom(c, t, d, 1.12, 1.0), t, 18), t)
    return S("doom", f)

def e_franklin():
    def f(t, d):
        c = cosmos(t, "azul")
        figura(c, "doom_metal", P(W * .3, W * .28), PISO, FH * .9, t, "izq")
        x, y = P(W * .72, W * .68), P(1000, 520); r = P(110, 100) * (1 + .08 * math.sin(t * 4))
        glow(c, x, y, r * 3, (120, 200, 255), 150); glow(c, x, y, r * 1.6, (255, 255, 255), 180)
        for k in range(3):
            rr = r * (1.4 + k * .6 + (t * .6 % .6)); ImageDraw.Draw(c).ellipse((x - rr, y - rr, x + rr, y + rr), outline=(150, 220, 255, int(160 - k * 45)), width=4)
        chip(c, "FRANKLIN RICHARDS", x, y + P(260, 230), (120, 200, 255), P(38, 36), eo(pr(t, .5, .3)))
        hilos(c, x, y, t, (120, 200, 255), n=16, abanico=(0, 360), largo=P(500, 450), a=120)
        return zoom(c, t, d, 1.0, 1.08)
    return S("franklin", f)

def e_centinelas():
    def f(t, d):
        c = cosmos(t, "rojo"); dr = ImageDraw.Draw(c); rng = random.Random(5)
        for fila in range(4):
            for k in range(9):
                x = W * (k + .5 + (fila % 2) * .5) / 9; y = P(820, 420) + fila * P(150, 110); s = P(46, 40) * (1 + fila * .25)
                u = pr(t, .2 + fila * .25 + k * .03, .4)
                if u <= 0: continue
                a = int(230 * u * (.6 + .4 * math.sin(t * 6 + k + fila)))
                dr.polygon([(x - s, y), (x - s * .3, y - s * .25), (x - s * .1, y)], fill=(255, 40, 40, a)); dr.polygon([(x + s, y), (x + s * .3, y - s * .25), (x + s * .1, y)], fill=(255, 40, 40, a))
                glow(c, x, y, s * .9, ROJO, int(70 * u))
        figura(c, "doom_brazos", W / 2, PISO, FH * .95, t, "sube")
        chip(c, "EJÉRCITO DE CENTINELAS", W / 2, P(560, 1010), ROJO, P(42, 40), eo(pr(t, .6, .3)))
        return shake(zoom(c, t, d, 1.0, 1.06), t, 12)
    return S("centinelas", f)

def e_impacto(txt, col=VERDE, pal="doom", sub=None, fig=None):
    def f(t, d):
        c = cosmos(t, pal, velocidad=2); mandala(c, W / 2, P(900, 470), P(460, 400), t, col, .35); particulas(c, t, col, n=35)
        if fig: figura(c, fig, W / 2, PISO + P(200, 160), FH, t, "sube", alpha=.55)
        rayos_velocidad(c, t, col, .7); lineas = txt.split("\n")
        for i, ln in enumerate(lineas):
            k = eb(pr(t, .05 + i * .15, .4)); texto(c, ln, W / 2, P(900, 470) + (i - (len(lineas) - 1) / 2) * P(170, 150), int(P(130, 128) * max(.05, k)), (255, 255, 255), glow_col=col, stroke=8)
        if sub: chip(c, sub, W / 2, P(1300, 800), col, P(44, 44), eo(pr(t, .6, .4)))
        flash(c, t, .2, col, 150); return shake(c, t, 16)
    return S("impacto", f)

def e_capitulo(n, titulo, col=VERDE, pal="mistico"):
    def f(t, d):
        c = cosmos(t, pal, velocidad=2); glow(c, W / 2, H / 2, P(500, 420), col, 90); mandala(c, W / 2, H / 2, P(380, 340), t, col, .5)
        texto(c, f"CAPÍTULO {n}", W / 2, H / 2 - P(90, 80), P(64, 60), col, alpha=eo(pr(t, .1, .3)))
        texto(c, titulo, W / 2 + (1 - eo(pr(t, .25, .5))) * W, H / 2 + P(40, 40), P(92, 96), (255, 255, 255), glow_col=col)
        rayos_velocidad(c, t, col, .5); flash(c, t, .15, col); return c
    return S("capitulo", f)

def e_portada():
    def f(t, d):
        c = cosmos(t, "mistico", velocidad=1.5); hilos(c, W / 2, P(600, 260), t, VERDE, n=26)
        figura(c, "iron_clasico", P(W * .22, W * .2), PISO, P(820, 680), t, "izq")
        figura(c, "doom_metal", W / 2, PISO, P(1000, 800), t, "sube", retraso=.1)
        figura(c, "loki_brazos", P(W * .8, W * .8), PISO, P(820, 680), t, "der", retraso=.2)
        texto(c, "SI DEJASTE MARVEL", W / 2, P(470, 150), P(96, 100), (255, 255, 255), alpha=eo(pr(t, .4, .3)), glow_col=VERDE)
        texto(c, "DESPUÉS DE ENDGAME", W / 2, P(590, 260), P(76, 80), VERDE, alpha=eo(pr(t, .6, .3)), glow_col=VERDE)
        flash(c, t); return zoom(c, t, d, 1.06, 1.0)
    return S("portada", f)

def e_spoilers():
    def f(t, d):
        c = cosmos(t, "rojo"); k = eb(pr(t, .1, .5))
        texto(c, "!", W / 2, P(780, 380), int(P(300, 240) * max(.05, k)), ORO, glow_col=ROJO, stroke=10)
        texto(c, "SPOILERS", W / 2, P(1060, 600), P(130, 120), (255, 255, 255), alpha=eo(pr(t, .3, .3)), glow_col=ROJO)
        for i, s_ in enumerate(["ENDGAME", "LOKI", "LOS 4 FANTÁSTICOS"]):
            chip(c, s_, W / 2 + P(0, (i - 1) * 480), P(1260 + i * 120, 790), ORO, P(40, 36), eo(pr(t, .6 + i * .2, .3)))
        return shake(c, t, 10)
    return S("spoilers", f)

def e_linea(items):
    def f(t, d):
        c = cosmos(t, "mistico")
        if not HZ: figura(c, "doom_metal", W / 2, 1880, 700, t, "sube", alpha=.55, reflejo=False)
        linea_tiempo(c, t, items); return zoom(c, t, d, 1.0, 1.05)
    return S("linea", f)

def e_estrellas(nota=5):
    def f(t, d):
        c = cosmos(t, "mistico"); texto(c, "¿VALE LA PENA VOLVER?", W / 2, P(620, 300), P(64, 66), (255, 255, 255), glow_col=VERDE)
        estrellas(c, t, nota, W / 2, P(900, 520)); texto(c, f"{nota} / 5", W / 2, P(1120, 700), P(90, 84), ORO, alpha=eo(pr(t, 1.5, .3)), glow_col=ORO)
        return zoom(c, t, d, 1.0, 1.05)
    return S("estrellas", f)

def e_cta(youtube=False):
    def f(t, d):
        c = cosmos(t, "doom")
        figura(c, "loki_brazos", P(W * .3, W * .14), P(1180, 880), P(620, 560), t, "izq", reflejo=False)
        figura(c, "doom_brazos", P(W * .72, W * .34), P(1180, 880), P(680, 620), t, "der", reflejo=False, retraso=.1)
        caja_comentario(c, t, "RESUMEN", x=P(W / 2, W * .7), y=P(1320, 400))
        if youtube: chip(c, "EXPLICACIÓN COMPLETA EN YOUTUBE", W / 2, P(1560, 900), ROJO, P(40, 38), eo(pr(t, 1.6, .3)), (40, 6, 10))
        barra_suscribir(c, t, x=P(W / 2, W * .7), y=P(1740, 600), inicio=2.0 if youtube else 1.4)
        return c
    return S("cta", f)

def e_pantalla_final():
    def f(t, d):
        c = cosmos(t, "doom", velocidad=.6); m = lib.marca("comics-store")
        lg = m["logo"].resize((P(520, 360), P(540, 374)), Image.LANCZOS); place(c, lg, P(W / 2, W * .5), P(560, 230), scale=eb(pr(t, .1, .5)), rot=math.sin(t * 2) * 2)
        for i, x in enumerate((P(W * .27, W * .3), P(W * .73, W * .7))):
            u = eo(pr(t, .4 + i * .2, .4)); bw, bh = P(440, 640), P(250, 360)
            L = Image.new("RGBA", (bw, bh), (0, 0, 0, 0)); dd = ImageDraw.Draw(L); dd.rounded_rectangle((3, 3, bw - 4, bh - 4), 24, fill=(10, 12, 20, 200), outline=(VERDE if i == 0 else NARANJA) + (255,), width=5)
            dd.text((bw / 2, bh / 2), "SIGUIENTE VIDEO" if i == 0 else "SUSCRÍBETE", font=F(P(34, 40)), fill=(255, 255, 255, 255), anchor="mm")
            place(c, L, x, P(1100, 640), alpha=u)
        particulas(c, t, VERDE, n=30); return c
    return S("pantalla_final", f)

TL4 = [("ENDGAME", "2019"), ("LOKI", "2021-23"), ("4 FANTÁSTICOS", "2025", (80, 200, 255)), ("DOOMSDAY", "18 DIC 2026", VERDE)]

# ---------------------------------------------------------------- guiones
def guion_tt():
    return [
        (e_doom(chip_txt="TE LO EXPLICO"), "Si dejaste Marvel después de Endgame… te explico todo en un minuto.", {"endgame", "minuto"}),
        (e_dos("iron_clasico", "cap_sincasco", "ENDGAME", "azul", chip_col=ORO), "Tony murió. Y Steve se quedó a vivir en el pasado.", {"tony", "murió", "steve"}),
        (e_fig("loki_cubo", "UNA NUEVA RAMA", "mistico"), "Pero Loki escapó con el teseracto… y rompió la línea del tiempo.", {"loki", "rompió"}),
        (e_loki_hilos(), "Hoy él solo sostiene el multiverso, como si fueran hilos en sus manos.", {"multiverso", "manos"}),
        (e_universos(), "Cada hilo es un universo: el nuestro, el de los Cuatro Fantásticos… y el de los X-Men.", {"universo", "x-men"}),
        (e_incursion(), "Y cuando dos universos chocan, uno destruye al otro. Eso se llama incursión.", {"destruye", "incursión"}),
        (e_fig("wanda_pie", "MULTIVERSO DE LA LOCURA", "rojo"), "Ya lo vimos cuando Wanda cruzó universos buscando a sus hijos.", {"wanda", "hijos"}),
        (e_narrador(), "En medio de ese caos llega Doctor Doom… con la cara de Robert Downey Junior.", {"doom", "downey"}),
        (e_franklin(), "Ya apareció en Los Cuatro Fantásticos, interesado en Franklin, el hijo de Reed y Sue.", {"franklin"}),
        (e_dos("reed_estira", "doom_trono", "HISTORIA CON DOOM", "azul", chip_col=(80, 200, 255)), "Y Sue cuenta que Doom antes era bondadoso. Tiene historia con ellos.", {"bondadoso"}),
        (e_centinelas(), "Y en el último tráiler levanta un ejército de Centinelas.", {"centinelas"}),
        (e_dos("thor_hacha", "cap_sincasco", "VUELVEN", "azul", chip_col=(120, 200, 255)), "Thor lo enfrenta… y Steve Rogers vuelve.", {"thor", "steve"}),
        (e_grupo(["xavier_silla", "magneto_pie", "wolverine_pie"], "X-MEN ORIGINALES", "mistico", (235, 60, 200)), "Y los X-Men originales llegan desde otro universo.", {"x-men"}),
        (e_grupo(["cap_martillo", "reed_estira", "wolverine_garras"], "3 UNIVERSOS · 1 ENEMIGO"), "Tres universos. Un solo enemigo. Doomsday llega el dieciocho de diciembre.", {"tres", "doomsday"}),
        (e_cta(youtube=True), "Comenta RESUMEN, y mira la explicación completa en nuestro canal de YouTube.", {"resumen", "youtube"}),
    ], [7, 11]

def guion_fb():
    return [
        (e_doom(chip_txt="TE LO EXPLICO"), "Si dejaste Marvel después de Endgame… te explico todo lo que pasó.", {"endgame"}),
        (e_fig("hulk_puno", "EL REGRESO", "doom"), "En Endgame, Hulk chasquea los dedos y regresa a la mitad del universo.", {"hulk", "mitad"}),
        (e_dos("iron_clasico", "cap_sincasco", "ENDGAME", "azul", chip_col=ORO), "Tony murió con el guantelete. Y Steve le dejó el escudo a Sam y se quedó a vivir en el pasado.", {"tony", "steve"}),
        (e_fig("thor_gordo", "SE VA AL ESPACIO", "azul"), "Y Thor se va al espacio con los Guardianes de la Galaxia.", {"thor", "guardianes"}),
        (e_fig("loki_cubo", "UNA NUEVA RAMA", "mistico"), "Pero en ese viaje en el tiempo, Loki escapó con el teseracto.", {"loki", "teseracto"}),
        (e_loki_hilos(), "Esa fuga terminó rompiendo la línea del tiempo. Hoy Loki sostiene el multiverso él solo, como hilos en sus manos.", {"multiverso", "manos"}),
        (e_universos(), "Cada hilo es un universo: el nuestro, el de los Cuatro Fantásticos, y el de los X-Men de siempre.", {"universo", "x-men"}),
        (e_incursion(), "Cuando dos universos chocan, uno destruye al otro. Se llama incursión.", {"incursión"}),
        (e_fig("wanda_pie", "MULTIVERSO DE LA LOCURA", "rojo"), "Ya lo vimos en el Multiverso de la Locura, cuando Wanda cruzó universos buscando a sus hijos.", {"wanda", "universos"}),
        (e_fig("strange_portal", "UNA INCURSIÓN", "mistico"), "Y a Strange le dicen que él mismo provocó una incursión.", {"strange", "incursión"}),
        (e_narrador(), "Quédate, porque ahora viene el que lo cambia todo.", {"cambia"}),
        (e_doom("doom_metal", "ROBERT DOWNEY JR."), "Doctor Doom… y lo interpreta Robert Downey Junior.", {"doom", "downey"}),
        (e_franklin(), "Ya apareció al final de Los Cuatro Fantásticos, interesado en Franklin, el hijo de Reed y Sue.", {"franklin"}),
        (e_dos("reed_estira", "doom_trono", "HISTORIA CON DOOM", "azul", chip_col=(80, 200, 255)), "Y Sue cuenta que Doom antes era bondadoso y generoso. Tiene historia con ella y con Reed.", {"bondadoso", "generoso"}),
        (e_centinelas(), "En el último tráiler, Doom levanta un ejército de Centinelas.", {"centinelas"}),
        (e_grupo(["thor_hacha", "cap_sincasco", "cosa_pie"], "TIERRA 616", "azul", (120, 200, 255)), "De un lado: los Avengers, Wakanda y los Nuevos Avengers, de la Tierra seiscientos dieciséis.", {"avengers", "seiscientos"}),
        (e_grupo(["reed_estira", "cosa_pie"], "TIERRA 828", "azul", (80, 200, 255)), "Los Cuatro Fantásticos, de la Tierra ochocientos veintiocho.", {"ochocientos"}),
        (e_grupo(["xavier_silla", "magneto_pie", "wolverine_pie"], "OTRO UNIVERSO", "mistico", (235, 60, 200)), "Y los X-Men originales, de otro universo.", {"x-men", "originales"}),
        (e_dos("magneto_cerca", "xavier_silla", "MCKELLEN · STEWART", "mistico", chip_col=(235, 60, 200)), "Con Ian McKellen como Magneto, y Patrick Stewart como el Profesor Xavier.", {"magneto", "xavier"}),
        (e_dos("wolverine_garras", "cap_pelea", "¿ALIADOS O RIVALES?", "rojo", vs=True), "Pero ojo: al principio podrían pelear entre ellos. Si un universo sobrevive, otro puede desaparecer.", {"pelear", "desaparecer"}),
        (e_dos("thor_hacha", "cap_sincasco", "PADRES", "azul", chip_col=(120, 200, 255)), "Y varios pelean por sus hijos: Thor con su hija Love, y Steve, que ahora también es papá.", {"love", "papá"}),
        (e_linea(TL4), "Doomsday llega a cines el dieciocho de diciembre.", {"doomsday", "dieciocho"}),
        (e_impacto("MENOS DE\n4 SEMANAS", VERDE, "doom", fig="doom_metal"), "Faltan menos de cuatro semanas.", {"cuatro", "semanas"}),
        (e_impacto("¿ESTÁS\nLISTO?", VERDE, "doom", fig="doom_brazos"), "¿Ya estás listo para volver?", {"listo"}),
        (e_cta(youtube=True), "Comenta RESUMEN, y mira la explicación completa en nuestro canal de YouTube.", {"resumen", "youtube"}),
    ], [2, 10, 20]

def guion_yt():
    return [
        (e_narrador(), INTRO_GAMER[0], INTRO_GAMER[1]),
        (e_doom(chip_txt="TE LO EXPLICO"), "Si dejaste Marvel después de Endgame, y hoy no entiendes nada… este video es para ti.", {"endgame", "ti"}),
        (e_portada(), "Te explico todo lo que pasó, y por qué Doctor Doom lo cambia todo.", {"doom"}),
        (e_spoilers(), "Aviso: hay spoilers de Endgame, de la serie de Loki y de Los Cuatro Fantásticos.", {"spoilers"}),
        (e_grupo(["iron_clasico", "loki_brazos", "thor_clasico", "hulk_pie"], "FIGURAS DE COMICS STORE", "mistico", VERDE), "Y ojo: todas las figuras que vas a ver son de nuestra tienda, Comics Store.", {"figuras", "comics", "store"}),
        (e_capitulo(1, "LO QUE DEJÓ ENDGAME", ORO, "azul"), "Capítulo uno. Lo que dejó Endgame.", {"endgame"}),
        (e_fig("thanos_frente", "EL CHASQUIDO", "thanos", sacude=True), "En Infinity War, Thanos borró a la mitad de la vida con un chasquido.", {"mitad", "chasquido"}),
        (e_impacto("5 AÑOS\nDESPUÉS", ORO, "azul", fig="iron_vuelo"), "Cinco años después, los Vengadores viajan en el tiempo para recuperar las gemas.", {"cinco", "gemas"}),
        (e_impacto("VORMIR", ROJO, "rojo"), "Natasha da su vida en Vormir para conseguir la gema del alma.", {"natasha", "vida"}),
        (e_fig("hulk_puno", "EL REGRESO", "doom"), "En Endgame, Hulk chasquea los dedos y regresa a la mitad del universo que Thanos había borrado.", {"hulk", "mitad"}),
        (e_fig("thanos_guante", "DERROTADO", "thanos"), "Thanos vuelve para la batalla final… y pierde.", {"thanos", "pierde"}),
        (e_fig("iron_clasico", "“YO SOY IRON MAN”", "rojo"), "Tony Stark usa las gemas para acabar con él. Y muere salvando a todos.", {"tony", "muere"}),
        (e_fig("cap_saludo", "EL ESCUDO PARA SAM", "azul", z=(1.0, 1.08)), "Steve devuelve las gemas, se queda a vivir en el pasado, y le deja el escudo a Sam Wilson.", {"steve", "sam"}),
        (e_fig("thor_gordo", "SE VA AL ESPACIO", "azul"), "Y Thor se va al espacio con los Guardianes de la Galaxia.", {"thor", "guardianes"}),
        (e_narrador(), "Pero en medio de todo eso pasó algo que casi nadie vio venir.", {"nadie"}),
        (e_capitulo(2, "LOKI Y EL MULTIVERSO", (170, 255, 60), "mistico"), "Capítulo dos. Loki y el multiverso.", {"loki", "multiverso"}),
        (e_fig("loki_cubo", "UNA NUEVA RAMA", "mistico"), "Cuando los Vengadores viajan al dos mil doce, Loki se roba el teseracto y escapa.", {"loki", "teseracto"}),
        (e_fig("loki_casco", "LA TVA", "mistico", efecto="hilos"), "Esa fuga crea una rama nueva en la línea del tiempo, y una agencia llamada la TVA lo atrapa.", {"rama", "tva"}),
        (e_fig("loki_lanza", "LA LÍNEA SAGRADA", "mistico", efecto="hilos"), "La TVA cuida una sola línea del tiempo, la Línea Sagrada, y borra cualquier rama que se salga.", {"sagrada", "borra"}),
        (e_impacto("AQUEL QUE\nPERMANECE", (170, 255, 60), "mistico"), "Detrás de todo estaba Aquel que Permanece, un hombre que controlaba el tiempo.", {"permanece", "tiempo"}),
        (e_fig("loki_casco", "SYLVIE", "rojo", sacude=True), "Pero Sylvie, otra variante de Loki, lo mata… y el multiverso queda libre.", {"sylvie", "libre"}),
        (e_impacto("EL MULTIVERSO\nSE ABRE", (170, 255, 60), "mistico"), "En su serie, todo se sale de control. El tiempo se divide en ramas infinitas.", {"infinitas"}),
        (e_loki_hilos(), "Al final, Loki se sienta en un trono al final del tiempo, sosteniendo cada rama con sus manos.", {"trono", "manos"}),
        (e_fig("loki_lanza", "DIOS DE LAS HISTORIAS", "mistico"), "Ya no es el dios del engaño. Es quien mantiene vivo el multiverso.", {"multiverso"}),
        (e_universos(), "Y cada una de esas ramas es un universo distinto: el nuestro, el de los Cuatro Fantásticos, el de los X-Men.", {"universo", "x-men"}),
        (e_incursion(), "El problema: cuando dos universos chocan, uno destruye al otro. Se llama incursión.", {"incursión"}),
        (e_fig("wanda_cerca", "MULTIVERSO DE LA LOCURA", "rojo", z=(1.0, 1.08)), "Ya lo vimos en el Multiverso de la Locura, cuando Wanda cruzó universos buscando a sus hijos.", {"wanda", "hijos"}),
        (e_fig("strange_portal", "UNA INCURSIÓN", "mistico"), "Y en esa misma película, a Strange le dicen que provocó una incursión.", {"strange", "incursión"}),
        (e_narrador(), "Ahora, ¿quién puede aprovechar todo ese caos? Aquí entra él.", {"caos"}),
        (e_capitulo(3, "LOS NUEVOS JUGADORES", (80, 200, 255), "azul"), "Capítulo tres. Los nuevos jugadores.", {"jugadores"}),
        (e_grupo(["reed_estira", "cosa_pie"], "TIERRA 828", "azul", (80, 200, 255)), "Los Cuatro Fantásticos llegaron en dos mil veinticinco, desde otro universo: la Tierra ochocientos veintiocho.", {"ochocientos"}),
        (e_fig("reed_estira", "PEDRO PASCAL", "azul"), "Reed Richards lo interpreta Pedro Pascal.", {"reed", "pascal"}),
        (e_grupo(["xavier_silla", "magneto_pie", "wolverine_pie"], "X-MEN ORIGINALES", "mistico", (235, 60, 200)), "Los X-Men originales también vuelven, con caras que conoces desde hace más de veinte años.", {"x-men", "veinte"}),
        (e_fig("magneto_vuelo", "MYSTIQUE VUELVE", "mistico"), "Hasta Rebecca Romijn vuelve como Mystique, el mismo papel que hizo en el año dos mil.", {"mystique", "dos"}),
        (e_dos("magneto_cerca", "xavier_silla", "MCKELLEN · STEWART", "mistico", chip_col=(235, 60, 200)), "Ian McKellen como Magneto. Patrick Stewart como el Profesor Xavier.", {"magneto", "xavier"}),
        (e_fig("wolverine_garras", "DEADPOOL Y WOLVERINE", "rojo", sacude=True), "Y los mutantes ya habían tocado la puerta: Wolverine apareció con Deadpool en dos mil veinticuatro.", {"wolverine", "deadpool"}),
        (e_grupo(["thor_hacha", "cap_sincasco", "hulk_pie"], "TIERRA 616", "azul", (120, 200, 255)), "Y en nuestro universo: los Avengers, Wakanda, y los Nuevos Avengers.", {"avengers", "wakanda"}),
        (e_grupo(["cap_corre", "thor_mjolnir", "hulk_roca"], "NUEVOS AVENGERS", "azul", (120, 200, 255)), "Los Thunderbolts terminaron su película presentados como los Nuevos Avengers.", {"thunderbolts", "nuevos"}),
        (e_grupo(["reed_estira", "cosa_pie"], "ESCENA POSCRÉDITOS", "azul", (80, 200, 255)), "Y en su escena poscréditos, la nave de los Cuatro Fantásticos llega a nuestro universo.", {"nave", "universo"}),
        (e_narrador(), "Y todos tienen un enemigo en común.", {"enemigo"}),
        (e_capitulo(4, "QUIÉN ES ESTE DOOM", VERDE, "doom"), "Capítulo cuatro. Quién es este Doom.", {"doom"}),
        (e_doom("doom_metal", "ROBERT DOWNEY JR."), "Doctor Doom llega al cine con la cara de Robert Downey Junior. Sí, el mismo Tony Stark.", {"downey", "stark"}),
        (e_dos("doom_trono", "reed_estira", "DOOM VS REED", "doom", vs=True), "En los cómics, Doom es el gran rival de Reed Richards. Lo odia desde siempre.", {"rival", "reed"}),
        (e_doom("doom_trono", "LATVERIA", "baja"), "Gobierna su propio país, Latveria, y mezcla la ciencia con la magia.", {"latveria", "magia"}),
        (e_franklin(), "Su primera aparición fue al final de Los Cuatro Fantásticos: interesado en Franklin, el hijo de Reed y Sue.", {"franklin"}),
        (e_dos("reed_estira", "doom_trono", "HISTORIA CON DOOM", "azul", chip_col=(80, 200, 255)), "En el tráiler, Sue cuenta que Doom antes era bondadoso y generoso. Tiene historia con ella y con Reed.", {"bondadoso", "generoso"}),
        (e_impacto("LE QUITARON\nTODO", VERDE, "doom", fig="doom_metal"), "Y que a Doom le quitaron todo lo que amaba.", {"todo", "amaba"}),
        (e_centinelas(), "Y Doom levanta un ejército de Centinelas, los robots de los X-Men.", {"centinelas"}),
        (e_dos("thor_hacha", "doom_brazos", "THOR VS DOOM", "doom", vs=True), "Thor se le enfrenta… y Doom lo lanza a un lado con su magia.", {"thor", "magia"}),
        (e_dos("wolverine_garras", "cap_pelea", "¿ALIADOS O RIVALES?", "rojo", vs=True), "Y los equipos podrían pelear entre ellos: si un universo sobrevive, otro puede desaparecer.", {"pelear", "desaparecer"}),
        (e_dos("thor_cerca", "cap_sincasco", "PADRES", "azul", chip_col=(120, 200, 255)), "Además, varios pelean por sus hijos: Thor con su hija Love, y Steve Rogers, que vuelve y ahora también es papá.", {"love", "papá"}),
        (e_narrador(), "Y si miras las fechas, ya casi está aquí.", {"fechas"}),
        (e_capitulo(5, "LO QUE VIENE", NARANJA, "mistico"), "Capítulo cinco. Lo que viene.", {"viene"}),
        (e_linea(TL4), "Avengers: Doomsday se estrena el dieciocho de diciembre de dos mil veintiséis.", {"doomsday", "dieciocho"}),
        (e_linea([("DOOMSDAY", "18 DIC 2026", VERDE), ("SECRET WARS", "17 DIC 2027", NARANJA)]), "Y después llega Secret Wars, el diecisiete de diciembre de dos mil veintisiete.", {"secret", "wars"}),
        (e_fig("doom_trono", "BATTLEWORLD", "doom"), "En los cómics, cuando el multiverso se destruye, Doom junta los restos en un solo planeta: Battleworld.", {"battleworld"}),
        (e_grupo(["cap_martillo", "iron_salto", "thor_martillos"], "PRIMERA DESDE ENDGAME", "azul", ORO), "Doomsday es la primera película de los Avengers desde Endgame.", {"primera", "endgame"}),
        (e_fig("cap_sincasco", "CHRIS EVANS VUELVE", "azul"), "Y Chris Evans vuelve como Steve Rogers.", {"evans", "steve"}),
        (e_impacto("MENOS DE\n4 SEMANAS", VERDE, "doom", fig="doom_metal"), "Faltan menos de cuatro semanas para el estreno.", {"cuatro", "semanas"}),
        (e_narrador(), "¿Mi opinión? Es el mejor momento para volver. Todo lo que pasó desde Endgame por fin se junta en una sola historia.", {"opinión", "volver"}),
        (e_estrellas(5), "¿Vale la pena volver a Marvel? Para mí, cinco de cinco.", {"cinco"}),
        (e_grupo(["loki_brazos", "doom_brazos", "iron_clasico"], "COMICS-STORE.COM.CO", "doom", VERDE), "Y si quieres a Loki, a Doom o a Iron Man en tu colección, los encuentras en comics store punto com punto co.", {"colección"}),
        (e_cta(), "Comenta RESUMEN si te sirvió, suscríbete y activa la campanita. Nos vemos en el próximo video de Comics Store.", {"resumen", "comics", "store"}),
    ], [1, 14, 28, 39, 51]

if __name__ == "__main__":
    v = sys.argv[1]; out = sys.argv[2]
    if v == "final": esc, re_ = [(e_pantalla_final(), "Te dejo aquí otro video que te va a encantar. Y si todavía no lo has hecho, suscríbete. ¡Nos vemos en el próximo video!", {"suscríbete"})], None
    else: esc, re_ = {"tt": guion_tt, "fb": guion_fb, "yt": guion_yt}[v]()
    if os.environ.get("HOJA"):
        tiles = []
        for fn, txt, cl in esc:
            fr = fn(1.8, 4.0).convert("RGB"); tiles.append(fr.resize((fr.width // 4, fr.height // 4)))
        tw, th = tiles[0].size; cols = 8 if tw < th else 5; rows = (len(tiles) + cols - 1) // cols; sh = Image.new("RGB", (tw * cols, th * rows))
        for i, im in enumerate(tiles): sh.paste(im, ((i % cols) * tw, (i // cols) * th))
        sh.save(out); print("hoja", len(tiles)); sys.exit()
    render(esc, out, regancho_idx=re_, musica="alegre", pron=PRON, estilo="neon", colores=COLORES,
           formato="horizontal" if lib.HORIZONTAL else "vertical", y_sub=250)
