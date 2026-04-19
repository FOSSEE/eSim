#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "[1/7] Installing system packages (Ubuntu/Debian)…"
sudo apt-get update
sudo apt-get install -y \
  python3.10 python3.10-venv python3-pip \
  curl wget unzip \
  ngspice kicad \
  portaudio19-dev \
  libgl1 libglib2.0-0 \
  libxcb-xinerama0 libxcb-cursor0 libxkbcommon-x11-0 \
  libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-render-util0 \
  libxcb-xinput0 libxcb-shape0 libxcb-randr0 libxcb-util1

echo "[2/7] Creating Python virtualenv…"
cd "$ROOT_DIR"
python3.10 -m venv .venv
source .venv/bin/activate

echo "[3/7] Installing Python dependencies…"
python -m pip install --upgrade pip wheel
# hdlparse needs setuptools<58 (use_2to3 removed in setuptools 58+)
python -m pip install setuptools==57.5.0
python -m pip install hdlparse==1.0.4 --no-build-isolation
echo "setuptools<58" > /tmp/pip-constraints.txt
python -m pip install -c /tmp/pip-constraints.txt -r requirements.txt
python -m pip install -c /tmp/pip-constraints.txt -r requirements-copilot.txt

echo "[4/7] Installing PaddlePaddle (CPU, AVX, MKL)…"
python -m pip install "paddlepaddle==2.5.2" \
  -f https://www.paddlepaddle.org.cn/whl/linux/mkl/avx/stable.html

echo "[5/7] Installing Ollama if missing…"
if ! command -v ollama >/dev/null 2>&1; then
  curl -fsSL https://ollama.com/install.sh | sh
fi

echo "[6/7] Pulling required Ollama models…"
ollama pull qwen2.5:3b
ollama pull minicpm-v
ollama pull nomic-embed-text

echo "[7/7] Installing Vosk small English model…"
VOSK_BASE="${XDG_DATA_HOME:-$HOME/.local/share}/esim-copilot"
mkdir -p "$VOSK_BASE"
cd "$VOSK_BASE"
if [ ! -d "vosk-model-small-en-us-0.15" ]; then
  wget -q https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip -O vosk-model-small-en-us-0.15.zip
  unzip -q vosk-model-small-en-us-0.15.zip
  rm -f vosk-model-small-en-us-0.15.zip
fi

echo
echo "Done."
echo "- Activate venv:  source \"$ROOT_DIR/.venv/bin/activate\""
echo "- Run ingestion (optional for RAG):  (cd \"$ROOT_DIR/src\" && python ingest.py)"
echo "- Run eSim:  (cd \"$ROOT_DIR/src/frontEnd\" && QT_QPA_PLATFORM=xcb python Application.py)"
echo
echo "Optional env vars:"
echo "- export VOSK_MODEL_PATH=\"$VOSK_BASE/vosk-model-small-en-us-0.15\""
echo "- export ESIM_COPILOT_DB_PATH=\"${XDG_DATA_HOME:-$HOME/.local/share}/esim-copilot/chroma\""

