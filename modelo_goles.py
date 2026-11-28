#!/usr/bin/env python3
"""MODELO DE GOLES (Dixon-Coles) — segunda opinión para fútbol, nunca reemplaza al mercado.

Usa penaltyblog (MIT). Ajusta fuerza de ataque/defensa de cada equipo con los resultados de la liga,
dando más peso a los partidos recientes, y da probabilidades de 1X2, empate, doble oportunidad,
sin empate, más/menos y ambos marcan.

CSV de entrada (cabeceras): fecha,local,visitante,gl,gv   (fecha AAAA-MM-DD)
  Ej.: los 966 partidos de la Liga BetPlay de Fernando.

Uso:
  python3 modelo_goles.py resultados.csv "Junior" "Millonarios"
  python3 modelo_goles.py resultados.csv "Junior" "Millonarios" --xi 0.003 --desde 2025-01-01
  python3 modelo_goles.py resultados.csv --backtest-empates 2026-01-01 --cuota-empate 3.4
Reglas (bitácora): L6 — en totales y córners confiar en el mercado; este modelo solo sirve de contraste.
Si el modelo y Pinnacle difieren más de 5 puntos, revisar bajas/rotación antes de creerle al modelo.
"""
import argparse, sys
import numpy as np, pandas as pd
import penaltyblog as pb


def cargar(path, desde=None, hasta=None):
    df = pd.read_csv(path)
    df.columns = [c.strip().lower() for c in df.columns]
    df["fecha"] = pd.to_datetime(df["fecha"])
    if desde: df = df[df["fecha"] >= pd.Timestamp(desde)]
    if hasta: df = df[df["fecha"] < pd.Timestamp(hasta)]
    return df.dropna(subset=["gl", "gv"]).sort_values("fecha")


def ajustar(df, xi, base=None):
    w = pb.models.dixon_coles_weights(df["fecha"], xi, base_date=base)
    m = pb.models.DixonColesGoalModel(df["gl"].astype(int), df["gv"].astype(int), df["local"], df["visitante"], w)
    m.fit(); return m


def resumen(g, local, visita):
    p = lambda x: f"{x*100:5.1f}%  (justa {1/x:5.2f})" if x > 0 else "  —"
    print(f"\n{local} vs {visita} — modelo Dixon-Coles")
    print(f"  Local        {p(g.home_win)}\n  Empate       {p(g.draw)}\n  Visitante    {p(g.away_win)}")
    print(f"  1X           {p(g.double_chance_1x)}\n  X2           {p(g.double_chance_x2)}")
    print(f"  Sin empate L {p(g.draw_no_bet_home)}\n  Sin empate V {p(g.draw_no_bet_away)}")
    for lin in (1.5, 2.5, 3.5):
        o, u = g.total_goals("over", lin), g.total_goals("under", lin)
        print(f"  Más {lin}      {p(o)}   Menos {lin} {p(u)}")
    print(f"  Ambos marcan {p(g.btts_yes)}")
    mat = np.array(g.grid); idx = np.dstack(np.unravel_index(np.argsort(mat.ravel())[::-1][:3], mat.shape))[0]
    print("  Marcadores más probables: " + ", ".join(f"{i}-{j} ({mat[i, j]*100:.1f}%)" for i, j in idx))
    print("\n  L6: en totales confiar en el mercado. Contrastar siempre con Pinnacle sin margen (justa.py).")


def backtest_empates(df, desde, xi, cuota, umbral):
    """Recorre partido por partido desde 'desde', ajustando solo con lo anterior (sin mirar el futuro)."""
    pend = df[df["fecha"] >= pd.Timestamp(desde)]; filas = []
    for fecha, grupo in pend.groupby(pend["fecha"].dt.date):
        hist = df[df["fecha"] < pd.Timestamp(fecha)]
        if len(hist) < 60: continue
        m = ajustar(hist, xi, base=pd.Timestamp(fecha))
        for _, r in grupo.iterrows():
            try: g = m.predict(r["local"], r["visitante"])
            except Exception: continue
            filas.append({"fecha": fecha, "partido": f"{r['local']}-{r['visitante']}", "p_empate": g.draw,
                          "empate": int(r["gl"] == r["gv"])})
    t = pd.DataFrame(filas)
    if t.empty: sys.exit("No hay partidos suficientes para el backtest")
    print(f"Partidos evaluados: {len(t)} · empates reales {t.empate.mean()*100:.1f}% · modelo medio {t.p_empate.mean()*100:.1f}%")
    for nombre, sel in (("Todos", t), (f"Modelo ≥{umbral*100:.0f}%", t[t.p_empate >= umbral])):
        if len(sel) == 0: continue
        gan = (sel.empate * (cuota - 1) - (1 - sel.empate)).sum()
        print(f"  {nombre:<14} {len(sel):4d} apuestas · acierto {sel.empate.mean()*100:5.1f}% · ROI a cuota {cuota}: {gan/len(sel)*100:+.1f}%")
    print("  (ROI con cuota fija: es una guía; el real depende de la cuota de cada partido)")


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("csv"); ap.add_argument("local", nargs="?"); ap.add_argument("visitante", nargs="?")
    ap.add_argument("--xi", type=float, default=0.0018, help="peso de lo reciente (más alto = olvida más rápido)")
    ap.add_argument("--desde"); ap.add_argument("--backtest-empates"); ap.add_argument("--cuota-empate", type=float, default=3.4)
    ap.add_argument("--umbral", type=float, default=0.30)
    a = ap.parse_args()
    df = cargar(a.csv, a.desde)
    if a.backtest_empates:
        return backtest_empates(df, a.backtest_empates, a.xi, a.cuota_empate, a.umbral)
    equipos = set(df["local"]) | set(df["visitante"])
    for e in (a.local, a.visitante):
        if e not in equipos:
            cerca = [x for x in equipos if e.lower()[:4] in x.lower()]
            sys.exit(f"'{e}' no está en el CSV. Parecidos: {cerca[:5]}")
    m = ajustar(df, a.xi)
    resumen(m.predict(a.local, a.visitante), a.local, a.visitante)


if __name__ == "__main__":
    main()
