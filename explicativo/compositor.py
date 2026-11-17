"""Compositor de escenas declarativas para historias (terror, misterio, leyendas).
Una escena es un dict:
  {"fondo": "cementerio", "el": [("dama", x, y, escala, {"anim": "flotar"}), ...], "fx": ["niebla", "lluvia"],
   "cam": (z0, z1, dx, dy), "tag": "1907", "pulso": 0, "luz": (x, y, r, (r,g,b))}
Lo estático se compone una vez; lo animado se dibuja por cuadro."""
import math, random, os
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFilter, ImageChops
from lib import *
import visuales as V

NEGRO = (8, 6, 12)

# ================================================================ FONDOS
def _cielo(pal, estrellas=True, luna=None, seed=5):
    c = vgrad(W, H, pal)
    if estrellas:
        h = Hi(); rnd = random.Random(seed)
        for _ in range(110):
            x, y, r = rnd.uniform(0, W), rnd.uniform(0, H * .55), rnd.uniform(1, 2.8); h.ellipse((x - r, y - r, x + r, y + r), fill=(230, 230, 255, rnd.randint(80, 220)))
        c.alpha_composite(h.done())
    if luna:
        x, y, r = luna; glow(c, x, y, r * 2.2, (200, 210, 255), 80); h = Hi(); h.ellipse((x - r, y - r, x + r, y + r), fill=(236, 236, 222))
        h.ellipse((x - r * .4, y - r * .5, x - r * .05, y - r * .15), fill=(214, 214, 200)); h.ellipse((x + r * .2, y + r * .2, x + r * .5, y + r * .5), fill=(214, 214, 200)); c.alpha_composite(h.done())
    return c

def _colinas(c, base, col, seed, amp=40):
    h = Hi(); rnd = random.Random(seed); ph = [rnd.uniform(0, 6) for _ in range(3)]; pts = [(0, H)]
    for x in range(0, W + 20, 20): pts.append((x, base - amp * math.sin(x / 210 + ph[0]) - amp * .5 * math.sin(x / 90 + ph[1]) - amp * .3 * math.sin(x / 41 + ph[2])))
    pts.append((W, H)); h.poly(pts, fill=col); c.alpha_composite(h.done())

def _arbol_seco(h, x, y, s=1., col=NEGRO, seed=1):
    rnd = random.Random(seed)
    def rama(x0, y0, ang, largo, grosor, n):
        x1 = x0 + math.cos(ang) * largo; y1 = y0 - math.sin(ang) * largo; h.line([(x0, y0), (x1, y1)], fill=col, width=max(2, grosor))
        if n > 0:
            for da in (-.5, .45): rama(x1, y1, ang + da + rnd.uniform(-.2, .2), largo * .7, int(grosor * .65), n - 1)
    rama(x, y, math.pi / 2 + rnd.uniform(-.1, .1), 260 * s, int(30 * s), 5)

def _bosque_siluetas(c, base, col, n=9, seed=2, s=1.):
    h = Hi(); rnd = random.Random(seed)
    for i in range(n):
        x = rnd.uniform(-50, W + 50); hh = rnd.uniform(300, 600) * s; w = hh * .32
        h.poly([(x, base - hh), (x - w, base), (x + w, base)], fill=col); h.rect((x - 10, base - 20, x + 10, base + 20), fill=col)
    c.alpha_composite(h.done())

BIB = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "biblioteca", "fondos")
def fondo_img_existe(nombre):
    import glob
    return bool(glob.glob(os.path.join(BIB, "h" if HORIZONTAL else "v", f"{nombre}.*")))

