"""Visuales por escena: íconos con volumen (dibujados con código) y gráficas animadas.
Cada visual se dibuja dentro de una caja (x0, y0, x1, y1) en el tiempo t de la escena."""
import math
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFilter, ImageFont

def _mix(a, b, k): return tuple(int(a[i] * (1 - k) + b[i] * k) for i in range(3))

def _grad(size, top, bot):
    w, h = size; g = Image.new("RGB", (1, h))
    for y in range(h): g.putpixel((0, y), _mix(top, bot, y / max(1, h - 1)))
    return g.resize((w, h))

def _fill(canvas, mask, top, bot, outline=(15, 15, 22), ow=10):
    """Rellena 'mask' con degradado (efecto volumen) + contorno + brillo."""
    S = canvas.size[0]
    body = _grad(canvas.size, top, bot).convert("RGBA"); body.putalpha(mask)
    if ow:
        edge = mask.filter(ImageFilter.MaxFilter(ow * 2 + 1))
        ol = Image.new("RGBA", canvas.size, outline + (255,)); ol.putalpha(edge)
        canvas.alpha_composite(ol)
    canvas.alpha_composite(body)

def _shine(canvas, mask, box, alpha=110):
    hl = Image.new("L", canvas.size, 0); ImageDraw.Draw(hl).ellipse(box, fill=alpha)
    hl = Image.composite(hl, Image.new("L", canvas.size, 0), mask).filter(ImageFilter.GaussianBlur(10))
    w = Image.new("RGBA", canvas.size, (255, 255, 255, 255)); w.putalpha(hl); canvas.alpha_composite(w)

def _shadow(img):
    S = img.size[0]; out = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    sh = Image.new("RGBA", (S, S), (0, 0, 0, 0)); a = img.getchannel("A").point(lambda v: int(v * .55))
    sh.putalpha(a); sh = sh.filter(ImageFilter.GaussianBlur(14))
    out.alpha_composite(sh, (10, 18)); out.alpha_composite(img); return out

def _M(S): return Image.new("L", (S, S), 0)

