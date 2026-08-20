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
6. Progress was verified at each step via terminal output (screenshots retained in `images/` for reference).

---

## Summary Table

| # | Issue | Blocks Main GUI? | Status | Difficulty |
|---|---|---|---|---|
| 1 | `setup-esim.sh` — broken `$SNAP`-based path, library setup fails | Indirect (breaks library setup step) | ✅ Fixed | Medium |
| 2 | `install-eSim.sh` referenced in `INSTALL` does not exist in source repo | No (blocks first-time users following docs) | ⚠️ Reported | Low–Medium |
| 3 | `launcher-esim.sh` — broken `$SNAP`-based path, GUI launcher fails | **Yes — directly blocks GUI launch** | ✅ Fixed | Medium |
| 4 | Python dependency chain missing (PyQt6 → numpy → matplotlib → hdlparse) | **Yes — directly blocks GUI launch** | ✅ Fixed (4/4 resolved) | **High** |

**Total issues reported: 4 (across 7 distinct root causes, since Issue 4 bundles 4 sub-dependencies)**
**Total issues fixed: 3 of 4 top-level issues (Issue 2 intentionally left to maintainers — see below)**

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

**Verification:**
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

**Symptom:**
```
launcher-esim.sh: line 10: /usr/bin/setup-esim.sh: No such file or directory
launcher-esim.sh: line 11: cd: /eSim/src/frontEnd: No such file or directory
python3: can't open file '.../Application.py': No such file or directory
```

**Root cause:**
Identical `$SNAP` pattern as Issue 1, but here it breaks the **actual GUI entry point**. `cd "$SNAP/eSim/src/frontEnd"` collapses to `cd /eSim/src/frontEnd` on a source install, which does not exist. The real entry point is at `<repo-root>/src/frontEnd/Application.py`.

**Fix:**
Rather than bypassing the launcher script, it was edited to resolve the path correctly at runtime, so the official launcher itself works for source installs:

- Commented out the Snap-only line `$SNAP/usr/bin/setup-esim.sh` (not applicable outside Snap).
- Changed `cd $SNAP/eSim/src/frontEnd` to:
  ```bash
  cd "$(dirname "$(pwd)")/src/frontEnd"
  ```

**Verification:** After the fix, `bash launcher-esim.sh` correctly reaches and executes `Application.py` (confirmed by a new, unrelated error appearing — i.e., the path-resolution problem was fully eliminated, and execution moved on to the next real issue, documented as Issue 4).

**Status:** ✅ Fixed, committed, and pushed to `scripts/launcher-esim.sh`.

---

## Issue 4 — Missing Python Dependency Chain (blocks GUI launch) — HIGHEST WEIGHTAGE

**Severity: Highest — per the evaluation criteria, this is a dependency chain that interrupts installation of the *main GUI* of eSim, not a smaller sub-block like NgVeri.**

Once Issue 3 was resolved, `Application.py` began executing but failed repeatedly as it hit successive missing Python modules. Each was diagnosed and resolved in sequence:

### 4.1 — `PyQt6` missing
```
ModuleNotFoundError: No module named 'PyQt6'
```
Root cause: Qt6 Python bindings (the GUI toolkit eSim's frontend is built on) and `pip3` itself were not present on a clean system.
Fix:
```bash
sudo apt install python3-pip -y
pip3 install PyQt6 --break-system-packages
```

### 4.2 — `numpy` missing
```
ModuleNotFoundError: No module named 'numpy'
```
Fix:
```bash
pip3 install numpy --break-system-packages
```

### 4.3 — `matplotlib` missing
```
ModuleNotFoundError: No module named 'matplotlib'
```
(raised from `src/ngspiceSimulation/plot_window.py`, which imports `matplotlib.pyplot`)
Fix:
```bash
pip3 install matplotlib --break-system-packages
```

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

## Impact

Before these fixes, a first-time contributor following the official `INSTALL` + `setup-esim.sh` + `launcher-esim.sh` flow on a current Ubuntu system would fail at **five separate points** before ever seeing the eSim GUI. After these fixes:

- Library setup (`setup-esim.sh`) completes cleanly.
- The GUI launcher correctly resolves paths on a source install.
- All four blocking Python dependencies are installed and resolved with documented, verified fixes.
- One remaining issue (`install-eSim.sh` doc mismatch) is clearly reported with a concrete recommendation for maintainers.

## Links

- Forked repository: https://github.com/Lutfullah07/eSim
- Pull Request: *(https://github.com/FOSSEE/eSim/pull/635)*
- Modified files: `scripts/setup-esim.sh`, `scripts/launcher-esim.sh`, `TASK4_REPORT.md`
