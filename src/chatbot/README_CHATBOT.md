# eSim AI Assistant — developer notes

User documentation: [docs/AI_ASSISTANT.md](../../docs/AI_ASSISTANT.md).

The assistant ("eSim Copilot") was built by the Summer Fellowship 2026 interns
on the `eSim-Chat-Bot-Semester-Long-Internship_Autumn-2025` branch and brought
onto eSim 2.6 without its branch-era PyQt5 main-window changes. Everything
talks to a local [Ollama](https://ollama.com) server on `localhost:11434`.

## Layout

| File | Role |
|---|---|
| `src/frontEnd/Chatbot.py` | `ChatbotGUI`: the chat panel (bubbles, history sidebar, model picker, image staging, mic, netlist and error analysis). |
| `src/chatbot/chatbot_thread.py` | `QThread` workers the panel uses (`OllamaWorker`, `OllamaVisionWorker`, `MicWorker`, model fetch/pull, status), `start_ollama()`, `REQUIRED_MODELS`, `VISION_MODEL`. |
| `src/chatbot/config.json` | System prompts, context sizes, sampling, history length for the panel. |
| `src/chatbot/chatbot_core.py` | Keyword router (`handle_input`) with documentation retrieval, known-error table and OCR. **Not called by the panel.** |
| `src/chatbot/ollama_runner.py` | Non-streaming Ollama client used by `chatbot_core` and `knowledge_base`. |
| `src/chatbot/knowledge_base.py`, `src/ingest.py`, `src/manuals/` | ChromaDB documentation retrieval (RAG). Not called by the panel. |
| `src/chatbot/image_handler.py` | PaddleOCR + vision analysis for `chatbot_core`. Not called by the panel. |
| `src/chatbot/stt_handler.py` | Offline Vosk speech-to-text. Not called by the panel. |
| `src/chatbot/error_solutions.py` | Known ngspice/eSim error table for `chatbot_core`. |

The panel is the only path users reach. It sends the system prompt plus the
last lines of the conversation straight to Ollama and streams the reply;
`chatbot_core`'s routing, retrieval and OCR are exercised only by tests. Wiring
them in would change behaviour and is a separate piece of work.

## Hooks into eSim

- **Main window** (`src/frontEnd/Application.py`): `ChatbotGUI` is imported
  inside `try/except ImportError`; without the chatbot's packages
  `chatbot_dock` stays `None` and no assistant entry appears anywhere.
  `initchatbot()` runs *before* `initToolBar()`, which builds the View menu,
  so **View → AI Assistant** can use the dock's toggle action. The floating
  button is repositioned from `resizeEvent`, an event filter on the dock, and
  the dock's `visibilityChanged` (connected to a bound method: a lambda there
  fired into the destroyed window at shutdown).
- **Project Explorer** (`src/frontEnd/ProjectExplorer.py`):
  `_add_chatbot_actions()` adds **Analyze Project Netlist** /
  **Analyze this Netlist**, which call `ChatbotGUI.analyse_netlist()`. The
  project netlist is named after `_projectLabel()` (the `.proj` stem), not the
  folder, because explorer paths are canonical and lower-cased on
  case-insensitive filesystems.
- **Simulation errors**: on a failed run (not a cancelled one)
  `NgspiceWidget._write_error_log()` saves ngspice's console output — minus
  eSim's own `[eSim] …` lines — as `<project>/ngspice_error.log`;
  `_on_process_started()` deletes it at the start of every run, so a later
  cancelled or abandoned run never reuses a stale log. `plotSimulationData`
  then calls `Application._explain_simulation_error()`, which shows the dock
  and passes the log to `ChatbotGUI.debug_error()`.
- **`debug_error()`** trims the log to what precedes
  `No compatibility mode selected!` plus what follows `Circuit:` (up to
  `Total CPU time` when the run got that far), and falls back to the whole log
  when that leaves nothing — eSim's nghdl-simulator ngspice prints parse
  errors after `Circuit:` and never reaches `Total CPU time`.

