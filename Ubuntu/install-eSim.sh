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
#                Sumanto Kar, Partha Singha Roy
#  ORGANIZATION: eSim Team, FOSSEE, IIT Bombay
#       CREATED: Wednesday 15 July 2015 15:26
#      REVISION: Tuesday 31 December 2024 17:28
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
    
    # Extract SKY130 PDK
    tar -xJf library/sky130_fd_pr.tar.xz

    # Remove any previous sky130-fd-pdr instance, if any
    sudo rm -rf /usr/share/local/sky130_fd_pr

    # Copy SKY130 library
    echo "Copying SKY130 PDK........................."

    sudo mkdir -p /usr/share/local/
    sudo mv sky130_fd_pr /usr/share/local/

    # Change ownership from root to the user
    sudo chown -R $USER:$USER /usr/share/local/sky130_fd_pr/

}


function installKicad
{
    echo "Installing KiCad..........................."

    # Detect Ubuntu version
    ubuntu_version=$(lsb_release -rs)

    # Define KiCad PPAs based on Ubuntu version
    if [[ "$ubuntu_version" == "24.04" ]]; then
        echo "Ubuntu 24.04 detected."
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
                exit 0
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
}


function copyKicadLibrary
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

    set +e      # Temporary disable exit on error
    trap "" ERR # Do not trap on error of any command
    
    # Remove extracted KiCad Library - not needed anymore
    rm -rf kicadLibrary

    set -e      # Re-enable exit on error
    trap error_exit ERR

    #Change ownership from Root to the User
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
