"""Música y ambientes 100 % generados por código (sin derechos de autor).
musica_epica(total, N, SR) y ambiente(nombre, dur, SR) -> np.float32"""
import numpy as np

def _lp(x, a):            # filtro pasa-bajos de un polo (vectorizado por bloques no hace falta: usamos IIR simple con lfilter si existe)
    try:
        from scipy.signal import lfilter
        return lfilter([a], [1, a - 1], x).astype(np.float32)
    except Exception:
        y = np.zeros_like(x); v = 0.
        for i, s in enumerate(x): v += a * (s - v); y[i] = v
        return y

def _ruido(n, seed=0): return np.random.default_rng(seed).standard_normal(n).astype(np.float32)
def _env(n, ataque=.3, suelta=.6, SR=24000):
    e = np.ones(n, np.float32); a = min(n // 2, int(ataque * SR)); s = min(n // 2, int(suelta * SR))
    if a: e[:a] = np.linspace(0, 1, a)
    if s: e[-s:] = np.linspace(1, 0, s)
    return e

def _saw(f, tt):
    return (2 * ((f * tt) % 1) - 1).astype(np.float32)

hz = lambda m: 440 * 2 ** ((m - 69) / 12)

def musica_epica(total, N, SR):
    """Oscura y épica en re menor: bordón grave, cuerdas sostenidas, ostinato, timbales y coro suave."""
    m = np.zeros(N, np.float32); bpm = 84; beat = 60 / bpm; bar = 4 * beat
    prog = [[50, 53, 57], [46, 50, 53], [43, 46, 50], [45, 49, 52]]          # Dm Bb Gm A
    bajos = [38, 34, 31, 33]
    nb = int(total / bar) + 2
    for b in range(nb):
        t0 = b * bar; i0 = int(t0 * SR)
        if i0 >= N: break
        n = min(int(bar * SR), N - i0); tt = np.arange(n) / SR; ch = prog[b % 4]
        # cuerdas (sierras filtradas, ligeramente desafinadas)
        pad = sum(_saw(hz(c) * d, tt) for c in ch for d in (0.997, 1.003)) / 6
        pad = _lp(pad, .06) * _env(n, .5, .5, SR) * .16
        # coro (senos con vibrato) una octava arriba cada 2 compases
        coro = 0
        if b % 2 == 1:
            vib = 1 + .004 * np.sin(2 * np.pi * 5 * tt)
            coro = sum(np.sin(2 * np.pi * hz(c + 12) * vib * tt) for c in ch) / 3 * _env(n, .8, .8, SR) * .05
        # bordón grave
        bor = _lp(_saw(hz(bajos[b % 4]), tt), .03) * .22 * _env(n, .05, .3, SR)
        m[i0:i0 + n] += (pad + coro + bor).astype(np.float32)
        # ostinato de corcheas (staccato)
        for s in range(8):
            ts = t0 + s * beat / 2; j = int(ts * SR)
            if j >= N: break
            k = min(int(.18 * SR), N - j); t2 = np.arange(k) / SR
            nota = ch[0] - 12 if s % 4 != 3 else ch[2] - 12
            m[j:j + k] += (_lp(_saw(hz(nota), t2), .2) * np.exp(-t2 * 14) * .09).astype(np.float32)
        # timbales: 1 y 3 (más fuerte en el 1)
        for s, v in ((0, .55), (2, .3)):
            j = int((t0 + s * beat) * SR)
            if j >= N: continue
            k = min(int(.9 * SR), N - j); t2 = np.arange(k) / SR
            tim = np.sin(2 * np.pi * np.cumsum(55 + 40 * np.exp(-t2 * 20)) / SR) * np.exp(-t2 * 4.5)
            tim += _lp(_ruido(k, b + s), .1) * np.exp(-t2 * 12) * .3
            m[j:j + k] += (tim * v * .5).astype(np.float32)
    return m

def ambiente(nombre, dur, SR):
    n = int(dur * SR); tt = np.arange(n) / SR; z = np.zeros(n, np.float32); seed = abs(hash(nombre)) % 999
    if n <= 0: return z
    if nombre in ("viento", "tormenta", "nieve"):
        w = _lp(_ruido(n, seed), .015); mod = .6 + .4 * np.sin(2 * np.pi * .23 * tt + 1) * np.sin(2 * np.pi * .07 * tt)
        silb = _lp(_ruido(n, seed + 1), .08) * (np.sin(2 * np.pi * .5 * tt) ** 2) * .3
        z = (w * 3.2 * mod + silb) * (1.0 if nombre == "tormenta" else .6 if nombre == "viento" else .4)
    elif nombre in ("fuego", "fogata", "chimenea", "antorchas"):
        base = _lp(_ruido(n, seed), .03) * 2.2
        rng = np.random.default_rng(seed); crack = np.zeros(n, np.float32)
        for _ in range(int(dur * (9 if nombre != "antorchas" else 4))):
            j = rng.integers(0, max(1, n - 400)); k = rng.integers(60, 400)
            crack[j:j + k] += _ruido(k, int(j)) * np.exp(-np.arange(k) / (k / 4)) * rng.uniform(.2, .7)
        z = (base + crack) * (.5 if nombre == "antorchas" else .8)
    elif nombre == "infierno":
        rug = _lp(_saw(32, tt) + _saw(32.7, tt), .01) * .9
        z = rug * (.7 + .3 * np.sin(2 * np.pi * .3 * tt)) + _lp(_ruido(n, seed), .02) * 2 + ambiente("fuego", dur, SR) * .6
    elif nombre == "maquina":
        sube = 1 + .5 * np.clip(tt / max(1, dur), 0, 1)
        z = (np.sin(2 * np.pi * 60 * sube * tt) * .35 + np.sin(2 * np.pi * 120 * sube * tt) * .2 + _saw(180 * sube, tt) * .05
             + _lp(_ruido(n, seed), .3) * .05 * (np.sin(2 * np.pi * 7 * tt) > .7))
    elif nombre in ("explosion", "impacto"):
        k = min(n, int(3.5 * SR)); t2 = np.arange(k) / SR
        boom = np.sin(2 * np.pi * np.cumsum(30 + 70 * np.exp(-t2 * 6)) / SR) * np.exp(-t2 * 1.6) * 1.4
        nz = _lp(_ruido(k, seed), .12) * np.exp(-t2 * 2.2) * 2.5
        z[:k] = (boom + nz) * (1.0 if nombre == "explosion" else .55)
        if nombre == "explosion": z += ambiente("fuego", dur, SR) * .5 * np.clip((tt - .6) / .5, 0, 1)
    elif nombre == "trueno":
        rng = np.random.default_rng(seed); z = ambiente("viento", dur, SR) * .7
        for j0 in (rng.uniform(.2, .8), rng.uniform(max(1, dur * .5), max(1.2, dur * .8))):
            j = int(j0 * SR); k = min(n - j, int(2.8 * SR))
            if k <= 0: continue
            t2 = np.arange(k) / SR; ru = _lp(_ruido(k, j), .02) * 5 * np.exp(-t2 * 1.3) * (1 + .5 * np.sin(2 * np.pi * 3 * t2))
            cr = _ruido(k, j + 1) * np.exp(-t2 * 25) * .8
            z[j:j + k] += ru + cr
    elif nombre == "magia":
        brillo = sum(np.sin(2 * np.pi * f * tt + p) * (.5 + .5 * np.sin(2 * np.pi * r * tt)) for f, p, r in ((880, 0, .7), (1318.5, 1, .9), (1760, 2, 1.3))) * .06
        hum = np.sin(2 * np.pi * 110 * tt) * .12 * (.6 + .4 * np.sin(2 * np.pi * .5 * tt)) + _lp(_ruido(n, seed), .05) * .4
        z = brillo + hum
    elif nombre == "campanas":
        z = ambiente("viento", dur, SR) * .5
        for j0 in np.arange(.3, dur, 2.6):
            j = int(j0 * SR); k = min(n - j, int(3 * SR)); t2 = np.arange(k) / SR
            z[j:j + k] += sum(np.sin(2 * np.pi * f * t2) * a for f, a in ((392, .3), (784 * 1.01, .15), (1176 * 1.02, .08))) * np.exp(-t2 * 1.2)
    elif nombre == "forja":
        z = ambiente("fuego", dur, SR) * .6
        for j0 in np.arange(.4, dur, .85):
            j = int(j0 * SR); k = min(n - j, int(.8 * SR)); t2 = np.arange(k) / SR
            z[j:j + k] += sum(np.sin(2 * np.pi * f * t2) * a for f, a in ((1250, .3), (2950, .15), (4100, .08))) * np.exp(-t2 * 9) + _ruido(k, j) * np.exp(-t2 * 60) * .5
    elif nombre == "cosmos":
        z = np.sin(2 * np.pi * 41 * tt) * .3 * (.7 + .3 * np.sin(2 * np.pi * .2 * tt)) + _lp(_ruido(n, seed), .01) * 1.5 + np.sin(2 * np.pi * 523 * tt) * .02 * np.sin(2 * np.pi * .3 * tt)
    elif nombre == "noche":
        z = _lp(_ruido(n, seed), .01) * 1.0
        rng = np.random.default_rng(seed)
        for j0 in np.arange(.2, dur, .9):   # grillos
            j = int((j0 + rng.uniform(0, .3)) * SR); k = min(n - j, int(.12 * SR))
            if k > 0: z[j:j + k] += np.sin(2 * np.pi * 4300 * np.arange(k) / SR) * (np.sin(2 * np.pi * 40 * np.arange(k) / SR) > 0) * .05
    z = np.asarray(z, np.float32)
    pk = np.abs(z).max()
    if pk > 1e-6: z = z / pk * .5
    ataque = .01 if nombre in ("explosion", "impacto", "trueno") else .35
    return (z * _env(n, ataque, .5, SR)).astype(np.float32)
