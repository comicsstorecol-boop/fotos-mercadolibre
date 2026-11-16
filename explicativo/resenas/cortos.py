"""Versiones cortas de las reseñas. Uso: python3 cortos.py <peli> fb|tt [salida]
fb = Facebook/Instagram (~2 min) · tt = TikTok (60-90 s)"""
import sys, importlib
peli, red = sys.argv[1], sys.argv[2]; out = sys.argv[3] if len(sys.argv) > 3 else f"/home/claude/{red}_{peli}.mp4"
sys.argv = [sys.argv[0]]
from _base import *
MOD = {"resplandor": "r03_resplandor", "alien": "r04_alien", "halloween": "r05_halloween", "hereditary": "r06_hereditary", "noche_muertos": "r07_noche_muertos",
       "bruja_blair": "r08_bruja_blair", "conjuro": "r09_conjuro", "dejame_salir": "r10_dejame_salir", "pesadilla_elm": "r11_pesadilla_elm"}
L = importlib.import_module(MOD[peli]); H = lambda i: L.H[i][0]; D = lambda i: L.D[i][0]
NOTA = {"resplandor": 4.5, "alien": 5, "halloween": 4.5, "hereditary": 4.5, "noche_muertos": 4.5, "bruja_blair": 4, "conjuro": 4, "dejame_salir": 4.5, "pesadilla_elm": 4.5}[peli]
NTXT = {5: "cinco de cinco", 4.5: "cuatro punto cinco de cinco", 4: "cuatro de cinco"}[NOTA]
V = {}
V["resplandor"] = lambda: dict(
 fb_g="Un hotel aislado por la nieve, un escritor sin inspiración… y un hotel que lo quiere para siempre. Esta es El resplandor, de Stanley Kubrick.",
 fb=[(H(0), "Jack Torrance acepta cuidar el hotel Overlook, en las montañas de Colorado, durante todo el invierno. Lleva a su esposa Wendy y a su hijo Danny.", {"overlook"}),
     (H(1), "En la entrevista le cuentan que un cuidador anterior enloqueció por el aislamiento y le hizo daño a su familia. Jack se ríe.", {"enloqueció"}),
     (H(4), "Danny tiene un don, el resplandor: ve cosas del pasado y del futuro. El cocinero le advierte que nunca entre a la habitación doscientos treinta y siete.", {"resplandor"}),
     (H(6), "Pasan las semanas. Jack no logra escribir, y Danny recorre en triciclo los pasillos infinitos, donde empieza a ver cosas que no deberían estar ahí.", {"triciclo"}),
     (H(9), "Jack conoce en un salón de fiesta al fantasma del antiguo cuidador, que le dice que su familia necesita ser corregida.", {"corregida"}),
     (H(10), "Wendy revisa la novela de Jack: cientos de páginas con una sola frase repetida miles de veces.", {"frase"}),
     ("H", "Jack, poseído por el hotel, persigue a su familia con un hacha. Danny escapa al laberinto de arbustos del jardín, borra sus huellas… y Jack muere congelado.", {"laberinto"}),
     (H(17), "Y la imagen final: una foto de una fiesta en el hotel en mil novecientos veintiuno. En el centro, sonriendo… está Jack.", {"foto"}),
     (D(0), "Dato: Stephen King, el autor del libro, nunca quedó contento con esta versión de su historia.", {"king"})],
 tt_g="El autor de esta historia odió la película… y aun así es una de las más aterradoras de la historia. Es El resplandor, de Kubrick.",
 tt=[(H(0), "Jack y su familia cuidan un hotel vacío en las montañas durante todo el invierno.", {"hotel"}),
     (H(9), "Pero el hotel tiene fantasmas, y uno le dice a Jack que su familia debe ser corregida.", {"fantasmas"}),
     (H(10), "Su esposa descubre que en meses Jack solo escribió una frase, repetida miles de veces.", {"frase"}),
     ("H", "Jack los persigue con un hacha. Su hijo escapa por un laberinto nevado, y Jack muere congelado. Al final, aparece en una foto del hotel… de mil novecientos veintiuno.", {"foto"})])
