# FOSSEE eSim Winter Internship 2026 – Task 4 Submission Overview

## Quick Summary

- **Task:** Screening Task 4 — Ubuntu 25.04 Installer Investigation & Fix
- **Target Repository:** `FOSSEE/eSim`
- **Target Branch:** `installers`
- **Component Fixed:** `Ubuntu/install-eSim-scripts/install-eSim-25.04.sh` (`copyKicadLibrary()`)
- **Automated Test Added:** `Ubuntu/tests/test_kicad8_copy.sh`
- **Local Commit:** `a1462d61baa6b0297f57da7f2eb73b39bc40ff4b`

---

## 1. The Issue
`install-eSim-25.04.sh` installs **KiCad 8.0** (`ppa:kicad/kicad-8.0-releases`). However, `copyKicadLibrary()` directed the global schematic symbol table (`sym-lib-table`) into `$HOME/.config/kicad/6.0/` due to legacy code inherited from the Ubuntu 23.04 installer.

On Ubuntu 25.04, KiCad 8.0 exclusively reads global symbol tables from `$HOME/.config/kicad/8.0/sym-lib-table`. As a result, eSim custom symbols (`eSim_Devices`, `eSim_Subckt`, `eSim_Plot`, `eSim_Nghdl`, etc.) fail to load in Eeschema.

---

## 2. The Fix
In `Ubuntu/install-eSim-scripts/install-eSim-25.04.sh`:
- Changed target directory to `kicad_config_dir="$HOME/.config/kicad/8.0"`.
- Added directory existence check and creation for `8.0`.
- Quoted all path variables to prevent word-splitting.
- Uninstaller was deliberately **not** made to delete `~/.config/kicad/8.0` with `rm -rf` to protect unrelated user KiCad settings.

---

## 3. Test Procedure
Run the automated regression test:
```bash
bash Ubuntu/tests/test_kicad8_copy.sh
```
The test:
1. Dynamically extracts `copyKicadLibrary()` from `install-eSim-25.04.sh` (zero code duplication).
2. Sets up an isolated sandbox in `/tmp` and overrides `HOME`.
3. Mocks `sudo` and `tar` to prevent system modifications.
4. Executes the production function in an isolated subshell.
5. Verifies that `~/.config/kicad/8.0/sym-lib-table` is created with identical contents, legacy `6.0` is not created, symbols are copied to the mock system destination, and a second consecutive run succeeds without error.

---

## 4. Limitations & Scope
- **Verification Environment:** Automated test execution and syntax validation were performed using **Windows Git Bash**. Live deployment and GUI visual verification on an actual **Ubuntu 25.04 VM** are scheduled as a pending verification step.
- **Scope:** This patch specifically fixes the KiCad 8.0 symbol-table path configuration. It does not resolve unrelated installer issues (e.g. wrapper script syntax or Python 3.13 venv dependencies).
