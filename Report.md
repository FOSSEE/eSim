# Task 2 – eSim Upgradation (Ubuntu 23.04 Fix)

## ❌ Issue:
- eSim’s `nghdl-install.sh` fails on Ubuntu 23.04 because `llvm-9` & `llvm-9-dev` are not available in official repositories.

## ✅ Fix:
- Updated the script to use `llvm-15` & `llvm-15-dev`, which are available and compatible with newer versions of GHDL.
- Also tested compatibility with GHDL 6.0.0-dev built with GNAT 10.5.0.

## 🛠️ Modified File:
- `nghdl-install.sh`

## 🔧 Tools Used:
- Ubuntu 23.04
- Bash
- GitHub
- Manual installation tests

## 👨‍💻 Author:
- Rishabh
- GitHub: https://github.com/RISHABH12005