V["alien"] = lambda: dict(
 fb_g="Siete tripulantes, una nave en medio del espacio… y algo que no debería estar a bordo. Esta es Alien, el octavo pasajero.",
 fb=[(H(0), "La nave de carga Nostromo regresa a la Tierra con siete tripulantes dormidos. Pero la computadora los despierta: detectó una señal desconocida.", {"nostromo", "señal"}),
     (H(3), "Bajan a un planeta oscuro y encuentran una nave gigantesca, abandonada, que no fue construida por humanos.", {"nave"}),
     (H(4), "Kane encuentra una cámara llena de huevos. Uno se abre… y algo salta directo a su cara.", {"huevos"}),
     ("H", "Días después Kane parece estar bien. Pero en plena cena, una criatura sale de su pecho y escapa por los pasillos. Ahora hay un octavo pasajero.", {"octavo"}),
     (H(10), "Ripley descubre que la compañía sabía todo: la orden era llevar la criatura a la Tierra. La tripulación era prescindible.", {"prescindible"}),
     (H(11), "Y Ash, el científico, resulta ser un androide puesto ahí para cumplir esa misión.", {"androide"}),
     (H(15), "Uno por uno caen todos. Ripley hace explotar la nave, escapa con el gato… y descubre que la criatura viene con ella. La expulsa al vacío.", {"vacío"}),
     (D(1), "Dato: el diseño de la criatura es del artista suizo H. R. Giger. Y la película ganó el Óscar a mejores efectos visuales.", {"giger", "óscar"})],
 tt_g="En mil novecientos setenta y nueve, una escena de cena dejó a medio mundo traumado. Esta es Alien.",
 tt=[(H(0), "Siete tripulantes despiertan en el espacio por una señal desconocida.", {"señal"}),
     (H(4), "En un planeta oscuro, algo sale de un huevo y se pega a la cara de uno de ellos.", {"huevo"}),
     ("H", "Días después, en plena cena, una criatura sale de su pecho. Y empieza la cacería dentro de la nave.", {"cena"}),
     (H(15), "Ripley es la única que sobrevive, junto al gato, y expulsa a la criatura al vacío del espacio.", {"ripley"})])
V["halloween"] = lambda: dict(
 fb_g="Con trescientos mil dólares y una máscara de dos dólares, crearon al asesino más famoso del cine. Esta es Halloween, de John Carpenter.",
 fb=[(H(1), "Noche de Halloween de mil novecientos sesenta y tres: un niño de seis años, Michael Myers, ataca a su hermana mayor. Lo internan en un sanatorio.", {"michael"}),
     (H(3), "Quince años después, la noche antes de Halloween, Michael escapa. Su psiquiatra, el doctor Loomis, sabe que va de regreso a casa.", {"escapa", "loomis"}),
     (H(6), "En el pueblo, una figura con máscara blanca empieza a seguir a Laurie, una estudiante tímida. Aparece… y desaparece.", {"máscara", "laurie"}),
     (H(10), "La noche de Halloween, Laurie cuida niños. Sus amigas hacen lo mismo en la casa del frente.", {"halloween"}),
     ("H", "Uno por uno, Michael ataca a sus amigas en silencio. Cuando Laurie va a buscarlas, él la está esperando.", {"silencio"}),
     (H(14), "Laurie se defiende con lo que encuentra y lo derriba varias veces. Pero Michael siempre se vuelve a levantar.", {"levantar"}),
     (H(17), "Loomis le dispara y Michael cae por el balcón. Pero cuando se asoma… el jardín está vacío.", {"vacío"}),
     (D(2), "Dato: la máscara de Michael era una máscara barata del capitán Kirk de Star Trek, pintada de blanco.", {"kirk"})],
 tt_g="El villano más famoso del terror usa una máscara que costó menos de dos dólares. Esta es Halloween.",
 tt=[(H(1), "Un niño de seis años ataca a su hermana la noche de Halloween. Lo encierran quince años.", {"niño"}),
     (H(3), "Escapa, y vuelve a su pueblo justo para otra noche de Halloween.", {"escapa"}),
     (H(6), "Una figura con máscara blanca empieza a seguir a Laurie… y a sus amigas.", {"máscara"}),
     ("H", "Laurie lucha toda la noche. Le disparan seis veces, cae del balcón… y el cuerpo desaparece.", {"desaparece"})])
