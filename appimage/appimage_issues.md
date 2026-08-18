# eSim AppImage: Encountered Issues and Errors

This document details the issues and error messages encountered during the build and runtime phases of the eSim AppImage on modern Linux environments (specifically tested on Ubuntu 26.04 Resolute with Wayland).

---

## 1. Missing Python Packages (PyQt5 Dependency)
### Error Message
```
Traceback (most recent call last):
  File "/tmp/.mount_eSimXXXXXX/usr/bin/esim", line 3, in <module>
    from PyQt5.QtWidgets import QApplication
ModuleNotFoundError: No module named 'PyQt5'
```

### Context & Root Cause
Originally, the AppImage did not package its own Python environment or dependencies (like PyQt5). Instead, the `AppRun` entry point relied on the host system's Python interpreter (`/usr/bin/python3`) and attempted to run pip installation at runtime or assume that PyQt5 was installed on the host system. This failed because:
- Host systems may restrict ad-hoc package installations due to **PEP 668 (system-managed environments)**.
- Mismatched host Python versions caused binary package incompatibilities.
- The AppImage was not truly self-contained or portable.

---

## 2. APT Package Installation Failures (Build-time Dependency)
### Error Message
```
E: Unable to locate package libgdk-pixbuf2.0-dev
```

### Context & Root Cause
During the prerequisite installation stage on newer Ubuntu/Debian releases, the build script failed because package names had changed in the upstream repositories (e.g., `libgdk-pixbuf2.0-dev` became `libgdk-pixbuf-2.0-dev`). Hardcoded package names in the build script broke support on newer distributions.

---

## 3. Qt Platform Plugin Initialization Failure (XCB)
### Error Message
```
qt.qpa.plugin: Could not load the Qt platform plugin "xcb" in "" even though it was found.
This application failed to start because no Qt platform plugin could be initialized. Reinstalling the application may fix this problem.

Available platform plugins are: eglfs, linuxfb, minimal, minimalegl, offscreen, vnc, wayland-egl, wayland, wayland-xcomposite-egl, wayland-xcomposite-glx, webgl, xcb.
```

### Context & Root Cause
The host environment was running a **Wayland** session (`XDG_SESSION_TYPE=wayland`). However, Qt5 defaults to the `xcb` (X11) platform plugin. Inside the AppImage container's execution sandbox, the host's X11/XCB libraries were either missing or misaligned with the loader's library path (`LD_LIBRARY_PATH`), causing the `libqxcb.so` plugin to fail to load.

---

## 4. Incompatible Qt Libraries (Qt Version Mismatch)
### Error Message
```
Cannot mix incompatible Qt library (5.15.19) with this library (5.15.18)
Aborted (core dumped)
```

### Context & Root Cause
When trying to run the Wayland platform plugin bundled with the PyQt5 wheel (`libqwayland-generic.so`), Qt attempted to resolve its dependencies. The bundled PyQt5 was compiled against Qt **5.15.19**, but the host system had Qt **5.15.18** installed. Because the host's `/usr/lib/x86_64-linux-gnu` took precedence in `LD_LIBRARY_PATH` over the PyQt5-specific directories, the dynamic linker loaded the host's older `libQt5Core.so.5`, causing a critical version conflict.
