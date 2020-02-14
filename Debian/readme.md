Ubuntu Installer Documentation 
====


It contains all the documenation for installers on Ubuntu 14.04 and above. 

## How to package eSim?

1. Add the installer file in `eSim-<version>` folder.
2. Remove following files from the folder:
	- `.git` folder
	- `code` folder
	- conf.py
	- index.rst
	- requirement.txt
	- .gitignore
	- .travis.yml
3. Add the tar file of `NGHDL` in the eSim folder.
