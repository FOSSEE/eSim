# eSim Ubuntu 25.04 – Installer & Runtime Failure Analysis

**Author:** Vishal Soni  
**Platform:** Ubuntu 25.04 (Plucky Puffin)  
**Project:** eSim (FOSSEE, IIT Bombay)

This document contains a full forensic analysis of the eSim installation and runtime stack on Ubuntu 25.04. It documents the debugging methodology, root cause analysis, and permanent resolution for 13 distinct failures.

---

## 1. Executive Summary

| Metric | Value |
| :--- | :--- |
| **Total Defects Identified** | **13** |
| **Critical Blockers** | 3 (Installer, GHDL, KiCad) |
| **Resolution Rate** | 100% (All Fixed) |
| **Compatibility Status** | **Fully Verified** |

Although eSim installation is automated, the transition to the **Ubuntu 25.04** environment (featuring LLVM 20, Python 3.13, and stricter APT policies) caused significant compatibility breaks.

## 2. Debugging Methodology

To ensure a robust port, the following engineering methodologies were applied:
1.  **Forensic Log Analysis**: Traced compiler failure logs to identify the specific flag mismatches in the GHDL/LLVM 20 build process.
2.  **Dependency Tree Tracing**: Analyzed `apt` and `pip` dependency graphs to isolate deprecated libraries (e.g., `libcanberra`) and conflicting PPA repositories.
3.  **Runtime Environment Isolation**: Implemented Python Virtual Environments (`venv`) to decouple application dependencies from the system-managed Python 3.13 stack.
4.  **Static Logic Review**: Audited shell scripts to identify hard-coded version whitelists and relative path assumptions.

---

## System Environment

- **OS:** Ubuntu 25.04 (Plucky)
- **Kernel:** Linux 6.14
- **Python:** 3.13
- **LLVM:** 20 (default)

---

## BUG 1: 🔴 [CRITICAL] Ubuntu 25 blocked by installer
**Tags:** `[Bash]` `[Installer Logic]`

### Technical Root Cause Analysis
The installer utilizes a restrictive whitelist of supported OS versions. It lacks forward compatibility logic, causing an immediate abort on version "25.04".

### Operational Impact
**Blocker**: Prevents 100% of installations on the target OS.

### Resolution Strategy & Implementation
Map the new OS version to the existing, binary-compatible installation routine for Ubuntu 24.04.

#### Patch (install-eSim.sh)
```diff
- "24.04")
-    SCRIPT="$SCRIPT_DIR/install-eSim-24.04.sh"
-    ;;
+ "24.04"|"25.04")
+    SCRIPT="$SCRIPT_DIR/install-eSim-24.04.sh"
+    ;; 
```

---

## BUG 2: 🟡 [MODERATE] APT called incorrectly
**Tags:** `[Bash]` `[APT]`

### Technical Root Cause Analysis
Syntactical error in the `apt-get` command invocation (missing the procedure verb).

### Resolution Strategy & Implementation
Correct the command syntax to ensure the package `xz-utils` is installed.

```diff
- sudo apt-get xz-utils 
- pip3 install volare 
+ sudo apt-get install -y xz-utils
+ pip3 install volare
```

---

## BUG 3: 🟠 [MAJOR] KiCad PPA is incompatible with Ubuntu 25
**Tags:** `[Package Management]` `[PPA]`

### Technical Root Cause Analysis
The installer attempts to inject an external PPA (`ppa:kicad/kicad-6.0-releases`). Launchpad does not build this PPA for Ubuntu 25.04 (Plucky), leading to immediate HTTP 404 errors during package retrieval.

### Resolution Strategy & Implementation
Ubuntu 25.04 natively provides a compatible KiCad version. The fix involves detecting the OS version and bypassing PPA injection in favor of the official upstream repository.

#### Corrected Logic (install-eSim-scripts/install-eSim-24.04.sh)

```bash
function installKicad
{
    echo "Installing KiCad..........................."
    ubuntu_version=$(lsb_release -rs)

    if [[ "$ubuntu_version" == "25.04" ]]; then
        echo "Ubuntu 25.04 detected — using official Ubuntu repository"
        sudo apt update
        sudo apt install -y kicad
        return
    fi
    # Legacy logic for 24.04 continues...
}
```

---

