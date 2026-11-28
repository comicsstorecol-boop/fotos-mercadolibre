# Análisis de apuestas — herramientas de cálculo (rama `analisis-apuestas`)

Base: [penaltyblog](https://github.com/martineastwood/penaltyblog) (MIT, Martin Eastwood). Instalar: `pip install penaltyblog pandas`.

| Script | Para qué |
|---|---|
| `justa.py` | Quita el margen a Pinnacle (método de Shin), compara las casas de Fernando, da EV, **cuota mínima** (EV ≥3%), nivel y monto en pesos según BANK Y STAKES (1 stake = $100.000, montos múltiplos de $5.000, 1/4 Kelly como techo, cuotas >4 máx 0.5 stake). Sin Pinnacle → CONDICIONAL (L13). |
| `modelo_goles.py` | Modelo Dixon-Coles (fútbol) desde un CSV `fecha,local,visitante,gl,gv`: 1X2, 1X/X2, sin empate, más/menos 1.5-3.5, ambos marcan, marcadores. Segunda opinión, nunca reemplaza al mercado (L6). `--backtest-empates` prueba la estrategia de empates sin mirar el futuro. |

Ejemplos:
```
python3 justa.py --pinnacle 2.10 3.30 3.60 --casa BetPlay 2.25 3.20 3.40 --casa Wplay 2.15 3.40 3.95
python3 justa.py --nombres Más Menos --pinnacle 1.95 1.89 --casa BetPlay 2.08 1.80
python3 modelo_goles.py liga_betplay.csv "Junior" "Millonarios"
python3 modelo_goles.py liga_betplay.csv --backtest-empates 2026-01-01 --cuota-empate 3.4
```
Estimaciones, no garantías.
