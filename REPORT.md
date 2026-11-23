# eSim 2.5 Installation on Ubuntu 25.04: Issue Report (Task 4)

**Author:** Rishita Goswami (GitHub: rg861348)
**Task:** eSim Semester Long Internship, Autumn 2026, Task 4 (eSim Upgradation)
**Pull request:** https://github.com/FOSSEE/eSim/pull/661
**Branch:** `installers` on my fork

## 1. Summary

| # | Issue | Severity | Status |
|---|-------|----------|--------|
| 1 | Install fails at "Installing volare" with `E: Invalid operation xz-utils` (22.04, 23.04, 24.04 scripts) | High, blocks the whole install | Fixed |
| 2 | `install-eSim-25.04.sh` is not executable in the repo (mode 644) | Low | Fixed |
| 3 | 25.04 script has no volare step (no match found) | Observation | Reported |
| 4 | Typo in the proxy prompt: "thorugh" | Cosmetic | Reported |

Technologies used: Bash, Python (venv), Git/GitHub, eSim, Ubuntu 25.04.

## 2. Test environment
- Host: HP laptop, Windows 11, 8 GB RAM
- Guest: Ubuntu 25.04 (plucky) in VirtualBox, confirmed with `lsb_release -a`
- eSim installer files cloned to `~/eSim`; scripts are in `Ubuntu/install-eSim-scripts/` (22.04, 23.04, 24.04, 25.04)
- Python 3.13 virtual environment created by the script at `~/.esim/env`

## 3. Issue 1: `E: Invalid operation xz-utils` (FIXED)

**Symptom**
The installer runs the proxy prompt, creates the virtual environment, installs the Python packages (matplotlib, PyQt5), then stops at the volare step:

    Installing volare
    E: Invalid operation xz-utils
    Error! Kindly resolve above error(s) and try again.
    Aborting Installation...

**Steps to reproduce**
1. `cd ~/eSim`
2. `bash Ubuntu/install-eSim-scripts/install-eSim-24.04.sh --install`
3. Answer `n` to "Is your internet connection behind proxy?"
4. The installation aborts at "Installing volare".

**Investigation**
1. Ran `sudo apt update` (works) and `sudo apt install -y xz-utils`. Result: "xz-utils is already the newest version (5.6.4-1ubuntu1)". So the package exists and is installed, and the problem is not a missing package.
2. Searched the scripts with `grep -rn "xz-utils" Ubuntu/`. The faulty lines are:
   - `install-eSim-22.04.sh` line 219
   - `install-eSim-23.04.sh` line 282
   - `install-eSim-24.04.sh` line 252
   Each reads `sudo apt-get xz-utils`.

**Root cause**
The `install` sub-command is missing in `sudo apt-get xz-utils`. Apt treats `xz-utils` as the operation, which gives "Invalid operation". Because the script aborts on any error, the whole installation stops, including the eSim GUI.

**Fix**

    sed -i 's/sudo apt-get xz-utils/sudo apt-get install -y xz-utils/g' Ubuntu/install-eSim-scripts/*.sh

The `-y` flag was added so the script does not wait for a confirmation prompt.

**Verification**
Running `grep -rn "xz-utils" Ubuntu/` after the change shows `sudo apt-get install -y xz-utils` at lines 219, 282 and 252.

**Git steps**
1. `git checkout -b installer`
2. `git add Ubuntu/install-eSim-scripts/*.sh`
3. First commit failed with "Author identity unknown", so I set `git config --global user.name` and `user.email`
4. `git commit` created commit `7c683187`: 4 files changed, 3 insertions, 3 deletions
5. `git push origin installer`
6. Opened pull request #661 into `FOSSEE:installers`: 3 commits, 3 files changed (22.04, 23.04, 24.04 scripts)

## 4. Issue 2: 25.04 script is not executable (FIXED)
The commit output shows `mode change 100644 => 100755` for `install-eSim-25.04.sh`. The file was stored without the execute permission, and it is now executable.

## 5. Observation: running the 25.04 script
After the fix I ran `bash Ubuntu/install-eSim-scripts/install-eSim-25.04.sh --install` on Ubuntu 25.04. It ran through apt index update, virtual environment creation, pip upgrade (25.0 to 26.3), Xterm check, Python packages, PyQt5, and the KiCad check ("Ubuntu 25.04 detected. KiCad 8.0 is already installed.") without errors.

## 6. Issue 3: No volare step in the 25.04 script (REPORTED, NOT FIXED)
`grep -n "volare" Ubuntu/install-eSim-scripts/install-eSim-25.04.sh` returned no match, and neither did `grep "xz-utils"`. The older scripts install volare and the xz-utils dependency. The maintainers should confirm whether this is intended.

## 7. Issue 4: Typo in the proxy prompt (REPORTED, NOT FIXED)
The prompt reads "Enter proxy details if you are connected to internet **thorugh** proxy" (should be "through").

## 8. Screenshots (evidence)

**Error at volare (24.04 script)**
![error](screenshots/1000140077.jpg)

**OS confirmation and available scripts**
![os](screenshots/1000140073.jpg)

**xz-utils is already installed (so the problem is the command)**
![xz](screenshots/1000140059.jpg)

**Faulty lines found with grep**
![grep](screenshots/1000140086.jpg)

**Fixed lines after sed**
![fixed](screenshots/1000140088.jpg)

**25.04 script run**
![run1](screenshots/1000140078.jpg)
![run2](screenshots/1000140080.jpg)
![run3](screenshots/1000140081.jpg)

**Commit and push**
![commit](screenshots/1000140092.jpg)

**Fork and pull request #661**
![fork](screenshots/1000140160.jpg)
![pr](screenshots/1000140164.jpg)
![diff](screenshots/1000140171.jpg)
