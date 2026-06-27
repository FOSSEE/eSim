# eSim Flatpak Configuration Details (README2)

This document outlines the modifications made to successfully build the eSim Flatpak package, its known limitations, and the necessary commands to build and run it.

## 🛠️ Changes Made for Flatpak Compatibility

To ensure the eSim Flatpak package builds and installs correctly on modern Linux distributions, several adjustments were made to the `org.fossee.eSim.yml` manifest:

1. **Fixed Ngspice URL and Checksum**: 
   - The previous `ngspice-45.2` source URL was broken (returned HTTP 404). 
   - Upgraded to **ngspice-46** (latest stable).
   - Added `dest-filename: ngspice-46.tar.gz` because the SourceForge redirect URL strips the filename, which previously caused `flatpak-builder` to throw an "Unknown archive format" error.

2. **Offline Python Dependency Installation**: 
   - *Problem*: The Flatpak build sandbox operates without network access, which causes live `pip install` commands to fail. 
   - *Solution*: All Python packages (and their transitive dependencies like `PyQt5-sip`, `PyQt5-Qt5`, `contourpy`, `cycler`, etc.) were pre-declared as `file` sources in the manifest. We used direct PyPI URLs and validated SHA256 hashes for each `.whl` file.
   - Updated the build command to install completely offline: `pip3 install --no-index --find-links=wheels --prefix=/app`.

3. **Removed `hdlparse` Dependency**:
   - `hdlparse` uses a deprecated `setup.py` option (`use_2to3`) that was removed in newer versions of setuptools. It fundamentally fails to install on **Python 3.12** (which is shipped with the `org.freedesktop.Sdk//24.08` SDK).
   - Consequently, `hdlparse` was omitted from the build, and the eSim Python codebase (`Maker.py` & `ModelGeneration.py`) was patched with a `try/except` block to gracefully handle its absence without crashing the application.

4. **Upgraded to PyQt6**:
   - The eSim GUI codebase was updated by upstream to use **PyQt6**. The Flatpak manifest was subsequently updated to download and bundle `PyQt6`, `PyQt6-Qt6`, and `PyQt6-sip` wheels instead of the older `PyQt5`.

5. **KiCad Host Sandbox Escape (`flatpak-spawn`)**:
   - To launch KiCad from within the eSim sandbox, eSim was updated to use `flatpak-spawn --host flatpak run org.kicad.KiCad`. The Flatpak manifest was granted the necessary D-Bus permission (`--talk-name=org.freedesktop.Flatpak`) to allow this host execution.

## ⚠️ Known Limitations

Because of the restricted sandbox environment and library incompatibilities, the Flatpak version of eSim has the following limitations:

1. **NGHDL is Unsupported**: Since `hdlparse` was removed (and due to the massive complexity of building the `ghdl` Ada compiler inside a Flatpak), the Verilog/Modelica digital modeling tool (NGHDL) will not work. 
2. **KiCad Symbol Creation Restricted**: The sandbox restricts write access to system-level KiCad directories.
3. **No External Terminals**: Features that require an external host terminal (like `xterm` for `gaw` waveform viewing) are not included.

*(Note: If you require full feature parity, especially for NGHDL or mixed-signal SKY130 workflows, it is highly recommended to use the native Ubuntu installer instead of Flatpak).*

## 🚀 How to Build and Run

### 1. Prerequisites
Ensure you have Flatpak and Flatpak-Builder installed on your system. You also **must** install the Flatpak version of KiCad, as eSim automatically looks for it to handle schematic design:

```bash
flatpak install flathub org.kicad.KiCad
```

### 2. Build the Package
Navigate to the root directory of the eSim project and run the following command to build and install the package locally:

```bash
flatpak-builder build flatpak/org.fossee.eSim.yml --install --user --force-clean
```
*(The `--force-clean` flag ensures a fresh build without stale cache files).*

### 3. Run eSim
Once the build is successful, launch the application with:

```bash
flatpak run org.fossee.eSim
```
