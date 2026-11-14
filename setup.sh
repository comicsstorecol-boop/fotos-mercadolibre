#!/usr/bin/env bash
# Prepara el entorno: librerías + voz latina (es_MX claude-high, licencia libre)
set -e
KIT="$(cd "$(dirname "$0")" && pwd)"
pip install --break-system-packages -q piper-tts soundfile numpy pillow 2>/dev/null || pip install -q piper-tts soundfile numpy pillow
if [ ! -f "$KIT/voz/es_MX-claude-high.onnx" ]; then
  mkdir -p "$KIT/voz" && cd "$KIT/voz"
  curl -sL -o v.tar.bz2 https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-es_MX-claude-high.tar.bz2
  tar xjf v.tar.bz2 vits-piper-es_MX-claude-high/es_MX-claude-high.onnx vits-piper-es_MX-claude-high/es_MX-claude-high.onnx.json
  mv vits-piper-es_MX-claude-high/* . && rm -rf vits-piper-es_MX-claude-high v.tar.bz2
fi
which ffmpeg >/dev/null || echo "FALTA ffmpeg"
echo "Kit listo"
