# Task 2 – eSim Upgradation (Ubuntu 23.04 Compatibility Fix)

## ❌ Problem Statement:
eSim (Electronics Simulation Software), developed by FOSSEE, has installation issues on **Ubuntu 23.04**. The main reason for the failure is that the **`llvm-9`** and **`llvm-9-dev`** packages—required by NGHDL and GHDL—are no longer available in the official Ubuntu repositories. The `nghdl-install.sh` and `eSim-install.sh` scripts fail when they attempt to install or reference these outdated packages.

---

## ✅ Solution Overview:
To ensure successful installation and execution of eSim on Ubuntu 23.04, I upgraded the toolchain and modified relevant scripts to be compatible with newer versions of Ubuntu and its available packages.

---

## 🔁 Step-by-Step Work Done:

### 🧩 Step 1: Initial Problem Analysis
- Cloned the original eSim repository and ran `install-eSim.sh`.
- Faced error due to missing `llvm-9` in both:
  - `nghdl-install.sh`
  - `eSim-install.sh`

### 🔧 Step 2: LLVM Upgrade Attempt
- Noticed that `llvm-9` is **deprecated** in Ubuntu 23.04.
- Tried installing `llvm-9` manually, but the installer aborted with an error.
- Replaced it with **`llvm-15`** and **`llvm-15-dev`** in the scripts:
  - Modified `nghdl-install.sh` to use `llvm-15` (available via APT).
  - Updated `$PATH` and `$LD_LIBRARY_PATH` to point to the new LLVM setup.

### 🔁 Step 3: GHDL Upgrade
- Old GHDL version in eSim used LLVM-9 backend.
- Cloned and built **GHDL `6.0.0-dev`** from source using:
  - LLVM-15 backend
  - GNAT 10.5.0
- Installed GHDL in a local directory: `~/ghdl/`
- Added `~/ghdl/bin` to `PATH` for proper GHDL usage across eSim.

### 🛠️ Step 4: Verilator Upgrade
- Updated Verilator to a newer version (manually built) to match latest simulation requirements.
- Ensured Verilator was installed system-wide and available in `PATH`.

### 🪛 Step 5: Script Fixes
- **`nghdl-install.sh`:**
  - Replaced LLVM-9 dependencies with LLVM-15.
  - Adjusted paths to use custom GHDL.
  - Verified NGHDL builds without issues.

- **`eSim-install.sh`:**
  - Attempted to remove LLVM-9 dependency here as well.
  - However, the script still references `llvm-9`, likely from internal scripts or unpatched variables.
  - Even after editing, the installer tries to fetch `llvm-9`, causing the whole process to abort.
  - I am currently tracing the root source of this reference to patch it effectively.

### ✅ Step 6: Testing and Verification
- After script changes:
  - Successfully compiled NGHDL.
  - Verified GHDL works using LLVM-15.
  - eSim GUI opens and runs.
  - Basic VHDL simulations tested and validated.
  - Custom GHDL and Verilator versions integrated into the eSim ecosystem.

---

## 🛠️ Tools & Environment:
| Tool            | Version                  |
|-----------------|--------------------------|
| **Ubuntu**      | 23.04 (Lunar Lobster)    |
| **GHDL**        | 6.0.0-dev (LLVM backend) |
| **LLVM**        | 15                       |
| **GNAT**        | 10.5.0                   |
| **Verilator**   | Latest (from source)     |
| **NGHDL**       | Patched from source      |
| **eSim**        | 2.4                      |

---

## 🧪 Testing Results:
| Component       | Status      | Notes                                           |
|------------------|-------------|--------------------------------------------------|
| GHDL 6.0.0-dev   | ✅ Working   | Built using LLVM 15 backend                      |
| NGHDL            | ✅ Working   | Installed successfully with updated LLVM paths  |
| eSim GUI         | ✅ Working   | Opens and simulates with NGHDL backend          |
| Simulations      | ✅ Verified  | Ran basic circuits to ensure full functionality |

---

## 📂 Modified Files:
- `nghdl-install.sh`
- (Partially) `eSim-install.sh` – further work needed to patch LLVM-9 dependency completely

---

## ⚠️ Current Limitation:
- Even after replacing `llvm-9` with `llvm-15`, the `eSim-install.sh` script **still references `llvm-9`** from an unknown location.
- This causes the **entire installation to abort**, despite the rest of the environment being compatible.
- Need to **trace the legacy `llvm-9` reference** (possibly hardcoded or from a sourced script) and remove it fully to finalize the patch.
![GitHub release (latest by date)](https://img.shields.io/github/v/release/fossee/esim?color=blueviolet)
![GitHub](https://img.shields.io/github/license/fossee/esim?color=blue)
![Python](https://img.shields.io/badge/python-v3.6+-blue.svg)
[![PEP8](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)
![Travis (.com)](https://img.shields.io/travis/com/Eyantra698Sumanto/eSim)
[![Documentation Status](https://readthedocs.org/projects/esim/badge/?version=latest)](https://esim.readthedocs.io/en/latest/?badge=latest)
[![GitHub forks](https://img.shields.io/github/forks/fossee/esim)](https://github.com/fossee/esim/network)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat)](https://github.com/fossee/esim)
![GitHub contributors](https://img.shields.io/github/contributors/fossee/esim)

## eSim

[eSim](https://esim.fossee.in/) is an open source EDA tool for circuit design, simulation, analysis and PCB design, developed by [FOSSEE Team](https://www.fossee.in/) at [IIT Bombay](https://www.iitb.ac.in/).
It is an integrated tool build using open source softwares such as KiCad, Ngspice and GHDL.

## Releases and Installation
eSim is released for the following distributions (operating systems):
* Ubuntu 22.04, 23.04, 24.04 LTS versions.
* Microsoft Windows 8, 10 and 11.

To use eSim on your machine having above distributions, please refer to link [here](https://esim.fossee.in/downloads) for installation and other guidelines.

> Note for other distributions: You can refer [`installers`](https://github.com/fossee/eSim/tree/installers) branch for documentation on packaging (for above mentioned distributions) to build installers for your operating system in a similar way. For providing your build, please check the `Contribution` section mentioned below.

## Features
* An open-source EDA tool.
* Perform Circuit Design.
* Perform Simulation.
* Perform Layout Design.
* Model and Subcircuit builder.
* Support for Mixed-Signal Simulations including Microcontrollers.
* eSim has been successfully ported to low cost FOSSEE [laptop](https://laptop.fossee.in/)

## Open-Source Softwares Used
* [Python](https://www.python.org/)
* [KiCad](https://www.kicad.org/)
* [NGHDL](https://github.com/fossee/nghdl/)
* [Makerchip](https://www.makerchip.com/)
* [SkyWater SKY130 PDK](https://skywater-pdk.rtfd.io/)

## eSim Manual
To know everything about eSim, how it works and it's feature please download the manual from [here](https://static.fossee.in/esim/manuals/eSim_Manual_2.5.pdf)

## Contact
For any queries regarding eSim please write us on at this [email address](mailto:contact-esim@fossee.in).

Other Contact Details are available [here](https://esim.fossee.in/contact-us).

## Contribution
Please refer [here](https://github.com/FOSSEE/eSim/blob/master/CONTRIBUTION.md) for further details.

## License
It is developed by FOSSEE Team at IIT Bombay and is released under GNU GPL License.