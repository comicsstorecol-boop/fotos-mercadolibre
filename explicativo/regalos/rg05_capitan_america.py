"""Guía de regalos navideños: fans de capitan_america. Uso: python3 explicativo/regalos/rg03_spiderman.py fb|tt salida.mp4"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); EXP = os.path.dirname(HERE); sys.path.insert(0, EXP); sys.path.insert(0, os.path.dirname(EXP))
from regalos import armar
from motor import render

IMG = os.path.join(os.path.dirname(EXP), "productos", "capitan_america")
AZUL2, ROJO2 = (50, 120, 255), (240, 40, 50)
PRON = {"spider-man": ("en", "Spider-Man"), "venom": ("en", "Venom"), "stan": ("en", "Stan"), "lee": ("en", "Lee"), "steve": ("en", "Steve"),
        "ditko": ("en", "Ditko"), "peter": ("en", "Peter"), "parker": ("en", "Parker"), "mcfarlane": ("en", "McFarlane"), "todd": ("en", "Todd"),
        "trucker": ("en", "trucker"), "hoodie": ("es", "júdi"), "marvel": ("en", "Marvel"), "legends": ("en", "Legends"), "comics-store": ("es", "cómics estor"), "joe": ("en", "Joe"), "simon": ("en", "Simon"), "kirby": ("en", "Kirby"), "hitler": ("es", "jitler"), "trucker": ("en", "trucker")}

G = {"productos": [
    dict(img=f"{IMG}/c1.png", nombre="MOUSE PAD CAPITÁN AMÉRICA", precio="$19.999", nota="DESDE 1941"),
    dict(img=f"{IMG}/c2.png", nombre="GORRA TRUCKER CAPITÁN AMÉRICA", precio="$29.999", nota="CASI UN MILLÓN DE COPIAS"),
    dict(img=f"{IMG}/c3.png", nombre="TERMO CON PITILLO CAPITÁN AMÉRICA", precio="$44.999", nota="EL ESCUDO ERA TRIANGULAR"),
    dict(img=f"{IMG}/c4.png", nombre="HOODIE CAPITÁN AMÉRICA", precio="$84.999", nota="REDONDO DESDE EL #2"),
    dict(img=f"{IMG}/c5.png", nombre="CAPITÁN AMÉRICA RETRO MARVEL LEGENDS", precio="$194.999", nota="EDICIÓN RETRO")]}

G["fb"] = [
    ("host", "¿Tienes un fan del Capitán América en tu vida y no sabes qué regalarle esta Navidad? Aquí van cinco ideas de Comics Store… para todos los bolsillos.", {"navidad", "bolsillos"}),
    ("host", "Y quédate hasta el final, porque el número cinco es la figura retro que todo coleccionista quiere.", {"cinco"}),
    ("p", 1, 0, "Número uno: el mouse pad del Capitán América, por menos de veinte mil pesos.", {"capitán", "veinte"}),
    ("host", "El Capitán América nació en marzo de mil novecientos cuarenta y uno, creado por Joe Simon y Jack Kirby.", {"cuarenta", "kirby"}, 1),
    ("p", 2, 0, "Número dos: la gorra trucker del Capitán América, por menos de treinta mil pesos.", {"gorra", "treinta"}),
    ("p", 2, 1, "En la portada de su primer cómic aparecía dándole un puño a Hitler… y ese número vendió casi un millón de copias.", {"hitler", "millón"}),
    ("host", "Hasta aquí, detalles económicos. Pero espera… porque ahora subimos de nivel.", {"nivel"}),
    ("p", 3, 0, "Número tres: el termo con pitillo del Capitán América, por menos de cuarenta y cinco mil pesos.", {"termo", "cuarenta"}),
    ("host", "¿Sabías que su primer escudo no era redondo? Era triangular. Otra editorial se quejó de que se parecía a su héroe, y en el número dos lo cambiaron por el escudo circular.", {"triangular", "circular"}, 3),
    ("p", 4, 0, "Número cuatro: el hoodie del Capitán América, por menos de ochenta y cinco mil pesos. Perfecto para el frío de diciembre.", {"hoodie", "ochenta"}),
    ("p", 4, 1, "Y ese escudo redondo se volvió el símbolo del personaje: hoy lo reconoce cualquiera, fan o no fan.", {"escudo", "símbolo"}),
    ("host", "Y ahora sí… el regalo para el coleccionista de verdad.", {"verdad"}),
    ("p", 5, 0, "Número cinco: el Capitán América retro de Marvel Legends, por menos de ciento noventa y cinco mil pesos. Con su caja estilo vintage.", {"retro", "ciento"}),
    ("host", "Más de ochenta años después, el centinela de la libertad sigue en pie. ¿Ya lo tienes en tu colección?", {"ochenta", "colección"}, 5),
    ("cierre", "Todos están en comics-store punto com punto co. ¿Cuál de los cinco le regalarías a tu fan del Capitán América? Déjalo en los comentarios y síguenos en Comics Store.", {"comentarios"}, "¿CUÁL REGALARÍAS?")]

G["tt"] = [
    ("host", "¿Qué le regalas a un fan del Capitán América esta Navidad? Cinco ideas, de menor a mayor precio.", {"navidad", "cinco"}),
    ("p", 1, 0, "Uno: el mouse pad del Capitán América, por menos de veinte mil pesos.", {"capitán", "veinte"}),
    ("host", "El Capitán América nació en mil novecientos cuarenta y uno, creado por Joe Simon y Jack Kirby.", {"cuarenta", "kirby"}, 1),
    ("p", 2, 0, "Dos: la gorra trucker, menos de treinta mil. Su primer cómic, de mil novecientos cuarenta y uno, vendió casi un millón de copias.", {"gorra", "millón"}),
    ("p", 3, 0, "Tres: el termo con pitillo, menos de cuarenta y cinco mil.", {"termo", "cuarenta"}),
    ("host", "Dato: su primer escudo era triangular. Lo cambiaron a redondo en el número dos.", {"triangular", "redondo"}, 3),
    ("p", 4, 0, "Cuatro: el hoodie del Capitán, menos de ochenta y cinco mil.", {"hoodie", "ochenta"}),
    ("host", "Y el número cinco… es para el coleccionista de verdad.", {"verdad"}),
    ("p", 5, 0, "Cinco: el Capitán América retro de Marvel Legends, por menos de ciento noventa y cinco mil.", {"retro", "ciento"}),
    ("host", "Más de ochenta años después, sigue siendo el centinela de la libertad. ¿Ya lo tienes en tu colección?", {"colección"}, 5),
    ("cierre", "Todos están en comics-store punto com punto co. ¿Cuál regalarías tú? Comenta y síguenos en Comics Store.", {"comenta"}, "¿CUÁL REGALARÍAS?")]

if __name__ == "__main__":
    ver = sys.argv[1]; out = sys.argv[2] if len(sys.argv) > 2 else f"/home/claude/salidas/regalos_capitan_america/{ver}.mp4"
    os.makedirs(os.path.dirname(out), exist_ok=True)
    esc, ganchos = armar(G, ver)
    render(esc, out, musica="alegre", pron=PRON, estilo="neon", y_sub=195, regancho_idx=ganchos, colores=(AZUL2, ROJO2))
