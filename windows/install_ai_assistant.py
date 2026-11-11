"""Install the runtime of the optional eSim AI Assistant on Windows.

Run by the installer's "aiassistant" task with eSim's bundled Python, as the
installing user (Ollama installs per user). The chat window's own Python
packages are already in the bundled interpreter; this adds what is too big to
bundle: the Ollama runtime -- pinned in deps-manifest.json and refused unless
its sha256 matches -- and the local models the chat window requires.

Best-effort throughout: every problem is reported and the eSim install still
completes. The assistant copes on its own later, too: it starts Ollama when
eSim opens and downloads any missing model on first start.
"""

import hashlib
import json
import os
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import urllib.request

WINDIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(WINDIR), "src"))

from chatbot.chatbot_thread import REQUIRED_MODELS  # noqa: E402

with open(os.path.join(WINDIR, "deps-manifest.json"), encoding="utf-8") as _fh:
    OLLAMA_SETUP = json.load(_fh)["ollama_setup"]

TEMP_DIR = tempfile.gettempdir()
# Where OllamaSetup.exe puts ollama.exe; the user PATH it adds is not visible
# to this already-running process.
OLLAMA_LOCATIONS = [
    os.path.join(os.environ.get("LOCALAPPDATA", ""), "Programs", "Ollama", "ollama.exe"),
    r"C:\Program Files\Ollama\ollama.exe",
]


def find_ollama():
    found = shutil.which("ollama")
    if found:
        return found
    return next((p for p in OLLAMA_LOCATIONS if os.path.isfile(p)), None)


def download(url, dest):
    with urllib.request.urlopen(url) as resp, open(dest, "wb") as out:
        total = int(resp.headers.get("Content-Length") or 0)
        done = 0
        while True:
            chunk = resp.read(1 << 20)
            if not chunk:
                break
            out.write(chunk)
            done += len(chunk)
            if total:
                print("\r  %d / %d MB" % (done >> 20, total >> 20), end="", flush=True)
    print()


def run(cmd):
    return subprocess.call(cmd)


def is_running():
    try:
        socket.create_connection(("localhost", 11434), timeout=0.5).close()
        return True
    except OSError:
        return False


def start_server(ollama):
    return subprocess.Popen(
        [ollama, "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))


def stop_server(server):
    server.terminate()


def _sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def install_ollama():
    """Download the pinned OllamaSetup.exe, verify it, run it silently."""
    setup = os.path.join(TEMP_DIR, OLLAMA_SETUP["filename"])
    print("Downloading Ollama (%s)..." % OLLAMA_SETUP["url"])
    try:
        download(OLLAMA_SETUP["url"], setup)
        if _sha256(setup) != OLLAMA_SETUP["sha256"].lower():
            print("The Ollama download does not match its pinned sha256; "
                  "not running it. Install Ollama from https://ollama.com instead.")
            return None
        print("Installing Ollama...")
        run([setup, "/VERYSILENT", "/NORESTART", "/SUPPRESSMSGBOXES"])
        # OllamaSetup always launches its tray app, which pops a Welcome
        # window over eSim's silent install and keeps running. Close it (and
        # the server it started); the models are pulled through our own
        # server below and eSim starts Ollama when the assistant needs it.
        run(["taskkill", "/im", "ollama app.exe", "/f", "/t"])
    finally:
        if os.path.exists(setup):
            os.remove(setup)
    return find_ollama()


def main():
    try:
        ollama = find_ollama() or install_ollama()
        if not ollama:
            print("Ollama is not installed; the AI Assistant will ask for it "
                  "when eSim starts.")
            return 0

        server = None
        if not is_running():
            server = start_server(ollama)
            for _ in range(30):
                if is_running():
                    break
                time.sleep(1)
        try:
            for model in REQUIRED_MODELS:
                print("Downloading AI model %s..." % model)
                if run([ollama, "pull", model]) != 0:
                    print("Could not download %s; the assistant fetches it on "
                          "first start." % model)
        finally:
            if server is not None:
                stop_server(server)
    except Exception as exc:  # never fail the eSim install over the assistant
        print("AI Assistant setup stopped: %s" % exc)
        print("eSim is installed; the assistant can finish setting up on first start.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
