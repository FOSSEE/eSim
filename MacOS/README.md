# eSim macOS Installer

A macOS installer for [eSim](https://esim.fossee.in/) — an open-source Electronic Design Automation (EDA) tool developed by FOSSEE, IIT Bombay. This project packages eSim and all its dependencies into a self-contained `.app` bundle distributed as a `.pkg` installer for macOS.

> **Capstone Project** — Developed by Thet Htar Shwe Sin (2018-MIIT-CSE-052) during internship at FOSSEE, IIT Bombay, under the supervision of Prof. Prabhu Ramachandran and Mr. Sumanto Kar.

---

## Features

- One-click `.pkg` installer — no Homebrew or manual setup required
- Self-contained `.app` bundle with all dependencies (Ngspice, Python, Qt, XQuartz)
- XQuartz/X11 dylib relinking using `@loader_path`
- Automatic environment setup via pre/post-install scripts
- Configuration directories created at install: `~/.esim/` and `~/.nghdl/`
- Tested on Apple Silicon arm64 (Virtual Machine)

---

## Requirements

- macOS 13 (Ventura) or later
- [XQuartz](https://www.xquartz.org/) installed (required for display)
- Apple Silicon (ARM64) or Intel (x86_64)

---

## Installation

The final `.pkg` installer is available via Google Drive (shared to supervisor).

1. Download `eSim.pkg` from the shared Google Drive
2. Double-click `eSim.pkg`
3. Follow the on-screen installation steps
4. Launch eSim from `/Applications/eSim.app`

> Make sure XQuartz is installed and running before launching eSim.

---

## Building from Source

If you want to build the installer yourself, follow the steps below in order.

### Prerequisites

- macOS with Xcode Command Line Tools
- Python 3.10+
- Qt 6
- CMake

### Step 1 — Build Dependencies & Set Up Virtual Environment

```bash
chmod +x build_esim.sh
./build_esim.sh
```

This script:

- Builds Ngspice 35 with X11/XQuartz support
- Installs required Python packages into a virtual environment
- Compiles and prepares all binary dependencies

---

### Step 2 — Bundle as `.app` Using PyInstaller

```bash
chmod +x bundle_esim.sh
./bundle_esim.sh
```

This script:

- Uses PyInstaller with `eSim.spec` to bundle the app
- Relinks XQuartz dylibs using `@loader_path` via `relink_ngspice.sh`
- Produces `eSim.app` inside the `dist/` folder

---

### Step 3 — Create the `.pkg` Installer

```bash
chmod +x create_pkg.sh
./create_pkg.sh
```

This script:

- Packages `eSim.app` using `pkgbuild`
- Includes `preinstall` and `postinstall` scripts for environment setup
- Produces the final `eSim.pkg` installer ready for distribution

---

## Project Structure

```
eSim-macOS-Installer/
├── build_esim.sh          # Step 1: Build dependencies and virtual env
├── bundle_esim.sh         # Step 2: Bundle app using PyInstaller
├── create_pkg.sh          # Step 3: Create .pkg installer
├── relink_ngspice.sh      # Relink XQuartz dylibs using @loader_path
├── eSim.spec              # PyInstaller spec file
├── eSimIcon.icns          # macOS app icon
├── bundled_spinit         # Ngspice init script bundled with app
├── scripts/               # Pre/post-install scripts for pkg
├── src/                   # eSim Python source (macOS-modified)
├── nghdl/                 # NGHDL source
├── library/               # KiCad symbol libraries
├── Examples/              # Example circuit files
└── images/                # UI images and assets
```

---

## Acknowledgements

- **Prof. Prabhu Ramachandran** — Principal Investigator, FOSSEE, IIT Bombay
- **Mr. Sumanto Kar** — Technical Mentor, FOSSEE, IIT Bombay
- **Dr. May Mya Aung** — Internal Supervisor, MIIT
- [FOSSEE Team](https://fossee.in/) for the original eSim codebase

---

## License

This project is based on [eSim](https://github.com/FOSSEE/eSim) which is licensed under the GNU GPL v3. See [LICENSE](LICENSE) for details.
