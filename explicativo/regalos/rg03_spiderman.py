"""Guía de regalos navideños: fans de Spider-Man. Uso: python3 explicativo/regalos/rg03_spiderman.py fb|tt salida.mp4"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); EXP = os.path.dirname(HERE); sys.path.insert(0, EXP); sys.path.insert(0, os.path.dirname(EXP))
from regalos import armar
from motor import render

IMG = os.path.join(os.path.dirname(EXP), "productos", "spiderman")
ROJO, AZUL = (235, 35, 45), (40, 110, 255)
PRON = {"spider-man": ("en", "Spider-Man"), "venom": ("en", "Venom"), "stan": ("en", "Stan"), "lee": ("en", "Lee"), "steve": ("en", "Steve"),
        "ditko": ("en", "Ditko"), "peter": ("en", "Peter"), "parker": ("en", "Parker"), "mcfarlane": ("en", "McFarlane"), "todd": ("en", "Todd"),
        "trucker": ("en", "trucker"), "hoodie": ("es", "júdi"), "marvel": ("en", "Marvel"), "legends": ("en", "Legends"), "comics-store": ("es", "cómics estor")}

G = {"productos": [
    dict(img=f"{IMG}/c1.png", nombre="MOUSE PAD SPIDER-MAN", precio="$19.999", nota="NACIÓ EN 1962"),
    dict(img=f"{IMG}/c2.png", nombre="GORRA TRUCKER SPIDER-MAN", precio="$29.999", nota="UNA REVISTA A PUNTO DE CERRAR"),
    dict(img=f"{IMG}/c3.png", nombre="HOODIE SPIDER-MAN BLACK", precio="$89.999", nota="LA IDEA DE UN FAN"),
    dict(img=f"{IMG}/c4.png", nombre="ALCANCÍA VENOM", precio="$119.999", nota="DEBUTÓ EN 1988"),
    dict(img=f"{IMG}/c5.png", nombre="SPIDER-MAN RETRO MARVEL LEGENDS", precio="$259.999", nota="EDICIÓN DE COLECCIÓN")]}

G["fb"] = [
    ("host", "¿Tienes un fan de Spider-Man en tu vida y no sabes qué regalarle esta Navidad? Aquí van cinco ideas de Comics Store… para todos los bolsillos.", {"navidad", "bolsillos"}),
    ("host", "Y quédate hasta el final, porque el número cinco es la figura que todo arácnido quiere en su vitrina.", {"cinco"}),
    ("p", 1, 0, "Número uno: el mouse pad de Spider-Man, por menos de veinte mil pesos. Perfecto para el gamer o para el amigo secreto.", {"spider-man", "veinte"}),
    ("host", "Spider-Man apareció por primera vez en agosto de mil novecientos sesenta y dos, creado por Stan Lee y Steve Ditko.", {"sesenta", "ditko"}, 1),
    ("p", 2, 0, "Número dos: la gorra trucker de Spider-Man, por menos de treinta mil pesos.", {"gorra", "treinta"}),
    ("p", 2, 1, "Dato curioso: Spider-Man debutó en Amazing Fantasy número quince… el último número de una revista que iban a cancelar. Nadie esperaba que se volviera un éxito.", {"último", "cancelar"}),
    ("host", "Hasta aquí, detalles económicos. Pero espera… porque ahora subimos de nivel.", {"nivel"}),
    ("p", 3, 0, "Número tres: el hoodie de Spider-Man con el traje negro, por menos de noventa mil pesos. Perfecto para el frío de diciembre.", {"negro", "noventa"}),
    ("host", "¿Sabías que el traje negro fue idea de un fan? Marvel le compró el diseño, y en mil novecientos ochenta y cuatro Spider-Man lo estrenó en Secret Wars.", {"fan", "ochenta"}, 3),
    ("p", 4, 0, "Número cuatro: la alcancía original de Venom, por menos de ciento veinte mil pesos. Para ahorrar con estilo… villano.", {"venom", "ciento"}),
    ("p", 4, 1, "Ese traje negro estaba vivo: era un simbionte. Cuando Peter Parker lo rechazó, se unió a Eddie Brock y en mil novecientos ochenta y ocho nació Venom.", {"simbionte", "venom"}),
    ("host", "Y ahora sí… el regalo para el coleccionista de verdad.", {"verdad"}),
    ("p", 5, 0, "Número cinco: la figura Marvel Legends de Spider-Man retro, por menos de doscientos sesenta mil pesos. Una joya para la vitrina.", {"retro", "doscientos"}),
    ("host", "Más de sesenta años después de aquella revista que iban a cancelar, el trepamuros sigue siendo el héroe más querido. ¿Lo tienes en tu colección?", {"sesenta", "colección"}, 5),
    ("cierre", "Todos están en comics-store punto com punto co. ¿Cuál de los cinco le regalarías a tu fan de Spider-Man? Déjalo en los comentarios y síguenos en Comics Store.", {"comentarios"}, "¿CUÁL REGALARÍAS?")]

G["tt"] = [
    ("host", "¿Qué le regalas a un fan de Spider-Man esta Navidad? Cinco ideas, de menor a mayor precio. Y el último… es de colección.", {"navidad", "colección"}),
    ("p", 1, 0, "Uno: el mouse pad de Spider-Man, por menos de veinte mil pesos.", {"spider-man", "veinte"}),
    ("host", "Spider-Man nació en agosto de mil novecientos sesenta y dos, creado por Stan Lee y Steve Ditko.", {"sesenta", "ditko"}, 1),
    ("p", 2, 0, "Dos: la gorra trucker, menos de treinta mil. Dato: Spider-Man nació en el último número de una revista que iban a cancelar.", {"gorra", "cancelar"}),
    ("p", 3, 0, "Tres: el hoodie del traje negro, menos de noventa mil.", {"negro", "noventa"}),
    ("host", "Y ese traje negro fue idea de un fan: Marvel le compró el diseño.", {"fan"}, 3),
    ("p", 4, 0, "Cuatro: la alcancía de Venom, menos de ciento veinte mil. El simbionte que nació de ese mismo traje.", {"venom", "simbionte"}),
    ("host", "Y el número cinco… es para el coleccionista de verdad.", {"verdad"}),
    ("p", 5, 0, "Cinco: Spider-Man retro de Marvel Legends, por menos de doscientos sesenta mil.", {"retro", "doscientos"}),
    ("host", "Más de sesenta años después, sigue siendo el héroe más querido. ¿Ya lo tienes en tu colección?", {"colección"}, 5),
    ("cierre", "Todos están en comics-store punto com punto co. ¿Cuál regalarías tú? Comenta y síguenos en Comics Store.", {"comenta"}, "¿CUÁL REGALARÍAS?")]

if __name__ == "__main__":
    ver = sys.argv[1]; out = sys.argv[2] if len(sys.argv) > 2 else f"/home/claude/salidas/regalos_spiderman/{ver}.mp4"
    os.makedirs(os.path.dirname(out), exist_ok=True)
    esc, ganchos = armar(G, ver)
    render(esc, out, musica="alegre", pron=PRON, estilo="neon", y_sub=195, regancho_idx=ganchos, colores=(ROJO, AZUL))