def fondo_img(nombre):
    """Fondo de la biblioteca (imágenes generadas por Fernando) según la orientación, o None."""
    import glob
    hits = sorted(glob.glob(os.path.join(BIB, "h" if HORIZONTAL else "v", f"{nombre}.*")))
    if not hits: return None
    from PIL import ImageEnhance
    im = Image.open(hits[0]).convert("RGB")
    im = ImageEnhance.Brightness(ImageEnhance.Color(im).enhance(.85)).enhance(.78).convert("RGBA")   # un poco más oscuro para que resalten siluetas y textos
    s = max(W / im.width, H / im.height)
    im = im.resize((int(im.width * s + .5), int(im.height * s + .5)), Image.LANCZOS)
    return im.crop(((im.width - W) // 2, (im.height - H) // 2, (im.width - W) // 2 + W, (im.height - H) // 2 + H))

@lru_cache(maxsize=32)
def fondo(nombre):
    im = fondo_img(nombre)
    if im is not None: return im
    if not HORIZONTAL: return _fondo_codigo(nombre)
    # respaldo horizontal: dibujar en vertical y recortar la franja del horizonte a pantalla completa
    import lib as _l
    g = globals(); saved = (g["W"], g["H"], _l.W, _l.H); g["W"], g["H"], _l.W, _l.H = 1080, 1920, 1080, 1920
    try: v = _fondo_codigo(nombre)
    finally: g["W"], g["H"], _l.W, _l.H = saved
    band = v.crop((0, 500, 1080, 1500)).resize((1920, int(1000 * 1920 / 1080)), Image.LANCZOS)
    return band.crop((0, (band.height - 1080) // 2, 1920, (band.height - 1080) // 2 + 1080))

def _fondo_codigo(nombre):
    N = [(0, (6, 8, 22)), (.6, (24, 26, 56)), (1, (8, 8, 16))]
    if nombre == "bosque":
        c = _cielo(N, luna=(780, 580, 80)); _bosque_siluetas(c, 1250, (16, 20, 34), 10, 3, 1.1); _bosque_siluetas(c, 1400, (10, 12, 20), 9, 5, 1.3)
        h = Hi(); h.rect((0, 1400, W, H), fill=(8, 10, 14)); c.alpha_composite(h.done())
    elif nombre == "cementerio":
        c = _cielo(N, luna=(300, 590, 90)); _colinas(c, 1250, (18, 20, 36), 4)
        h = Hi(); h.rect((0, 1380, W, H), fill=(10, 10, 18))
        _arbol_seco(h, 900, 1380, 1.2, (6, 6, 10), 7)
        for i, (x, y, s) in enumerate([(160, 1440, 1), (420, 1470, 1.2), (690, 1430, .9), (300, 1600, 1.4), (820, 1620, 1.3)]):
            col = (40 + i * 4, 42 + i * 4, 56 + i * 4)
            if i % 2: h.rect((x - 60 * s, y - 150 * s, x + 60 * s, y), r=60 * s, fill=col)
            else: h.rect((x - 14 * s, y - 190 * s, x + 14 * s, y), fill=col); h.rect((x - 60 * s, y - 150 * s, x + 60 * s, y - 120 * s), fill=col)
        c.alpha_composite(h.done())
    elif nombre == "casa":
        from lib import noche_casa; c = noche_casa().copy()
    elif nombre == "granja":  # casa aislada en el campo (Vermont)
        c = _cielo(N, luna=(820, 580, 70)); _colinas(c, 1180, (20, 24, 40), 8, 70); _bosque_siluetas(c, 1260, (12, 14, 24), 12, 9, .8)
        h = Hi(); h.rect((0, 1300, W, H), fill=(10, 12, 16))
        h.poly([(300, 1350), (300, 1080), (520, 900), (740, 1080), (740, 1350)], fill=(14, 12, 20)); h.rect((560, 1150, 660, 1270), fill=(255, 196, 110)); c.alpha_composite(h.done())
        glow(c, 610, 1210, 120, (255, 190, 90), 130)
    elif nombre == "mar":
        c = _cielo([(0, (8, 12, 26)), (.55, (30, 40, 70)), (1, (6, 10, 20))], luna=(760, 580, 70))
        h = Hi(); h.rect((0, 1150, W, H), fill=(10, 20, 36))
        for i in range(14): h.line([(0, 1170 + i * 55), (W, 1170 + i * 55)], fill=(24, 40, 66), width=4)
        c.alpha_composite(h.done())
    elif nombre == "tormenta_mar":
        c = vgrad(W, H, [(0, (14, 16, 22)), (.5, (40, 46, 60)), (1, (8, 12, 20))]); h = Hi(); h.rect((0, 1150, W, H), fill=(12, 22, 34))
        for i in range(12): h.arc((i * 120 - 120, 1080 + (i % 3) * 30, i * 120 + 120, 1260 + (i % 3) * 30), 180, 360, fill=(36, 56, 80), width=10)
        c.alpha_composite(h.done())
    elif nombre == "cuarto":
        from lib import cuarto_oscuro; c = cuarto_oscuro().copy()
    elif nombre == "habitacion":  # dormitorio con cama de frente y ventana
        c = vgrad(W, H, [(0, (22, 18, 34)), (1, (8, 6, 12))]); h = Hi()
        h.rect((300, 420, 780, 900), r=10, fill=(26, 34, 70)); h.rect((300, 420, 780, 900), r=10, outline=(14, 10, 18), width=20); h.line([(540, 420), (540, 900)], fill=(14, 10, 18), width=14)
        h.rect((0, 1350, W, H), fill=(30, 22, 26))
        h.rect((180, 1050, 900, 1250), r=20, fill=(60, 50, 70)); h.rect((140, 1200, 940, 1420), r=26, fill=(210, 206, 220)); h.rect((240, 1120, 480, 1210), r=40, fill=(236, 234, 240)); h.rect((140, 1380, 940, 1460), fill=(14, 10, 14))
        c.alpha_composite(h.done()); glow(c, 540, 660, 220, (120, 140, 230), 60)
    elif nombre == "biblioteca":
        c = vgrad(W, H, [(0, (34, 22, 16)), (1, (10, 6, 4))]); h = Hi(); rnd = random.Random(4)
        for sy in range(300, 1300, 200):
            h.rect((40, sy + 170, W - 40, sy + 190), fill=(60, 36, 22)); x = 60
            while x < W - 80:
                w = rnd.randint(26, 48); hh = rnd.randint(120, 165); h.rect((x, sy + 170 - hh, x + w, sy + 170), fill=random.Random(x + sy).choice([(110, 40, 30), (40, 60, 90), (90, 80, 40), (50, 80, 50), (120, 100, 70)])); x += w + 4
        h.rect((0, 1380, W, H), fill=(26, 16, 12)); h.rect((200, 1300, 880, 1360), fill=(70, 44, 28)); c.alpha_composite(h.done())
    elif nombre == "pasillo":
        c = vgrad(W, H, [(0, (40, 30, 30)), (1, (10, 8, 8))]); h = Hi(); vx, vy = 540, 820
        h.poly([(0, 0), (vx - 80, vy - 120), (vx - 80, vy + 120), (0, H)], fill=(60, 40, 36)); h.poly([(W, 0), (vx + 80, vy - 120), (vx + 80, vy + 120), (W, H)], fill=(52, 34, 30))
        h.poly([(0, H), (vx - 80, vy + 120), (vx + 80, vy + 120), (W, H)], fill=(90, 30, 30)); h.rect((vx - 80, vy - 120, vx + 80, vy + 120), fill=(20, 14, 14))
        for k in range(5):
            f = .25 + k * .17; y0 = vy - 120 - (vy - 120) * f * .9; y1 = vy + 120 + (H - vy - 120) * f * .9
            for side in (-1, 1):
                x = vx + side * (80 + (W / 2 - 80) * f * .95); h.line([(x, y0 + 80 * f), (x, y1 - 160 * f)], fill=(30, 20, 18), width=int(6 + 10 * f))
        c.alpha_composite(h.done())
        for k in range(3): glow(c, 540, 260 + k * 160, 50 + k * 10, (255, 220, 160), 120)
    elif nombre == "hotel_nieve":
        c = _cielo([(0, (20, 26, 44)), (.6, (70, 84, 110)), (1, (200, 210, 225))], estrellas=False); _colinas(c, 900, (110, 120, 140), 3, 120); _colinas(c, 1000, (150, 160, 178), 6, 80)
        h = Hi(); h.rect((0, 1250, W, H), fill=(226, 232, 240))
        h.rect((140, 900, 940, 1260), fill=(40, 34, 40)); h.poly([(110, 910), (540, 760), (970, 910)], fill=(30, 26, 32))
        for r in range(3):
            for k in range(8):
                lit = (r * 8 + k) % 5 == 0; h.rect((180 + k * 95, 950 + r * 100, 230 + k * 95, 1010 + r * 100), fill=(255, 200, 110) if lit else (20, 18, 24))
        for x in range(0, W, 140): h.poly([(x, 1260), (x + 40, 1120), (x + 80, 1260)], fill=(30, 50, 46))
        c.alpha_composite(h.done())
    elif nombre == "calle":
        c = _cielo([(0, (8, 10, 22)), (.6, (30, 28, 50)), (1, (10, 10, 16))], estrellas=False); h = Hi()
        for (x, w, hh) in [(0, 220, 700), (210, 180, 560), (380, 240, 820), (610, 200, 620), (800, 280, 760)]:
            h.rect((x, 1250 - hh, x + w, 1300), fill=(18, 18, 30))
            for yy in range(1300 - hh + 40, 1250, 90):
                for xx in range(x + 30, x + w - 30, 60):
                    if (xx * 7 + yy) % 5 == 0: h.rect((xx, yy, xx + 30, yy + 44), fill=(255, 210, 120))
        h.rect((0, 1300, W, H), fill=(22, 22, 30)); h.rect((0, 1290, W, 1320), fill=(46, 46, 58))
        h.line([(860, 1300), (860, 860)], fill=(30, 30, 36), width=14); h.line([(860, 870), (780, 870)], fill=(30, 30, 36), width=10)
        c.alpha_composite(h.done()); glow(c, 780, 900, 180, (255, 230, 170), 120)
    elif nombre == "japon":  # callejón japonés de noche con faroles
        c = _cielo([(0, (14, 8, 22)), (.6, (40, 22, 46)), (1, (10, 8, 14))], estrellas=False); h = Hi()
        for side, x in ((-1, 0), (1, W)):
            h.poly([(x, 300), (x - side * 330, 640), (x - side * 330, 1400), (x, 1600)], fill=(24, 16, 26))
        h.rect((0, 1400, W, H), fill=(20, 16, 22))
        for i, (x, y) in enumerate([(270, 760), (810, 760), (330, 1000), (750, 1000)]):
            h.ellipse((x - 46, y - 64, x + 46, y + 64), fill=(220, 60, 50)); h.rect((x - 30, y - 74, x + 30, y - 60), fill=(30, 20, 20)); h.rect((x - 30, y + 60, x + 30, y + 74), fill=(30, 20, 20))
        c.alpha_composite(h.done())
        for (x, y) in [(270, 760), (810, 760), (330, 1000), (750, 1000)]: glow(c, x, y, 110, (255, 120, 80), 120)
    elif nombre == "rio":
        c = _cielo(N, luna=(540, 580, 70)); _bosque_siluetas(c, 1150, (14, 18, 30), 12, 11, .9)
        h = Hi(); h.rect((0, 1150, W, H), fill=(12, 24, 40))
        for i in range(10): h.line([(80 + i * 40, 1180 + i * 70), (1000 - i * 40, 1180 + i * 70)], fill=(30, 50, 80), width=3)
        h.poly([(0, 1150), (300, 1150), (0, H)], fill=(10, 14, 12)); h.poly([(W, 1150), (W - 300, 1150), (W, H)], fill=(10, 14, 12)); c.alpha_composite(h.done())
        glow(c, 540, 1300, 200, (140, 170, 220), 50)
    elif nombre == "fiesta":  # salón de baile antiguo
        c = vgrad(W, H, [(0, (40, 18, 30)), (1, (12, 6, 10))]); h = Hi()
        for x in range(60, W, 190): h.rect((x, 300, x + 60, 1300), fill=(60, 30, 40))
        h.rect((0, 1300, W, H), fill=(50, 26, 22))
        for i in range(12):
            x = (i % 6) * 190; y = 1300 + (i // 6) * 300; h.rect((x, y, x + 95, y + 150), fill=(70, 40, 30)); h.rect((x + 95, y + 150, x + 190, y + 300), fill=(70, 40, 30))
        c.alpha_composite(h.done())
        for x in (270, 810): glow(c, x, 380, 160, (255, 200, 120), 140)
    elif nombre == "abismo":  # cósmico / dimensión
        c = vgrad(W, H, [(0, (4, 10, 14)), (.5, (10, 40, 44)), (1, (2, 6, 8))]); rnd = random.Random(8); h = Hi()
        for _ in range(160):
            x, y, r = rnd.uniform(0, W), rnd.uniform(0, H), rnd.uniform(1, 3); h.ellipse((x - r, y - r, x + r, y + r), fill=(160, 255, 220, rnd.randint(60, 200)))
        c.alpha_composite(h.done()); glow(c, 540, 900, 420, (40, 200, 160), 60)
    elif nombre == "ciudad_antigua":  # R'lyeh: geometría imposible
        c = vgrad(W, H, [(0, (8, 22, 24)), (.6, (20, 50, 50)), (1, (4, 12, 14))]); h = Hi(); rnd = random.Random(12)
        for i in range(14):
            x = rnd.uniform(-80, W); w = rnd.uniform(120, 260); hh = rnd.uniform(400, 1000); sk = rnd.uniform(-120, 120)
            h.poly([(x, 1500), (x + sk, 1500 - hh), (x + w + sk * .6, 1500 - hh * .9), (x + w, 1500)], fill=(14 + i * 2, 36 + i * 2, 38 + i * 2))
        h.rect((0, 1480, W, H), fill=(8, 20, 24)); c.alpha_composite(h.done())
    elif nombre == "estudio":
        c = vgrad(W, H, ESTUDIO)
    elif nombre == "negro":
        c = Image.new("RGBA", (W, H), (4, 3, 6, 255))
    elif nombre == "carretera":
        c = _cielo(N, estrellas=False); h = Hi(); h.rect((0, 1150, W, H), fill=(12, 12, 16))
        h.poly([(470, 1150), (610, 1150), (1000, H), (80, H)], fill=(30, 30, 36))
        for i in range(6): y = 1180 + i * 130; h.rect((530 - i * 6, y, 550 + i * 6, y + 40 + i * 12), fill=(220, 210, 160))
        c.alpha_composite(h.done()); glow(c, 540, 1150, 140, (255, 230, 170), 90)
    elif nombre == "motel":
        c = _cielo(N, estrellas=False); h = Hi(); h.rect((0, 1350, W, H), fill=(14, 14, 18)); h.rect((40, 1050, 1040, 1350), fill=(30, 26, 30)); h.rect((20, 1020, 1060, 1060), fill=(20, 18, 22))
        for i in range(6):
            x = 80 + i * 160; h.rect((x, 1150, x + 70, 1340), fill=(16, 14, 18)); h.rect((x + 90, 1170, x + 140, 1230), fill=(255, 210, 130) if i in (1, 4) else (40, 36, 44))
        h.rect((780, 700, 1000, 820), r=12, fill=(30, 10, 14)); h.rect((880, 820, 900, 1020), fill=(40, 36, 40)); c.alpha_composite(h.done())
        etiqueta(c, "MOTEL", 890, 760, (255, 80, 90), size=56); glow(c, 890, 760, 200, (255, 60, 80), 110)
    elif nombre == "espacio":
        c = _cielo([(0, (2, 3, 10)), (.6, (6, 10, 26)), (1, (2, 3, 8))]); glow(c, 760, 1500, 520, (90, 140, 200), 90)
        h = Hi(); h.ellipse((300, 1250, 1300, 2250), fill=(40, 60, 80)); c.alpha_composite(h.done())
    elif nombre == "nave":  # pasillo de nave espacial
        c = vgrad(W, H, [(0, (10, 14, 16)), (1, (4, 6, 8))]); h = Hi()
        for i in range(7):
            k = 1 - i * .12; w_, hh = 900 * k, 1300 * k; h.rect((540 - w_ / 2, 1000 - hh / 2, 540 + w_ / 2, 1000 + hh / 2), r=60 * k, outline=(40 + i * 6, 60 + i * 6, 60 + i * 6), width=max(3, int(16 * k)))
        for y in (500, 1500): h.line([(0, y), (W, y)], fill=(30, 40, 40), width=6)
        c.alpha_composite(h.done()); glow(c, 540, 1000, 200, (120, 255, 200), 60)
    elif nombre == "suburbio":
        c = _cielo([(0, (20, 12, 30)), (.6, (60, 30, 40)), (1, (14, 10, 16))], luna=(820, 600, 70)); h = Hi(); h.rect((0, 1350, W, H), fill=(14, 12, 14))
        for x, w_, hh in ((40, 360, 300), (560, 420, 340)):
            h.rect((x, 1350 - hh, x + w_, 1350), fill=(26, 20, 26)); h.poly([(x - 30, 1350 - hh), (x + w_ / 2, 1350 - hh - 160), (x + w_ + 30, 1350 - hh)], fill=(20, 16, 20))
            h.rect((x + 60, 1350 - hh + 80, x + 140, 1350 - hh + 160), fill=(255, 196, 110))
        for x in (470, 1010): _arbol_seco(h, x, 1350, .9, (8, 6, 10), int(x))
        c.alpha_composite(h.done())
    elif nombre == "desierto":  # excavación en el desierto al atardecer
        c = vgrad(W, H, [(0, (40, 20, 30)), (.45, (190, 90, 40)), (.62, (240, 160, 80)), (1, (90, 50, 30))]); glow(c, 540, 1080, 260, (255, 210, 120), 200)
        h = Hi(); h.ellipse((440, 980, 640, 1180), fill=(255, 220, 150))
        h.poly([(0, 1250), (300, 1150), (620, 1240), (900, 1160), (W, 1230), (W, H), (0, H)], fill=(150, 80, 40))
        h.poly([(0, 1420), (380, 1330), (760, 1420), (W, 1360), (W, H), (0, H)], fill=(110, 58, 32))
        for x in (180, 820): h.rect((x - 50, 1180, x + 50, 1330), fill=(120, 66, 36)); h.rect((x - 70, 1165, x + 70, 1190), fill=(130, 74, 40))
        c.alpha_composite(h.done())
    elif nombre == "iglesia":
        c = vgrad(W, H, [(0, (10, 8, 16)), (1, (24, 16, 20))]); h = Hi()
        for x in (200, 540, 880):
            h.rect((x - 90, 500, x + 90, 1000), r=90, fill=(40, 46, 80)); h.line([(x, 520), (x, 1000)], fill=(20, 18, 30), width=10); h.line([(x - 90, 760), (x + 90, 760)], fill=(20, 18, 30), width=10)
        h.rect((0, 1380, W, H), fill=(18, 12, 14)); h.rect((330, 1160, 750, 1380), fill=(50, 30, 26)); h.rect((300, 1140, 780, 1170), fill=(200, 190, 170))
        h.rect((520, 860, 560, 1100), fill=(200, 170, 90)); h.rect((470, 910, 610, 945), fill=(200, 170, 90))
        c.alpha_composite(h.done())
        for x in (360, 720): glow(c, x, 1100, 90, (255, 190, 100), 160)
    elif nombre == "cine":
        c = vgrad(W, H, [(0, (6, 6, 12)), (1, (16, 10, 14))]); glow(c, 540, 820, 520, (170, 190, 255), 120)
        h = Hi(); h.rect((90, 560, 990, 1080), fill=(190, 200, 230))
        for r in range(4):
            y = 1300 + r * 160
            for i in range(-1, 8):
                x = i * 160 + (r % 2) * 80; h.ellipse((x - 62, y - 70, x + 62, y + 50), fill=(12 + r * 4, 10, 16)); h.rect((x - 72, y, x + 72, y + 120), r=20, fill=(60 + r * 10, 14, 24))
        c.alpha_composite(h.done())
    else:
        c = vgrad(W, H, N)
    return c

# ================================================================ FIGURAS (siluetas con luz de borde)
@lru_cache(maxsize=64)
def figura(tipo, rim=(255, 170, 110), col=(10, 8, 14)):
    h = Hi(440, 900)
    def cuerpo(cc, o=0):
        if tipo in ("hombre", "policia", "anciano", "nino"):
            sh = .78 if tipo == "nino" else 1
            cx = 220 + o; top = 900 - 860 * sh
            hr = 62 * sh; h.ellipse((cx - hr, top, cx + hr, top + hr * 2), fill=cc)
            h.rect((cx - 100 * sh, top + hr * 2 + 10, cx + 100 * sh, top + 520 * sh), r=60 * sh, fill=cc)
            h.rect((cx - 140 * sh, top + hr * 2 + 30, cx - 90 * sh, top + 460 * sh), r=24 * sh, fill=cc); h.rect((cx + 90 * sh, top + hr * 2 + 30, cx + 140 * sh, top + 460 * sh), r=24 * sh, fill=cc)
            h.rect((cx - 80 * sh, top + 480 * sh, cx - 14 * sh, 895), r=26 * sh, fill=cc); h.rect((cx + 14 * sh, top + 480 * sh, cx + 80 * sh, 895), r=26 * sh, fill=cc)
            if tipo == "policia": h.rect((cx - 70, top - 30, cx + 70, top + 30), r=10, fill=cc); h.rect((cx - 90, top + 20, cx + 90, top + 40), fill=cc)
            if tipo == "anciano": h.line([(cx + 150, top + 300), (cx + 190, 895)], fill=cc, width=14)
        elif tipo in ("mujer", "dama", "llorona"):
            cx = 220 + o; top = 40
            h.ellipse((cx - 56, top, cx + 56, top + 124), fill=cc)
            hair = 520 if tipo == "llorona" else 240
            h.rect((cx - 70, top + 30, cx + 70, top + hair), r=60, fill=cc)
            h.poly([(cx - 70, top + 140), (cx + 70, top + 140), (cx + 190, 895), (cx - 190, 895)], fill=cc)
            h.rect((cx - 120, top + 150, cx - 76, top + 420), r=22, fill=cc); h.rect((cx + 76, top + 150, cx + 120, top + 420), r=22, fill=cc)
            if tipo == "llorona":
                h.line([(cx - 110, top + 360), (cx - 60, top + 120)], fill=cc, width=40); h.line([(cx + 110, top + 360), (cx + 60, top + 120)], fill=cc, width=40)
        elif tipo == "sombra":
            cx = 220 + o; h.ellipse((cx - 70, 60, cx + 70, 210), fill=cc); h.poly([(cx - 90, 200), (cx + 90, 200), (cx + 150, 895), (cx - 150, 895)], fill=cc)
            for k in range(-2, 3): h.line([(cx + k * 30, 880), (cx + k * 50, 900)], fill=cc, width=26)
        elif tipo == "perro":
            h.ellipse((60 + o, 560, 360 + o, 760), fill=cc); h.ellipse((300 + o, 470, 430 + o, 600), fill=cc); h.rect((380 + o, 520, 440 + o, 575), r=20, fill=cc)
            for x in (90, 150, 260, 320): h.rect((x + o, 700, x + 34 + o, 890), r=14, fill=cc)
            h.poly([(310 + o, 500), (330 + o, 420), (360 + o, 490)], fill=cc); h.line([(70 + o, 600), (10 + o, 520)], fill=cc, width=22)
    cuerpo(rim, 7); cuerpo(col, 0)
    if tipo in ("dama", "llorona"):
        im = h.done(); return im
    return h.done()

def dama_blanca():
    return figura("dama", (190, 220, 255), (226, 232, 244))

def llorona_fig():
    return figura("llorona", (170, 210, 255), (214, 222, 238))

# ================================================================ OBJETOS
@lru_cache(maxsize=64)
def objeto(tipo, var=""):
    if tipo == "vela":
        h = Hi(120, 320); h.rect((30, 120, 90, 320), r=10, fill=(236, 226, 200)); h.ellipse((44, 40, 76, 125), fill=(255, 210, 120)); h.ellipse((52, 70, 68, 120), fill=(255, 250, 220)); return h.done()
    if tipo == "carta":
        h = Hi(520, 380); h.rect((10, 10, 510, 370), r=10, fill=(232, 220, 190)); h.poly([(10, 10), (260, 200), (510, 10)], fill=(214, 200, 168))
        for y in range(230, 340, 34): h.line([(60, y), (460, y)], fill=(150, 130, 100), width=4)
        return h.done()
    if tipo == "libro":
        return libro_antiguo(var.split("|")[0] if var else "", var.split("|")[1] if "|" in var else "")
    if tipo == "lapida":
        h = Hi(360, 460); h.rect((20, 20, 340, 460), r=150, fill=(90, 92, 104)); h.rect((40, 40, 320, 460), r=130, fill=(110, 112, 126))
        im = h.done()
        if var: d = ImageDraw.Draw(im); d.text((180, 240), var, font=F(44), fill=(50, 50, 60), anchor="mm")
        return im
    if tipo == "pata_mono":
        h = Hi(360, 520); col = (90, 64, 44); dk = (60, 40, 28)
        h.rect((130, 260, 230, 520), r=40, fill=col); h.ellipse((80, 120, 280, 330), fill=col)
        for i, (x, a) in enumerate([(100, -25), (150, -8), (205, 8), (255, 25)]):
            h.line([(x, 160), (x + a, 20 + abs(a))], fill=col, width=40); h.ellipse((x + a - 22, abs(a), x + a + 22, 44 + abs(a)), fill=dk)
        h.line([(90, 230), (30, 170)], fill=col, width=40)
        return h.done()
    if tipo == "almohadon":
        h = Hi(620, 320); h.rect((10, 10, 610, 310), r=120, fill=(238, 236, 244)); h.arc((60, 40, 560, 280), 200, 340, fill=(214, 212, 224), width=8)
        if var == "manchas":
            for (x, y, r) in [(220, 160, 14), (260, 190, 9), (300, 150, 6), (400, 200, 11)]: h.ellipse((x - r, y - r, x + r, y + r), fill=(110, 40, 50))
        return h.done()
    if tipo == "criatura":  # parásito: bola oscura con patitas
        h = Hi(300, 220); h.ellipse((60, 50, 240, 190), fill=(40, 20, 30))
        for k in range(4):
            for s in (-1, 1): h.line([(150 + s * 60, 110 + k * 18), (150 + s * 130, 80 + k * 40)], fill=(40, 20, 30), width=10)
        h.ellipse((110, 80, 130, 100), fill=(255, 60, 60)); h.ellipse((170, 80, 190, 100), fill=(255, 60, 60)); return h.done()
    if tipo == "cilindro":  # cerebro en cilindro (Lovecraft)
        h = Hi(320, 560); h.rect((40, 60, 280, 540), r=30, fill=(150, 170, 180)); h.rect((60, 90, 260, 500), r=20, fill=(30, 60, 70))
        h.ellipse((90, 200, 230, 330), fill=(220, 150, 160)); h.ellipse((40, 30, 280, 100), fill=(180, 200, 210))
        for k in range(3): h.ellipse((120 + k * 30, 520, 140 + k * 30, 540), fill=(80, 255, 160))
        return h.done()
    if tipo == "alado":  # Mi-Go: criatura alada con pinzas (silueta)
        h = Hi(600, 520); cc = (60, 40, 50)
        h.ellipse((220, 160, 380, 420), fill=cc); h.ellipse((240, 90, 360, 200), fill=(120, 60, 90))
        for s in (-1, 1):
            h.poly([(300 + s * 60, 220), (300 + s * 290, 80), (300 + s * 260, 300)], fill=(40, 30, 40))
            h.line([(300 + s * 70, 330), (300 + s * 170, 440)], fill=cc, width=18); h.poly([(300 + s * 170, 440), (300 + s * 210, 420), (300 + s * 190, 480)], fill=cc)
        return h.done()
    if tipo == "idolo":  # ídolo de criatura con tentáculos (Cthulhu, dominio público)
        h = Hi(460, 640); st = (70, 110, 90); dk = (40, 70, 58)
        h.rect((90, 520, 370, 640), r=20, fill=(60, 60, 54))
        h.poly([(130, 520), (330, 520), (360, 300), (100, 300)], fill=st)
        h.ellipse((120, 90, 340, 320), fill=st)
        for i in range(6):
            x = 150 + i * 32; h.line([(x, 260), (x + (i - 2.5) * 14, 420), (x + (i - 2.5) * 30, 480)], fill=dk, width=20)
        for s in (-1, 1): h.poly([(230 + s * 90, 200), (230 + s * 230, 60), (230 + s * 210, 300)], fill=dk)
        h.ellipse((170, 170, 200, 200), fill=(200, 255, 120)); h.ellipse((260, 170, 290, 200), fill=(200, 255, 120))
        return h.done()
    if tipo == "barco":
        h = Hi(620, 460); h.poly([(20, 280), (600, 280), (520, 400), (100, 400)], fill=(30, 24, 22)); h.rect((280, 40, 300, 290), fill=(30, 24, 22))
        h.poly([(300, 60), (300, 260), (480, 260)], fill=(200, 196, 180)); h.poly([(280, 80), (280, 250), (140, 250)], fill=(180, 176, 160)); return h.done()
    if tipo == "maquina":  # máquina de escribir
        h = Hi(560, 380); h.rect((40, 160, 520, 360), r=30, fill=(40, 40, 46)); h.rect((120, 40, 440, 190), r=10, fill=(236, 232, 220)); h.rect((90, 180, 470, 210), r=10, fill=(20, 20, 24))
        for r in range(3):
            for k in range(10): h.ellipse((90 + k * 40 + r * 10, 230 + r * 40, 116 + k * 40 + r * 10, 256 + r * 40), fill=(200, 200, 200))
        return h.done()
    if tipo == "triciclo":
        h = Hi(420, 320); h.ellipse((20, 160, 160, 300), outline=(30, 30, 40), width=16); h.ellipse((300, 200, 400, 300), outline=(30, 30, 40), width=14)
        h.line([(90, 230), (350, 250)], fill=(160, 30, 40), width=18); h.line([(150, 120), (110, 230)], fill=(160, 30, 40), width=16); h.rect((200, 150, 300, 180), r=10, fill=(30, 30, 40)); h.line([(120, 120), (190, 120)], fill=(30, 30, 40), width=12)
        return h.done()
    if tipo == "mascarilla":
        h = Hi(420, 280); h.rect((60, 40, 360, 240), r=90, fill=(240, 242, 246)); h.line([(60, 120), (0, 60)], fill=(220, 222, 230), width=10); h.line([(360, 120), (420, 60)], fill=(220, 222, 230), width=10)
        for y in (100, 140, 180): h.line([(100, y), (320, y)], fill=(210, 212, 220), width=4)
        return h.done()
    if tipo == "tijeras":
        h = Hi(300, 520); m = (200, 206, 216)
        h.poly([(130, 20), (160, 20), (180, 300), (140, 300)], fill=m); h.poly([(170, 20), (140, 20), (120, 300), (160, 300)], fill=(170, 176, 186))
        h.ellipse((60, 290, 160, 400), outline=(30, 30, 36), width=24); h.ellipse((140, 290, 240, 400), outline=(30, 30, 36), width=24); return h.done()
    if tipo == "chaqueta":
        h = Hi(460, 480); cc = (60, 50, 44); h.poly([(120, 40), (340, 40), (440, 160), (400, 470), (60, 470), (20, 160)], fill=cc)
        h.poly([(190, 40), (230, 200), (270, 40)], fill=(236, 232, 224)); h.line([(230, 200), (230, 470)], fill=(40, 34, 30), width=8)
        for y in (260, 330, 400): h.ellipse((240, y, 256, y + 16), fill=(200, 170, 90))
        return h.done()
    if tipo == "mano":
        h = Hi(360, 420); sk = (232, 190, 160); h.rect((90, 200, 270, 420), r=60, fill=sk)
        for i, x in enumerate((100, 145, 190, 235)): h.rect((x, 40 + abs(i - 1.5) * 20, x + 38, 260), r=19, fill=sk)
        h.line([(90, 300), (20, 220)], fill=sk, width=46); return h.done()
    if tipo == "lengua_mano":  # mano y lengua (perro bajo la cama) - sin gore
        im = objeto("mano").copy(); h = Hi(360, 420); h.ellipse((140, 330, 260, 420), fill=(230, 110, 130)); im.alpha_composite(h.done()); return im
    if tipo == "espejo":
        h = Hi(380, 560); h.ellipse((10, 10, 370, 550), fill=(120, 90, 40)); h.ellipse((40, 40, 340, 520), fill=(150, 170, 190)); h.line([(100, 120), (180, 80)], fill=(230, 240, 250), width=10); return h.done()
    if tipo == "agua_vaso":
        h = Hi(220, 320); h.poly([(20, 20), (200, 20), (180, 300), (40, 300)], fill=(200, 220, 240, 140)); h.poly([(30, 120), (190, 120), (180, 300), (40, 300)], fill=(140, 180, 230, 160))
        if var == "vacio": h.poly([(30, 120), (190, 120), (180, 300), (40, 300)], fill=(0, 0, 0, 0))
        return h.done()
    if tipo == "rosa":
        h = Hi(220, 420); h.line([(110, 140), (110, 420)], fill=(40, 90, 50), width=12); h.ellipse((50, 40, 170, 160), fill=(180, 20, 40)); h.ellipse((70, 60, 150, 140), fill=(140, 10, 30)); return h.done()
    if tipo == "telefono":
        h = Hi(320, 560); h.rect((20, 20, 300, 540), r=40, fill=(20, 20, 26)); h.rect((40, 70, 280, 470), r=10, fill=(60, 120, 200)); return h.done()
    if tipo == "tentaculo":
        h = Hi(300, 900); pts = []
        for i in range(40):
            y = 900 - i * 22; x = 150 + 70 * math.sin(i / 5); pts.append((x, y))
        for i in range(len(pts) - 1): h.line([pts[i], pts[i + 1]], fill=(30, 80, 70), width=max(8, 70 - i * 1.6))
        return h.done()
    if tipo == "piedra":
        h = Hi(460, 360); h.ellipse((10, 30, 450, 340), fill=(24, 22, 26)); h.ellipse((40, 50, 300, 160), fill=(44, 42, 48))
        for i in range(5):
            x = 80 + i * 70; h.arc((x, 170, x + 50, 220), 0, 300, fill=(120, 255, 200), width=6); h.line([(x + 10, 240), (x + 40, 280)], fill=(120, 255, 200), width=6)
        return h.done()
    if tipo == "mascara":
        h = Hi(360, 460); h.ellipse((20, 20, 340, 440), fill=(222, 196, 176)); h.ellipse((80, 150, 150, 210), fill=(20, 16, 18)); h.ellipse((210, 150, 280, 210), fill=(20, 16, 18))
        h.poly([(180, 220), (160, 300), (200, 300)], fill=(200, 170, 150)); h.line([(130, 350), (230, 350)], fill=(120, 70, 70), width=10); return h.done()
    if tipo == "auto":
        h = Hi(620, 300); h.rect((20, 120, 600, 240), r=40, fill=(40, 44, 56)); h.poly([(140, 120), (200, 40), (430, 40), (500, 120)], fill=(34, 38, 48))
        h.poly([(215, 55), (300, 55), (300, 115), (165, 115)], fill=(120, 150, 180)); h.poly([(320, 55), (420, 55), (470, 115), (320, 115)], fill=(120, 150, 180))
        for x in (140, 480): h.ellipse((x - 55, 190, x + 55, 300), fill=(14, 14, 16))
        h.ellipse((560, 150, 600, 180), fill=(255, 230, 160)); return h.done()
    if tipo == "llave":
        h = Hi(260, 420); h.ellipse((60, 10, 200, 150), outline=(214, 180, 90), width=24); h.rect((118, 140, 142, 400), fill=(214, 180, 90)); h.rect((142, 330, 200, 352), fill=(214, 180, 90)); h.rect((142, 370, 180, 392), fill=(214, 180, 90))
        h.rect((40, 160, 220, 230), r=10, fill=(150, 40, 40)); return h.done()
    if tipo == "pajaro":  # ave disecada sobre su base
        h = Hi(420, 460); col = (70, 60, 54); h.ellipse((90, 120, 330, 330), fill=col); h.ellipse((250, 60, 360, 170), fill=col); h.poly([(350, 110), (410, 125), (350, 140)], fill=(200, 160, 60))
        h.poly([(100, 160), (0, 80), (60, 260)], fill=(60, 50, 46)); h.ellipse((300, 95, 320, 115), fill=(250, 220, 120)); h.rect((60, 380, 360, 440), fill=(90, 60, 40)); h.line([(180, 320), (170, 380)], fill=(60, 50, 40), width=10); return h.done()
    if tipo == "mecedora":
        h = Hi(420, 560); col = (40, 30, 26); h.rect((90, 20, 120, 360), fill=col); h.rect((300, 20, 330, 360), fill=col); h.rect((90, 20, 330, 60), fill=col)
        h.rect((80, 300, 340, 340), fill=col); h.rect((90, 340, 110, 470), fill=col); h.rect((310, 340, 330, 470), fill=col); h.arc((-20, 380, 440, 560), 200, 340, fill=col, width=18); return h.done()
    if tipo == "huevo":
        h = Hi(320, 420); h.ellipse((30, 20, 290, 400), fill=(80, 90, 70)); h.ellipse((60, 60, 160, 200), fill=(110, 120, 96)); return h.done()
    if tipo == "gato":
        h = Hi(380, 360); col = (210, 150, 70); h.ellipse((60, 140, 300, 330), fill=col); h.ellipse((200, 40, 340, 170), fill=col)
        h.poly([(215, 60), (225, 0), (255, 50)], fill=col); h.poly([(285, 50), (315, 0), (330, 70)], fill=col); h.arc((0, 160, 140, 340), 90, 270, fill=col, width=20)
        h.ellipse((235, 90, 255, 112), fill=(30, 30, 20)); h.ellipse((290, 90, 310, 112), fill=(30, 30, 20)); return h.done()
    if tipo == "computadora":
        h = Hi(560, 460); h.rect((20, 20, 540, 360), r=20, fill=(30, 34, 40)); h.rect((50, 50, 510, 330), fill=(10, 30, 20))
        for i, w_ in enumerate((380, 260, 330, 200)): h.rect((80, 80 + i * 55, 80 + w_, 100 + i * 55), fill=(90, 255, 140))
        h.rect((200, 360, 360, 440), fill=(40, 44, 50)); return h.done()
    if tipo == "calabaza":
        h = Hi(440, 400); h.rect((205, 10, 235, 90), fill=(70, 90, 40))
        for x0 in (40, 120, 200): h.ellipse((x0, 70, x0 + 200, 380), fill=(230, 120, 30))
        h.poly([(140, 170), (190, 230), (100, 230)], fill=(255, 220, 90)); h.poly([(300, 170), (340, 230), (250, 230)], fill=(255, 220, 90)); h.poly([(110, 280), (330, 280), (300, 330), (140, 330)], fill=(255, 220, 90)); return h.done()
    if tipo == "casa_munecas":
        h = Hi(560, 560); h.poly([(20, 200), (280, 20), (540, 200)], fill=(110, 70, 60)); h.rect((40, 200, 520, 540), fill=(200, 180, 150))
        for (x, y) in ((60, 220), (290, 220), (60, 380), (290, 380)): h.rect((x, y, x + 210, y + 140), fill=(120, 100, 90)); h.rect((x + 70, y + 60, x + 110, y + 140), fill=(80, 60, 50))
        h.ellipse((150, 260, 180, 290), fill=(230, 200, 170)); h.rect((152, 290, 178, 340), fill=(60, 60, 80)); return h.done()
    if tipo == "fuego":
        h = Hi(360, 480); h.poly([(180, 0), (330, 300), (280, 470), (80, 470), (30, 300)], fill=(255, 120, 30)); h.poly([(180, 140), (270, 330), (230, 470), (130, 470), (90, 330)], fill=(255, 200, 60)); return h.done()
    if tipo == "radio":
        h = Hi(520, 340); h.rect((10, 60, 510, 330), r=30, fill=(90, 60, 40)); h.ellipse((40, 100, 240, 300), fill=(50, 34, 24)); h.rect((280, 110, 480, 170), r=8, fill=(230, 210, 150))
        for x in (310, 400): h.ellipse((x, 220, x + 60, 280), fill=(200, 180, 130)); 
        h.line([(380, 60), (470, 0)], fill=(160, 160, 160), width=6); return h.done()
    if tipo == "camara_video":
        h = Hi(560, 360); h.rect((20, 80, 400, 300), r=30, fill=(40, 40, 46)); h.poly([(400, 130), (540, 80), (540, 300), (400, 250)], fill=(30, 30, 36)); h.ellipse((60, 20, 160, 80), fill=(200, 30, 30))
        h.rect((60, 120, 200, 200), fill=(20, 60, 50)); return h.done()
    if tipo == "tienda":
        h = Hi(620, 420); h.poly([(20, 400), (310, 30), (600, 400)], fill=(60, 110, 70)); h.poly([(250, 400), (310, 160), (370, 400)], fill=(20, 30, 20)); return h.done()
    if tipo == "mapa":
        h = Hi(560, 420); h.poly([(20, 40), (190, 10), (370, 40), (540, 10), (540, 390), (370, 410), (190, 390), (20, 410)], fill=(220, 200, 150))
        h.line([(80, 330), (180, 250), (300, 280), (430, 150)], fill=(200, 60, 50), width=8); h.ellipse((410, 120, 460, 170), outline=(200, 60, 50), width=8); return h.done()
    if tipo == "caja_musica":
        h = Hi(460, 360); h.rect((30, 140, 430, 340), r=16, fill=(120, 70, 50)); h.poly([(30, 140), (80, 30), (480, 30), (430, 140)], fill=(150, 90, 60)); h.ellipse((200, 210, 260, 270), fill=(220, 190, 110)); h.rect((430, 220, 460, 240), fill=(200, 180, 120)); return h.done()
    if tipo == "taza":
        h = Hi(460, 380); h.ellipse((20, 300, 440, 370), fill=(220, 220, 225)); h.poly([(90, 120), (370, 120), (330, 320), (130, 320)], fill=(240, 240, 245)); h.ellipse((90, 90, 370, 150), fill=(200, 200, 205))
        h.ellipse((120, 100, 340, 140), fill=(90, 60, 40)); h.arc((330, 150, 430, 270), 270, 90, fill=(240, 240, 245), width=22); h.line([(250, 120), (380, 10)], fill=(190, 190, 200), width=12); return h.done()
    if tipo == "venado":
        h = Hi(460, 460); col = (60, 44, 34); h.ellipse((60, 200, 340, 340), fill=col); h.rect((280, 110, 330, 240), fill=col); h.ellipse((270, 70, 380, 150), fill=col)
        for x in (90, 140, 250, 300): h.rect((x, 320, x + 22, 450), fill=col)
        h.line([(300, 75), (270, 10), (240, 0)], fill=col, width=10); h.line([(340, 75), (380, 10), (420, 0)], fill=col, width=10); return h.done()
    if tipo == "camara_foto":
        h = Hi(520, 360); h.rect((20, 80, 500, 340), r=30, fill=(40, 40, 46)); h.rect((160, 30, 300, 90), r=10, fill=(40, 40, 46)); h.ellipse((170, 120, 350, 300), fill=(20, 20, 26)); h.ellipse((210, 160, 310, 260), fill=(70, 90, 120))
        h.rect((390, 110, 460, 150), fill=(240, 240, 220)); return h.done()
    if tipo == "cruz":
        h = Hi(240, 420); h.rect((95, 10, 145, 410), r=8, fill=(214, 180, 90)); h.rect((20, 100, 220, 150), r=8, fill=(214, 180, 90)); return h.done()
    if tipo == "ouija":
        h = Hi(620, 420); h.rect((10, 10, 610, 410), r=40, fill=(150, 104, 60)); h.rect((30, 30, 590, 390), r=30, outline=(70, 44, 24), width=6)
        h.arc((70, 70, 550, 380), 200, 340, fill=(60, 36, 20), width=8); h.arc((110, 140, 510, 420), 205, 335, fill=(60, 36, 20), width=8)
        h.ellipse((70, 60, 150, 140), fill=(240, 220, 120)); h.ellipse((470, 60, 550, 140), fill=(230, 230, 240)); return h.done()
    if tipo == "amuleto":
        h = Hi(260, 360); h.line([(130, 0), (130, 80)], fill=(150, 120, 80), width=6); h.ellipse((40, 70, 220, 330), fill=(96, 88, 70))
        h.ellipse((80, 150, 120, 185), fill=(30, 26, 22)); h.ellipse((140, 150, 180, 185), fill=(30, 26, 22)); h.rect((95, 230, 165, 250), r=6, fill=(30, 26, 22)); return h.done()
    if tipo == "estatua_alada":
        h = Hi(520, 760); col = (64, 58, 50)
        h.poly([(260, 220), (20, 60), (60, 330), (200, 360)], fill=col); h.poly([(260, 220), (500, 60), (460, 330), (320, 360)], fill=col)
        h.ellipse((200, 120, 320, 250), fill=col); h.rect((200, 240, 320, 560), r=40, fill=col); h.rect((160, 560, 360, 620), fill=(50, 46, 40)); h.rect((120, 620, 400, 700), fill=(44, 40, 36))
        h.ellipse((225, 165, 245, 185), fill=(255, 120, 60)); h.ellipse((275, 165, 295, 185), fill=(255, 120, 60)); return h.done()
    if tipo == "camara_cine":
        h = Hi(560, 460); h.ellipse((60, 10, 220, 170), outline=(200, 200, 210), width=14); h.ellipse((240, 10, 400, 170), outline=(200, 200, 210), width=14)
        h.rect((40, 170, 420, 380), r=24, fill=(60, 60, 70)); h.poly([(420, 220), (540, 170), (540, 380), (420, 330)], fill=(40, 40, 48)); h.rect((210, 380, 250, 460), fill=(50, 50, 56)); return h.done()
    if tipo == "claqueta":
        h = Hi(520, 460); h.rect((20, 140, 500, 440), r=12, fill=(24, 24, 28)); h.rect((20, 60, 500, 140), fill=(240, 240, 240))
        for i in range(5): h.poly([(20 + i * 100, 60), (70 + i * 100, 60), (20 + i * 100 + 50 - 30, 140), (20 + i * 100 - 30, 140)], fill=(24, 24, 28))
        for y in (220, 300, 380): h.line([(60, y), (460, y)], fill=(200, 200, 200), width=4)
        return h.done()
    if tipo == "estrella":
        h = Hi(300, 300); pts = [(150 + (140 if k % 2 == 0 else 60) * math.sin(math.pi * k / 5), 160 - (140 if k % 2 == 0 else 60) * math.cos(math.pi * k / 5)) for k in range(10)]
        h.poly(pts, fill=(255, 210, 60)); return h.done()
    if tipo == "retrato":
        h = Hi(400, 520); h.rect((10, 10, 390, 510), r=10, fill=(120, 86, 40)); h.rect((40, 40, 360, 480), fill=(200, 190, 170))
        h.ellipse((150, 120, 250, 230), fill=(90, 80, 70)); h.poly([(130, 230), (270, 230), (330, 480), (70, 480)], fill=(236, 232, 226)); h.rect((140, 110, 260, 300), r=40, fill=(60, 50, 44)); h.ellipse((160, 135, 240, 225), fill=(214, 196, 176))
        return h.done()
    if tipo == "dulces":
        h = Hi(460, 300)
        for i, (x, y, c) in enumerate([(120, 180, (255, 190, 60)), (240, 140, (255, 120, 80)), (350, 190, (250, 220, 120))]):
            h.ellipse((x - 60, y - 50, x + 60, y + 50), fill=c); h.poly([(x - 60, y), (x - 110, y - 40), (x - 110, y + 40)], fill=c); h.poly([(x + 60, y), (x + 110, y - 40), (x + 110, y + 40)], fill=c)
        return h.done()
    if tipo == "caldera":
        h = Hi(420, 600); h.rect((60, 120, 360, 560), r=60, fill=(80, 70, 66)); h.ellipse((60, 60, 360, 200), fill=(100, 90, 86)); h.ellipse((150, 260, 270, 380), fill=(230, 230, 220)); h.line([(210, 320), (250, 280)], fill=(200, 30, 30), width=10)
        h.rect((300, 20, 340, 120), fill=(70, 60, 56)); return h.done()
    return V.icono(tipo).resize((360, 360)) if tipo in V.ICONOS else Image.new("RGBA", (10, 10))

# ================================================================ EFECTOS DINÁMICOS
@lru_cache(maxsize=4)
def _capa_niebla(col=(160, 170, 210), a=80):
    L = Image.new("RGBA", (W * 2, 700), (0, 0, 0, 0)); d = ImageDraw.Draw(L); rnd = random.Random(2)
    for _ in range(26):
        x = rnd.uniform(0, W * 2); y = rnd.uniform(150, 550); r = rnd.uniform(160, 320); d.ellipse((x - r, y - r * .35, x + r, y + r * .35), fill=col + (a,))
    return L.filter(ImageFilter.GaussianBlur(45))

def fx_niebla(c, t, y=1250, col=(160, 170, 210), a=80):
    L = _capa_niebla(col, a); off = int((t * 40) % W); c.alpha_composite(L.crop((off, 0, off + W, 700)), (0, int(y - 350)))

def fx_lluvia(c, t, n=160, a=120):
    L = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L); rnd = random.Random(int(t * 30))
    for _ in range(n):
        x = rnd.uniform(0, W); y = rnd.uniform(0, H); d.line([(x, y), (x - 14, y + 60)], fill=(170, 190, 220, a), width=2)
    c.alpha_composite(L)

def fx_nieve(c, t, n=140):
    L = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L); rnd = random.Random(5)
    for i in range(n):
        x0, y0, sp, r = rnd.uniform(0, W), rnd.uniform(0, H), rnd.uniform(40, 120), rnd.uniform(2, 6)
        y = (y0 + t * sp) % H; x = x0 + 30 * math.sin(t + i); d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 255, 255, 200))
    c.alpha_composite(L)

def fx_rayo(c, t, periodo=3.2, fase=.8):
    k = (t + fase) % periodo
    if k < .08 or .16 < k < .22: c.alpha_composite(Image.new("RGBA", (W, H), (220, 230, 255, 150)))

def fx_parpadeo(c, t, x, y, r, col=(255, 200, 120)):
    k = .75 + .25 * math.sin(t * 13) * math.sin(t * 7.3); glow(c, x, y, r, col, int(170 * k), r * .5)

def fx_particulas(c, t, col=(160, 255, 220), n=40):
    L = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L); rnd = random.Random(9)
    for i in range(n):
        x0, y0, sp = rnd.uniform(0, W), rnd.uniform(0, H), rnd.uniform(15, 50); y = (y0 - t * sp) % H; x = x0 + 20 * math.sin(t * .8 + i); r = 2 + (i % 3)
        d.ellipse((x - r, y - r, x + r, y + r), fill=col + (int(120 + 100 * math.sin(t * 3 + i)),))
    c.alpha_composite(L)

