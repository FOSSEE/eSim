#!/bin/bash 
#=============================================================================
#          FILE: install-eSim-24.04.sh (also used for 25.04)
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
#
#  CHANGES (Ubuntu 25.04 compatibility fixes):
#  - BUG FIX #2: installDependency() — 'sudo apt-get xz-utils' was missing
#    the 'install' subcommand. Fixed to 'sudo apt-get install -y xz-utils'.
#  - BUG FIX #3: installDependency() — All pip3 install calls after virtualenv
#    activation were using system pip3, which fails on Ubuntu 25.04 with
#    PEP 668 "externally-managed-environment" error. Fixed to use 'pip'
#    (which points to venv pip after activation), with --no-build-isolation
#    where needed. Also added fallback for hdlparse via pip.
#  - BUG FIX #4: installKicad() — Version check hardcoded to "24.04" only.
#    On Ubuntu 25.04 this branched to the kicad-6.0-releases PPA, causing a
#    major version mismatch with the 8.x library paths used later. Fixed to
#    include 25.04 in the KiCad 8 branch.
#  - BUG FIX #5: copyKicadLibrary() — KiCad config path hardcoded to
#    ~/.config/kicad/6.0 but KiCad 8 uses ~/.config/kicad/8.0. Fixed to
#    detect the installed KiCad major version and use the correct path.
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


