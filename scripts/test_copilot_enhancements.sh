#!/usr/bin/env bash
# Test script for Copilot enhancements - run on Ubuntu VM
# Usage: ./scripts/test_copilot_enhancements.sh
# Prereq: source .venv/bin/activate, ollama serve running

set -e
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "=== eSim Copilot Enhancement Tests ==="
echo ""

# Ensure venv
if [ -z "$VIRTUAL_ENV" ]; then
    echo "[1] Activating venv..."
    source .venv/bin/activate
fi

# Add src to path
export PYTHONPATH="$ROOT/src:$PYTHONPATH"
cd src

echo "[2] Test: Netlist contract loading"
python3 -c "
from frontEnd.Chatbot import NETLIST_CONTRACT
assert NETLIST_CONTRACT, 'NETLIST_CONTRACT should not be empty'
print('  OK: Contract loaded, length:', len(NETLIST_CONTRACT))
"

echo "[3] Test: RAG relevance threshold"
python3 -c "
from chatbot.knowledge_base import search_knowledge, RELEVANCE_THRESHOLD
print('  RELEVANCE_THRESHOLD:', RELEVANCE_THRESHOLD)
result = search_knowledge('how to add ground in eSim', n_results=2)
if result:
    print('  OK: RAG returned context, length:', len(result))
else:
    print('  SKIP: RAG empty (run ingest.py first if needed)')
"

echo "[4] Test: PaddleOCR / image_handler import"
python3 -c "
from chatbot.image_handler import HAS_PADDLE, analyze_and_extract
if HAS_PADDLE:
    print('  OK: PaddleOCR available')
else:
    print('  OK: PaddleOCR unavailable (expected message shown at import)')
"

echo "[5] Test: Ollama connectivity (optional)"
python3 -c "
try:
    from chatbot.ollama_runner import run_ollama
    r = run_ollama('Say OK in one word.')
    if r and len(r) > 0:
        print('  OK: Ollama responded')
    else:
        print('  WARN: Ollama returned empty (is ollama serve running?)')
except Exception as e:
    print('  WARN: Ollama test failed:', e)
"

echo ""
echo "=== All tests completed ==="
