# Recortador de shorts

Saca clips verticales (9:16) de cualquier video largo de la fábrica (YouTube horizontal o vertical),
con subtítulos karaoke neón en los colores de la página, gancho arriba y cierre con el sitio web.

Adaptado de [claude-shorts](https://github.com/AgriciDaniel/claude-shorts) (MIT, ver `LICENSE_claude-shorts`):
`cortes.py` es su `snap_boundaries.py` (cortes en palabras completas, frases y silencios) y
`RUBRICA_claude-shorts.md` es su rúbrica para puntuar tramos.

## Preparar (una vez por sesión)
`RECORTADOR=1 ./setup.sh` → instala sherpa-onnx + OpenCV y baja Parakeet TDT v3 (~490 MB, desde GitHub).
En el PC de Fernando también sirve `pip install faster-whisper` (se usa primero si está).

## Flujo recomendado (Claude elige los tramos)
1. `python3 recortador/recortar.py VIDEO.mp4 --marca comics-store --guion guion.txt --solo-candidatos`
   - `--guion`: el texto narrado (si el video salió de la fábrica, ya existe). Con él los subtítulos
     quedan escritos exactos (Doom, Comics Store…). Sin guion se aplica `correcciones.json`.
   - Deja `transcripcion.json` (tiempos por palabra) y `candidatos.json` (respaldo automático).
2. Claude lee la transcripción con la rúbrica y escribe `segmentos.json`:
   `[{"start": 11.0, "end": 34.8, "gancho": "LO QUE NADIE TE CUENTA DE DOOM"}]`
   Reglas: 20–60 s, que se entienda solo (sin "como dije antes"), arranque fuerte, cierre en frase completa,
   gancho ≤6 palabras, verdadero y sacado del tramo.
3. `python3 recortador/recortar.py VIDEO.mp4 --marca comics-store --segmentos segmentos.json`
   → `/home/claude/salidas/shorts_<video>/short_01.mp4 …`

Automático sin revisar: `--n 4` (sin `--segmentos`).

## Opciones
- `--encuadre auto` (sigue la cara si hay narrador; si no, centro) · `centro` · `completo` (video entero sobre fondo desenfocado).
- `--cierre "TEXTO"` / `--sin-cierre` (por defecto "VIDEO COMPLETO EN NUESTRO CANAL" + sitio de la marca).
- `--min/--max` duración en segundos.
- Nombres mal oídos: agregarlos a `correcciones.json` (`"lo que oye": "como se escribe"`).

Velocidad en la nube (2 núcleos): transcribir ~12 s por minuto de video; render ~8 s por short de 25 s.
