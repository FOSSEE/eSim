#!/bin/bash 
#=============================================================================
#          FILE: install-eSim.sh
# 
#         USAGE: ./install-eSim.sh --install 
#                            OR
#                ./install-eSim.sh --uninstall
#                
#   DESCRIPTION: Installation script for eSim EDA Suite
#
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#       AUTHORS: Fahim Khan, Rahul Paknikar, Saurabh Bansode,
#                Sumanto Kar, Partha Singha Roy, Harsha Narayana P, 
#                Jayanth Tatineni, Anshul Verma
#       MENTORS: Sumanto Kar, Varad Patil, Shanti Priya K, Aditya M
#       INTERNS: Akshay Rukade, Haripriyan R
#  ORGANIZATION: eSim Team, FOSSEE, IIT Bombay
#       CREATED: Wednesday 15 July 2015 15:26
#      REVISION: Sunday 25 May 2025 17:40
#=============================================================================

# All variables goes here
config_dir="$HOME/.esim"
config_file="config.ini"
eSim_Home=`pwd`
ngspiceFlag=0

## All Functions goes here

error_exit()
{

    echo -e "\n\nError! Kindly resolve above error(s) and try again."
    echo -e "\nAborting Installation...\n"

}


function createConfigFile
{

    # Creating config.ini file and adding configuration information
    # Check if config file is present
    if [ -d $config_dir ];then
        rm $config_dir/$config_file && touch $config_dir/$config_file
    else
        mkdir $config_dir && touch $config_dir/$config_file
    fi
    
    echo "[eSim]" >> $config_dir/$config_file
    echo "eSim_HOME = $eSim_Home" >> $config_dir/$config_file
    echo "LICENSE = %(eSim_HOME)s/LICENSE" >> $config_dir/$config_file
    echo "KicadLib = %(eSim_HOME)s/library/kicadLibrary.tar.xz" >> $config_dir/$config_file
    echo "IMAGES = %(eSim_HOME)s/images" >> $config_dir/$config_file
    echo "VERSION = %(eSim_HOME)s/VERSION" >> $config_dir/$config_file
    echo "MODELICA_MAP_JSON = %(eSim_HOME)s/library/ngspicetoModelica/Mapping.json" >> $config_dir/$config_file
   
}


#function installNghdl
#{
#
#    echo "Installing NGHDL..........................."
#    unzip -o nghdl.zip
#    cd nghdl/
#    chmod +x install-nghdl.sh
#
#    # Do not trap on error of any command. Let NGHDL script handle its own errors.
#    trap "" ERR
#
#    ./install-nghdl.sh --install       # Install NGHDL
#        
#    # Set trap again to error_exit function to exit on errors
#    trap error_exit ERR
#
#    ngspiceFlag=1
#    cd ../
#
#}

#function installNghdl
#{
#    echo "Installing NGHDL..........................."
#
#    NGHDL_FILE="$eSim_Home/nghdl.zip"
#    NGHDL_DIR="$eSim_Home/nghdl"
#
#    # Check if zip file exists
#    if [ -f "$NGHDL_FILE" ]; then
#        echo "Extracting NGHDL..."
#        unzip -o "$NGHDL_FILE" -d "$eSim_Home"
#
#        # Check if folder exists after extraction
#        if [ -d "$NGHDL_DIR" ]; then
#            cd "$NGHDL_DIR"
#            chmod +x install-nghdl.sh
#
#            # Let NGHDL script handle its own errors
#            trap "" ERR
#
#            ./install-nghdl.sh --install
#
#            # Restore error handling
#            trap error_exit ERR
#
#            cd "$eSim_Home"
#            ngspiceFlag=1
#        else
#            echo "NGHDL directory not found after extraction. Skipping NGHDL setup."
#        fi
#
#    else
#        echo "NGHDL zip file not found. Skipping NGHDL installation."
#    fi
#}

