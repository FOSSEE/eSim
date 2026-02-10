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
