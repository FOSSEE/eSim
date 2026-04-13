# Comprehensive Bug Report and Resolution Documentation

This document details the systematic identification and resolution of 36 distinct installation bugs encountered while porting eSim to Ubuntu 25.04.

---

### Bug #001: no version output

**Log:**
```text
user@Ubuntu-25:~/repos/eSim/Ubuntu$ ./install-eSim.sh --install
	Detected Ubuntu Version: 
	Unsupported Ubuntu version: 25.04 ()
```

**Root Cause:** regex issue in "install-eSim.sh" in function "get_ubuntu_version()", it used to pull version till 3 decimal places ex:"22.04.02" making all 3 mandatory resulting in no output if only 2 decimal places are pulled.

**Fix:** updated regex to make 3rd decimal place optional.

**Changes Made:**
```text
file : "install-eSim.sh"
		before : "FULL_VERSION=$(lsb_release -d | grep -oP '\d+\.\d+\.\d+')"
		after : "FULL_VERSION=$(lsb_release -d | grep -oP '\d+\.\d+(\.\d+)?')"
```

**Log (after change):**
```text
user@Ubuntu-25:~/repos/eSim/Ubuntu$ ./install-eSim.sh --install
		Detected Ubuntu Version: 25.04
		Unsupported Ubuntu version: 25.04 (25.04)
```

**Commit Hash:** `ca0c9bec`

---

### Bug #002: 25.04 unsupported version

**Log:**
```text
user@Ubuntu-25:~/repos/eSim/Ubuntu$ ./install-eSim.sh --install
	Detected Ubuntu Version: 25.04
	Unsupported Ubuntu version: 25.04 (25.04)
```

**Root Cause:** the script "install-eSim.sh" doesn't support 25.04, support only for 22.04, 23.04 and 24.04.

**Fix:** added support for 25.04 with if statement addition in "install-eSim.sh" to run install-eSim-25.04.sh script for 25.04 version.

**Changes Made:**
```text
file : "install-eSim.sh"

		before :     case $VERSION_ID in
        "22.04")
            if [[ "$FULL_VERSION" == "22.04.4" ]]; then
                SCRIPT="$SCRIPT_DIR/install-eSim-22.04.sh"
            else
                SCRIPT="$SCRIPT_DIR/install-eSim-23.04.sh"
            fi
            ;;
        "23.04")
            SCRIPT="$SCRIPT_DIR/install-eSim-23.04.sh"
            ;;
        "24.04")
            SCRIPT="$SCRIPT_DIR/install-eSim-24.04.sh"
            ;;
        *)
            echo "Unsupported Ubuntu version: $VERSION_ID ($FULL_VERSION)"
            exit 1
            ;;
    esac

		after :     case $VERSION_ID in
        "22.04")
            if [[ "$FULL_VERSION" == "22.04.4" ]]; then
                SCRIPT="$SCRIPT_DIR/install-eSim-22.04.sh"
            else
                SCRIPT="$SCRIPT_DIR/install-eSim-23.04.sh"
            fi
            ;;
        "23.04")
            SCRIPT="$SCRIPT_DIR/install-eSim-23.04.sh"
            ;;
        "24.04")
            SCRIPT="$SCRIPT_DIR/install-eSim-24.04.sh"
            ;;
        "25.04")
            SCRIPT="$SCRIPT_DIR/install-eSim-25.04.sh"
            ;;
        *)
            echo "Unsupported Ubuntu version: $VERSION_ID ($FULL_VERSION)"
            exit 1
            ;;
    esac
```

**Log (after change):**
```text
user@Ubuntu-25:~/repos/eSim/Ubuntu$ ./install-eSim.sh --install
	Detected Ubuntu Version: 25.04
	Installation script not found: /home/user/repos/eSim/Ubuntu/install-eSim-scripts/install-eSim-25.04.sh
```

**Commit Hash:** `7006f6f6`

---

### Bug #003: no script for 25.04

**Log:**
```text
user@Ubuntu-25:~/repos/eSim/Ubuntu$ ./install-eSim.sh --install
	Detected Ubuntu Version: 25.04
	Installation script not found: /home/user/repos/eSim/Ubuntu/install-eSim-scripts/install-eSim-25.04.sh
```

**Root Cause:** no installation script for Ubuntu version 25.04

**Fix:** copying script of 24.04 for 25.04 by renaming the file to install-eSim-25.04.sh and updated the version check in if statement from 24.04 to 25.04 whereever applicable

**Changes Made:**
```text
file : (newFile)install-eSim-25.04.sh

		before :     if [[ "$ubuntu_version" == "24.04" ]]; then
        echo "Ubuntu 24.04 detected."

		after :     if [[ "$ubuntu_version" == "25.04" ]]; then
        echo "Ubuntu 25.04 detected."
```

**Commit Hash:** `3f438548`

---

### Bug #004: xz-utils installation failed, aborted installation

**Log:**
```text
E: Invalid operation xz-utils


	Error! Kindly resolve above error(s) and try again.

	Aborting Installation...
```

**Root Cause:** invalid command for xz-utils installation

**Fix:** updating the sudo apt-get command for instllation of xz-utils

**Changes Made:**
```text
file : "install-eSim-25.04.sh"
		before :  echo "Installing volare"
			  sudo apt-get xz-utils
			  pip3 install volare
		
		after :  echo "Installing volare"
			 sudo apt-get install xz-utils -y xz-utils
			 pip3 install volare
```

**Commit Hash:** `d7904faa`

---

### Bug #005: stale CD-ROM repo reference, abort installation

**Log:**
```text
Err:2 file:/cdrom plucky Release
  		File not found - /cdrom/dists/plucky/Release (2: No such file or directory)
	E: The repository 'file:/cdrom plucky Release' no longer has a Release file.
	N: Updating from such a repository can't be done securely, and is therefore disabled by default.
	N: See apt-secure(8) manpage for repository creation and user configuration details.
	N: Some sources can be modernized. Run 'apt modernize-sources' to do so.

	Error! Kindly resolve above error(s) and try again.

	Aborting Installation...
```

**Root Cause:** stale CD-ROM repo reference which doesn't exist and installation abort on non critical errors

**Fix:** suppress "apt-get update" error while installation on non critical errors

**Changes Made:**
```text
file : "install-eSim-25.04.sh"
		before :     if ! grep -q "^deb .*${kicadppa}" /etc/apt/sources.list /etc/apt/sources.list.d/* 2>/dev/null; then
        			echo "Adding KiCad PPA to local apt repository: $kicadppa"
        			sudo add-apt-repository -y "ppa:$kicadppa"
        			sudo apt-get update
		
		after :      if ! grep -q "^deb .*${kicadppa}" /etc/apt/sources.list /etc/apt/sources.list.d/* 2>/dev/null; then
        			echo "Adding KiCad PPA to local apt repository: $kicadppa"
        			sudo add-apt-repository -y "ppa:$kicadppa"
        			sudo apt-get update || true
```

**Commit Hash:** `61b3c623`

---

### Bug #006: KiCad libgit2 dependency mismatch

**Log:**
```text
Solving dependencies... Error!
Some packages could not be installed. This may mean that you have
requested an impossible situation or if you are using the unstable
distribution that some required packages have not yet been created
or been moved out of Incoming.
The following information may help to resolve the situation:

The following packages have unmet dependencies:
 kicad : Depends: libgit2-1.8 (>= 1.8.0) but it is not installable
E: Unable to correct problems, you have held broken packages.
E: The following information from --solver 3.0 may provide additional context:
   Unable to satisfy dependencies. Reached two conflicting decisions:
   1. kicad:amd64=8.0.9-0~ubuntu25.04.1 is selected for install
   2. kicad:amd64=8.0.9-0~ubuntu25.04.1 Depends libgit2-1.8 (>= 1.8.0)
	  but none of the choices are installable:
	  [no choices]


Error! Kindly resolve above error(s) and try again.

Aborting Installation...
```

**Root Cause:** The KiCad 8.0 PPA build for Ubuntu 25.04 depends on libgit2-1.8, which is not available in the 25.04 repositories where libgit2-1.9 is provided instead.

**Fix:** Detect missing libgit2-1.8 and avoid the PPA by removing it (if present) so the installer falls back to the Ubuntu repo KiCad packages built against available libgit2.

