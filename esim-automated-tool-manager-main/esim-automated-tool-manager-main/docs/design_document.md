# Automated Tool Manager for eSim

## Overview

eSim is an open-source Electronic Design Automation (EDA) tool used for circuit design, simulation, analysis, and PCB design. To work correctly, eSim depends on several external tools such as **Ngspice** and **KiCad**, along with system dependencies like **Python** and **Git**.

Many users face issues while setting up eSim because required tools are missing, not available in the system PATH, or incompatible in version. Identifying and fixing these issues manually is time-consuming and error-prone.

This project provides a **Python-based Automated Tool Manager for eSim** that helps users verify system readiness and safely manage external tools before running eSim.

---

## What This Tool Does

The Automated Tool Manager performs the following actions:

- Detects whether **Ngspice** and **KiCad** are installed  
- Displays the installed versions of detected tools  
- Checks essential system dependencies (**Python** and **Git**)  
- Automatically installs tools on **Linux** using the system package manager (`apt`)  
- Provides **guided installation instructions** on Windows  
- Checks whether the installed tool versions match **recommended versions**  
- Identifies PATH-related configuration issues  
- Logs all actions, checks, and errors  

---

## Version Update Check (Important Clarification)

The tool includes a **version update recommendation system**.

### What it DOES
- Detects the currently installed version of a tool  
- Compares it with a **recommended version** defined inside the tool  
- Informs the user if an update is **recommended for compatibility**

### What it DOES NOT do
- It does **not force updates**
- It does **not automatically upgrade or downgrade tools**
- It does **not modify the system silently**

This design choice ensures **system safety**, avoids permission issues, and keeps the tool suitable for cross-platform use.

---

## Why This Tool Is Useful

- Prevents common setup and configuration errors  
- Saves time by automating dependency checks  
- Improves reliability through version validation  
- Avoids unsafe system-level changes  
- Designed to be modular and extensible  

---

## How to Use

### Check system readiness
```bash
python cli.py --check 
---
```

## 6. Module Description

### Command Line Interface (CLI)
Provides user interaction using command-line flags for checking, installing, and update validation.

### Tool Detection Module
Detects whether external tools are installed and retrieves version information.

### Dependency Checker Module
Validates availability of system dependencies such as Python and Git.

### Installer Module
Automatically installs tools on Linux using apt and provides guided installation instructions on Windows.

### Update Checker Module
Compares installed tool versions with recommended versions to identify compatibility issues.

### Configuration Manager
Checks whether detected tools are available in the system PATH and provides guidance if misconfigured.

### Logger Module
Records all actions, errors, and system responses in a log file.

---

## 7. Design Decisions and Rationale

- A CLI-based approach was chosen to keep the tool lightweight and cross-platform.
- Automatic installation is enabled only on Linux to avoid permission and system risks.
- Version enforcement is limited to detection and recommendation to ensure safety.
- Modular architecture allows easy extension during future development or internship work.

---

## 8. Technologies Used

- Python 3
- Windows / Linux Operating Systems
- argparse
- subprocess
- logging
- colorama

---

## 9. Future Enhancements

- GUI-based interface
- macOS package manager integration
- Full automatic updates
- Configuration auto-fix for PATH variables
- Tool version pinning

---

## 10. Sample Input and Output

### System Readiness Check

```bash
python cli.py --check
```

```
✔ Ngspice installed
  Version: ngspice-39

✖ KiCad not installed
  Hint: Install and add to PATH

✔ Python available
✔ Git available
```

---

### Tool Installation (Linux Only)

```bash
python cli.py --install ngspice
```

```
ℹ Attempting to install Ngspice using apt...
✔ Ngspice installation completed successfully
```

---

### Tool Update Recommendation Check

```bash
python cli.py --update-check Ngspice
```

```
✖ Ngspice update recommended → version 39
```

```
✔ Ngspice is up to date
```


## 11. Conclusion

The Automated Tool Manager for eSim provides a safe, modular, and extensible solution for verifying and managing external tools required by eSim. It focuses on correctness, usability, and system safety, making it suitable as a screening-level prototype and a foundation for future enhancements.
