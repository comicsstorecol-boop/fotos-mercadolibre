#!/bin/sh
# Cola de renders: cada línea "script version salida". Los segmentos ya hechos se reutilizan si el entorno se reinicia.
cd /home/claude/kit-peludos
while read -r scr ver out; do
  [ -z "$scr" ] && continue
  [ -f "$out" ] && { echo "SKIP $out"; continue; }
  mkdir -p "$(dirname "$out")"
  python3 "$scr" "$ver" "$out" < /dev/null > "/home/claude/log_$(basename "$out" .mp4).log" 2>&1 && echo "DONE $out" || echo "FAIL $out"
done < /home/claude/cola.txt
echo COLA_TERMINADA