V["hereditary"] = lambda: dict(
 fb_g="La llaman la película más perturbadora del siglo veintiuno. Esta es El legado del diablo, o Hereditary, de Ari Aster.",
 fb=[(H(0), "Muere Ellen, la abuela de la familia Graham: una mujer reservada y llena de secretos.", {"ellen"}),
     (H(1), "Su hija Annie construye casas en miniatura y vive con su esposo y sus hijos, Peter y Charlie, una niña extraña que chasquea la lengua.", {"annie", "charlie"}),
     (H(5), "Una noche, en un viaje urgente al hospital, ocurre un accidente terrible en la carretera. Charlie no sobrevive. Y apenas van treinta minutos de película.", {"accidente"}),
     (H(8), "La familia se rompe por la culpa y el dolor. Una amiga del grupo de apoyo le enseña a Annie un ritual para hablar con los muertos.", {"ritual"}),
     (H(11), "Y funciona demasiado bien. Annie descubre que su madre lideraba una secta que adoraba a Paimon, un rey del infierno.", {"paimon"}),
     ("H", "Todo era un plan: Paimon necesitaba el cuerpo de un joven. El verdadero objetivo siempre fue Peter.", {"peter"}),
     (H(16), "Al final, Peter despierta en una casa del árbol rodeado de la secta. Le ponen una corona. Ya no es él.", {"corona"}),
     (D(4), "Costó unos diez millones de dólares y recaudó más de ochenta. Muchos críticos la compararon con El exorcista.", {"exorcista"})],
 tt_g="Lo que pasa a los treinta minutos de esta película dejó a medio cine en silencio. Es El legado del diablo.",
 tt=[(H(1), "Después de la muerte de la abuela, la familia Graham empieza a vivir cosas extrañas.", {"abuela"}),
     (H(5), "Una noche, un accidente en la carretera destruye a la familia para siempre.", {"accidente"}),
     (H(11), "La madre descubre que la abuela lideraba una secta que adoraba a un rey del infierno.", {"secta"}),
     ("H", "Y que todo, desde el principio, era un plan para entregarle a ese demonio el cuerpo de su hijo.", {"hijo"})])
V["noche_muertos"] = lambda: dict(
 fb_g="Esta película inventó a los zombis modernos… y no tiene dueño. Es La noche de los muertos vivientes, de George A. Romero.",
 fb=[(H(2), "En un cementerio, un hombre ataca a Barbra y a su hermano. Ella escapa y se esconde en una granja abandonada.", {"cementerio"}),
     (H(4), "Llega Ben, que toma el control y tapa las ventanas con tablas. En mil novecientos sesenta y ocho, el héroe era un hombre negro: algo casi nunca visto.", {"ben"}),
     (H(6), "Por la radio escuchan que, en todo el país, los muertos se están levantando y atacando a los vivos.", {"radio"}),
     (H(8), "En el sótano hay más sobrevivientes. Y empiezan las peleas entre ellos, mientras afuera los muertos se multiplican.", {"peleas"}),
     (H(11), "Los muertos entran a la casa. Todos van cayendo, hasta que solo queda Ben, encerrado en el sótano.", {"sótano"}),
     ("H", "Al amanecer, un grupo armado recorre el campo. Ben se asoma aliviado… y lo confunden con un muerto. El único sobreviviente muere por error.", {"error"}),
     (D(0), "Costó apenas ciento catorce mil dólares y recaudó unos treinta millones.", {"ciento"}),
     (D(4) if False else "H", "Y por un error al cambiarle el título, no tiene aviso de derechos de autor. Por eso está en dominio público y cualquiera puede verla gratis.", {"dominio"})],
 tt_g="El héroe sobrevive toda la noche a los muertos… y lo mata un humano. Así termina La noche de los muertos vivientes.",
 tt=[(H(3), "Una mujer escapa de un cementerio y se esconde en una granja.", {"granja"}),
     (H(6), "La radio confirma lo imposible: los muertos se están levantando.", {"muertos"}),
     (H(11), "Los sobrevivientes pelean entre ellos y van cayendo uno por uno.", {"pelean"}),
     ("H", "Solo Ben sobrevive la noche. Al amanecer, lo confunden con un muerto… y le disparan.", {"disparan"})])
