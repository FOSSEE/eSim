# FOSSEE eSim Winter Internship 2026
## Screening Task 4: Technical Report & Fix Analysis

- **Candidate:** Screening Task 4 Submission
- **Target Repository:** `FOSSEE/eSim`
- **Target Branch:** `installers`
- **Target Application:** eSim 2.5
- **Target OS:** Ubuntu 25.04 (Plucky Puffin)
- **Investigated File:** `Ubuntu/install-eSim-scripts/install-eSim-25.04.sh`
- **Automated Test Suite:** `Ubuntu/tests/test_kicad8_copy.sh`
- **Local Commit Hash:** `a1462d61baa6b0297f57da7f2eb73b39bc40ff4b`

---

## 1. Executive Summary & Task Scope

Screening Task 4 requires candidates to investigate the eSim 2.5 installer on Ubuntu 25.04, identify genuine technical defects in the installer codebase, implement a verified fix on the `installers` branch, and establish automated regression testing.

Our investigation identified a critical path configuration mismatch in `Ubuntu/install-eSim-scripts/install-eSim-25.04.sh`: while the installer installs **KiCad 8.0**, the library setup function `copyKicadLibrary()` directed the global schematic symbol table (`sym-lib-table`) into the legacy KiCad **6.0** configuration directory (`$HOME/.config/kicad/6.0/`).

This report documents:
1. The exact technical defect and why it breaks schematic symbol loading in KiCad 8.
2. The root cause and historical lineage across installer versions (22.04, 23.04, 24.04, 25.04).
3. The exact minimal backward-compatible patch applied to `install-eSim-25.04.sh`.
4. A factual comparative review against existing Ubuntu 25.04-related pull requests in `FOSSEE/eSim`.
5. An automated test harness (`Ubuntu/tests/test_kicad8_copy.sh`) that dynamically extracts and validates the production function under an isolated sandbox.
6. Verification commands, obtained execution outputs, and pending platform validations.

> **Important Scope & Testing Notice:**
> - This fix addresses the **KiCad 8.0 symbol-table configuration path**, not the entire end-to-end installation of all eSim suite tools.
> - Automated unit tests documented herein were executed using **Windows Git Bash**. Full live suite deployment and Eeschema GUI symbol loading on an actual **Ubuntu 25.04 VM** remain marked as pending platform verification.

---

## 2. Technical Defect: KiCad 8 Symbol-Table Configuration Path

### Current Behavior
In `install-eSim-25.04.sh`, `installKicad()` provisions KiCad 8.0:
```bash
kicadppa="kicad/kicad-8.0-releases"
```

However, in `copyKicadLibrary()` (lines 234–244), the script created and targeted the KiCad 6.0 directory:
```bash
if [ -d ~/.config/kicad/6.0 ];then
    echo "kicad config folder already exists"
else
    echo ".config/kicad/6.0 does not exist"
    mkdir -p ~/.config/kicad/6.0
fi

# Copy symbol table for eSim custom symbols
cp kicadLibrary/template/sym-lib-table ~/.config/kicad/6.0/
```

### Authoritative KiCad Configuration Path Specification
KiCad adheres to the XDG Base Directory Specification on Linux:
- KiCad 6: reads `$XDG_CONFIG_HOME/kicad/6.0/` (default: `$HOME/.config/kicad/6.0/`)
- KiCad 7: reads `$XDG_CONFIG_HOME/kicad/7.0/` (default: `$HOME/.config/kicad/7.0/`)
- KiCad 8: reads `$XDG_CONFIG_HOME/kicad/8.0/` (default: **`$HOME/.config/kicad/8.0/`**)

The global symbol library table file must reside at:
`$HOME/.config/kicad/8.0/sym-lib-table`

### Technical Consequence on Ubuntu 25.04
When KiCad 8.0 launches from eSim on Ubuntu 25.04:
1. KiCad 8 searches for `$HOME/.config/kicad/8.0/sym-lib-table`.
2. It never inspects `$HOME/.config/kicad/6.0/sym-lib-table`.
3. KiCad treats this as a first-time launch and prompts the user to initialize a blank or default symbol table.
4. All eSim custom symbol libraries (`eSim_Devices`, `eSim_Subckt`, `eSim_Plot`, `eSim_Nghdl`, etc.) fail to load in Eeschema, leaving schematic components unresolved.

---

## 3. Root Cause & Lineage Across Ubuntu Installers
A comparative code audit of `Ubuntu/install-eSim-scripts/` revealed how this regression was introduced:

