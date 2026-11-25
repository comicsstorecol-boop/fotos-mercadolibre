"""Comics Store · Teoría: ¿Strange vio venir a Doom? — 3 versiones (tt, fb, yt) con figuras reales de la tienda.
Uso: python3 t01_strange_doom.py tt|fb|yt salida.mp4   (yt con FORMATO=horizontal)"""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from teoria_figuras import *
from motor import render

PRON = {"strange": ("en", "Strange"), "doom": ("en", "Doom"), "thanos": ("es", "tános"), "infinity": ("es", "infíniti"), "war": ("es", "uor"),
        "wars": ("es", "uors"), "secret": ("es", "sícret"), "endgame": ("es", "éndgueim"), "battleworld": ("es", "bátoluorld"), "tony": ("es", "tóni"),
        "hickman": ("es", "jícman"), "beyonders": ("es", "biyónders"), "reed": ("es", "rid"), "richards": ("es", "ríchards"), "robert": ("es", "róbert"),
        "downey": ("es", "dáuni"), "junior": ("es", "yúnior"), "benedict": ("es", "bénedict"), "cumberbatch": ("es", "cúmberbach"),
        "sheriff": ("es", "shérif"), "thors": ("es", "tors"), "comics": ("en", "Comics"), "youtube": ("es", "yutub"), "jonathan": ("es", "yónatan")}
COLORES = (VERDE, NARANJA)   # subtítulos: verde Doom + naranja místico
FH = P(1180, 760)            # alto de figura protagonista
PISO = P(1760, 890)

# ---------------------------------------------------------------- escenas
def e_strange_hilos(fig="strange_magia", chip_txt=None):
    def f(t, d):
        c = cosmos(t, "mistico"); hx, hy = P(W / 2, W * .5), P(860, 330)
        hilos(c, hx, hy, t, VERDE, n=30, abanico=(180, 360))
        mandala(c, hx, P(1050, 520), P(420, 330), t, NARANJA, .8)
        figura(c, fig, P(W / 2, W * .5), PISO, FH, t, "sube", NARANJA)
        particulas(c, t, NARANJA)
        if chip_txt: chip(c, chip_txt, P(W / 2, W * .5), P(1820, 1010), VERDE, alpha=eo(pr(t, .8, .4)))
        flash(c, t); return zoom(c, t, d, 1.08, 1.0)
    return S("strange_hilos", f)

def e_contador():
    def f(t, d):
        c = cosmos(t, "mistico"); hilos(c, W / 2, H + 40, t, VERDE, n=44, abanico=(195, 345), largo=H * 1.1)
        figura(c, "strange_magia", W / 2, PISO, P(620, 480), t, "sube", NARANJA, retraso=.1)
        contador_futuros(c, t, W / 2, P(760, 300)); flash(c, t, .12)
        return zoom(c, t, d, 1.0, 1.08)
    return S("contador", f)

def e_uno():
    def f(t, d):
        c = cosmos(t, "azul"); glow(c, W / 2, P(900, 480), P(380, 300), VERDE, 120)
        k = eb(pr(t, .15, .5)); texto(c, "1", W / 2, P(880, 470), int(P(560, 420) * max(.05, k)), (255, 255, 255), glow_col=VERDE, stroke=10)
        chip(c, "UN SOLO FUTURO", W / 2, P(1300, 800), VERDE, P(52, 50), eo(pr(t, .6, .4)))
        figura(c, "strange_magia", P(W * .2, W * .15), PISO, P(560, 640), t, "izq", NARANJA, retraso=.3, alpha=.9)
        rayos_velocidad(c, t, VERDE); return shake(zoom(c, t, d, 1.05, 1.0), t, 10)
    return S("uno", f)

def e_thanos_gema(fig="thanos_guante", chip_txt="GEMA DEL TIEMPO"):
    def f(t, d):
        c = cosmos(t, "thanos")
        figura(c, fig, P(W / 2 + 60, W * .62), PISO, FH, t, "der", ORO)
        u = eio(pr(t, .4, 1.6)); gx = P(220, 420) + (P(W / 2 + 120, W * .62) - P(220, 420)) * u; gy = P(700, 360) - math.sin(u * math.pi) * 160 + u * P(-20, 40)
        gema(c, gx, gy, P(60, 52), t)
        chip(c, chip_txt, P(W / 2, W * .3), P(1830, 960), VERDE, alpha=eo(pr(t, .7, .4)))
        particulas(c, t, ORO, n=30); flash(c, t); return zoom(c, t, d, 1.0, 1.1)
    return S("thanos_gema", f)

def e_chasquido():
    def f(t, d):
        c = cosmos(t, "rojo"); figura(c, "thanos_frente", W / 2, PISO, FH, t, "pop", ORO)
        if t > .8:
            u = pr(t, .8, .15); c.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(220 * (1 - u)))))
        particulas(c, t, (200, 180, 160), sube=True, n=45, a=230)
        chip(c, "MITAD DEL UNIVERSO", W / 2, P(1840, 1000), ROJO, alpha=eo(pr(t, 1, .4)))
        return shake(zoom(c, t, d, 1.0, 1.12), max(0, t - .8), 20, .6)
    return S("chasquido", f)

