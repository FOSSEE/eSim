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