# ================================================================ COMPOSICIÓN
SILUETAS = {"hombre", "mujer", "policia", "anciano", "nino", "sombra", "perro", "auto", "pajaro", "mecedora", "seto", "gato", "venado", "estatua_alada", "tienda"}
@lru_cache(maxsize=128)
def silueta(tipo, var="", rim=(255, 170, 110)):
    """Versión cinematográfica para fondos fotográficos: figura negra con borde de luz, bordes suaves y sombra."""
    im = _img_el_base(tipo, var)
    if im is None: return None
    a = im.getchannel("A"); pad = 40
    W2, H2 = im.width + pad * 2, im.height + pad * 2
    A = Image.new("L", (W2, H2), 0); A.paste(a, (pad, pad))
    out = Image.new("RGBA", (W2, H2), (0, 0, 0, 0))
    # halo suave de luz alrededor (luz de contorno)
    halo = A.filter(ImageFilter.GaussianBlur(10)).point(lambda v: int(v * .55))
    L = Image.new("RGBA", (W2, H2), rim + (0,)); L.putalpha(halo); out.alpha_composite(L)
    # borde de luz fino desplazado hacia arriba-izquierda
    edge = ImageChops.subtract(A, A.transform(A.size, Image.AFFINE, (1, 0, 3, 0, 1, 3)))
    E = Image.new("RGBA", (W2, H2), rim + (0,)); E.putalpha(edge.filter(ImageFilter.GaussianBlur(1.2)).point(lambda v: min(255, v * 2))); 
    body = Image.new("RGBA", (W2, H2), (8, 8, 12, 0)); body.putalpha(A.filter(ImageFilter.GaussianBlur(1.1)))
    out.alpha_composite(body); out.alpha_composite(E)
    return out

