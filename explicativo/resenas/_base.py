import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); EXP = os.path.dirname(HERE)
sys.path.insert(0, EXP); sys.path.insert(0, os.path.dirname(EXP))
from resena import resena_completa
from motor import render
AMB = (255, 200, 120); AZ = (150, 190, 255); ROJO = (220, 40, 50); FRIO = (170, 200, 255); VERDE_T = (120, 255, 140); ORO = (255, 210, 100)
def en(*ws): return {w.lower().strip(".,"): ("en", w) for w in ws}
GANCHO = "Hay historias que deberían permanecer enterradas… Esta noche, vamos a despertar una de ellas."
def correr(esc, ganchos, nombre, pron):
    out = sys.argv[1] if len(sys.argv) > 1 else f"/home/claude/resena_{nombre}.mp4"
    render(esc, out, musica="terror", pron=pron, estilo="neon", y_sub=330, regancho_idx=ganchos)
