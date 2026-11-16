"""Versiones cortas de Psicosis: python3 c02_psicosis.py fb|tt [salida]"""
import sys
red = sys.argv.pop(1) if len(sys.argv) > 1 and sys.argv[1] in ("fb", "tt") else "fb"
from _base import *
import r02_psicosis as L
H, D = L.H, L.D
if red == "fb":
    lista = [
     (H[0][0], "Marion Crane, una secretaria de Phoenix, se roba cuarenta mil dólares de su jefe y huye para empezar una nueva vida con su novio.", {"marion", "dólares"}),
     (H[2][0], "En el camino, un policía la detiene y la mira con sospecha. Ella, asustada, cambia de carro para no dejar rastro y sigue manejando hasta que cae la noche.", {"policía"}),
     (H[4][0], "Una noche de tormenta, cansada y nerviosa, se detiene en un motel solitario al lado de la carretera: el Motel Bates.", {"bates"}),
     (H[6][0], "La atiende Norman, un joven tímido que vive con su madre en la casa de la colina. Una madre que le grita y lo controla.", {"norman", "madre"}),
     (H[7][0], "Cenan juntos entre aves disecadas. Y esa conversación hace que Marion decida volver al día siguiente y devolver el dinero.", {"devolver"}),
     (H[9][0], "Pero esa noche, en la ducha, una silueta aparece detrás de la cortina. Y la protagonista muere antes de la mitad de la película. En mil novecientos sesenta, nadie se atrevía a hacer eso.", {"silueta", "protagonista"}),
     ("H", "Un detective y luego la hermana de Marion siguen la pista hasta el motel. Y descubren algo imposible: la madre de Norman lleva diez años muerta.", {"muerta"}),
     (H[16][0], "En el sótano encuentran su cuerpo momificado. Y entonces aparece Norman, vestido con la ropa de su madre. Durante años, él se había convertido en ella.", {"norman", "ella"}),
     (D[3][0], "Dato: la escena de la ducha dura unos cuarenta y cinco segundos, pero tomó siete días de rodaje. Y la sangre era jarabe de chocolate.", {"siete", "chocolate"}),
     (D[1][0], "El estudio odiaba la historia y le dio a Hitchcock apenas ochocientos mil dólares. La película recaudó unos cincuenta millones.", {"ochocientos", "cincuenta"}),
    ]
    esc, g = resena_corta("En mil novecientos sesenta, una película hizo que medio mundo le tuviera miedo a la ducha. Esta es Psicosis, de Alfred Hitchcock.", lista, 5,
                          "Mi calificación: cinco de cinco. Una obra maestra que cambió el terror para siempre.")
else:
    lista = [
     (H[0][0], "Marion se roba cuarenta mil dólares y huye en su carro.", {"dólares"}),
     (H[4][0], "Una noche de tormenta llega al Motel Bates, donde la atiende Norman, un joven tímido que vive con su madre.", {"bates", "norman"}),
     (H[7][0], "Cenan juntos entre aves disecadas, y Norman le dice algo escalofriante: que todos enloquecemos un poco a veces.", {"enloquecemos"}),
     (H[9][0], "Esa noche, en la ducha, una silueta aparece detrás de la cortina. Y Marion, la protagonista, no sale con vida.", {"silueta"}),
     (H[16][0], "Su hermana investiga y descubre lo imposible: la madre de Norman lleva diez años muerta… y Norman se convirtió en ella.", {"muerta", "ella"}),
     (D[3][0], "Esa escena de la ducha tomó siete días de rodaje. Y la sangre era jarabe de chocolate.", {"chocolate"}),
     L.O[0],
    ]
    esc, g = resena_corta("Esta película mató a su protagonista a mitad de la historia… y el público enloqueció. Es Psicosis, de Alfred Hitchcock, de mil novecientos sesenta.", lista, 5, "Mi nota: cinco de cinco.",
                          cta="¿Te atreverías a verla? La reseña completa está en nuestro YouTube. Síguenos en Comics Store.")
if __name__ == "__main__": correr_corta(esc, g, "psicosis", L.PRON, red)
