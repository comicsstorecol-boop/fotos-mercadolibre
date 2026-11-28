# Fábrica de videos (rama `video-guerra-de-peludos`)

Objetivo: Fernando da un TEMA → salen 3 videos listos para publicar:
- **YouTube**: 5–10 min, horizontal 1920x1080 nativo (`FORMATO=horizontal`)
- **Facebook/Instagram**: ~2 min, vertical
- **TikTok**: 60–90 s, vertical

## Estructura
| Carpeta | Qué hay |
|---|---|
| `fabrica.py` | Orquestador: `python3 fabrica.py temas/<slug>.py` genera las 3 versiones en `/home/claude/salidas/<slug>/` y anota en `catalogo.json` |
| `temas/` | Un archivo por video: textos, pronunciación, colores del tema y versiones cortas |
| `biblioteca/fondos/h` y `/v` | Fondos generados por Fernando (ChatGPT), horizontales y verticales (ver `biblioteca/README.md`) |
| `marcas/<pagina>/` | Logo, colores, narrador y presentador (`marcas/comics-store/intros/`) |
| `explicativo/` | Motor: `motor.py` (voz, música, karaoke, render), `compositor.py` (escenas), `resena.py` (plantilla de reseñas, presentador animado, versiones cortas) |
| `voz_fernando.enc` | Voz de Fernando cifrada (se descifra con setup.sh) |
| `generador.py` | Videos estilo plantilla (datos/tops/pronósticos) |

## Reglas fijas
- Reseña: intro presentador → portada → spoilers → Cap. 1 Historia → Cap. 2 Detrás de cámaras → Cap. 3 Opinión → calificación → cierre. Ganchos en 4 puntos.
- Cortas: gancho en 2–3 s, sin capítulos, cierre "reseña completa en nuestro YouTube".
- Colores de subtítulos según el tema (`COLORES` en el archivo del tema).
- Nunca dibujar personajes con derechos; nada de imágenes de películas.
- Nombres en inglés → `PRON` con fonemas en inglés.
- Renders largos: lanzar con nohup y vigilar con sleep (solo avanzan mientras hay herramientas corriendo).

## Reglas de calidad (aprobadas 17-nov-2026)
- Sobre fondos de foto NO se dibujan objetos ni siluetas de código (se ignoran solos). Las personas salen en las escenas clave que genera Fernando (Pnn por película).
- Datos y cifras van como etiqueta (`tag`), no como dibujo.
- El primer plano del presentador también mueve la boca con la voz (`boca=(x, labio, ancho/2, mentón, apertura)`).

## Línea gamer (videojuegos, cartoons, superhéroes, productos gamer) — nov 2026
- Narrador: el mismo encapuchado, en set neón: marcas/comics-store/intros/gamer_narrador_h.png y _v.png (ya mejorados x2).
- Las figuras del fondo son mercancía real de Fernando, solo decoración: no animarlas, no nombrarlas, no ponerlas al frente en miniaturas.
- Falta: coordenadas de cabeza/boca para animarlo (como Anfitrion de terror) y sus escenarios.
- GTA VI y demás juegos: sin capturas, logos ni personajes; escenas originales con la ambientación.

## Guía de regalos (Navidad) — nov 2026
- `explicativo/regalos.py` + `explicativo/regalos/rgNN_<tema>.py` → `python3 ... fb|tt salida.mp4`. Fernando escoge los 5 productos y manda las fotos (las de la web, con marco neón y REC); van en `productos/<tema>/p1..p5.jpg` (no se suben al repo).
- Narrador = CLIPS REALES de Higgsfield (Kling, 10 s, sin voz) en `marcas/comics-store/intros/clips/` (navidad_hablando_v1/v2 = 9:16, h/h2 = 16:9 para YouTube); se alternan tomas en bucle de ida y vuelta. Ya no se anima la boca de la foto (se veía mal).
- Pedestal: `biblioteca/fondos/v/navidad_pedestal.png`. No renderizar dos videos a la vez (se queda sin memoria).
- Productos SIN fondo (rembg isnet) con borde neón VERDE del logo, apoyados en el centro del pedestal; los anchos crecen hasta 1,45x. Recortes en `productos/<tema>/cN.png`.
- Pedestal: `navidad_pedestal_limpio.png` + letrero de Fernando `biblioteca/efectos/letrero_paraiso.png` (tubos verde/rosado parpadeando por separado). "REGALO #n" va en el borde del pedestal, encima del nombre.
- Overlays en video de Fernando (`biblioteca/efectos/video/`): neon_parpadeo, neon_escenario, bokeh_navidad, destello (al aparecer cada producto), light_leak (transiciones). Mezcla "screen".