## BUG 4: 🟠 [MAJOR] Broken KiCad PPA blocks APT forever
**Tags:** `[System Recovery]` `[APT]`

### Operational Impact
**System Instability**: invalid PPA entries persist in `/etc/apt/sources.list.d/`, causing all future system updates (`apt update`) to fail.

### Resolution Strategy & Implementation
Implement a pre-flight cleanup routine to purge invalid PPA artifacts before attempting installation.

```bash
# Remove any old KiCad PPAs that break Ubuntu 25
sudo rm -f /etc/apt/sources.list.d/kicad*
sudo add-apt-repository --remove ppa:kicad/kicad-6.0-releases -y 2>/dev/null
sudo add-apt-repository --remove ppa:kicad/kicad-8.0-releases -y 2>/dev/null
sudo apt-get update
```

---

## BUG 5: 🟡 [MODERATE] KiCad library path wrong
**Tags:** `[Scripting]` `[Path Resolution]`

### Technical Root Cause Analysis
The installation scripts rely on relative directory paths (assuming execution from `Ubuntu/`), but the entry point script executes them from `~/eSim`. This causes `file not found` errors for resources.

### Resolution Strategy & Implementation
Implement dynamic path resolution using `${BASH_SOURCE[0]}` to establish an absolute `BASE_DIR`.

```diff
#!/bin/bash
+ BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")"/.. && pwd)"
```

```diff
- tar xf library/kicadLibrary.tar.xz -C /usr/share/kicad
+ tar xf "$BASE_DIR/library/kicadLibrary.tar.xz" -C /usr/share/kicad
```

---

## BUG 6: 🔴 [CRITICAL] KiCad library never extracted
**Tags:** `[Archive Management]` `[Deployment]`

### Technical Root Cause Analysis
The script attempts to copy files from a directory (`kicadLibrary`) that does not exist. The installer failed to include the step to **decompress** the source tarball (`kicadLibrary.tar.xz`).

### Operational Impact
**Functional Failure**: The electronic component library is empty, rendering the software unusable for circuit design.

### Resolution Strategy & Implementation
Inject the decompression step prior to the copy operation.

```bash
cd ~/eSim/Ubuntu/library
# Explicitly extract the archive before copying
tar -xf kicadLibrary.tar.xz
```

```diff
- cp "$KICAD_CONFIG/sym-lib-table" "$KICAD_CONFIG/sym-lib-table"
+ cp "$BASE_DIR/library/kicadLibrary/template/sym-lib-table" "$KICAD_CONFIG/sym-lib-table"
```

---

## BUG 7: 🟡 [MODERATE] KiCad symbol paths wrong
**Tags:** `[File Operations]`

### Resolution Strategy & Implementation
Correct the source path to use the absolute `BASE_DIR`.

```diff
- cp kicadLibrary/eSim-symbols/* "$KICAD_CONFIG/symbols/"
+ cp "$BASE_DIR/library/kicadLibrary/eSim-symbols/"* "$KICAD_CONFIG/symbols/"
```

---

## BUG 8: 🟡 [MODERATE] NGHDL zip not found
**Tags:** `[Scripting]`

### Technical Root Cause Analysis
Execution context misuse: The script attempts to unzip a file present in a subdirectory without changing into that directory first.

### Resolution Strategy & Implementation
Force a directory change to `BASE_DIR` before invoking `unzip`.

```bash
echo "Installing NGHDL..........................."
cd "$BASE_DIR"     # <--- Fix: Switch to correct directory
unzip -o nghdl.zip
cd nghdl
chmod +x install-nghdl.sh
```

---

## BUG 9: 🟠 [MAJOR] libcanberra no longer exists
**Tags:** `[Dependency Management]` `[Deprecated Libs]`

### Technical Root Cause Analysis
The `libcanberra-gtk-module` library has been deprecated and effectively removed from the Ubuntu 25.04 package repositories.

### Resolution Strategy & Implementation
Remove the deprecated dependency from the installation manifest.

```diff
- sudo apt install -y libcanberra-gtk-module libcanberra-gtk3-module
+ # sudo apt install -y libcanberra-gtk-module libcanberra-gtk3-module
```

---

## BUG 10: 🔴 [CRITICAL] LLVM 20 breaks GHDL
**Tags:** `[Compilation]` `[LLVM Toolchain]` `[C++]`

