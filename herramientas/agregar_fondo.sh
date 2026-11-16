#!/bin/bash
# Uso: herramientas/agregar_fondo.sh <nombre> <imagen> [<imagen2> ...]  -> detecta orientación, mejora x2 y guarda en biblioteca/fondos/{h,v}/<nombre>.png
cd "$(dirname "$0")/.."
[ -f /tmp/x2.pth ] || curl -sSL -o /tmp/x2.pth https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.1/RealESRGAN_x2plus.pth
n=$1; shift
for f in "$@"; do
  o=$(python3 -c "from PIL import Image;w,h=Image.open('$f').size;print('h' if w>h else 'v')")
  python3 herramientas/mejorar_imagen.py "$f" "biblioteca/fondos/$o/$n.png" && echo "$n $o OK"
done