V["bruja_blair"] = lambda: dict(
 fb_g="Tres estudiantes entraron a un bosque a grabar un documental. Solo encontraron sus cámaras. Esta es El proyecto de la bruja de Blair.",
 fb=[(H(1), "Heather, Josh y Mike llegan a un pueblo de Maryland para filmar un documental sobre la leyenda de la bruja de Blair.", {"bruja"}),
     (H(3), "Les cuentan la historia de un ermitaño que se llevó niños al bosque, y siempre ponía a uno de ellos de cara a la pared.", {"pared"}),
     (H(6), "Se internan en el bosque y se pierden. Descubren que el mapa ya no existe: Mike lo tiró al río.", {"mapa"}),
     (H(8), "Las noches empeoran: risas de niños, pasos, y algo que sacude la carpa. Por las mañanas aparecen figuras de ramas colgando de los árboles.", {"carpa"}),
     (H(10), "Una mañana, Josh desaparece. De noche solo escuchan sus gritos a lo lejos.", {"josh"}),
     (H(13), "Siguiendo los gritos, encuentran una casa abandonada. En el sótano, Mike está parado en una esquina… de cara a la pared.", {"esquina"}),
     ("H", "La cámara cae. La imagen se corta. Y nunca vemos qué los atacó.", {"nunca"}),
     (D(1), "Los actores pasaron ocho días solos en el bosque, improvisando todo. Costó unos sesenta mil dólares y recaudó doscientos cuarenta y ocho millones.", {"ocho", "sesenta"})],
 tt_g="Al estrenarse, mucha gente creyó que estos tres actores estaban realmente desaparecidos. Es La bruja de Blair.",
 tt=[(H(4), "Tres estudiantes se meten a un bosque a grabar un documental sobre una bruja.", {"bosque"}),
     (H(6), "Se pierden, y el mapa desaparece.", {"mapa"}),
     (H(10), "De noche algo sacude la carpa, y uno de ellos desaparece.", {"desaparece"}),
     ("H", "Al final, en una casa abandonada, uno está de cara a la pared… y la cámara cae. Nunca vemos qué los atacó.", {"pared"})])
V["conjuro"] = lambda: dict(
 fb_g="Una granja, cinco hijas… y alguien más aplaudiendo en la oscuridad. Esta es El conjuro, de James Wan.",
 fb=[(H(0), "En mil novecientos setenta y uno, la familia Perron se muda a una vieja granja en Rhode Island.", {"perron"}),
     (H(2), "El perro aparece muerto, y todos los relojes se detienen a las tres y siete de la mañana.", {"relojes"}),
     (H(5), "Carolyn, la mamá, escucha aplausos en el sótano. Baja con un fósforo… y unas manos aplauden a su lado, en la oscuridad.", {"aplausos"}),
     (H(7), "Llaman a Ed y Lorraine Warren, investigadores paranormales reales: él demonólogo, ella clarividente.", {"warren"}),
     (H(8), "Descubren que en esa tierra vivió una mujer acusada de brujería, que maldijo a todo el que la habitara.", {"maldijo"}),
     ("H", "La entidad posee a Carolyn y la empuja a atacar a sus propias hijas. Ed tiene que hacer el exorcismo él mismo.", {"exorcismo"}),
     (H(13), "Lorraine le pide a Carolyn que recuerde un día feliz con su familia… y ese recuerdo la salva.", {"recuerdo"}),
     (D(3), "Dato: la clasificaron para mayores de diecisiete años sin sangre ni groserías. Solo porque daba demasiado miedo.", {"miedo"})],
 tt_g="Esta película la clasificaron solo para adultos… sin sangre, sin groserías. Solo porque daba demasiado miedo.",
 tt=[(H(0), "Una familia se muda a una granja vieja con sus cinco hijas.", {"granja"}),
     (H(2), "Los relojes se detienen a las tres y siete de la mañana, cada noche.", {"relojes"}),
     (H(5), "Y en el sótano oscuro, unas manos aplauden junto a la mamá.", {"aplauden"}),
     ("H", "Los Warren, investigadores reales, descubren que la casa está maldita… y que la entidad quiere a la madre.", {"warren"})])
