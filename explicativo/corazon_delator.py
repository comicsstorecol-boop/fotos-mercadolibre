"""Comics Store · Estilo explicativo: El corazón delator (Edgar Allan Poe, 1843)."""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
from lib import *
from motor import render
import visuales as V
from PIL import Image, ImageDraw

M = marca("comics-store")
def corazon_oscuro(size):
    ic = V.icono("corazon").resize((size, size)); dark = Image.new("RGBA", ic.size, (90, 0, 12, 255)); dark.putalpha(ic.getchannel("A"))
    return Image.blend(ic, dark, .45)
ROJO = (210, 20, 40); AMBAR = (255, 200, 110)

def narrador(c, x, y, s=1., rim=(255, 170, 90)):
    place(c, persona("de_pie", (12, 10, 16), rim, s), x, y)

def policia(c, x, y, s=.8):
    p = persona("de_pie", (10, 14, 30), (90, 150, 255), s).copy(); d = ImageDraw.Draw(p)
    w = p.width; d.rounded_rectangle((w * .32, 8, w * .68, 50 * s), 10, fill=(10, 14, 30)); d.rectangle((w * .26, 44 * s, w * .74, 58 * s), fill=(10, 14, 30))
    place(c, p, x, y)

def e1(t, d):  # gancho
    c = cuarto_oscuro().copy(); glow(c, 540, 820, 150, AMBAR, int(150 + 40 * math.sin(t * 9)))
    h = Hi(); h.rect((520, 860, 560, 960), fill=(236, 226, 200)); h.ellipse((528, 815, 552, 865), fill=(255, 210, 120)); c.alpha_composite(h.done())
    narrador(c, 300, 1150, 1.1); vineta(c, .8); return camera(c, t, d, 1.0, 1.12, 0, -40)

def e2(t, d):
    c = vgrad(W, H, [(0, (40, 26, 20)), (1, (12, 8, 6))]).copy(); glow(c, W / 2, 1000, 400, AMBAR, 70)
    place(c, libro_antiguo("El corazón delator", "Edgar Allan Poe"), W / 2, 1050, scale=eb(pr(t, .1, .6)))
    etiqueta(c, "1843", W / 2, 640, AMBAR, size=70, alpha=eo(pr(t, .9, .4)), borde=AMBAR); vineta(c, .6)
    return camera(c, t, d, 1.0, 1.08)

def e3(t, d):
    c = noche_casa().copy(); niebla(c, t, 1450); vineta(c, .5); return camera(c, t, d, 1.0, 1.12, 0, 60)

def e4(t, d):
    c = vgrad(W, H, NOCHE).copy(); glow(c, W / 2, 900, 400, (150, 185, 210), 60)
    ojo_grande(c, W / 2, 950, 760, eo(pr(t, .1, .6)), (math.sin(t) * 30, 0), True)
    # buitre en silueta cruzando
    x = -200 + (t / d) * (W + 400); h = Hi(); y = 520 + math.sin(t * 3) * 20
    h.poly([(x - 160, y), (x - 40, y - 30 - 30 * math.sin(t * 6)), (x, y + 10), (x + 40, y - 30 - 30 * math.sin(t * 6)), (x + 160, y), (x, y + 30)], fill=(6, 6, 10))
    c.alpha_composite(h.done()); vineta(c, .7); return camera(c, t, d, 1.05, 1.15)

def e5(t, d):
    c = cuarto_oscuro().copy(); noche = min(7, 1 + int(t / d * 7))
    haz_linterna(c, 60, 720, 22 + math.sin(t * 2) * 3, 1150, 7 + 4 * eo(pr(t, .2, 1)), 95)
    reloj(c, 300, 430, 110, 12, 0); etiqueta(c, f"NOCHE {noche}", 800, 430, AMBAR, size=60, borde=AMBAR)
    h = Hi(); h.rect((0, 380, 70, 1350), fill=(4, 3, 6)); c.alpha_composite(h.done()); vineta(c, .7)
    return camera(c, t, d, 1.0, 1.06)

def e6(t, d):
    c = vgrad(W, H, NOCHE).copy(); ojo_grande(c, W / 2, 950, 760, 0.0); etiqueta(c, "CERRADO", W / 2, 1300, (180, 190, 230), size=56, alpha=eo(pr(t, .6, .4)))
    vineta(c, .8); return camera(c, t, d, 1.0, 1.05)

def e7(t, d):  # re-gancho
    c = vgrad(W, H, [(0, (40, 0, 10)), (1, (6, 0, 2))]).copy()
    contador(c, 8, t, W / 2, 960, (255, 255, 255), 520, "", 0.0, .01)
    etiqueta(c, "LA OCTAVA NOCHE", W / 2, 1380, (255, 120, 120), size=56, alpha=eo(pr(t, .3, .3)), borde=ROJO)
    if t < .12: c.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(220 * (1 - t / .12)))))
    vineta(c, .7); return camera(c, t, d, 1.15, 1.0)

def e8(t, d):
    c = vgrad(W, H, NOCHE).copy(); haz_linterna(c, 40, 1500, -40, 1500, 6, 120)
    ojo_grande(c, 640, 760, 640, eo(pr(t, .2, .25)), (0, 0), True); vineta(c, .75)
    return camera(c, t, d, 1.0, 1.1, 40, -40)

