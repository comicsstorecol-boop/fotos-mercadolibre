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

## Visuales por escena (opcional, campo `visual` en cada dato)
- `{"tipo":"icono","nombre":"trofeo"}` — íconos 3D: trofeo, calendario (con "texto":"19"), cronometro, ojo, balon, baloncesto, control, alerta, grafica, corazon, lupa, rayo, sonido, dinero
- `{"tipo":"barra","valor":82,"etiqueta":"Probabilidad","nota":"Cuota mínima 1.30"}` — barra que se llena (unidad por defecto %)
- `{"tipo":"comparar","items":[["Perro",45000],["Gato",64000]],"unidad":" Hz"}` — barras comparativas (3er valor opcional = etiqueta)
- `{"tipo":"tabla","filas":[["1","Nacional","40"],...],"resaltar":[0],"eliminados":[8]}` — tabla de posiciones animada
- `{"tipo":"lista","titulo":"Grupo A","items":[...],"resaltar":[0]}` — lista que aparece ítem por ítem
- `"cuenta_regresiva": true` en el guion muestra #N..#1

## Ganchos de retención
- `"gancho": {"texto": "frase corta en pantalla", "voz": "frase dicha", "icono": "alerta"}` → el video ARRANCA con el gancho (antes del logo, que pasa a 1,3 s).
- `"reganchos": [{"despues_de": 3, "texto": "¡Espera!…", "voz": "…", "icono": "rayo"}]` → pausa corta tras el dato N (contando todos los datos en orden).
- Automático: zoom de golpe al empezar cada dato y subtítulos palabra por palabra en gancho, intro y re-ganchos.