V["dejame_salir"] = lambda: dict(
 fb_g="Conocer a los suegros nunca fue tan aterrador. Esta es Déjame salir, de Jordan Peele, la película de terror que ganó un Óscar.",
 fb=[(H(1), "Chris, un fotógrafo, viaja a conocer a los papás de su novia Rose. Ella le asegura que no son racistas.", {"chris", "rose"}),
     (H(4), "La familia Armitage es amable… quizá demasiado. La mamá es psiquiatra y practica la hipnosis.", {"hipnosis"}),
     (H(5), "Los empleados de la casa sonríen todo el tiempo, pero parecen a punto de llorar.", {"empleados"}),
     (H(6), "Una noche, la mamá revuelve una taza de té… y lo hipnotiza sin permiso.", {"taza"}),
     (H(7), "Chris cae en el lugar hundido: un vacío donde ve todo, pero no controla su cuerpo.", {"hundido"}),
     (H(12), "Descubre fotos de Rose con muchas otras parejas. Ella era parte del plan.", {"plan"}),
     ("H", "La verdad: la familia subasta cuerpos de jóvenes negros, y con una cirugía, el cerebro de un comprador blanco ocupa su cuerpo. Chris escapa justo a tiempo, y lo rescata su mejor amigo.", {"subasta"}),
     (D(4), "Costó cuatro millones y medio de dólares, recaudó doscientos cincuenta y cinco millones, y Jordan Peele ganó el Óscar a mejor guion original.", {"óscar"})],
 tt_g="Una cuchara, una taza de té… y te quedas atrapado dentro de tu propio cuerpo. Esto es Déjame salir.",
 tt=[(H(1), "Chris va a conocer a la familia de su novia.", {"familia"}),
     (H(6), "La suegra lo hipnotiza revolviendo una taza de té.", {"hipnotiza"}),
     (H(7), "Y cae en un vacío donde ve todo, pero no puede moverse.", {"vacío"}),
     ("H", "La familia roba cuerpos para meter dentro a otras personas. Y Chris era el siguiente.", {"cuerpos"})])
V["pesadilla_elm"] = lambda: dict(
 fb_g="Puedes escapar de un asesino… pero no puedes dejar de dormir para siempre. Esta es Pesadilla en la calle Elm, de Wes Craven.",
 fb=[(H(0), "Tina sueña con un hombre quemado, con sombrero y cuchillas en los dedos. Despierta… y su pijama está rasgado.", {"tina"}),
     (H(2), "Su amiga Nancy descubre que ella y otros chicos tienen la misma pesadilla.", {"nancy"}),
     (H(3), "Esa noche, Tina muere dormida en su cama. Y luego su novio, en su celda. El asesino ataca en los sueños.", {"sueños"}),
     (H(6), "Nancy decide no dormir, y el hombre le dice su nombre en sueños: Freddy.", {"freddy"}),
     (H(9), "Su mamá le confiesa que Freddy era un criminal del barrio, y que los padres le prendieron fuego. Ahora se venga en los hijos.", {"fuego"}),
     ("H", "Freddy alcanza a Glen, el novio de Nancy, interpretado por un desconocido Johnny Depp en su primera película.", {"depp"}),
     (H(15), "Nancy saca a Freddy de su sueño, lo enfrenta y le da la espalda. Le quita el poder que le da su miedo.", {"miedo"}),
     (D(0), "Wes Craven se inspiró en noticias reales de personas que tenían pesadillas terribles… y murieron durmiendo.", {"reales"})],
 tt_g="Esta película está inspirada en personas reales que murieron… mientras soñaban. Es Pesadilla en la calle Elm.",
 tt=[(H(0), "Varios chicos del barrio sueñan con el mismo hombre quemado.", {"sueñan"}),
     (H(3), "Y si él te atrapa en el sueño, mueres en la vida real.", {"mueres"}),
     (H(6), "Nancy decide no volver a dormir, mientras descubre quién es: Freddy Krueger.", {"freddy"}),
     ("H", "Al final lo vence quitándole lo único que le da poder: su miedo.", {"miedo"})])

