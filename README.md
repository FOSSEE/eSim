eSim Packaging
====

It contains all the documentation for packaging eSim for distribution.


# Packaging eSim for Distribution:

1. eSim is currently packaged and distributed for Ubuntu OS (Linux) and MS Windows OS.

2. Refer the [documentation](Version_Change.md) for the changes to be done when a new release is to be made.

> Note: These changes have to be made `first` before proceeding with the packaging on either platform.

3. Refer the [documentation](Ubuntu/README.md) to package eSim for Ubuntu OS.

4. Refer the [documentation](Windows/README.md) to package eSim for Windows OS.


---

# FOSSEE Summer Fellowship 2026 - Ubuntu 25.04 Port

As part of the eSim upgradation task, the installer has been ported to support Ubuntu 25.04. The upstream installer failed due to dependency removals, version mismatches, and strict detection logic.

During debugging in a clean environment, 38 distinct installation blockers were identified and resolved through 38 atomic commits in the installers branch.

## Porting Summary
- High difficulty (15): dependency chain resolutions (LLVM/GHDL handling, NGHDL sub-installer chain, dynamic path discovery)
- Medium difficulty (14): PPA management, virtualenv ownership issues, package fallback logic, snap-based KiCad installation
- Low difficulty (7): regex fixes, syntax-level fixes, and missing assets handling

## Ubuntu 25.04 Documentation
All Ubuntu 25.04 port documentation is in the Ubuntu directory:
- [Changelog and Commit Mapping](Ubuntu/CHANGELOG.md)
- [Detailed Bug Report](Ubuntu/BUG_REPORT.md)
- [Final Installer Script](Ubuntu/install-eSim-scripts/install-eSim-25.04.sh)
