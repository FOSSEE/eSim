#!/bin/bash 
#===============================================================================
#
#          FILE: install-eSim.sh
# 
#         USAGE: ./install-eSim.sh --install 
#                 or
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
#       CREATED: Wednesday 18 December 2019 16:14
#      REVISION:  ---
#===============================================================================

#All variables goes here
config_dir="$HOME/.esim"
config_file="config.ini"
eSim_Home=`pwd`
ngspiceFlag=0

##All Functions goes here

function createConfigFile
{
    #Creating config.ini file and adding configuration information
    #Check if config file is present
    if [ -d $config_dir ];then
        rm $config_dir/$config_file && touch $config_dir/$config_file
    else
        mkdir $config_dir && touch $config_dir/$config_file
    fi
    
    echo "[eSim]" >> $config_dir/$config_file
    echo "eSim_HOME = $eSim_Home" >> $config_dir/$config_file
    echo "LICENSE = %(eSim_HOME)s/LICENSE" >> $config_dir/$config_file
    echo "KicadLib = %(eSim_HOME)s/kicadSchematicLibrary" >> $config_dir/$config_file
    echo "IMAGES = %(eSim_HOME)s/images" >> $config_dir/$config_file
    echo "VERSION = %(eSim_HOME)s/VERSION" >> $config_dir/$config_file
    echo "MODELICA_MAP_JSON = %(eSim_HOME)s/src/ngspicetoModelica/Mapping.json" >> $config_dir/$config_file
}

function installNghdl
{

    echo "Installing nghdl............"
    unzip nghdl-master.zip
    mv nghdl-master nghdl
    cd nghdl/
    ./install-nghdl.sh --install
        
    if [ $? -ne 0 ];then
    	echo -e "\n\nNghdl ERROR: Error while installing nghdl\n\n"
        exit 0
    else
        ngspiceFlag=1
        cd ..
    fi
    
    #Creating empty eSim_Nghdl.lib in home directory
    if [ -f /usr/share/kicad/library/eSim_Nghdl.lib ];then
        echo "eSim_Nghdl.lib is already available"
    else
        touch /usr/share/kicad/library/eSim_Nghdl.lib
    fi

}

