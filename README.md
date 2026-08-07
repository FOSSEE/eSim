# Task 4: eSim Upgradation

[![FOSSEE Task](https://img.shields.io/badge/FOSSEE%20Internship-Task%204%20Upgradation-blue?logo=github)](https://fossee.in/Semester-Internship/Autumn/2026)
[![Target OS](https://img.shields.io/badge/Ubuntu-25.04-orange?logo=ubuntu)](https://releases.ubuntu.com/)
[![Python Version](https://img.shields.io/badge/Python-3.12%2B%20%7C%203.13-yellow?logo=python)](https://www.python.org/)
[![eSim Version](https://img.shields.io/badge/eSim-v2.5-brightgreen)](https://esim.fossee.in/)
[![Release Zip](https://img.shields.io/badge/Release%20Zip-v2.5--ubuntu25.04--26i--task4-blueviolet?logo=github)](https://github.com/vishnunandan555/eSim/releases/tag/v2.5-ubuntu25.04-26i-task4)
[![Developer Log](https://img.shields.io/badge/Dev%20Log-Google%20Docs-red?logo=google-docs)](https://docs.google.com/document/d/1tMAMabGyeEjOVv5GhLCyBLGgkvl-6we5XsEBKnBn9Pg/edit?usp=sharing)

> **FOSSEE Semester Long Internship Autumn 2026 — Task 4 Review**  
> **Author:** [Vishnu Nandan](https://github.com/vishnunandan555)  
> **Repository:** [https://github.com/vishnunandan555/eSim](https://github.com/vishnunandan555/eSim)  
> **Branches with Changes:** [`installers`](https://github.com/vishnunandan555/eSim/tree/installers) & [`master`](https://github.com/vishnunandan555/eSim/tree/master)  
> **Release Package Zip:** [GitHub Release v2.5-ubuntu25.04-26i-task4](https://github.com/vishnunandan555/eSim/releases/tag/v2.5-ubuntu25.04-26i-task4)  
> **Full Developer Log:** [Google Docs Dev Log Link](https://docs.google.com/document/d/1tMAMabGyeEjOVv5GhLCyBLGgkvl-6we5XsEBKnBn9Pg/edit?usp=sharing)

---

## Overview

This repository contains all fixes and updates for installing and running **eSim v2.5** and **NGHDL** on modern Linux systems, specifically **Ubuntu 25.04** (which ships with Python 3.13 by default).

During testing of eSim 2.5 on fresh Ubuntu 25.04 virtual machines, several issues stopped the installer or broke eSim on startup. These included script syntax errors, missing C compiler header packages, unhandled command-line flags, VM memory freezes during Verilator compilation, missing Python dependencies (`PyQt6`), and INI configuration corruption.

---

## Debugging & Testing Methodology

To debug the installation flow systematically without corrupting the host machine:

1. **Virtual Environment Isolation**: All testing was carried out inside fresh KVM virtual machines (on Fedora host) running Ubuntu 25.04.
2. **Terminal Log Capturing & Filtering**: Installation runs were captured using log redirection and filtered for critical errors:
   ```bash
   ./install-eSim.sh --install 2>&1 | tee install_log.txt
   grep -i -E "error|failed|unable|cannot" install_log.txt
   ```
3. **Execution Pipeline Tracing**: Traced errors through the installer function execution sequence (`createConfigFile` -> `installDependency` -> `installKicad` -> `copyKicadLibrary` -> `installNghdl` -> `installSky130Pdk` -> `createDesktopStartScript`) to isolate the exact step causing failure.
4. **Iterative Verification**: Performed full uninstalls and fresh VM state restores before confirming each fix to ensure full reproducibility from scratch.

---

## Branch-wise Recap of Changes Made (Newest to Oldest)

### 1. `installers` Branch (4 Commits)

* **Fixed INI Config Duplication (`DuplicateSectionError`)**: Changed file header writing in `install-eSim-25.04.sh` from append mode (`>>`) to overwrite mode (`>`). Re-running the installer no longer appends duplicate `[eSim]` headers to `~/.esim/config.ini`.  
  [*Commit `ef336538`*](https://github.com/vishnunandan555/eSim/commit/ef336538)

* **Added PyQt6 Virtual Environment Dependency**: Integrated `pip install PyQt6` during virtual environment setup (`~/.esim/env`) in `install-eSim-25.04.sh` to resolve `ModuleNotFoundError: No module named 'PyQt6'` on Python 3.12+/3.13.  
  [*Commit `df2c8101`*](https://github.com/vishnunandan555/eSim/commit/df2c8101)

* **Global `config_dir` Scope Export**: Declared `config_dir` in global script scope to prevent main script evaluation warnings (`./install-eSim.sh: line 62: /: Is a directory`).  
  [*Commit `a87ed7ce`*](https://github.com/vishnunandan555/eSim/commit/a87ed7ce)

* **Closed Syntax Error in Main Installer**: Fixed unclosed `if` block at line 69 of `install-eSim.sh` by adding missing `fi` before function definitions, resolving `./install-eSim.sh: line 70: syntax error near unexpected token '}'`.  
  [*Commit `ce9dd90e`*](https://github.com/vishnunandan555/eSim/commit/ce9dd90e)

---

### 2. `master` Branch (6 Commits)

* **Synced Upstream FOSSEE Core Updates**: Merged upstream FOSSEE main repository updates to maintain full compatibility with recent eSim core enhancements.  
  [*Commit `f3cd999d`*](https://github.com/vishnunandan555/eSim/commit/f3cd999d)

* **Added Missing C Compiler Development Headers**: Added `libfftw3-dev` and `libreadline-dev` to the automated `apt` installation list to resolve missing headers (`fftw3.h` and `readline/readline.h`) during C-to-HDL model compilation.  
  [*Commit `6d1163cb`*](https://github.com/vishnunandan555/eSim/commit/6d1163cb)

* **Merged NGHDL Installer Fixes PR #2**: Consolidated and merged all NGHDL installer pipeline updates into `master`.  
  [*Pull Request #2*](https://github.com/vishnunandan555/eSim/pull/2) / [*Commit `db391bb3`*](https://github.com/vishnunandan555/eSim/commit/db391bb3)

* **Bundled NGHDL Source Packages & 25.04 Subscript**: Added missing source archives (GHDL, Verilator, NGHDL simulator source tarballs) into `nghdl/` and linked main installer to run OS-specific subscript `install-nghdl-25.04.sh`.  
  [*Commit `33e8ec6d`*](https://github.com/vishnunandan555/eSim/commit/33e8ec6d)

* **Fixed `confi.gure` Typo & Bounded Parallel Build**: Fixed typographical error `../confi.gure` on line 98 of `install-nghdl.sh`. Replaced macOS command `$(sysctl -n hw.ncpu)` with bounded `-j5` parallelism (`make -j5`) to stop Verilator builds from crashing VM memory.  
  [*Commit `d3a575a7`*](https://github.com/vishnunandan555/eSim/commit/d3a575a7)

* **Added `--install` Flag Routing in NGHDL**: Added `--install|install)` case pattern in `install-nghdl.sh` so calling `./install-nghdl.sh --install` triggers automated setup instead of falling into `*` default case with `Unknown argument`.  
  [*Commit `51dd0794`*](https://github.com/vishnunandan555/eSim/commit/51dd0794)

---

## OS Support & Limitations

| Operating System | Support Status | Notes |
| :--- | :--- | :--- |
| **Ubuntu 25.04** | Supported | Verified on clean VM. Fully working with Python 3.13 & PyQt6 virtualenv. |
| **Ubuntu 26.04** | Blocked (Upstream PPA) | Tested on experimental VM. Blocked because `ppa:kicad/kicad-8.0-releases` has no package files for `resolute` yet (HTTP 404). |

---

## How to Test & Install (Ubuntu 25.04)

### Method 1: Using Pre-packaged GitHub Release Zip (Quickest)

For quick evaluation, I have prepared and published a ready-to-run distribution `.zip` archive on the GitHub Releases page:

1. Download the release archive from the [GitHub Release Page](https://github.com/vishnunandan555/eSim/releases/tag/v2.5-ubuntu25.04-26i-task4).
2. Extract the downloaded zip archive on your Ubuntu 25.04 system.
3. Open a terminal inside the extracted directory and run:
   ```bash
   chmod +x install-eSim.sh
   ./install-eSim.sh --install
   ```
4. Launch eSim by typing `esim` in terminal or clicking the desktop shortcut.

---

### Method 2: Testing directly from Git Repository Branches

```bash
# 1. Clone repo
git clone https://github.com/vishnunandan555/eSim.git
cd eSim

# 2. Checkout installers branch and copy install-eSim.sh & install-eSim-scripts to temporary location
git checkout installers
cp Ubuntu/install-eSim.sh /tmp/
cp -r Ubuntu/install-eSim-scripts /tmp/

# 3. Checkout master branch
git checkout master

# 4. Paste the copied installer scripts into the master branch root
cp /tmp/install-eSim.sh .
cp -r /tmp/install-eSim-scripts .

# 5. Pack kicadLibrary to tar.xz inside library/ folder and remove original kicadLibrary directory
cd library
tar -cJf kicadLibrary.tar.xz kicadLibrary/
rm -rf kicadLibrary/
cd ..

# 6. Zip nghdl folder in master branch root and remove original nghdl directory
zip -r nghdl.zip nghdl/
rm -rf nghdl/

# 7. Grant execution permission and run installer
chmod +x install-eSim.sh
./install-eSim.sh --install

# 8. Launch eSim
esim
```

---

## Transparency & AI Disclosure

All debugging, script modifications, and testing were performed manually inside Fedora KVM virtual machines running Ubuntu 25.04. Real-time engineering notes and terminal outputs were recorded in the [Google Docs Dev Log](https://docs.google.com/document/d/1tMAMabGyeEjOVv5GhLCyBLGgkvl-6we5XsEBKnBn9Pg/edit?usp=sharing).

AI usage across the project was minimal (specifically Google Gemini for brief syntax queries during debugging, as noted in the devlog). Only this README document was structured and formatted with AI assistance to ensure clean presentation.
