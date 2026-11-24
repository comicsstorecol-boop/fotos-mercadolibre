"""Narrador con video real (clips que genera Fernando) sincronizado con la voz.

Cada clip trae la apertura de boca medida cuadro a cuadro (biblioteca/narrador/<estilo>/boca.json,
herramientas/medir_boca.py). Para cada escena se arma una edición de los clips cuya boca sigue a la
voz: trozos de ~0,3 s elegidos por parecido de apertura, velocidad ajustable (0,8x–1,2x) y, cuando hay
que saltar a otro punto, fundido corto. En silencios se eligen tramos con la boca cerrada.
"""
import os, json, glob, math, subprocess
import numpy as np
from PIL import Image, ImageFilter
import lib, motor
from lib import W, H, HORIZONTAL

HERE = os.path.dirname(os.path.abspath(__file__))
BIB = os.path.join(os.path.dirname(HERE), "biblioteca", "narrador")
CACHE = "/tmp/narrador_frames"
FPS_SRC = 24.
RATES = (.64, .72, .8, .88, .96)        # cuadros de origen por cuadro de salida (0,8 = tiempo real)
K = 9                                    # cuadros por trozo (0,3 s)


def _frames(estilo, ori, nombre):
    d = os.path.join(CACHE, estilo, ori, nombre)
    if not os.path.isdir(d) or not os.listdir(d):
        os.makedirs(d, exist_ok=True)
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", os.path.join(BIB, estilo, ori, nombre + ".mp4"), "-q:v", "2", f"{d}/%05d.jpg"], check=True)
    return sorted(glob.glob(f"{d}/*.jpg"))


def _norm(v):
    v = np.array([np.nan if x is None else x for x in v], float)
    if np.isnan(v).any():   # huecos sin cara: interpolar
        i = np.arange(len(v)); ok = ~np.isnan(v); v = np.interp(i, i[ok], v[ok])
    v = np.convolve(v, [.25, .5, .25], "same")
    lo, hi = np.percentile(v, 8), np.percentile(v, 97)
    return np.clip((v - lo) / max(1e-6, hi - lo), 0, 1)


