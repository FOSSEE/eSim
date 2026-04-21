
eSim Upgradation
====

This repository documents the issues encountered while installing **eSim 2.5**
on **Ubuntu 25.04** as part of the **FOSSEE Semester Long Internship Spring 2026
Screening Task (Task 4)**.

---

## System Information

- Host OS: Windows (Virtualized Ubuntu)
- Guest OS: Ubuntu 25.04
- Architecture: x86_64
- Internet: College Wi-Fi (No proxy)
- Python: Python 3 (system-installed)

---

## Objective of the Task

The objective of this task was to:
- Attempt installation of eSim using the official installer
- Identify bugs/issues in the installation process
- Fix issues where possible
- Clearly document all findings and attempts

## Isusues Encountered ##

### Issue 1: Missing Installation Script for Ubuntu 25.04

**Issue Description**
The eSim repository did not contain an installation script for Ubuntu 25.04.                                                                                                  Users running Ubuntu 25.04 were unable to find a corresponding installer script, which prevented them from installing eSim on the latest Ubuntu version.
  
**Analysis:**
On reviewing the repository, it was observed that installer scripts were available only for earlier Ubuntu versions (such as 22.04, 23.04, and 24.04). 
The installer structure relies on version-specific scripts, and since Ubuntu 25.04 was not included, the installation process could not proceed for users on this OS version.

This gap occurred because the repository had not yet been updated to support the newly released Ubuntu 25.04.

**Action Taken:**
-Identified the absence of an installer script for Ubuntu 25.04.
-Created/added a new installer script for Ubuntu 25.04 following the structure and conventions of existing Ubuntu installer scripts.
-Placed the script under the appropriate directory: `Ubuntu/install-eSim-scripts/`
-Ensured consistency with existing installation logic so that the new script integrates smoothly with the current installer workflow.

### Issue 2: Volare Installation Fails Due to Missing xz-utils

**Issue Description**
During the eSim installation process, the Volare package failed to install on some Ubuntu systems. The error occurred because the system did not have the xz-utils package installed, which is required for extracting .tar.xz archives during Volare installation.

**Analysis:**
The installer attempts to download and extract the Volare software.
Extraction requires the xz command, provided by the xz-utils package.

On systems where xz-utils was missing, the installer failed with errors such as:
`E: Invalid operation xz-utils`

This caused the Volare installation step to fail, halting the overall eSim installation process.

The issue occurs on fresh Ubuntu installations where xz-utils is not pre-installed.

**Action Taken:**
Updated the installer script to check for the presence of xz-utils before attempting Volare installation.

If xz-utils is not installed, the installer now automatically installs it using:
`sudo apt-get install -y xz-utils`

Verified that after this addition, Volare installs successfully without errors on Ubuntu systems lacking xz-utils.
Ensured that this fix is backward-compatible and does not affect systems that already have xz-utils installed.

### Issue 3: KiCad 6.0 PPA causes installation failure on Ubuntu 25.04

**Issue Description**
During the execution of the eSim installer on Ubuntu 25.04 (Plucky Puffin), the installation process fails while updating APT repositories. The installer attempts to add the KiCad 6.0 PPA (ppa:kicad/kicad-6.0-releases), which does not provide a valid Release file for Ubuntu 25.04. This causes apt update to fail and results in the installer aborting prematurely.

**Analysis:**
The main installer detects Ubuntu 25.04 and falls back to using the Ubuntu 24.04 child installer script.

The child installer script contains the installKicad function, which:
Adds KiCad PPAs based on Ubuntu version

Defaults to using kicad/kicad-6.0-releases for non-24.04 versions

The KiCad 6.0 PPA does not support Ubuntu 25.04, leading to the following error during apt update:
`E: The repository 'https://ppa.launchpadcontent.net/kicad/kicad-6.0-releases/ubuntu plucky Release' does not have a Release file.`
Since APT treats this as a fatal error, the installation process terminates with:
`Error! Kindly resolve above error(s) and try again.
Aborting Installation...`
The root cause was identified as outdated PPA handling logic inside the installKicad function, which is incompatible with newer Ubuntu releases.

**Action Taken:**
The installKicad function in the child installer script was rewritten to handle Ubuntu versions more safely.

The updated function:
-Detects Ubuntu 25.04 explicitly
-Avoids adding any external KiCad PPAs on Ubuntu 25.04
-Installs KiCad directly from the official Ubuntu repositories, which already provide a supported KiCad 8.x version

This prevents invalid repository additions, allows apt update to complete successfully, and ensures KiCad installs correctly on Ubuntu 25.04.
The rewritten logic improves forward compatibility and avoids unsafe fallback behavior for future Ubuntu releases.

### Issue 4:eSim Installer Fails Due to Missing kicadLibrary.tar.xz on Ubuntu 25.04

**Issue Description**
The eSim installation script aborts with a fatal tar error after successfully installing KiCad. The installer attempts to extract a KiCad library archive (library/kicadLibrary.tar.xz) that does not exist in the expected path, causing the installation to terminate prematurely.

Although KiCad is installed correctly via APT, the overall eSim installation fails due to this missing file.

``KiCad installation completed successfully!
tar (child): library/kicadLibrary.tar.xz: Cannot open: No such file or directory
tar (child): Error is not recoverable: exiting now
tar: Child returned status 2
tar: Error is not recoverable: exiting now
Error! Kindly resolve above error(s) and try again.
Aborting Installation...
``

**Analysis:**
The installer script assumes the presence of library/kicadLibrary.tar.xz.
This file is not present in the library/ directory at runtime.

Possible causes:
The library archive is not included in the repository or release package.
Git submodules or LFS-tracked files were not initialized or fetched.
The script uses a hardcoded relative path that breaks if executed from a different directory.
The installer is not compatible with Ubuntu 25.04 and expects an older directory structure or packaging logic.
Notably, KiCad itself installs successfully, indicating the failure is isolated to the eSim-specific KiCad library extraction step.