| Script | KiCad Version in `installKicad` | Path in `copyKicadLibrary` | Status / Analysis |
|---|---|---|---|
| `install-eSim-23.04.sh` | KiCad 6.0 (`ppa:kicad/kicad-6.0-releases`) | `~/.config/kicad/6.0/` | **Correct for Ubuntu 23.04**, which targeted KiCad 6.0. |
| `install-eSim-24.04.sh` | KiCad 8.0 (`ppa:kicad/kicad-8.0-releases`) | `~/.config/kicad/6.0/` | **Defect introduced:** PPA was bumped to 8.0 in commit `d3ba66b3`, but `copyKicadLibrary` was overlooked. |
| `install-eSim-25.04.sh` | KiCad 8.0 (`ppa:kicad/kicad-8.0-releases`) | `~/.config/kicad/6.0/` | **Defect inherited:** Cloned from `24.04.sh` in commit `f4cede1` without updating the path. |
| `install-eSim-22.04.sh` | KiCad 8.0 (`ppa:kicad/kicad-8.0-releases`) | Dynamic (`8.0` default) | Updated independently in `22.04.sh` lines 234–244 to detect `$HOME/.config/kicad/8.0`. |

The legacy `6.0` path in `install-eSim-25.04.sh` was an accidental inheritance, not an intentional design choice.

---

## 4. Factual Comparative Review Against Existing Pull Requests

To ensure our contribution avoids duplicating prior work, all open and merged pull requests addressing Ubuntu 25.04 on the `installers` branch were audited via the GitHub REST API:

| PR # | Author | Scope of Changes in `install-eSim-25.04.sh` | Did it fix `copyKicadLibrary()` path? |
|---|---|---|---|
| **#628** | `Somesh-coding` | Changed line 136 (`exit 0` → `return 0` in KiCad version check). Added root `install-eSim.sh`. | **No.** `copyKicadLibrary()` was untouched; `~/.config/kicad/6.0` remained. |
| **#632** | `sakshirathi2006` | Changed line 136 (`return 0`) and line 154 (unpinned KiCad package). | **No.** `copyKicadLibrary()` was untouched; `~/.config/kicad/6.0` remained. |
| **#638** | `Lutfullah07` | Added root-level copy of `install-eSim-25.04.sh` and task report. | **No.** Did not fix `Ubuntu/install-eSim-scripts/install-eSim-25.04.sh`. |
| **#640** | `insha-fab` | Modified `Ubuntu/install-eSim.sh` OS version detection. | **No.** Did not touch `install-eSim-25.04.sh`. |
| **#641** | `animeshmanna1976` | Documentation report (`Ubuntu/TASK4_REPORT.md`). | **No.** Documentation only; no script code changed. |
| **#656** | `dev25bansal-ops` | Modified `installKicad()` (lines 112–160) and `installDependency()` (unzip, xz-utils, pyhdlparser commit pin). | **No.** Lines 234–244 of `copyKicadLibrary()` were untouched; still targeted `6.0`. |
| **#657** | `hyperpixelated` | Updated `nghdl/install-nghdl.sh` on `master` branch. | **No.** Does not touch Ubuntu installer scripts. |

**Audit Conclusion:**
Evidence confirms that none of the existing pull requests resolved the KiCad 8.0 configuration path defect in `copyKicadLibrary()` within `Ubuntu/install-eSim-scripts/install-eSim-25.04.sh`. Our patch addresses this specific unpatched issue.

---

## 5. Applied Code Modification

