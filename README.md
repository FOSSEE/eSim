eSim Packaging
====

It contains all the documentation for packaging eSim for distribution.


# Packaging eSim for Distribution:

1. eSim is currently packaged and distributed for Ubuntu OS (Linux) and MS Windows OS.

2. Refer the [documentation](Version_Change.md) for the changes to be done when a new release is to be made.

> Note: These changes have to be made `first` before proceeding with the packaging on either platform.

3. Refer the [documentation](Ubuntu/README.md) to package eSim for Ubuntu OS.

4. Refer the [documentation](Windows/README.md) to package eSim for Windows OS.

## What's New in v3.2.1
- Added Ubuntu 25.x support
- Added compatibility for Intel, AMD, and ARM64 systems
- Fixed LLVM 20+ compatibility for GHDL installer
- Fixed GCC 15 / C23 build issues in NGHDL simulator
- Improved package compatibility and removed deprecated dependencies
