# eSim AI Assistant

The eSim AI Assistant is a chat panel inside eSim that answers questions about
eSim, ngspice, KiCad and circuits, explains netlists, and explains why a
simulation failed. It runs a language model **locally** through
[Ollama](https://ollama.com): questions, netlists and logs never leave your
computer (voice input is the one exception, see below).

The assistant is optional. eSim works exactly as before without it.

## Installing

### Ubuntu

`install-eSim.sh --install` asks:

```
Install the eSim AI Assistant (downloads Ollama and ~2.2 GB of local AI models)? (y/n):
```

Answering `y` installs:

- the assistant's Python packages (`ollama`, `SpeechRecognition`) into eSim's
  own virtualenv, and `python3-pyaudio` for the microphone;
- Ollama, with its official installer, if it is not already present;
- the models the assistant uses: `qwen2.5:3b` (1.9 GB) and `nomic-embed-text`
  (0.3 GB).

If a download fails, the installer prints a warning and carries on; eSim is
installed either way.

To add the assistant to an existing installation, install Ollama from
[ollama.com](https://ollama.com), then:

```bash
~/.esim/env/bin/pip install -r ~/eSim/requirements-copilot.txt
ollama pull qwen2.5:3b
```

(Adjust `~/eSim` to wherever eSim is installed.)

### Windows

The installer has an extra option, **Install the eSim AI Assistant**, on the
*Select Additional Tasks* page. It is unticked by default because it downloads
Ollama (1.5 GB) and the models (2.2 GB). When ticked, a console window shows
the downloads after the files are copied. The Ollama download is checked
against a pinned SHA-256 checksum and is not run if it does not match.

Without the option, eSim still shows the assistant; it tells you to install
Ollama from [ollama.com](https://ollama.com). Once Ollama is installed, the
assistant downloads its model the next time eSim starts.

### Uninstalling

Uninstalling eSim does **not** remove Ollama or its models, since other
applications may use them. Remove Ollama through its own uninstaller (Windows
*Apps* settings, or the steps on ollama.com for Linux).

## Using the assistant

The assistant opens on the right of the eSim window. Toggle it with
**View → AI Assistant** or the round robot button at the bottom right.

When eSim starts, the assistant starts Ollama if it is not already running and
shows **Live** in its header once a model is ready. The model in use is shown
in the drop-down next to the ≡ (chat history) button.

- **Ask a question.** Type in the box at the bottom and press Enter or ➤.
  ↑/↓ recalls earlier questions.
- **Analyse a netlist.** Right-click a project in the Project Explorer and
  choose **Analyze Project Netlist** (uses `<project>.cir.out`), or right-click
  a `.cir`, `.cir.out` or `.net` file and choose **Analyze this Netlist**.
  Generate the netlist first (KiCad-to-Ngspice conversion).
- **Explain a failed simulation.** When a simulation fails, the assistant
  opens and explains ngspice's error automatically. The error output is also
  kept as `ngspice_error.log` in the project folder; it is removed when the
  next simulation starts.
- **Ask about a schematic image.** Attach an image with 📎 or drag it into the
  panel. This needs a vision model, which the installers do not download
  (5.5 GB):

  ```bash
  ollama pull minicpm-v
  ```

- **Voice input.** 🎤 records a question and types it into the box. Speech is
  converted to text by Google's online speech service, so it needs internet
  and sends the recording to Google.
- **Past chats.** ≡ opens the chat history; chats can be renamed, exported
  and deleted there.

## Where the assistant keeps data

| What | Where |
|---|---|
| Chat history | `~/.esim/chat_sessions/` |
| Pasted images | `~/.esim/clipboard_images/` |
| Models | Ollama's model store (managed by Ollama; `ollama list` shows them, `ollama rm <model>` deletes one) |

## Troubleshooting

| Message or symptom | What to do |
|---|---|
| "Could not start Ollama" | Install Ollama from ollama.com and restart eSim. |
| "No Ollama models found" | Run `ollama pull qwen2.5:3b`. |
| The assistant is missing from **View** | Its Python packages are not installed; see the manual steps above. |
| Mic button does nothing | Install PyAudio (`sudo apt install python3-pyaudio` on Ubuntu) and check the internet connection. |
| Replies are slow | The model runs on your CPU unless Ollama finds a supported GPU. The first reply after starting also loads the model into memory. |

## Limitations

- Answers come from a small local model and can be wrong. The assistant does
  not look up the eSim documentation, so check important advice against the
  eSim manual.
- Some ngspice failures (for example a floating node) end with a success exit
  code; eSim treats those runs as successful, so the assistant is not opened
  for them. Ask it about the console output instead.
- In the dark theme the chat area itself stays light.