### Symptom
```text
Unhandled version llvm 20.1.2 
Aborting Installation...
```

### Technical Root Cause Analysis
Ubuntu 25.04 defaults to **LLVM 20**. The GHDL 4.1 build configuration script (`configure`) does not support LLVM versions >15 without explicit overrides, and crashes when parsing the version string "20".

### Resolution Strategy & Implementation
**Toolchain Side-loading**: Install **LLVM 18** (supported) alongside LLVM 20 and explicitly point the GHDL build environment to the LLVM 18 binaries (`llvm-config-18`).

#### Patch (install-nghdl-24.04.sh)

1. **Install Compatibility Layer:**
    ```bash
    sudo apt install -y llvm-18 llvm-18-dev clang-18
    ```

2. **Patch Build Configuration:**
    ```diff
    function installGHDL {
        echo "Installing GHDL using LLVM 18"
        tar -xzf $ghdl.tar.gz
        cd $ghdl || exit 1
    
    +   export LLVM_CONFIG=/usr/bin/llvm-config-18
    +   export CC=clang-18
    +   export CXX=clang++-18
    
    -   ./configure --with-llvm
    +   ./configure --with-llvm-config=/usr/bin/llvm-config-18
        
        make -j$(nproc)
        sudo make install
    }
    ```

---

## BUG 11: 🟡 [MODERATE] Wrong GHDL configure flag
**Tags:** `[Build Systems]`

### Technical Root Cause Analysis
`--with-llvm` is a deprecated flag that does not accept valid paths in newer configuration scripts.

### Resolution Strategy & Implementation
Use the specific path-override flag for `llvm-config`.

```diff
- ./configure --with-llvm
+ ./configure --with-llvm-config=/usr/bin/llvm-config-18
```

---

## BUG 12: 🟡 [MODERATE] Desktop launcher points to wrong path
**Tags:** `[Desktop Integration]`

### Technical Root Cause Analysis
The desktop entry file (`/usr/bin/esim`) hardcodes a path to `/src/frontEnd` that does not account for the `Ubuntu/` subdirectory in this distribution structure.

### Resolution Strategy & Implementation
 Update the launcher script to point to the valid executable path.

```diff
#!/bin/bash
- cd /home/vishal/eSim/src/frontEnd || exit
- /home/vishal/eSim/venv/bin/python Application.py
+ cd /home/vishal/eSim/Ubuntu/src/frontEnd || exit
+ python3 Application.py
```

---

## BUG 13: 🟠 [MAJOR] Missing Python module (hdlparse)
**Tags:** `[Python]` `[VirtualEnv]`

### Technical Root Cause Analysis
Python 3.13 on Ubuntu 25 enforces **PEP 668** (externally managed environments), preventing global `pip` installs. The application fails because it cannot find required modules (`hdlparse`) in the system path.

### Resolution Strategy & Implementation
**Environment Encapsulation**: Create a dedicated Virtual Environment (`venv`) for eSim and install dependencies there. Update the launcher to explicitly source this environment.

```bash
# 1. Create Environment
python3 -m venv ~/eSim/venv
source ~/eSim/venv/bin/activate
pip install hdlparse numpy matplotlib pyqt5
```

```bash
# 2. Update Launcher
source /home/vishal/eSim/venv/bin/activate
cd /home/vishal/eSim/Ubuntu/src/frontEnd
python Application.py
```

---

## 3. Skills Demonstrated & Conclusion

The successful porting of eSim to Ubuntu 25.04 required a multidisciplinary engineering approach, resolving issues from the kernel interface level up to the application runtime.

| Skill Domain | Relevant Bugs | Engineering Competency |
| :--- | :--- | :--- |
| **Compiler Toolchains** | Bug 10, 11 | Managing complex C++/LLVM build dependencies and version conflicts. |
| **System Internals** | Bug 3, 4, 9 | Debugging APT repositories, PPA architecture, and library linking. |
| **Shell Automation** | Bug 1, 5, 8, 12 | Writing robust, path-independent bash scripts for automated deployment. |
| **Python Environments** | Bug 13 | Adhering to modern PEP standards (venv) for dependency isolation. |
| **release Engineering** | Bug 1, 6 | Fixing installer logic and binary distribution packaging (tarballs). |

**Result: eSim is now fully functional and verified on Ubuntu 25.04**
