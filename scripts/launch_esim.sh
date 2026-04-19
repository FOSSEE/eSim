#!/usr/bin/env bash
# Launch eSim with Copilot
# Usage: ./scripts/launch_esim.sh   or   bash scripts/launch_esim.sh

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

# Ensure .esim dir exists (avoids workspace error)
mkdir -p ~/.esim

# Vosk STT model (if installed)
VOSK_DEFAULT="$HOME/.local/share/esim-copilot/vosk-model-small-en-us-0.15"
if [ -z "$VOSK_MODEL_PATH" ] && [ -d "$VOSK_DEFAULT" ]; then
  export VOSK_MODEL_PATH="$VOSK_DEFAULT"
fi

# Activate venv and launch
source .venv/bin/activate
cd src/frontEnd
QT_QPA_PLATFORM=xcb python Application.py
