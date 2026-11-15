# Estilo EXPLICATIVO (historias, terror, explicaciones)
Una escena ilustrada por frase, cámara en movimiento, transiciones suaves y subtítulos karaoke.
- `lib.py`: biblioteca (paisaje, sala, laboratorio, persona, cara_humana, perro_perfil, bulldog, hueso, aro, ondas, cono, burbuja, etiqueta, contador, camera, karaoke, tiempos_palabras, glow, vgrad, paletas ATARDECER/NOCHE/DIA/ESTUDIO).
- Se usan también los íconos de `visuales.py` y la voz/música/efectos de `generador.py`.
- NO es necesario usar la mascota de la página: las escenas muestran lo que se narra (lugares, personas, objetos, diagramas). Para cerrar usar `escena_cierre(marca("<pagina>"), t, d, "¿PREGUNTA?")`.
- Cada video es un script como `piloto_perro_cabeza.py`: lista ESCENAS = [(función_escena, frase, {palabras_clave}), ...].
- Render: `python3 explicativo/<script>.py salida.mp4` (PREVIEW=1 para hoja de vista previa). ~5 s de render por segundo de video.
