"""Comics Store · Noticia: Loki y Steve Rogers (Avengers: Doomsday)"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
from noticia_imagen import armar
from motor import render
IMG = os.path.join(os.path.dirname(HERE), "noticias", "loki_steve.jpg")
PRON = {"steve": ("en", "Steve"), "avengers": ("es", "avényers"), "doomsday": ("es", "dúmsdei"), "tva": ("es", "te ve a"), "thor": ("es", "tor")}
L = [
 ((2.3, 1.0, (.62, .5), (.5, .5)), "¡Loki trajo a Steve Rogers al universo de los Cuatro Fantásticos!", {"loki", "steve", "fantásticos"}),
 ((1.1, 2.2, (.55, .3), (.62, .16)), "Según las filtraciones, en el primer acto de Avengers: Doomsday, Loki descubre que Steve está en un tiempo en el que no debería estar.", {"filtraciones", "doomsday"}),
 ((2.3, 1.5, (.4, .83), (.42, .82)), "Pero al ver que Steve ya tiene una familia, decide no borrarlo… y lo lleva a otro universo, para que pueda hacer su vida ahí sin problemas.", {"familia", "universo"}),
 ((1.3, 2.4, (.55, .5), (.6, .5)), "Al final, Loki le da su tarjeta de la TVA, para que lo llame si alguna vez lo necesita.", {"tarjeta"}),
 ((2.3, 1.6, (.6, .16), (.58, .2)), "Steve mira a un Loki cambiado, y sonríe por el hombre en el que se convirtió.", {"cambiado"}),
 ((1.4, 2.3, (.45, .82), (.4, .83)), "Y le dice algo que nos rompió el corazón: que Thor estaría orgulloso de él.", {"thor", "orgulloso"}),
]
esc, cierre = armar(IMG, L, pregunta="¿TE EMOCIONÓ?")
esc.append((cierre, "¿Te emociona el regreso de Steve? Comenta y síguenos en Comics Store.", {"steve"}))
if __name__ == "__main__":
    render(esc, sys.argv[1] if len(sys.argv) > 1 else "/home/claude/noticia_loki_steve.mp4", musica="alegre", pron=PRON, estilo="neon", y_sub=330)