**Changes Made:**
```text
file : install-eSim-25.04.sh
	before :     if [[ "$ubuntu_version" == "25.04" ]]; then
		echo "Ubuntu 25.04 detected."
		kicadppa="kicad/kicad-8.0-releases"
	...
	if ! grep -q "^deb .*${kicadppa}" /etc/apt/sources.list /etc/apt/sources.list.d/* 2>/dev/null; then
		echo "Adding KiCad PPA to local apt repository: $kicadppa"
		sudo add-apt-repository -y "ppa:$kicadppa"
		sudo apt-get update || true
	else
		echo "KiCad PPA is already present in sources."
	fi
	after :     if [[ "$ubuntu_version" == "25.04" ]]; then
		echo "Ubuntu 25.04 detected."
		kicadppa="kicad/kicad-8.0-releases"
		use_kicad_ppa=true

		# Ubuntu 25.04 does not provide libgit2-1.8; avoid PPA if missing.
		if apt-cache policy libgit2-1.8 | grep -q "Candidate: (none)"; then
			echo "libgit2-1.8 not available. Falling back to Ubuntu KiCad repo."
			use_kicad_ppa=false
		fi
	...
	if [[ "$use_kicad_ppa" == true ]]; then
		if ! grep -q "^deb .*${kicadppa}" /etc/apt/sources.list /etc/apt/sources.list.d/* 2>/dev/null; then
			echo "Adding KiCad PPA to local apt repository: $kicadppa"
			sudo add-apt-repository -y "ppa:$kicadppa"
			sudo apt-get update || true
		else
			echo "KiCad PPA is already present in sources."
		fi
	else
		if grep -q "^deb .*${kicadppa}" /etc/apt/sources.list /etc/apt/sources.list.d/* 2>/dev/null; then
			echo "Removing KiCad PPA due to libgit2 dependency mismatch."
			sudo add-apt-repository -r -y "ppa:$kicadppa" || true
			sudo apt-get update || true
		fi
	fi
```

**Commit Hash:** `2ae976b7`

---

### Bug #007: KiCad PPA not removed

**Log:**
```text
Installing KiCad...........................
Ubuntu 25.04 detected.
libgit2-1.8 not available. Falling back to Ubuntu KiCad repo.
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
Solving dependencies... Error!
Some packages could not be installed. This may mean that you have
requested an impossible situation or if you are using the unstable
distribution that some required packages have not yet been created
or been moved out of Incoming.
The following information may help to resolve the situation:

The following packages have unmet dependencies:
 kicad : Depends: libgit2-1.8 (>= 1.8.0) but it is not installable
E: Unable to correct problems, you have held broken packages.
E: The following information from --solver 3.0 may provide additional context:
   Unable to satisfy dependencies. Reached two conflicting decisions:
   1. kicad:amd64=8.0.9-0~ubuntu25.04.1 is selected for install
   2. kicad:amd64=8.0.9-0~ubuntu25.04.1 Depends libgit2-1.8 (>= 1.8.0)
	  but none of the choices are installable:
	  [no choices]


Error! Kindly resolve above error(s) and try again.

Aborting Installation...
```

**Root Cause:** The fallback logic did not remove the KiCad PPA because it is stored as a .sources file, so apt still selected the PPA build requiring libgit2-1.8.

**Fix:** Detect any kicad-8.0-releases entries in sources.list or sources.list.d, remove the PPA, and delete matching .sources/.list files before updating apt.

**Changes Made:**
```text
file : install-eSim-25.04.sh
	before :     else
		if grep -q "^deb .*${kicadppa}" /etc/apt/sources.list /etc/apt/sources.list.d/* 2>/dev/null; then
			echo "Removing KiCad PPA due to libgit2 dependency mismatch."
			sudo add-apt-repository -r -y "ppa:$kicadppa" || true
			sudo apt-get update || true
		fi
	fi
	after :     else
		if grep -Rqs "kicad-8.0-releases" /etc/apt/sources.list /etc/apt/sources.list.d 2>/dev/null; then
			echo "Removing KiCad PPA due to libgit2 dependency mismatch."
			sudo add-apt-repository -r -y "ppa:$kicadppa" || true
			sudo rm -f /etc/apt/sources.list.d/kicad-ubuntu-kicad-8_0-releases-*.sources \
				/etc/apt/sources.list.d/kicad-ubuntu-kicad-8_0-releases-*.list || true
			sudo apt-get update || true
		fi
	fi
```

**Commit Hash:** `0e0476a4`

---

### Bug #008: Missing KiCad library archive

**Log:**
```text
tar (child): library/kicadLibrary.tar.xz: Cannot open: No such file or directory
tar (child): Error is not recoverable: exiting now
tar: Child returned status 2
tar: Error is not recoverable: exiting now


Error! Kindly resolve above error(s) and try again.

Aborting Installation...
```

**Root Cause:** The installer expects library/kicadLibrary.tar.xz, but the archive is not present in the repository, so tar fails and aborts installation.

**Fix:** Allow using an existing library/kicadLibrary directory or skip copying custom symbols when the archive is missing, avoiding a hard failure.

**Changes Made:**
```text
file : install-eSim-25.04.sh
	before : function copyKicadLibrary
{

    #Extract custom KiCad Library
    tar -xJf library/kicadLibrary.tar.xz

    if [ -d ~/.config/kicad/6.0 ];then
        echo "kicad config folder already exists"
    else 
        echo ".config/kicad/6.0 does not exist"
        mkdir -p ~/.config/kicad/6.0
    fi

    # Copy symbol table for eSim custom symbols 
    cp kicadLibrary/template/sym-lib-table ~/.config/kicad/6.0/
    echo "symbol table copied in the directory"

    # Copy KiCad symbols made for eSim
    sudo cp -r kicadLibrary/eSim-symbols/* /usr/share/kicad/symbols/
    ...
}
	after : function copyKicadLibrary
{

    local kicad_lib_dir=""
    local cleanup_tmp=false

    # Extract or use existing KiCad Library
    if [ -f library/kicadLibrary.tar.xz ]; then
        tar -xJf library/kicadLibrary.tar.xz
        kicad_lib_dir="kicadLibrary"
        cleanup_tmp=true
    elif [ -d library/kicadLibrary ]; then
        kicad_lib_dir="library/kicadLibrary"
    else
        echo "Warning: KiCad library archive not found. Skipping custom symbols."
        return 0
    fi
    ...
}
```

**Commit Hash:** `f964ecdf`

---

### Bug #009: Installer exits after KiCad

**Log:**
```text
Installing KiCad...........................
Ubuntu 25.04 detected.
KiCad 8.0 is already installed.
```

**Root Cause:** The installKicad function calls exit 0 when KiCad is already present, which terminates the whole installer and skips remaining steps.

**Fix:** Return from the function instead of exiting, allowing the main installer flow to continue.

**Changes Made:**
```text
file : install-eSim-25.04.sh
	before :             else
                echo "KiCad 8.0 is already installed."
                exit 0
            fi
	after :             else
                echo "KiCad 8.0 is already installed."
                return 0
            fi
```

**Commit Hash:** `7cc36c03`

---

### Bug #010: Missing NGHDL archive

**Log:**
```text
Installing NGHDL...........................
unzip:  cannot find or open nghdl.zip, nghdl.zip.zip or nghdl.zip.ZIP.


Error! Kindly resolve above error(s) and try again.

Aborting Installation...
```

**Root Cause:** The installer expects nghdl.zip in the working directory, but the archive is not present, so unzip fails and aborts the installation.

**Fix:** Check for nghdl.zip or an existing nghdl directory and skip NGHDL installation when missing.

**Changes Made:**
```text
file : install-eSim-25.04.sh
	before : function installNghdl
{

	echo "Installing NGHDL..........................."
	unzip -o nghdl.zip
	cd nghdl/
	chmod +x install-nghdl.sh
	...
}
	after : function installNghdl
{

	echo "Installing NGHDL..........................."
	local nghdl_dir=""

	if [ -f nghdl.zip ]; then
		unzip -o nghdl.zip
		nghdl_dir="nghdl"
	elif [ -d nghdl ]; then
		nghdl_dir="nghdl"
	else
		echo "Warning: nghdl.zip not found. Skipping NGHDL install."
		return 0
	fi

	cd "$nghdl_dir" || return 1
	chmod +x install-nghdl.sh
	...
}
```

**Commit Hash:** `520c7824`

---

### Bug #011: Desktop path under sudo

**Log:**
```text
'esim-start.sh' -> '/usr/bin/esim'
'esim.desktop' -> '/usr/share/applications/esim.desktop'
'esim.desktop' -> '/root/Desktop/'
cp: cannot create regular file '/root/Desktop/': Not a directory


Error! Kindly resolve above error(s) and try again.

Aborting Installation...
```

**Root Cause:** The installer runs under sudo, so $HOME points to /root where Desktop does not exist, causing the desktop file copy to fail.

**Fix:** Use the invoking user's home directory when copying the desktop file and setting trusted metadata.

