"""Guía de regalos navideños: fans de hulk. Uso: python3 explicativo/regalos/rg03_spiderman.py fb|tt salida.mp4"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); EXP = os.path.dirname(HERE); sys.path.insert(0, EXP); sys.path.insert(0, os.path.dirname(EXP))
from regalos import armar
from motor import render

IMG = os.path.join(os.path.dirname(EXP), "productos", "hulk")
VERDE, MORADO = (60, 220, 60), (170, 80, 255)
PRON = {"spider-man": ("en", "Spider-Man"), "venom": ("en", "Venom"), "stan": ("en", "Stan"), "lee": ("en", "Lee"), "steve": ("en", "Steve"),
        "ditko": ("en", "Ditko"), "peter": ("en", "Peter"), "parker": ("en", "Parker"), "mcfarlane": ("en", "McFarlane"), "todd": ("en", "Todd"),
        "trucker": ("en", "trucker"), "hoodie": ("es", "júdi"), "marvel": ("en", "Marvel"), "legends": ("en", "Legends"), "comics-store": ("es", "cómics estor"), "hulk": ("es", "jolk"), "red": ("en", "Red"), "brand": ("en", "Brand"), "new": ("en", "New"), "day": ("en", "Day"), "ruffalo": ("en", "Ruffalo"), "bruce": ("en", "Bruce"), "banner": ("en", "Banner"), "holland": ("en", "Holland"), "harrison": ("en", "Harrison"), "ford": ("en", "Ford"), "thunderbolt": ("en", "Thunderbolt"), "ross": ("en", "Ross"), "frankenstein": ("es", "frankenstein"), "jekyll": ("en", "Jekyll"), "hyde": ("en", "Hyde"), "kirby": ("en", "Kirby")}

G = {"productos": [
    dict(img=f"{IMG}/c1.png", nombre="MOUSE PAD HULK", precio="$19.999", nota="NACIÓ EN 1962"),
    dict(img=f"{IMG}/c2.png", nombre="CAMISETA HULK RETRO", precio="$54.999", nota="¡ORIGINALMENTE GRIS!"),
    dict(img=f"{IMG}/c3.png", nombre="MUG 3D HULK", precio="$84.999", nota="FRANKENSTEIN + JEKYLL"),
    dict(img=f"{IMG}/c4.png", nombre="HULK BRAND NEW DAY", precio="$254.999", nota="DE LA PELÍCULA 2026"),
    dict(img=f"{IMG}/c5.png", nombre="RED HULK MARVEL LEGENDS", precio="$289.999", nota="EL GENERAL ROSS")]}

G["fb"] = [
    ("host", "¿Tienes un fan de Hulk en tu vida y no sabes qué regalarle esta Navidad? Aquí van cinco ideas de Comics Store… para todos los bolsillos.", {"navidad", "bolsillos"}),
    ("host", "Y quédate hasta el final, porque el número cinco es un Hulk… que no es verde.", {"verde"}),
    ("p", 1, 0, "Número uno: el mouse pad de Hulk, por menos de veinte mil pesos. Perfecto para el gamer o el amigo secreto.", {"hulk", "veinte"}),
    ("host", "Hulk nació en mayo de mil novecientos sesenta y dos, creado por Stan Lee y Jack Kirby.", {"sesenta", "kirby"}, 1),
    ("p", 2, 0, "Número dos: la camiseta retro de Hulk, por menos de cincuenta y cinco mil pesos.", {"retro", "cincuenta"}),
    ("p", 2, 1, "Y aquí va el dato que pocos saben: en su primer cómic Hulk era gris. La imprenta no lograba un gris parejo… y Stan Lee lo cambió a verde.", {"gris", "verde"}),
    ("host", "Hasta aquí, detalles económicos. Pero espera… porque ahora subimos de nivel.", {"nivel"}),
    ("p", 3, 0, "Número tres: el mug en tres de de Hulk, por menos de ochenta y cinco mil pesos. Café con fuerza de gigante esmeralda.", {"mug", "ochenta"}),
    ("host", "Stan Lee se inspiró en dos clásicos del terror: Frankenstein y el extraño caso del doctor Jekyll y míster Hyde.", {"frankenstein", "jekyll"}, 3),
    ("p", 4, 0, "Número cuatro: el Hulk de Spider-Man Brand New Day, de Marvel Legends, por menos de doscientos cincuenta y cinco mil pesos.", {"brand", "doscientos"}),
    ("p", 4, 1, "Es el Hulk salvaje de la película de este año, donde Mark Ruffalo volvió como Bruce Banner junto al Spider-Man de Tom Holland.", {"salvaje", "ruffalo"}),
    ("host", "Y ahora sí… el regalo para el coleccionista de verdad.", {"verdad"}),
    ("p", 5, 0, "Número cinco: Red Hulk de Marvel Legends, por menos de doscientos noventa mil pesos. Una bestia para la vitrina.", {"red", "doscientos"}),
    ("host", "Red Hulk apareció en dos mil ocho, y detrás de él estaba el general Thunderbolt Ross, el eterno enemigo de Banner. En el cine lo interpretó Harrison Ford.", {"ross", "ford"}, 5),
    ("cierre", "Todos están en comics-store punto com punto co. ¿Cuál de los cinco le regalarías a tu fan de Hulk? Déjalo en los comentarios y síguenos en Comics Store.", {"comentarios"}, "¿CUÁL REGALARÍAS?")]

G["tt"] = [
    ("host", "¿Qué le regalas a un fan de Hulk esta Navidad? Cinco ideas, de menor a mayor precio. Y el último… no es verde.", {"navidad", "verde"}),
    ("p", 1, 0, "Uno: el mouse pad de Hulk, por menos de veinte mil pesos.", {"hulk", "veinte"}),
    ("host", "Hulk nació en mil novecientos sesenta y dos, creado por Stan Lee y Jack Kirby.", {"sesenta", "kirby"}, 1),
    ("p", 2, 0, "Dos: la camiseta retro, menos de cincuenta y cinco mil. Dato: en su primer cómic, Hulk era gris.", {"retro", "gris"}),
    ("p", 3, 0, "Tres: el mug en tres de de Hulk, menos de ochenta y cinco mil.", {"mug", "ochenta"}),
    ("host", "Stan Lee lo creó inspirado en Frankenstein y en Jekyll y Hyde.", {"frankenstein"}, 3),
    ("p", 4, 0, "Cuatro: el Hulk salvaje de Spider-Man Brand New Day, menos de doscientos cincuenta y cinco mil.", {"salvaje", "doscientos"}),
    ("host", "Y el número cinco… es para el coleccionista de verdad.", {"verdad"}),
    ("p", 5, 0, "Cinco: Red Hulk, el general Ross transformado, por menos de doscientos noventa mil.", {"red", "ross"}),
    ("host", "Red Hulk apareció en dos mil ocho, y en el cine lo interpretó Harrison Ford. ¿Ya lo tienes?", {"ford"}, 5),
    ("cierre", "Todos están en comics-store punto com punto co. ¿Cuál regalarías tú? Comenta y síguenos en Comics Store.", {"comenta"}, "¿CUÁL REGALARÍAS?")]

if __name__ == "__main__":
    ver = sys.argv[1]; out = sys.argv[2] if len(sys.argv) > 2 else f"/home/claude/salidas/regalos_hulk/{ver}.mp4"
    os.makedirs(os.path.dirname(out), exist_ok=True)
    esc, ganchos = armar(G, ver)
    render(esc, out, musica="alegre", pron=PRON, estilo="neon", y_sub=195, regancho_idx=ganchos, colores=(VERDE, MORADO))
