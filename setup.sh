#!/usr/bin/env bash
# Prepara el entorno: librerías, voz base latina (Kokoro "Alex", es-419) y convertidor a la voz de Fernando (kNN-VC).
set -e
KIT="$(cd "$(dirname "$0")" && pwd)"
PIP="pip install --break-system-packages -q"
$PIP piper-tts kokoro-onnx soundfile numpy pillow librosa torch torchaudio 2>/dev/null || pip install -q piper-tts kokoro-onnx soundfile numpy pillow librosa torch torchaudio
mkdir -p "$KIT/voz" "$KIT/knnvc"
GH=https://github.com
# voz base Kokoro
for f in kokoro-v1.0.onnx voices-v1.0.bin; do
  [ -s "$KIT/voz/$f" ] || curl -sL -o "$KIT/voz/$f" $GH/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/$f
done
# voz Piper de respaldo (sin conversión)
if [ ! -f "$KIT/voz/es_MX-claude-high.onnx" ]; then
  cd "$KIT/voz" && curl -sL -o v.tar.bz2 $GH/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-es_MX-claude-high.tar.bz2
  tar xjf v.tar.bz2 vits-piper-es_MX-claude-high/es_MX-claude-high.onnx vits-piper-es_MX-claude-high/es_MX-claude-high.onnx.json
  mv vits-piper-es_MX-claude-high/* . && rm -rf vits-piper-es_MX-claude-high v.tar.bz2
fi
# convertidor de voz kNN-VC
cd "$KIT/knnvc"
[ -d repo ] || git clone -q --depth 1 $GH/bshall/knn-vc repo
for f in WavLM-Large.pt prematch_g_02500000.pt; do
  [ -s "$f" ] || curl -sL -o "$f" $GH/bshall/knn-vc/releases/download/v0.1/$f
done
which ffmpeg >/dev/null || echo "FALTA ffmpeg"
echo "Kit listo"
