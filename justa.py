#!/usr/bin/env python3
"""PROBABILIDAD JUSTA, VALOR Y CUOTA MÍNIMA — método de Fernando (FILTRO DURO L13).

Usa penaltyblog (MIT, github.com/martineastwood/penaltyblog) para quitarle el margen a Pinnacle
con el método de Shin (corrige el sesgo favorito/no favorito mejor que dividir por el total).

Ejemplos:
  # 1X2 (local, empate, visitante): Pinnacle + casas de Fernando
  python3 justa.py --pinnacle 2.10 3.30 3.60 --casa BetPlay 2.25 3.20 3.40 --casa Wplay 2.15 3.40 3.70
  # Mercado de 2 opciones (tenis, más/menos, spread)
  python3 justa.py --nombres Más Menos --pinnacle 1.95 1.89 --casa BetPlay 2.02 1.80
  # Sin Pinnacle → promedio de casas sin margen y el pick queda CONDICIONAL (L13)
  python3 justa.py --casa BetPlay 2.25 3.20 3.40 --casa Codere 2.20 3.25 3.45
  # Ajuste propio (máx ±3 puntos, solo con evidencia):  --ajuste 0 +2 -2
  # Guardar para el registro: --json salida.json
"""
import argparse, json, sys
import penaltyblog as pb

BANK = 10_000_000; STAKE = BANK // 100          # 1 stake = 1% del bank = $100.000
EV_MIN = 0.03                                    # L13
METODO = "shin"


def sin_margen(cuotas, metodo=METODO):
    r = pb.implied.calculate_implied(list(cuotas), method=metodo)
    return list(r.probabilities), r.margin


def redondear(monto):  # montos cerrados, múltiplos de $5.000
    return int(round(monto / 5000.0)) * 5000


def nivel_y_monto(ev, cuota, p, prob_verificada):
    if ev < EV_MIN:
        return "NO APOSTAR", 0, 0
    if ev < 0.04:   niv, rango = "Bajo", (0.25, 0.5)
    elif ev <= 0.06: niv, rango = "Medio", (0.5, 1.0)
    else:           niv, rango = "Alto*", (1.0, 2.0)  # *solo si hay noticia confirmada y mercado a favor
    if cuota > 4.0: rango = (min(rango[0], 0.5), 0.5)
    if not prob_verificada: niv, rango = "CONDICIONAL", (0.25, 0.5)
    kelly4 = max(0.0, (p * cuota - 1) / (cuota - 1)) / 4 * 100      # en stakes (1 stake = 1% bank)
    alto = min(rango[1], kelly4, 2.0)                                # 1/4 Kelly como techo; tope 2% del bank
    bajo = min(rango[0], alto)
    return niv, redondear(bajo * STAKE), redondear(alto * STAKE)


def main():
    ap = argparse.ArgumentParser(description="Probabilidad justa sin margen, EV y cuota mínima")
    ap.add_argument("--pinnacle", nargs="+", type=float)
    ap.add_argument("--casa", nargs="+", action="append", default=[], metavar=("NOMBRE", "CUOTA"))
    ap.add_argument("--nombres", nargs="+")
    ap.add_argument("--ajuste", nargs="+", type=float, help="puntos porcentuales por opción (máx ±3)")
    ap.add_argument("--metodo", default=METODO)
    ap.add_argument("--json")
    a = ap.parse_args()

    casas = {c[0]: [float(x) for x in c[1:]] for c in a.casa}
    n = len(a.pinnacle) if a.pinnacle else len(next(iter(casas.values())))
    nombres = a.nombres or (["Local", "Empate", "Visitante"] if n == 3 else [f"Opción {i+1}" for i in range(n)])

    if a.pinnacle:
        justa, margen = sin_margen(a.pinnacle, a.metodo); verificada = True
        print(f"Pinnacle: margen {margen*100:.1f}% → probabilidad justa ({a.metodo})")
    else:
        sets = [sin_margen(v, a.metodo)[0] for v in casas.values()]
        justa = [sum(s[i] for s in sets) / len(sets) for i in range(n)]; verificada = False
        print("⚠️ SIN Pinnacle: promedio de casas sin margen → todo pick queda CONDICIONAL (L13)")
    if a.ajuste:
        if any(abs(x) > 3 for x in a.ajuste): sys.exit("El ajuste propio no puede pasar de ±3 puntos")
        justa = [max(0.001, p + x / 100) for p, x in zip(justa, a.ajuste)]
        s = sum(justa); justa = [p / s for p in justa]
        print("Ajuste propio aplicado (si el valor depende solo de esto → máximo nivel Bajo)")

    filas = []
    for i, nom in enumerate(nombres):
        p = justa[i]; minima = (1 + EV_MIN) / p
        mejor = max(((c, v[i]) for c, v in casas.items()), key=lambda x: x[1], default=(None, None))
        fila = {"opcion": nom, "prob_justa": round(p, 4), "cuota_justa": round(1 / p, 3), "cuota_minima": round(minima, 2),
                "casas": {c: {"cuota": v[i], "ev": round(p * v[i] - 1, 4)} for c, v in casas.items()}}
        if mejor[0]:
            ev = p * mejor[1] - 1
            niv, m0, m1 = nivel_y_monto(ev, mejor[1], p, verificada)
            if a.ajuste and niv not in ("NO APOSTAR", "CONDICIONAL"): niv = "Bajo"; m1 = min(m1, redondear(0.5 * STAKE))
            fila.update({"mejor_casa": mejor[0], "mejor_cuota": mejor[1], "ev": round(ev, 4), "nivel": niv, "monto": [m0, m1]})
        filas.append(fila)

    print(f"\n{'Opción':<11}{'Prob':>7}{'Justa':>7}{'Mín':>7}   Mejor casa        EV     Nivel / monto")
    for f in filas:
        linea = f"{f['opcion']:<11}{f['prob_justa']*100:>6.1f}%{f['cuota_justa']:>7.2f}{f['cuota_minima']:>7.2f}"
        if "mejor_casa" in f:
            m0, m1 = f["monto"]
            monto = "—" if m1 == 0 else (f"${m1:,}" if m0 == m1 else f"${m0:,}–${m1:,}").replace(",", ".")
            linea += f"   {f['mejor_casa']:<10}{f['mejor_cuota']:>6.2f}  {f['ev']*100:>+5.1f}%   {f['nivel']} {monto}"
        print(linea)
    print("\nCuota mínima = la que da EV ≥3% contra la probabilidad justa. *Alto solo con noticia confirmada y mercado a favor.")
    if a.json:
        json.dump({"metodo": a.metodo, "verificada": verificada, "filas": filas}, open(a.json, "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