The minimal fix was applied directly to [Ubuntu/install-eSim-scripts/install-eSim-25.04.sh](file:///c:/Users/Lenovo/Desktop/eSim-Internship/eSim/Ubuntu/install-eSim-scripts/install-eSim-25.04.sh#L231-L246):

```diff
--- a/Ubuntu/install-eSim-scripts/install-eSim-25.04.sh
+++ b/Ubuntu/install-eSim-scripts/install-eSim-25.04.sh
@@ -231,15 +231,17 @@ function copyKicadLibrary
     #Extract custom KiCad Library
     tar -xJf library/kicadLibrary.tar.xz

-    if [ -d ~/.config/kicad/6.0 ];then
+    kicad_config_dir="$HOME/.config/kicad/8.0"
+
+    if [ -d "$kicad_config_dir" ];then
         echo "kicad config folder already exists"
     else
-        echo ".config/kicad/6.0 does not exist"
-        mkdir -p ~/.config/kicad/6.0
+        echo "$kicad_config_dir does not exist"
+        mkdir -p "$kicad_config_dir"
     fi

     # Copy symbol table for eSim custom symbols
-    cp kicadLibrary/template/sym-lib-table ~/.config/kicad/6.0/
+    cp "kicadLibrary/template/sym-lib-table" "$kicad_config_dir/"
     echo "symbol table copied in the directory"

     # Copy KiCad symbols made for eSim
```

### Design Decisions:
1. **Explicit 8.0 Path:** Sets `kicad_config_dir="$HOME/.config/kicad/8.0"` matching KiCad 8.0 specification.
2. **Path Quoting:** All variables are quoted to prevent word-splitting on paths containing spaces.
3. **Preserved Conventions:** Retained original variable naming, echo statements, and indentation style.
4. **Uninstaller Safety:** The uninstaller at line 420 was deliberately **not** modified to execute `rm -rf $HOME/.config/kicad/8.0`, preventing accidental destruction of unrelated user KiCad 8 settings.

---

## 6. Automated Test Suite (`Ubuntu/tests/test_kicad8_copy.sh`)

A dedicated unit test script was created at [Ubuntu/tests/test_kicad8_copy.sh](file:///c:/Users/Lenovo/Desktop/eSim-Internship/eSim/Ubuntu/tests/test_kicad8_copy.sh).

### Key Architectural Safeguards:
- **Zero Code Duplication:** Dynamically extracts the live `copyKicadLibrary()` function from `install-eSim-25.04.sh` using `sed` and evaluates it into the test shell.
- **Trap-Safe Subshell Execution:** Invokes `(copyKicadLibrary)` inside an isolated subshell so internal shell options (`set +e`, `set -e`) and traps (`trap error_exit ERR`) do not mutate the test harness.
- **Host Protection:** Redirects `HOME` to `$TEST_SANDBOX/mock_home`. Real host settings remain completely untouched.
- **Mocked Boundaries:**
  - `sudo cp`: Redirects `/usr/share/kicad/symbols/` into a sandbox directory.
  - `sudo chown`: Safe no-op stub.
  - `tar`: Safe no-op stub (archive decompression is tested separately).
- **Automatic Cleanup:** Registers `trap 'rm -rf "$TEST_SANDBOX"' EXIT` ensuring cleanup on both success and failure.

---

## 7. Verification Results

All tests were executed under **Windows Git Bash** (`C:\Program Files\Git\bin\bash.exe`, Bash 5.2):

### 1. Syntax Checks
```bash
bash -n Ubuntu/install-eSim-scripts/install-eSim-25.04.sh  # Exit Code: 0
bash -n Ubuntu/tests/test_kicad8_copy.sh                 # Exit Code: 0
git diff --check                                         # Exit Code: 0
```

### 2. Test Execution
```bash
bash Ubuntu/tests/test_kicad8_copy.sh
```

**Output Log:**
```text
============================================================
Running focused test for production copyKicadLibrary()...
============================================================
Target installer: .../Ubuntu/install-eSim-scripts/install-eSim-25.04.sh

[Test 1] Executing extracted copyKicadLibrary() on fresh environment...
/tmp/esim_kicad8_test.5cG2rQ/mock_home/.config/kicad/8.0 does not exist
symbol table copied in the directory
  [PASS] Target directory ~/.config/kicad/8.0/ was created.
  [PASS] Target sym-lib-table exists at: /tmp/esim_kicad8_test.5cG2rQ/mock_home/.config/kicad/8.0/sym-lib-table
  [PASS] sym-lib-table contents match fixture exactly.
  [PASS] Legacy directory ~/.config/kicad/6.0/ was NOT created.
  [PASS] Symbol copied to system directory: /tmp/esim_kicad8_test.5cG2rQ/mock_usr_share_kicad_symbols/eSim_Devices.kicad_sym
  [PASS] Temporary kicadLibrary/ directory was cleaned up by function.

[Test 2] Executing extracted copyKicadLibrary() second time (idempotency check)...
kicad config folder already exists
symbol table copied in the directory
  [PASS] Detected existing config directory on rerun.
  [PASS] sym-lib-table remains valid and identical after rerun.
  [PASS] Legacy directory ~/.config/kicad/6.0/ still does NOT exist.

============================================================
ALL TESTS PASSED: Extracted production function verified.
============================================================
Exit Code: 0
```

---

## 8. Limitations & Pending Platform Verification

1. **Host Environment:** Syntax validation and automated unit testing were executed on Windows Git Bash. Running `bash Ubuntu/tests/test_kicad8_copy.sh` inside the actual Ubuntu 25.04 VM is scheduled as the next step.
2. **Scope:** This fix addresses KiCad 8 symbol-table path resolution. It does not resolve unrelated installer issues (e.g. entry-point wrapper syntax in `Ubuntu/install-eSim.sh`, Python 3.13 venv PEP 668 isolation, or KiCad package micro-version pinning).
3. **End-to-End Suite Status:** No claim is made that eSim 2.5 is completely installed or operational on Ubuntu 25.04 until live VM testing confirms full GUI and simulation integration.
