"""The optional eSim AI Assistant on Windows.

The chat window's Python packages are bundled into the private interpreter
at build time; the Ollama runtime (1.5 GB) and the models are fetched at
install time by windows/install_ai_assistant.py when the user ticks the
installer task. Static checks read installer.iss / build-windows.ps1 /
deps-manifest.json as text; the helper runs with downloads and processes
replaced by fakes, so nothing here needs Windows.
"""

import hashlib
import json
import os
import re
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
WINDIR = os.path.dirname(HERE)
REPO = os.path.dirname(WINDIR)
sys.path.insert(0, WINDIR)
sys.path.insert(0, os.path.join(REPO, "src"))

import install_ai_assistant as helper  # noqa: E402
from chatbot.chatbot_thread import REQUIRED_MODELS  # noqa: E402


def _read(name):
    with open(os.path.join(WINDIR, name), encoding="utf-8") as fh:
        return fh.read()


def _iss_lines(section):
    out, inside = [], False
    for line in _read("installer.iss").splitlines():
        s = line.strip()
        if s.startswith("[") and s.endswith("]"):
            inside = s.lower() == "[%s]" % section.lower()
        elif inside and s and not s.startswith(";"):
            out.append(s)
    # Join Inno's backslash line continuations into one entry per line.
    return re.sub(r"\\\s*\n\s*", " ", "\n".join(out)).splitlines()


# ── installer.iss ──────────────────────────────────────────────────────────

def test_assistant_is_an_opt_in_task():
    task = [l for l in _iss_lines("Tasks") if 'Name: "aiassistant"' in l]
    assert task, "installer.iss has no aiassistant task"
    assert "unchecked" in task[0], "a multi-GB download must be opt-in"


def test_task_runs_the_helper_with_bundled_python_as_the_user():
    run = [l for l in _iss_lines("Run") if "install_ai_assistant.py" in l]
    assert len(run) == 1
    entry = run[0]
    assert r'Filename: "{app}\python\python.exe"' in entry
    assert "Tasks: aiassistant" in entry
    # Ollama installs per user; an elevated run would put it in the admin's
    # profile, not the user's.
    assert "runasoriginaluser" in entry
    assert "waituntilterminated" in entry


def test_helper_runs_before_eSim_is_offered_for_launch():
    lines = _iss_lines("Run")
    helper_at = next(i for i, l in enumerate(lines) if "install_ai_assistant.py" in l)
    launch_at = next(i for i, l in enumerate(lines) if "postinstall" in l)
    assert helper_at < launch_at


# ── build + manifest ───────────────────────────────────────────────────────

def test_build_bundles_the_chat_windows_python_packages():
    stage_python = re.search(r"function Stage-Python \{.*?\n\}", _read("build-windows.ps1"), re.S)
    body = stage_python.group(0)
    assert "requirements-copilot.txt" in body
    assert re.search(r"import [^'\n]*\bollama\b", body), "import check must cover ollama"
    assert re.search(r"(?im)^pyaudio\b", _read("requirements-windows.txt"))


def test_build_ships_the_helper_and_its_manifest_in_the_install():
    # The repo windows/ dir is left out of the stage wholesale; files the
    # installed eSim needs are copied back one by one. Without these two the
    # AI Assistant task runs python on a missing file (exit 2) and installs
    # nothing, while setup still reports success.
    stage_app = re.search(r"function Stage-App \{.*?\n\}", _read("build-windows.ps1"), re.S).group(0)
    copies = [l for l in stage_app.splitlines() if l.strip().startswith("Copy-Item") and "$stageWin" in l]
    for name in ("install_ai_assistant.py", "deps-manifest.json"):
        assert any("'%s'" % name in l for l in copies), "%s is not staged into windows\\" % name


def test_ollama_download_is_pinned_to_a_release_not_latest():
    entry = json.loads(_read("deps-manifest.json"))["ollama_setup"]
    assert "/latest/" not in entry["url"]
    assert "/v%s/" % entry["version"] in entry["url"]
    assert entry["filename"] == "OllamaSetup.exe"


# ── install_ai_assistant.py ────────────────────────────────────────────────

class Machine:
    """Fake Windows machine: records downloads and commands."""

    def __init__(self, tmp_path, ollama_installed=True, server_up=True,
                 payload=b"ollama-setup", failing_pulls=()):
        self.tmp = tmp_path
        self.ollama = str(tmp_path / "Ollama" / "ollama.exe")
        self.installed = ollama_installed
        self.server_up = server_up
        self.payload = payload
        self.failing_pulls = set(failing_pulls)
        self.downloads, self.commands, self.started, self.stopped = [], [], [], []

    def find_ollama(self):
        return self.ollama if self.installed else None

    def download(self, url, dest):
        self.downloads.append(url)
        with open(dest, "wb") as fh:
            fh.write(self.payload)

    def run(self, cmd):
        self.commands.append([os.path.basename(cmd[0])] + list(cmd[1:]))
        if os.path.basename(cmd[0]) == "OllamaSetup.exe":
            self.installed = True
            self.server_up = True   # setup starts the Ollama tray app and its server
        if cmd[0] == "taskkill":
            self.server_up = False
        if cmd[1:2] == ["pull"] and cmd[2] in self.failing_pulls:
            return 1
        return 0

    def is_running(self):
        return self.server_up

    def start_server(self, ollama):
        self.started.append(ollama)
        self.server_up = True
        return "server"

    def stop_server(self, server):
        self.stopped.append(server)


