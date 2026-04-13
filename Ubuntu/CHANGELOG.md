# eSim Ubuntu 25.04 Port - Changelog & Commit Mapping

This log tracks the 36 atomic commits made to resolve the Ubuntu 25.04 installation failures. For detailed terminal logs and code diffs for each bug, please refer to [BUG_REPORT.md](./BUG_REPORT.md).

| Bug ID | Commit Title | Category |
| :--- | :--- | :--- |
| **#001** | Fix: no version output | Version Detection |
| **#002** | Fix: 25.04 unsupported version | Version Detection |
| **#003** | Fix: no script for 25.04 | File Management |
| **#004** | Fix: xz-utils installation failed, aborted installation | Package Management |
| **#005** | Fix: stale CD-ROM repo reference, abort installation | APT Sources |
| **#006** | Fix: KiCad libgit2 dependency mismatch | Package Management |
| **#007** | Fix: KiCad PPA not removed | APT Sources |
| **#008** | Fix: Missing KiCad library archive | File Management |
| **#009** | Fix: Installer exits after KiCad | Flow Control |
| **#010** | Fix: Missing NGHDL archive | File Management |
| **#011** | Fix: Desktop path under sudo | Permissions |
| **#012** | Fix: Desktop copy from main flow | Flow Control |
| **#013** | Fix: Missing logo icon | File Management |
| **#014** | Fix: KiCad PPA added on 25.04 | Package Management |
| **#015** | Fix: Stale cdrom apt source | APT Sources |
| **#016** | Fix: file:///cdrom entry not disabled | APT Sources |
| **#017** | Fix: gio trusted attribute warning | System Config |
| **#018** | Fix: esim launcher path/venv | Permissions |
| **#019** | Fix: chown invalid user | Permissions |
| **#020** | Fix: esim app missing | Application Launch |
| **#021** | Fix: Virtualenv permission denied when creating env | Permissions |
| **#022** | Fix: NGHDL installer rejects Ubuntu 25.04 | Sub-installer |
| **#023** | Fix: NGHDL 25.04 detection fails | Version Detection |
| **#024** | Fix: NGHDL fallback script not executable | Permissions |
| **#025** | Fix: Missing libcanberra-gtk-module | Package Management |
| **#026** | Fix: Canberra module candidate missing | Package Management |
| **#027** | Fix: NGHDL installs missing canberra | Sub-installer |
| **#028** | Fix: NGHDL rejects LLVM 20.1 | Package Management |
| **#029** | Fix: LLVM 20.1.2 still unhandled | Package Management |
| **#030** | Fix: LLVM 20.1.2 still unhandled | Package Management |
| **#031** | Fix: GHDL configure rejects LLVM 20.x | Sub-installer |
| **#032** | Fix: NGHDL sub-installer chain-link failure | Sub-installer |
| **#033** | Fix: NGHDL clean reinstall fails on existing directory | File Management |
| **#034** | Fix: GHDL configure fails with incorrect srcdir | Sub-installer |
| **#035** | Fix: Incorrect eSim_Home Path in Startup Script | Application Launch |
| **#036** | Fix: Source Discovery Failure | Application Launch |
