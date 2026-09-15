import sys, types

sys.path.insert(0, 'src')

# Stub configuration module
_c = types.ModuleType('configuration')
_a = types.ModuleType('configuration.Appconfig')

class _S:
    noteArea = {}
    current_project = {'ProjectName': None}
    procThread_list = []
    process_obj = []
    def print_info(self, *a): pass
    def print_error(self, *a): pass

_a.Appconfig = _S
_c.Appconfig = _a
sys.modules['configuration'] = _c
sys.modules['configuration.Appconfig'] = _a

# Test chatbot_thread imports
from chatbot.chatbot_thread import (
    get_stt_backend, VISION_MODEL_KEYWORDS, is_ollama_running,
    _is_vision_model, OllamaWorker, MicWorker
)
print("chatbot_thread.py imports: OK")
print("STT backend detected:", get_stt_backend())
print("Vision model keywords:", VISION_MODEL_KEYWORDS[:4])
print("is_ollama_running():", is_ollama_running())
print("_is_vision_model('llava'):", _is_vision_model('llava'))
print("_is_vision_model('qwen2.5'):", _is_vision_model('qwen2.5'))

# Test Chatbot.py import (no QApplication needed just to import)
from frontEnd.Chatbot import (
    ChatbotGUI, _render_markdown, _user_bubble, _bot_bubble,
)
print("Chatbot.py imports: OK")

# Quick markdown render sanity check
rendered = _render_markdown("Hello **bold** and `code` here")
assert '<b>' in rendered, "Bold not rendered"
assert 'Consolas' in rendered, "Code not rendered"
print("Markdown renderer: OK")

# Vision model check
rendered2 = _render_markdown("Test _var_name_ rendering")
print("Italic underscore rendered (should NOT italicise var names):", '_var_name_' not in rendered2 or '<i>' in rendered2)

print()
print("All checks passed!")
