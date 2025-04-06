# Task 2 – eSim Upgradation (Ubuntu 23.04 Compatibility Fix)

## ❌ Problem Statement:
eSim, an open-source EDA tool developed by FOSSEE (IIT Bombay), currently fails to install properly on **Ubuntu 23.04**. The failure occurs primarily due to missing dependencies—specifically, **`llvm-9`** and **`llvm-9-dev`**—which are no longer available in the official Ubuntu repositories.

The problem becomes evident during the execution of the **`nghdl-install.sh`** script, which attempts to fetch and build NGHDL using these outdated LLVM packages. As a result, the installation breaks and users are unable to use NGHDL-related simulation features.

---

## ✅ Solution Overview:
To resolve this issue and ensure compatibility with modern systems, I performed the following updates and tests:

- Replaced all references to **`llvm-9`** and **`llvm-9-dev`** in the `nghdl-install.sh` script with **`llvm-15`** and **`llvm-15-dev`**, which are available and stable in Ubuntu 23.04 repositories.
- Verified compatibility by:
  - Compiling the **latest development version of GHDL (`6.0.0-dev`)** using the LLVM backend and GNAT 10.5.0.
  - Reconfiguring the installation script to use the **locally built version of GHDL** from `~/ghdl/bin`.
  - Ensuring NGHDL compiles and integrates correctly without dependency errors.

---

## 🛠️ Tools & Environment:
| Tool            | Version                  |
|-----------------|--------------------------|
| **Ubuntu**      | 23.04 (Lunar Lobster)    |
| **GHDL**        | 6.0.0-dev (LLVM backend) |
| **LLVM**        | 15                       |
| **GNAT**        | 10.5.0                   |
| **NGHDL**       | From eSim repo           |
| **Bash**        | v5.2                     |
| **Git**         | Latest from APT          |

---

## 🔧 Key File Modified:
- [`nghdl-install.sh`](https://github.com/RISHABH12005/esim-nghdl-patch/blob/main/nghdl-install.sh)  
  - Replaced `llvm-9` with `llvm-15`
  - Modified `$PATH` and `$LD_LIBRARY_PATH` to include custom GHDL build (`~/ghdl`)
  - Removed hardcoded dependency assumptions

---

## 🧪 Testing Results:
| Component     | Status     | Notes                                           |
|---------------|------------|-------------------------------------------------|
| GHDL 6.0.0-dev | ✅ Working  | Built using LLVM 15 backend                     |
| NGHDL         | ✅ Working  | Installed successfully with updated LLVM paths |
| eSim GUI      | ✅ Working  | No crashes or backend issues                   |
| Simulations   | ✅ Verified | Basic VHDL simulations tested in GUI + NGHDL   |

---

## 👨‍💻 Author:
- **Name:** Rishabh  
- **GitHub:** [@RISHABH12005](https://github.com/RISHABH12005)

---

## 📁 Repository:
You can find the updated script and step-by-step instructions here:  
🔗 **[GitHub Repo – eSim Ubuntu 23.04 Fix](https://github.com/RISHABH12005/esim-nghdl-patch)**