@lru_cache(maxsize=64)
def icono(nombre, texto="", S=420):
    c = Image.new("RGBA", (S, S), (0, 0, 0, 0)); u = S / 100
    P = lambda pts: [(x * u, y * u) for x, y in pts]
    B = lambda b: tuple(v * u for v in b)
    if nombre == "trofeo":
        m = _M(S); d = ImageDraw.Draw(m)
        d.pieslice(B((24, -2, 76, 58)), 0, 180, fill=255); d.rectangle(B((24, 8, 76, 28)), fill=255)
        d.rectangle(B((45, 55, 55, 72)), fill=255); d.rounded_rectangle(B((30, 72, 70, 86)), int(3 * u), fill=255)
        h = _M(S); hd = ImageDraw.Draw(h)
        for bx in ((8, 12, 34, 44), (66, 12, 92, 44)): hd.arc(B(bx), 0, 360, fill=255, width=int(6 * u))
        hd.rectangle(B((24, 0, 76, 50)), fill=0); m = Image.composite(Image.new("L", (S, S), 255), m, h)
        _fill(c, m, (255, 230, 110), (190, 120, 20)); _shine(c, m, B((30, 10, 48, 40)))
        ImageDraw.Draw(c).polygon(P([(50, 22), (54, 32), (64, 32), (56, 38), (59, 48), (50, 42), (41, 48), (44, 38), (36, 32), (46, 32)]), fill=(255, 250, 220))
    elif nombre == "calendario":
        m = _M(S); ImageDraw.Draw(m).rounded_rectangle(B((12, 14, 88, 90)), int(10 * u), fill=255)
        _fill(c, m, (255, 255, 255), (205, 210, 225))
        t = _M(S); td = ImageDraw.Draw(t); td.rounded_rectangle(B((12, 14, 88, 40)), int(10 * u), fill=255); td.rectangle(B((12, 30, 88, 40)), fill=255)
        _fill(c, t, (255, 90, 90), (190, 20, 40), ow=0)
        d = ImageDraw.Draw(c)
        for x in (30, 70): d.rounded_rectangle(B((x - 4, 6, x + 4, 22)), int(3 * u), fill=(60, 60, 70))
        if texto:
            f = ImageFont.truetype("/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf", int(36 * u))
            d.text((50 * u, 66 * u), texto, font=f, fill=(30, 30, 40), anchor="mm")
    elif nombre == "cronometro":
        m = _M(S); d = ImageDraw.Draw(m); d.ellipse(B((14, 18, 86, 90)), fill=255); d.rounded_rectangle(B((43, 4, 57, 18)), int(3 * u), fill=255)
        _fill(c, m, (235, 240, 250), (140, 150, 170)); dd = ImageDraw.Draw(c)
        dd.ellipse(B((22, 26, 78, 82)), fill=(250, 252, 255), outline=(30, 30, 40), width=int(2 * u))
        for i in range(12):
            a = i * math.pi / 6; dd.line([(50 * u + math.sin(a) * 23 * u, 54 * u - math.cos(a) * 23 * u), (50 * u + math.sin(a) * 26 * u, 54 * u - math.cos(a) * 26 * u)], fill=(30, 30, 40), width=int(1.5 * u))
        dd.line([(50 * u, 54 * u), (50 * u, 34 * u)], fill=(220, 40, 50), width=int(3 * u)); dd.line([(50 * u, 54 * u), (64 * u, 60 * u)], fill=(30, 30, 40), width=int(3 * u))
        _shine(c, m, B((22, 22, 50, 44)), 80)
    elif nombre == "ojo":
        m = _M(S); d = ImageDraw.Draw(m); d.chord(B((4, 22, 96, 110)), 200, 340, fill=255); d.chord(B((4, -10, 96, 78)), 20, 160, fill=255)
        _fill(c, m, (255, 255, 255), (210, 215, 225))
        ir = _M(S); ImageDraw.Draw(ir).ellipse(B((32, 28, 68, 64)), fill=255); ir = Image.composite(ir, _M(S), m)
        _fill(c, ir, (150, 255, 120), (20, 140, 60), ow=0)
        ImageDraw.Draw(c).ellipse(B((42, 38, 58, 54)), fill=(10, 10, 15)); ImageDraw.Draw(c).ellipse(B((52, 34, 60, 42)), fill=(255, 255, 255))
    elif nombre in ("balon", "baloncesto"):
        m = _M(S); ImageDraw.Draw(m).ellipse(B((8, 8, 92, 92)), fill=255)
        if nombre == "balon":
            _fill(c, m, (255, 255, 255), (190, 195, 205)); d = ImageDraw.Draw(c)
            def pent(cx, cy, r, rot=0): return [(cx * u + r * u * math.sin(rot + i * 2 * math.pi / 5), cy * u - r * u * math.cos(rot + i * 2 * math.pi / 5)) for i in range(5)]
            d.polygon(pent(50, 50, 14), fill=(25, 25, 30))
            for i in range(5):
                a = i * 2 * math.pi / 5; d.polygon(pent(50 + 34 * math.sin(a), 50 - 34 * math.cos(a), 11, math.pi), fill=(25, 25, 30))
            c.putalpha(Image.composite(c.getchannel("A"), _M(S), m.filter(ImageFilter.MaxFilter(21))))
        else:
            _fill(c, m, (255, 160, 60), (200, 80, 10)); d = ImageDraw.Draw(c); w = int(2.5 * u)
            d.line(B((8, 50, 92, 50)), fill=(30, 15, 5), width=w); d.line(B((50, 8, 50, 92)), fill=(30, 15, 5), width=w)
            d.arc(B((-30, 14, 38, 86)), -60, 60, fill=(30, 15, 5), width=w); d.arc(B((62, 14, 130, 86)), 120, 240, fill=(30, 15, 5), width=w)
        _shine(c, m, B((20, 14, 52, 40)))
    elif nombre == "control":
        m = _M(S); d = ImageDraw.Draw(m); d.rounded_rectangle(B((8, 30, 92, 70)), int(18 * u), fill=255)
        d.ellipse(B((6, 40, 40, 90)), fill=255); d.ellipse(B((60, 40, 94, 90)), fill=255)
        _fill(c, m, (70, 70, 90), (20, 20, 30)); d = ImageDraw.Draw(c)
        d.rectangle(B((20, 46, 34, 52)), fill=(200, 200, 210)); d.rectangle(B((24, 42, 30, 56)), fill=(200, 200, 210))
        for (x, y, col) in [(72, 42, (90, 220, 90)), (80, 49, (240, 70, 70)), (64, 49, (70, 140, 255)), (72, 56, (250, 210, 60))]:
            d.ellipse(B((x - 4, y - 4, x + 4, y + 4)), fill=col)
        _shine(c, m, B((14, 30, 60, 46)), 60)
    elif nombre == "alerta":
        m = _M(S); ImageDraw.Draw(m).polygon(P([(50, 6), (95, 88), (5, 88)]), fill=255)
        _fill(c, m, (255, 230, 80), (230, 150, 10)); d = ImageDraw.Draw(c)
        d.rounded_rectangle(B((45, 32, 55, 64)), int(4 * u), fill=(30, 25, 10)); d.ellipse(B((44, 70, 56, 82)), fill=(30, 25, 10))
    elif nombre == "grafica":
        d = ImageDraw.Draw(c)
        for i, h in enumerate((22, 38, 54, 72)):
            m = _M(S); ImageDraw.Draw(m).rounded_rectangle(B((10 + i * 21, 92 - h, 26 + i * 21, 92)), int(3 * u), fill=255)
            _fill(c, m, (140, 255, 120), (20, 150, 60), ow=6)
        a = _M(S); ImageDraw.Draw(a).line(P([(8, 64), (34, 44), (52, 52), (84, 18)]), fill=255, width=int(6 * u))
        ImageDraw.Draw(a).polygon(P([(90, 10), (90, 30), (72, 16)]), fill=255)
        _fill(c, a, (255, 255, 255), (220, 220, 230), ow=6)
    elif nombre == "corazon":
        m = _M(S); d = ImageDraw.Draw(m); d.ellipse(B((8, 14, 54, 58)), fill=255); d.ellipse(B((46, 14, 92, 58)), fill=255)
        d.polygon(P([(10, 44), (90, 44), (50, 92)]), fill=255)
        _fill(c, m, (255, 90, 120), (190, 10, 50)); _shine(c, m, B((16, 18, 40, 38)))
    elif nombre == "lupa":
        m = _M(S); d = ImageDraw.Draw(m); d.ellipse(B((8, 8, 66, 66)), fill=255); d.line(P([(58, 58), (90, 90)]), fill=255, width=int(14 * u))
        _fill(c, m, (90, 90, 110), (30, 30, 40)); d = ImageDraw.Draw(c); d.ellipse(B((16, 16, 58, 58)), fill=(170, 220, 255))
        _shine(c, m, B((18, 18, 40, 34)), 140)
    elif nombre == "rayo":
        m = _M(S); ImageDraw.Draw(m).polygon(P([(58, 4), (18, 56), (46, 56), (36, 96), (82, 38), (54, 38)]), fill=255)
        _fill(c, m, (255, 245, 120), (240, 160, 0)); _shine(c, m, B((30, 10, 56, 40)))
    elif nombre == "sonido":
        m = _M(S); d = ImageDraw.Draw(m); d.rectangle(B((10, 38, 28, 62)), fill=255); d.polygon(P([(26, 38), (50, 18), (50, 82), (26, 62)]), fill=255)
        _fill(c, m, (230, 235, 245), (130, 140, 160)); d = ImageDraw.Draw(c)
        for i, r in enumerate((14, 26, 38)):
            d.arc(B((50 - r, 50 - r, 50 + r + 10, 50 + r)), -50, 50, fill=(90, 230, 120), width=int(5 * u))
    elif nombre == "dinero":
        m = _M(S); ImageDraw.Draw(m).ellipse(B((10, 10, 90, 90)), fill=255)
        _fill(c, m, (255, 225, 100), (200, 140, 20)); d = ImageDraw.Draw(c)
        d.ellipse(B((20, 20, 80, 80)), outline=(170, 110, 10), width=int(3 * u))
        f = ImageFont.truetype("/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf", int(46 * u))
        d.text((50 * u, 52 * u), "$", font=f, fill=(150, 95, 5), anchor="mm"); _shine(c, m, B((20, 16, 50, 40)))
    else:
        return icono("rayo", "", S)
    return _shadow(c)