# -----------------------------------------------------------------------------
# FIX (Issue 17 - NGHDL/LLVM/GHDL Incompatibility on Ubuntu 25.x):
#
# NGHDL requires GHDL v0.37 (LLVM backend) and Verilator v4.210.
# These exact versions are NOT available on Ubuntu 25.x via apt.
# Ubuntu 25.x ships GHDL 4.x (incompatible ABI) and LLVM 19+ (NGHDL
# build expects LLVM 14 or earlier). Attempting to build nghdl-simulator
# from the bundled source tarball will therefore fail at compile time.
#
# Additionally, the nghdl.zip file is not included in the installer
# repository and must be supplied separately.
#
# Workaround for Ubuntu 25.x users:
#   Use the Flatpak version of eSim which bundles compatible tool versions:
#     flatpak install flathub org.fossee.eSim
#     flatpak run org.fossee.eSim
# -----------------------------------------------------------------------------

function installNghdl
{
    echo "Installing NGHDL..........................."

    # Check Ubuntu major version — NGHDL is not compatible with Ubuntu 25.x+
    # due to GHDL and LLVM version conflicts (see note above).
    ubuntu_version=$(lsb_release -rs)
    major_version=$(echo "$ubuntu_version" | cut -d. -f1)

    if [[ "$major_version" -ge 25 ]]; then
        echo "------------------------------------------------------------"
        echo "WARNING: NGHDL is NOT supported on Ubuntu $ubuntu_version."
        echo "  NGHDL requires GHDL v0.37 (LLVM) and Verilator v4.210."
        echo "  Ubuntu 25.x ships GHDL 4.x and LLVM 19+ which are"
        echo "  incompatible with the NGHDL build system."
        echo "  Skipping NGHDL installation."
        echo "  For full NGHDL support, use the Flatpak version of eSim:"
        echo "    flatpak install flathub org.fossee.eSim"
        echo "------------------------------------------------------------"
        return
    fi

    NGHDL_FILE="$eSim_Home/nghdl.zip"
    NGHDL_DIR="$eSim_Home/nghdl"

    # Check if zip file exists before attempting extraction
    if [ -f "$NGHDL_FILE" ]; then
        echo "Extracting NGHDL..."
        unzip -o "$NGHDL_FILE" -d "$eSim_Home"

        # Verify extraction produced the expected directory
        if [ -d "$NGHDL_DIR" ]; then
            cd "$NGHDL_DIR"
            chmod +x install-nghdl.sh

            # Let NGHDL script handle its own errors
            trap "" ERR

            ./install-nghdl.sh --install

            # Restore error handling
            trap error_exit ERR

            cd "$eSim_Home"
            ngspiceFlag=1
        else
            echo "NGHDL directory not found after extraction. Skipping NGHDL setup."
        fi

    else
        echo "NGHDL zip file not found. Skipping NGHDL installation."
    fi
}

function installSky130Pdk
{

    echo "Installing SKY130 PDK......................"

    
    # Remove any previous sky130-fd-pdr instance, if any
    sudo rm -rf /usr/share/local/sky130_fd_pr
    #installing sky130
    volare enable --pdk sky130 --pdk-root /usr/share/local/ 0fe599b2afb6708d281543108caf8310912f54af
    # Copy SKY130 library
    echo "Copying SKY130 PDK........................."

    sudo mkdir -p /usr/share/local/
    sudo mv /usr/share/local/volare/sky130/versions/0fe599b2afb6708d281543108caf8310912f54af/sky130A/libs.ref/sky130_fd_pr /usr/share/local/
    rm -rf /usr/share/local/volare/

    # Change ownership from root to the user
    sudo chown -R $USER:$USER /usr/share/local/sky130_fd_pr/

}