function addKicadPPA
{
    #sudo add-apt-repository ppa:js-reynaud/ppa-kicad
    kicadppa="reynaud/kicad-4"
    #Checking if ghdl ppa is already exist
    grep -h "^deb.*$kicadppa*" /etc/apt/sources.list.d/* > /dev/null 2>&1
    if [ $? -ne 0 ]
    then
        echo "Adding kicad-4 PPA to install latest ghdl version"
        sudo add-apt-repository --yes ppa:js-reynaud/kicad-4
        sudo apt-get update
    else
        echo "KiCad-4 is available in synaptic"
    fi
}

function installDependency
{

    echo "Installing KiCad............"
    sudo apt-get install -y kicad
    if [ $? -ne 0 ]; then
    	echo -e "\n\nKiCad couldn't be installed.\nKindly resolve above APT repository errors and try again."
        exit 1
    fi

    echo "Installing PyQt4............"
    sudo apt-get install -y python-qt4
    if [ $? -ne 0 ]; then
    	echo -e "\n\nPyQt-4 dependency couldn't be installed.\nKindly resolve above APT repository errors and try again."
        exit 1
    fi
    
    echo "Installing Matplotlib......."
    sudo apt-get install -y python-matplotlib
    if [ $? -ne 0 ]; then
    	echo -e "\n\nMatplotlib dependency couldn't be installed.\nKindly resolve above APT repository errors and try again."
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

    cp -r src/.OfflineFiles/fp-lib-table ~/.config/kicad/
    cp -r src/.OfflineFiles/fp-lib-table-online ~/.config/kicad/
    echo "fp-lib-table copied in the directory"
    sudo cp -r src/.OfflineFiles/TerminalBlock_Altech_AK300-2_P5.00mm.kicad_mod /usr/share/kicad/modules/Connectors_Terminal_Blocks.pretty/
    sudo cp -r src/.OfflineFiles/TO-220-3_Vertical.kicad_mod /usr/share/kicad/modules/TO_SOT_Packages_THT.pretty/
    #Copy KiCad library made for eSim
    sudo cp -r kicadSchematicLibrary/*.lib /usr/share/kicad/library/
    sudo cp -r kicadSchematicLibrary/*.dcm /usr/share/kicad/library/

    #Change ownership from Root to the User
    sudo chown -R $USER:$USER /usr/share/kicad/library/

    # Full path of 'kicad.pro file'
    KICAD_PRO="/usr/share/kicad/template/kicad.pro"
    KICAD_ORIGINAL="/usr/share/kicad/template/kicad.pro.original"

    if [ -f "$KICAD_ORIGINAL" ];then
        echo "kicad.pro.original file found....."
        sudo cp -rv kicadSchematicLibrary/kicad.pro ${KICAD_PRO}
    else 
        echo "Making copy of original file"
        sudo cp -rv ${KICAD_PRO}{,.original}                                             
        sudo cp -rv kicadSchematicLibrary/kicad.pro ${KICAD_PRO}
    fi

}

function createDesktopStartScript
{
    
    #Generating new esim-start.sh
    echo "#!/bin/bash" > esim-start.sh
    echo "cd $eSim_Home/src/frontEnd" >> esim-start.sh
    echo "python2 Application.py" >> esim-start.sh
    
    #Make it executable
    sudo chmod 755 esim-start.sh
    #Copy esim start script
    sudo cp -vp esim-start.sh /usr/bin/esim

    #Generating esim.desktop file
    echo "[Desktop Entry]" > esim.desktop
    getVersion=`tail -1 VERSION`
    echo "Version=$getVersion" >> esim.desktop
    echo "Name=eSim" >> esim.desktop
    echo "Comment=EDA Tools" >> esim.desktop
    echo "GenericName=eSim" >> esim.desktop
    echo "Keywords=eda-tools" >> esim.desktop
    echo "Exec=esim %u" >> esim.desktop
    echo "Terminal=false" >> esim.desktop
    echo "X-MultipleArgs=false" >> esim.desktop
    echo "Type=Application" >> esim.desktop
    getIcon="$config_dir/logo.png"
    echo "Icon=$getIcon" >> esim.desktop
    echo "Categories=Development;" >> esim.desktop
    echo "MimeType=text/html;text/xml;application/xhtml+xml;application/xml;application/rss+xml;application/rdf+xml;image/gif;image/jpeg;image/png;x-scheme-handler/http;x-scheme-handler/https;x-scheme-handler/ftp;x-scheme-handler/chrome;video/webm;application/x-xpinstall;" >> esim.desktop
    echo "StartupNotify=true" >> esim.desktop
    echo "Actions=NewWindow;NewPrivateWindow;" >> esim.desktop


    #Make esim.desktop file executable
    sudo chmod 755 esim.desktop
    #Copy desktop icon file to Desktop
    cp -vp esim.desktop $HOME/Desktop/
    #Copying logo.png to .esim directory to access as icon
    cp -vp images/logo.png $config_dir

}

####################################################################
#                   MAIN START FROM HERE                           #
####################################################################

###Checking if file is passsed as argument to script

if [ "$#" -eq 1 ];then
    option=$1
else
    echo "USAGE : "
    echo "./install-eSim.sh --install"
    echo "./install-eSim.sh --uninstall"
    exit 1;
fi

##Checking flags
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
            #Calling functions
            installNghdl
            createConfigFile
            addKicadPPA
            installDependency
            copyKicadLibrary
            createDesktopStartScript

    elif [ $getProxy == "n" -o $getProxy == "N" ];then
            echo "Install without proxy"
            
            #Calling functions
            installNghdl
            createConfigFile
            addKicadPPA
            installDependency
            copyKicadLibrary
            createDesktopStartScript

            if [ $? -ne 0 ];then
                echo -e "\n\n\nFreeEDA ERROR: Unable to install required packages. Please check your internet connection.\n\n"
                exit 0
            fi

            echo "-----------------eSim installed Successfully-----------------"
            echo "Type \"esim\" in Terminal to launch it"
            echo "or double click on \"eSim\" icon placed on Desktop"
    
    else
        echo "Please select the right option"
        exit 0    
    fi


elif [ $option == "--uninstall" ];then
    echo -n "Are you sure?  It will remove complete eSim including KiCad, Ngspice, NGHDL, your subcircuit and model library packages(y/n):"
    read getConfirmation
    if [ $getConfirmation == "y" -o $getConfirmation == "Y" ];then
        echo "Deleting Files................"
        sudo rm -rf $HOME/.esim $HOME/.config/kicad $HOME/Desktop/esim.desktop esim-start.sh esim.desktop /usr/bin/esim
        echo "Removing KiCad................"
        sudo apt-get remove -y kicad
        echo "Removing NGHDL................"
        rm -rf src/modelParamXML/Nghdl/*
        cd nghdl/
    	./install-nghdl.sh --uninstall
    	cd ../
    	rm -rf nghdl

        if [ $? -eq 0 ];then
            echo "Uninstalled successfully"
        else
            echo "Error while removing some file/directory. Please remove it manually"
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