@pytest.fixture
def machine(tmp_path, monkeypatch):
    def make(**kw):
        m = Machine(tmp_path, **kw)
        for name in ("find_ollama", "download", "run", "is_running",
                     "start_server", "stop_server"):
            monkeypatch.setattr(helper, name, getattr(m, name))
        monkeypatch.setattr(helper, "TEMP_DIR", str(tmp_path))
        monkeypatch.setattr(helper, "OLLAMA_SETUP", {
            "url": "https://github.com/ollama/ollama/releases/download/v1/OllamaSetup.exe",
            "filename": "OllamaSetup.exe",
            "sha256": hashlib.sha256(b"ollama-setup").hexdigest(),
        })
        return m
    return make


def _pulled(m):
    return [c[2] for c in m.commands if c[1:2] == ["pull"]]


def test_existing_ollama_is_used_and_models_are_pulled(machine):
    m = machine()

    assert helper.main() == 0
    assert m.downloads == []
    assert _pulled(m) == list(REQUIRED_MODELS)


def test_missing_ollama_is_downloaded_verified_and_installed_silently(machine, tmp_path):
    m = machine(ollama_installed=False)

    assert helper.main() == 0
    assert m.downloads == [helper.OLLAMA_SETUP["url"]]
    setup = next(c for c in m.commands if c[0] == "OllamaSetup.exe")
    assert "/VERYSILENT" in setup and "/SUPPRESSMSGBOXES" in setup
    assert _pulled(m) == list(REQUIRED_MODELS)
    assert not (tmp_path / "OllamaSetup.exe").exists(), "installer left in TEMP"


def test_tray_app_started_by_ollama_setup_is_closed(machine):
    # OllamaSetup always launches "ollama app.exe", which opens a Welcome
    # window in the middle of eSim's silent install and keeps running, so a
    # scripted `Start-Process -Wait` install never returns.
    m = machine(ollama_installed=False, server_up=False)

    assert helper.main() == 0
    names = [c[0] for c in m.commands]
    kill = m.commands[names.index("taskkill")]
    assert names.index("OllamaSetup.exe") < names.index("taskkill")
    assert kill[1:] == ["/im", "ollama app.exe", "/f", "/t"]
    # the models still come down through the helper's own server
    assert m.started == [m.ollama] and m.stopped == ["server"]
    assert _pulled(m) == list(REQUIRED_MODELS)


def test_a_users_own_ollama_app_is_left_running(machine):
    m = machine()

    assert helper.main() == 0
    assert not any(c[0] == "taskkill" for c in m.commands)


def test_tampered_download_is_never_run(machine, tmp_path, capsys):
    m = machine(ollama_installed=False, payload=b"not the pinned installer")

    assert helper.main() == 0  # eSim's own install must still finish
    assert not any(c[0] == "OllamaSetup.exe" for c in m.commands)
    assert _pulled(m) == []
    assert "sha256" in capsys.readouterr().out.lower()
    assert not (tmp_path / "OllamaSetup.exe").exists()


def test_server_is_started_for_the_download_and_stopped_after(machine):
    m = machine(server_up=False)

    assert helper.main() == 0
    assert m.started == [m.ollama]
    assert m.stopped == ["server"]
    assert _pulled(m) == list(REQUIRED_MODELS)


def test_a_failed_model_download_does_not_stop_the_rest(machine, capsys):
    m = machine(failing_pulls={REQUIRED_MODELS[0]})

    assert helper.main() == 0
    assert _pulled(m) == list(REQUIRED_MODELS)
    assert REQUIRED_MODELS[0] in capsys.readouterr().out


def test_unexpected_error_still_lets_the_install_finish(machine, monkeypatch, capsys):
    machine()

    def boom():
        raise OSError("disk full")
    monkeypatch.setattr(helper, "find_ollama", boom)

    assert helper.main() == 0
    assert "disk full" in capsys.readouterr().out


def test_real_download_and_hash_check_against_a_local_server(tmp_path, monkeypatch):
    # The real download() and hash check, served locally instead of GitHub.
    import http.server
    import threading

    payload = os.urandom(3 * (1 << 20) + 17)      # multi-chunk, odd size
    (tmp_path / "srv").mkdir()
    (tmp_path / "srv" / "OllamaSetup.exe").write_bytes(payload)
    handler = lambda *a, **k: http.server.SimpleHTTPRequestHandler(
        *a, directory=str(tmp_path / "srv"), **k)
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        monkeypatch.setattr(helper, "TEMP_DIR", str(tmp_path))
        monkeypatch.setattr(helper, "OLLAMA_SETUP", {
            "url": "http://127.0.0.1:%d/OllamaSetup.exe" % server.server_port,
            "filename": "OllamaSetup.exe",
            "sha256": hashlib.sha256(payload).hexdigest(),
        })
        ran = []
        monkeypatch.setattr(helper, "run", lambda cmd: ran.append(cmd) or 0)
        monkeypatch.setattr(helper, "find_ollama", lambda: "ollama.exe" if ran else None)

        assert helper.install_ollama() == "ollama.exe"
        assert ran and ran[0][0] == str(tmp_path / "OllamaSetup.exe")
        assert not (tmp_path / "OllamaSetup.exe").exists()
    finally:
        server.shutdown()