def _img_el(tipo, var=""):
    if FOTO_ACTIVA[0] and tipo in SILUETAS and var != "color":
        return silueta(tipo, var, (130, 180, 255) if var == "frio" else (255, 170, 110))
    return _img_el_base(tipo, var)
FOTO_ACTIVA = [False]

def _img_el_base(tipo, var=""):
    if tipo == "dama": return dama_blanca()
    if tipo == "llorona": return llorona_fig()
    if tipo in ("hombre", "mujer", "policia", "anciano", "nino", "sombra", "perro"):
        return figura(tipo, (255, 170, 110) if var != "frio" else (130, 180, 255))
    if tipo == "ojo": return None
    if tipo == "seto": return figura("perro", (90, 160, 90), (34, 86, 44))
    return objeto(tipo, var)

def _a_horizontal(spec):
    """Adapta una escena escrita en coordenadas verticales al lienzo horizontal."""
    if not HORIZONTAL or spec.get("h"): return spec
    sp = dict(spec)
    sp["el"] = [(e[0], X(e[1]), Y(e[2]), e[3] * KS) + tuple(e[4:]) for e in spec.get("el", [])]
    sp["glows"] = [(g[0] if False else X(g[0]), Y(g[1]), g[2] * KS) + tuple(g[3:]) for g in spec.get("glows", [])]
    sp["velas"] = [(X(v[0]), Y(v[1]), v[2] * KS) + tuple(v[3:]) for v in spec.get("velas", [])]
    if "tag_y" in spec: sp["tag_y"] = Y(spec["tag_y"])
    else: sp["tag_y"] = Y(560)
    sp["niebla_y"] = Y(spec.get("niebla_y", 1300))
    if "cam" in spec: z0, z1, dx, dy = spec["cam"]; sp["cam"] = (z0, z1, dx * 1.2, dy * .5)
    return sp

