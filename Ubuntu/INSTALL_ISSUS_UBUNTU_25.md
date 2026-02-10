# eSim 2.5 Installation on Ubuntu 25.04

## Issue 1: Ubuntu 25.04 Not Supported by Installer

### Description
The eSim installer script does not recognize Ubuntu 25.04 and exits or installs incorrect dependencies.

### Error Observed
Installer checks OS version and fails due to unsupported Ubuntu release.

### Root Cause
eSim 2.5 officially supports Ubuntu 24.04 and earlier. Ubuntu 25.04 is not yet handled in the installer logic.

### Fix Applied
Mapped Ubuntu 25.04 to Ubuntu 24.04 in `install-eSim.sh` so that supported dependency logic could be reused.

### Result
Installer proceeds beyond OS detection stage successfully.

### Status
Fixed 

## Issue 2: Invalid apt operations for xz-utils

### Description
After fixing the Ubuntu 25.04 OS version mapping, the installer failed during dependency installation with the following error: Invalid operation xz-utils
This caused the installation process to abort even though `xz-utils` is a valid and required package.

### Error Observed
Installer invoked `apt` incorrectly and got xz-utils error.

### Root Cause
Invalid operation `xz-utils`

### Incorrect Command
```bash
sudo apt xz-utils

###Corrected commands
sudo apt install -y xz-utils

### Result
Installation proceeds successfully after correcting the xz-utils installation command.

### Status
Fixed


##Issue 3: Kicad ppa not available on ubuntu 25.04

##Description

apt update failed with:

The repository 'ppa:kicad/kicad-6.0-releases' does not have a Release file

###Root Cause

KiCad PPAs are not published for Ubuntu 25.04. Ubuntu 25.04 already provides KiCad 8 via official repositories.

###Fix Applied

For Ubuntu 25.04:

All KiCad PPAs are skipped

KiCad is installed directly from Ubuntu’s official repositories:

###Result

No repository or dependency errors occur during KiCad installation.

###Status

Fixed

##Issue 4:KiCad library extraction path failure

###Description

Installation failed with:
tar: library/kicadLibrary.tar.xz: No such file or directory

###Root Cause

The installer used relative paths that were invalid depending on the working directory.

###Fix Applied

The extraction logic was updated to use paths based on eSim_HOME, ensuring the archive is always found correctly.

###Result

The KiCad library archive is extracted reliably.

###Status

Fixed

##Issue 6: Incorrect KiCad library path in configuration

###Description

KiCad symbols were not detected even after successful extraction.

###Root Cause

The configuration file pointed to:

kicadLibrary.tar.xz instead of the extracted directory.

###Fix Applied

The configuration entry was updated to reference the extracted directory:

KicadLib = %(eSim_HOME)s/library/kicadLibrary

###Result

KiCad correctly loads eSim custom symbols.

###Status

Fixed

###Final working state
esim runs on ubuntu 25.04 (Ubuntu/docs/ubuntu-25.04-bugs/Screenshot From 2026-02-10 14-26-05.png)


eSim runs on the version Ubuntu 25.04.