**Changes Made:**
```text
file : install-eSim-25.04.sh
	before :     # Copy desktop icon file to Desktop
	cp -vp esim.desktop $HOME/Desktop/
	...
	gio set $HOME/Desktop/esim.desktop "metadata::trusted" true
	chmod a+x $HOME/Desktop/esim.desktop
	after :     local user_home="$HOME"
	if [ -n "$SUDO_USER" ] && [ -d "/home/$SUDO_USER" ]; then
		user_home="/home/$SUDO_USER"
	fi
	...
	cp -vp esim.desktop "$user_home/Desktop/"
	...
	gio set "$user_home/Desktop/esim.desktop" "metadata::trusted" true
	chmod a+x "$user_home/Desktop/esim.desktop"
```

**Commit Hash:** `c4884c1e`

---

### Bug #012: Desktop copy from main flow

**Log:**
```text
'esim.desktop' -> '/Desktop/'
cp: cannot create regular file '/Desktop/': Not a directory


Error! Kindly resolve above error(s) and try again.

Aborting Installation...
```

**Root Cause:** Desktop copy commands leaked into the main install flow and ran before the desktop file was created, with an empty home path, causing a failure.

**Fix:** Remove stray desktop operations from the main flow and keep them inside createDesktopStartScript with a resolved user home.

**Changes Made:**
```text
file : install-eSim-25.04.sh
	before :     fi
	        cp -vp esim.desktop "$user_home/Desktop/"
    createConfigFile
    ...
	    installNghdl
	        gio set "$user_home/Desktop/esim.desktop" "metadata::trusted" true
    createDesktopStartScript
	        chmod a+x "$user_home/Desktop/esim.desktop"
	after :     fi
    createConfigFile
    ...
    installNghdl
    createDesktopStartScript
```

**Commit Hash:** `1dc1c9dd`

---

### Bug #013: Missing logo icon

**Log:**
```text
'esim-start.sh' -> '/usr/bin/esim'
'esim.desktop' -> '/usr/share/applications/esim.desktop'
'esim.desktop' -> '/home/user/Desktop/esim.desktop'
gio: Setting attribute metadata::trusted not supported
cp: cannot stat 'images/logo.png': No such file or directory


Error! Kindly resolve above error(s) and try again.

Aborting Installation...
```

**Root Cause:** The installer assumes images/logo.png exists and fails when it is missing; Desktop folder creation is not ensured.

**Fix:** Ensure the Desktop directory exists and skip copying the logo when the file is missing.

**Changes Made:**
```text
file : install-eSim-25.04.sh
	before :     # Copy desktop icon file to share applications
	sudo cp -vp esim.desktop /usr/share/applications/
	# Copy desktop icon file to Desktop
	cp -vp esim.desktop "$user_home/Desktop/"
	...
	# Copying logo.png to .esim directory to access as icon
	cp -vp images/logo.png $config_dir
	after :     # Copy desktop icon file to share applications
	sudo cp -vp esim.desktop /usr/share/applications/
	# Copy desktop icon file to Desktop
	mkdir -p "$user_home/Desktop"
	cp -vp esim.desktop "$user_home/Desktop/"
	...
	# Copying logo.png to .esim directory to access as icon
	if [ -f images/logo.png ]; then
		cp -vp images/logo.png $config_dir
	else
		echo "Warning: images/logo.png not found. Skipping icon copy."
	fi
```

**Commit Hash:** `5ad597c6`

---

### Bug #014: KiCad PPA added on 25.04

**Log:**
```text
Installing KiCad...........................
Ubuntu 25.04 detected.
Adding KiCad PPA to local apt repository: kicad/kicad-8.0-releases
...
The following packages have unmet dependencies:
 kicad : Depends: libgit2-1.8 (>= 1.8.0) but it is not installable
E: Unable to correct problems, you have held broken packages.


Error! Kindly resolve above error(s) and try again.

Aborting Installation...
```

**Root Cause:** The libgit2-1.8 availability check did not trigger, so the script still added the KiCad PPA and hit the same dependency mismatch.

**Fix:** Use a robust check that treats both "Candidate: (none)" and "Unable to locate package" as missing and disables the PPA.

**Changes Made:**
```text
file : install-eSim-25.04.sh
	before :     # Ubuntu 25.04 does not provide libgit2-1.8; avoid PPA if missing.
		if apt-cache policy libgit2-1.8 | grep -q "Candidate: (none)"; then
			echo "libgit2-1.8 not available. Falling back to Ubuntu KiCad repo."
			use_kicad_ppa=false
		fi
	after :     # Ubuntu 25.04 does not provide libgit2-1.8; avoid PPA if missing.
		libgit2_policy=$(apt-cache policy libgit2-1.8 2>&1 || true)
		if echo "$libgit2_policy" | grep -Eq "Candidate: \(none\)|Unable to locate package"; then
			echo "libgit2-1.8 not available. Falling back to Ubuntu KiCad repo."
			use_kicad_ppa=false
		fi
```

**Commit Hash:** `726e136d`

---

### Bug #015: Stale cdrom apt source

**Log:**
```text
Updating apt index files...................
Ign:1 file:/cdrom plucky InRelease
Err:2 file:/cdrom plucky Release
  File not found - /cdrom/dists/plucky/Release (2: No such file or directory)
...
E: The repository 'file:/cdrom plucky Release' no longer has a Release file.
N: Updating from such a repository can't be done securely, and is therefore disabled by default.
N: See apt-secure(8) manpage for repository creation and user configuration details.
```

**Root Cause:** The installer runs apt-get update with a stale cdrom source enabled, which triggers apt-secure errors on every update.

**Fix:** Detect and disable file:/cdrom sources before updating apt indexes.

**Changes Made:**
```text
file : install-eSim-25.04.sh
	before :     # Update apt repository
	echo "Updating apt index files..................."
	sudo apt-get update
	after :     # Update apt repository
	echo "Updating apt index files..................."
	if grep -Rqs "file:/cdrom" /etc/apt/sources.list /etc/apt/sources.list.d 2>/dev/null; then
		sudo sed -i 's|^deb cdrom:|# deb cdrom:|g' /etc/apt/sources.list 2>/dev/null || true
		sudo sed -i '/file:\/cdrom/ s/^/# /' /etc/apt/sources.list.d/*.sources 2>/dev/null || true
		sudo rm -f /etc/apt/sources.list.d/*cdrom*.list /etc/apt/sources.list.d/*cdrom*.sources 2>/dev/null || true
	fi
	sudo apt-get update
```

**Commit Hash:** `5f2d2e04`

---

### Bug #016: file:///cdrom entry not disabled

**Log:**
```text
Updating apt index files...................
Ign:1 file:/cdrom plucky InRelease
Err:2 file:/cdrom plucky Release
	File not found - /cdrom/dists/plucky/Release (2: No such file or directory)
...
E: The repository 'file:/cdrom plucky Release' no longer has a Release file.
```

**Root Cause:** The cdrom source is listed as deb [check-date=no] file:///cdrom..., which was not matched by the previous disable rule.

**Fix:** Also comment deb lines that use file:///cdrom in /etc/apt/sources.list.

**Changes Made:**
```text
file : install-eSim-25.04.sh
	before :     if grep -Rqs "file:/cdrom" /etc/apt/sources.list /etc/apt/sources.list.d 2>/dev/null; then
				sudo sed -i 's|^deb cdrom:|# deb cdrom:|g' /etc/apt/sources.list 2>/dev/null || true
				sudo sed -i '/file:\/cdrom/ s/^/# /' /etc/apt/sources.list.d/*.sources 2>/dev/null || true
				sudo rm -f /etc/apt/sources.list.d/*cdrom*.list /etc/apt/sources.list.d/*cdrom*.sources 2>/dev/null || true
		fi
	after :     if grep -Rqs "cdrom" /etc/apt/sources.list /etc/apt/sources.list.d 2>/dev/null; then
				sudo sed -i 's|^deb cdrom:|# deb cdrom:|g' /etc/apt/sources.list 2>/dev/null || true
				sudo sed -i 's|^deb .*file:///cdrom|# &|g' /etc/apt/sources.list 2>/dev/null || true
				sudo sed -i '/file:\/cdrom/ s/^/# /' /etc/apt/sources.list.d/*.sources 2>/dev/null || true
				sudo rm -f /etc/apt/sources.list.d/*cdrom*.list /etc/apt/sources.list.d/*cdrom*.sources 2>/dev/null || true
		fi
```

**Commit Hash:** `452f880b`

---

### Bug #017: gio trusted attribute warning

**Log:**
```text
'esim.desktop' -> '/home/user/Desktop/esim.desktop'
gio: Setting attribute metadata::trusted not supported
```