def escena(spec):
    """Devuelve f(t, d) a partir de la especificación."""
    spec = _a_horizontal(spec)
    base_cache = {}
    foto = fondo_img_existe(spec.get("fondo", "estudio"))
    def build_base():
        FOTO_ACTIVA[0] = foto
        c = fondo(spec.get("fondo", "estudio")).copy()
        for g in spec.get("glows", []): glow(c, *g)
        for el in spec.get("el", []):
            tipo, x, y, s = el[:4]; o = el[4] if len(el) > 4 else {}
            if o.get("anim"): continue
            im = _img_el(tipo, o.get("var", ""))
            if im is not None: place(c, im, x, y, scale=s, rot=o.get("rot", 0), alpha=o.get("alpha", 1))
        return c
    def f(t, d):
        if "b" not in base_cache: base_cache["b"] = build_base()
        FOTO_ACTIVA[0] = foto
        c = base_cache["b"].copy()
        for el in spec.get("el", []):
            tipo, x, y, s = el[:4]; o = el[4] if len(el) > 4 else {}
            a = o.get("anim")
            if not a: continue
            if tipo == "ojo":
                ojo_grande(c, x, y, 700 * s, eo(pr(t, o.get("t0", .2), .5)) if a == "abrir" else 1., (math.sin(t) * 25, 0), True); continue
            im = _img_el(tipo, o.get("var", "")); st = o.get("t0", .1); xx, yy, sc, rot, al = x, y, s, o.get("rot", 0), 1.
            if a == "entrar": sc = s * eb(pr(t, st, .5))
            elif a == "flotar": yy = y + math.sin(t * 1.6) * 18; al = .55 + .45 * eo(pr(t, st, .8))
            elif a == "aparecer": al = eo(pr(t, st, 1.0))
            elif a == "balancear": rot = rot + math.sin(t * 2.2) * 6
            elif a == "caminar_der": xx = x + (t / d) * o.get("dist", 300); yy = y + abs(math.sin(t * 6)) * -10
            elif a == "caminar_izq": xx = x - (t / d) * o.get("dist", 300); yy = y + abs(math.sin(t * 6)) * -10
            elif a == "acercar": sc = s * (1 + .5 * eio(t / d)); yy = y + 80 * eio(t / d)
            elif a == "temblar": xx = x + math.sin(t * 40) * 6; yy = y + math.cos(t * 33) * 4
            elif a == "caer": yy = y - 600 * (1 - eo(pr(t, st, .7)))
            elif a == "girar": rot = rot + t * 30
            elif a == "latir": sc = s * (1 + .12 * max(0, math.sin(t * 7)))
            elif a == "desvanecer": al = 1 - eo(pr(t, st, 1.2))
            if im is not None: place(c, im, xx, yy, scale=sc, rot=rot, alpha=al)
        fx = spec.get("fx", [])
        if "niebla" in fx: fx_niebla(c, t, spec.get("niebla_y", 1300))
        if "niebla_verde" in fx: fx_niebla(c, t, spec.get("niebla_y", 1300), (90, 200, 160), 70)
        if "lluvia" in fx: fx_lluvia(c, t)
        if "nieve" in fx: fx_nieve(c, t)
        if "rayo" in fx: fx_rayo(c, t)
        if "particulas" in fx: fx_particulas(c, t)
        if "chispas" in fx: fx_particulas(c, t, (255, 200, 120), 30)
        for (x, y, r, col) in spec.get("velas", []): fx_parpadeo(c, t, x, y, r, col)
        if spec.get("pulso"): pulso(c, t, spec.get("bpm", 80), fuerza=spec["pulso"])
        elif spec.get("vineta", .65): vineta(c, spec.get("vineta", .65))
        if spec.get("tag"): etiqueta(c, spec["tag"], W / 2, spec.get("tag_y", 560), spec.get("tag_col", (255, 210, 140)), size=spec.get("tag_size", 52), alpha=eo(pr(t, .4, .4)), borde=spec.get("tag_col", (255, 210, 140)))
        if spec.get("flash") and t < .12: c.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(210 * (1 - t / .12)))))
        z0, z1, dx, dy = spec.get("cam", (1.0, 1.08, 0, 0))
        return camera(c, t, d, z0, z1, dx, dy)
    f.__name__ = spec.get("id", "esc")
    return f

def historia(lista, marca_nombre="comics-store", pregunta="¿MÁS TERROR?"):
    """lista: [(spec_dict, frase, {claves})]. Agrega cierre de marca."""
    out = []
    for i, (spec, frase, clave) in enumerate(lista):
        spec = dict(spec); spec.setdefault("id", f"e{i + 1:02d}"); out.append((escena(spec), frase, clave))
    m = marca(marca_nombre)
    def cierre(t, d): return escena_cierre(m, t, d, pregunta)
    return out, cierre
