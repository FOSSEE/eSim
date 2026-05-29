# eSim – Ubuntu 25.04 Support Report

This report documents the issues faced while installing **eSim** and its dependency **nghdl** on Ubuntu 25.04, along with the fixes implemented.

---

## 🔧 nghdl

### 1. LLVM

* **Issue:**
  GHDL does not support the latest version of LLVM (`llvm-20.1`) available in Ubuntu 25.04.
* **Fix:**
  Modified the installer script to install `llvm-18.1`, which is supported.

---

### 2. InstallGHDL

* **Issue:**
  The installer script uses `/usr/bin/llvm-config` assuming `llvm-20.1`.
  Example command:

  ```bash
  ./configure --with-llvm-config=/usr/bin/llvm-config
  ```
* **Fix:**
  Replaced with the correct path for LLVM 18.1:

  ```bash
  ./configure --with-llvm-config=/usr/bin/llvm-config-18
  ```

---

### 3. Gtk Canberra

* **Issue:**
  `libcanberra-gtk-module` package is no longer available in Ubuntu 25.04.
* **Fix:**
  Modified installer to use only `libcanberra-gtk3-module`.

---

## 🔧 eSim

### 1. install-eSim.sh

* **Issue:**
  Ubuntu 25.04 was not supported in the main installer script.
* **Fix:**
  Added Ubuntu 25.04 support.

---

### 2. New Installer Script

* **Added:**
  `install-eSim-scripts/install-eSim-25.04.sh`

* **Differences from `install-eSim-24.04.sh`:**

  #### installKicad function:

  * Defines PPA for Ubuntu 25.04:

    ```bash
    ppa:kicad/kicad-8.0-releases
    ```

    (same as Ubuntu 24.04).
  * Installed specific version:

    ```bash
    kicad=8.0.8+dfsg-1
    ```

    instead of the latest version (latest causes dependency issues with `libgit2-1.8`).

---