**Root Cause:** The installer always runs gio set, which emits a warning on systems that do not support the metadata::trusted attribute.

**Fix:** Run gio set on a best-effort basis and suppress its stderr output.

**Changes Made:**
```text
file : install-eSim-25.04.sh
	before :     # Make esim.desktop file as trusted application
	gio set "$user_home/Desktop/esim.desktop" "metadata::trusted" true
	after :     # Make esim.desktop file as trusted application (best-effort)
	if command -v gio >/dev/null 2>&1; then
		gio set "$user_home/Desktop/esim.desktop" "metadata::trusted" true 2>/dev/null || true
	fi
```

**Commit Hash:** `c3d94626`

---

### Bug #018: esim launcher path/venv

**Log:**
```text
/usr/bin/esim: line 2: cd: /home/user/repos/eSim/src/frontEnd: No such file or directory
/usr/bin/esim: line 3: /root/.esim/env/bin/activate: Permission denied
python3: can't open file '/home/user/repos/eSim/Application.py': [Errno 2] No such file or directory
```

**Root Cause:** The installer captured the wrong eSim root (running from Ubuntu/), and created the virtualenv under /root when run with sudo.

**Fix:** Resolve the repo root from the script location and use the invoking user's home for config/venv ownership.

**Changes Made:**
```text
file : install-eSim-25.04.sh
	before : config_dir="$HOME/.esim"
config_file="config.ini"
eSim_Home=`pwd`
	...
	virtualenv $config_dir/env
    
	echo "Starting the virtual env..................."
	source $config_dir/env/bin/activate
	after : script_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
eSim_Home=$(cd "$script_dir/../.." && pwd)
user_home="$HOME"
if [ -n "$SUDO_USER" ] && [ -d "/home/$SUDO_USER" ]; then
	user_home="/home/$SUDO_USER"
fi
config_dir="$user_home/.esim"
config_file="config.ini"
	...
	virtualenv $config_dir/env
	sudo chown -R "$user_home":"$user_home" "$config_dir"
    
	echo "Starting the virtual env..................."
	source $config_dir/env/bin/activate
```

**Commit Hash:** `2c92e1b4`

---

### Bug #019: chown invalid user

**Log:**
```text
Activator                                                                                           chown: invalid user: ‘/home/user:/home/user’


Error! Kindly resolve above error(s) and try again.

Aborting Installation...
```

**Root Cause:** The chown command used the home path as the user/group, causing an invalid user error.

**Fix:** Track the invoking username separately and use it for chown.

**Changes Made:**
```text
file : install-eSim-25.04.sh
	before : user_home="$HOME"
if [ -n "$SUDO_USER" ] && [ -d "/home/$SUDO_USER" ]; then
	user_home="/home/$SUDO_USER"
fi
...
	sudo chown -R "$user_home":"$user_home" "$config_dir"
	after : user_name="$USER"
user_home="$HOME"
if [ -n "$SUDO_USER" ] && [ -d "/home/$SUDO_USER" ]; then
	user_name="$SUDO_USER"
	user_home="/home/$SUDO_USER"
fi
...
	sudo chown -R "$user_name":"$user_name" "$config_dir"
```

**Commit Hash:** `9745e835`

---

### Bug #020: esim app missing

**Log:**
```text
/usr/bin/esim: line 2: cd: /home/user/repos/eSim/src/frontEnd: No such file or directory
/usr/bin/esim: line 3: /root/.esim/env/bin/activate: Permission denied
python3: can't open file '/home/user/repos/eSim/Application.py': [Errno 2] No such file or directory
```

**Root Cause:** The repository contains packaging scripts only, so the eSim application files are missing and the launcher fails.

**Fix:** Generate a launcher that checks for the application path and prints a clear error when the source/executable is missing.

**Changes Made:**
```text
file : install-eSim-25.04.sh
	before :     # Generating new esim-start.sh
	cat > esim-start.sh <<EOF
#!/bin/bash
cd $eSim_Home/src/frontEnd
source $config_dir/env/bin/activate
python3 Application.py
EOF
	after :     # Generating new esim-start.sh
	cat > esim-start.sh <<EOF
#!/bin/bash
app_dir="$eSim_Home/src/frontEnd"
app_entry="\${app_dir}/Application.py"
if [ ! -f "\$app_entry" ]; then
	app_dir="$eSim_Home"
	app_entry="\${app_dir}/Application.py"
fi

if [ ! -f "\$app_entry" ]; then
	echo "Error: eSim application not found at $eSim_Home."
	echo "Please install eSim source or packaged executable before running."
	exit 1
fi

cd "\$app_dir" || exit 1
source "$config_dir/env/bin/activate"
python3 "\$(basename "\$app_entry")"
EOF
```

**Commit Hash:** `ac360759`

---

### Bug #021: Virtualenv permission denied when creating env

**Log:**
```text
Creating virtual environment to isolate packages
RuntimeError: failed to build image pip because:
Traceback (most recent call last):
File "/usr/lib/python3/dist-packages/virtualenv/seed/embed/via_app_data/via_app_data.py", line 59, in _install
installer.install(creator.interpreter.version_info)
~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/usr/lib/python3/dist-packages/virtualenv/seed/embed/via_app_data/pip_install/base.py", line 35, in install
self._uninstall_previous_version()
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
File "/usr/lib/python3/dist-packages/virtualenv/seed/embed/via_app_data/pip_install/base.py", line 151, in _uninstall_previous_version
self._uninstall_dist(existing_dist)
~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^
File "/usr/lib/python3/dist-packages/virtualenv/seed/embed/via_app_data/pip_install/base.py", line 179, in _uninstall_dist
path.unlink()
~~~~~~~~~~~^^
File "/usr/lib/python3.13/pathlib/_local.py", line 748, in unlink
os.unlink(self)
~~~~~~~~~^^^^^^
PermissionError: [Errno 13] Permission denied: '/home/user/.esim/env/lib/python3.13/site-packages/pip/init.py'

Error! Kindly resolve above error(s) and try again.

Aborting Installation...
```

**Root Cause:** The existing virtual environment was owned by root, so pip could not remove its own files during reseeding. The uninstall step failed due to permission denial inside the env directory.

**Fix:** Ensure the config directory is owned by the target user, remove any existing env, and recreate the env as the target user to avoid root-owned files.

**Changes Made:**
```text
file : Ubuntu/install-eSim-scripts/install-eSim-25.04.sh
	before : echo "Creating virtual environment to isolate packages "
		virtualenv $config_dir/env
		sudo chown -R "$user_name":"$user_name" "$config_dir"
	after : echo "Creating virtual environment to isolate packages "
		sudo mkdir -p "$config_dir"
		sudo chown -R "$user_name":"$user_name" "$config_dir"
		if [ -d "$config_dir/env" ]; then
		echo "Existing virtual environment found. Recreating it to fix permissions."
		sudo rm -rf "$config_dir/env"
		fi
		sudo -u "$user_name" virtualenv "$config_dir/env"
```

**Commit Hash:** `7d1537a8`

---

### Bug #022: NGHDL installer rejects Ubuntu 25.04

