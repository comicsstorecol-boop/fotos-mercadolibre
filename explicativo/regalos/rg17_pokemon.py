"""Regalos: fans de Pokémon. python3 rg17_pokemon.py fb|tt salida.mp4"""
from _tema import *
S = "pokemon"
G = {"productos": [
    dict(img=img(S, 1), nombre="GORRA TRUCKER POKÉBOLA", precio="$29.999", nota="30 AÑOS DE POKÉMON"),
    dict(img=img(S, 2), nombre="COJÍN SNORLAX", precio="$74.999", nota="EL REY DE LA SIESTA"),
    dict(img=img(S, 3), nombre="HOODIE CAPOTA PIKACHU", precio="$89.999", nota="ESCONDIDO EN EL BOSQUE"),
    dict(img=img(S, 4), nombre="PELUCHE CHARIZARD", precio="$99.999", nota="EL FAVORITO"),
    dict(img=img(S, 5), nombre="MUG 3D POKÉBOLA", precio="$99.999", nota="¡ATRÁPALOS YA!")]}
G["fb"] = [
    ("host", "¿Tienes un fan de Pokémon en tu vida y no sabes qué regalarle esta Navidad? Aquí van cinco ideas de Comics Store, para todos los presupuestos.", {"navidad", "pokémon"}),
    ("host", "Y quédate hasta el final, porque el último regalo es para atrapar… tu café.", {"atrapar", "café"}),
    ("p", 1, 0, "Número uno: la gorra trucker con la Pokébola, por menos de treinta mil pesos.", {"pokébola", "treinta"}),
    ("host", "Este año Pokémon cumplió treinta años: los primeros juegos salieron en Japón en febrero de mil novecientos noventa y seis.", {"treinta", "noventa"}, 1),
    ("p", 2, 0, "Número dos: el cojín de Snorlax, por menos de setenta y cinco mil pesos.", {"snorlax", "setenta"}),
    ("p", 2, 1, "Dicen que Snorlax se inspiró en Kōji Nishino, uno de los creadores del juego. Perfecto para la siesta navideña.", {"nishino", "siesta"}),
    NIVEL,
    ("p", 3, 0, "Número tres: el hoodie negro de Pikachu, por menos de noventa mil pesos.", {"pikachu", "noventa"}),
    ("host", "Dato: en el primer juego, Pikachu estaba escondido en un bosque y era muy difícil de encontrar.", {"bosque", "difícil"}, 3),
    ("p", 4, 0, "Número cuatro: el peluche de Charizard, por menos de cien mil pesos.", {"charizard", "cien"}),
    ("p", 4, 1, "El dragón de fuego que todo niño de los noventa quería tener en su equipo.", {"fuego", "equipo"}),
    VERDAD,
    ("p", 5, 0, "Número cinco: el mug tres de en forma de Pokébola, también por menos de cien mil pesos.", {"mug", "cien"}),
    ("host", "Y un dato para cerrar: Pokémon es la franquicia que más dinero ha generado en toda la historia. Más que cualquier película o cómic.", {"franquicia", "historia"}, 5),
    CIERRE_FB("Pokémon")]
G["tt"] = [
    ("host", "¿Qué le regalas a un fan de Pokémon esta Navidad? Cinco ideas, de menor a mayor precio.", {"navidad", "cinco"}),
    ("p", 1, 0, "Uno: la gorra trucker de la Pokébola, menos de treinta mil.", {"pokébola", "treinta"}),
    ("host", "Este año Pokémon cumplió treinta años. ¡Treinta!", {"treinta"}, 1),
    ("p", 2, 0, "Dos: el cojín de Snorlax, menos de setenta y cinco mil.", {"snorlax", "setenta"}),
    ("host", "Ideal para la siesta después de la cena de Navidad.", {"siesta"}, 2),
    ("p", 3, 0, "Tres: el hoodie de Pikachu, menos de noventa mil.", {"pikachu", "noventa"}),
    ("host", "En el primer juego, Pikachu estaba escondido en un bosque. ¡Casi nadie lo encontraba!", {"bosque"}, 3),
    ("p", 4, 0, "Cuatro: el peluche de Charizard, menos de cien mil.", {"charizard", "cien"}),
    VERDAD_TT,
    ("p", 5, 0, "Cinco: el mug tres de de Pokébola, menos de cien mil.", {"mug", "pokébola"}),
    ("host", "Pokémon es la franquicia que más dinero ha generado en la historia. ¿Cuál escoges?", {"historia"}, 5),
    TT_EXTRA,
    CIERRE_TT]
if __name__ == "__main__":
    correr(S, G, ((255, 210, 0), (240, 60, 60)), {"pokémon": ("es", "pokemon"), "pokébola": ("es", "pokebola"), "snorlax": ("en", "Snorlax"), "pikachu": ("es", "pikachu"),
           "charizard": ("en", "Charizard"), "kōji": ("es", "koyi"), "nishino": ("es", "nishino"), "mug": ("en", "mug"), "trucker": ("en", "trucker")})
