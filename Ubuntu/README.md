eSim Installer (Ubuntu OS)
====

It contains the documentation to package eSim for Ubuntu OS.

> Note: If planning to freeze the eSim source code for a target platform (Ubuntu OS), then refer this [documentation](executable.md). Remember to update the installer script to work with this executable!


## How to package eSim for Ubuntu OS?

1. Take the `master` branch containing the source code. Rename the folder to `eSim-<version>`.

2. Add the installer script `install-eSim.sh` from `installers` branch to `eSim-<version>` folder.

3. Add the eSim executable (if available) in `eSim-<version>` folder. Also, remove following files from this folder:
	- `.git` folder
	- `code` folder
	- `src` folder (Applicable only if eSim executable is used)
	- conf.py
	- setup.py
	- index.rst
	- requirement.txt
	- .gitignore
	- .travis.yml
    - `library/browser/User-Manual/figures` folder
    - library/browser/User-Manual/eSim.html

4. Add eSim user manual `eSim_Manual_<version>.pdf` at location `library/browser/User-Manual`.

5. Add the zip file of `NGHDL` (`nghdl.zip`) in the eSim folder.

> Note: Refer this [documentation](https://github.com/fossee/nghdl/tree/installers/Ubuntu/README.md) on packaging of NGHDL for Ubuntu OS.

6. Compress `kicadLibrary` folder to a `tar.xz` format and then remove that folder.

7. Compress `eSim-<version>` to a zip format for distribution.