def e_polvo():
    def f(t, d):
        c = cosmos(t, "mistico", velocidad=.5); a = 1 - .75 * eio(pr(t, .6, d - .8))
        figura(c, "strange_portal", W / 2, PISO, P(1000, 760), t, "pop", NARANJA, alpha=a, flota=False)
        particulas(c, t, (210, 190, 170), sube=True, n=45, a=int(240 * (1 - a) + 40))
        chip(c, "“ERA LA ÚNICA FORMA”", W / 2, P(560, 160), NARANJA, P(46, 46), eo(pr(t, .5, .4)))
        return zoom(c, t, d, 1.0, 1.06)
    return S("polvo", f)

def e_impacto(txt, col=VERDE, pal="doom", sub=None, fig=None):
    def f(t, d):
        c = cosmos(t, pal, velocidad=2); mandala(c, W / 2, P(900, 470), P(460, 400), t, col, .35); particulas(c, t, col, n=35)
        if fig: figura(c, fig, W / 2, PISO + P(200, 160), FH, t, "sube", col, alpha=.55)
        rayos_velocidad(c, t, col, .7)
        lineas = txt.split("\n")
        for i, ln in enumerate(lineas):
            k = eb(pr(t, .05 + i * .15, .4)); texto(c, ln, W / 2, P(900, 470) + (i - (len(lineas) - 1) / 2) * P(170, 150), int(P(130, 128) * max(.05, k)), (255, 255, 255), glow_col=col, stroke=8)
        if sub: chip(c, sub, W / 2, P(1300, 800), col, P(44, 44), eo(pr(t, .6, .4)))
        flash(c, t, .2, col, 150); return shake(c, t, 16)
    return S("impacto", f)

def e_doom(fig="doom_brazos", pal="doom", chip_txt=None, entra="sube", z=(1.12, 1.0)):
    def f(t, d):
        c = cosmos(t, pal); glow(c, W / 2, P(900, 500), P(520, 420), VERDE, 110 + int(40 * math.sin(t * 5)))
        mandala(c, W / 2, P(950, 500), P(470, 380), t, VERDE, .55)
        figura(c, fig, W / 2, PISO, FH, t, entra, VERDE)
        particulas(c, t, VERDE, n=40)
        if chip_txt: chip(c, chip_txt, W / 2, P(1840, 1000), VERDE, alpha=eo(pr(t, .6, .4)))
        return glitch(shake(zoom(c, t, d, *z), t, 18), t)
    return S("doom", f)

def e_narrador(titulo=None, sub=None, col=VERDE):
    return S("narrador", narrador_escena(titulo, col, sub))

def e_portada():
    def f(t, d):
        c = cosmos(t, "mistico", velocidad=1.5); hilos(c, W / 2, P(600, 260), t, VERDE, n=26)
        figura(c, "doom_metal", P(W * .3, W * .3), PISO, P(1000, 820), t, "izq", VERDE)
        figura(c, "strange_magia", P(W * .72, W * .7), PISO, P(1000, 820), t, "der", NARANJA, retraso=.15)
        texto(c, "STRANGE", P(W / 2, W / 2), P(470, 150), P(120, 110), NARANJA, alpha=eo(pr(t, .4, .3)), glow_col=NARANJA)
        texto(c, "VS DOOM", P(W / 2, W / 2), P(610, 270), P(120, 110), VERDE, alpha=eo(pr(t, .6, .3)), glow_col=VERDE)
        chip(c, "LA TEORÍA", W / 2, P(1840, 390), (255, 255, 255), P(46, 40), eo(pr(t, .9, .3)))
        flash(c, t); return zoom(c, t, d, 1.06, 1.0)
    return S("portada", f)

def e_spoilers():
    def f(t, d):
        c = cosmos(t, "rojo"); k = eb(pr(t, .1, .5))
        texto(c, "⚠" if False else "!", W / 2, P(780, 380), int(P(300, 240) * max(.05, k)), ORO, glow_col=ROJO, stroke=10)
        texto(c, "SPOILERS", W / 2, P(1060, 600), P(130, 120), (255, 255, 255), alpha=eo(pr(t, .3, .3)), glow_col=ROJO)
        for i, s in enumerate(["INFINITY WAR", "ENDGAME", "CÓMICS SECRET WARS"]):
            chip(c, s, W / 2 + P(0, (i - 1) * 480), P(1260 + i * 120, 790), ORO, P(40, 36), eo(pr(t, .6 + i * .2, .3)))
        return shake(c, t, 10)
    return S("spoilers", f)

def e_capitulo(n, titulo, col=NARANJA, pal="mistico"):
    def f(t, d):
        c = cosmos(t, pal, velocidad=2); glow(c, W / 2, H / 2, P(500, 420), col, 90)
        mandala(c, W / 2, H / 2, P(380, 340), t, col, .5)
        texto(c, f"CAPÍTULO {n}", W / 2, H / 2 - P(90, 80), P(64, 60), col, alpha=eo(pr(t, .1, .3)))
        texto(c, titulo, W / 2 + (1 - eo(pr(t, .25, .5))) * W, H / 2 + P(40, 40), P(98, 100), (255, 255, 255), glow_col=col)
        rayos_velocidad(c, t, col, .5); flash(c, t, .15, col); return c
    return S("capitulo", f)