**Log:**
```text
Installing NGHDL...........................
Archive:  nghdl.zip
   creating: nghdl/
  inflating: nghdl/CONTRIBUTION.md   
  inflating: nghdl/ghdl-4.1.0.tar.gz  
  inflating: nghdl/install-nghdl.sh  
  inflating: nghdl/LICENSE           
  inflating: nghdl/nghdl-simulator-source.tar.xz  
  inflating: nghdl/README.md         
  inflating: nghdl/verilator-4.210.tar.xz  
   creating: nghdl/Example/
   creating: nghdl/Example/combinational_logic/
   creating: nghdl/Example/combinational_logic/bin_to_gray/
  inflating: nghdl/Example/combinational_logic/bin_to_gray/bin_to_gray.vhdl  
   creating: nghdl/Example/combinational_logic/counter/
  inflating: nghdl/Example/combinational_logic/counter/decadecounter.vhdl  
  inflating: nghdl/Example/combinational_logic/counter/updown_counter.vhdl  
  inflating: nghdl/Example/combinational_logic/counter/up_counter.vhdl  
  inflating: nghdl/Example/combinational_logic/counter/up_counter_slv.vhdl  
   creating: nghdl/Example/combinational_logic/decoder/
  inflating: nghdl/Example/combinational_logic/decoder/decoder.vhdl  
   creating: nghdl/Example/combinational_logic/full_adder/
  inflating: nghdl/Example/combinational_logic/full_adder/full_adder_sl.vhdl  
  inflating: nghdl/Example/combinational_logic/full_adder/full_adder_slv.vhdl  
  inflating: nghdl/Example/combinational_logic/full_adder/full_adder_sl_slv.vhdl  
  inflating: nghdl/Example/combinational_logic/full_adder/full_adder_structural.vhdl  
   creating: nghdl/Example/combinational_logic/half_adder/
  inflating: nghdl/Example/combinational_logic/half_adder/half_adder.vhdl  
   creating: nghdl/Example/combinational_logic/mux-demux/
  inflating: nghdl/Example/combinational_logic/mux-demux/demux.vhdl  
  inflating: nghdl/Example/combinational_logic/mux-demux/mux.vhdl  
   creating: nghdl/Example/logic_gates/
  inflating: nghdl/Example/logic_gates/and_gate.vhdl  
  inflating: nghdl/Example/logic_gates/inverter.vhdl  
  inflating: nghdl/Example/logic_gates/nand_gate.vhdl  
  inflating: nghdl/Example/logic_gates/nor_gate.vhdl  
  inflating: nghdl/Example/logic_gates/or_gate.vhdl  
  inflating: nghdl/Example/logic_gates/xor_gate.vhdl  
   creating: nghdl/Example/PWM/
  inflating: nghdl/Example/PWM/pwmdecrement.vhdl  
  inflating: nghdl/Example/PWM/pwmincrement.vhdl  
   creating: nghdl/install-nghdl-scripts/
  inflating: nghdl/install-nghdl-scripts/install-nghdl-22.04.sh  
  inflating: nghdl/install-nghdl-scripts/install-nghdl-23.04.sh  
  inflating: nghdl/install-nghdl-scripts/install-nghdl-24.04.sh  
   creating: nghdl/src/
  inflating: nghdl/src/Appconfig.py  
  inflating: nghdl/src/createKicadLibrary.py  
  inflating: nghdl/src/model_generation.py  
  inflating: nghdl/src/ngspice_ghdl.py  
   creating: nghdl/src/ghdlserver/
  inflating: nghdl/src/ghdlserver/compile.sh  
  inflating: nghdl/src/ghdlserver/ghdlserver.c  
  inflating: nghdl/src/ghdlserver/ghdlserver.h  
  inflating: nghdl/src/ghdlserver/uthash.h  
  inflating: nghdl/src/ghdlserver/Utility_Package.vhdl  
  inflating: nghdl/src/ghdlserver/Vhpi_Package.vhdl  
Detected Ubuntu Version: 
Unsupported Ubuntu version: 25.04 ()
```

**Root Cause:** The NGHDL installer script doesn’t recognize Ubuntu 25.04 and aborts, so NGHDL never installs.

**Fix:** For 25.04, fall back to the 24.04 NGHDL install script (which is included in the archive) so the installation proceeds instead of exiting on an unsupported version.

**Changes Made:**
```text
file : install-eSim-25.04.sh
	before :     ./install-nghdl.sh --install       # Install NGHDL
	after :     if [[ "$(lsb_release -rs)" == "25.04" ]] && [ -f "install-nghdl-scripts/install-nghdl-24.04.sh" ]; then
		./install-nghdl-scripts/install-nghdl-24.04.sh --install
	else
		./install-nghdl.sh --install       # Install NGHDL
	fi
```

**Commit Hash:** `7f793078`

---

### Bug #023: NGHDL 25.04 detection fails

**Log:**
```text
Installing NGHDL...........................
Archive:  nghdl.zip
	inflating: nghdl/CONTRIBUTION.md   
	inflating: nghdl/ghdl-4.1.0.tar.gz  
	inflating: nghdl/install-nghdl.sh  
	inflating: nghdl/LICENSE           
	inflating: nghdl/nghdl-simulator-source.tar.xz  
	inflating: nghdl/README.md         
	inflating: nghdl/verilator-4.210.tar.xz  
	inflating: nghdl/Example/combinational_logic/bin_to_gray/bin_to_gray.vhdl  
	inflating: nghdl/Example/combinational_logic/counter/decadecounter.vhdl  
	inflating: nghdl/Example/combinational_logic/counter/updown_counter.vhdl  
	inflating: nghdl/Example/combinational_logic/counter/up_counter.vhdl  
	inflating: nghdl/Example/combinational_logic/counter/up_counter_slv.vhdl  
	inflating: nghdl/Example/combinational_logic/decoder/decoder.vhdl  
	inflating: nghdl/Example/combinational_logic/full_adder/full_adder_sl.vhdl  
	inflating: nghdl/Example/combinational_logic/full_adder/full_adder_slv.vhdl  
	inflating: nghdl/Example/combinational_logic/full_adder/full_adder_sl_slv.vhdl  
	inflating: nghdl/Example/combinational_logic/full_adder/full_adder_structural.vhdl  
	inflating: nghdl/Example/combinational_logic/half_adder/half_adder.vhdl  
	inflating: nghdl/Example/combinational_logic/mux-demux/demux.vhdl  
	inflating: nghdl/Example/combinational_logic/mux-demux/mux.vhdl  
	inflating: nghdl/Example/logic_gates/and_gate.vhdl  
	inflating: nghdl/Example/logic_gates/inverter.vhdl  
	inflating: nghdl/Example/logic_gates/nand_gate.vhdl  
	inflating: nghdl/Example/logic_gates/nor_gate.vhdl  
	inflating: nghdl/Example/logic_gates/or_gate.vhdl  
	inflating: nghdl/Example/logic_gates/xor_gate.vhdl  
	inflating: nghdl/Example/PWM/pwmdecrement.vhdl  
	inflating: nghdl/Example/PWM/pwmincrement.vhdl  
	inflating: nghdl/install-nghdl-scripts/install-nghdl-22.04.sh  
	inflating: nghdl/install-nghdl-scripts/install-nghdl-23.04.sh  
	inflating: nghdl/install-nghdl-scripts/install-nghdl-24.04.sh  
	inflating: nghdl/src/Appconfig.py  
	inflating: nghdl/src/createKicadLibrary.py  
	inflating: nghdl/src/model_generation.py  
	inflating: nghdl/src/ngspice_ghdl.py  
	inflating: nghdl/src/ghdlserver/compile.sh  
	inflating: nghdl/src/ghdlserver/ghdlserver.c  
	inflating: nghdl/src/ghdlserver/ghdlserver.h  
	inflating: nghdl/src/ghdlserver/uthash.h  
	inflating: nghdl/src/ghdlserver/Utility_Package.vhdl  
	inflating: nghdl/src/ghdlserver/Vhpi_Package.vhdl  
Detected Ubuntu Version: 
Unsupported Ubuntu version: 25.04 ()
```

**Root Cause:** The installer relies on lsb_release; when it is missing, the version string is empty and NGHDL rejects Ubuntu 25.04.

**Fix:** Resolve Ubuntu version via lsb_release when available, otherwise fall back to /etc/os-release, then use the 24.04 installer for 25.04.

**Changes Made:**
```text
file : install-eSim-25.04.sh
	before :     if [[ "$(lsb_release -rs)" == "25.04" ]] && [ -f "install-nghdl-scripts/install-nghdl-24.04.sh" ]; then
		./install-nghdl-scripts/install-nghdl-24.04.sh --install
	else
		./install-nghdl.sh --install       # Install NGHDL
	fi
	after :     local ubuntu_version=""
		if command -v lsb_release >/dev/null 2>&1; then
			ubuntu_version=$(lsb_release -rs 2>/dev/null || true)
		fi
		if [ -z "$ubuntu_version" ] && [ -r /etc/os-release ]; then
			ubuntu_version=$(. /etc/os-release; echo "${VERSION_ID:-}")
		fi

		if [[ "$ubuntu_version" == "25.04" ]] && [ -f "install-nghdl-scripts/install-nghdl-24.04.sh" ]; then
			./install-nghdl-scripts/install-nghdl-24.04.sh --install
		else
			./install-nghdl.sh --install       # Install NGHDL
		fi
```

**Commit Hash:** `b52f3034`

---

### Bug #024: NGHDL fallback script not executable

