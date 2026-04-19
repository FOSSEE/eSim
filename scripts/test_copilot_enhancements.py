#!/usr/bin/env python3
"""
Test script for Copilot enhancements - run on Ubuntu VM.
Usage: cd ~/work/eSim && source .venv/bin/activate && python scripts/test_copilot_enhancements.py
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

os.chdir(SRC)


def test_netlist_contract():
    """Test that netlist contract loads from one of the bundled paths."""
    from frontEnd.Chatbot import NETLIST_CONTRACT
    assert NETLIST_CONTRACT, "NETLIST_CONTRACT should not be empty"
    assert "FACT" in NETLIST_CONTRACT or "SPICE" in NETLIST_CONTRACT
    print("[PASS] Netlist contract loaded")
    return True


def test_rag_relevance_threshold():
    """Test RAG search_knowledge with relevance threshold."""
    from chatbot.knowledge_base import search_knowledge, RELEVANCE_THRESHOLD
    print(f"  RELEVANCE_THRESHOLD = {RELEVANCE_THRESHOLD}")
    result = search_knowledge("how to add ground", n_results=3)
    # May be empty if ingest not run
    if result:
        assert "=== ESIM OFFICIAL DOCUMENTATION ===" in result
        print("[PASS] RAG search returned filtered context")
    else:
        print("[SKIP] RAG empty (run: cd src && python ingest.py)")
    return True


def test_paddleocr_message():
    """Test that image_handler imports and HAS_PADDLE is set."""
    from chatbot import image_handler
    # Just verify it doesn't crash; message is printed at import
    assert hasattr(image_handler, "HAS_PADDLE")
    print(f"[PASS] image_handler.HAS_PADDLE = {image_handler.HAS_PADDLE}")
    return True


def test_chatbot_copy_button():
    """Test that ChatbotGUI has copy_btn and copy_last_response."""
    from frontEnd.Chatbot import ChatbotGUI
    assert hasattr(ChatbotGUI, "copy_last_response")
    # Create instance would need QApplication - skip for headless
    print("[PASS] ChatbotGUI has copy_last_response method")
    return True


def test_ollama_connectivity():
    """Test Ollama is reachable (optional)."""
    try:
        from chatbot.ollama_runner import run_ollama
        r = run_ollama("Reply with exactly: OK")
        if r and "ok" in r.lower():
            print("[PASS] Ollama responded")
        else:
            print("[WARN] Ollama returned unexpected:", r[:50] if r else "empty")
    except Exception as e:
        print(f"[WARN] Ollama test failed: {e}")
    return True


def main():
    print("=== eSim Copilot Enhancement Tests ===\n")
    tests = [
        test_netlist_contract,
        test_rag_relevance_threshold,
        test_paddleocr_message,
        test_chatbot_copy_button,
        test_ollama_connectivity,
    ]
    for t in tests:
        try:
            t()
        except Exception as e:
            print(f"[FAIL] {t.__name__}: {e}")
    print("\n=== Done ===")


if __name__ == "__main__":
    main()
