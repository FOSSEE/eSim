"""The installer's optional eSim AI Assistant step (installChatbot).

The real function is carved out of install-eSim.sh and run under bash with
pip, ollama, curl and sudo replaced by recording stubs, so nothing is
installed or downloaded. Needs bash >= 4 (any supported Ubuntu).
"""

import ast
import os
import re
import stat
import subprocess
import textwrap

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
INSTALLER = os.path.join(REPO, "Ubuntu", "install-eSim.sh")
CHATBOT_THREAD = os.path.join(REPO, "src", "chatbot", "chatbot_thread.py")


def _installer():
    with open(INSTALLER, encoding="utf-8") as f:
        return f.read()


def _function(name):
    match = re.search(r"^%s\(\) \{\n.*?^\}\n" % name, _installer(), re.S | re.M)
    assert match, "%s() not found in install-eSim.sh" % name
    return match.group(0)


def _installer_models():
    match = re.search(r"^CHATBOT_MODELS=\(([^)]*)\)", _installer(), re.M)
    assert match, "CHATBOT_MODELS not found in install-eSim.sh"
    return re.findall(r'"([^"]+)"', match.group(1))


def _required_models():
    tree = ast.parse(open(CHATBOT_THREAD, encoding="utf-8").read())
    for node in tree.body:
        if (isinstance(node, ast.Assign)
                and getattr(node.targets[0], "id", None) == "REQUIRED_MODELS"):
            return ast.literal_eval(node.value)
    raise AssertionError("REQUIRED_MODELS not found in chatbot_thread.py")


def test_installer_pulls_exactly_the_models_the_chat_window_requires():
    # The chat window downloads any missing REQUIRED_MODELS on first start;
    # pulling the same list at install time is what avoids that surprise.
    assert _installer_models() == _required_models()


def test_step_runs_after_the_virtualenv_and_before_the_launcher():
    steps = re.findall(r'^\s+"(\w+):', _installer().split("INSTALL_STEPS=(")[1]
                       .split(")")[0], re.M)
    assert "installChatbot" in steps
    assert steps.index("installDependency") < steps.index("installChatbot") \
        < steps.index("createDesktopStartScript")


def test_uninstall_leaves_ollama_alone():
    # Ollama and its models may serve other applications on the machine:
    # the uninstaller may mention them, but must never act on them.
    lines = [l.strip() for l in _function("uninstall_eSim").splitlines()
             if "ollama" in l.lower()]
    assert lines and all(l.startswith("log ") for l in lines)


def _stub(path, body):
    with open(path, "w") as f:
        f.write("#!/bin/bash\n" + body + "\n")
    os.chmod(path, os.stat(path).st_mode | stat.S_IEXEC)


@pytest.fixture
def run_step(tmp_path):
    """Run installChatbot with an answer; return (exit code, output, calls)."""
    def run(answer, ollama_installed=True, server_up=True, fail=()):
        bin_dir = tmp_path / "bin"
        bin_dir.mkdir(exist_ok=True)
        calls = tmp_path / "calls.log"
        calls.write_text("")
        rec = 'echo "$(basename "$0") $*" >> "%s"' % calls
        failing = lambda tool: "exit 1" if tool in fail else "exit 0"
        _stub(bin_dir / "pip", rec + "\n" + failing("pip"))
        _stub(bin_dir / "sudo", rec + '\n"$@"')
        _stub(bin_dir / "apt-get", rec + "\n" + failing("apt-get"))
        _stub(bin_dir / "curl", rec + '\necho "echo ollama-installer-ran"\n'
              + failing("curl"))
        if ollama_installed:
            served = tmp_path / "served"
            _stub(bin_dir / "ollama", rec + textwrap.dedent('''
                case "$1" in
                  list) %s ;;
                  serve) touch "%s"; exec sleep 30 ;;
                  pull) %s ;;
                esac''' % ("exit 0" if server_up else '[ -f "%s" ]' % served,
                           served, failing("ollama pull"))))
        env_dir = tmp_path / "config" / "env" / "bin"
        env_dir.mkdir(parents=True, exist_ok=True)
        (env_dir / "activate").write_text("")
        (tmp_path / "requirements-copilot.txt").write_text(
            "# comment\n\nollama>=0.3\nSpeechRecognition>=3.10\n")

        script = "\n".join([
            'log()  { echo "LOG $*"; }',
            'warn() { echo "WARN $*"; }',
            'error_exit() { echo "ERR-TRAP"; exit 99; }',
            re.search(r"^CHATBOT_MODELS=\([^)]*\)", _installer(), re.M).group(0),
            'config_dir="%s"' % (tmp_path / "config"),
            'eSim_Home="%s"' % tmp_path,
            _function("installChatbot"),
            "set -e; set -E; trap error_exit ERR",
            "installChatbot",
            'echo "STEP-RETURNED"',
            'trap -p ERR | grep -q error_exit && echo "TRAP-RESTORED"',
            'case $- in *e*) echo "ERREXIT-RESTORED";; esac',
        ])
        proc = subprocess.run(
            ["bash", "-c", script], input=answer + "\n", text=True,
            capture_output=True, timeout=60,
            env={"PATH": "%s:/usr/bin:/bin" % bin_dir, "HOME": str(tmp_path)})
        return proc.returncode, proc.stdout + proc.stderr, calls.read_text()
    return run


def test_declining_installs_nothing(run_step):
    code, out, calls = run_step("n")

    assert code == 0 and "STEP-RETURNED" in out
    assert calls == ""


def test_accepting_installs_packages_and_models(run_step):
    code, out, calls = run_step("y")

    assert code == 0 and "STEP-RETURNED" in out
    # One guarded pip call per requirements-copilot.txt entry (the repo-wide
    # rule in windows/tests/test_packaging_pins.py), comments skipped.
    assert re.findall(r"^pip install (.*)$", calls, re.M) == \
        ["ollama>=0.3", "SpeechRecognition>=3.10"]
    for model in _required_models():
        assert "ollama pull %s" % model in calls
    assert "curl" not in calls  # Ollama already present


def test_missing_ollama_is_installed_with_its_official_script(run_step):
    code, out, calls = run_step("y", ollama_installed=False)

    assert code == 0 and "STEP-RETURNED" in out
    assert "curl -fsSL https://ollama.com/install.sh" in calls
    assert "ollama-installer-ran" in out
    # Ollama's installer unpacks a .tar.zst and aborts without zstd, which a
    # fresh Ubuntu 26.04 lacks (found by a full --install in a clean system).
    apt = re.findall(r"^apt-get install -y (.*)$", calls.split("curl -fsSL")[0], re.M)
    assert apt and {"curl", "zstd"} <= set(apt[-1].split())


def test_server_is_started_for_the_download_when_not_running(run_step):
    # No systemd (containers, WSL): the official installer cannot start the
    # service, so the step runs a temporary server just for the pulls.
    code, out, calls = run_step("y", server_up=False)

    assert code == 0 and "STEP-RETURNED" in out
    assert "ollama serve" in calls


@pytest.mark.parametrize("broken", ["pip", "curl", "ollama pull"])
def test_a_failed_download_warns_and_the_install_continues(run_step, broken):
    code, out, calls = run_step(
        "y", ollama_installed=(broken != "curl"), fail=(broken,))

    assert code == 0
    assert "WARN" in out
    assert "ERR-TRAP" not in out
    assert "STEP-RETURNED" in out
    assert "TRAP-RESTORED" in out and "ERREXIT-RESTORED" in out
