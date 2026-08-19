# Task 4 - eSim Upgradation - Bug Report

## Author
GitHub: Lutfullah07

## Environment
- OS: Ubuntu 26.04 LTS (via VirtualBox VM)
- eSim Version: 2.5 (FOSSEE/eSim, master branch)
- Note: Ubuntu 25.04 has reached end-of-life, so 26.04 LTS was used, which
  satisfies the task requirement of "25.04 and above"

## Issue Found

### Problem
Running scripts/setup-esim.sh failed with the following error:
cp: cannot stat '/3rdparty/template/sym-lib-table': No such file or directory

### Root Cause
The script had the line:
eSim_HOME="$SNAP/eSim"

$SNAP is an environment variable that is only set when eSim is installed as a
Snap package. When the script is run manually after cloning from source,
$SNAP is empty, causing the path to become /3rdparty/template/sym-lib-table,
which does not exist. Additionally, the 3rdparty folder does not exist
anywhere in the source repository. The actual file exists at:
library/kicadLibrary/template/sym-lib-table

### Fix Applied
Updated scripts/setup-esim.sh

Before:
eSim_HOME="$SNAP/eSim"
cp "$SNAP/3rdparty/template/sym-lib-table" "$TARGET/template/"

After:
eSim_HOME="$(dirname "$(pwd)")"
cp "$eSim_HOME/library/kicadLibrary/template/sym-lib-table" "$TARGET/template/"

This makes eSim_HOME resolve dynamically based on the script location instead
of depending on the Snap-only $SNAP variable, and points to the correct
current location of sym-lib-table in the repository.

### Verification
After applying the fix, ran:
sudo ./setup-esim.sh

Output:
Setting up eSim libraries for the first time...
eSim libraries setup completed.

No errors were raised, confirming the fix works.

## Summary
- Issue: Broken path due to unset $SNAP variable during manual installation
- File affected: scripts/setup-esim.sh
- Severity: High - blocks eSim library setup when installed from source
- Status: Fixed and verified

---

# Issue 2 - install-eSim.sh Referenced in Documentation Does Not Exist in Repository

## Problem
The INSTALL file instructs Ubuntu users to run:
chmod +x install-eSim.sh
./install-eSim.sh --install

However, this file does not exist anywhere in the cloned GitHub repository.

## Verification
Ran the following command from the repository root:
find . -iname "install-eSim.sh"

This returned no output, confirming the file is genuinely absent from the
source repository.

## Root Cause (Suspected)
install-eSim.sh appears to only be bundled inside the downloadable release
archive (eSim-2.5.zip from esim.fossee.in), not in the GitHub source
repository itself. Anyone who clones the repository directly from GitHub
(instead of downloading the release zip) and follows the INSTALL file will
immediately hit a "No such file or directory" error, since the actual
installer script in this repository is scripts/setup-esim.sh, not
install-eSim.sh.

## Status
Reported, not fixed. This is a documentation-code mismatch rather than a
script bug. A proper fix would require either:
1. Adding install-eSim.sh to the repository root, or
2. Updating the INSTALL file to reference scripts/setup-esim.sh instead

This was not fixed as it requires a decision from the maintainers on which
installation path (Flatpak, zip release, or direct source) should be the
documented standard for GitHub-based installs.


### Issue 3: Invalid Snap Path in Launcher Script (launcher-esim.sh)- Status: FIXED- Affected File: scripts/launcher-esim.sh- Symptom: Executing launcher-esim.sh fails with missing setup-esim.sh and frontEnd directory errors.- Root Cause: Script relied on empty $SNAP variable in source installs.</code><br/>
<code>- **Fix:** Commented out setup-esim call and updated path to cd "$(dirname "$(pwd)")/src/frontEnd".### Issue 4: Python Dependency Chain for eSim GUI Launch- Status: FIXED- Affected Files: Front-End GUI Launchers (Application.py, DockArea.py, Maker.py)- Symptom: eSim GUI fails to launch on Ubuntu 25.04+ with multiple ModuleNotFoundError exceptions.- Root Cause & Fixes:  1. PyQt6: Missing GUI library. Fixed via pip3 install PyQt6 --break-system-packages  2. numpy & matplotlib: Missing computing/plotting packages. Fixed via pip3 install numpy matplotlib --break-system-packages  3. hdlparse (Critical Finding): Original PyPI package (v1.0.1) failed with "use_2to3 is invalid" error due to modern setuptools (v58+). Fixed by installing maintained fork pyHDLParser (v1.0.7) via git tarball.  4. watchdog: Missing file watcher library. Fixed via pip3 install watchdog --break-system-packages- Verification: Verified eSim GUI launching and workspace setup dialog appearing without crashes.