function installIhpPdk
{
    echo -n "Do you want to install IHP Open PDK for analog IC design? (y/n): "
    read installIhp
    
    if [ "$installIhp" == "y" -o "$installIhp" == "Y" ]; then
        echo "Installing IHP Open PDK........................"
        
        if [ -f "ihp/ihp-install-script.sh" ]; then
            cd ihp/
            chmod +x ihp-install-script.sh
            trap "" ERR
            ./ihp-install-script.sh --install
            trap error_exit ERR
            cd ../
        else
            echo "IHP install script not found. Skipping..."
        fi
    else
        echo "Skipping IHP Open PDK installation"
    fi
}


function installKicad
{
    echo "Installing KiCad..........................."

    # Detect Ubuntu version
    ubuntu_version=$(lsb_release -rs)
    major_version=$(echo "$ubuntu_version" | cut -d. -f1)

    # Define KiCad PPA based on version
    if [[ "$major_version" -ge 24 ]]; then
        echo "Ubuntu 24 or newer detected."
        kicadppa="kicad/kicad-8.0-releases"
    else
        echo "Older Ubuntu detected."
        kicadppa="kicad/kicad-6.0-releases"
    fi

    # Check if KiCad is already installed
    if dpkg -s kicad &>/dev/null; then
        installed_version=$(dpkg-query -W -f='${Version}' kicad | cut -d'.' -f1)

        if [[ "$installed_version" == "8" ]]; then
            echo "KiCad 8 is already installed."
            return
        else
            echo "Different KiCad version ($installed_version) detected."

            # Auto-remove incompatible version (no user prompt for automation)
            echo "Removing incompatible KiCad version..."
            sudo apt-get remove --purge -y kicad kicad-footprints kicad-libraries kicad-symbols kicad-templates
            sudo apt-get autoremove -y
        fi
    fi

    echo "Setting up KiCad repository..."

    # Try adding PPA (preferred for KiCad 8)
    if sudo add-apt-repository -y "ppa:$kicadppa"; then
        echo "KiCad PPA added successfully."
        sudo apt-get update
        echo "Installing KiCad from PPA (preferred version)..."
    else
        echo "Warning: Failed to add KiCad PPA. Falling back to Ubuntu repository."
        sudo apt-get update
    fi

    # Install KiCad (always runs)
    sudo apt-get install -y kicad kicad-footprints kicad-libraries kicad-symbols kicad-templates

    # Verify installation
    if command -v kicad &> /dev/null; then
        echo "KiCad installation completed successfully!"
    else
        echo "Error: KiCad installation failed."
        exit 1
    fi
}



#    # Detect Ubuntu version
#    ubuntu_version=$(lsb_release -rs)
#
#    # Define KiCad PPAs based on Ubuntu version
#    if [[ "$ubuntu_version" == "24.04" ]]; then
#        echo "Ubuntu 24.04 detected."
#        kicadppa="kicad/kicad-8.0-releases"
#
#        # Check if KiCad is installed using dpkg-query for the main package
#        if dpkg -s kicad &>/dev/null; then
#            installed_version=$(dpkg-query -W -f='${Version}' kicad | cut -d'.' -f1)
#            if [[ "$installed_version" != "8" ]]; then
#                echo "A different version of KiCad ($installed_version) is installed."
#                read -p "Do you want to remove it and install KiCad 8.0? (yes/no): " response
#
#                if [[ "$response" =~ ^([Yy][Ee][Ss]|[Yy])$ ]]; then
#                    echo "Removing KiCad $installed_version..."
#                    sudo apt-get remove --purge -y kicad kicad-footprints kicad-libraries kicad-symbols kicad-templates
#                    sudo apt-get autoremove -y
#                else
#                    echo "Exiting installation. KiCad $installed_version remains installed."
#                    exit 1
#                fi
#            else
#                echo "KiCad 8.0 is already installed."
#                exit 0
#            fi
#        fi
#
#    else
#        kicadppa="kicad/kicad-6.0-releases"
#    fi

    # Check if the PPA is already added