class NarradorVideo:
    def __init__(self, estilo="terror", zoom=1.0, foco_y=.0):
        self.ori = "h" if HORIZONTAL else "v"; self.zoom, self.foco_y = zoom, foco_y
        data = json.load(open(os.path.join(BIB, estilo, "boca.json")))
        self.clips = []
        for nombre in sorted(os.path.basename(p)[:-4] for p in glob.glob(os.path.join(BIB, estilo, self.ori, "*.mp4"))):
            d = data[f"{self.ori}/{nombre}"]; fr = _frames(estilo, self.ori, nombre)
            bb = np.array([b for b in d["bbox"] if b]); cx = float(np.median((bb[:, 0] + bb[:, 2]) / 2)); cy = float(np.median((bb[:, 1] + bb[:, 3]) / 2)); fh = float(np.median(bb[:, 3] - bb[:, 1]))
            self.clips.append(dict(frames=fr, m=_norm(d["boca"])[:len(fr)], cx=cx, cy=cy, fh=fh))
        self.uso = [np.zeros(len(c["frames"])) for c in self.clips]
        self._esc = None; self._plan = None; self._lru = {}

    # ------------------------------------------------------------------ edición sincronizada
    def _M(self, c, pos):
        m = self.clips[c]["m"]; pos = np.clip(pos, 0, len(m) - 1); i = np.floor(pos).astype(int); j = np.minimum(i + 1, len(m) - 1); a = pos - i
        return m[i] * (1 - a) + m[j] * a

    def planificar(self, lv, lead, nf):
        T = np.zeros(nf); off = int(round(lead * 30)) - 1     # la boca se adelanta 1 cuadro a la voz
        for f in range(nf):
            k = f - off
            if 0 <= k < len(lv): T[f] = lv[k]
        T = np.clip(T / max(.35, np.percentile(T[T > 0], 85) if (T > 0).any() else 1), 0, 1)
        plan = []; cur = None
        for f0 in range(0, nf, K):
            n = min(K, nf - f0); tgt = T[f0:f0 + n]; idx = np.arange(n); best = None
            if cur is not None:   # seguir donde va, cambiando un poco la velocidad
                c, s = cur
                for r in RATES:
                    pos = s + r * (idx + 1)
                    if pos[-1] >= len(self.clips[c]["m"]) - 1: continue
                    cost = np.abs(self._M(c, pos) - tgt).mean() + .5 * abs(r - .8) ** 2
                    if best is None or cost < best[0]: best = (cost, c, pos, False)
            for c, cl in enumerate(self.clips):   # o saltar a otro tramo (con fundido)
                m = cl["m"]; L = len(m); starts = np.arange(0, L - int(n * .8) - 2, 2)
                if not len(starts): continue
                P = starts[:, None] + .8 * idx[None, :]; Mv = self._M(c, P)
                cost = np.abs(Mv - tgt[None, :]).mean(1) + .05 * self.uso[c][starts] + (.10 if cur is None or cur[0] == c else .38) * (cur is not None)
                j = int(np.argmin(cost))
                if best is None or cost[j] < best[0]: best = (float(cost[j]), c, P[j], cur is not None)
            _, c, pos, salto = best
            for i, p in enumerate(pos):
                fade = None
                if salto and i < 5 and cur is not None:
                    pc, ps = cur; fade = (pc, min(ps + .8 * (i + 1), len(self.clips[pc]["frames"]) - 1), (i + 1) / 6)
                plan.append((c, float(p), fade))
            cur = (c, float(pos[-1]))
            u = self.uso[c]; a, b = int(pos[0]), int(pos[-1]) + 1; u *= .97; u[max(0, a - 12):b + 12] += 1
        return plan

    # ------------------------------------------------------------------ cuadros
    def _img(self, c, p):
        k = (c, int(round(p)))
        if k not in self._lru:
            if len(self._lru) > 24: self._lru.pop(next(iter(self._lru)))
            fr = self.clips[c]["frames"]; self._lru[k] = Image.open(fr[min(len(fr) - 1, k[1])]).convert("RGB")
        return self._lru[k]

    def escena(self, z0=1.0, z1=1.15, cy=.42, nombre="anf"):
        zoom, foco_y = self.zoom, self.foco_y
        def f(t, d):
            e = motor.ESCENA
            if e is None: return Image.new("RGBA", (W, H), (0, 0, 0, 255))
            if self._esc is not e["id"]:
                self._esc = e["id"]; self._plan = self.planificar(e["lv"], e["lead"], e["nf"])
            i = min(len(self._plan) - 1, max(0, int(round(t * 30))))
            c, p, fade = self._plan[i]; im = self._img(c, p)
            if fade: im = Image.blend(self._img(fade[0], fade[1]), im, fade[2])
            cl = self.clips[c]; SW, SH = im.size
            z = (min(z0, z1) + (max(z0, z1) - min(z0, z1)) * .5 * (1 - math.cos(math.pi * min(1, t / max(d, .1))))) * zoom
            z = max(1.0, z * (1 + .004 * math.sin(t * 1.6)))
            w, h = SW / z, SH / z
            fx = cl["cx"]; fy = cl["cy"] + cl["fh"] * foco_y
            x0 = min(max(fx - w / 2, 0), SW - w); y0 = min(max(fy - h * (.42 if zoom > 1.2 else cy), 0), SH - h)
            out = im.resize((W, H), Image.LANCZOS, box=(x0, y0, x0 + w, y0 + h)).convert("RGBA")
            if t < .4: out.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, int(255 * (1 - t / .4)))))
            return out
        f.__name__ = nombre; return f


def disponible(estilo="terror"):
    ori = "h" if HORIZONTAL else "v"
    return os.path.exists(os.path.join(BIB, estilo, "boca.json")) and bool(glob.glob(os.path.join(BIB, estilo, ori, "*.mp4")))