ICONOS = ["trofeo", "calendario", "cronometro", "ojo", "balon", "baloncesto", "control", "alerta", "grafica", "corazon", "lupa", "rayo", "sonido", "dinero"]

# ---------------------------------------------------------------- dibujo en escena
def dibujar(c, v, t, box, col, F, FR, text_layer, put, ease_out, ease_back, prog, fit_size):
    x0, y0, x1, y1 = box; W = x1 - x0; H = y1 - y0; cx = (x0 + x1) / 2
    tipo = v.get("tipo", "icono")
    if tipo == "icono":
        size = int(min(W, H) * .95)
        put(c, icono(v.get("nombre", "rayo"), str(v.get("texto", ""))).resize((size, size), Image.LANCZOS),
            cx, (y0 + y1) / 2 + math.sin(t * 2.2) * 10, scale=ease_back(prog(t, .15, .55)), rot=math.sin(t * 1.6) * 5)
    elif tipo == "barra":
        val = float(v["valor"]); mx = float(v.get("max", 100)); k = ease_out(prog(t, .3, 1.4))
        bw, bh = W - 60, 90; bx = x0 + 30; by = (y0 + y1) / 2 - 10
        lab = v.get("etiqueta", "")
        if lab: put(c, text_layer(lab.upper(), fit_size(lab.upper(), 46, bw), fill=(235, 235, 245)), cx, by - 110, alpha=ease_out(prog(t, .2, .4)))
        L = Image.new("RGBA", c.size, (0, 0, 0, 0)); d = ImageDraw.Draw(L)
        d.rounded_rectangle((bx, by, bx + bw, by + bh), 45, fill=(20, 20, 30, 230), outline=(255, 255, 255, 60), width=3)
        fw = int(bw * val / mx * k)
        if fw > 40:
            g = Image.new("RGBA", (fw, bh)); gg = _grad((fw, bh), _mix(col, (255, 255, 255), .35), col).convert("RGBA")
            m = Image.new("L", (fw, bh), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, fw - 1, bh - 1), 45, fill=255); gg.putalpha(m)
            L.alpha_composite(gg, (bx, int(by)))
        c.alpha_composite(L)
        num = f"{val * k:.0f}{v.get('unidad', '%')}"
        put(c, text_layer(num, 120, fill=(255, 255, 255), stroke=6, stroke_fill=(0, 0, 0)), cx, by + bh + 90, scale=.9 + .1 * ease_back(prog(t, 1.5, .4)))
        if v.get("nota"):
            put(c, text_layer(v["nota"], fit_size(v["nota"], 40, bw), fill=col), cx, by + bh + 185, alpha=ease_out(prog(t, 1.6, .4)))
    elif tipo == "comparar":
        items = v["items"]; mx = max(float(i[1]) for i in items); n = len(items)
        rowh = min(150, H / n); cols = v.get("colores") or [col, (90, 160, 255), (255, 200, 60), (230, 90, 120)]
        for i, it in enumerate(items):
            k = ease_out(prog(t, .3 + i * .35, 1.1)); y = y0 + rowh * i + rowh * .15
            put(c, text_layer(str(it[0]).upper(), 40, fill=(235, 235, 245)), x0 + 30 + text_layer(str(it[0]).upper(), 40).width / 2, y + 20, alpha=ease_out(prog(t, .2 + i * .35, .3)))
            bw = (W - 60) * float(it[1]) / mx * k; ccol = tuple(cols[i % len(cols)])
            L = Image.new("RGBA", c.size, (0, 0, 0, 0)); d = ImageDraw.Draw(L)
            d.rounded_rectangle((x0 + 30, y + 50, x1 - 30, y + 50 + rowh * .38), 22, fill=(20, 20, 30, 200))
            if bw > 30: d.rounded_rectangle((x0 + 30, y + 50, x0 + 30 + bw, y + 50 + rowh * .38), 22, fill=ccol)
            c.alpha_composite(L)
            lbl = str(it[2]) if len(it) > 2 else f"{float(it[1]) * k:,.0f}".replace(",", ".") + v.get("unidad", "")
            put(c, text_layer(lbl, 40, fill=(255, 255, 255), stroke=4, stroke_fill=(0, 0, 0)),
                min(x1 - 120, x0 + 40 + bw + 90), y + 50 + rowh * .19, alpha=ease_out(prog(t, .6 + i * .35, .3)))
    elif tipo == "tabla":
        filas = v["filas"]; hl = set(v.get("resaltar", [])); out = set(v.get("eliminados", []))
        rowh = min(78, H / len(filas)); fs = int(rowh * .62)
        for i, f in enumerate(filas):
            k = ease_out(prog(t, .2 + i * .09, .45)); y = y0 + i * rowh
            L = Image.new("RGBA", c.size, (0, 0, 0, 0)); d = ImageDraw.Draw(L)
            fill = col + (235,) if i in hl else ((150, 30, 40, 200) if i in out else (16, 16, 26, 205))
            d.rounded_rectangle((x0 + 20, y + 4, x1 - 20, y + rowh - 4), 14, fill=fill, outline=(255, 255, 255, 40), width=2)
            off = int((1 - k) * 300)
            if k > 0:
                Lc = L.crop((0, 0, c.size[0], c.size[1])); c.alpha_composite(Lc, (0, 0)) if off == 0 else c.alpha_composite(L.crop((0, 0, c.size[0] - off, c.size[1])), (off, 0))
                tc = (10, 10, 15) if i in hl else (240, 240, 248)
                put(c, text_layer(str(f[0]), fs, fill=tc), x0 + 65 + off, y + rowh / 2, alpha=k)
                nm = text_layer(str(f[1]), fs, fill=tc)
                put(c, nm, x0 + 110 + nm.width / 2 + off, y + rowh / 2, alpha=k)
                put(c, text_layer(str(f[2]), fs, fill=tc), x1 - 75 + off, y + rowh / 2, alpha=k)
    elif tipo == "lista":
        if v.get("titulo"):
            put(c, text_layer(v["titulo"].upper(), 64, fill=col, stroke=4, stroke_fill=(0, 0, 0)), cx, y0 + 40, scale=ease_back(prog(t, .1, .4)))
        items = v["items"]; rowh = min(105, (H - 90) / len(items))
        for i, it in enumerate(items):
            k = ease_out(prog(t, .4 + i * .25, .4)); y = y0 + 95 + i * rowh
            L = Image.new("RGBA", c.size, (0, 0, 0, 0)); d = ImageDraw.Draw(L)
            hi = i in set(v.get("resaltar", []))
            d.rounded_rectangle((x0 + 60, y, x1 - 60, y + rowh - 14), 20, fill=(col + (int(235 * k),)) if hi else (16, 16, 26, int(215 * k)), outline=col + (int(200 * k),), width=3)
            c.alpha_composite(L)
            put(c, text_layer(str(it), fit_size(str(it), 52, W - 180), fill=(10, 10, 15) if hi else (245, 245, 250)), cx, y + (rowh - 14) / 2, alpha=k, scale=.85 + .15 * k)
