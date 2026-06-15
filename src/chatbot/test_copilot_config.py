# test_copilot_config.py
import sys
import os

# Append src to path so Python can resolve your modules
sys.path.append(os.path.abspath("./src"))

try:
    from chatbot.chatbot_thread import OllamaWorker
    print("[SUCCESS] Module imports matched cleanly.")
    
    # Instantiate the worker to trigger config loading
    worker = OllamaWorker([])
    
    print("\n--- Parsing Verification ---")
    print(f"Target Text Model: {worker.config_data.get('models', {}).get('text_model')}")
    print(f"Sampling Temp:     {worker.config_data.get('sampling', {}).get('temperature')}")
    print(f"Context Window:    {worker.config_data.get('context_window', {}).get('text_num_ctx')} tokens")
    
    if worker.config_data:
        print("\n[PASSED] config.json successfully loaded and mapped to the backend thread!")
    else:
        print("\n[FAILED] config.json data dictionary is empty. Check your directory paths.")

except Exception as e:
    print(f"\n[CRITICAL FAULT] Test environment broke down: {e}")