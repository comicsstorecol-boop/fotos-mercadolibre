"""Regalos: fans de Flash. python3 rg12_flash.py fb|tt salida.mp4"""
from _tema import *
S = "flash"
G = {"productos": [
    dict(img=img(S, 1), nombre="MOUSE PAD FLASH", precio="$19.999", nota="DESDE 1940"),
    dict(img=img(S, 2), nombre="CAMISETA ESCUDO FLASH", precio="$54.999", nota="BARRY ALLEN · 1956"),
    dict(img=img(S, 3), nombre="HOODIE CAPOTA FLASH", precio="$84.999", nota="EL HOMBRE MÁS RÁPIDO"),
    dict(img=img(S, 4), nombre="FLASH SUPER POWERS", precio="$169.999", nota="ESTILO RETRO DE LOS 80"),
    dict(img=img(S, 5), nombre="FLASH JUSTICE LEAGUE TASK FORCE", precio="$189.999", nota="WALLY WEST · VIDEOJUEGO")]}
G["fb"] = [
    ("host", "¿Tienes un fan de Flash en tu vida y no sabes qué regalarle esta Navidad? Aquí van cinco ideas de Comics Store, para todos los presupuestos.", {"navidad", "flash"}),
    ("host", "Y quédate hasta el final, porque el último Flash salió de un videojuego.", {"videojuego"}),
    ("p", 1, 0, "Número uno: el mouse pad de Flash, por menos de veinte mil pesos.", {"mouse", "veinte"}),
    ("host", "El primer Flash, Jay Garrick, apareció en mil novecientos cuarenta. Y usaba un casco con alas.", {"cuarenta", "casco"}, 1),
    ("p", 2, 0, "Número dos: la camiseta con el escudo de Flash, por menos de cincuenta y cinco mil pesos.", {"escudo", "cincuenta"}),
    ("p", 2, 1, "Este es el rayo de Barry Allen, que llegó en mil novecientos cincuenta y seis y arrancó la Edad de Plata de los cómics.", {"barry", "plata"}),
    NIVEL,
    ("p", 3, 0, "Número tres: el hoodie de Flash, por menos de ochenta y cinco mil pesos.", {"hoodie", "ochenta"}),
    ("host", "Para el más rápido de la casa… aunque en la mañana de Navidad, todos corren igual de rápido al árbol.", {"rápido", "árbol"}, 3),
    ("p", 4, 0, "Número cuatro: Flash de la línea Super Powers, de McFarlane, por menos de ciento setenta mil pesos.", {"super", "ciento"}),
    ("p", 4, 1, "Es un homenaje a los juguetes Super Powers de los años ochenta, con su empaque retro.", {"ochenta", "retro"}),
    VERDAD,
    ("p", 5, 0, "Número cinco: Flash de Justice League Task Force, de McFarlane, por menos de ciento noventa mil pesos.", {"task", "ciento"}),
    ("host", "Es Wally West, tal como salía en el videojuego de pelea de mil novecientos noventa y cinco. Y trae una pieza para armar a Darkseid.", {"wally", "darkseid"}, 5),
    CIERRE_FB("Flash")]
G["tt"] = [
    ("host", "¿Qué le regalas a un fan de Flash esta Navidad? Cinco ideas, de menor a mayor precio.", {"navidad", "cinco"}),
    ("p", 1, 0, "Uno: el mouse pad de Flash, menos de veinte mil.", {"mouse", "veinte"}),
    ("host", "Dato: el primer Flash apareció en mil novecientos cuarenta, con un casco con alas.", {"cuarenta"}, 1),
    ("p", 2, 0, "Dos: la camiseta del escudo de Flash, menos de cincuenta y cinco mil.", {"escudo", "cincuenta"}),
    ("host", "El rayo de Barry Allen, que llegó en mil novecientos cincuenta y seis.", {"barry"}, 2),
    ("p", 3, 0, "Tres: el hoodie de Flash, menos de ochenta y cinco mil.", {"hoodie", "ochenta"}),
    ("p", 4, 0, "Cuatro: Flash Super Powers, estilo retro de los ochenta, menos de ciento setenta mil.", {"super", "retro"}),
    ("host", "Un homenaje a los juguetes clásicos de los años ochenta, con todo y empaque.", {"homenaje"}, 4),
    VERDAD_TT,
    ("p", 5, 0, "Cinco: Flash de Justice League Task Force, menos de ciento noventa mil.", {"task", "ciento"}),
    ("host", "Es Wally West, del videojuego de mil novecientos noventa y cinco. Y trae una pieza de Darkseid.", {"wally", "darkseid"}, 5),
    ("host", "¿Cuál de los cinco escoges?", {"escoges"}, 5),
    TT_EXTRA,
    CIERRE_TT]
if __name__ == "__main__":
    correr(S, G, ((255, 40, 30), (255, 210, 0)), {"flash": ("en", "Flash"), "mouse": ("en", "mouse"), "pad": ("en", "pad"), "jay": ("en", "Jay"), "garrick": ("en", "Garrick"),
           "barry": ("en", "Barry"), "allen": ("en", "Allen"), "super": ("en", "Super"), "powers": ("en", "Powers"), "justice": ("en", "Justice"), "league": ("en", "League"),
           "task": ("en", "Task"), "force": ("en", "Force"), "wally": ("en", "Wally"), "west": ("en", "West"), "darkseid": ("en", "Darkseid")})
