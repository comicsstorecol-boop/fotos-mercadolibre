# Kit de videos — Guerra de Peludos

Genera videos verticales (1080x1920) con el logo, el Bulldog y el gato animados hablando, voz latina de locutor, música y efectos.

```bash
./setup.sh                                   # instala librerías y descarga la voz
python3 generador.py guiones/X.json video.mp4
PREVIEW=1 python3 generador.py guiones/X.json video.mp4   # solo una hoja de vista previa
```

## Formato del guion (JSON)
- `titulo`: texto del cartel de la intro ("5 cosas que no sabías")
- `subtitulo_logo` (opcional): texto bajo el logo (por defecto "PERROS VS GATOS")
- `subtitulo_intro` (opcional, un solo equipo): texto grande en la intro
- `intro_voz`, `outro_voz`: lo que dice el narrador al inicio y al final
- `outro_texto`: dos líneas del cartel final
- `equipos`: 1 o 2 equipos. Cada uno: `equipo` ("perro" o "gato"), `nombre`, `plural`, `seccion_voz` (opcional), `datos`
- `datos`: lista con `titulo`, `texto` (en pantalla) y `voz` (opcional; si falta lee "Número N. titulo. texto"). En `voz` escribir los números en letras.
