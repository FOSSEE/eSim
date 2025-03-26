# eSim Tool Manager for Windows

---

This Tool Manager allows you to manage, install, and update essential tools such as **Ngspice**, **KiCad**, **GHDL**, and more for eSim on **Windows**.

## 1. Download and Install eSim

1. Download eSim from the official website:  
   https://esim.fossee.in/downloads

2. Run the Windows installer and complete the installation.

3. By default, eSim will be installed at: C:\FOSSEE

---

## 2. Set Up Tool Manager

1. Download the Tool Manager ZIP package.

2. Extract it into the `C:\FOSSEE` directory, **alongside**:
- `eSim`
- `KiCad`
- `MSYS`
- `nghdl-simulator`

Your folder structure should look like this:
eSim, KiCad, MSYS, nghdl-simulator and Tool-Manager folders under the C:\FOSSEE.

---

## 3. Run Tool Manager

1. Open a terminal (Command Prompt or PowerShell).

2. Navigate to the Tool Manager directory:

```bash
cd C:\FOSSEE\Tool-Manager
```

3. Run the following command:

```bash
python main.py
```

Use the GUI to view, install, or update tools as needed.


## 4. Manual Package Download (If Automated Download Fails)

If automatic package downloads fail, you can manually download the necessary packages and 
place them in the appropriate folder.

Download Links & Saved Filename

[ghdl-v4.1.0.pkg.tar.zst](https://github.com/ghdl/ghdl/releases/download/v4.1.0/mingw-w64-x86_64-ghdl-llvm-ci-1-any.pkg.tar.zst)

[ghdl-v4.0.0.pkg.tar.zst](https://github.com/ghdl/ghdl/releases/download/v4.0.0/mingw-w64-x86_64-ghdl-llvm-ci-1-any.pkg.tar.zst)

[ghdl-v3.0.0.pkg.tar.zst](https://github.com/ghdl/ghdl/releases/download/v3.0.0/mingw-w64-x86_64-ghdl-llvm-ci-1-any.pkg.tar.zst)

[kicad-7.0.11.exe](https://downloads.kicad.org/kicad/windows/explore/stable/download/kicad-7.0.11-rc3-x86_64.exe)

[kicad-8.0.9.exe](https://downloads.kicad.org/kicad/windows/explore/stable/download/kicad-8.0.9-x86_64.exe)

Place all downloaded files in the appropriate folder, such as:

C:\FOSSEE\Tool-Manager\packages\

---