def e_endgame_dedo():
    def f(t, d):
        c = cosmos(t, "azul"); figura(c, "strange_magia", P(W * .4, W * .3), PISO, FH, t, "izq", NARANJA)
        k = eb(pr(t, .4, .5)); texto(c, "1", P(W * .78, W * .7), P(800, 450), int(P(380, 360) * max(.05, k)), (255, 255, 255), glow_col=NARANJA, stroke=10)
        chip(c, "5 AÑOS DESPUÉS", P(W * .78, W * .7), P(1150, 780), NARANJA, P(40, 42), eo(pr(t, .2, .4)))
        return zoom(c, t, d, 1.0, 1.1)
    return S("endgame", f)

def e_comic(sub="2015", num="#1", fig=None, titulo="SECRET WARS"):
    def f(t, d):
        c = cosmos(t, "doom"); hilos(c, W / 2, P(900, 500), t, VERDE, n=18, abanico=(0, 360), largo=P(900, 900), a=120)
        if fig: figura(c, fig, P(W * .72, W * .74), PISO, P(900, 820), t, "der", VERDE, retraso=.3)
        comic(c, P(W / 2 if not fig else W * .45, W * .36), P(950, 520), t, titulo, sub, num, ancho=P(520 if not fig else 390, 440))
        chip(c, f"CÓMIC · {sub}", P(W / 2, W * .36), P(1640, 1000), ORO, P(42, 40), eo(pr(t, .7, .3)))
        return zoom(c, t, d, 1.0, 1.08)
    return S("comic", f)

def e_incursion():
    def f(t, d):
        c = cosmos(t, "rojo"); u = eio(pr(t, .2, max(.5, d - .8)))
        x1 = P(W * .2, W * .25) + u * P(W * .22, W * .2); x2 = P(W * .8, W * .75) - u * P(W * .22, W * .2)
        planeta(c, x1, P(900, 500), P(220, 200), t, AZUL); planeta(c, x2, P(950, 520), P(220, 200), t * 1.3 + 2, ROJO)
        if u > .95: flash(c, t - (.2 + .95 * max(.5, d - .8)), .3, (255, 240, 220), 230)
        chip(c, "INCURSIONES", W / 2, P(1500, 900), ROJO, alpha=eo(pr(t, .4, .3)))
        return shake(c, max(0, t - d + .6), 18, .6)
    return S("incursion", f)

def e_trio(chip_txt="HOMBRE MOLÉCULA", chip2=None):
    def f(t, d):
        c = cosmos(t, "mistico"); glow(c, W / 2, P(700, 260), P(300, 260), (255, 255, 255), 90)
        figura(c, "doom_brazos", P(W * .3, W * .3), PISO, P(950, 800), t, "izq", VERDE)
        figura(c, "strange_portal", P(W * .7, W * .7), PISO, P(950, 800), t, "der", NARANJA, retraso=.15)
        chip(c, chip_txt, W / 2, P(560, 140), MORADO, P(44, 42), eo(pr(t, .5, .3)))
        if chip2: chip(c, chip2, W / 2, P(1850, 235), ROJO, P(40, 38), eo(pr(t, .9, .3)))
        return zoom(c, t, d, 1.0, 1.07)
    return S("trio", f)

def e_battleworld(con_doom=True, chip_txt="BATTLEWORLD"):
    def f(t, d):
        c = cosmos(t, "doom"); r = P(400, 330); py = P(1250, 760)
        planeta(c, W / 2, py, r, t)
        if con_doom: figura(c, "doom_trono", W / 2, py - r * .78, P(760, 560), t, "baja", VERDE, retraso=.5, reflejo=False)
        chip(c, chip_txt, W / 2, P(470, 150), VERDE, P(52, 48), eo(pr(t, .3, .3)))
        particulas(c, t, VERDE, n=30); flash(c, t); return zoom(c, t, d, 1.08, 1.0)
    return S("battleworld", f)

def e_lista(items, col=ORO, pal="doom", fig="doom_trono"):
    def f(t, d):
        c = cosmos(t, pal); figura(c, fig, P(W / 2, W * .25), PISO, P(820, 880), t, "pop", VERDE, alpha=P(.45, 1.))
        paso = max(.6, (d - .6) / len(items))
        for i, it in enumerate(items):
            chip(c, it, P(W / 2, W * .66), P(700 + i * 210, 330 + i * 190), col, P(42, 42), eo(pr(t, .2 + i * paso, .35)))
        return zoom(c, t, d, 1.0, 1.05)
    return S("lista", f)

def e_duo(chip_txt="MANO DERECHA"):
    def f(t, d):
        c = cosmos(t, "doom"); planeta(c, W / 2, P(1900, 1250), P(520, 420), t, VERDE, .8)
        figura(c, "doom_trono", P(W * .32, W * .35), PISO, FH, t, "izq", VERDE)
        figura(c, "strange_magia", P(W * .72, W * .66), PISO, FH * .96, t, "der", NARANJA, retraso=.35)
        chip(c, chip_txt, P(W * .72, W * .66), P(560, 150), NARANJA, P(44, 42), eo(pr(t, .9, .3)))
        return zoom(c, t, d, 1.0, 1.08)
    return S("duo", f)

