"""Regalos: fans de Chainsaw Man. python3 rg18_chainsaw_man.py fb|tt salida.mp4"""
from _tema import *
S = "chainsaw_man"
G = {"productos": [
    dict(img=img(S, 1), nombre="CAMISETA POCHITA", precio="$54.999", nota="EL PERRO MOTOSIERRA"),
    dict(img=img(S, 2), nombre="CAMISETA CHAINSAW MAN II", precio="$54.999", nota="DESDE 2018"),
    dict(img=img(S, 3), nombre="PELUCHE CHAINSAW MAN", precio="$74.999", nota="TIERNO… Y CON SIERRAS"),
    dict(img=img(S, 4), nombre="FIGURA CHAINSAW MAN", precio="$99.999", nota="¡INCLUYE A POCHITA!"),
    dict(img=img(S, 5), nombre="FIGURA CHAINSAW MAN II", precio="$99.999", nota="ARCO DE REZE · 2025")]}
G["fb"] = [
    ("host", "¿Tienes un fan de Chainsaw Man en tu vida y no sabes qué regalarle esta Navidad? Aquí van cinco ideas de Comics Store.", {"navidad", "chainsaw"}),
    ("host", "Y quédate, porque hay un peluche tierno… con motosierras.", {"peluche", "motosierras"}),
    ("p", 1, 0, "Número uno: la camiseta de Pochita, por menos de cincuenta y cinco mil pesos.", {"pochita", "cincuenta"}),
    ("host", "Pochita es el demonio perro motosierra que se une a Denji… y le da su corazón para convertirlo en Chainsaw Man.", {"perro", "corazón"}, 1),
    ("p", 2, 0, "Número dos: la camiseta Chainsaw Man dos, también por menos de cincuenta y cinco mil pesos.", {"camiseta", "cincuenta"}),
    ("p", 2, 1, "El manga de Tatsuki Fujimoto empezó en diciembre de dos mil dieciocho, en la Shonen Jump.", {"fujimoto", "dieciocho"}),
    NIVEL,
    ("p", 3, 0, "Número tres: el peluche de Chainsaw Man, por menos de setenta y cinco mil pesos.", {"peluche", "setenta"}),
    ("host", "Suave para abrazar… pero con motosierras en los brazos. Así es este anime.", {"abrazar", "motosierras"}, 3),
    ("p", 4, 0, "Número cuatro: la figura de Chainsaw Man con Pochita, por menos de cien mil pesos.", {"figura", "cien"}),
    ("p", 4, 1, "Y aquí va el dato: la película del Arco de Reze superó los diez mil millones de yenes solo en Japón.", {"reze", "millones"}),
    VERDAD,
    ("p", 5, 0, "Número cinco: la figura Chainsaw Man dos, también por menos de cien mil pesos.", {"figura", "cien"}),
    ("host", "Y en Estados Unidos fue el primer anime en quedar número uno en taquilla dos fines de semana seguidos.", {"número", "seguidos"}, 5),
    CIERRE_FB("Chainsaw Man")]
G["tt"] = [
    ("host", "¿Qué le regalas a un fan de Chainsaw Man esta Navidad? Cinco ideas, de menor a mayor precio.", {"navidad", "cinco"}),
    ("p", 1, 0, "Uno: la camiseta de Pochita, menos de cincuenta y cinco mil.", {"pochita", "cincuenta"}),
    ("host", "El demonio perro motosierra que le dio su corazón a Denji.", {"corazón"}, 1),
    ("p", 2, 0, "Dos: la camiseta Chainsaw Man dos, menos de cincuenta y cinco mil.", {"camiseta", "cincuenta"}),
    ("host", "Dato: el manga de Tatsuki Fujimoto empezó en dos mil dieciocho.", {"fujimoto"}, 2),
    ("p", 3, 0, "Tres: el peluche de Chainsaw Man, menos de setenta y cinco mil. Tierno… con motosierras.", {"peluche", "motosierras"}),
    ("p", 4, 0, "Cuatro: la figura con Pochita, menos de cien mil.", {"figura", "pochita"}),
    ("host", "La película del Arco de Reze superó los diez mil millones de yenes en Japón.", {"reze"}, 4),
    VERDAD_TT,
    ("p", 5, 0, "Cinco: la figura Chainsaw Man dos, menos de cien mil.", {"figura", "cien"}),
    ("host", "¿Cuál de los cinco escoges?", {"escoges"}, 5),
    TT_EXTRA,
    CIERRE_TT]
if __name__ == "__main__":
    correr(S, G, ((255, 120, 20), (230, 30, 40)), {"chainsaw": ("en", "Chainsaw"), "man": ("en", "Man"), "pochita": ("es", "pochita"), "denji": ("es", "denyi"),
           "tatsuki": ("es", "tatsuki"), "fujimoto": ("es", "fuyimoto"), "shonen": ("es", "shónen"), "jump": ("en", "Jump"), "reze": ("es", "reze")})