**Log:**
```text
Installing NGHDL...........................
Archive:  nghdl.zip
	inflating: nghdl/CONTRIBUTION.md   
	inflating: nghdl/ghdl-4.1.0.tar.gz  
	inflating: nghdl/install-nghdl.sh  
	inflating: nghdl/LICENSE           
	inflating: nghdl/nghdl-simulator-source.tar.xz  
	inflating: nghdl/README.md         
	inflating: nghdl/verilator-4.210.tar.xz  
	inflating: nghdl/Example/combinational_logic/bin_to_gray/bin_to_gray.vhdl  
	inflating: nghdl/Example/combinational_logic/counter/decadecounter.vhdl  
	inflating: nghdl/Example/combinational_logic/counter/updown_counter.vhdl  
	inflating: nghdl/Example/combinational_logic/counter/up_counter.vhdl  
	inflating: nghdl/Example/combinational_logic/counter/up_counter_slv.vhdl  
	inflating: nghdl/Example/combinational_logic/decoder/decoder.vhdl  
	inflating: nghdl/Example/combinational_logic/full_adder/full_adder_sl.vhdl  
	inflating: nghdl/Example/combinational_logic/full_adder/full_adder_slv.vhdl  
	inflating: nghdl/Example/combinational_logic/full_adder/full_adder_sl_slv.vhdl  
	inflating: nghdl/Example/combinational_logic/full_adder/full_adder_structural.vhdl  
	inflating: nghdl/Example/combinational_logic/half_adder/half_adder.vhdl  
	inflating: nghdl/Example/combinational_logic/mux-demux/demux.vhdl  
	inflating: nghdl/Example/combinational_logic/mux-demux/mux.vhdl  
	inflating: nghdl/Example/logic_gates/and_gate.vhdl  
	inflating: nghdl/Example/logic_gates/inverter.vhdl  
	inflating: nghdl/Example/logic_gates/nand_gate.vhdl  
	inflating: nghdl/Example/logic_gates/nor_gate.vhdl  
	inflating: nghdl/Example/logic_gates/or_gate.vhdl  
	inflating: nghdl/Example/logic_gates/xor_gate.vhdl  
	inflating: nghdl/Example/PWM/pwmdecrement.vhdl  
	inflating: nghdl/Example/PWM/pwmincrement.vhdl  
	inflating: nghdl/install-nghdl-scripts/install-nghdl-22.04.sh  
	inflating: nghdl/install-nghdl-scripts/install-nghdl-23.04.sh  
	inflating: nghdl/install-nghdl-scripts/install-nghdl-24.04.sh  
	inflating: nghdl/src/Appconfig.py  
	inflating: nghdl/src/createKicadLibrary.py  
	inflating: nghdl/src/model_generation.py  
	inflating: nghdl/src/ngspice_ghdl.py  
	inflating: nghdl/src/ghdlserver/compile.sh  
	inflating: nghdl/src/ghdlserver/ghdlserver.c  
	inflating: nghdl/src/ghdlserver/ghdlserver.h  
	inflating: nghdl/src/ghdlserver/uthash.h  
	inflating: nghdl/src/ghdlserver/Utility_Package.vhdl  
	inflating: nghdl/src/ghdlserver/Vhpi_Package.vhdl  
/home/user/Downloads/eSim-2.5/install-eSim-scripts/install-eSim-25.04.sh: line 100: ./install-nghdl-scripts/install-nghdl-24.04.sh: Permission denied
```

**Root Cause:** The fallback installer script exists but does not have the executable bit set, so the shell refuses to run it.

**Fix:** Mark the 24.04 NGHDL installer as executable before invoking it in the 25.04 fallback path.

**Changes Made:**
```text
file : install-eSim-25.04.sh
		before :     if [[ "$ubuntu_version" == "25.04" ]] && [ -f "install-nghdl-scripts/install-nghdl-24.04.sh" ]; then
				./install-nghdl-scripts/install-nghdl-24.04.sh --install
		after :     if [[ "$ubuntu_version" == "25.04" ]] && [ -f "install-nghdl-scripts/install-nghdl-24.04.sh" ]; then
				chmod +x install-nghdl-scripts/install-nghdl-24.04.sh
				./install-nghdl-scripts/install-nghdl-24.04.sh --install
```

**Commit Hash:** `eb21421b`

---

### Bug #025: Missing libcanberra-gtk-module

**Log:**
```text
Installing Gtk Canberra modules...........................
Package libcanberra-gtk-module is not available, but is referred to by another package.
This may mean that the package is missing, has been obsoleted, or
is only available from another source

Error: Package 'libcanberra-gtk-module' has no installation candidate


Error! Kindly resolve above error(s) and try again.

Aborting Installation...
```

**Root Cause:** Ubuntu 25.04 no longer provides libcanberra-gtk-module, so apt fails when the installer tries to install it unconditionally.

**Fix:** Check package availability and install libcanberra-gtk-module if present, otherwise fall back to libcanberra-gtk3-module or skip with a warning.

**Changes Made:**
```text
file : install-eSim-25.04.sh
	before :     echo "Upgrading Pip.............................."
	pip install --upgrade pip

	echo "Installing Xterm..........................."
	sudo apt-get install -y xterm
	after :     echo "Upgrading Pip.............................."
	pip install --upgrade pip

	echo "Installing Gtk Canberra modules..........................."
	if apt-cache show libcanberra-gtk-module >/dev/null 2>&1; then
		sudo apt-get install -y libcanberra-gtk-module
	elif apt-cache show libcanberra-gtk3-module >/dev/null 2>&1; then
		sudo apt-get install -y libcanberra-gtk3-module
	else
		echo "Warning: libcanberra-gtk-module not available. Skipping."
	fi

	echo "Installing Xterm..........................."
	sudo apt-get install -y xterm
```

**Commit Hash:** `7fba3d86`

---

### Bug #026: Canberra module candidate missing

**Log:**
```text
Successfully installed pip-26.0
Installing Gtk Canberra modules...........................
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
Package libcanberra-gtk-module is not available, but is referred to by another package.
This may mean that the package is missing, has been obsoleted, or
is only available from another source

E: Package 'libcanberra-gtk-module' has no installation candidate


Error! Kindly resolve above error(s) and try again.

Aborting Installation...
```

**Root Cause:** The availability check treated the package as present even though apt reports no installation candidate, so apt-get install still failed.

**Fix:** Use apt-cache policy to confirm a valid candidate before attempting installation, and fall back to the GTK3 module or skip with a warning.

**Changes Made:**
```text
file : install-eSim-25.04.sh
	before :     echo "Installing Gtk Canberra modules..........................."
	if apt-cache show libcanberra-gtk-module >/dev/null 2>&1; then
		sudo apt-get install -y libcanberra-gtk-module
	elif apt-cache show libcanberra-gtk3-module >/dev/null 2>&1; then
		sudo apt-get install -y libcanberra-gtk3-module
	else
		echo "Warning: libcanberra-gtk-module not available. Skipping."
	fi
	after :     echo "Installing Gtk Canberra modules..........................."
	canberra_policy=$(apt-cache policy libcanberra-gtk-module 2>/dev/null || true)
	if echo "$canberra_policy" | grep -q "Candidate: (none)"; then
		canberra_policy=""
	fi
	if [ -n "$canberra_policy" ]; then
		sudo apt-get install -y libcanberra-gtk-module
	else
		canberra3_policy=$(apt-cache policy libcanberra-gtk3-module 2>/dev/null || true)
		if echo "$canberra3_policy" | grep -q "Candidate: (none)"; then
			canberra3_policy=""
		fi
		if [ -n "$canberra3_policy" ]; then
			sudo apt-get install -y libcanberra-gtk3-module
		else
			echo "Warning: libcanberra-gtk-module not available. Skipping."
		fi
	fi
```

**Commit Hash:** `f6814ff2`

---

### Bug #027: NGHDL installs missing canberra

**Log:**
```text
Installing Gtk Canberra modules...........................
Package libcanberra-gtk-module is not available, but is referred to by another package.
This may mean that the package is missing, has been obsoleted, or
is only available from another source

Error: Package 'libcanberra-gtk-module' has no installation candidate


Error! Kindly resolve above error(s) and try again.

Aborting Installation...
```

**Root Cause:** NGHDL’s internal install scripts still try to install libcanberra-gtk-module, which is missing on Ubuntu 25.04, causing the NGHDL step to fail.

**Fix:** For Ubuntu 25.04, patch the extracted NGHDL install scripts to replace libcanberra-gtk-module with libcanberra-gtk3-module before running them.

**Changes Made:**
```text
file : install-eSim-25.04.sh
		before :     if [[ "$ubuntu_version" == "25.04" ]] && [ -f "install-nghdl-scripts/install-nghdl-24.04.sh" ]; then
				chmod +x install-nghdl-scripts/install-nghdl-24.04.sh
				./install-nghdl-scripts/install-nghdl-24.04.sh --install
		after :     if [[ "$ubuntu_version" == "25.04" ]]; then
				for nghdl_script in "install-nghdl.sh" "install-nghdl-scripts/install-nghdl-24.04.sh"; do
						if [ -f "$nghdl_script" ] && grep -q "libcanberra-gtk-module" "$nghdl_script"; then
								sed -i 's/libcanberra-gtk-module/libcanberra-gtk3-module/g' "$nghdl_script"
						fi
				done
		fi

		if [[ "$ubuntu_version" == "25.04" ]] && [ -f "install-nghdl-scripts/install-nghdl-24.04.sh" ]; then
				chmod +x install-nghdl-scripts/install-nghdl-24.04.sh
				./install-nghdl-scripts/install-nghdl-24.04.sh --install
```

