#!/usr/bin/env python3
"""RECORTADOR DE SHORTS — saca clips verticales de un video largo de la fábrica.

Basado en el flujo de claude-shorts (MIT): transcribir con tiempos por palabra →
elegir los mejores tramos → ajustar los cortes a frases y silencios → encuadre
vertical 9:16 → subtítulos karaoke neón con los colores de la página.

Uso típico (Claude elige los tramos):
  1) python3 recortador/recortar.py VIDEO.mp4 --marca comics-store --solo-candidatos
     → deja transcripcion.json y candidatos.json en la carpeta de salida.
  2) Claude lee la transcripción con RUBRICA_claude-shorts.md y escribe segmentos.json:
     [{"start": 12.4, "end": 58.0, "gancho": "DOOM NO ERA EL VILLANO"}, ...]
  3) python3 recortador/recortar.py VIDEO.mp4 --marca comics-store --segmentos segmentos.json

Automático (sin revisar): python3 recortador/recortar.py VIDEO.mp4 --marca comics-store --n 4

Opciones: --min 30 --max 60 (segundos), --salida DIR, --cierre "TEXTO", --sin-cierre,
          --encuadre auto|centro|completo  (completo = video entero sobre fondo desenfocado)
"""
import os, sys, json, re, argparse, subprocess, statistics

AQUI = os.path.dirname(os.path.abspath(__file__)); KIT = os.path.dirname(AQUI)
sys.path.insert(0, AQUI)
from transcribir import transcribir
import cortes

W, H = 1080, 1920
GANCHO_PAL = ("nadie", "secreto", "verdad", "nunca", "jamás", "increíble", "por qué", "porqué", "error", "mentira",
              "prohibid", "oscuro", "real", "terrible", "peor", "mejor", "único", "imagina", "sabías", "atención", "cuidado",
              "muerte", "muere", "murió", "miedo", "sangre", "millones", "récord", "historia")


def ffprobe(path, campos):
    r = subprocess.run(["ffprobe", "-v", "quiet", "-select_streams", "v:0", "-show_entries", f"stream={campos}",
                        "-of", "json", path], capture_output=True, text=True)
    return json.loads(r.stdout)["streams"][0]


# ---------- 1. candidatos automáticos (respaldo si Claude no elige) ----------
def puntuar(frases, i, j):
    texto = " ".join(f["text"] for f in frases[i:j]).lower()
    primera = frases[i]["text"].lower()
    gancho = 30 * ("?" in primera or "¿" in primera) + 25 * bool(re.search(r"\d", primera)) + \
             15 * sum(p in primera for p in GANCHO_PAL) + 10 * ("!" in primera or "¡" in primera)
    arranque_flojo = -40 * bool(re.match(r"^(y |pero |entonces |así que |como dije|por eso )", primera))
    intensidad = 6 * texto.count("!") + 4 * texto.count("?") + 5 * len(re.findall(r"\d+", texto)) + \
                 4 * sum(texto.count(p) for p in GANCHO_PAL)
    cierre = 20 * (frases[j - 1]["text"][-1:] in ".?!")
    return min(gancho, 100) * 0.30 + min(intensidad, 100) * 0.25 + cierre + arranque_flojo


def candidatos(trans, n, dmin, dmax):
    fr = trans["segments"]; out = []
    for i in range(len(fr)):
        for j in range(i + 1, len(fr) + 1):
            d = fr[j - 1]["end"] - fr[i]["start"]
            if d > dmax: break
            if d >= dmin:
                out.append({"start": fr[i]["start"], "end": fr[j - 1]["end"], "score": round(puntuar(fr, i, j), 1),
                            "inicio_texto": fr[i]["text"][:90]})
    out.sort(key=lambda c: -c["score"]); elegidos = []
    for c in out:  # sin solaparse
        if all(c["end"] <= e["start"] or c["start"] >= e["end"] for e in elegidos):
            elegidos.append(c)
        if len(elegidos) >= n: break
    return sorted(elegidos, key=lambda c: c["start"])