## Teorías con figuras de la tienda (Strange/Doom) — nov 2026
- `explicativo/teoria_figuras.py` + `explicativo/t01_strange_doom.py tt|fb|yt|final salida.mp4` (yt y final con FORMATO=horizontal; el segmento `final` es la pantalla final de YouTube: se le agregan 7 s congelados y se pega al final).
- Figuras = FOTOS DE FERNANDO (sus productos de ML/web), recortadas con rembg isnet + limpieza de restos blancos; contorno neón por personaje (Doom verde, Strange naranja, Thanos morado; `COLOR_FIG`). Recortes en FIG_DIR (no se suben).
- Narrador = clips reales de Higgsfield del set gamer: `intros/clips/gamer_hablando_v1..v6` (9:16) y `gamer_hablando_h1..h2` (16:9). `gamer_otroset_h1` es de otro set: no mezclar. Cada escena de narrador usa otra toma: solo los tramos donde está hablando (detección de movimiento en la cara), arranca ya hablando y el clip avanza al ritmo de la voz (casi quieto en los silencios). Los clips con corte de cámara se parten solos en tomas separadas. Imagen del set 16:9: `intros/gamer_narrador_h2.png`.
- Animaciones en código: hilos del tiempo, mandalas, contador, ajedrez, dominós, planeta de parches, cómic inventado, línea de tiempo, estrellas, caja de comentario + barra de suscribirse. Subtítulos neón verde/naranja.
## Narrador en video real (24-nov-2026)
- Clips del narrador que genera Fernando (Higgsfield) en biblioteca/narrador/terror/{h,v}/*.mp4; boca medida con herramientas/medir_boca.py (insightface, modelos buffalo_s de GitHub) → boca.json.
- explicativo/narrador_video.py arma para cada escena una edición de los clips que sigue la voz (trozos de 0,3 s, velocidad 0,8–1,2x, fundidos cortos). Correlación boca–voz medida ≈0,5 sin desfase.
- Activo por defecto en YouTube horizontal (NARRADOR_VIDEO=0 para volver al narrador animado). Para agregar clips: copiar mp4 y volver a correr medir_boca.py.
- Narrador SINCRONIZADO (nov-24): los clips traen audio; se mide cuándo habla el narrador y cada aparición arranca justo donde él empieza a hablar (menos el lead), así entra hablando a la vez que la voz; luego velocidad normal, sin congelar. `motor.render` deja la actividad de la voz en `fn.voz`/`fn.lead`.
- Subtítulos de la guía de regalos en y_sub=195 (encima del letrero neón, que debe verse).
- `t02_si_dejaste_marvel.py` ("Si dejaste Marvel después de Endgame"): mismas reglas. Figuras disponibles (fotos de Fernando, en FIG_DIR): doom_*, strange_*, thanos_*, iron_*, cap_*, loki_*, thor_*, wolverine_*, magneto_*, xavier_silla, reed_estira, cosa_pie, cuatro_grupo, hulk_*, wanda_*. Los bustos (cap_saludo, thor_cerca, magneto_cerca, loki_cubo, wanda_cerca) van solos, no en parejas. `h_fit` evita que las poses abiertas se salgan del cuadro. Duraciones: revisar la suma del log antes de renderizar todo (TikTok ≥60 s, FB ~2 min, YouTube ≥5 min).
- Narrador GAMER sincronizado por BOCA (nov-24): clips partidos en cada corte de cámara en `biblioteca/narrador/gamer/{v,h}/*.mp4` + `boca.json` (medir_boca.py). `teoria_figuras.narrador_escena` normaliza la boca con todas las tomas juntas (una toma quieta no se infla) y edita trozos de 0,4 s que siguen la voz desde el primer cuadro; saltos caros y, entre tomas distintas, corte limpio (sin fundido doble). Para nuevos clips: partir en cortes, extraer cuadros a /tmp/narrador_frames/gamer/<ori>/<nombre>/ y correr medir_boca.py.

- ENTRADAS por línea (nov-24, guardadas en biblioteca/entradas/entradas.json como "entrada_gamer" y "entrada_terror"): TERROR = presentador encapuchado con "Hay historias que deberían permanecer enterradas…". LÍNEA GAMER (superhéroes, videojuegos, reseñas, teorías) = `INTRO_GAMER` en teoria_figuras.py: "Bienvenido a Comics Store. Aquí hablamos de héroes, villanos y videojuegos como nadie te los ha contado. Empecemos." Nunca mezclar. Cierre gamer: "¡Nos vemos en el próximo video!".
- Guía de regalos por PERSONAJE (nov-24): rg03 Spider-Man (hecho), rg04 Hulk, rg05 Capitán América (guiones listos). Orden: Marvel → DC → anime. TikTok debe durar ≥60 s (agregar 2 frases del narrador con mini-producto).
- Fotos: Chrome (extensión) arma una tira de 1200px por producto y la descarga a Descargas; `explicativo/regalos/recortar.py tira.jpg productos/<tema> solido|figura ...` recorta. Chrome debe permitir descargas múltiples para comics-store.com.co.
- `motor.render` guarda un segmento por escena (`<salida>.seg/`): si el entorno se reinicia, retoma. `herramientas_cola.sh` + cola.txt renderiza en fila.
- "Así nació Doom" (nov-25, `t03_asi_nacio_doom.py`): YouTube 10-20 min + 4 shorts verticales sacados del mismo guion (`s1..s4`, tramos por texto con `_tramo`). Mezcla figuras con IMÁGENES HD de Fernando (ChatGPT, sin personajes con derechos) en `biblioteca/fondos/doom/01..14.png` con `e_foto` (movimiento de cámara). AUDIO: `sonido.py` = música épica y ambientes generados por código (viento, fogata, chimenea, infierno, máquina, explosión, trueno, magia, campanas, forja, cosmos, noche, impacto); `motor.render(musica="epica")` y cada escena puede llevar `fn.amb = "viento+magia"`. SEMILLA por tema para que el narrador abra con otras tomas. Parte 2 ("Así termina Doom en Doomsday") después del 18-dic.
- Reed Richards: usar SIEMPRE figuras de pie (reed_pie, reed_legends, reed_pie2, reed_herbie) rotando; NO usar reed_estira (pose acostada, se ve de otra escala junto a Doom). Figuras nuevas en FIG_DIR: antorcha_mcu, sue_mcu, cosa_mcu, yelena_pie, cap_sigilo, iron_cromo, magneto_mckellen, thor_iw, gambit_pie, ciclope_pie, doom_pie4.
- PROPORCIÓN: figuras que comparten escena usan la MISMA altura (la menor que quepa) — e_dos/e_grupo. Nunca escalar cada figura por separado.
- CLIMA VISUAL (explicativo/clima.py): lluvia, relámpagos, nieve, viento, parpadeo de noche, brasas/fuego, destello de explosión. Por escena con fn.clima (mapa FOTO_CLIMA por imagen + CLAVE_CLIMA por palabra) y `esc = clima.envolver(esc)`.
- SERIE "CAMINO A DOOMSDAY" (10 caps, plan en el proyecto: claude/Serie_Camino_a_Doomsday.md). Cap 3 = explicativo/t04_illuminati.py (importa t03 y cambia IMG_DIR/SEMILLA). Fondos en biblioteca/fondos/illuminati. Figuras nuevas: blackbolt_mano/pie, bestia_mcu/clasico/ruge/estatua.
- Cap 4 Incursiones = explicativo/t05_incursiones.py (fondos biblioteca/fondos/incursiones; figura nueva molecula_pie). Escenas nuevas: e_reloj (cuenta regresiva), e_dilema, e_revela (silueta que se revela), e_moleculas.
- Cap 5 4 Fantásticos = explicativo/t06_cuatro_fantasticos.py (fondos biblioteca/fondos/cuatro). Figuras nuevas: annihilus_pie/alas, topo_pie/grupo/moloides, franklin_pie, futuro_pareja/trio.
- NARRADOR v2 (desde Cap. 6): _planificar_v2 en teoria_figuras. Tomas de 1,2 s mínimo, boca nunca quieta con voz (penaliza x3), historial global que prohíbe repetir el mismo tramo/gesto, al cortar cambia de toma y alterna plano general (h*) / primer plano (cv*). Los primeros planos horizontales cv*.mp4 salen de los clips verticales (recorte 1080x608 alrededor de la cara, escalado a 1920x1080). Para más variedad: pedir a Fernando más clips HORIZONTALES 16:9 de Higgsfield (10-15 s, distintos gestos).
- NARRADOR 30 fps: después de setup.sh correr `python3 herramientas/narrador_30fps.py` (convierte clips a 30 fps interpolados + primeros planos cv* con cas, y reescala boca.json). El editor v2 reproduce SIEMPRE a 1x (sin cambios de velocidad: se veían raros).
