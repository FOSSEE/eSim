#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "[1/8] Installing system packages (Ubuntu/Debian)…"
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

echo "[2/8] Creating Python virtualenv…"
cd "$ROOT_DIR"
python3.10 -m venv .venv
source .venv/bin/activate

echo "[3/8] Installing Python dependencies…"
python -m pip install --upgrade pip wheel
# hdlparse needs setuptools<58 (use_2to3 removed in setuptools 58+)
python -m pip install setuptools==57.5.0
python -m pip install hdlparse==1.0.4 --no-build-isolation || {
    echo
    echo "ERROR: hdlparse installation failed."
    echo "The original hdlparse package may fail on some systems."
    echo
    echo "Alternative:"
    echo "pip install 'hdlparse @ git+https://github.com/nehadhumal-dev/hdlparse.git'"
    echo
    exit 1
}
echo "setuptools<58" > /tmp/pip-constraints.txt
python -m pip install -c /tmp/pip-constraints.txt -r requirements.txt
python -m pip install -c /tmp/pip-constraints.txt -r requirements-copilot.txt

echo "[4/8] Installing PaddlePaddle (CPU, AVX, MKL)…"
python -m pip install "paddlepaddle==2.6.2" \
  -f https://www.paddlepaddle.org.cn/whl/linux/mkl/avx/stable.html

echo "[5/8] Installing Ollama if missing…"
if ! command -v ollama >/dev/null 2>&1; then
  curl -fsSL https://ollama.com/install.sh | sh
fi

echo "[6/8] Pulling required Ollama models…"
ollama pull qwen2.5:3b
ollama pull minicpm-v
ollama pull nomic-embed-text

echo "[7/8] Installing Vosk small English model…"
VOSK_BASE="${XDG_DATA_HOME:-$HOME/.local/share}/esim-copilot"
mkdir -p "$VOSK_BASE"
cd "$VOSK_BASE"
if [ ! -d "vosk-model-small-en-us-0.15" ]; then
  wget -q https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip -O vosk-model-small-en-us-0.15.zip
  unzip -q vosk-model-small-en-us-0.15.zip
  rm -f vosk-model-small-en-us-0.15.zip
fi
echo "[8/8] Running RAG ingestion..."
CHROMA_DB="$ROOT_DIR/src/chroma_db"

if [ ! -d "$CHROMA_DB" ] || [ -z "$(ls -A "$CHROMA_DB" 2>/dev/null)" ]; then
    echo "Creating knowledge base..."
    (
        cd "$ROOT_DIR/src"
        python ingest.py
    ) || {
        echo "ERROR: RAG ingestion failed."
        exit 1
    }
else
    echo "Knowledge base already exists, skipping ingestion."
fi

echo
echo "Done."
echo
echo "To start a new session:"
echo "  cd \"$ROOT_DIR\""
echo "  source .venv/bin/activate"
echo "  cd src/frontEnd"
echo "  python Application.py"
echo
echo "RAG knowledge base:"
echo "  Stored in: $ROOT_DIR/src/chroma_db"
echo
echo "Optional env vars:"
echo "- export VOSK_MODEL_PATH=\"$VOSK_BASE/vosk-model-small-en-us-0.15\""
echo "- export ESIM_COPILOT_DB_PATH=\"${XDG_DATA_HOME:-$HOME/.local/share}/esim-copilot/chroma\""