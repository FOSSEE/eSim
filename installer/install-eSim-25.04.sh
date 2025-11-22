#!/bin/bash

config_dir="$HOME/.esim"
config_file="config.ini"
eSim_Home=`pwd`
ngspiceFlag=0


###############################################
# ERROR
###############################################
error_exit() {
    echo -e "\n\nError! Kindly resolve above error(s) and try again."
    echo -e "\nAborting Installation...\n"
}


###############################################
# CREATE CONFIG FILE
###############################################
createConfigFile() {

    if [ -d $config_dir ]; then
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


###############################################
# INSTALL NGHDL
###############################################
installNghdl() {
    echo "Installing NGHDL..."
    unzip -o nghdl.zip
    cd nghdl/
    chmod +x install-nghdl.sh

    trap "" ERR
    ./install-nghdl.sh --install
    trap error_exit ERR

    ngspiceFlag=1
    cd ../
}


###############################################
# INSTALL SKY130
###############################################
installSky130Pdk() {
    echo "Installing SKY130 PDK..."

    tar -xJf library/sky130_fd_pr.tar.xz
    sudo rm -rf /usr/share/local/sky130_fd_pr

    echo "Copying SKY130 PDK..."
    sudo mkdir -p /usr/share/local/
    sudo mv sky130_fd_pr /usr/share/local/
    sudo chown -R $USER:$USER /usr/share/local/sky130_fd_pr/
}


###############################################
# FIXED KICAD INSTALL
###############################################
installKicad() {

    ubuntu_version=$(lsb_release -rs)

    echo "Installing KiCad..."

    # If skip flag from main script
    if [[ "$ESIM_SKIP_KICAD" == "1" ]]; then
        echo "KiCad installation skipped (handled by main installer)."
        return
    fi

    # Ubuntu 24.04 → KiCad 8 PPA
    if [[ "$ubuntu_version" == "24.04" ]]; then
        echo "Ubuntu 24.04 detected — installing KiCad 8 via PPA..."
        sudo add-apt-repository -y ppa:kicad/kicad-8.0-releases
        sudo apt update
        sudo apt install -y kicad kicad-footprints kicad-libraries \
             kicad-symbols kicad-templates
        return
    fi

    # Fallback for older versions
    echo "Installing KiCad from Ubuntu repo..."
    sudo apt update
    sudo apt install -y kicad kicad-footprints kicad-libraries \
         kicad-symbols kicad-templates
}


###############################################
# INSTALL DEPENDENCIES
###############################################
installDependency() {

    set +e
    trap "" ERR

    echo "Updating apt index..."
    sudo apt-get update
    
    set -e
    trap error_exit ERR
    
    sudo apt install -y python3-virtualenv
    virtualenv $config_dir/env
    
    source $config_dir/env/bin/activate

    pip install --upgrade pip
    
    sudo apt-get install -y xterm python3-psutil python3-pyqt5 python3-matplotlib python3-setuptools python3-pip

    pip3 install watchdog
    pip3 install --upgrade https://github.com/hdl/pyhdlparser/tarball/master
    pip3 install makerchip-app
    pip3 install sandpiper-saas
    pip3 install hdlparse
    pip3 install matplotlib
    pip3 install PyQt5
}


###############################################
# COPY KICAD LIB
###############################################
copyKicadLibrary() {

    if [[ "$ESIM_SKIP_KICAD" == "1" ]]; then
        echo "Skipping KiCad library copy."
        return
    fi

    tar -xJf library/kicadLibrary.tar.xz

    mkdir -p ~/.config/kicad/6.0

    cp kicadLibrary/template/sym-lib-table ~/.config/kicad/6.0/
    sudo cp -r kicadLibrary/eSim-symbols/* /usr/share/kicad/symbols/

    rm -rf kicadLibrary
    sudo chown -R $USER:$USER /usr/share/kicad/symbols/
}


###############################################
# CREATE DESKTOP ICON
###############################################
createDesktopStartScript() {

    echo '#!/bin/bash' > esim-start.sh
    echo "cd $eSim_Home/src/frontEnd" >> esim-start.sh
    echo "source $config_dir/env/bin/activate" >> esim-start.sh
    echo "python3 Application.py" >> esim-start.sh

    sudo chmod 755 esim-start.sh
    sudo cp -vp esim-start.sh /usr/bin/esim
    rm esim-start.sh

    echo "[Desktop Entry]" > esim.desktop
    echo "Version=1.0" >> esim.desktop
    echo "Name=eSim" >> esim.desktop
    echo "Exec=esim %u" >> esim.desktop
    echo "Terminal=true" >> esim.desktop
    echo "Type=Application" >> esim.desktop
    echo "Icon=$config_dir/logo.png" >> esim.desktop
    echo "Categories=Development;" >> esim.desktop

    sudo chmod 755 esim.desktop
    sudo cp -vp esim.desktop /usr/share/applications/
    cp -vp esim.desktop $HOME/Desktop/

    gio set $HOME/Desktop/esim.desktop "metadata::trusted" true
    chmod a+x $HOME/Desktop/esim.desktop
    rm esim.desktop

    cp -vp images/logo.png $config_dir
}


###############################################
# MAIN LOGIC
###############################################

if [[ $# -ne 1 ]]; then
    echo "USAGE:"
    echo "./install-eSim.sh --install"
    echo "./install-eSim.sh --uninstall"
    exit 1
fi

option=$1


# ----------- INSTALL MODE --------------
if [[ $option == "--install" ]]; then

    set -e
    set -E
    trap error_exit ERR

    echo -n "Is your internet connection behind proxy? (y/n): "
    read getProxy

    if [[ $getProxy == "y" || $getProxy == "Y" ]]; then
        echo "Proxy not recommended — skipping."
    fi

    createConfigFile
    installDependency
    installKicad
    copyKicadLibrary
    installNghdl
    installSky130Pdk
    createDesktopStartScript

    echo "----------------- eSim Installed Successfully -----------------"
fi

