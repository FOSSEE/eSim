#!/bin/bash 
#===============================================================================
#
#          FILE: install.sh
# 
#         USAGE: ./install.sh --install 
#                 or
#                ./install.sh --uninstall
#                
#   DESCRIPTION: This is installation/uninstallation script for eSim
# 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Fahim Khan, (fahim.elex@gmail.com)
#  ORGANIZATION: FOSSEE at IIT Bombay.
#       CREATED: Wednesday 15 July 2015 15:26
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
    

}


function installNghdl
{
echo -n "Do you want to install nghdl? (y/n): "
read getNghdl

if [ $getNghdl == "y" -o $getNghdl == "Y" ];then
    echo "Downloading nghdl"
    wget https://github.com/FOSSEE/nghdl/archive/master.zip
    unzip master.zip
    mv nghdl-master nghdl
    rm master.zip

    echo "Installing nghdl"
    cd nghdl/
    ./install-nghdl.sh
    
    if [ $? -ne 0 ];then
        echo -e "\n\n\nNghdl ERROR: Error while installing nghdl\n\n"
        exit 0
    else
        ngspiceFlag=1
        cd ..
    fi
    #Creating empty eSim_kicad.lib in home directory
    if [ -f $HOME/eSim_kicad.lib ];then
        echo "eSim_kicad.lib is already available"
    else
        touch $HOME/eSim_kicad.lib
    fi

elif [ $getNghdl == "n" -o $getNghdl == "N" ];then
    echo "Proceeding without installing nghdl"
else
    echo "Please select the right option"
    exit 0
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
        echo "Kicad-4 is available in synaptic"
    fi
}

function installDependency
{

    echo "Installing Kicad............"
    sudo apt-get install -y kicad
    if [ $ngspiceFlag -ne 1 ];then
        echo "Installing ngspice.........."
        sudo apt-get install -y ngspice
    else
        echo "ngspice already installed......"
    fi
    echo "Installing PyQt4............"
    sudo apt-get install -y python-qt4
    echo "Installing Matplotlib......."
    sudo apt-get install -y python-matplotlib

}

function copyKicadLibrary
{

    #Copy Kicad library made for eSim
    sudo cp -r kicadSchematicLibrary/*.lib /usr/share/kicad/library/
    sudo cp -r kicadSchematicLibrary/*.dcm /usr/share/kicad/library/

    # Full path of 'kicad.pro file'[Verified for Ubuntu 12.04]                  
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
    echo "python Application.py" >> esim-start.sh
    
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


    
    #Copy desktop icon file to Desktop
    cp -vp esim.desktop $HOME/Desktop/eSim


    #Copying logo.png to .esim directory to access as icon
    cp images/logo.png $config_dir
}

####################################################################
#                   MAIN START FROM HERE                           #
####################################################################



###Checking if file is passsed as argument to script

if [ "$#" -eq 1 ];then
    option=$1
else
    echo "USAGE : "
    echo "./install.sh --install"
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
            createConfigFile
            installNghdl
            addKicadPPA
            installDependency
            copyKicadLibrary
            createDesktopStartScript

    elif [ $getProxy == "n" -o $getProxy == "N" ];then
            echo "Install without proxy"
            
            #Calling functions
            createConfigFile
            installNghdl
            addKicadPPA
            installDependency
            copyKicadLibrary
            createDesktopStartScript

            if [ $? -ne 0 ];then
                echo -e "\n\n\nFreeEDA ERROR: Unable to install required packages. Please check your internet connection.\n\n"
                exit 0
            fi
    
    else
            echo "Please select the right option"
            exit 0    
    fi


elif [ $option == "--uninstall" ];then
    echo -n "Are you sure ? As it will remove complete eSim including your subcircuit and model library packages(y/n):"
    read getConfirmation
    if [ $getConfirmation == "y" -o $getConfirmation == "Y" ];then
        sudo rm -rf $HOME/.esim $HOME/Desktop/eSim esim-start.sh esim.desktop /usr/bin/esim
        if [ $? -eq 0 ];then
            echo "Uninstalled successfully"
        else
            echo "Error while removing some file/directory.Please remove it manually"
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