def e9(t, d):
    c = vgrad(W, H, [(0, (20, 4, 10)), (1, (4, 0, 2))]).copy(); k = pulso(c, t, 80 + 60 * t / d)
    glow(c, W / 2, 960, 300, ROJO, int(80 + 100 * k)); place(c, corazon_oscuro(520), W / 2, 960, scale=.9 + .18 * k)
    return camera(c, t, d, 1.0, 1.1)

def e10(t, d):
    c = vgrad(W, H, [(0, (20, 14, 12)), (1, (8, 6, 6))]).copy(); tablas(c, t, .5 * (1 - eio(pr(t, .4, 1.2))), y0=760)
    niebla(c, t, 1150, (140, 120, 100), 50); vineta(c, .8); return camera(c, t, d, 1.08, 1.0)

def e11(t, d):
    c = noche_casa().copy(); col = (255, 40, 60) if int(t * 4) % 2 else (40, 100, 255)
    glow(c, 520, 1450, 260, col, 120); policia(c, 380, 1360); policia(c, 660, 1360)
    reloj(c, 900, 220, 80, 4, 0); vineta(c, .6); return camera(c, t, d, 1.0, 1.08)

def e12(t, d):
    c = vgrad(W, H, [(0, (26, 20, 24)), (1, (8, 6, 8))]).copy(); tablas(c, t, 0, y0=1240, n=6)
    for x in (300, 780):
        policia(c, x, 980, .75); h = Hi(); h.rect((x - 110, 1150, x + 110, 1180), fill=(50, 30, 20)); c.alpha_composite(h.done())
    glow(c, 540, 1500, 120, ROJO, int(60 + 60 * math.sin(t * 6))); etiqueta(c, "JUSTO ENCIMA", W / 2, 640, AMBAR, size=54, alpha=eo(pr(t, .5, .4)), borde=AMBAR)
    vineta(c, .6); return camera(c, t, d, 1.0, 1.06)

def e13(t, d):
    c = vgrad(W, H, [(0, (40, 0, 8)), (1, (6, 0, 2))]).copy(); k = pulso(c, t, 140, fuerza=1.4)
    glow(c, W / 2, 960, 340, ROJO, int(100 + 120 * k)); place(c, corazon_oscuro(640), W / 2 + math.sin(t * 50) * 8 * k, 960, scale=.9 + .3 * k)
    return camera(c, t, d, 1.0, 1.18)

def e14(t, d):
    c = vgrad(W, H, [(0, (20, 14, 12)), (1, (8, 6, 6))]).copy(); lv = eb(pr(t, d * .45, .4))
    tablas(c, t, lv, y0=760)
    if lv > .3: glow(c, W / 2, 1110, 300, AMBAR, int(160 * lv))
    narrador(c, 540, 1500, .8, (255, 80, 80)); vineta(c, .6)
    return camera(c, t, d, 1.0, 1.1)

def e15(t, d):
    c = vgrad(W, H, [(0, (10, 8, 20)), (1, (2, 2, 6))]).copy(); narrador(c, W / 2, 1180, 1.25, (180, 60, 60))
    k = pulso(c, t, 70, fuerza=.8); glow(c, W / 2, 950, 70 + 30 * k, ROJO, 230, 30); return camera(c, t, d, 1.0, 1.12)

def e16(t, d): return escena_cierre(M, t, d, "¿MÁS TERROR CLÁSICO?")

ESCENAS = [
    (e1, "Un hombre jura que no está loco… mientras te cuenta cómo cometió un crimen.", {"loco", "crimen"}),
    (e2, "Es El corazón delator, el cuento de terror que Edgar Allan Poe publicó en mil ochocientos cuarenta y tres.", {"delator", "poe"}),
    (e3, "El narrador vive con un anciano. No lo odia, no quiere su dinero… pero no soporta uno de sus ojos.", {"anciano", "ojos"}),
    (e4, "Un ojo azul pálido, cubierto por un velo… como el ojo de un buitre.", {"buitre"}),
    (e5, "Durante siete noches, a medianoche, abre su puerta y asoma una linterna… muy, muy despacio.", {"siete", "medianoche"}),
    (e6, "Pero el ojo siempre está cerrado. Y sin ver ese ojo, no se atreve.", {"cerrado"}),
    (e7, "Hasta que llega la octava noche.", {"octava"}),
    (e8, "El anciano despierta. Y el rayo de la linterna cae justo sobre el ojo abierto.", {"despierta", "ojo"}),
    (e9, "Entonces el narrador escucha algo: el latido de un corazón… cada vez más fuerte.", {"latido", "fuerte"}),
    (e10, "Esa noche, el anciano muere. Y él esconde el cuerpo bajo las tablas del piso.", {"tablas"}),
    (e11, "A las cuatro de la mañana llega la policía: un vecino escuchó un grito.", {"policía", "grito"}),
    (e12, "Él, muy tranquilo, los invita a sentarse… justo encima del escondite.", {"encima"}),
    (e13, "Pero empieza a oír el latido otra vez. Más fuerte. ¡Más fuerte!", {"latido"}),
    (e14, "No lo soporta más, y confiesa gritando: ¡levanten las tablas!", {"confiesa", "tablas"}),
    (e15, "¿Era el corazón del anciano… o el peso de su propia culpa?", {"culpa"}),
    (e16, "¿Quieres más clásicos de terror? Comenta y síguenos en Comics Store.", {"terror"}),
]

if __name__ == "__main__":
    render(ESCENAS, sys.argv[1] if len(sys.argv) > 1 else "/home/claude/corazon_delator.mp4", regancho_idx=6, musica="terror")
