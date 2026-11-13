# eSim 2.5 on Ubuntu 25.04: installation fixes

| # | Issue | Fix |
|---|-------|-----|
| 1 | Syntax error in install-eSim.sh | Removed stray code, closed the `if` |
| 2-3 | No 25.04 support; empty version | Use 25.04 script; version via lsb_release -rs |
| 4 | `exit 0` in installKicad | `return 0` |
| 5 | NGHDL has no 25.04 case | Added case + script |
| 6 | libcanberra-gtk-module missing | libcanberra-gtk3-module |
| 7 | GHDL 4.1.0 rejects LLVM 20 | Use LLVM 18 |

## How to reproduce
1. Download and unzip eSim 2.5 from https://esim.fossee.in/downloads
2. Copy `install-eSim.sh` and `install-eSim-scripts/` from this folder into it
3. Replace `nghdl/install-nghdl.sh` and add `install-nghdl-25.04.sh` inside nghdl.zip
4. Run `./install-eSim.sh --install`

Full report: report/esim_report.pdf
