"""Genera fondos 'mercado de apuestas / trading' 1080x1920 para BitBot Sports y La Tabla FC."""
import random, math, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont
W, H = 1080, 1920
FB = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
F = lambda s: ImageFont.truetype(FB, s)
GREEN, RED, LIME, PURPLE, BLUE = (40, 230, 90), (235, 50, 60), (170, 255, 40), (150, 50, 230), (40, 150, 255)

def glow_layer(draw_fn, blur):
    L = Image.new("RGBA", (W, H), (0, 0, 0, 0)); draw_fn(ImageDraw.Draw(L))
    return L.filter(ImageFilter.GaussianBlur(blur))

def build(path, pitch=False, seed=7):
    rnd = random.Random(seed)
    im = Image.new("RGBA", (W, H))
    for y in range(H):
        k = y / H; ImageDraw.Draw(im).line([(0, y), (W, y)], fill=(int(14 - 8 * k), int(12 - 6 * k), int(30 - 18 * k), 255))
    # luces de estadio
    im.alpha_composite(glow_layer(lambda d: (d.ellipse((-300, -250, 500, 450), fill=PURPLE + (120,)),
                                              d.ellipse((650, -200, 1400, 420), fill=BLUE + (100,)),
                                              d.ellipse((-200, 1500, 600, 2200), fill=GREEN + (70,)),
                                              d.ellipse((700, 1350, 1400, 2100), fill=PURPLE + (90,))), 160))
    d = ImageDraw.Draw(im)
    # rejilla
    for x in range(0, W, 60): d.line([(x, 0), (x, H)], fill=(22, 52, 40))
    for y in range(0, H, 60): d.line([(0, y), (W, y)], fill=(22, 52, 40))
    if pitch:
        pc = (78, 82, 100)
        d.rectangle((60, 260, W - 60, H - 260), outline=pc, width=4); d.line([(60, H / 2), (W - 60, H / 2)], fill=pc, width=4)
        d.ellipse((W / 2 - 170, H / 2 - 170, W / 2 + 170, H / 2 + 170), outline=pc, width=4)
        d.rectangle((W / 2 - 260, 260, W / 2 + 260, 520), outline=pc, width=4); d.rectangle((W / 2 - 260, H - 520, W / 2 + 260, H - 260), outline=pc, width=4)
    # velas japonesas
    def candles(y0, y1, n, x0=30, x1=W - 30, trend=.6):
        price = 0.0; vals = []
        for i in range(n):
            o = price; c = o + rnd.gauss(trend, 3.2); hi = max(o, c) + abs(rnd.gauss(0, 1.6)); lo = min(o, c) - abs(rnd.gauss(0, 1.6))
            vals.append((o, c, hi, lo)); price = c
        mn = min(v[3] for v in vals); mx = max(v[2] for v in vals)
        Y = lambda v: y1 - (v - mn) / (mx - mn) * (y1 - y0)
        step = (x1 - x0) / n; body = step * .55; pts = []
        G = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(G)
        for i, (o, c, hi, lo) in enumerate(vals):
            x = x0 + i * step + step / 2; col = GREEN if c >= o else RED
            for dd in (gd, d):
                dd.line([(x, Y(hi)), (x, Y(lo))], fill=col + (200,), width=3)
                dd.rectangle((x - body / 2, min(Y(o), Y(c)), x + body / 2, max(Y(o), Y(c)) + 2), fill=col + (215,))
            pts.append((x, Y((o + c) / 2)))
        im.alpha_composite(G.filter(ImageFilter.GaussianBlur(8)))
        ma = [(pts[i][0], sum(p[1] for p in pts[max(0, i - 5):i + 1]) / len(pts[max(0, i - 5):i + 1])) for i in range(len(pts))]
        ImageDraw.Draw(im).line(ma, fill=LIME + (230,), width=4, joint="curve")
    candles(330, 820, 34)
    candles(1250, 1560, 26, trend=.3)
    d = ImageDraw.Draw(im)
    # línea con puntos
    pts = []; v = 0
    for i in range(12):
        v += rnd.uniform(-20, 45); pts.append((60 + i * 85, 1150 - v))
    im.alpha_composite(glow_layer(lambda g: g.line(pts, fill=LIME + (200,), width=10), 10))
    d = ImageDraw.Draw(im); d.line(pts, fill=LIME, width=4)
    for p in pts: d.ellipse((p[0] - 9, p[1] - 9, p[0] + 9, p[1] + 9), fill=(220, 255, 180))
    # paneles de cuotas
    def panel(x, y, rows):
        w, h = 330, 70 * len(rows) + 30
        d.rounded_rectangle((x, y, x + w, y + h), 18, fill=(10, 14, 22, 200), outline=GREEN + (160,), width=3)
        for i, (up, txt) in enumerate(rows):
            yy = y + 20 + i * 70; col = GREEN if up else RED
            tri = [(x + 30, yy + 40), (x + 58, yy + 40), (x + 44, yy + 14)] if up else [(x + 30, yy + 16), (x + 58, yy + 16), (x + 44, yy + 42)]
            d.polygon(tri, fill=col); d.text((x + 80, yy + 2), txt, font=F(40), fill=col)
    panel(W - 380, 120, [(True, "+1.75"), (False, "-2.10"), (True, "+3.25")])
    panel(40, 1640, [(True, "1.85"), (False, "3.40")])
    # ticker de mercado
    d.rounded_rectangle((40, 900, W - 40, 980), 16, fill=(8, 10, 16, 210), outline=PURPLE + (180,), width=3)
    d.text((70, 915), "LOCAL 1.85   EMPATE 3.40   VISITA 4.10   +2.5 1.92", font=F(36), fill=(220, 230, 240))
    # barras
    for i in range(9):
        hgt = rnd.randint(60, 260); x = 520 + i * 55
        d.rectangle((x, 1880 - hgt, x + 34, 1880), fill=(GREEN if i % 3 else LIME) + (150,))
    im.convert("RGB").save(path, quality=92)

if __name__ == "__main__":
    build("marcas/bitbot-sports/fondo.png", pitch=False, seed=7)
    build("marcas/la-tabla-fc/fondo.png", pitch=True, seed=11)
