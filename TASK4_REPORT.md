# Task 4 Execution Report

## Overview
This report details the diagnostics and fixes applied to the eSim build and launch environment.

---

## 📸 Visual Verification & Evidence (Screenshots)

The following sequence of screenshots documents the step-by-step diagnostic and resolution process for Task 4 issues:

| Figure | Evidence Screenshot | Diagnostic & Resolution Context |
| :---: | :--- | :--- |
| **Figure 1** | ![Issue 4 Evidence](images/Screenshot%202026-08-20%20014520.png) | **Issue 4 Identification:** `INSTALL` documentation search failing to locate missing `install-esim.sh`. |
| **Figure 2** | ![Issue 1 Path Inspection](images/Screenshot%202026-08-20%20020543.png) | **Issue 1 & 3 Root Cause:** `cat launcher-esim.sh` revealing unpopulated `$SNAP` environment variables. |
| **Figure 3** | ![Launcher Crash](images/Screenshot%202026-08-20%20020632.png) | **Issue 1 Launcher Failure:** Initial execution crash due to missing `/usr/bin/setup-esim.sh` and invalid frontend path. |
| **Figure 4** | ![Path Trace](images/Screenshot%202026-08-20%20021032.png) | **Issue 1 Path Diagnosis:** Tracing real application entrypoint at `src/frontEnd/Application.py`. |
| **Figure 5** | ![PyQt6 Missing](images/Screenshot%202026-08-20%20021807.png) | **Issue 2 Dependency Error:** Launcher execution revealing `ModuleNotFoundError: No module named 'PyQt6'`. |
| **Figure 6** | ![Pip Setup](images/Screenshot%202026-08-20%20022113.png) | **Issue 2 Environment Setup:** Resolving missing `python3-pip` packaging tools. |
| **Figure 7** | ![PyQt6 Downloading](images/Screenshot%202026-08-20%20022719.png) | **Issue 2 Resolution:** Installing `PyQt6` binaries via `pip3 install --break-system-packages`. |
| **Figure 8** | ![PyQt6 Installed](images/Screenshot%202026-08-20%20022805.png) | **Issue 2 Verification:** Successful completion of `PyQt6` module installation. |
| **Figure 9** | ![NumPy Missing](images/Screenshot%202026-08-20%20023035.png) | **Issue 2 Secondary Dependency:** Sub-system execution revealing missing `numpy` requirement. |
| **Figure 10** | ![NumPy Installed](images/Screenshot%202026-08-20%20023145.png) | **Issue 2 Final Verification:** Successful installation of `numpy-2.5.2`. |