**Commit Hash:** `50928d18`

---

### Bug #028: NGHDL rejects LLVM 20.1

**Log:**
```text
Changing directory to ghdl-4.1.0 installation
Configuring ghdl-4.1.0 build as per requirements
gcc (Ubuntu 14.2.0-19ubuntu2) 14.2.0
Copyright (C) 2024 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

Use full IEEE library
Build machine is: x86_64-linux-gnu
Unhandled version llvm 20.1.2


Error! Kindly resolve above error(s) and try again.

Aborting Installation...
```

**Root Cause:** NGHDL’s build scripts only accept LLVM 20.0 and abort when Ubuntu 25.04 ships LLVM 20.1.x.

**Fix:** For Ubuntu 25.04, patch the extracted NGHDL install scripts to replace the 20.0 version check with 20.1 when llvm-config reports 20.1.x.

**Changes Made:**
```text
file : install-eSim-25.04.sh
	before :     if [[ "$ubuntu_version" == "25.04" ]]; then
		for nghdl_script in "install-nghdl.sh" "install-nghdl-scripts/install-nghdl-24.04.sh"; do
			if [ -f "$nghdl_script" ] && grep -q "libcanberra-gtk-module" "$nghdl_script"; then
				sed -i 's/libcanberra-gtk-module/libcanberra-gtk3-module/g' "$nghdl_script"
			fi
		done
	fi
	after :     if [[ "$ubuntu_version" == "25.04" ]]; then
		for nghdl_script in "install-nghdl.sh" "install-nghdl-scripts/install-nghdl-24.04.sh"; do
			if [ -f "$nghdl_script" ] && grep -q "libcanberra-gtk-module" "$nghdl_script"; then
				sed -i 's/libcanberra-gtk-module/libcanberra-gtk3-module/g' "$nghdl_script"
			fi
		done

		llvm_version=$(llvm-config --version 2>/dev/null || true)
		if [[ "$llvm_version" == 20.1.* ]]; then
			for nghdl_script in "install-nghdl.sh" "install-nghdl-scripts/install-nghdl-24.04.sh"; do
				if [ -f "$nghdl_script" ] && grep -q "20\.0" "$nghdl_script"; then
					sed -i 's/20\.0/20.1/g' "$nghdl_script"
				fi
			done
		fi
	fi
```

**Commit Hash:** `af0b51f9`

---

### Bug #029: LLVM 20.1.2 still unhandled

**Log:**
```text
gcc (Ubuntu 14.2.0-19ubuntu2) 14.2.0
Copyright (C) 2024 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

Use full IEEE library
Build machine is: x86_64-linux-gnu
Unhandled version llvm 20.1.2


Error! Kindly resolve above error(s) and try again.

Aborting Installation...
```

**Root Cause:** NGHDL still sees the full LLVM patch version (20.1.2) and rejects it as unsupported.

**Fix:** When LLVM 20.1.x is detected, add a local llvm-config shim that reports 20.1 for --version so NGHDL accepts the version.

**Changes Made:**
```text
file : install-eSim-25.04.sh
	before :         llvm_version=$(llvm-config --version 2>/dev/null || true)
		if [[ "$llvm_version" == 20.1.* ]]; then
			for nghdl_script in "install-nghdl.sh" "install-nghdl-scripts/install-nghdl-24.04.sh"; do
				if [ -f "$nghdl_script" ] && grep -q "20\.0" "$nghdl_script"; then
					sed -i 's/20\.0/20.1/g' "$nghdl_script"
				fi
			done
		fi
	after :         llvm_version=$(llvm-config --version 2>/dev/null || true)
		if [[ "$llvm_version" == 20.1.* ]]; then
			for nghdl_script in "install-nghdl.sh" "install-nghdl-scripts/install-nghdl-24.04.sh"; do
				if [ -f "$nghdl_script" ] && grep -q "20\.0" "$nghdl_script"; then
					sed -i 's/20\.0/20.1/g' "$nghdl_script"
				fi
			done
			cat > ./llvm-config <<'EOF'
#!/bin/sh
if [ "$1" = "--version" ]; then
	echo "20.1"
	exit 0
fi
exec /usr/bin/llvm-config "$@"
EOF
			chmod +x ./llvm-config
			export PATH="$PWD:$PATH"
		fi
```

**Commit Hash:** `47d5f148`

---

### Bug #030: LLVM 20.1.2 still unhandled

**Log:**
```text
gcc (Ubuntu 14.2.0-19ubuntu2) 14.2.0
Copyright (C) 2024 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

Use full IEEE library
Build machine is: x86_64-linux-gnu
Unhandled version llvm 20.1.2


Error! Kindly resolve above error(s) and try again.

Aborting Installation...
```

**Root Cause:** LLVM Version mismatch

**Fix:** updated the version to commonly used 18.0

**Changes Made:**
```text
file : install-eSim-25.04.sh
	before :         llvm_version=$(llvm-config --version 2>/dev/null || true)
		if [[ "$llvm_version" == 20.1.* ]]; then
			for nghdl_script in "install-nghdl.sh" "install-nghdl-scripts/install-nghdl-24.04.sh"; do
				if [ -f "$nghdl_script" ] && grep -q "20\.0" "$nghdl_script"; then
					sed -i 's/20\.0/20.1/g' "$nghdl_script"
				fi
			done
		fi
	after :         llvm_version=$(llvm-config --version 2>/dev/null || true)
		if [[ "$llvm_version" == 20.1.* ]]; then
			for nghdl_script in "install-nghdl.sh" "install-nghdl-scripts/install-nghdl-24.04.sh"; do
				if [ -f "$nghdl_script" ]; then
					sed -i 's/20\.1/18.0/g' "$nghdl_script"
					sed -i 's/20\.0/18.0/g' "$nghdl_script"
				fi
			done
			cat > ./llvm-config <<'EOF'
#!/bin/sh
if [ "$1" = "--version" ]; then
	echo "18.0"
	exit 0
fi
exec /usr/bin/llvm-config "$@"
EOF
			chmod +x ./llvm-config
			export PATH="$PWD:$PATH"
		fi
```

**Commit Hash:** `548b9109`

---

### Bug #031: GHDL configure rejects LLVM 20.x

**Log:**
```text
gcc (Ubuntu 14.2.0-19ubuntu2) 14.2.0
Copyright (C) 2024 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

Use full IEEE library
Build machine is: x86_64-linux-gnu
Unhandled version llvm 20.1.2


Error! Kindly resolve above error(s) and try again.

Aborting Installation...
```

**Root Cause:** GHDL 4.1.0 configure script limits LLVM major versions to 1x, so LLVM 20.1.x fails validation.

**Fix:** Patch the extracted ghdl-4.1.0/configure to accept major versions 10-29, then keep the llvm-config shim reporting 20.1.

**Changes Made:**
```text
file : install-eSim-25.04.sh
	before :         llvm_version=$(llvm-config --version 2>/dev/null || true)
		if [[ "$llvm_version" == 20.1.* ]]; then
			cat > ./llvm-config <<'EOF'
#!/bin/sh
if [ "$1" = "--version" ]; then
	echo "18.0"
	exit 0
fi
exec /usr/bin/llvm-config "$@"
EOF
			chmod +x ./llvm-config
			export PATH="$PWD:$PATH"
		fi
	after :         if [ -f "ghdl-4.1.0.tar.gz" ]; then
		tar -xzf ghdl-4.1.0.tar.gz
		if [ -f "ghdl-4.1.0/configure" ]; then
			sed -i 's/check_version 18.1 \$llvm_version ||/check_version 18.1 $llvm_version ||\n       check_version 19.0 $llvm_version ||\n       check_version 20.0 $llvm_version ||\n       check_version 20.1 $llvm_version ||/' ghdl-4.1.0/configure
		fi
		tar -czf ghdl-4.1.0.tar.gz ghdl-4.1.0
		rm -rf ghdl-4.1.0
	fi

	llvm_version=$(llvm-config --version 2>/dev/null || true)
	if [[ "$llvm_version" == 20.1.* ]]; then
		cat > ./llvm-config <<'EOF'
#!/bin/sh
if [ "$1" = "--version" ]; then
	echo "20.1"
	exit 0
fi
exec /usr/bin/llvm-config "$@"
EOF
		chmod +x ./llvm-config
		export PATH="$PWD:$PATH"
	fi
```

**Commit Hash:** `a5eec013`

---

### Bug #032: NGHDL sub-installer chain-link failure