EXTRA = {
 "resplandor": lambda: dict(
  fb=[(H(11), "Wendy logra encerrar a Jack en la despensa, pero alguien desde afuera le abre la puerta. El hotel lo está ayudando.", {"despensa"})],
  tt=[(H(2), "Su hijo Danny tiene un don: ve cosas que pasaron y que van a pasar. Y el hotel está lleno de ellas.", {"don"}),
      (H(6), "Mientras Danny recorre los pasillos en triciclo, Jack se vuelve cada vez más irritable.", {"triciclo"})]),
 "alien": lambda: dict(
  fb=[(H(6), "La criatura está pegada a la cara de Kane, y no pueden quitársela: su sangre es un ácido que perfora el metal.", {"ácido"}),
      (H(9), "El octavo pasajero crece muy rápido y empieza a cazarlos en los ductos de ventilación.", {"ductos"})],
  tt=[(H(10), "Y la compañía lo sabía todo: la tripulación era prescindible.", {"prescindible"}),
      (H(11), "Hasta el científico de la nave resulta ser un androide.", {"androide"}),
      (D(1), "El diseño de la criatura es del artista suizo H. R. Giger, y ganó el Óscar a mejores efectos visuales.", {"giger"})]),
 "halloween": lambda: dict(
  fb=[(H(7), "Loomis llega al pueblo y descubre que la lápida de la hermana de Michael desapareció. Ya no hay duda: Michael volvió.", {"lápida"}),
      (H(11), "El niño que cuida Laurie le dice que vio al hombre del saco en la casa del frente. Ella no le cree. Pero tiene razón.", {"saco"}),
      (D(1), "La grabaron en unas tres semanas con trescientos mil dólares, y recaudó unos setenta millones.", {"setenta"})],
  tt=[(H(4), "Su psiquiatra está convencido de que detrás de esos ojos no hay nada humano.", {"humano"}),
      (D(2), "Dato: su máscara era una máscara barata del capitán Kirk de Star Trek, pintada de blanco.", {"kirk"}),
      (D(1), "Costó trescientos mil dólares y recaudó setenta millones.", {"setenta"})]),
 "hereditary": lambda: dict(
  fb=[(H(7), "Peter, en shock, llega a casa y no dice nada. Es su madre quien descubre lo ocurrido a la mañana siguiente.", {"shock"}),
      (H(14), "Annie intenta romper el vínculo con fuego, pero el ritual se vuelve contra ella: Steve muere y Annie queda poseída.", {"fuego"}),
      (D(3), "Dato: Paimon no es un invento. Aparece en antiguos libros de demonología como uno de los reyes del infierno.", {"paimon"})],
  tt=[(H(2), "La hija menor, Charlie, era la favorita de la abuela, y tiene una costumbre inquietante: chasquea la lengua.", {"charlie"}),
      (H(16), "Al final, el hijo despierta rodeado de la secta, y le ponen una corona. Ya no es él.", {"corona"})]),
 "noche_muertos": lambda: dict(
  fb=[(H(9), "Intentan escapar en una camioneta para cargar gasolina, pero hay un incendio y la pareja más joven no regresa.", {"incendio"}),
      (H(12), "Barbra ve entre la multitud a su propio hermano, ya convertido. Él la arrastra hacia afuera.", {"hermano"}),
      (D(1), "Dato: en toda la película nunca se dice la palabra zombi. Pero aquí nació el zombi moderno.", {"zombi"})],
  tt=[(H(4), "Llega Ben, un hombre que tapa las ventanas con tablas. En mil novecientos sesenta y ocho, un héroe negro era casi revolucionario.", {"ben"}),
      (H(12), "Los muertos entran a la casa, y hasta Barbra cae ante su propio hermano, ya convertido.", {"hermano"}),
      (D(0), "Costó apenas ciento catorce mil dólares, y hoy cualquiera la puede ver gratis: está en dominio público.", {"gratis"})]),
 "bruja_blair": lambda: dict(
  fb=[(H(5), "Encuentran un pequeño cementerio de piedras en el bosque, y Josh tumba uno sin querer. Desde esa noche, todo empeora.", {"piedras"}),
      (H(11), "La escena más famosa: Heather, con la linterna en la cara, llora y pide perdón a las familias, porque siente que todo es su culpa.", {"perdón"}),
      (D(4), "Su publicidad presentó a los actores como desaparecidos. Mucha gente creyó que era real.", {"real"})],
  tt=[(H(3), "Les cuentan de un ermitaño que se llevaba niños al bosque, y siempre dejaba a uno de cara a la pared.", {"pared"}),
      (D(1), "Los actores pasaron ocho días solos en el bosque improvisando todo. Y gran parte del miedo era real.", {"real"}),
      (D(6), "Costó unos sesenta mil dólares y recaudó doscientos cuarenta y ocho millones.", {"sesenta"})]),
 "conjuro": lambda: dict(
  fb=[(H(3), "Las niñas juegan a esconderse con los ojos vendados, siguiendo aplausos. Pero un día, alguien que no es de la familia empieza a aplaudir también.", {"aplaudir"}),
      (H(4), "Una de las hijas encuentra una caja musical con un espejo, y dice que en el reflejo ve a un niño.", {"caja"}),
      (D(2), "La granja real todavía existe, y sus dueños actuales dicen que la actividad nunca terminó.", {"existe"}),
      (D(5), "Costó veinte millones de dólares y recaudó más de trescientos diecinueve.", {"veinte"})],
  tt=[(H(7), "Ed es demonólogo. Lorraine puede ver lo que los demás no.", {"lorraine"}),
      (H(12), "La entidad posee a la mamá y la empuja contra sus propias hijas.", {"posee"}),
      (D(2), "Y lo más inquietante: la casa real todavía existe.", {"existe"})]),
 "dejame_salir": lambda: dict(
  fb=[(H(3), "En el camino atropellan a un venado, y Chris se queda extrañamente afectado mirando al animal herido.", {"venado"}),
      (H(10), "En una fiesta, el único invitado negro parece otra persona. Con el flash de una foto, despierta un segundo y le grita a Chris que se vaya.", {"flash"}),
      (H(14), "Atado en el sótano, Chris se tapa los oídos con algodón para no escuchar la cuchara, y logra escapar.", {"algodón"})],
  tt=[(H(5), "Los empleados de la casa sonríen todo el tiempo… pero parecen a punto de llorar.", {"sonríen"}),
      (H(10), "En una fiesta, otro invitado despierta un segundo con el flash de una foto, y le grita que se vaya.", {"flash"}),
      (D(4), "Costó cuatro millones y medio, recaudó doscientos cincuenta y cinco millones, y ganó el Óscar a mejor guion.", {"óscar"})]),
 "pesadilla_elm": lambda: dict(
  fb=[(H(7), "En una clínica del sueño, Nancy lucha con Freddy y despierta con su sombrero en las manos. Lo sacó del sueño.", {"sombrero"}),
      (H(13), "Nancy arma un plan: llena la casa de trampas y se duerme a propósito para atrapar a Freddy y traerlo al mundo real.", {"trampas"}),
      (D(2), "Costó cerca de un millón de dólares y recaudó unos cincuenta y siete millones.", {"millón"})],
  tt=[(H(9), "Su mamá le confiesa la verdad: los padres del barrio le prendieron fuego a ese hombre años atrás. Ahora se venga en los sueños de sus hijos.", {"fuego"}),
      (H(11), "Su novio, interpretado por un Johnny Depp de veintiún años en su primera película, se queda dormido… y no despierta.", {"depp"})]),
}
v = V[peli]()
x = EXTRA[peli]()
v["fb"] = v["fb"][:-1] + x["fb"] + v["fb"][-1:] + [L.O[0], L.O[1]]
v["tt"] = v["tt"][:-1] + x["tt"] + v["tt"][-1:] + [L.O[0]]
if red == "fb":
    esc, g = resena_corta(v["fb_g"], v["fb"], NOTA, f"Mi calificación: {NTXT}.")
else:
    esc, g = resena_corta(v["tt_g"], v["tt"], NOTA, f"Mi nota: {NTXT}.",
                          cta="¿La has visto? La reseña completa está en nuestro YouTube. Síguenos en Comics Store.")
if __name__ == "__main__": correr_corta(esc, g, peli, L.PRON, red) if False else render(esc, out, musica="terror", pron=L.PRON, estilo="neon", y_sub=330, regancho_idx=g)