function installNghdl
{
    echo "Installing NGHDL..........................."
    unzip -o nghdl.zip
    cd nghdl/
    chmod +x install-nghdl.sh

    # Do not trap on error of any command. Let NGHDL script handle its own errors.
    trap "" ERR

    ./install-nghdl.sh --install       # Install NGHDL
        
    # Set trap again to error_exit function to exit on errors
    trap error_exit ERR

    ngspiceFlag=1
    cd ../
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

    # BUG FIX #4: The original code only checked for "24.04" and fell back to
    # kicad-6.0-releases PPA for any other version including 25.04. This caused
    # a major version mismatch since the rest of the script expects KiCad 8.x
    # paths (e.g. ~/.config/kicad/8.0). Fixed by including 25.04 in the KiCad 8
    # branch using a version comparison instead of exact string match.
    if [[ "$ubuntu_version" == "24.04" || "$ubuntu_version" == "25.04" || \
          "$(echo "$ubuntu_version >= 24.04" | bc)" -eq 1 ]]; then
        echo "Ubuntu $ubuntu_version detected. Using KiCad 8.0 releases."
        kicadppa="kicad/kicad-8.0-releases"

        # Check if KiCad is installed using dpkg-query for the main package
        if dpkg -s kicad &>/dev/null; then
            installed_version=$(dpkg-query -W -f='${Version}' kicad | cut -d'.' -f1)
            if [[ "$installed_version" != "8" ]]; then
                echo "A different version of KiCad ($installed_version) is installed."
                read -p "Do you want to remove it and install KiCad 8.0? (yes/no): " response

                if [[ "$response" =~ ^([Yy][Ee][Ss]|[Yy])$ ]]; then
                    echo "Removing KiCad $installed_version..."
                    sudo apt-get remove --purge -y kicad kicad-footprints kicad-libraries kicad-symbols kicad-templates
                    sudo apt-get autoremove -y
                else
                    echo "Exiting installation. KiCad $installed_version remains installed."
                    exit 1
                fi
            else
                echo "KiCad 8.0 is already installed."
                return 0
            fi
        fi
    else
        kicadppa="kicad/kicad-6.0-releases"
    fi

    # Check if the PPA is already added
    if ! grep -q "^deb .*${kicadppa}" /etc/apt/sources.list /etc/apt/sources.list.d/* 2>/dev/null; then
        echo "Adding KiCad PPA to local apt repository: $kicadppa"
        sudo add-apt-repository -y "ppa:$kicadppa"
        sudo apt-get update
    else
        echo "KiCad PPA is already present in sources."
    fi

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
    
    echo "Installing virtualenv......................"
    sudo apt install -y python3-virtualenv
   
    echo "Creating virtual environment to isolate packages"
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

    echo "Installing Setuptools......................"
    sudo apt-get install -y python3-setuptools

    # Install NgVeri Dependencies
    echo "Installing Pip3............................"
    sudo apt install -y python3-pip

    # BUG FIX #2: Original line was 'sudo apt-get xz-utils' — missing the
    # 'install' subcommand. This caused apt-get to print usage and silently
    # continue, leaving xz-utils uninstalled (required by volare/SKY130).
    echo "Installing xz-utils........................"
    sudo apt-get install -y xz-utils

    # BUG FIX #3: All pip3 calls below were using system pip3 instead of the
    # virtualenv's pip. On Ubuntu 25.04, PEP 668 enforces that system pip3
    # cannot install packages into the system Python. Since we already activated
    # the virtualenv above, we use 'pip' (venv pip) instead of 'pip3' (system).
    echo "Installing Watchdog........................"
    pip install watchdog

    echo "Installing Hdlparse........................"
    pip install --upgrade https://github.com/hdl/pyhdlparser/tarball/master || \
        pip install hdlparse  # fallback to PyPI version if GitHub fetch fails

    echo "Installing Makerchip......................."
    pip install makerchip-app

    echo "Installing SandPiper Saas.................."
    pip install sandpiper-saas

    echo "Installing Hdlparse (PyPI)...................."
    pip install hdlparse

    echo "Installing matplotlib......................"
    pip install matplotlib

    echo "Installing PyQt5..........................."
    pip install PyQt5

    echo "Installing volare.........................."
    pip install volare
}


function copyKicadLibrary
{
    # Extract custom KiCad Library
    tar -xJf library/kicadLibrary.tar.xz

    # BUG FIX #5: Original code hardcoded the KiCad config path to
    # ~/.config/kicad/6.0, but KiCad 8.x (installed by installKicad for
    # Ubuntu 24.04/25.04) uses ~/.config/kicad/8.0. Copying the sym-lib-table
    # to the wrong directory means eSim custom symbols are never loaded.
    # Fix: detect the installed KiCad major version and use the correct path.
    kicad_major_version=$(dpkg-query -W -f='${Version}' kicad 2>/dev/null | cut -d'.' -f1)
    kicad_config_path="$HOME/.config/kicad/${kicad_major_version}.0"

    echo "Detected KiCad major version: $kicad_major_version"
    echo "Using KiCad config path: $kicad_config_path"

    if [ -d "$kicad_config_path" ]; then
        echo "KiCad config folder already exists: $kicad_config_path"
    else
        echo "Creating KiCad config folder: $kicad_config_path"
        mkdir -p "$kicad_config_path"
    fi

    # Copy symbol table for eSim custom symbols 
    cp kicadLibrary/template/sym-lib-table "$kicad_config_path/"
    echo "Symbol table copied to $kicad_config_path"

    # Copy KiCad symbols made for eSim
    sudo cp -r kicadLibrary/eSim-symbols/* /usr/share/kicad/symbols/

    set +e      # Temporary disable exit on error
    trap "" ERR # Do not trap on error of any command
    
    # Remove extracted KiCad Library - not needed anymore
    rm -rf kicadLibrary

    set -e      # Re-enable exit on error
    trap error_exit ERR

    # Change ownership from Root to the User
    sudo chown -R $USER:$USER /usr/share/kicad/symbols/
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
    # Copy desktop icon file to Desktop
    cp -vp esim.desktop $HOME/Desktop/

    set +e      # Temporary disable exit on error
    trap "" ERR # Do not trap on error of any command

    # Make esim.desktop file as trusted application
    gio set $HOME/Desktop/esim.desktop "metadata::trusted" true
    # Set Permission and Execution bit
    chmod a+x $HOME/Desktop/esim.desktop

    # Remove local copy of esim.desktop file
    rm esim.desktop

    set -e      # Re-enable exit on error
    trap error_exit ERR

    # Copying logo.png to .esim directory to access as icon
    cp -vp images/logo.png $config_dir
}


####################################################################
#                   MAIN START FROM HERE                           #
####################################################################

### Checking if file is passed as argument to script

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

    echo "Enter proxy details if you are connected to internet through proxy"
    
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
