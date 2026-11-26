"""Regalos: fans de One Piece. python3 rg15_one_piece.py fb|tt salida.mp4"""
from _tema import *
S = "one_piece"
G = {"productos": [
    dict(img=img(S, 1), nombre="CAMISETA LUFFY GEAR 5", precio="$54.999", nota="DESDE 1997"),
    dict(img=img(S, 2), nombre="FIGURA LUFFY CON BASE", precio="$64.999", nota="EL REY DE LOS PIRATAS"),
    dict(img=img(S, 3), nombre="FIGURA RORONOA ZORO", precio="$99.999", nota="ESTILO DE TRES ESPADAS"),
    dict(img=img(S, 4), nombre="TAZA 3D SOMBRERO DE PAJA", precio="$119.999", nota="+600 MILLONES DE COPIAS"),
    dict(img=img(S, 5), nombre="FIGURA SHANKS", precio="$184.999", nota="EL DEL SOMBRERO")]}
G["fb"] = [
    ("host", "¿Tienes un fan de One Piece en tu vida y no sabes qué regalarle esta Navidad? Aquí van cinco ideas de Comics Store, para todos los presupuestos.", {"navidad", "piece"}),
    ("host", "Y quédate hasta el final, porque ahí está el dueño original del sombrero de paja.", {"sombrero", "paja"}),
    ("p", 1, 0, "Número uno: la camiseta de Luffy en Gear cinco, por menos de cincuenta y cinco mil pesos.", {"gear", "cincuenta"}),
    ("host", "One Piece empezó en mil novecientos noventa y siete, en la revista Shonen Jump, creado por Eiichiro Oda.", {"noventa", "oda"}, 1),
    ("p", 2, 0, "Número dos: la figura de Luffy con base, por menos de sesenta y cinco mil pesos.", {"luffy", "sesenta"}),
    ("p", 2, 1, "El pirata de goma que sueña con ser el Rey de los Piratas.", {"goma", "rey"}),
    NIVEL,
    ("p", 3, 0, "Número tres: la figura de Roronoa Zoro, por menos de cien mil pesos.", {"zoro", "cien"}),
    ("host", "El espadachín que pelea con tres espadas… una de ellas en la boca.", {"tres", "boca"}, 3),
    ("p", 4, 0, "Número cuatro: la taza tres de en forma de sombrero de paja, por menos de ciento veinte mil pesos.", {"taza", "ciento"}),
    ("p", 4, 1, "Y aquí va el dato: el manga de One Piece ya superó los seiscientos millones de copias. Tiene récord Guinness.", {"seiscientos", "guinness"}),
    VERDAD,
    ("p", 5, 0, "Número cinco: la figura de Shanks, por menos de ciento ochenta y cinco mil pesos.", {"shanks", "ciento"}),
    ("host", "Shanks fue quien le regaló a Luffy su famoso sombrero de paja. Sin él… no habría aventura.", {"sombrero", "aventura"}, 5),
    CIERRE_FB("One Piece")]
G["tt"] = [
    ("host", "¿Qué le regalas a un fan de One Piece esta Navidad? Cinco ideas, de menor a mayor precio.", {"navidad", "cinco"}),
    ("p", 1, 0, "Uno: la camiseta de Luffy en Gear cinco, menos de cincuenta y cinco mil.", {"gear", "cincuenta"}),
    ("host", "Dato: One Piece empezó en mil novecientos noventa y siete, creado por Eiichiro Oda.", {"oda"}, 1),
    ("p", 2, 0, "Dos: la figura de Luffy con base, menos de sesenta y cinco mil.", {"luffy", "sesenta"}),
    ("host", "El pirata de goma que sueña con ser el Rey de los Piratas.", {"rey"}, 2),
    ("p", 3, 0, "Tres: Roronoa Zoro, el de las tres espadas, menos de cien mil.", {"zoro", "cien"}),
    ("host", "Y sí: una de las espadas la sostiene con la boca.", {"boca"}, 3),
    ("p", 4, 0, "Cuatro: la taza tres de del sombrero de paja, menos de ciento veinte mil.", {"taza", "ciento"}),
    ("host", "El manga ya pasó los seiscientos millones de copias. ¡Récord Guinness!", {"seiscientos"}, 4),
    VERDAD_TT,
    ("p", 5, 0, "Cinco: Shanks, el que le regaló el sombrero a Luffy, menos de ciento ochenta y cinco mil.", {"shanks", "sombrero"}),
    ("host", "¿Cuál de los cinco escoges?", {"escoges"}, 5),
    TT_EXTRA,
    CIERRE_TT]
if __name__ == "__main__":
    correr(S, G, ((235, 45, 45), (255, 205, 50)), {"one": ("en", "One"), "piece": ("en", "Piece"), "luffy": ("es", "lufi"), "gear": ("en", "Gear"), "shonen": ("es", "shónen"),
           "jump": ("en", "Jump"), "eiichiro": ("es", "eiichiro"), "oda": ("es", "oda"), "roronoa": ("es", "roronoa"), "zoro": ("es", "zoro"),
           "guinness": ("en", "Guinness"), "shanks": ("en", "Shanks")})
