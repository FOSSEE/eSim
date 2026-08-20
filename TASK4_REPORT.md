# Task 4 — eSim Upgradation Report

**Submitted by:** Lutfullah (GitHub: [Lutfullah07](https://github.com/Lutfullah07))
**FOSSEE eSim Semester Long Internship — Autumn 2026**
**Repository:** [Lutfullah07/eSim](https://github.com/Lutfullah07/eSim) (fork of FOSSEE/eSim)

## Objective

To install eSim-2.5 from source on a modern Ubuntu system (Ubuntu 26.04 LTS), identify dependency and installation issues that are **not covered by existing documentation or scripts**, document them clearly, and fix as many as possible — prioritizing issues that block the **main eSim GUI** from launching, per the stated evaluation criteria.

## Test Environment

| Component | Detail |
|---|---|
| Host | Windows, VirtualBox 7.2.14 |
| Guest OS | Ubuntu 26.04 LTS (VM) |
| Resources | 4–6 GB RAM, 2 CPU cores, 25 GB disk |
| Python | 3.14 |
| Repository branch | `master` (the `installer` branch referenced in some FOSSEE docs does not exist in the current source tree) |

## Methodology

1. Cloned the forked repository into a clean Ubuntu VM with no prior eSim installation.
2. Followed the official `INSTALL` instructions and `scripts/setup-esim.sh` step by step.
3. Every failure was reproduced, the exact error message was recorded, and the responsible script/line or missing package was traced using `find`, direct execution, and Python tracebacks.
4. Each root cause was diagnosed **before** attempting a fix (not just patched blindly).
5. Fixes were implemented, re-tested to confirm resolution, and committed/pushed individually to keep history traceable.
6. Progress was verified at each step and captured with terminal screenshots (see `images/` folder), culminating in a full, successful launch of the eSim GUI.

---

## Summary Table

| # | Issue | Blocks Main GUI? | Status | Difficulty |
|---|---|---|---|---|
| 1 | `setup-esim.sh` — broken `$SNAP`-based path, library setup fails | Indirect (breaks library setup step) | ✅ Fixed | Medium |
| 2 | `install-eSim.sh` referenced in `INSTALL` does not exist in source repo | No (blocks first-time users following docs) | ⚠️ Reported | Low–Medium |
| 3 | `launcher-esim.sh` — broken `$SNAP`-based path, GUI launcher fails | **Yes — directly blocks GUI launch** | ✅ Fixed | Medium |
| 4 | Python dependency chain missing (PyQt6 → numpy → matplotlib → hdlparse) | **Yes — directly blocks GUI launch** | ✅ Fixed (4/4 resolved) | **High** |
| 5 | `.esim` config directory not auto-created, workspace selection crashes | **Yes — directly blocks GUI launch** | ✅ Fixed | Medium |

**Total issues reported: 5 (across 8 distinct root causes, since Issue 4 bundles 4 sub-dependencies)**
**Total issues fixed: 4 of 5 top-level issues (Issue 2 intentionally left to maintainers — see below)**
**Final result: eSim-2.5 GUI launches successfully end-to-end — see final proof screenshot at the bottom of this report.**

---

## Issue 1 — `scripts/setup-esim.sh`: Broken Snap-based path resolution

**Severity:** Medium (breaks the library-setup step of the official installation flow)

**Symptom:**
```
cp: cannot stat '/3rdparty/template/sym-lib-table': No such file or directory
```

**Root cause:**
The script defines `eSim_HOME="$SNAP/eSim"`. The `$SNAP` environment variable is only populated when eSim is installed as a **Snap package**. When installing from source (as instructed in `INSTALL`), `$SNAP` is empty, so `eSim_HOME` collapses to `/eSim`, an invalid absolute path that doesn't exist on a source install. Every path built from `eSim_HOME` downstream fails silently or with a misleading "file not found" error.

**Fix:**
Changed the home-path resolution to derive the actual repository root at runtime instead of relying on a Snap-only variable:

```bash
eSim_HOME="$(dirname "$(pwd)")"
```

and corrected the copy command to reference the real library path:

```bash
cp "$eSim_HOME/library/kicadLibrary/template/sym-lib-table" "$TARGET/template/"
```

**Verification:** `sudo ./setup-esim.sh` now completes with `eSim libraries setup completed.` and no errors.

**Status:** ✅ Fixed, committed, and pushed to `scripts/setup-esim.sh`.

---

## Issue 2 — `install-eSim.sh` referenced in documentation does not exist in source repo

**Severity:** Low–Medium (blocks first-time users who follow `INSTALL` literally)

**Symptom:**
`INSTALL` instructs Ubuntu users to run `install-eSim.sh`. This file does not exist anywhere in the source repository.

**Proof — searching the entire repo for the file `INSTALL` tells users to run, and finding nothing:**

![install-eSim.sh not found in repository](images/issue2-install-esim-sh-missing.png)

```
find . -iname "install-eSim.sh"
```
returns no output — confirmed absent from the cloned source tree.

**Root cause:**
`install-eSim.sh` most likely only ships inside the pre-packaged downloadable `.zip`/release build of eSim, not in the GitHub source repository that `INSTALL` is written for. This is a **documentation-vs-repository mismatch**: a new contributor cloning the repo (as `INSTALL` itself suggests) hits a dead end immediately.

**Why not fixed directly:** Resolving this requires a maintainer decision — either (a) update `INSTALL` to point users to `scripts/setup-esim.sh` instead, or (b) add the missing `install-eSim.sh` to the source tree. Making that call unilaterally risks diverging from the intended install flow, so this is reported with a recommendation rather than patched.

**Status:** ⚠️ Reported in this document and in the upstream PR description for maintainer review.

---

## Issue 3 — `scripts/launcher-esim.sh`: Broken Snap-based path resolution (blocks GUI launch)

**Severity: High — this directly prevents the main eSim GUI from starting.**

**The original, unmodified script relied entirely on Snap-only variables:**

![Original launcher-esim.sh using $SNAP paths](images/issue3-original-launcher-script.png)

**Symptom when run as-is:**

![launcher-esim.sh fails with path errors](images/issue3-launcher-error.png)

```
launcher-esim.sh: line 10: /usr/bin/setup-esim.sh: No such file or directory
launcher-esim.sh: line 11: cd: /eSim/src/frontEnd: No such file or directory
python3: can't open file '.../Application.py': No such file or directory
```

**Root cause:**
Identical `$SNAP` pattern as Issue 1, but here it breaks the **actual GUI entry point**. `cd "$SNAP/eSim/src/frontEnd"` collapses to `cd /eSim/src/frontEnd` on a source install, which does not exist. The real entry point had to be located manually:

![Locating the real Application.py path with find](images/issue3-finding-real-path.png)

The actual entry point is at `<repo-root>/src/frontEnd/Application.py`.

**Fix:**
Rather than bypassing the launcher script, it was edited directly so the official launcher itself works for source installs:

- Commented out the Snap-only line `$SNAP/usr/bin/setup-esim.sh` (not applicable outside Snap).
- Changed `cd $SNAP/eSim/src/frontEnd` to:
  ```bash
  cd "$(dirname "$(pwd)")/src/frontEnd"
  ```

**Verification:** After the fix, `bash launcher-esim.sh` correctly reaches and executes `Application.py`. Confirmation of this is that the *exact* `$SNAP`-path errors above disappear completely, and execution proceeds to a new, unrelated error (missing Python module `PyQt6`) — proving the path-resolution problem was fully eliminated:

![Path fix confirmed — script now reaches Application.py and hits the next real issue](images/issue3-fixed-pyqt6-error-appears.png)

**Status:** ✅ Fixed, committed, and pushed to `scripts/launcher-esim.sh`.

---

## Issue 4 — Missing Python Dependency Chain (blocks GUI launch) — HIGHEST WEIGHTAGE

**Severity: Highest — per the evaluation criteria, this is a dependency chain that interrupts installation of the *main GUI* of eSim, not a smaller sub-block like NgVeri.**

Once Issue 3 was resolved, `Application.py` began executing but failed repeatedly as it hit successive missing Python modules. Each was diagnosed and resolved in sequence.

### 4.1 — `PyQt6` missing

```
ModuleNotFoundError: No module named 'PyQt6'
```

Root cause: Qt6 Python bindings (the GUI toolkit eSim's frontend is built on) and `pip3` itself were not present on a clean system. Initial attempts to install `pip3`/`python-pip` via `apt` failed with "no installation candidate":

![pip/pip3 not available via apt directly](images/issue4-1-pip-troubleshooting.png)

Fix — installed `python3-pip` correctly, then installed PyQt6 with the required flag for externally-managed environments:
```bash
sudo apt install python3-pip -y
pip3 install PyQt6 --break-system-packages
```

![PyQt6 installing](images/issue4-1-pyqt6-installing.png)

![PyQt6 successfully installed](images/issue4-1-pyqt6-installed.png)

### 4.2 — `numpy` missing

```
ModuleNotFoundError: No module named 'numpy'
```

![numpy missing error](images/issue4-2-numpy-missing.png)

Fix:
```bash
pip3 install numpy --break-system-packages
```

![numpy successfully installed](images/issue4-2-numpy-installed.png)

### 4.3 — `matplotlib` missing

```
ModuleNotFoundError: No module named 'matplotlib'
```
(raised from `src/ngspiceSimulation/plot_window.py`, which imports `matplotlib.pyplot`)

Fix:
```bash
pip3 install matplotlib --break-system-packages
```
Successfully installed: `contourpy-1.3.3 cycler-0.12.1 fonttools-4.63.0 kiwisolver-1.5.0 matplotlib-3.11.1 python-dateutil-2.9.0.post0 six-1.17.0`

### 4.4 — `hdlparse` missing *and* incompatible with modern Python (deepest root cause found)

```
ModuleNotFoundError: No module named 'hdlparse'
```
(raised from `src/maker/Maker.py`, which imports `hdlparse.verilog_parser`)

A first attempt to install the obvious candidate failed:
```bash
pip3 install hdlparse --break-system-packages
# error in hdlparse setup command: use_2to3 is invalid
```

**Root cause investigation:** The `hdlparse` package published on PyPI (v1.0.1, by kevinpt/zhelnio) has not been updated since ~2016. Its `setup.py` sets `use_2to3=True`, a setuptools feature that used to auto-convert Python 2 source to Python 3 at install time. Modern `setuptools` (v58+) has **removed `2to3` support entirely**, so this package cannot install on *any* current Ubuntu/Python system — not specific to this VM.

An attempted workaround (downgrading `setuptools` to `<58`) was tried and **failed for a second, independent reason**: Python 3.14 itself has removed `pkgutil.ImpImporter`, an API that old `setuptools` versions depend on internally:
```
AttributeError: module 'pkgutil' has no attribute 'ImpImporter'
```
This confirmed the downgrade path was a dead end — the original PyPI `hdlparse` package is fundamentally incompatible with a modern Python + setuptools stack, in two independent ways. `setuptools` was restored to latest (`84.0.0`).

**Actual fix:** A maintained fork of `hdlparse` exists that removes the Python 2 / `2to3` dependency entirely: [`github.com/hdl/pyHDLParser`](https://github.com/hdl/pyHDLParser).
```bash
pip3 install --upgrade "https://github.com/hdl/pyhdlparser/tarball/master" --break-system-packages
```
Result: `Successfully installed hdlparse-1.0.7` (fork version; the abandoned PyPI package was `1.0.1`).

**Recommendation for maintainers:** eSim's `requirements`/setup documentation should either pin the working fork (`hdl/pyHDLParser`) directly, or vendor a small compatible verilog/VHDL parser, since the PyPI `hdlparse` dependency is permanently broken on any current Python toolchain.

**Status:** ✅ All four sub-dependencies fixed. This was the deepest and most technically involved fix in this task, and directly unblocked the eSim GUI launch chain.

---

## Issue 5 — `.esim` config directory not created, workspace selection crashes

**Severity: High — this also directly blocks the GUI on first launch.**

**Symptom:**
After all Python dependencies were resolved and the launcher reached the workspace-selection dialog, clicking "OK" produced:
```
FileNotFoundError: [Errno 2] No such file or directory: '/home/lutfullah/.esim/workspace.txt'
```

**Root cause:**
`src/frontEnd/Workspace.py` (`createWorkspace`, line 133) attempts to write directly to `~/.esim/workspace.txt` without first checking whether the parent directory `~/.esim` exists. On a first-time install, this directory has never been created, so the `open(..., 'w')` call fails outright.

**Fix:**
```bash
mkdir -p ~/.esim
```
This should ideally be handled inside `Workspace.py` itself (e.g. `os.makedirs(os.path.dirname(path), exist_ok=True)` before opening the file) rather than requiring the user to pre-create it — noting this as a recommended code-level fix for maintainers.

**Verification:** After creating the directory, `bash launcher-esim.sh` → workspace dialog → "OK" completed without error, and the full eSim-2.5 GUI loaded successfully.

**Status:** ✅ Fixed (workaround applied; root cause and a suggested proper code fix documented above for maintainers).

---

## Final Result — eSim GUI Successfully Launched

After resolving Issues 1, 3, 4, and 5, running `bash launcher-esim.sh` from a completely clean Ubuntu 26.04 VM completes the entire chain — Snap-path resolution, all four Python dependencies, and workspace initialization — and launches the full eSim-2.5 main window with no errors:

![eSim-2.5 GUI launched successfully — final proof](images/final-esim-gui-launched.png)

Terminal output confirms:
```
eSim Started......
Project Selected : None
[INFO]: Workspace : /home/lutfullah/eSim-Workspace
```

## Impact

Before these fixes, a first-time contributor following the official `INSTALL` + `setup-esim.sh` + `launcher-esim.sh` flow on a current Ubuntu system would fail at **five separate points** before ever seeing the eSim GUI. After these fixes, all five issues are either resolved or clearly reported with a concrete recommendation, and the main eSim GUI launches end-to-end and is verified working.

## Links

- Forked repository: https://github.com/Lutfullah07/eSim
- Pull Request: https://github.com/FOSSEE/eSim/pull/635
- Report: https://github.com/Lutfullah07/eSim/blob/master/TASK4_REPORT.md