def e_lupa():
    def f(t, d):
        c = cosmos(t, "mistico"); figura(c, "strange_magia", W / 2, PISO, FH, t, "pop", NARANJA)
        b = c.filter(ImageFilter.GaussianBlur(int(4 + 10 * eo(pr(t, .1, .5))))); c = b
        lupa(c, P(W * .6, W * .58), P(800, 420), t)
        chip(c, "UN DETALLE", W / 2, P(1500, 880), (255, 255, 255), P(54, 50), eo(pr(t, .3, .3)))
        return zoom(c, t, d, 1.0, 1.1)
    return S("lupa", f)

def e_balsa(chip_txt="ESCONDIDA DE DOOM", abierta=0.):
    def f(t, d):
        c = cosmos(t, "azul"); balsa(c, W / 2, P(900, 480), t, abierta=abierta + .5 * eo(pr(t, 1, 1)) * (abierta > 0))
        hilos(c, W / 2, P(900, 480), t, AZUL, n=16, abanico=(0, 360), largo=P(700, 700), a=110)
        chip(c, chip_txt, W / 2, P(1380, 860), AZUL, P(46, 44), eo(pr(t, .5, .3)))
        return zoom(c, t, d, 1.0, 1.1)
    return S("balsa", f)

def e_muerte():
    def f(t, d):
        c = cosmos(t, "rojo"); figura(c, "doom_metal", P(W * .38, W * .4), PISO, FH, t, "pop", VERDE)
        a = 1 - eio(pr(t, .9, 1.)); figura(c, "strange_magia", P(W * .76, W * .68), PISO, FH * .9, t, "der", NARANJA, alpha=a, flota=False)
        if t > .9: particulas(c, t, (230, 200, 190), n=40, a=int(240 * (1 - a)))
        flash(c, max(0, t - .9), .3, ROJO, 200)
        chip(c, "DOOM LO MATA", W / 2, P(1840, 1010), ROJO, P(50, 46), eo(pr(t, 1.1, .3)))
        return shake(c, max(0, t - .9), 22, .6)
    return S("muerte", f)

def e_versus():
    def f(t, d):
        c = cosmos(t, "azul"); figura(c, "doom_brazos", P(W * .3, W * .3), PISO, FH * .95, t, "izq", VERDE)
        texto(c, "VS", W / 2, P(760, 450), P(150, 150), (255, 255, 255), alpha=eo(pr(t, .3, .3)), glow_col=AZUL)
        chip(c, "REED RICHARDS", P(W * .72, W * .72), P(1000, 560), AZUL, P(46, 46), eo(pr(t, .5, .3)))
        chip(c, "“LO HABRÍA HECHO MEJOR”", W / 2, P(1840, 1010), ORO, P(40, 40), eo(pr(t, 1.6, .3)))
        rayos_velocidad(c, t, AZUL); return shake(zoom(c, t, d, 1.0, 1.06), t, 12)
    return S("versus", f)

def e_ajedrez(chip_txt=None, movs=1):
    def f(t, d):
        c = cosmos(t, "mistico"); s = P(78, 62); cx, cy = W / 2, P(780, 420)
        piezas = [("rey", (60, 200, 110), (1, 3), (1, 3), 99), ("peon", (240, 240, 250), (4, 1), (4, 1), 99), ("peon", (240, 240, 250), (3, 4), (3, 4), 99),
                  ("reina", (220, 60, 70), (4, 4), (2, 3) if movs else (4, 4), .6), ("torre", (60, 200, 110), (0, 0), (0, 2) if movs > 1 else (0, 0), 1.6)]
        glow(c, cx, cy + s * 3.3, s * 5, MORADO, 80); ajedrez(c, t, cx, cy, s, piezas)
        if chip_txt: chip(c, chip_txt, P(W * .4, W / 2), P(1440, 1000), NARANJA, P(44, 42), eo(pr(t, .7, .3)))
        figura(c, "strange_magia", P(W * .8, W * .85), P(1800, 640), P(620, 520), t, "der", NARANJA, retraso=.4, reflejo=False)
        return zoom(c, t, d, 1.0, 1.1)
    return S("ajedrez", f)

def e_dominos(chip_txt=None):
    def f(t, d):
        c = cosmos(t, "thanos"); n = P(9, 13); paso = P(105, 120); x0 = W / 2 - (n - 1) * paso / 2
        dominos(c, t, x0, P(1150, 700), n, paso, vel=max(.1, (d - 1) / n))
        if chip_txt:
            for i, s in enumerate(chip_txt):
                chip(c, s, P(W / 2, W * (.25 + .25 * i)), P(560 + i * 130, 230), ORO, P(38, 38), eo(pr(t, .3 + i * max(.1, (d - 1) / 3), .3)))
        return zoom(c, t, d, 1.0, 1.08)
    return S("dominos", f)

def e_linea(items):
    def f(t, d):
        c = cosmos(t, "mistico")
        if not HZ: figura(c, "doom_metal", W / 2, 1880, 700, t, "sube", VERDE, alpha=.55, reflejo=False)
        linea_tiempo(c, t, items); return zoom(c, t, d, 1.0, 1.05)
    return S("linea", f)

