"""Regalos: fans de la Liga de la Justicia (Wonder Woman y Aquaman). python3 rg19_liga_justicia.py fb|tt salida.mp4"""
from _tema import *
S = "liga_justicia"
G = {"productos": [
    dict(img=img(S, 1), nombre="GORRA TRUCKER WONDER WOMAN", precio="$29.999", nota="DESDE 1941"),
    dict(img=img(S, 2), nombre="CAMISETA AQUAMAN", precio="$54.999", nota="EL REY DE ATLANTIS"),
    dict(img=img(S, 3), nombre="MUG 3D WONDER WOMAN", precio="$94.999", nota="EL LAZO DE LA VERDAD"),
    dict(img=img(S, 4), nombre="AQUAMAN SUPER FRIENDS RETRO", precio="$164.900", nota="ESTILO CLÁSICO"),
    dict(img=img(S, 5), nombre="AQUAMAN DC MULTIVERSE JLA", precio="$179.999", nota="PIEZA DE PLASTIC MAN")]}
G["fb"] = [
    ("host", "¿Tienes un fan de la Liga de la Justicia y no sabes qué regalarle esta Navidad? Aquí van cinco ideas de Comics Store, con la Mujer Maravilla y Aquaman.", {"liga", "navidad"}),
    ("host", "Y quédate, porque hay un dato de la Mujer Maravilla que tiene que ver con… detectar mentiras.", {"mentiras"}),
    ("p", 1, 0, "Número uno: la gorra trucker de Wonder Woman, por menos de treinta mil pesos.", {"gorra", "treinta"}),
    ("host", "La Liga de la Justicia apareció en mil novecientos sesenta, con siete miembros fundadores. Y estos dos estaban ahí.", {"sesenta", "siete"}, 1),
    ("p", 2, 0, "Número dos: la camiseta de Aquaman, por menos de cincuenta y cinco mil pesos.", {"aquaman", "cincuenta"}),
    ("p", 2, 1, "Aquaman nació en mil novecientos cuarenta y uno… pero su primera portada llegó casi veinte años después, justo con la Liga.", {"cuarenta", "portada"}),
    NIVEL,
    ("p", 3, 0, "Número tres: el mug tres de de Wonder Woman, por menos de noventa y cinco mil pesos.", {"mug", "noventa"}),
    ("host", "Su creador, el psicólogo William Moulton Marston, ayudó a desarrollar el detector de mentiras. Por eso ella tiene el Lazo de la Verdad.", {"detector", "verdad"}, 3),
    ("p", 4, 0, "Número cuatro: Aquaman de Super Friends, estilo retro, por menos de ciento sesenta y cinco mil pesos.", {"super", "ciento"}),
    ("p", 4, 1, "Un homenaje a los Súper Amigos, la caricatura con la que muchos conocimos a la Liga.", {"amigos", "caricatura"}),
    VERDAD,
    ("p", 5, 0, "Número cinco: Aquaman de DC Multiverse, por menos de ciento ochenta mil pesos.", {"multiverse", "ciento"}),
    ("host", "Y trae una pieza para armar a Plastic Man. Para el coleccionista que lo quiere todo.", {"plastic", "coleccionista"}, 5),
    CIERRE_FB("la Liga de la Justicia")]
G["tt"] = [
    ("host", "¿Qué le regalas a un fan de la Liga de la Justicia esta Navidad? Cinco ideas, de menor a mayor precio.", {"liga", "cinco"}),
    ("p", 1, 0, "Uno: la gorra trucker de Wonder Woman, menos de treinta mil.", {"gorra", "treinta"}),
    ("host", "Dato: la Liga apareció en mil novecientos sesenta, con siete fundadores.", {"sesenta"}, 1),
    ("p", 2, 0, "Dos: la camiseta de Aquaman, menos de cincuenta y cinco mil.", {"aquaman", "cincuenta"}),
    ("host", "Aquaman nació en mil novecientos cuarenta y uno, pero su primera portada fue con la Liga.", {"portada"}, 2),
    ("p", 3, 0, "Tres: el mug tres de de Wonder Woman, menos de noventa y cinco mil.", {"mug", "noventa"}),
    ("host", "Su creador ayudó a inventar el detector de mentiras. De ahí el Lazo de la Verdad.", {"detector", "verdad"}, 3),
    ("p", 4, 0, "Cuatro: Aquaman de Super Friends, estilo retro, menos de ciento sesenta y cinco mil.", {"super", "retro"}),
    ("host", "Un homenaje a la caricatura de los Súper Amigos.", {"amigos"}, 4),
    VERDAD_TT,
    ("p", 5, 0, "Cinco: Aquaman de DC Multiverse, menos de ciento ochenta mil. ¡Con pieza de Plastic Man!", {"multiverse", "plastic"}),
    ("host", "¿Cuál de los cinco escoges?", {"escoges"}, 5),
    TT_EXTRA,
    CIERRE_TT]
if __name__ == "__main__":
    correr(S, G, ((60, 160, 255), (255, 200, 40)), {"wonder": ("en", "Wonder"), "woman": ("en", "Woman"), "aquaman": ("en", "Aquaman"), "william": ("en", "William"),
           "moulton": ("en", "Moulton"), "marston": ("en", "Marston"), "super": ("en", "Super"), "friends": ("en", "Friends"), "multiverse": ("en", "Multiverse"),
           "plastic": ("en", "Plastic"), "man": ("en", "Man"), "mug": ("en", "mug"), "trucker": ("en", "trucker")})
