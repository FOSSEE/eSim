# !/bin/bash 
# ===============================================================================
#          FILE: install-eSim.sh
# 
#         USAGE: ./install-eSim.sh --install 
#                            OR
#                ./install-eSim.sh --uninstall
#                
#   DESCRIPTION: This is installation/uninstallation script for eSim
#
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Fahim Khan, Rahul Paknikar, Saurabh Bansode
#  ORGANIZATION: FOSSEE at IIT Bombay.
#       CREATED: Friday 14 February 2020 16:14
#      REVISION:  ---
# ===============================================================================

# All variables goes here
config_dir="$HOME/.esim"
config_file="config.ini"
eSim_Home=`pwd`
ngspiceFlag=0

## All Functions goes here

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

    echo "Installing NGHDL......................."
    unzip nghdl-master.zip
    mv nghdl-master nghdl
    cd nghdl/
    ./install-nghdl.sh --install
        
    if [ $? -ne 0 ];then
    	echo -e "\n\nERROR: cannot install NGHDL\n\n"
        exit 0
    else
        ngspiceFlag=1
        cd ..
    fi

}


function addKicadPPA
{

    #sudo add-apt-repository ppa:js-reynaud/ppa-kicad
    kicadppa="reynaud/kicad-4"
    grep -h "^deb.*$kicadppa*" /etc/apt/sources.list.d/* > /dev/null 2>&1
    if [ $? -ne 0 ]
    then
        echo "Adding KiCad-4 PPA to local apt-repository"
        sudo add-apt-repository --yes ppa:js-reynaud/kicad-4
    else
        echo "KiCad-4 is available in synaptic"
    fi

}


function installDependency
{

	#Update apt repository
	echo "Updating apt index files..................."
    sudo apt-get update
    
    echo "Installing Xterm..........................."
    sudo apt-get install -y xterm
    if [ $? -ne 0 ]; then
        echo -e "\n\n\"Xterm\" dependency couldn't be installed.\nKindly resolve above errors and try again."
        exit 1
    fi

    echo "Installing KiCad..........................."
    sudo apt install -y --no-install-recommends kicad
    if [ $? -ne 0 ]; then
    	echo -e "\n\n\"KiCad\" dependency couldn't be installed.\nKindly resolve above errors and try again."
        exit 1
    fi

}


function copyKicadLibrary
{

    if [ -f ~/.config/kicad ];then
          echo "kicad folder already exists"
    else 
          echo ".config/kicad does not exist"
          mkdir ~/.config/kicad
    fi

    # Dump KiCad config path
    echo "$HOME/.config/kicad" > $eSim_Home/library/supportFiles/kicad_config_path.txt

    #Copy fp-lib-table for switching modes
    cp -r library/supportFiles/fp-lib-table ~/.config/kicad/
    cp -r library/supportFiles/fp-lib-table-online ~/.config/kicad/
    echo "fp-lib-table copied in the directory"

    #Extract custom KiCad Library
    tar -xJf library/kicadLibrary.tar.xz

    #Copy KiCad libraries
    echo "Copying KiCad libraries...................."

    sudo cp -r kicadLibrary/library /usr/share/kicad/
    sudo cp -r kicadLibrary/modules /usr/share/kicad/    
    sudo cp -r kicadLibrary/template/* /usr/share/kicad/template/

    #Copy KiCad library made for eSim
    sudo cp -r kicadLibrary/kicad_eSim-Library/* /usr/share/kicad/library/

    # Full path of 'kicad.pro file'
    KICAD_PRO="/usr/share/kicad/template/kicad.pro"
    KICAD_ORIGINAL="/usr/share/kicad/template/kicad.pro.original"

    if [ -f "$KICAD_ORIGINAL" ];then
        echo "kicad.pro.original file found....."
        sudo cp -rv kicadLibrary/template/kicad.pro ${KICAD_PRO}
    else 
        echo "Making copy of original file"
        sudo cp -rv ${KICAD_PRO}{,.original}                                             
        sudo cp -rv kicadLibrary/template/kicad.pro ${KICAD_PRO}
    fi

    #remove extracted KiCad Library - not needed anymore
    rm -rf kicadLibrary

    #Change ownership from Root to the User
    sudo chown -R $USER:$USER /usr/share/kicad/library/

}


function createDesktopStartScript
{    
	# Generating new esim-start.sh
    echo '#!/bin/bash' > esim-start.sh
    echo "cd $eSim_Home" >> esim-start.sh
    echo "./eSim" >> esim-start.sh
    
    # Make it executable
    sudo chmod 755 esim-start.sh
    # Copy esim start script
    sudo cp -vp esim-start.sh /usr/bin/esim
    # Remove local copy of esim start script
    rm esim-start.sh

	# Make eSim executable
    sudo chmod 755 eSim

    # Generating esim.desktop file
    echo "[Desktop Entry]" > esim.desktop
    getVersion=`tail -1 VERSION`
    echo "Version=$getVersion" >> esim.desktop
    echo "Name=eSim" >> esim.desktop
    echo "Comment=EDA Tools" >> esim.desktop
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
    echo "Actions=NewWindow;NewPrivateWindow;" >> esim.desktop

    # Make esim.desktop file executable
    sudo chmod 755 esim.desktop
    # Copy desktop icon file to Desktop
    cp -vp esim.desktop $HOME/Desktop/
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
            # Calling functions
            createConfigFile
            addKicadPPA
            installDependency
            copyKicadLibrary
            installNghdl
            createDesktopStartScript

    elif [ $getProxy == "n" -o $getProxy == "N" ];then
            echo "Install without proxy"
            
            # Calling functions
            createConfigFile
            addKicadPPA
            installDependency
            copyKicadLibrary
            installNghdl
            createDesktopStartScript

            if [ $? -ne 0 ];then
                echo -e "\n\n\nFreeEDA ERROR: Unable to install required packages. Please check your internet connection.\n\n"
                exit 0
            fi

            echo "-----------------eSim Installed Successfully-----------------"
            echo "Type \"esim\" in Terminal to launch it"
            echo "or double click on \"eSim\" icon placed on Desktop"
    
    else
        echo "Please select the right option"
        exit 0    
    fi


elif [ $option == "--uninstall" ];then
    echo -n "Are you sure? It will remove complete eSim including KiCad, Ngspice and NGHDL packages(y/n):"
    read getConfirmation
    if [ $getConfirmation == "y" -o $getConfirmation == "Y" ];then
        echo "Removing eSim............................"
        sudo rm -rf $HOME/.esim $HOME/Desktop/esim.desktop esim.desktop /usr/bin/esim
        echo "Removing KiCad..........................."
        sudo apt purge -y kicad
        sudo rm -rf /usr/share/kicad
        sudo rm -rf $HOME/.config/kicad
        rm -f $eSim_Home/library/supportFiles/kicad_config_path.txt 
        echo "Removing NGHDL..........................."
        rm -rf library/modelParamXML/Nghdl/*
        cd nghdl/
        if [ $? -eq 0 ];then
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
        echo "Please select the right option"
        exit 0
    fi

else 
    echo "Please select the proper operation."
    echo "--install"
    echo "--uninstall"
fi
