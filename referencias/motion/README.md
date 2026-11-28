# Guías de animación (de iart-ai, MIT — ver LICENSE_iart-ai)

Reglas de oficio para animaciones que hace la fábrica. Son guías (escritas para Remotion/JS);
en la fábrica se aplican las mismas reglas en Python/PIL:
- Todo valor sale del número de cuadro (nunca de un reloj): ya es así en lib.py.
- Las cifras se animan con easing (easeOutCubic), se redondean antes de mostrarlas y la caja de dígitos es fija (no salta).
- Verificar: inicio | mitad | final en una sola imagen con `herramientas/hoja_contacto.sh salida.png f0.png f1.png f2.png`.

| Archivo | Para qué página |
|---|---|
| graficas_animadas.md, carrera_de_barras.md | La Tabla FC (tablas por jornada), BitBot Sports (probabilidades) |
| tipografia_cinetica.md, recetas_revelado.md | Ganchos y títulos de todas las páginas |
| subtitulos_animados.md | Karaoke (motor.py y recortador) |
| cuenta_regresiva.md, video_corto.md | Tops de Guerra de Peludos y Comics Store; shorts |
