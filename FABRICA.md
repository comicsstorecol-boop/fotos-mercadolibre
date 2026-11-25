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

- ENTRADAS por línea (nov-24): TERROR = presentador encapuchado con "Hay historias que deberían permanecer enterradas…". LÍNEA GAMER (superhéroes, videojuegos, reseñas, teorías) = `INTRO_GAMER` en teoria_figuras.py: "Bienvenido a Comics Store. Aquí hablamos de héroes, villanos y videojuegos como nadie te los ha contado. Empecemos." Nunca mezclar. Cierre gamer: "¡Nos vemos en el próximo video!".
