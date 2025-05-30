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
#                Sumanto Kar, Partha Singha Roy, Shiva Krishna Sangati,
#                Jayanth Tatineni, Anshul Verma
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


function installKicad {
    echo "Installing KiCad..."

    kicadppa="kicad/kicad-8.0-releases"
    findppa=$(grep -h -r "^deb.$kicadppa" /etc/apt/sources.list* > /dev/null 2>&1 || test $? = 1)
    
    if [ -z "$findppa" ]; then
        echo "Adding KiCad-8 PPA to local apt repository..."
        sudo add-apt-repository -y ppa:kicad/kicad-8.0-releases
        sudo apt update
    else
        echo "KiCad-8 PPA is already added."
    fi

    echo "Installing KiCad and necessary libraries..."
    sudo apt install -y --no-install-recommends kicad

    echo "KiCad installation completed successfully!"
}


function installDependency {
    set +e      # Temporary disable exit on error
    trap "" ERR # Do not trap on error of any command

    echo "Updating apt index files..................."
    sudo apt-get update
    
    set -e      # Re-enable exit on error
    trap error_exit ERR
    
    echo "Installing virtualenv......................."
    sudo apt install -y python3-virtualenv
   
    echo "Creating virtual environment to isolate packages "
    rm -rf $config_dir/env
    virtualenv $config_dir/env
    
    echo "Starting the virtual env..................."
    source $config_dir/env/bin/activate

    echo "Upgrading Pip.............................."
    pip install --upgrade pip
    
    echo "Reinstalling Matplotlib and PyQt5 to fix corrupted dependencies"
    pip install --force-reinstall --no-cache-dir PyQt5 PyQt5-sip matplotlib
    
    echo "Installing Xterm..........................."
    sudo apt-get install -y xterm
    
    echo "Installing Psutil.........................."
    sudo apt-get install -y python3-psutil
    
    echo "Installing PyQt5..........................."
    sudo apt-get install -y python3-pyqt5
    
    echo "Installing Matplotlib......................"
    sudo apt-get install -y python3-matplotlib
    
    echo "Installing Distutils......................."
    sudo apt-get install -y python3-distutils
    
    echo "Installing Pip3............................"
    sudo apt install -y python3-pip

    echo "Installing Watchdog........................"
    pip3 install watchdog

    echo "Installing Hdlparse........................"
    pip3 install --upgrade https://github.com/hdl/pyhdlparser/tarball/master

    echo "Installing Makerchip......................."
    pip3 install makerchip-app

    echo "Installing SandPiper Saas.................."
    pip3 install sandpiper-saas

    echo "Installing Hdlparse......................"
    pip3 install hdlparse

    echo "Installing matplotlib................"
    pip3 install matplotlib

    echo "Installing PyQt5............."
    pip3 install PyQt5  

    echo "Installing volare"
    sudo apt-get xz-utils
    pip3 install volare
}





function copyKicadLibrary {
    set -e  # Exit immediately on error
    trap 'echo "An error occurred! Exiting..."; exit 1' ERR

    echo "Extracting custom KiCad Library..."
    tar -xJf library/kicadLibrary.tar.xz -C library || { echo "Extraction failed!"; exit 1; }

    # Detect the latest installed KiCad version
    kicad_config_dir="$HOME/.config/kicad"
    latest_version=$(ls "$kicad_config_dir" | grep -E "^[0-9]+\.[0-9]+$" | sort -V | tail -n 1)

    if [ -z "$latest_version" ]; then
        latest_version="8.0"  # Default to the latest known version
        mkdir -p "$kicad_config_dir/$latest_version"
        echo "Created KiCad config directory: $kicad_config_dir/$latest_version"
    else
        echo "Using existing KiCad version: $latest_version"
    fi

    kicad_version_dir="$kicad_config_dir/$latest_version"

    # Copy the symbol table for eSim custom symbols
    echo "Copying symbol table..."
    cp library/kicadLibrary/template/sym-lib-table "$kicad_version_dir/"

    # Ensure KiCad symbols directory exists
    kicad_symbols_dir="/usr/share/kicad/symbols"
    if [ ! -d "$kicad_symbols_dir" ]; then
        echo "Creating KiCad symbols directory..."
        sudo mkdir -p "$kicad_symbols_dir"
    fi

    # Copy custom symbols using rsync for better reliability
    echo "Copying eSim custom symbols..."
    sudo rsync -av library/kicadLibrary/eSim-symbols/ "$kicad_symbols_dir/"

    # Cleanup: Remove extracted KiCad Library (not needed anymore)
    echo "Removing extracted KiCad library..."
    rm -rf library/kicadLibrary

    # Change ownership from root to the user only if needed
    if [ "$(stat -c "%U" "$kicad_symbols_dir")" != "$USER" ]; then
        echo "Changing ownership of KiCad symbols directory..."
        sudo chown -R "$USER:$USER" "$kicad_symbols_dir"
    fi

    echo "KiCad Library successfully copied and configured!"
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

        echo "Removing Virtual env......................."
        sudo rm -r $config_dir/env

        echo "Removing SKY130 PDK......................"
        sudo rm -R /usr/share/local/sky130_fd_pr

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
