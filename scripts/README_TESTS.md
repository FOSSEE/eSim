# Copilot Enhancement Tests

Run these tests on the Ubuntu VM after activating the venv.

## Copy Updated Code to VM

From your **local machine** (Windows), sync the updated code to the Ubuntu VM:

### Automated: deploy_to_vm.ps1 (recommended)

```powershell
# First time: copy template (if needed) and edit VM_HOST, VM_USER
copy scripts\deploy_to_vm.ps1.example scripts\deploy_to_vm.ps1   # if deploy_to_vm.ps1 doesn't exist

# Run from eSim repo root:
.\scripts\deploy_to_vm.ps1
```

This script syncs `src` and `scripts` via SCP, stops any running eSim on the VM, and prints the final step to run in MobaXterm. (`deploy_to_vm.ps1` is in `.gitignore`.)

### Manual options

### Option A: rsync (recommended)

```powershell
# From eSim repo root on local machine
cd <path-to-eSim-repo>
rsync -avz --exclude ".venv" --exclude "__pycache__" --exclude ".git" . harvi@192.168.29.208:~/work/eSim/
```

### Option B: scp (specific files/folders)

```powershell
# Copy entire src and scripts
scp -r src scripts harvi@192.168.29.208:~/work/eSim/

# Or copy only changed files
scp src/chatbot/knowledge_base.py src/chatbot/image_handler.py src/frontEnd/Chatbot.py harvi@192.168.29.208:~/work/eSim/src/
scp -r scripts harvi@192.168.29.208:~/work/eSim/
```

### Option C: Git (if both sides use the same repo)

```bash
# On local: commit and push
git add -A && git commit -m "Copilot enhancements" && git push

# On VM: pull
ssh harvi@192.168.29.208 "cd ~/work/eSim && git pull"
```

**Note:** Replace `192.168.29.208` and `harvi` if your VM uses different IP/user. On Windows, `scp` is available with OpenSSH; for `rsync`, use WSL or install via Git for Windows.

---

## Prerequisites

- Ubuntu VM (e.g. 192.168.29.208, user `harvi`)
- Repo at `~/work/eSim`
- Virtual environment with dependencies: `source .venv/bin/activate`
- Optional: `ollama serve` running for Ollama connectivity test
- Optional: RAG ingest run (`cd src && python ingest.py`) for RAG test

## Run Tests

### Option 1: Python script (recommended)

```bash
cd ~/work/eSim
source .venv/bin/activate
python scripts/test_copilot_enhancements.py
```

### Option 2: Shell script

```bash
cd ~/work/eSim
chmod +x scripts/test_copilot_enhancements.sh
./scripts/test_copilot_enhancements.sh
```

## What Is Tested

| Test | Description |
|------|-------------|
| Netlist contract | Contract loads from one of the bundled paths |
| RAG relevance | `search_knowledge()` filters by relevance threshold |
| PaddleOCR | `image_handler` imports; `HAS_PADDLE` set |
| Copy button | `ChatbotGUI.copy_last_response` exists |
| Ollama | Optional: Ollama responds to a short prompt |

## Expected Output

- `[PASS]` – test succeeded
- `[SKIP]` – test skipped (e.g. RAG empty if ingest not run)
- `[WARN]` – non-blocking (e.g. Ollama not running)
- `[FAIL]` – test failed (investigate)
