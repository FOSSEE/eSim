#!/bin/bash 
#===============================================================================
#
#          FILE: install-nghdl.sh
# 
#         USAGE: ./install-nghdl.sh 
# 
#   DESCRIPTION: It is installation script for ngspice and ghdl work (nghdl). 
# 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Fahim Khan , fahim.elex@gmail.com
#  ORGANIZATION: eSim, FOSSEE group at IIT Bombay
#       CREATED: Tuesday 02 December 2014 17:01
#      REVISION:  ---
#===============================================================================

ngspice="ngspice-nghdl"
ghdl="ghdl-0.36"
config_dir="$HOME/.nghdl"
config_file="config.ini"
src_dir=`pwd`

#Will be used to take backup of any file
sysdate="$(date)"
timestamp=`echo $sysdate|awk '{print $3"_"$2"_"$6"_"$4 }'`


#All functions goes here
function addghdlPPA
{
        ghdlppa="pgavin/ghdl"
        #Checking if ghdl ppa is already exist
        grep -h "^deb.*$ghdlppa*" /etc/apt/sources.list.d/* > /dev/null 2>&1
        if [ $? -ne 0 ]
        then
            echo "Adding ghdl PPA to install latest ghdl version"
            sudo add-apt-repository -y ppa:pgavin/ghdl
            sudo apt-get update
        else
            echo "ghdl is available in synaptic"
        fi
}

# make
# gnat
# llvm
# clang
# zlib1g-dev
function installDependency
{

    # echo "Updating indexes to install latest versions......"
    # sudo apt-get update

    # echo "Installing dependencies for ghdl-0.36 LLVM......."
    # echo "Installing make.................................."
    # sudo apt-get install -y make
    # echo "Installing gnat-5.................................."
    # sudo apt-get install -y gnat-5
    # echo "Installing llvm.................................."
    # sudo apt-get install -y llvm
    # echo "Installing clang.................................."
    # sudo apt-get install -y clang
    # echo "Installing zlib1g-dev.................................."
    # sudo apt-get install -y zlib1g-dev

    # if [ -d $HOME/$ghdl ]; then
    #     echo "$ghdl directory already exists at $HOME"
    #     echo "Leaving ghdl-0.36 LLVM installation"
    # else
    #     tar -xzvf $ghdl.tar.gz -C $HOME
    #     if [ "$?" == 0 ];then
    #         echo "ghdl-0.36 LLVM successfully extracted to $HOME......"
    #         echo "Changing directory to ghdl-0.36 LLVM installation..."
    #         cd $HOME/$ghdl
    #         echo "Configuring ghdl-0.36 build as per requirements....."
    #         #Other configure flags can be found at - https://github.com/ghdl/ghdl/blob/master/configure
    #         sudo ./configure --with-llvm-config
    #         echo "Building the install file for ghdl-0.36 LLVM....."
    #         sudo make
    #         echo "Installing ghdl-0.36 LLVM....."
    #         sudo make install
    #     else
    #         echo "Unable to extract ghdl-0.36 LLVM"
    #         echo "Exiting installation"
    #         exit 1
    #     fi
    # fi
    
    echo "Installing flex.................................."
    sudo apt-get install -y flex
    echo "Installing bison................................."
    sudo apt-get install -y bison

    # Specific dependency for nvidia graphic cards
    echo "Installing graphics dependency for ngspice souce build"
    echo "Installing libxaw7................................"
    sudo apt-get install libxaw7
    echo "Installing libxaw7-dev............................"
    sudo apt-get install libxaw7-dev
}


function installNgspice
{
    echo "Installing ngspice..................................."
    #Checking if ngspice-nghdl directory is already present in Home directory
    if [ -d $HOME/$ngspice ];then
        echo "$ngspice directory already exists at $HOME"
        echo "Leaving ngspice installation"
    else
        #Extracting Ngspice to Home Directory
        cd $src_dir
        tar -xzvf $ngspice.tar.gz -C $HOME 
        if [ "$?" == 0 ];then 
            echo "Ngspice extracted sucessfuly to $HOME "
            #change to ngspice-nghdl directory
            cd $HOME/$ngspice
            #Make local install directory
            mkdir -p install_dir
            #Make release directory for build
            mkdir -p release
            #Change to release directory
            cd release
            echo "Installing Ngspice....."
            echo "------------------------------------"  
            sleep 5
            ../configure --enable-xspice --disable-debug  --prefix=$HOME/$ngspice/install_dir/ --exec-prefix=$HOME/$ngspice/install_dir/   
            
            #dirty fix for adding patch to ngspice base code
            cp $src_dir/src/outitf.c $HOME/$ngspice/src/frontend
 
            make
            make install
            if [ "$?" == 0 ];then
                echo "Ngspice Installed sucessfully......"
                echo "Adding softlink for the installed ngspice......"

                sudo ln -s $HOME/$ngspice/install_dir/bin/ngspice /usr/bin/ngspice
                if [ "$?" == 0 ];then
                    echo "failed to add softlink"
                    echo "ngspice already installed at /usr/bin/ngspice..."
                    echo "Remove earlier installations and try again..."
                else
                    echo "Added softlink for ngspce"
                fi

            else 
                echo "There was some error in installing ngspice"
            fi


        else 
            echo "Unable to extract ngspice tar file"
            exit 1;
        fi

    fi
}

function createConfigFile
{
    #Creating config.ini file and adding configuration information
    #Check if config file is present
    if [ -d $config_dir ];then
        rm $config_dir/$config_file && touch $config_dir/$config_file
    else
        mkdir $config_dir && touch $config_dir/$config_file

    fi
    
    echo "[NGSPICE]" >> $config_dir/$config_file
    echo "NGSPICE_HOME = $HOME/$ngspice" >> $config_dir/$config_file
    echo "DIGITAL_MODEL = %(NGSPICE_HOME)s/src/xspice/icm/ghdl" >> $config_dir/$config_file
    echo "RELEASE = %(NGSPICE_HOME)s/release" >> $config_dir/$config_file
    echo "[SRC]" >> $config_dir/$config_file
    echo "SRC_HOME = $src_dir" >> $config_dir/$config_file
    echo "LICENSE = %(SRC_HOME)s/LICENSE" >> $config_dir/$config_file

}

function createSoftLink
{

    ## Creating softlink 
    cd /usr/local/bin
    if [[ -L nghdl ]];then
        echo "Symlink was already present"
        sudo unlink nghdl
        sudo ln -sf $src_dir/src/ngspice_ghdl.py nghdl

    else
        echo "Creating synmlink"
        sudo ln -sf $src_dir/src/ngspice_ghdl.py nghdl
    fi
    cd $pwd

}

#####################################################################
#       Script start from here                                     #
#####################################################################
echo "Enter proxy details if you are connected to internet thorugh proxy"

echo -n "Is your internet connection behind proxy? (y/n): "
read getProxy
if [ $getProxy == "y" -o $getProxy == "Y" ];then
        echo -n 'Proxy hostname :'
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
        export HTTP_PROXY=http://$username:$passwd@$proxyHostname:$proxyPort
        export HTTPS_PROXY=http://$username:$passwd@$proxyHostname:$proxyPort
        export ftp_proxy=http://$username:$passwd@$proxyHostname:$proxyPort
        export FTP_PROXY=http://$username:$passwd@$proxyHostname:$proxyPort

        echo "Install with proxy"
        #Calling functions
        addghdlPPA
        installDependency
        if [ $? -ne 0 ];then
            echo -e "\n\n\nERROR: Unable to install required packages. Please check your internet connection.\n\n"
            exit 0
        fi
        installNgspice
        createConfigFile
        createSoftLink

elif [ $getProxy == "n" -o $getProxy == "N" ];then
        echo "Install without proxy"

        #Calling functions
        addghdlPPA
        installDependency
        if [ $? -ne 0 ];then
            echo -e "\n\n\nERROR: Unable to install required packages. Please check your internet connection.\n\n"
            exit 0
        fi
        installNgspice
        createConfigFile
        createSoftLink


else
        echo "Please select the right option"
        exit 0

fi