#    if ! grep -q "^deb .*${kicadppa}" /etc/apt/sources.list /etc/apt/sources.list.d/* 2>/dev/null; then
#        echo "Adding KiCad PPA to local apt repository: $kicadppa"
#        sudo add-apt-repository -y "ppa:$kicadppa"
#        sudo apt-get update
#    else
#        echo "KiCad PPA is already present in sources."
#    fi

	echo "Skipping KiCad PPA (not supported for this Ubuntu version)"
	sudo apt-get update

    # Install KiCad packages
    sudo apt-get install -y --no-install-recommends kicad kicad-footprints kicad-libraries kicad-symbols kicad-templates

    echo "KiCad installation completed successfully!"
}


function installDependency
{

    set +e      # Temporary disable exit on error
    trap "" ERR # Do not trap on error of any command

    # Update apt repository
    echo "Updating apt index files..................."
    sudo apt-get update
    
    set -e      # Re-enable exit on error
    trap error_exit ERR
    
    echo "Instaling virtualenv......................."
    sudo apt install python3-virtualenv
   
    echo "Creating virtual environment to isolate packages "
    virtualenv $config_dir/env
    
    echo "Starting the virtual env..................."
    source $config_dir/env/bin/activate

    echo "Upgrading Pip.............................."
    pip install --upgrade pip
    
    echo "Installing Xterm..........................."
    sudo apt-get install -y xterm
    
    echo "Installing Psutil.........................."
    sudo apt-get install -y python3-psutil
    
    echo "Installing PyQt5..........................."
    sudo apt-get install -y python3-pyqt5

    echo "Installing Matplotlib......................"
    sudo apt-get install -y python3-matplotlib

    echo "Installing Setuptools..................."
    sudo apt-get install -y python3-setuptools

    # Install NgVeri Depedencies
    echo "Installing Pip3............................"
    sudo apt install -y python3-pip

#   -----------------------------------------------------------------------------
#   FIX (Issue 18 - PEP 668 / pip3 outside venv fails on Ubuntu 25.x):
#
#   Ubuntu 25.x enforces PEP 668 (externally-managed-environment).
#   Calling bare 'pip3 install <pkg>' on the system Python raises:
#     error: externally-managed-environment
#   because the system Python is managed by apt and pip is blocked
#   from writing into it directly.
#
#   All pip installs below that previously used bare 'pip3' have been
#   changed to use 'pip' (which resolves to the active virtualenv's pip
#   after 'source $config_dir/env/bin/activate' above).
#   This ensures all packages are installed inside the isolated venv,
#   not into the system Python — which is the correct behaviour anyway.
#
#   Original lines (removed):
#    pip3 install watchdog
#    pip3 install --upgrade https://github.com/hdl/pyhdlparser/tarball/master
#    pip3 install makerchip-app
#    pip3 install sandpiper-saas
#    pip3 install hdlparse
#    pip3 install matplotlib
#    pip3 install PyQt5
#    pip3 install volare
#   -----------------------------------------------------------------------------

    echo "Installing Watchdog........................"
    pip install watchdog

    echo "Installing Hdlparse........................"
    pip install --upgrade https://github.com/hdl/pyhdlparser/tarball/master

    echo "Installing Makerchip......................."
    pip install makerchip-app

    echo "Installing SandPiper Saas.................."
    pip install sandpiper-saas

    echo "Installing Hdlparse......................"
    pip install hdlparse

    echo "Installing matplotlib................"
    pip install matplotlib

    echo "Installing PyQt5............."
    pip install PyQt5

    echo "Installing volare"
    sudo apt-get install -y xz-utils || echo "xz-utils already installed"
    pip install volare
}