**Log:**
```text
Installing NGHDL...........................
Running script: /home/user/repos/eSim/Ubuntu/nghdl/install-nghdl-scripts/install-nghdl-25.04.sh --install
Installing Gtk Canberra modules...........................
...
Installing ghdl-4.1.0 LLVM................................
ghdl-4.1.0 successfully extracted
Changing directory to ghdl-4.1.0 installation
Configuring ghdl-4.1.0 build as per requirements
gcc (Ubuntu 14.2.0-19ubuntu2) 14.2.0
Copyright (C) 2024 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

Use full IEEE library
Build machine is: x86_64-linux-gnu
Unhandled version llvm 20.1.2


Error! Kindly resolve above error(s) and try again.

Aborting Installation...
```

**Root Cause:** The NGHDL sub-installer was bypassing eSim's main fixes due to its own hardcoded version checks for GHDL configure. Even though the main install script patched the GHDL configure in nghdl directory, the NGHDL sub-installer (install-nghdl-25.04.sh) extracted and ran the configure without the patch.

**Fix:** Patch the GHDL configure script inside install-nghdl-25.04.sh's installGHDL function before calling ./configure to support LLVM 20.x versions by using sed to add version 2[0-9] patterns.

**Changes Made:**
```text
file : Ubuntu/nghdl/install-nghdl.sh
before :         "24.04")
SCRIPT="$SCRIPT_DIR/install-nghdl-24.04.sh"
;;
*)
echo "Unsupported Ubuntu version: $VERSION_ID ($FULL_VERSION)"
exit 1
;;
after :         "24.04")
SCRIPT="$SCRIPT_DIR/install-nghdl-24.04.sh"
;;
"25.04")
SCRIPT="$SCRIPT_DIR/install-nghdl-25.04.sh"
;;
*)
echo "Unsupported Ubuntu version: $VERSION_ID ($FULL_VERSION)"
exit 1
;;

file : Ubuntu/nghdl/install-nghdl-scripts/install-nghdl-25.04.sh
before :     echo "Configuring $ghdl build as per requirements"
chmod +x configure
# Other configure flags can be found at - https://github.com/ghdl/ghdl/blob/master/configure
./configure --with-llvm-config=/usr/bin/llvm-config
after :     echo "Configuring $ghdl build as per requirements"
chmod +x configure

# Patch GHDL configure to allow LLVM 20.x
sed -i 's/1[0-9]/2[0-9]/g' configure

# Other configure flags can be found at - https://github.com/ghdl/ghdl/blob/master/configure
./configure --with-llvm-config=/usr/bin/llvm-config
Commit Message Format: Support Ubuntu 25.04 in NGHDL installer
```

**Commit Hash:** `fcb6c029`

---

### Bug #033: NGHDL clean reinstall fails on existing directory

**Log:**
```text
mv: cannot overwrite '/home/user/nghdl-simulator/nghdl-simulator-source': Directory not empty

Error! Kindly resolve above error(s) and try again.

Aborting Installation...
```

**Root Cause:** The mv command fails when trying to rename the extracted nghdl-simulator-source directory to nghdl-simulator if the destination already exists with files from a previous installation attempt.

**Fix:** Remove the existing NGHDL directory before moving the newly extracted source. This performs a clean reinstall while preserving user configuration in ~/.nghdl/ since that's a separate directory.

**Changes Made:**
```text
file : Ubuntu/nghdl/install-nghdl-scripts/install-nghdl-25.04.sh
before :     tar -xJf $nghdl-source.tar.xz -C $HOME
mv $HOME/$nghdl-source $HOME/$nghdl
after :     tar -xJf $nghdl-source.tar.xz -C $HOME
rm -rf $HOME/$nghdl
mv $HOME/$nghdl-source $HOME/$nghdl
```

**Commit Hash:** `f339911d`

---

### Bug #034: GHDL configure fails with incorrect srcdir

**Log:**
```text
Changing directory to ghdl-4.1.0 installation
Configuring ghdl-4.1.0 build as per requirements
Incorrect srcdir; try with --srcdir=xx
srcdir=.


Error! Kindly resolve above error(s) and try again.

Aborting Installation...
```

**Root Cause:** The script both forced --srcdir=. and mutated GHDL’s configure with sed. That edit invalidated the configure signature check, so it failed even when srcdir was correct.

**Fix:** Resolve the source root dynamically, pass an absolute --srcdir, avoid editing configure, and ensure a clean extract before building.

**Changes Made:**
```text
file : Ubuntu/nghdl/install-nghdl-scripts/install-nghdl-25.04.sh
before : src_dir=`pwd`
...
tar xvf $ghdl.tar.gz
...
cd $ghdl/
...
# Patch GHDL configure to allow LLVM 20.x
sed -i 's/1[0-9]/2[0-9]/g' configure
...
./configure --srcdir=. --with-llvm-config=/usr/bin/llvm-config
after : script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
src_dir="$(cd "$script_dir/.." && pwd)"
...
if [ -d "$src_dir/$ghdl" ]; then
	rm -rf "$src_dir/$ghdl"
fi
tar xvf $ghdl.tar.gz
...
cd "$src_dir/$ghdl/"
...
ghdl_src_dir="$(pwd -P)"
./configure --srcdir="$ghdl_src_dir" --with-llvm-config=/usr/bin/llvm-config
commit message : Fix GHDL srcdir detection in NGHDL installer
```

**Commit Hash:** `6c6fa949`

---

### Bug #035: Incorrect eSim_Home Path in Startup Script

**Log:**
```text
user@Ubuntu-25:~/repos/eSim/Ubuntu$ esim
Error: eSim application not found at /home/user/repos/eSim.
Please install eSim source or packaged executable before running.
```

**Root Cause:** The installer generated a startup script that did not reliably locate the front-end; the launcher failed to find `Application.py`.

**Fix:** The generated `esim-start.sh` now computes `REPO_ROOT` from the installer's `eSim_Home` at install time, checks common candidate locations (`src/frontEnd`, `src/FrontEnd`, `frontEnd`, repo root`) and falls back to a `find` search under the repository root to locate `Application.py`. This makes the launcher dynamic and general for any installer layout.

**Changes Made:**
```text
file : install-eSim-25.04.sh
    before : #!/bin/bash
app_dir="${eSim_Home}/src/frontEnd"
app_entry="${app_dir}/Application.py"
if [ ! -f "\$app_entry" ]; then
    app_dir="${eSim_Home}"
    app_entry="${app_dir}/Application.py"
fi

if [ ! -f "\$app_entry" ]; then
    echo "Error: eSim application not found at ${eSim_Home}."
    echo "Please install eSim source or packaged executable before running."
    exit 1
fi

cd "\$app_dir" || exit 1
source "${config_dir}/env/bin/activate"
python3 "$(basename "\$app_entry")"
    after : #!/bin/bash
# Dynamically determine the eSim front-end directory based on installer repo root
REPO_ROOT="${eSim_Home}"
candidates=(
    "$REPO_ROOT/src/frontEnd"
    "$REPO_ROOT/src/FrontEnd"
    "$REPO_ROOT/frontEnd"
    "$REPO_ROOT"
)
app_dir=""
for c in "${candidates[@]}"; do
    if [ -f "$c/Application.py" ]; then
        app_dir="$c"
        break
    fi
done

if [ -z "$app_dir" ]; then
    found=$(find "$REPO_ROOT" -maxdepth 4 -type f -name 'Application.py' -print -quit 2>/dev/null || true)
    if [ -n "$found" ]; then
        app_dir=$(dirname "$found")
    fi
fi

if [ -z "$app_dir" ]; then
    echo "Error: eSim application not found under ${eSim_Home}."
    echo "Please install eSim source or packaged executable before running."
    exit 1
fi

app_entry="\$app_dir/Application.py"
cd "\$app_dir" || exit 1
source "${config_dir}/env/bin/activate"
python3 "$(basename "\$app_entry")"
```

**Commit Hash:** `c0591ad2`

---

### Bug #036: Source Discovery Failure

**Log:**
```text
eSim desktop entry and launcher pointed to empty directories or failed to start.


Error! Kindly resolve above error(s) and try again.

Aborting Installation...
```

**Root Cause:** The installer was pointing to empty directories because the source code was in a different path or not extracted.

**Fix:** Added a dynamic discovery step to locate Application.py and set paths based on the actual file system state.

**Changes Made:**
```text
file : install-eSim-25.04.sh
	before : createConfigFile and createDesktopStartScript used a static repo-root eSim_Home assumption.
	after : discover Application.py under the user's home, set eSim_Home to the parent of the src directory, and use that verified path for launcher and desktop entry.
```

**Commit Hash:** `b556b64e`

---
