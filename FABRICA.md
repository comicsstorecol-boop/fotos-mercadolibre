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
- Narrador = CLIP REAL de Higgsfield (Kling, 10 s, sin voz) en bucle de ida y vuelta: `marcas/comics-store/intros/clips/`. Ya no se anima la boca de la foto (se veía mal).
- Pedestal: `biblioteca/fondos/v/navidad_pedestal.png`. No renderizar dos videos a la vez (se queda sin memoria).