## eSim theme gotcha

eSim's Aurora stylesheet gives every `QPushButton` `min-width: 72px` and
`padding: 8px 16px`, and a stylesheet `min-width` overrides
`setFixedSize()`. Unhandled, the panel's small icon buttons grew to ~100 px
and forced the dock to ~830 px. `_keep_fixed_button_sizes(root)` restates
each fixed-size button's size in the button's own stylesheet (which outranks
the application's) and corrects for borders. **Call it at the end of any
builder that creates fixed-size buttons** (it is already called by
`ChatbotGUI`, `ChatSidebar`, `_SessionItemWidget`, `ChatHistoryViewer` and
`_make_thumbnail`).

The panel's own colours are hard-coded for a light background; it does not
follow eSim's dark theme.

## Models

`REQUIRED_MODELS` in `chatbot_thread.py` is the single list of models the
panel needs (`qwen2.5:3b`, `nomic-embed-text`); it matches
`ollama_runner._DEFAULT_TEXT_MODEL`. On start the panel pulls any that are
missing. The installers pull the same list:

- `Ubuntu/install-eSim.sh` keeps a copy in `CHATBOT_MODELS`;
  `Ubuntu/tests/test_chatbot_step.py` fails if the two drift.
- `windows/install_ai_assistant.py` imports `REQUIRED_MODELS` directly.

Image questions need a vision model (`VISION_MODEL = "minicpm-v"`), which is
not installed by default because of its size (5.5 GB).

## Packaging

- `requirements-copilot.txt` lists only what the panel imports (`ollama`,
  `SpeechRecognition`). The branch's old pins (paddleocr 2.7, paddlepaddle
  2.6.2, pillow 10.4, opencv 4.6) only install on Python ≤ 3.10; eSim 2.6
  targets 3.11–3.14. `chromadb`, `paddleocr` and `vosk` for the unused
  modules are deliberately not listed.
- **Ubuntu**: the optional `installChatbot` step installs each
  `requirements-copilot.txt` entry into `~/.esim/env` (one guarded
  `pip install` per package — `windows/tests/test_packaging_pins.py` enforces
  that for every pip call in the script), `python3-pyaudio` from apt, Ollama
  via its official script (needs `curl` and `zstd`), then the models, starting
  a temporary `ollama serve` when no service is running (containers, WSL).
- **Windows**: `build-windows.ps1` bundles `requirements-copilot.txt` and
  PyAudio into the private Python. The opt-in `aiassistant` task in
  `installer.iss` runs `windows/install_ai_assistant.py` as the installing
  user; it downloads `OllamaSetup.exe` from the `ollama_setup` entry in
  `deps-manifest.json`, refuses it unless the SHA-256 matches, installs it
  silently and pulls the models. To move to a newer Ollama, update the
  entry's `version`, `url` and `sha256` (GitHub publishes the digest on the
  release asset and in the release's `sha256sum.txt`).

## Tests

```bash
# The panel inside eSim, the theme, installers' expectations
python -m pytest src/frontEnd/tests/test_chatbot_widgets.py \
                 src/frontEnd/tests/test_chatbot_integration.py \
                 src/ngspiceSimulation/tests/test_ngspice_error_log.py \
                 windows/tests/test_ai_assistant.py
# The chatbot package (needs ollama; retrieval / offline-speech tests skip
# unless chromadb / sounddevice + vosk are installed)
python -m pytest src/chatbot/tests
# The Ubuntu installer step (bash >= 4, e.g. on Ubuntu)
python3 -m pytest Ubuntu/tests/test_chatbot_step.py
```

The `frontEnd` tests replace `ChatbotGUI` with a stand-in or disable its
Ollama start-up, so they need no Ollama server. Many tests under
`src/chatbot/tests` document known weaknesses of `chatbot_core` and its
helpers ("vulnerability" tests) and assert the current behaviour.
