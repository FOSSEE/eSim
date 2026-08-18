# eSim Universal AppImage Builder

[![Build Status](https://img.shields.io/badge/build-automated-success.svg)](https://github.com/mahakgupta0123/eSim_Universal_packagemanager_linux)
[![Platform](https://img.shields.io/badge/platform-Linux%20x86__64-blue.svg)](https://www.linux.org/)
[![License](https://img.shields.io/badge/License-GPL%20v3-red.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Distros](https://img.shields.io/badge/distros-Ubuntu%20%7C%20Fedora%20%7C%20Arch%20%7C%20openSUSE-orange.svg)](#-supported-distributions)

A comprehensive, automated build system for creating a **Universal AppImage** of [eSim](https://esim.fossee.in/) — an open-source EDA tool for circuit design, simulation, analysis, and PCB design developed by the [FOSSEE](https://fossee.in/) initiative at IIT Bombay.

This project solves the "dependency hell" problem on Linux by bundling eSim and all its complex requirements into a **single, portable executable** that works across virtually all modern Linux distributions — no installation required.

---

## 🚀 Key Features

- **True Multi-Distro Compatibility** — Automatically detects and handles dependencies for:
  - **Ubuntu / Debian / Linux Mint** (`apt`)
  - **Fedora / RHEL / CentOS** (`dnf` / `yum`)
  - **Arch Linux / Manjaro** (`pacman`)
  - **openSUSE** (`zypper`)

- **Bundled Tool Suite**:
  - **eSim 2.5** — Latest stable EDA suite with schematic capture, simulation, and PCB design
  - **KiCad 6.0.11** — Bundled via AppImage for perfect compatibility and isolation
  - **NgSpice 35** — Custom-built from source with specialized patches for NGHDL/GHDL integration, clean termination, and Arch compatibility
  - **OpenModelica / OMEdit** — Modelica-based modeling and simulation environment
  - **GHDL** — Open-source VHDL simulator for NGHDL digital models
  - **Verilator** — Fast Verilog HDL simulator for NgVeri integration
  - **Makerchip** — Built-in support for Makerchip IDE integration

- **Zero Configuration** — Automatically sets up Python virtual environments, GTK resources, library paths, and runtime dependencies inside the AppImage

- **Cross-Distribution Library Bundling** — Intelligent fallback system that downloads Ubuntu `.deb` packages for libraries not available on non-Ubuntu systems (OpenSceneGraph, Qt5WebKit, ICU, omniORB)

---

## 📋 Prerequisites

Before running the builder, ensure you have:

1. **A Linux machine** (x86_64 architecture)
2. **Sudo privileges** (for installing build tools like `gcc`, `wget`, `python3`, etc.)
3. **Internet connection** — The script downloads several hundred MB of sources and tools
4. **Disk space** — At least **5 GB** of free space for the build process
5. **Basic build tools** — The script will install anything missing, but having `git`, `gcc`, and `wget` pre-installed speeds things up

---

## 🛠️ Build Instructions

Creating your universal AppImage is as simple as running one command:

### 1. Clone the Repository
```bash
git clone https://github.com/mahakgupta0123/eSim_Universal_packagemanager_linux.git
cd eSim_Universal_packagemanager_linux
```

### 2. Make the Script Executable
```bash
chmod +x build-appimage.sh
```

### 3. Run the Builder
```bash
./build-appimage.sh
```

The script proceeds through **10 automated stages**:

| Stage | Description |
|-------|-------------|
| 1 | Distribution detection & system checks |
| 2 | Prerequisite & dependency installation |
| 3 | Tool downloading (KiCad AppImage, OpenModelica, etc.) |
| 4 | eSim source preparation & patching |
| 5 | NgSpice compilation from source (with GHDL patches) |
| 6 | Verilator setup & compilation |
| 7 | Python environment & package installation |
| 8 | GTK resource bundling (icons, themes, schemas) |
| 9 | KiCad & OMEdit library bundling |
| 10 | AppImage creation & packaging |

---

## 🖥️ Usage

Once the build is complete, you will find `eSim-2.5.AppImage` (~625 MB) in the `build-eSim-AppImage/` directory.

### Running the AppImage
```bash
./build-eSim-AppImage/eSim-2.5.AppImage
```

> [!TIP]
> You can copy this single file to **any other Linux distribution** and it will run without needing to install eSim's complex dependency tree!

### What's Included
When you launch the AppImage, you get access to:
- **eSim** — Main schematic/simulation GUI
- **KiCad** — Schematic & PCB editor (launched from within eSim)
- **OMEdit** — OpenModelica editor for Modelica models
- **NgSpice** — Circuit simulation engine (runs automatically from eSim)
- **NGHDL** — VHDL digital model integration
- **NgVeri** — Verilog digital model integration via Verilator

---

## 🐧 Supported Distributions

| Distribution | Package Manager | Status |
|-------------|----------------|--------|
| Ubuntu 20.04+ | `apt` | ✅ Fully tested |
| Debian 11+ | `apt` | ✅ Fully tested |
| Linux Mint 21+ | `apt` | ✅ Fully tested |
| Fedora 38+ | `dnf` | ✅ Fully tested |
| Arch Linux | `pacman` | ✅ Fully tested |
| Manjaro | `pacman` | ✅ Fully tested |
| openSUSE Leap/Tumbleweed | `zypper` | ✅ Supported |
| RHEL / CentOS 8+ | `dnf` / `yum` | ✅ Supported |

> [!NOTE]
> The **build** can be performed on any supported distribution. The resulting AppImage is portable and can **run** on any x86_64 Linux distribution with FUSE support.

---

## 🔧 Troubleshooting

### FUSE Error (Ubuntu 22.04+)
If the AppImage fails to run with a message about FUSE:
```bash
sudo apt update && sudo apt install libfuse2
```

### OMEdit Not Opening
If OMEdit fails to launch, it's usually a missing Qt5 library. The builder automatically handles this by:
- Bundling Ubuntu `.deb` libraries for OpenSceneGraph, Qt5WebKit, ICU, and omniORB
- Installing native Qt5 modules (`qt5-declarative`, `qt5-sensors`, `qt5-location`) during the build

To manually check: run `ldd eSim.AppDir/usr/bin/OMEdit.bin | grep "not found"` inside the build directory.

### Qt / Wayland Display Issues
The AppImage automatically detects Wayland and X11 sessions and handles setting `QT_QPA_PLATFORM` and prioritizing bundled PyQt5 libraries. However, if you experience display initialization errors, you can force a platform by prepending the environment variable:
```bash
# Force X11 compatibility mode
QT_QPA_PLATFORM=xcb ./eSim-2.5.AppImage

# Force Wayland native mode
QT_QPA_PLATFORM=wayland ./eSim-2.5.AppImage
```

### Build Failures
Common causes:
- **Interrupted internet** during large downloads (KiCad AppImage is ~600 MB)
- **Missing disk space** (at least 5 GB required)
- **Unsupported architecture** (only x86_64 is currently supported)

For details on past issues faced and how they were resolved, see:
- [appimage_issues.md](file:///home/ashu/Downloads/eSim_packagemanager/appimage/appimage_issues.md) — Documentation of error logs and root causes.
- [appimage_fix_implementation.md](file:///home/ashu/Downloads/eSim_packagemanager/appimage/appimage_fix_implementation.md) — Technical details of the python bundling and library isolation fixes.

---

## 📁 Project Structure

```
eSim_Universal_packagemanager_linux/
├── build-appimage.sh            # Main build script (~7800 lines)
├── README.md                    # This file
├── appimage_issues.md           # Documentation of errors and issues faced
├── appimage_fix_implementation.md # Technical details of the fixes implemented
└── build-eSim-AppImage/         # Created during build
    ├── downloads/               # Downloaded tools & dependencies
    ├── eSim.AppDir/             # AppImage filesystem
    │   ├── AppRun               # Entry point launcher (Wayland/X11 & Python wrapper)
    │   ├── usr/
    │   │   ├── bin/             # eSim, KiCad, OMEdit, NgSpice binaries
    │   │   ├── lib/             # Bundled shared libraries
    │   │   ├── python/          # Standalone bundled CPython 3.12 environment
    │   │   └── share/           # eSim source, resources, models
    │   └── ...
    └── eSim-2.5.AppImage        # Final portable AppImage
```

---

## 🏗️ Architecture & Design

The build system uses a **layered approach** to handle cross-distribution compatibility:

1. **Detection Layer** — Identifies the host distro and package manager
2. **Dependency Layer** — Installs build-time and runtime dependencies using the native package manager
3. **Compilation Layer** — Builds NgSpice from source with custom patches; compiles Verilator object files
4. **Bundling Layer** — Copies all binaries, libraries, Python packages, GTK resources, and KiCad into the AppDir
5. **Fallback Layer** — For libraries not available on the host system (e.g., OMEdit's Ubuntu-specific dependencies), downloads `.deb` packages from Ubuntu archives and extracts the needed `.so` files
6. **Packaging Layer** — Creates the final AppImage using `appimagetool`

---

## 📜 License

This project is part of the [FOSSEE](https://fossee.in/) initiative at IIT Bombay and follows the licensing of the bundled tools (primarily GPL v3). See the individual component headers for details.

---

*Developed for the eSim Community to provide a seamless simulation experience on Linux.*
