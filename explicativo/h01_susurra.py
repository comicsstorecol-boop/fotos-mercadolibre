"""Comics Store · Terror: El que susurra en la oscuridad (H. P. Lovecraft, 1931)"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
from compositor import historia
from motor import render
VERDE = (120, 255, 200); ROJO = (255, 60, 60); AMB = (255, 200, 120)
H = [
 ({"fondo": "rio", "fx": ["lluvia", "rayo"], "cam": (1, 1.12, 0, 60)}, "En mil novecientos veintisiete, una inundación arrasó Vermont… y los ríos arrastraron algo que no era de este mundo.", {"inundación", "mundo"}),
 ({"fondo": "rio", "el": [("alado", 560, 1300, .9, {"anim": "flotar"})], "fx": ["niebla"], "niebla_y": 1350, "cam": (1.05, 1.15, 0, 40)}, "Los campesinos juraron ver cuerpos extraños flotando en el agua: con alas, con pinzas… y sin rostro.", {"alas", "rostro"}),
 ({"fondo": "biblioteca", "el": [("hombre", 380, 1250, 1.0), ("libro", 720, 1200, .55, {"var": "Folclor|Miskatonic"})], "cam": (1, 1.06, 0, 0)}, "Albert Wilmarth, profesor de folclor en la Universidad de Miskatonic, pensó que eran puras leyendas.", {"leyendas"}),
 ({"fondo": "estudio", "el": [("carta", 540, 980, 1.3, {"anim": "entrar"})], "flash": True, "glows": [(540, 980, 360, AMB, 90)], "cam": (1.1, 1.0, 0, 0)}, "Hasta que recibió una carta.", {"carta"}),
 ({"fondo": "granja", "fx": ["niebla"], "cam": (1, 1.1, 0, 50)}, "La enviaba Henry Akeley, un granjero que vivía solo, en lo profundo de las colinas.", {"solo", "colinas"}),
 ({"fondo": "bosque", "glows": [(300, 1180, 16, ROJO, 255), (340, 1180, 16, ROJO, 255), (760, 1220, 14, ROJO, 255), (796, 1220, 14, ROJO, 255)], "fx": ["niebla"], "cam": (1, 1.14, 0, 80)}, "Akeley aseguraba que esas criaturas existían de verdad… y que lo estaban vigilando.", {"vigilando"}),
 ({"fondo": "estudio", "el": [("carta", 330, 900, .8, {"rot": 8}), ("piedra", 700, 1150, 1.0, {"anim": "entrar", "t0": .8})], "glows": [(700, 1150, 260, VERDE, 70)], "cam": (1, 1.08, 0, 0)}, "Le mandó fotos de huellas imposibles… y una piedra negra con símbolos que nadie podía leer.", {"piedra", "símbolos"}),
 ({"fondo": "bosque", "el": [("sonido", 540, 1000, 1.1, {"anim": "entrar"})], "fx": ["niebla"], "cam": (1, 1.1, 0, 0)}, "Pero lo peor fue un disco: una grabación hecha de noche, en medio del bosque.", {"disco", "grabación"}),
 ({"fondo": "abismo", "el": [("sonido", 540, 960, 1.3, {"anim": "temblar"})], "fx": ["particulas"], "pulso": .6, "bpm": 100, "cam": (1, 1.12, 0, 0)}, "Entre las voces humanas se oía otra… un zumbido que imitaba palabras.", {"zumbido"}),
 ({"fondo": "abismo", "glows": [(800, 420, 120, (180, 160, 255), 160)], "el": [("alado", 480, 1050, 1.3, {"anim": "entrar"})], "fx": ["particulas"], "tag": "MI-GO", "tag_y": 1500, "tag_col": VERDE, "cam": (1, 1.1, 0, 0)}, "Las criaturas se llamaban Mi-Go: seres alados que venían de Yuggoth, un mundo en el borde del sistema solar.", {"yuggoth"}),
 ({"fondo": "granja", "pulso": 1.0, "bpm": 120, "flash": True, "cam": (1.15, 1.0, 0, 0)}, "Y ahora venían por Akeley.", {"akeley"}),
 ({"fondo": "granja", "el": [("perro", 300, 1430, .45, {"anim": "desvanecer", "t0": 1.5})], "fx": ["rayo"], "cam": (1, 1.1, 0, 60)}, "Sus cartas se volvieron desesperadas: disparos en la noche, sus perros desaparecidos, el teléfono muerto.", {"disparos", "perros"}),
 ({"fondo": "biblioteca", "el": [("hombre", 540, 1250, 1.0, {"anim": "temblar"})], "velas": [(860, 1180, 90, AMB)], "cam": (1, 1.08, 0, 0)}, "Wilmarth le rogó que huyera de esa casa.", {"huyera"}),
 ({"fondo": "estudio", "el": [("carta", 540, 1000, 1.3, {"anim": "aparecer"})], "glows": [(540, 1000, 400, (255, 230, 170), 110)], "cam": (1, 1.06, 0, 0)}, "Pero entonces llegó una carta distinta. Tranquila. Casi feliz.", {"distinta"}),
 ({"fondo": "abismo", "el": [("alado", 540, 1000, 1.0, {"anim": "flotar"})], "fx": ["particulas"], "glows": [(540, 1000, 380, (120, 255, 200), 60)], "cam": (1, 1.08, 0, 0)}, "Akeley decía que todo había sido un malentendido: los Mi-Go eran sabios, y querían compartir sus secretos.", {"secretos"}),
 ({"fondo": "estudio", "el": [("carta", 300, 900, .7, {"rot": -8}), ("piedra", 760, 900, .7), ("sonido", 540, 1250, .9, {"anim": "entrar", "t0": 1.2})], "cam": (1, 1.06, 0, 0)}, "Le pedía que fuera a visitarlo… y que llevara todas las pruebas: las cartas, las fotos y el disco.", {"pruebas"}),
 ({"fondo": "granja", "el": [("hombre", 380, 1360, .7), ("sombra", 680, 1360, .75, {"anim": "aparecer"})], "fx": ["niebla"], "cam": (1, 1.08, 0, 0)}, "Wilmarth viajó a Vermont. En la estación lo esperaba un desconocido que decía ser amigo de Akeley.", {"desconocido"}),
 ({"fondo": "cuarto", "el": [("sombra", 760, 1150, .9)], "velas": [(260, 1000, 80, AMB)], "vineta": .85, "cam": (1, 1.1, 0, 0)}, "La granja estaba en silencio. Akeley lo recibió a oscuras, envuelto en una manta, sentado en un sillón.", {"oscuras"}),
 ({"fondo": "cuarto", "el": [("sombra", 760, 1150, .9, {"anim": "temblar"})], "velas": [(260, 1000, 70, AMB)], "vineta": .9, "cam": (1.05, 1.2, 80, 0)}, "Hablaba en susurros. Decía que estaba enfermo… y no movía ni la cara, ni las manos.", {"susurros"}),
 ({"fondo": "abismo", "el": [("cilindro", 540, 1000, 1.2, {"anim": "entrar"})], "glows": [(540, 1000, 330, VERDE, 90)], "cam": (1, 1.08, 0, 0)}, "Le habló de algo imposible: los Mi-Go podían sacar un cerebro humano y guardarlo vivo dentro de un cilindro de metal.", {"cerebro", "cilindro"}),
 ({"fondo": "abismo", "el": [("cilindro", 540, 1000, .9, {"anim": "flotar"})], "fx": ["particulas"], "cam": (1, 1.25, 0, 0)}, "Así, un hombre podía viajar por el espacio… sin su cuerpo.", {"espacio"}),
 ({"fondo": "biblioteca", "el": [("cilindro", 300, 1200, .6), ("cilindro", 540, 1200, .6, {"anim": "latir"}), ("cilindro", 780, 1200, .6)], "glows": [(540, 1200, 200, VERDE, 120)], "cam": (1, 1.12, 0, 60)}, "En la repisa había varios cilindros. Y uno de ellos… le habló.", {"habló"}),
 ({"fondo": "habitacion", "vineta": .85, "cam": (1, 1.08, 0, 0)}, "Esa noche, Wilmarth no pudo dormir.", {"dormir"}),
 ({"fondo": "pasillo", "el": [("sonido", 540, 820, .6, {"anim": "temblar"})], "glows": [(540, 820, 160, VERDE, 140)], "cam": (1, 1.25, 0, 0)}, "Desde la sala llegaban voces: varias… y entre ellas, ese zumbido.", {"zumbido"}),
 ({"fondo": "cuarto", "velas": [(260, 1000, 80, AMB)], "vineta": .8, "cam": (1, 1.1, 120, 40)}, "Bajó en silencio. El sillón de Akeley estaba vacío.", {"vacío"}),
 ({"fondo": "cuarto", "el": [("mascara", 740, 1080, .8, {"anim": "aparecer"}), ("mano", 600, 1260, .4, {"rot": 20}), ("mano", 900, 1260, .4, {"rot": -20})], "pulso": 1.0, "bpm": 110, "cam": (1, 1.18, 100, 40)}, "Sobre el sillón estaban la cara y las manos de Akeley… eran una máscara.", {"máscara"}),
 ({"fondo": "bosque", "glows": [(420, 1500, 120, (255, 250, 210), 200), (660, 1500, 120, (255, 250, 210), 200)], "fx": ["niebla"], "cam": (1, 1.15, 0, -80)}, "Wilmarth huyó en el carro por los caminos del bosque, sin mirar atrás.", {"huyó"}),
 ({"fondo": "negro", "el": [("sombra", 540, 1100, 1.1, {"anim": "flotar"})], "pulso": .8, "bpm": 70, "cam": (1, 1.1, 0, 0)}, "Quien le susurraba en la oscuridad… nunca fue Akeley.", {"nunca"}),
 ({"fondo": "abismo", "el": [("cilindro", 540, 1000, 1.1, {"anim": "latir"})], "glows": [(540, 1000, 300, VERDE, 110)], "cam": (1, 1.2, 0, 0)}, "Y en uno de esos cilindros… tal vez seguía su cerebro. Despierto.", {"cerebro"}),
 ({"fondo": "biblioteca", "el": [("libro", 540, 1150, 1.0, {"anim": "entrar", "var": "El que susurra|en la oscuridad"})], "tag": "H. P. LOVECRAFT · 1931", "tag_y": 700, "cam": (1, 1.06, 0, 0)}, "Lovecraft publicó este relato en mil novecientos treinta y uno. ¿Te atreverías a escuchar ese disco?", {"lovecraft", "disco"}),
]
esc, cierre = historia(H, "comics-store", "¿MÁS HISTORIAS?")
esc.append((cierre, "¿Quieres más historias de terror? Comenta y síguenos en Comics Store.", {"terror"}))
if __name__ == "__main__":
    render(esc, sys.argv[1] if len(sys.argv) > 1 else "/home/claude/terror_01_susurra.mp4", regancho_idx=10, musica="terror")