#function copyKicadLibrary
#{
#
#    #Extract custom KiCad Library
#    tar -xJf library/kicadLibrary.tar.xz
#
#    if [ -d ~/.config/kicad/6.0 ];then
#        echo "kicad config folder already exists"
#    else 
#        echo ".config/kicad/6.0 does not exist"
#        mkdir -p ~/.config/kicad/6.0
#    fi
#
#    # Copy symbol table for eSim custom symbols 
#    cp kicadLibrary/template/sym-lib-table ~/.config/kicad/6.0/
#    echo "symbol table copied in the directory"
#
#    # Copy KiCad symbols made for eSim
#    sudo cp -r kicadLibrary/eSim-symbols/* /usr/share/kicad/symbols/
#
#    set +e      # Temporary disable exit on error
#    trap "" ERR # Do not trap on error of any command
#    
#    # Remove extracted KiCad Library - not needed anymore
#    rm -rf kicadLibrary
#
#    set -e      # Re-enable exit on error
#    trap error_exit ERR
#
#    #Change ownership from Root to the User
#    sudo chown -R $USER:$USER /usr/share/kicad/symbols/
#
#}

function copyKicadLibrary
{
    LIB_PATH="$eSim_Home/library"
    LIB_FILE="$LIB_PATH/kicadLibrary.tar.xz"

    # Create library directory
    mkdir -p "$LIB_PATH"

    # Extract only if file exists
    if [ -f "$LIB_FILE" ]; then
        echo "Extracting KiCad library..."
        tar -xJf "$LIB_FILE" -C "$LIB_PATH"

        # Check if extracted folder exists
        if [ -d "$LIB_PATH/kicadLibrary" ]; then

#           -----------------------------------------------------------------------------
#           FIX (Issue 19 - KiCad config directory hardcoded to 6.0, wrong for KiCad 8):
#
#           The original code always used ~/.config/kicad/6.0/ as the config directory.
#           When KiCad 8 is installed (which is the case on Ubuntu 24+), it uses
#           ~/.config/kicad/8.0/ instead. Copying sym-lib-table into the 6.0 path means
#           eSim's custom symbols are never loaded by KiCad 8.
#
#           Original lines (removed):
#            if [ -d ~/.config/kicad/6.0 ]; then
#                echo "kicad config folder already exists"
#            else
#                echo ".config/kicad/6.0 does not exist"
#                mkdir -p ~/.config/kicad/6.0
#            fi
#            cp "$LIB_PATH/kicadLibrary/template/sym-lib-table" ~/.config/kicad/6.0/
#           -----------------------------------------------------------------------------

            # Detect installed KiCad major version to resolve correct config directory
            kicad_major=$(kicad --version 2>/dev/null | grep -oP '^\d+' || echo "8")
            kicad_config_dir="$HOME/.config/kicad/${kicad_major}.0"

            if [ -d "$kicad_config_dir" ]; then
                echo "KiCad config folder already exists: $kicad_config_dir"
            else
                echo "Creating KiCad config directory: $kicad_config_dir"
                mkdir -p "$kicad_config_dir"
            fi

            # Copy symbol table into the correct versioned config directory
            cp "$LIB_PATH/kicadLibrary/template/sym-lib-table" "$kicad_config_dir/"
            echo "symbol table copied"

            # Copy symbols
            sudo cp -r "$LIB_PATH/kicadLibrary/eSim-symbols/"* /usr/share/kicad/symbols/

            # Cleanup
            rm -rf "$LIB_PATH/kicadLibrary"

            # Fix permissions
            sudo chown -R $USER:$USER /usr/share/kicad/symbols/

        else
            echo "Extraction failed or folder missing. Skipping KiCad library setup."
        fi

    else
        echo "KiCad library file not found. Skipping library setup."
    fi
}


