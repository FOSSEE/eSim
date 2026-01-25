# eSim Docker

<p align="center">
  <img src="assets/esim_logo.png" alt="eSim Logo" width="80"/>
  <img src="assets/esim_text.png" alt="eSim" width="200"/>
</p>

<p align="center">
  <b>Run eSim anywhere using Docker - No installation required!</b>
</p>

<p align="center">
  <a href="../../releases/latest">Download Launcher</a> •
  <a href="#quick-start">Quick Start</a> •# eSim Docker

<p align="center">
  <img src="assets/esim_logo.png" alt="eSim Logo" width="80"/>
  <img src="assets/esim_text.png" alt="eSim" width="200"/>
</p>

<p align="center">
  <b>Run eSim anywhere using Docker - No installation required!</b>
</p>

<p align="center">
  <a href="../../releases/latest">Download Launcher</a> •
  <a href="#quick-start">Quick Start</a> •
  <a href="#troubleshooting">Troubleshooting</a>
</p>

---

## About

This project provides a Docker-based solution to run **eSim** (Electronic Circuit Simulation) on any operating system. eSim is developed by FOSSEE, IIT Bombay and integrates KiCad, Ngspice, and Python for circuit design and simulation.

**What's included:**
- KiCad for schematic design
- Ngspice for SPICE simulation  
- GAW3 analog waveform viewer
- All eSim libraries pre-configured

---

## Quick Start

### Step 1: Get Docker

Download [Docker Desktop](https://www.docker.com/products/docker-desktop) and make sure it's running.

### Step 2: Download the Launcher

Go to [Releases](../../releases/latest) and download:
- Windows: `eSim-Launcher-Windows.exe`
- Linux: `eSim-Launcher-Linux`
- macOS: `eSim-Launcher-macOS`

### Step 3: Run it

**Windows:** Double-click the `.exe` file.

**Linux:** Open terminal and run:
```bash
chmod +x eSim-Launcher-Linux
./eSim-Launcher-Linux
```

**macOS:** Open terminal and run:
```bash
chmod +x eSim-Launcher-macOS
./eSim-Launcher-macOS
```

---

## Display Modes

The launcher offers two display modes:

| Mode | Best For | How it Works |
|------|----------|--------------|
| **VNC** | Windows, macOS | Opens eSim in your browser. Works everywhere, no setup needed. |
| **X11** | Linux | Opens eSim in a native window. Best performance on Linux. |

### Recommendations

- **Linux** → Use X11 mode (recommended, no lag)
- **Windows** → Use VNC mode (X11 works but KiCad may lag)
- **macOS** → Use VNC mode (X11 requires XQuartz)

Both modes work on all platforms - the launcher will guide you through any required setup.

---

## Command Line Usage

```bash
# Interactive menu
python run_esim_docker.py

# Direct VNC mode
python run_esim_docker.py --vnc

# Direct X11 mode  
python run_esim_docker.py --x11

# Update image
python run_esim_docker.py --pull
```

---

## Workspace

Your projects are saved to:

| OS | Location |
|----|----------|
| Windows | `C:\Users\<you>\eSim_Workspace` |
| Linux/macOS | `~/eSim_Workspace` |

This folder is mounted into the container, so your files persist.

---

## Troubleshooting

### Docker not running
Open Docker Desktop and wait for it to fully start.

### Browser shows "localhost not found"
Wait a few seconds and refresh. The container needs time to start.

### VNC shows blank screen
Refresh the browser page. If still blank, restart the launcher.

### X11 mode: window doesn't appear (Windows)
Make sure VcXsrv is running. The launcher auto-installs it if needed.

### X11 mode: window doesn't appear (macOS)
Install XQuartz from xquartz.org, then run `xhost +localhost` in terminal.

---

## Building from Source

```bash
docker build -t esim:latest .
python run_esim_docker.py --build
```

---

## Credits

- **eSim** - FOSSEE Team, IIT Bombay
- **KiCad** - KiCad Developers
- **Ngspice** - Ngspice Team
- **GAW3** - Hervé Quillévéré, Stefan Schippers

Created as part of the FOSSEE Internship program.

---

## License

GPL-3.0

  <a href="#troubleshooting">Troubleshooting</a>
</p>

---

## About

This project provides a Docker-based solution to run **eSim** (Electronic Circuit Simulation) on any operating system. eSim is developed by FOSSEE, IIT Bombay and integrates KiCad, Ngspice, and Python for circuit design and simulation.

**What's included:**
- KiCad for schematic design
- Ngspice for SPICE simulation  
- GAW3 analog waveform viewer
- All eSim libraries pre-configured

---

## Quick Start

### Step 1: Get Docker

Download [Docker Desktop](https://www.docker.com/products/docker-desktop) and make sure it's running.

### Step 2: Download the Launcher

Go to [Releases](../../releases/latest) and download:
- Windows: `eSim-Launcher-Windows.exe`
- Linux: `eSim-Launcher-Linux`
- macOS: `eSim-Launcher-macOS`

### Step 3: Run it

**Windows:** Double-click the `.exe` file.

**Linux:** Open terminal and run:
```bash
chmod +x eSim-Launcher-Linux
./eSim-Launcher-Linux
```

**macOS:** Open terminal and run:
```bash
chmod +x eSim-Launcher-macOS
./eSim-Launcher-macOS
```

---

## Display Modes

The launcher offers two display modes:

| Mode | Best For | How it Works |
|------|----------|--------------|
| **VNC** | Windows, macOS | Opens eSim in your browser. Works everywhere, no setup needed. |
| **X11** | Linux | Opens eSim in a native window. Best performance on Linux. |

### Recommendations

- **Linux** → Use X11 mode (recommended, no lag)
- **Windows** → Use VNC mode (X11 works but KiCad may lag)
- **macOS** → Use VNC mode (X11 requires XQuartz)

Both modes work on all platforms - the launcher will guide you through any required setup.

---

## Command Line Usage

```bash
# Interactive menu
python run_esim_docker.py

# Direct VNC mode
python run_esim_docker.py --vnc

# Direct X11 mode  
python run_esim_docker.py --x11

# Update image
python run_esim_docker.py --pull
```

---

## Workspace

Your projects are saved to:

| OS | Location |
|----|----------|
| Windows | `C:\Users\<you>\eSim_Workspace` |
| Linux/macOS | `~/eSim_Workspace` |

This folder is mounted into the container, so your files persist.

---

## Troubleshooting

### Docker not running
Open Docker Desktop and wait for it to fully start.

### Browser shows "localhost not found"
Wait a few seconds and refresh. The container needs time to start.

### VNC shows blank screen
Refresh the browser page. If still blank, restart the launcher.

### X11 mode: window doesn't appear (Windows)
Make sure VcXsrv is running. The launcher auto-installs it if needed.

### X11 mode: window doesn't appear (macOS)
Install XQuartz from xquartz.org, then run `xhost +localhost` in terminal.

---

## Building from Source

```bash
docker build -t esim:latest .
python run_esim_docker.py --build
```

---

## Credits

- **eSim** - FOSSEE Team, IIT Bombay
- **KiCad** - KiCad Developers
- **Ngspice** - Ngspice Team
- **GAW3** - Hervé Quillévéré, Stefan Schippers

Created as part of the FOSSEE Internship program.

---

## License

GPL-3.0
