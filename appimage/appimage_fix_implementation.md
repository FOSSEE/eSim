# eSim AppImage: Fixes and Implementation Approach

This document explains the technical details, implementation plan, and approach used to resolve build-time and runtime issues for the eSim AppImage.

---

## 1. Portable Python & Dependency Bundling
### Approach
To bypass host-system Python version mismatches and restrictions like PEP 668 (system-managed environments), we integrated a fully self-contained Python interpreter into the AppImage bundle.

### Implementation
- During build time, the build script downloads a pre-compiled, portable CPython distribution (`python-build-standalone` version 3.12.1).
- It extracts this distribution to `$APPDIR/usr/python`.
- The build script installs all Python dependencies (including `PyQt5`, `hdlparse`, and others) directly into this bundled Python environment.
- At runtime, the `AppRun` launcher configures python env variables:
  ```bash
  export PYTHONHOME="${HERE}/usr/python"
  export PYTHONPATH="${HERE}/usr/share/eSim/src"
  export PATH="${HERE}/usr/python/bin:${PATH}"
  ```
- This completely eliminates dependency on the host's python interpreter or internet access for pip packages at runtime.

---

## 2. Dynamic APT Package Detection
### Approach
To make the build script compatible across multiple generations of Debian and Ubuntu releases, we replaced hardcoded package lists with dynamic package detection.

### Implementation
- We updated the `install_deps_apt` function in `build-appimage.sh` to query package managers:
  ```bash
  install_gdk_pixbuf() {
      if apt-cache show libgdk-pixbuf-2.0-dev >/dev/null 2>&1; then
          sudo apt-get install -y libgdk-pixbuf-2.0-dev
      elif apt-cache show libgdk-pixbuf2.0-dev >/dev/null 2>&1; then
          sudo apt-get install -y libgdk-pixbuf2.0-dev
      fi
  }
  ```
- This ensures the build process automatically adapts to changing package nomenclature upstream.

---

## 3. Runtime Qt Platform Server Auto-Detection
### Approach
To support both modern Wayland-based desktops (like Ubuntu 22.04+ and 26.04 GNOME) and older X11-based desktops, we added a runtime display server detector to the main `AppRun` launcher.

### Implementation
- Added detection code in the `AppRun` heredoc:
  ```bash
  if [ -z "${QT_QPA_PLATFORM}" ]; then
      if [ -n "${WAYLAND_DISPLAY}" ] && [ "${XDG_SESSION_TYPE}" = "wayland" ]; then
          export QT_QPA_PLATFORM=wayland
      elif [ -n "${DISPLAY}" ]; then
          export QT_QPA_PLATFORM=xcb
      else
          export QT_QPA_PLATFORM=xcb
      fi
  fi
  ```
- Pointed the Qt platform plugins engine to the bundled plugins directory from PyQt5:
  ```bash
  PYQT5_QT_PLUGINS="${HERE}/usr/python/lib/python3.12/site-packages/PyQt5/Qt5/plugins"
  if [ -d "${PYQT5_QT_PLUGINS}" ]; then
      export QT_PLUGIN_PATH="${PYQT5_QT_PLUGINS}:${HERE}/usr/lib/qt5/plugins:${QT_PLUGIN_PATH}"
  else
      export QT_PLUGIN_PATH="${HERE}/usr/lib/qt5/plugins:${QT_PLUGIN_PATH}"
  fi
  ```

---

## 4. Resolving Qt Library Version Conflicts
### Approach
We isolated the AppImage's Qt plugins from host system libraries by forcing the dynamic linker to prioritize the bundled PyQt5 Qt libraries.

### Implementation
- Prepend the PyQt5 Qt5 library directory to `LD_LIBRARY_PATH` inside `AppRun`:
  ```bash
  _PYQT5_QT_LIB="${HERE}/usr/python/lib/python3.12/site-packages/PyQt5/Qt5/lib"
  if [ -d "${_PYQT5_QT_LIB}" ]; then
      export LD_LIBRARY_PATH="${_PYQT5_QT_LIB}:${LD_LIBRARY_PATH}"
  fi
  ```
- This forces the system loader to resolve dependencies for `libqwayland-generic.so` and `libqxcb.so` against the bundled Qt libraries (`5.15.19`) instead of mixing them with host Qt libraries (like `5.15.18` on the host).
