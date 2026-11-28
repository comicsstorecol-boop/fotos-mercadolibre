#!/usr/bin/env python3
"""Transcribe un video con marcas de tiempo por PALABRA.

Motor 1 (PC de Fernando): faster-whisper, si está instalado y puede bajar su modelo.
Motor 2 (nube de Claude): sherpa-onnx + Parakeet TDT v3 (habla español), modelo
descargado desde GitHub por setup.sh (RECORTADOR=1) en recortador/modelo/.

Salida JSON (mismo formato que claude-shorts, para reutilizar sus pasos):
  {"idioma": "es", "duracion": s, "palabras": [{"text","start","end"}],
   "segments": [{"start","end","text","words":[{"word","start","end"}]}]}

Uso: python3 recortador/transcribir.py video.mp4 salida.json
"""
import os, sys, json, re, subprocess, tempfile, glob

AQUI = os.path.dirname(os.path.abspath(__file__))
MODELO_DIR = os.environ.get("RECORTADOR_MODELO", os.path.join(AQUI, "modelo"))
FIN_FRASE = ".?!¿¡…"


def _audio16k(video):
    wav = tempfile.mktemp(suffix=".wav")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", video, "-vn", "-ac", "1", "-ar", "16000", wav], check=True)
    return wav


def _duracion(path):
    r = subprocess.run(["ffprobe", "-v", "quiet", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                       capture_output=True, text=True)
    return float(r.stdout.strip())


def _con_faster_whisper(wav, tam="small"):
    from faster_whisper import WhisperModel
    m = WhisperModel(tam, device="auto", compute_type="int8")
    segs, info = m.transcribe(wav, language="es", word_timestamps=True, vad_filter=True)
    pal = []
    for s in segs:
        for w in s.words or []:
            pal.append({"text": w.word.strip(), "start": round(w.start, 3), "end": round(w.end, 3)})
    return pal


def _con_parakeet(wav):
    import sherpa_onnx, soundfile as sf, numpy as np
    d = MODELO_DIR
    if not os.path.isdir(d):
        cand = glob.glob(os.path.join(d + "*")) + glob.glob("/home/claude/modelos/sherpa-onnx-nemo-parakeet*")
        d = cand[0] if cand else d
    sub = glob.glob(os.path.join(d, "sherpa-onnx-nemo-parakeet*"))
    if sub: d = sub[0]
    f = lambda n: glob.glob(os.path.join(d, n))[0]
    rec = sherpa_onnx.OfflineRecognizer.from_transducer(
        encoder=f("encoder*.onnx"), decoder=f("decoder*.onnx"), joiner=f("joiner*.onnx"),
        tokens=f("tokens.txt"), model_type="nemo_transducer", num_threads=os.cpu_count() or 2)
    audio, sr = sf.read(wav, dtype="float32")
    pal, VENT = [], 25.0  # trozos de 25 s cortados en silencios para no gastar memoria
    n, i = len(audio), 0
    while i < n:
        fin = min(n, i + int(VENT * sr))
        if fin < n:  # buscar el punto más silencioso en los últimos 3 s del trozo
            zona = audio[fin - 3 * sr:fin]
            ener = np.convolve(np.abs(zona), np.ones(800) / 800, mode="same")
            fin = fin - 3 * sr + int(np.argmin(ener))
        st = rec.create_stream(); st.accept_waveform(sr, audio[i:fin]); rec.decode_stream(st)
        r, off = st.result, i / sr
        # unir tokens BPE en palabras (un token que empieza con espacio abre palabra)
        actual = None
        for tok, t in zip(r.tokens, r.timestamps):
            s = tok.replace("▁", " ")
            if not s.strip(): continue
            pega_num = actual is not None and s.strip()[:1].isdigit() and actual["text"][-1:].isalpha()
            if s.startswith(" ") or actual is None or pega_num:
                if actual: pal.append(actual)
                actual = {"text": s.strip(), "start": round(off + t, 3), "end": round(off + t + 0.25, 3)}
            else:
                actual["text"] += s.strip(); actual["end"] = round(off + t + 0.2, 3)
        if actual: pal.append(actual)
        i = fin
    # el fin de cada palabra no puede pasar el inicio de la siguiente
    for a, b in zip(pal, pal[1:]):
        a["end"] = round(min(a["end"], b["start"]), 3)
    return pal


def _norm(w):
    import unicodedata
    w = unicodedata.normalize("NFD", w.lower()); w = "".join(c for c in w if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9ñ]", "", w)


def alinear_con_guion(pal, texto):
    """Cambia las palabras reconocidas por las del GUION (nombres bien escritos: Doom, Comics Store…)
    conservando los tiempos. Usa difflib; los tramos distintos reparten el tiempo en proporción."""
    import difflib
    gw = texto.split()
    a, b = [_norm(p["text"]) for p in pal], [_norm(w) for w in gw]
    out = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if op == "equal":
            for k in range(i2 - i1):
                out.append({**pal[i1 + k], "text": gw[j1 + k]})
        elif op in ("replace", "insert") and j2 > j1:
            t0 = pal[i1]["start"] if i1 < len(pal) else pal[-1]["end"]
            t1 = pal[i2 - 1]["end"] if i2 > i1 else (pal[i1]["start"] if i1 < len(pal) else t0 + 0.3)
            if i2 == i1 and out: t0 = out[-1]["end"]
            largos = [max(1, len(gw[j])) for j in range(j1, j2)]; tot = sum(largos); t = t0
            for j, L in zip(range(j1, j2), largos):
                d = (t1 - t0) * L / tot
                out.append({"text": gw[j], "start": round(t, 3), "end": round(t + d, 3)}); t += d
        # "delete": palabras oídas que no están en el guion → se descartan
    return out


def corregir(pal, correcciones):
    """Reemplazos fijos de nombres mal reconocidos (recortador/correcciones.json)."""
    txt = [p["text"] for p in pal]
    for mal, bien in sorted(correcciones.items(), key=lambda kv: -len(kv[0].split())):
        m = mal.split(); n = len(m)
        for i in range(len(txt) - n + 1):
            if [_norm(x) for x in txt[i:i + n]] == [_norm(x) for x in m]:
                cola = re.sub(r"^.*?([.,;:!?…]*)$", r"\1", txt[i + n - 1])
                txt[i] = bien + cola
                for k in range(1, n): txt[i + k] = ""
    out = []
    for p, t in zip(pal, txt):
        if t: out.append({**p, "text": t})
        elif out: out[-1]["end"] = p["end"]
    return out


def transcribir(video, salida, guion=None):
    wav = _audio16k(video)
    motor = os.environ.get("MOTOR_TRANSCRIPCION", "")
    pal = None
    if motor != "parakeet":
        try:
            pal = _con_faster_whisper(wav); usado = "faster-whisper"
        except Exception as e:
            print(f"faster-whisper no disponible ({type(e).__name__}); uso Parakeet", file=sys.stderr)
    if pal is None:
        pal = _con_parakeet(wav); usado = "parakeet"
    os.remove(wav)
    if guion:
        pal = alinear_con_guion(pal, open(guion, encoding="utf-8").read() if os.path.exists(guion) else guion)
    else:
        cj = os.path.join(AQUI, "correcciones.json")
        if os.path.exists(cj): pal = corregir(pal, json.load(open(cj, encoding="utf-8")))
    # agrupar en frases (claude-shorts espera "segments" con "words")
    segs, cur = [], []
    for w in pal:
        cur.append(w)
        if w["text"][-1:] in FIN_FRASE or len(cur) >= 30:
            segs.append(cur); cur = []
    if cur: segs.append(cur)
    data = {"idioma": "es", "motor": usado, "duracion": _duracion(video), "palabras": pal,
            "segments": [{"start": s[0]["start"], "end": s[-1]["end"], "text": " ".join(w["text"] for w in s),
                          "words": [{"word": w["text"], "start": w["start"], "end": w["end"]} for w in s]} for s in segs]}
    json.dump(data, open(salida, "w"), ensure_ascii=False, indent=1)
    print(f"Transcripción lista ({usado}): {len(pal)} palabras, {len(segs)} frases → {salida}")
    return data


if __name__ == "__main__":
    transcribir(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
