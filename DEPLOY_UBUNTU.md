# Deploy eSim Copilot on Ubuntu (VM or WSL2)

Use this guide for **first-time deployment** of the AI chatbot on a Linux environment.

---

## VM setup checklist (Option A)

| Step | Action |
|------|--------|
| 1 | Download [Ubuntu 22.04 Desktop](https://ubuntu.com/download/desktop) ISO |
| 2 | Create VM (VirtualBox/Hyper-V/VMware): 4–8 GB RAM, 25 GB disk |
| 3 | Install Ubuntu in VM, install Guest Additions (VirtualBox) if using shared folder |
| 4 | Copy eSim into VM (shared folder or zip) → `~/work/eSim` |
| 5 | Run `./scripts/setup_copilot_ubuntu.sh` |
| 6 | Start `ollama serve` in a second terminal |
| 7 | Run `python ingest.py` (optional) |
| 8 | Launch: `QT_QPA_PLATFORM=xcb python Application.py` from `src/frontEnd` |

---

## Option A: Ubuntu VM (recommended for full GUI)

### 1. Create Ubuntu VM

#### 1a. Download Ubuntu 22.04 Desktop

- Go to [ubuntu.com/download/desktop](https://ubuntu.com/download/desktop)
- Download **Ubuntu 22.04 LTS** (64-bit, ~4 GB ISO)

#### 1b. Choose your hypervisor

| Tool | Steps |
|------|-------|
| **VirtualBox** (free) | 1. Install [VirtualBox](https://www.virtualbox.org/wiki/Downloads)<br>2. New VM → Name: `eSim-Ubuntu`, Type: Linux, Version: Ubuntu (64-bit)<br>3. RAM: **4096 MB** (minimum), **8192 MB** recommended for Ollama<br>4. Create virtual disk: **VDI**, **Dynamically allocated**, **25 GB**<br>5. Settings → Storage → Empty → Choose Ubuntu ISO<br>6. Start VM → Install Ubuntu (normal install, minimal if offered) |
| **Hyper-V** (Windows Pro) | 1. Enable Hyper-V: `OptionalFeatures` → check Hyper-V<br>2. Hyper-V Manager → New → Virtual Machine<br>3. Generation 2, 4096 MB RAM, 25 GB disk<br>4. Connect to Ubuntu ISO, boot and install |
| **VMware Workstation** | Same as VirtualBox: New VM → Typical → Ubuntu ISO → 4 GB RAM, 25 GB disk |

**Important:** Allocate at least **4 GB RAM**; 8 GB is better if you run Ollama models inside the VM.

---

### 2. Get the code into Ubuntu

#### Option 2a – Copy from Windows (shared folder or zip)

**Using VirtualBox shared folder:**

1. In VirtualBox: VM Settings → Shared Folders → Add
2. Folder path: `C:\Users\91900\Downloads\eSIM-Software-AIChatBot\repos`
3. Folder name: `repos` (or `esim_repo`)
4. Check **Auto-mount**, **Make permanent**
5. Inside Ubuntu VM, install Guest Additions (Devices → Insert Guest Additions CD, then run it)
6. Add your user to `vboxsf`: `sudo usermod -aG vboxsf $USER` → log out and back in
7. Copy eSim into your home:
   ```bash
   mkdir -p ~/work
   cp -r /media/sf_repos/eSim ~/work/eSim
   cd ~/work/eSim
   git checkout Chatbot_Enhancements
   ```

**Using zip (no shared folder):**

1. On Windows, zip the folder:
   - Right-click `repos\eSim` → Send to → Compressed folder
   - Or in PowerShell (from workspace root): `.\repos\eSim\scripts\zip_for_vm.ps1` → creates `eSim-for-VM.zip`
2. Copy `eSim-for-VM.zip` into the VM (drag-drop, USB, or network share)
3. Inside Ubuntu:
   ```bash
   mkdir -p ~/work && cd ~/work
   unzip /path/to/eSim-for-VM.zip   # e.g. unzip ~/Downloads/eSim-for-VM.zip
   cd eSim
   git checkout Chatbot_Enhancements
   ```

#### Option 2b – Clone from GitHub (if Chatbot_Enhancements is on your fork)

```bash
sudo apt update && sudo apt install -y git
mkdir -p ~/work && cd ~/work
git clone https://github.com/FOSSEE/eSim.git
cd eSim
git fetch origin pull/434/head:pr-434
git checkout -b Chatbot_Enhancements pr-434
# If you pushed Chatbot_Enhancements to your fork:
# git remote add myfork https://github.com/YOUR_USER/eSim.git
# git fetch myfork Chatbot_Enhancements
# git checkout Chatbot_Enhancements
```

---

### 3. Run one-command setup

```bash
cd ~/work/eSim
chmod +x scripts/setup_copilot_ubuntu.sh
./scripts/setup_copilot_ubuntu.sh
```

This installs system packages, Python venv, Ollama, models (qwen2.5:3b, minicpm-v, nomic-embed-text), and Vosk. It may take 15–30 minutes depending on your connection.

---

### 4. Start Ollama (keep running in a separate terminal)

Open a **new terminal** and run:

```bash
ollama serve
```

Leave this running. The Copilot needs Ollama to answer questions.

---

### 5. Ingest manuals for RAG (optional but recommended)

```bash
cd ~/work/eSim
source .venv/bin/activate
cd src
python ingest.py
```

Add `.txt` manuals to `src/manuals/` first if you have them; otherwise ingest may find nothing (RAG will still work, but with less context).

---

### 6. Launch eSim with Copilot

```bash
cd ~/work/eSim
source .venv/bin/activate
cd src/frontEnd
QT_QPA_PLATFORM=xcb python Application.py
```

Click the **eSim Copilot** button in the toolbar to open the AI chat.

---

### Quick copy-paste (after VM is ready and code is in ~/work/eSim)

```bash
cd ~/work/eSim && git checkout Chatbot_Enhancements
chmod +x scripts/setup_copilot_ubuntu.sh && ./scripts/setup_copilot_ubuntu.sh
# When done: open a second terminal and run: ollama serve
# Then in first terminal:
source .venv/bin/activate && cd src && python ingest.py
cd ~/work/eSim && source .venv/bin/activate && cd src/frontEnd && QT_QPA_PLATFORM=xcb python Application.py
```

---

## Option B: WSL2 (Windows Subsystem for Linux)

### 1. Install WSL2 + Ubuntu

In **PowerShell (Admin)**:

```powershell
wsl --install
wsl --set-default-version 2
wsl --install -d Ubuntu-22.04
```

Reboot if prompted, then open **Ubuntu 22.04** from Start.

### 2. Follow steps 2–5 from Option A

All commands are the same inside the Ubuntu terminal.

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| "Ollama not responding" | Run `ollama serve` in a separate terminal before launching eSim |
| GUI doesn't appear (WSL) | Ensure you use the Ubuntu app (not SSH). WSLg provides display automatically |
| Voice input fails | Microphone passthrough in WSL can be unreliable; text + image + netlist still work |
| `python ingest.py` finds no files | Add `.txt` manuals to `src/manuals/` before running ingest |

---

## Branch: Chatbot_Enhancements

This deployment uses the `Chatbot_Enhancements` branch, based on Hariom's PR 434, with:

- Seamless install script for Ubuntu
- User-writable ChromaDB path
- Optional speech-to-text (graceful fallback if Vosk missing)
- Split requirements (base + copilot)
