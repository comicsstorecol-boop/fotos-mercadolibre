"""Comics Store · Terror: La pata de mono (W. W. Jacobs, 1902)"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
from compositor import historia
from motor import render
AMB = (255, 200, 120); FUEGO = (255, 130, 50); ORO = (255, 210, 90)
H = [
 ({"fondo": "estudio", "el": [("pata_mono", 540, 1050, 1.1, {"anim": "aparecer"})], "glows": [(540, 1050, 300, FUEGO, 70)], "cam": (1, 1.15, 0, 0)}, "Imagina que puedes pedir tres deseos. Ahora imagina que cada uno se cumple… de la peor manera posible.", {"tres", "peor"}),
 ({"fondo": "casa", "fx": ["lluvia"], "cam": (1, 1.1, 0, 60)}, "Una noche de tormenta, en una casa de Inglaterra, la familia White recibe una visita.", {"white"}),
 ({"fondo": "cuarto", "el": [("hombre", 280, 1250, .8), ("mujer", 520, 1260, .75), ("nino", 760, 1280, .8)], "velas": [(900, 1080, 130, FUEGO)], "cam": (1, 1.06, 0, 0)}, "El señor White, su esposa y su hijo Herbert escuchan a un viejo amigo: un sargento que regresó de la India.", {"herbert", "india"}),
 ({"fondo": "cuarto", "el": [("pata_mono", 540, 1100, 1.0, {"anim": "entrar"})], "velas": [(900, 1080, 130, FUEGO)], "vineta": .85, "cam": (1, 1.1, 0, 0)}, "De su bolsillo saca algo extraño: una pata de mono, seca y arrugada.", {"pata"}),
 ({"fondo": "abismo", "el": [("pata_mono", 540, 1050, .9, {"anim": "flotar"})], "fx": ["particulas"], "tag": "3 DESEOS", "tag_y": 1500, "tag_col": ORO, "cam": (1, 1.1, 0, 0)}, "Cuenta que un viejo faquir le echó un hechizo: tres hombres podrán pedirle tres deseos cada uno.", {"hechizo", "deseos"}),
 ({"fondo": "cuarto", "el": [("hombre", 540, 1250, .9, {"anim": "temblar"})], "velas": [(900, 1080, 130, FUEGO)], "vineta": .85, "cam": (1, 1.08, 0, 0)}, "Pero el sargento está pálido. Él ya pidió los suyos… y no quiere hablar de lo que pasó.", {"pálido"}),
 ({"fondo": "cuarto", "el": [("pata_mono", 820, 1150, .6, {"anim": "caer"})], "glows": [(820, 1200, 260, FUEGO, 200)], "fx": ["chispas"], "cam": (1, 1.1, 60, 0)}, "De pronto, lanza la pata al fuego. Pero el señor White, curioso, la rescata.", {"fuego", "rescata"}),
 ({"fondo": "cuarto", "el": [("nino", 760, 1280, .8), ("hombre", 340, 1250, .8)], "velas": [(900, 1080, 120, FUEGO)], "cam": (1, 1.06, 0, 0)}, "Esa noche, Herbert se ríe del hechizo y le dice a su padre: pide doscientas libras para terminar de pagar la casa.", {"doscientas"}),
 ({"fondo": "negro", "el": [("pata_mono", 540, 1050, 1.1, {"anim": "temblar"})], "glows": [(540, 1050, 280, FUEGO, 110)], "pulso": .8, "bpm": 100, "flash": True, "cam": (1.12, 1.0, 0, 0)}, "El señor White lo pide en voz alta… y siente cómo la pata se retuerce en su mano.", {"retuerce"}),
 ({"fondo": "estudio", "el": [("dinero", 540, 1050, .9, {"anim": "aparecer"})], "vineta": .8, "cam": (1, 1.06, 0, 0)}, "Pero no aparece ningún dinero. Se ríen, y se van a dormir.", {"dinero"}),
 ({"fondo": "calle", "el": [("nino", 540, 1440, .6, {"anim": "caminar_der", "dist": 200})], "cam": (1, 1.06, 0, 0)}, "Al día siguiente, Herbert sale a trabajar a la fábrica, como siempre.", {"fábrica"}),
 ({"fondo": "casa", "el": [("sombra", 540, 1380, .6, {"anim": "aparecer"})], "vineta": .85, "cam": (1, 1.08, 0, 0)}, "Esa tarde, un hombre desconocido toca la puerta de los White.", {"desconocido"}),
 ({"fondo": "negro", "pulso": 1.0, "bpm": 60, "flash": True, "cam": (1.15, 1.0, 0, 0)}, "Herbert murió. Un accidente con las máquinas.", {"murió"}),
 ({"fondo": "estudio", "el": [("dinero", 540, 1050, 1.0, {"anim": "aparecer"})], "pulso": .7, "bpm": 70, "tag": "£ 200", "tag_y": 1400, "tag_col": ORO, "cam": (1, 1.12, 0, 0)}, "La empresa ofrece una compensación a la familia: exactamente doscientas libras.", {"doscientas"}),
 ({"fondo": "cementerio", "fx": ["niebla"], "cam": (1, 1.08, 0, 40)}, "Entierran a Herbert en el cementerio, a un par de kilómetros de la casa.", {"cementerio"}),
 ({"fondo": "habitacion", "el": [("mujer", 540, 1140, .7, {"anim": "temblar"})], "vineta": .9, "cam": (1, 1.08, 0, 0)}, "Una semana después, a medianoche, la señora White despierta gritando.", {"medianoche"}),
 ({"fondo": "cuarto", "el": [("pata_mono", 540, 1100, .9, {"anim": "latir"})], "pulso": .9, "bpm": 110, "cam": (1, 1.15, 0, 0)}, "¡La pata! Todavía quedan dos deseos. Le exige a su esposo que pida que su hijo vuelva a la vida.", {"vida"}),
 ({"fondo": "negro", "el": [("pata_mono", 540, 1050, 1.0, {"anim": "temblar"})], "glows": [(540, 1050, 260, FUEGO, 100)], "cam": (1, 1.1, 0, 0)}, "Él tiembla. Herbert llevaba días enterrado… y el accidente lo había dejado irreconocible. Aun así, pide el deseo.", {"irreconocible"}),
 ({"fondo": "cuarto", "velas": [(260, 1000, 60, AMB)], "vineta": .9, "cam": (1, 1.06, 0, 0)}, "No pasa nada. La vela se apaga. Silencio.", {"silencio"}),
 ({"fondo": "casa", "fx": ["lluvia"], "pulso": 1.0, "bpm": 50, "flash": True, "cam": (1.12, 1.0, 0, 0)}, "Y entonces… alguien golpea la puerta.", {"golpea"}),
 ({"fondo": "pasillo", "el": [("mujer", 540, 1350, .5, {"anim": "caminar_izq", "dist": 0})], "pulso": 1.0, "bpm": 120, "cam": (1, 1.25, 0, 0)}, "¡Es Herbert! La madre corre a la puerta y lucha con el cerrojo.", {"herbert", "cerrojo"}),
 ({"fondo": "negro", "el": [("pata_mono", 540, 1050, .9, {"anim": "temblar"})], "pulso": 1.2, "bpm": 160, "cam": (1, 1.15, 0, 0)}, "Los golpes son cada vez más fuertes. El padre busca la pata en el suelo, desesperado… y pide su último deseo.", {"último"}),
 ({"fondo": "negro", "flash": True, "vineta": .95, "cam": (1, 1.04, 0, 0)}, "Los golpes se detienen de golpe.", {"detienen"}),
 ({"fondo": "calle", "fx": ["niebla"], "vineta": .8, "cam": (1, 1.1, 0, 40)}, "La puerta se abre. Afuera solo hay un camino vacío… bajo la luz de un farol.", {"vacío"}),
 ({"fondo": "estudio", "el": [("pata_mono", 540, 1050, 1.0)], "glows": [(540, 1050, 280, FUEGO, 70)], "cam": (1, 1.1, 0, 0)}, "Nunca sabremos qué estaba detrás de esa puerta. Ni cuál fue el tercer deseo.", {"tercer"}),
 ({"fondo": "biblioteca", "el": [("libro", 540, 1150, 1.0, {"anim": "entrar", "var": "La pata|de mono"})], "tag": "W. W. JACOBS · 1902", "tag_y": 700, "cam": (1, 1.06, 0, 0)}, "La pata de mono fue escrita por W. W. Jacobs en mil novecientos dos. Y nos dejó una lección: ten cuidado con lo que deseas.", {"cuidado"}),
]
esc, cierre = historia(H, "comics-store", "¿CUÁL FUE EL 3.er DESEO?")
esc.append((cierre, "¿Cuál crees que fue el tercer deseo? Comenta y síguenos en Comics Store.", {"tercer"}))
if __name__ == "__main__":
    render(esc, sys.argv[1] if len(sys.argv) > 1 else "/home/claude/terror_05_pata_mono.mp4", regancho_idx=12, musica="terror")
