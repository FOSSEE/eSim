eSim Packaging
====

It contains all the documentation for packaging eSim for distribution.


# Packaging eSim for Distribution:

1. eSim is currently packaged and distributed for Ubuntu OS (Linux) and MS Windows OS.

2. Refer the [documentation](Version_Change.md) for the changes to be done when a new release is to be made.

> Note: These changes have to be made `first` before proceeding with the packaging on either platform.

3. Refer the [documentation](Ubuntu/README.md) to package eSim for Ubuntu OS.

4. Refer the [documentation](Windows/README.md) to package eSim for Windows OS.

# 📦 Tool Manager for eSim – Multi-Platform Support

This repository contains platform-specific versions of the **Tool Installation and Management System** for eSim. It supports installing, updating, and managing tools like **Ngspice**, **KiCad**, **GHDL**, **Verilator**, and more.

---

## 📁 Folder Structure

- `Ubuntu/` – Tool Manager for standard Ubuntu installations  
- `Ubuntu-Standalone/` – Standalone version for Ubuntu using APT  
- `Windows/` – Tool Manager (Updater) for standard eSim Windows installation  
- `Windows-Standalone/` – Standalone version for Windows using Chocolatey

---

## 📖 Installation Instructions

- **Ubuntu:**  
  Refer to the [`INSTALL-TOOLMANAGER`](./Ubuntu/INSTALL-TOOLMANAGER) file inside the `Ubuntu/` folder for complete setup instructions.

- **Ubuntu-Standalone:**  
  Open the `Ubuntu-Standalone/README.md` for instructions specific to the standalone version.

- **Windows:**  
  See `Windows/README.md` for installation steps when using Tool Manager with an existing eSim installation.

- **Windows-Standalone:**  
  Refer to `Windows-Standalone/README.md` for using the standalone version with Chocolatey support.

---

## 📥 Download Instructions

You can download the ZIP file for any specific platform folder (`Ubuntu`, `Ubuntu-Standalone`, `Windows`, `Windows-Standalone`) separately and follow the instructions inside.

Make sure to read the corresponding `README.md` or `INSTALL-TOOLMANAGER` for proper setup.

---

## 🔗 eSim Official Website

For more details about eSim, visit:  
👉 [https://esim.fossee.in](https://esim.fossee.in)

---