function createDesktopStartScript
{    

    # Generating new esim-start.sh
    echo '#!/bin/bash' > esim-start.sh
    echo "cd $eSim_Home/src/frontEnd" >> esim-start.sh
    echo "source $config_dir/env/bin/activate" >> esim-start.sh
    echo "python3 Application.py" >> esim-start.sh

    # Make it executable
    sudo chmod 755 esim-start.sh
    # Copy esim start script
    sudo cp -vp esim-start.sh /usr/bin/esim
    # Remove local copy of esim start script
    rm esim-start.sh

    # Generating esim.desktop file
    echo "[Desktop Entry]" > esim.desktop
    echo "Version=1.0" >> esim.desktop
    echo "Name=eSim" >> esim.desktop
    echo "Comment=EDA Tool" >> esim.desktop
    echo "GenericName=eSim" >> esim.desktop
    echo "Keywords=eda-tools" >> esim.desktop
    echo "Exec=esim %u" >> esim.desktop
    echo "Terminal=true" >> esim.desktop
    echo "X-MultipleArgs=false" >> esim.desktop
    echo "Type=Application" >> esim.desktop
    getIcon="$config_dir/logo.png"
    echo "Icon=$getIcon" >> esim.desktop
    echo "Categories=Development;" >> esim.desktop
    echo "MimeType=text/html;text/xml;application/xhtml+xml;application/xml;application/rss+xml;application/rdf+xml;image/gif;image/jpeg;image/png;x-scheme-handler/http;x-scheme-handler/https;x-scheme-handler/ftp;x-scheme-handler/chrome;video/webm;application/x-xpinstall;" >> esim.desktop
    echo "StartupNotify=true" >> esim.desktop

    # Make esim.desktop file executable
    sudo chmod 755 esim.desktop
    # Copy desktop icon file to share applications
    sudo cp -vp esim.desktop /usr/share/applications/
    
#    # Copy desktop icon file to Desktop
#    cp -vp esim.desktop $HOME/Desktop/
#
#    set +e      # Temporary disable exit on error
#    trap "" ERR # Do not trap on error of any command
#
#    # Make esim.desktop file as trusted application
#    gio set $HOME/Desktop/esim.desktop "metadata::trusted" true
#    # Set Permission and Execution bit
#    chmod a+x $HOME/Desktop/esim.desktop
#
#    # Remove local copy of esim.desktop file
#    rm esim.desktop
#
#    set -e      # Re-enable exit on error
#    trap error_exit ERR

	USER_HOME=$(eval echo ~$SUDO_USER)

	# Copy to Desktop
	mkdir -p "$USER_HOME/Desktop"
	cp -vp esim.desktop "$USER_HOME/Desktop/"

	set +e
	trap "" ERR

	# Make trusted
#	gio set "$USER_HOME/Desktop/esim.desktop" "metadata::trusted" true
	
	gio set "$USER_HOME/Desktop/esim.desktop" "metadata::trusted" true 2>/dev/null || echo "Skipping gio trust setting"
	
	chmod a+x "$USER_HOME/Desktop/esim.desktop"

	rm esim.desktop

	set -e
	trap error_exit ERR

    # Copying logo.png to .esim directory to access as icon
#    cp -vp images/logo.png $config_dir
    
    if [ -f "images/logo.png" ]; then
    	cp -vp images/logo.png $config_dir
    else
	echo "Logo file not found. Skipping icon setup."
    fi


}


####################################################################
#                   MAIN START FROM HERE                           #
####################################################################

### Checking if file is passsed as argument to script

if [ "$#" -eq 1 ];then
    option=$1
else
    echo "USAGE : "
    echo "./install-eSim.sh --install"
    echo "./install-eSim.sh --uninstall"
    exit 1;
fi

## Checking flags