# ---------- 2. encuadre vertical ----------
def x_cara(video, t0, t1, src_w, src_h):
    """Centro horizontal (px) siguiendo caras con el detector de OpenCV; None si no hay caras."""
    try:
        import cv2
    except ImportError:
        return None
    try:
        xml = os.path.join(getattr(getattr(cv2, "data", None), "haarcascades", ""), "haarcascade_frontalface_default.xml")
        if not os.path.exists(xml): return None
        casc = cv2.CascadeClassifier(xml)
        if casc.empty(): return None
    except Exception:
        return None
    cap = cv2.VideoCapture(video); xs = []
    paso = max(0.5, (t1 - t0) / 40)
    t = t0
    while t < t1:
        cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000); ok, fr = cap.read()
        if ok:
            g = cv2.cvtColor(cv2.resize(fr, (src_w // 2, src_h // 2)), cv2.COLOR_BGR2GRAY)
            caras = casc.detectMultiScale(g, 1.15, 6, minSize=(40, 40))
            if len(caras):
                x, y, w, h = max(caras, key=lambda c: c[2] * c[3]); xs.append((x + w / 2) * 2)
        t += paso
    cap.release()
    return statistics.median(xs) if len(xs) >= 4 else None


def filtro_encuadre(video, seg, modo):
    s = ffprobe(video, "width,height"); sw, sh = s["width"], s["height"]
    if sw * 16 <= sh * 9 + 2:  # ya es vertical
        return f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}"
    if modo == "completo":
        return (f"split[a][b];[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=30:3,eq=brightness=-0.25[f];"
                f"[b]scale={W}:-2[v];[f][v]overlay=0:(H-h)/2")
    cw = round(sh * 9 / 16)
    cx = x_cara(video, seg["start"], seg["end"], sw, sh) if modo == "auto" else None
    cx = sw / 2 if cx is None else cx
    x = int(min(max(cx - cw / 2, 0), sw - cw))
    return f"crop={cw}:{sh}:{x}:0,scale={W}:{H}"


# ---------- 3. subtítulos karaoke (ASS) ----------
def _ass_color(rgb, alfa=0):
    r, g, b = rgb; return f"&H{alfa:02X}{b:02X}{g:02X}{r:02X}"


def _t(s):
    s = max(0, s); h = int(s // 3600); m = int(s % 3600 // 60); return f"{h}:{m:02d}:{s % 60:05.2f}"


def escribir_ass(path, palabras, t0, t1, marca, gancho, cierre, fuente):
    c1, c2 = [tuple(c) for c in marca.get("glow", [(57, 235, 30), (255, 46, 166)])]
    oscuro = tuple(int(v * 0.25) for v in c2)
    cab = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Sub,{fuente},122,&H00FFFFFF,&H00FFFFFF,{_ass_color(oscuro)},&H96000000,0,0,0,0,100,100,2,0,1,10,5,2,60,60,540,1
Style: Gancho,{fuente},132,{_ass_color(c1)},&H00FFFFFF,&H00000000,&HA0000000,0,0,0,0,100,100,2,0,1,11,7,8,80,80,230,1
Style: Cierre,{fuente},104,&H00FFFFFF,&H00FFFFFF,{_ass_color(oscuro)},&HA0000000,0,0,0,0,100,100,2,0,1,8,4,5,60,60,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    ev = []
    pal = [dict(p) for p in palabras if p["end"] > t0 and p["start"] < t1]
    # grupos de máx. 3 palabras / 16 letras, cortando en puntuación
    grupos, g = [], []
    for p in pal:
        g.append(p)
        if len(g) == 3 or sum(len(x["text"]) for x in g) > 16 or p["text"][-1:] in ".?!,;:":
            grupos.append(g); g = []
    if g: grupos.append(g)
    fin_sub = t1 - (2.6 if cierre else 0)
    for gi, g in enumerate(grupos):
        fin_g = grupos[gi + 1][0]["start"] if gi + 1 < len(grupos) else g[-1]["end"] + 0.4
        fin_g = min(fin_g, g[-1]["end"] + 0.6)
        for k, p in enumerate(g):
            a = p["start"]; b = g[k + 1]["start"] if k + 1 < len(g) else fin_g
            a, b = max(a, t0) - t0, min(b, fin_sub) - t0
            if b <= a: continue
            partes = []
            for m, q in enumerate(g):
                txt = re.sub(r"[{}\\]", "", q["text"].upper())
                if m == k:
                    partes.append("{\\c" + _ass_color(c1) + "\\3c" + _ass_color(tuple(int(v * .3) for v in c1)) +
                                  "\\fscx112\\fscy112}" + txt + "{\\r}")
                else:
                    partes.append(txt)
            pop = "{\\fad(60,0)}" if k == 0 else ""
            ev.append(f"Dialogue: 0,{_t(a)},{_t(b)},Sub,,0,0,0,,{pop}{' '.join(partes)}")
    if gancho:
        ev.append(f"Dialogue: 1,{_t(0)},{_t(min(3.2, t1 - t0))},Gancho,,0,0,0,,"
                  "{\\fad(80,250)\\t(0,180,\\fscx115\\fscy115)\\t(180,360,\\fscx100\\fscy100)}" + gancho.upper())
    if cierre:
        ev.append(f"Dialogue: 1,{_t(t1 - t0 - 2.6)},{_t(t1 - t0)},Cierre,,0,0,0,,{{\\fad(200,0)}}{cierre.upper()}\\N{{\\c{_ass_color(c1)}\\fs78}}{marca.get('cta', '')}")
    open(path, "w", encoding="utf-8").write(cab + "\n".join(ev) + "\n")


def fuente_disponible():
    for nombre in ("Anton", "Bebas Neue", "Montserrat ExtraBold", "Arial Black", "DejaVu Sans"):
        r = subprocess.run(["fc-list", nombre], capture_output=True, text=True)
        if r.stdout.strip(): return nombre
    return "Arial"


# ---------- 4. render ----------
def render_clip(video, seg, out, marca, encuadre, cierre, palabras, fuente):
    ass = out.replace(".mp4", ".ass")
    escribir_ass(ass, palabras, seg["start"], seg["end"], marca, seg.get("gancho"), cierre, fuente)
    vf = filtro_encuadre(video, seg, encuadre)
    dur = seg["end"] - seg["start"]
    filtro = f"[0:v]{vf}[enc];[enc]ass='{ass}'[v]"
    af = f"afade=t=in:d=0.08,afade=t=out:st={dur - 0.35:.2f}:d=0.35,loudnorm=I=-14:TP=-1.5:LRA=11"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{seg['start']:.3f}", "-t", f"{dur:.3f}", "-i", video,
                    "-filter_complex", filtro, "-map", "[v]", "-map", "0:a?", "-af", af,
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-r", "30",
                    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", out], check=True)


def main():
    ap = argparse.ArgumentParser(description="Recortador de shorts de la fábrica de videos")
    ap.add_argument("video"); ap.add_argument("--marca", default="comics-store")
    ap.add_argument("--n", type=int, default=4); ap.add_argument("--min", type=float, default=30)
    ap.add_argument("--max", type=float, default=60); ap.add_argument("--salida")
    ap.add_argument("--segmentos"); ap.add_argument("--guion", help="texto del guion (.txt) para subtítulos exactos"); ap.add_argument("--solo-candidatos", action="store_true")
    ap.add_argument("--encuadre", default="auto", choices=["auto", "centro", "completo"])
    ap.add_argument("--cierre", default="VIDEO COMPLETO EN NUESTRO CANAL"); ap.add_argument("--sin-cierre", action="store_true")
    a = ap.parse_args()

    base = os.path.splitext(os.path.basename(a.video))[0]
    dest = a.salida or f"/home/claude/salidas/shorts_{base}"; os.makedirs(dest, exist_ok=True)
    marca = json.load(open(os.path.join(KIT, "marcas", a.marca, "marca.json")))
    tj = os.path.join(dest, "transcripcion.json")
    trans = json.load(open(tj)) if os.path.exists(tj) else transcribir(a.video, tj, a.guion)

    if a.segmentos:
        segs = json.load(open(a.segmentos)); segs = segs.get("segments", segs) if isinstance(segs, dict) else segs
    else:
        segs = candidatos(trans, a.n, a.min, a.max)
        json.dump(segs, open(os.path.join(dest, "candidatos.json"), "w"), ensure_ascii=False, indent=1)
        print(f"{len(segs)} candidatos → {dest}/candidatos.json")
        if a.solo_candidatos: return

    pal = cortes.load_word_timeline(tj)
    silencios = cortes.detect_silences(a.video)
    dur = trans["duracion"]; fuente = fuente_disponible()
    for i, s in enumerate(segs, 1):
        s["start"], s["end"] = cortes.snap_segment(pal, silencios, s, dur)
        s["end"] = min(s["end"], s["start"] + a.max + 3)
        out = os.path.join(dest, f"short_{i:02d}.mp4")
        render_clip(a.video, s, out, marca, a.encuadre, None if a.sin_cierre else a.cierre, pal, fuente)
        print(f"LISTO {out}  ({s['start']:.1f}–{s['end']:.1f} s, {s['end'] - s['start']:.0f} s)", flush=True)
    json.dump(segs, open(os.path.join(dest, "segmentos_usados.json"), "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