def e_figura_texto(fig, chip_txt, col=VERDE, pal="doom", entra="pop"):
    def f(t, d):
        c = cosmos(t, pal); mandala(c, W / 2, P(950, 520), P(430, 360), t, col, .45)
        figura(c, fig, W / 2, PISO, FH, t, entra, col)
        chip(c, chip_txt, W / 2, P(1840, 1010), col, P(46, 44), eo(pr(t, .5, .3)))
        particulas(c, t, col, n=30); flash(c, t, .15); return zoom(c, t, d, 1.1, 1.0)
    return S("figura", f)

def e_estrellas(nota=4):
    def f(t, d):
        c = cosmos(t, "mistico"); texto(c, "¿QUÉ TAN POSIBLE ES?", W / 2, P(620, 300), P(64, 66), (255, 255, 255), glow_col=NARANJA)
        estrellas(c, t, nota, W / 2, P(900, 520)); texto(c, f"{nota} / 5", W / 2, P(1120, 700), P(90, 84), ORO, alpha=eo(pr(t, 1.5, .3)), glow_col=ORO)
        return zoom(c, t, d, 1.0, 1.05)
    return S("estrellas", f)

def e_cta(youtube=False):
    def f(t, d):
        c = cosmos(t, "doom"); figura(c, "doom_brazos", P(W / 2, W * .27), P(1180, 880), P(760, 720), t, "pop", VERDE, reflejo=False)
        caja_comentario(c, t, "DOOM", x=P(W / 2, W * .66), y=P(1320, 400))
        if youtube:
            chip(c, "▶  EXPLICACIÓN COMPLETA EN YOUTUBE" if False else "EXPLICACIÓN COMPLETA EN YOUTUBE", W / 2, P(1560, 900), ROJO, P(40, 38), eo(pr(t, 1.6, .3)), (40, 6, 10))
        barra_suscribir(c, t, x=P(W / 2, W * .66), y=P(1750, 600) if not youtube else P(1740, 600), inicio=2.0 if youtube else 1.4)
        return c
    return S("cta", f)

# ---------------------------------------------------------------- guiones
TT = [
    (e_strange_hilos(chip_txt="14.000.605 FUTUROS"), "Strange vio catorce millones seiscientos cinco futuros… y solo en uno ganaban.", {"catorce", "uno"}),
    (e_contador(), "Lo dijo en Infinity War. Un solo futuro, entre millones.", {"infinity", "solo"}),
    (e_thanos_gema(), "Y aun así… le entregó la gema del tiempo a Thanos.", {"gema", "thanos"}),
    (e_endgame_dedo(), "Y en Endgame, le levantó un solo dedo a Tony. Era la única forma.", {"endgame", "dedo"}),
    (e_narrador(), "¿Por qué? Hay una teoría que lo cambia todo.", {"teoría"}),
    (e_doom(), "¿Y si en ese único futuro… ya aparecía Doctor Doom?", {"doom"}),
    (e_ajedrez("PIEZAS EN MOVIMIENTO", 2), "Strange no jugaba contra Thanos. Estaba moviendo piezas para algo más grande.", {"piezas", "grande"}),
    (e_comic(fig="doom_metal"), "En los cómics de Secret Wars, del dos mil quince, Doom se convierte en un dios.", {"secret", "wars", "dios"}),
    (e_battleworld(), "Junta los restos del multiverso en un solo planeta: Battleworld.", {"battleworld"}),
    (e_figura_texto("strange_portal", "MIRÓ… Y HUYÓ", NARANJA, "mistico"), "Strange también pudo tener ese poder. Lo miró… y huyó. Doom no.", {"huyó", "doom"}),
    (e_duo(), "¿Y quién gobierna a su lado, como su mano derecha? ¡Doctor Strange!", {"strange"}),
    (e_balsa("ESCONDIDA DE DOOM"), "Pero Strange escondía un secreto: una balsa con los últimos héroes.", {"secreto", "balsa"}),
    (e_muerte(), "Cuando los ayuda a escapar… Doom lo mata.", {"mata"}),
    (e_linea([("INFINITY\nWAR", "2018"), ("ENDGAME", "2019"), ("DOOMSDAY", "18 DIC 2026", VERDE)]), "Avengers: Doomsday se estrena el dieciocho de diciembre. ¿Strange lo sabía desde el principio?", {"doomsday", "principio"}),
    (e_cta(youtube=True), "Comenta DOOM si crees la teoría. La explicación completa está en nuestro canal de YouTube.", {"doom", "youtube"}),
]
RE_TT = [4, 11]

