"""Comics Store · Terror: El Horla (Guy de Maupassant, 1887)"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
from compositor import historia
from motor import render
AMB = (255, 200, 120); AZ = (140, 180, 255); FUEGO = (255, 120, 40)
H = [
 ({"fondo": "estudio", "el": [("libro", 540, 1050, 1.0, {"anim": "aparecer", "var": "Diario|8 de mayo"})], "velas": [(820, 1250, 80, AMB)], "cam": (1, 1.08, 0, 0)}, "Esto es el diario de un hombre que se volvió loco… o que descubrió algo que nadie más podía ver.", {"loco", "ver"}),
 ({"fondo": "rio", "el": [("barco", 680, 1250, .7, {"anim": "caminar_izq", "dist": 300})], "glows": [(540, 1300, 200, AMB, 60)], "cam": (1, 1.08, 0, 0)}, "Una mañana de mayo, frente a su casa en Francia, ve pasar por el río un hermoso barco brasileño. Feliz, lo saluda.", {"brasileño", "saluda"}),
 ({"fondo": "habitacion", "pulso": .5, "bpm": 90, "cam": (1, 1.08, 0, 0)}, "Desde ese día, todo empieza a cambiar. Tiene fiebre. Está triste sin razón.", {"fiebre"}),
 ({"fondo": "habitacion", "el": [("sombra", 540, 1150, .8, {"anim": "aparecer"})], "pulso": .9, "bpm": 110, "vineta": .9, "cam": (1, 1.15, 0, 60)}, "Y en las noches tiene una pesadilla horrible: siente que alguien se sienta sobre su pecho… y lo ahoga.", {"pecho", "ahoga"}),
 ({"fondo": "mar", "fx": ["niebla"], "cam": (1, 1.1, 0, 0)}, "Los médicos le recomiendan un viaje. Se va unos días y se siente mejor.", {"viaje"}),
 ({"fondo": "habitacion", "el": [("agua_vaso", 820, 1160, .6)], "vineta": .8, "cam": (1, 1.06, 0, 0)}, "Pero al volver a casa, las pesadillas regresan. Y una noche, nota algo extraño.", {"extraño"}),
 ({"fondo": "estudio", "el": [("agua_vaso", 540, 1050, 1.2, {"var": "vacio", "anim": "aparecer"})], "tag": "LA JARRA ESTÁ VACÍA", "tag_y": 1450, "tag_col": AZ, "cam": (1, 1.12, 0, 0)}, "Antes de dormir había dejado una jarra llena de agua. Al despertar… estaba vacía.", {"vacía"}),
 ({"fondo": "habitacion", "velas": [(820, 1150, 70, AMB)], "vineta": .85, "cam": (1, 1.06, 0, 0)}, "Él no se había levantado. La puerta estaba cerrada con llave. Nadie había entrado.", {"nadie"}),
 ({"fondo": "estudio", "el": [("agua_vaso", 540, 1050, 1.1, {"var": "vacio"})], "glows": [(540, 1050, 260, AZ, 60)], "cam": (1, 1.1, 0, 0)}, "Hace una prueba: envuelve la jarra en tela blanca y se mancha los labios con grafito. Si él bebe, lo sabrá.", {"prueba"}),
 ({"fondo": "estudio", "el": [("agua_vaso", 540, 1050, 1.1, {"var": "vacio", "anim": "temblar"})], "pulso": 1.0, "bpm": 120, "flash": True, "cam": (1.15, 1.0, 0, 0)}, "A la mañana siguiente, la tela está limpia… y el agua, otra vez, desapareció.", {"desapareció"}),
 ({"fondo": "negro", "el": [("sombra", 540, 1100, 1.0, {"anim": "flotar"})], "vineta": .9, "cam": (1, 1.1, 0, 0)}, "Ya no hay duda: hay alguien más en la casa. Alguien invisible.", {"invisible"}),
 ({"fondo": "granja", "el": [("rosa", 540, 1250, .9, {"anim": "caer"})], "fx": ["niebla"], "cam": (1, 1.1, 0, 60)}, "Un día, en su jardín, ve cómo una rosa se dobla… y se arranca sola, como si una mano invisible la tomara.", {"rosa", "mano"}),
 ({"fondo": "biblioteca", "el": [("libro", 540, 1150, .9, {"anim": "balancear", "var": "|"})], "velas": [(840, 1180, 80, AMB)], "cam": (1, 1.08, 0, 0)}, "Otra noche, mientras lee, ve cómo la página de un libro se pasa sola.", {"página", "sola"}),
 ({"fondo": "negro", "el": [("sombra", 540, 1100, 1.1, {"anim": "aparecer"})], "pulso": .9, "bpm": 95, "tag": "EL HORLA", "tag_y": 1500, "tag_col": AZ, "cam": (1, 1.12, 0, 0)}, "Le pone un nombre a esa presencia: el Horla. Y siente que lo controla, que le quita la voluntad.", {"horla", "voluntad"}),
 ({"fondo": "estudio", "el": [("carta", 540, 1050, 1.2, {"anim": "entrar"})], "tag": "SÃO PAULO, BRASIL", "tag_y": 620, "cam": (1, 1.06, 0, 0)}, "Entonces lee una noticia: en Brasil hay una epidemia de locura. La gente dice que seres invisibles se alimentan de ellos.", {"brasil", "invisibles"}),
 ({"fondo": "rio", "el": [("barco", 540, 1250, .8, {"anim": "aparecer"})], "flash": True, "pulso": .8, "bpm": 110, "cam": (1.15, 1.0, 0, 0)}, "Y lo entiende todo: el Horla llegó en aquel barco brasileño… el mismo que él saludó.", {"barco", "saludó"}),
 ({"fondo": "habitacion", "el": [("espejo", 540, 1050, 1.1)], "vineta": .85, "cam": (1, 1.1, 0, 0)}, "Una noche se para frente al espejo, esperando atraparlo.", {"espejo"}),
 ({"fondo": "habitacion", "el": [("espejo", 540, 1050, 1.1), ("hombre", 540, 1080, .35, {"anim": "desvanecer", "t0": .6})], "pulso": 1.0, "bpm": 130, "cam": (1, 1.2, 0, 0)}, "Y su propio reflejo desaparece. Algo transparente estaba de pie entre él y el espejo.", {"reflejo", "transparente"}),
 ({"fondo": "casa", "fx": ["niebla"], "cam": (1, 1.1, 0, 0)}, "Decide matarlo. Pone persianas de hierro y una puerta de metal en su cuarto.", {"matarlo"}),
 ({"fondo": "casa", "glows": [(690, 1075, 160, FUEGO, 200)], "pulso": .7, "bpm": 100, "cam": (1, 1.12, 0, 0)}, "Una noche siente al Horla en la habitación, sale de golpe, cierra todo con llave… y prende fuego a la casa.", {"fuego"}),
 ({"fondo": "casa", "glows": [(540, 1150, 420, FUEGO, 210), (300, 1250, 220, (255, 200, 60), 160)], "fx": ["chispas"], "cam": (1, 1.1, 0, -40)}, "La casa arde toda la noche. En medio del caos, recuerda que sus sirvientes también dormían adentro.", {"arde"}),
 ({"fondo": "negro", "el": [("hombre", 540, 1300, .9, {"anim": "temblar"})], "glows": [(540, 1500, 380, FUEGO, 120)], "cam": (1, 1.1, 0, 0)}, "Mira las llamas y se pregunta: ¿puede morir algo que no tiene cuerpo?", {"morir"}),
 ({"fondo": "negro", "el": [("sombra", 540, 1100, 1.0, {"anim": "flotar"})], "pulso": .8, "bpm": 70, "cam": (1, 1.15, 0, 0)}, "Y llega a la peor conclusión: el Horla no está muerto. Sigue ahí… esperando.", {"esperando"}),
 ({"fondo": "biblioteca", "el": [("libro", 540, 1150, 1.0, {"anim": "entrar", "var": "El Horla|Maupassant"})], "tag": "GUY DE MAUPASSANT · 1887", "tag_y": 700, "cam": (1, 1.06, 0, 0)}, "Guy de Maupassant publicó El Horla en mil ochocientos ochenta y siete. Hasta hoy se discute si es una historia de terror… o el diario de una mente rota.", {"maupassant"}),
]
esc, cierre = historia(H, "comics-store", "¿LOCURA O REALIDAD?")
esc.append((cierre, "¿Tú qué crees: locura o realidad? Comenta y síguenos en Comics Store.", {"locura", "realidad"}))
if __name__ == "__main__":
    render(esc, sys.argv[1] if len(sys.argv) > 1 else "/home/claude/terror_03_horla.mp4", regancho_idx=9, musica="terror")