if [ $option == "--install" ];then

    set -e  # Set exit option immediately on error
    set -E  # inherit ERR trap by shell functions

    # Trap on function error_exit before exiting on error
    trap error_exit ERR


    echo "Enter proxy details if you are connected to internet thorugh proxy"
    
    echo -n "Is your internet connection behind proxy? (y/n): "
    read getProxy
    if [ $getProxy == "y" -o $getProxy == "Y" ];then
        echo -n 'Proxy Hostname :'
        read proxyHostname

        echo -n 'Proxy Port :'
        read proxyPort

        echo -n username@$proxyHostname:$proxyPort :
        read username

        echo -n 'Password :'
        read -s passwd

        unset http_proxy
        unset https_proxy
        unset HTTP_PROXY
        unset HTTPS_PROXY
        unset ftp_proxy
        unset FTP_PROXY

        export http_proxy=http://$username:$passwd@$proxyHostname:$proxyPort
        export https_proxy=http://$username:$passwd@$proxyHostname:$proxyPort
        export https_proxy=http://$username:$passwd@$proxyHostname:$proxyPort
        export HTTP_PROXY=http://$username:$passwd@$proxyHostname:$proxyPort
        export HTTPS_PROXY=http://$username:$passwd@$proxyHostname:$proxyPort
        export ftp_proxy=http://$username:$passwd@$proxyHostname:$proxyPort
        export FTP_PROXY=http://$username:$passwd@$proxyHostname:$proxyPort

        echo "Install with proxy"

    elif [ $getProxy == "n" -o $getProxy == "N" ];then
        echo "Install without proxy"
    
    else
        echo "Please select the right option"
        exit 0    
    fi

    # Calling functions
    createConfigFile
    installDependency
    installKicad
    copyKicadLibrary
    installNghdl
    installSky130Pdk
    installIhpPdk
    createDesktopStartScript

    if [ $? -ne 0 ];then
        echo -e "\n\n\nERROR: Unable to install required packages. Please check your internet connection.\n\n"
        exit 0
    fi

    echo "-----------------eSim Installed Successfully-----------------"
    echo "Type \"esim\" in Terminal to launch it"
    echo "or double click on \"eSim\" icon placed on Desktop"


elif [ $option == "--uninstall" ];then
    echo -n "Are you sure? It will remove eSim completely including KiCad, Makerchip, NGHDL and SKY130 PDK along with their models and libraries (y/n):"
    read getConfirmation
    if [ $getConfirmation == "y" -o $getConfirmation == "Y" ];then
        echo "Removing eSim............................"
        sudo rm -rf $HOME/.esim $HOME/Desktop/esim.desktop /usr/bin/esim /usr/share/applications/esim.desktop
        echo "Removing KiCad..........................."
        sudo apt purge -y kicad kicad-footprints kicad-libraries kicad-symbols kicad-templates
        sudo rm -rf /usr/share/kicad
	sudo rm /etc/apt/sources.list.d/kicad*
        # Remove KiCad config for all known versions (6.0 and 8.0)
        rm -rf $HOME/.config/kicad/6.0
        rm -rf $HOME/.config/kicad/8.0

        echo "Removing Virtual env......................."
        sudo rm -r $config_dir/env

        echo "Removing SKY130 PDK......................"
        sudo rm -R /usr/share/local/sky130_fd_pr

        echo "Removing IHP Open PDK...................."
        if [ -f "ihp/install-ihp-openpdk.sh" ]; then
            cd ihp/
            chmod +x install-ihp-openpdk.sh
            ./install-ihp-openpdk.sh --uninstall
            cd ../
        fi

        echo "Removing NGHDL..........................."
        rm -rf library/modelParamXML/Nghdl/*
        rm -rf library/modelParamXML/Ngveri/*
        cd nghdl/
        if [ $? -eq 0 ];then
        	chmod +x install-nghdl.sh
    	    ./install-nghdl.sh --uninstall
    	    cd ../
    	    rm -rf nghdl
            if [ $? -eq 0 ];then
                echo -e "----------------eSim Uninstalled Successfully----------------"
            else
                echo -e "\nError while removing some files/directories in \"nghdl\". Please remove it manually"
            fi
        else
            echo -e "\nCannot find \"nghdl\" directory. Please remove it manually"
        fi
    elif [ $getConfirmation == "n" -o $getConfirmation == "N" ];then
        exit 0
    else 
        echo "Please select the right option."
        exit 0
    fi

else 
    echo "Please select the proper operation."
    echo "--install"
    echo "--uninstall"
fi