FB = [
    (e_strange_hilos(chip_txt="14.000.605 FUTUROS"), "Strange vio catorce millones seiscientos cinco futuros… y solo en uno ganaban.", {"catorce", "uno"}),
    (e_doom(), "Pero, ¿y si en ese único futuro… ya aparecía Doctor Doom?", {"doom"}),
    (e_contador(), "En Infinity War, Strange revisa catorce millones seiscientos cinco futuros. Ganan en uno.", {"infinity", "uno"}),
    (e_thanos_gema(), "Y aun así, le entrega la gema del tiempo a Thanos.", {"gema", "thanos"}),
    (e_chasquido(), "Thanos chasquea los dedos, y la mitad del universo desaparece.", {"mitad"}),
    (e_polvo(), "Antes de convertirse en polvo, le dice a Tony que era la única forma.", {"única"}),
    (e_endgame_dedo(), "Y en Endgame, le levanta un solo dedo. Ese era el futuro.", {"endgame", "dedo"}),
    (e_narrador(), "Quédate, porque lo que pasa en los cómics es todavía más oscuro.", {"cómics", "oscuro"}),
    (e_comic(fig="doom_metal"), "En Secret Wars, del dos mil quince, el multiverso se destruye.", {"secret", "wars", "multiverso"}),
    (e_incursion(), "Los universos chocan entre sí. Se llaman incursiones.", {"incursiones"}),
    (e_trio(chip2="BEYONDERS"), "Doom, Strange y el Hombre Molécula se enfrentan a los Beyonders, los seres detrás de esa destrucción.", {"beyonders"}),
    (e_doom("doom_metal", chip_txt="PODER INFINITO"), "Les roban su poder. Strange confiesa que miró ese poder… y huyó. Doom no.", {"poder", "huyó"}),
    (e_battleworld(), "Con los restos del multiverso, Doom crea un solo planeta: Battleworld. Y se vuelve su dios.", {"battleworld", "dios"}),
    (e_lista(["SOL: LA ANTORCHA HUMANA", "MURALLA: LA COSA", "POLICÍA: LOS THORS"]), "El sol del planeta es la Antorcha Humana, la muralla es la Cosa, y la policía, un ejército de Thors.", {"sol", "muralla", "policía"}),
    (e_duo("SHERIFF"), "¿Y quién está a su derecha? Doctor Strange, como su sheriff.", {"sheriff", "strange"}),
    (e_balsa("8 AÑOS DORMIDOS"), "Pero Strange escondía una balsa con los últimos héroes. Llevaban ocho años dormidos.", {"balsa", "ocho"}),
    (e_muerte(), "Cuando los ayuda a escapar, Doom pierde el control… y mata a su único amigo.", {"mata", "amigo"}),
    (e_versus(), "Al final, Doom admite algo que nunca había dicho: que Reed Richards lo habría hecho mejor.", {"reed", "mejor"}),
    (e_ajedrez("PIEZAS EN MOVIMIENTO", 2), "Ahora une los puntos: Strange no jugaba contra Thanos. Estaba moviendo piezas.", {"piezas"}),
    (e_dominos(["LA GEMA", "EL CHASQUIDO", "TONY"]), "La gema, el chasquido, el sacrificio de Tony… fichas que caen una detrás de otra.", {"fichas"}),
    (e_figura_texto("doom_brazos", "ROBERT DOWNEY JR."), "Y en el cine, Doom lo interpreta Robert Downey Junior.", {"downey"}),
    (e_linea([("DOOMSDAY", "18 DIC 2026", VERDE), ("SECRET\nWARS", "17 DIC 2027", NARANJA)]), "Avengers: Doomsday llega el dieciocho de diciembre, y Secret Wars, en diciembre de dos mil veintisiete.", {"doomsday", "secret", "wars"}),
    (e_estrellas(4), "¿Qué tan posible es esta teoría? Para mí, cuatro de cinco estrellas.", {"cuatro"}),
    (e_impacto("¿LO SABÍA\nTODO?", NARANJA, "mistico", fig="strange_portal"), "¿Strange lo sabía todo desde el principio?", {"todo"}),
    (e_cta(youtube=True), "Comenta DOOM si crees la teoría. La explicación completa está en nuestro canal de YouTube.", {"doom", "youtube"}),
]
RE_FB = [1, 7, 16]

YT = [
    (e_narrador(), INTRO_GAMER[0], INTRO_GAMER[1]),
    (e_strange_hilos(chip_txt="14.000.605 FUTUROS"), "Doctor Strange vio catorce millones seiscientos cinco futuros. Y solo en uno, los Vengadores ganaban.", {"catorce", "uno"}),
    (e_doom(), "Pero, ¿y si en ese único futuro… el verdadero enemigo no era Thanos, sino Doctor Doom?", {"doom"}),
    (e_portada(), "Esta es la teoría de Strange y Doom.", {"teoría"}),
    (e_spoilers(), "Aviso: hay spoilers de Infinity War, de Endgame y de los cómics de Secret Wars.", {"spoilers"}),
    (e_trio("FIGURAS DE COMICS STORE"), "Y ojo: todas las figuras que ves en este video son de nuestra tienda, Comics Store.", {"figuras", "comics", "store"}),
    (e_capitulo(1, "LO QUE VIO STRANGE", NARANJA), "Capítulo uno. Lo que vio Strange.", {"strange"}),
    (e_strange_hilos("strange_portal"), "En Infinity War, Strange usa la gema del tiempo para mirar hacia adelante.", {"infinity", "gema"}),
    (e_figura_texto("strange_magia", "LA GEMA ANTES QUE TODO", NARANJA, "mistico"), "Strange había advertido que, si tenía que elegir, protegería la gema antes que a Tony o a Peter.", {"gema", "elegir"}),
    (e_contador(), "Revisa catorce millones seiscientos cinco futuros posibles.", {"catorce"}),
    (e_uno(), "Y cuando Tony le pregunta en cuántos ganan, responde: en uno.", {"uno"}),
    (e_thanos_gema(), "Minutos después, hace algo que nadie entendió: le entrega la gema del tiempo a Thanos.", {"gema", "thanos"}),
    (e_impacto("¿A CAMBIO\nDE TONY?", ROJO, "rojo", fig="thanos_guante"), "Y la entrega a cambio de la vida de Tony. Algo no cuadraba.", {"tony", "cuadraba"}),
    (e_chasquido(), "Thanos completa el guantelete, chasquea los dedos, y la mitad del universo desaparece.", {"mitad"}),
    (e_polvo(), "Strange también se convierte en polvo. Pero antes, le dice a Tony que era la única forma.", {"polvo", "única"}),
    (e_endgame_dedo(), "Cinco años después, en Endgame, Strange regresa y le levanta un solo dedo a Tony.", {"endgame", "dedo"}),
    (e_impacto("UN SOLO\nFUTURO", NARANJA, "mistico"), "Ese era el futuro. El único. Y Tony entrega su vida para cumplirlo.", {"único", "vida"}),
    (e_narrador(), "Pero espera. Si Strange vio el final… ¿qué vio después del final?", {"después"}),
    (e_capitulo(2, "DOOM EN LOS CÓMICS", VERDE, "doom"), "Capítulo dos. Doom en los cómics.", {"doom"}),
    (e_comic("1984", "#1", fig="doom_brazos"), "Doom ya había intentado ser un dios en el primer Secret Wars, de mil novecientos ochenta y cuatro.", {"dios", "secret", "wars"}),
    (e_comic("2015", "#1", fig="doom_metal"), "Pero en el Secret Wars de dos mil quince, escrito por Jonathan Hickman, lo consigue.", {"hickman", "consigue"}),
    (e_incursion(), "Los universos empiezan a chocar entre sí. Se llaman incursiones, y destruyen el multiverso.", {"incursiones", "multiverso"}),
    (e_trio(chip2="BEYONDERS"), "Doom, Strange y el Hombre Molécula se enfrentan a los Beyonders, los seres detrás de esa destrucción.", {"beyonders"}),
    (e_doom("doom_metal", chip_txt="PODER INFINITO"), "Les roban su poder. Y Doom se queda con él.", {"poder", "doom"}),
    (e_figura_texto("strange_portal", "MIRÓ… Y HUYÓ", NARANJA, "mistico"), "Strange confiesa que miró ese poder infinito… y huyó. Doom no.", {"huyó", "doom"}),
    (e_battleworld(), "Con los restos del multiverso, Doom crea un solo planeta: Battleworld.", {"battleworld"}),
    (e_doom("doom_trono", chip_txt="DIOS EMPERADOR", entra="baja"), "Ahí todos lo adoran como el Dios Emperador Doom.", {"dios", "emperador"}),
    (e_lista(["SOL: LA ANTORCHA HUMANA", "MURALLA: LA COSA", "POLICÍA: LOS THORS"]), "El sol del planeta es la Antorcha Humana. La muralla que lo protege es la Cosa. Y la policía, un ejército de Thors.", {"sol", "muralla", "policía"}),
    (e_battleworld(False, "REINOS Y BARONES"), "El planeta está dividido en reinos, y cada reino lo gobierna un barón que responde ante Doom.", {"reinos", "barón"}),
    (e_doom("doom_trono", chip_txt="SUE · FRANKLIN · VALERIA", entra="pop"), "Doom incluso se casa con Sue Storm, y cría a sus hijos, Franklin y Valeria.", {"sue", "valeria"}),
    (e_lista(["MANO IZQUIERDA: VALERIA", "MANO DERECHA: STRANGE"], NARANJA), "Valeria es su mano izquierda. Y su mano derecha…", {"izquierda", "derecha"}),
    (e_duo("SHERIFF"), "…es Doctor Strange, como su sheriff.", {"sheriff", "strange"}),
    (e_narrador(), "Y aquí viene la parte que casi nadie recuerda.", {"nadie"}),
    (e_balsa("ESCONDIDA DE DOOM"), "Strange guardaba un secreto: una balsa con los últimos héroes del universo, escondida incluso de Doom.", {"secreto", "balsa"}),
    (e_balsa("8 AÑOS DORMIDOS", abierta=.3), "Llevaban ocho años dormidos. Y Strange decide despertarlos.", {"ocho", "despertarlos"}),
    (e_lupa(), "Y ese detalle lo cambia todo.", {"detalle"}),
    (e_muerte(), "Cuando Strange los ayuda a escapar, Doom pierde el control… y mata a su único amigo.", {"mata", "amigo"}),
    (e_balsa("REED RICHARDS DESPIERTA", abierta=.6), "Entre los que despertó estaba Reed Richards, el esposo de Sue. Y ahí empieza la guerra final.", {"reed", "guerra"}),
    (e_versus(), "Al final, el poder pasa a Reed Richards. Y Doom admite algo que nunca había dicho: que Reed lo habría hecho mejor.", {"reed", "mejor"}),
    (e_capitulo(3, "LA TEORÍA", NARANJA), "Capítulo tres. La teoría.", {"teoría"}),
    (e_ajedrez("PIEZAS EN MOVIMIENTO", 1), "Ahora une los puntos. Strange no estaba jugando contra Thanos.", {"thanos"}),
    (e_ajedrez("UNA PARTIDA MÁS GRANDE", 2), "Estaba moviendo piezas para una partida mucho más grande.", {"piezas", "grande"}),
    (e_dominos(["LA GEMA", "EL CHASQUIDO", "TONY"]), "Entregar la gema, el chasquido, el sacrificio de Tony… fichas que caen una detrás de otra.", {"fichas"}),
    (e_strange_hilos("strange_magia"), "Si de verdad vio catorce millones de futuros, es difícil creer que no viera lo que venía después.", {"después"}),
    (e_incursion(), "Y en el Multiverso de la Locura, el propio Strange provoca una incursión. La misma palabra de los cómics.", {"incursión", "cómics"}),
    (e_doom("doom_brazos", chip_txt="EL FINAL ERA DOOM"), "La teoría dice que el único futuro que vio Strange no terminaba con Thanos. Terminaba con Doom.", {"doom"}),
    (e_duo("CARA A CARA"), "Y que, como en los cómics, Strange sabe que tarde o temprano le toca estar frente a él.", {"frente"}),
    (e_narrador(), "Ahora mira las fechas, porque esto ya está a la vuelta de la esquina.", {"fechas"}),
    (e_capitulo(4, "LO QUE VIENE", VERDE, "doom"), "Capítulo cuatro. Lo que viene.", {"viene"}),
    (e_figura_texto("doom_metal", "ROBERT DOWNEY JR."), "Doom llega al cine en Avengers: Doomsday, y lo interpreta Robert Downey Junior.", {"doomsday", "downey"}),
    (e_linea([("INFINITY\nWAR", "2018"), ("ENDGAME", "2019"), ("DOOMSDAY", "18 DIC 2026", VERDE), ("SECRET\nWARS", "17 DIC 2027", NARANJA)]),
     "Doomsday se estrena el dieciocho de diciembre de dos mil veintiséis. Y Secret Wars, el diecisiete de diciembre de dos mil veintisiete.", {"doomsday", "secret", "wars"}),
    (e_figura_texto("strange_portal", "“MUCHO” EN SECRET WARS", NARANJA, "mistico"), "Y Benedict Cumberbatch ha dicho que Strange estará mucho en Secret Wars.", {"cumberbatch", "mucho"}),
    (e_lista(["VENGADORES", "X-MEN", "CUATRO FANTÁSTICOS"], VERDE, "mistico", "doom_brazos"), "Doomsday junta héroes de tres universos: Vengadores, X-Men y los Cuatro Fantásticos.", {"tres", "universos"}),
    (e_impacto("MENOS DE\n4 SEMANAS", VERDE, "doom", fig="doom_metal"), "Y faltan menos de cuatro semanas para el estreno.", {"cuatro", "semanas"}),
    (e_capitulo(5, "MI OPINIÓN", NARANJA), "Capítulo cinco. Mi opinión.", {"opinión"}),
    (e_narrador(), "Strange es el personaje que más sabe del multiverso. Si alguien vio venir a Doom, fue él.", {"multiverso", "doom"}),
    (e_strange_hilos("strange_portal"), "No creo que Marvel lo diga tan directo. Pero el Strange del cine ya cargó con decisiones así antes.", {"decisiones"}),
    (e_duo("CARA A CARA"), "Y un enfrentamiento entre los dos doctores… sería de lo mejor de esta saga.", {"doctores", "mejor"}),
    (e_estrellas(4), "¿Qué tan posible es esta teoría? Cuatro de cinco estrellas.", {"cuatro"}),
    (e_impacto("¿LO SABÍA\nTODO?", NARANJA, "mistico", fig="strange_portal"), "Y tú, ¿crees que Strange lo sabía todo desde el principio?", {"todo"}),
    (e_trio("COMICS-STORE.COM.CO"), "Y si quieres a Doom o a Strange en tu colección, los encuentras en comics store punto com punto co.", {"colección"}),
    (e_cta(), "Comenta DOOM si crees la teoría, suscríbete y activa la campanita. Nos vemos en el próximo video de Comics Store.", {"doom", "comics", "store"}),
]
RE_YT = [2, 17, 32, 47]

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
FINAL = [(e_pantalla_final(), "Te dejo aquí otro video que te va a encantar. Y si todavía no lo has hecho, suscríbete. ¡Nos vemos en el próximo video!", {"suscríbete"})]

if __name__ == "__main__":
    v = sys.argv[1]; out = sys.argv[2]
    esc, re_ = {"tt": (TT, RE_TT), "fb": (FB, RE_FB), "yt": (YT, RE_YT), "final": (FINAL, None)}[v]
    if os.environ.get("SOLO"): esc = [esc[int(i)] for i in os.environ["SOLO"].split(",")]
    render(esc, out, regancho_idx=re_, musica="alegre", pron=PRON, estilo="neon", colores=COLORES,
           formato="horizontal" if lib.HORIZONTAL else "vertical", y_sub=250)
