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
#  ORGANIZATION: eSim Team, FOSSEE, IIT Bombay
#       CREATED: Wednesday 15 July 2015 15:26
#      REVISION: Sunday 25 May 2025 17:40
#=============================================================================

# All variables goes here
script_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
eSim_Home=$(cd "$script_dir/../.." && pwd)
user_name="$USER"
user_home="$HOME"
if [ -n "$SUDO_USER" ] && [ -d "/home/$SUDO_USER" ]; then
    user_name="$SUDO_USER"
    user_home="/home/$SUDO_USER"
fi
config_dir="$user_home/.esim"
config_file="config.ini"
ngspiceFlag=0
kicad_config_version="6.0"
kicad_symbols_dir="/usr/share/kicad/symbols"

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

    # Do not trap on error of any command. Let NGHDL script handle its own errors.
    trap "" ERR

    local ubuntu_version=""
    if command -v lsb_release >/dev/null 2>&1; then
        ubuntu_version=$(lsb_release -rs 2>/dev/null || true)
    fi
    if [ -z "$ubuntu_version" ] && [ -r /etc/os-release ]; then
        ubuntu_version=$(. /etc/os-release; echo "${VERSION_ID:-}")
    fi

    if [[ "$ubuntu_version" == "25.04" ]]; then
        for nghdl_script in "install-nghdl.sh" "install-nghdl-scripts/install-nghdl-24.04.sh"; do
            if [ -f "$nghdl_script" ] && grep -q "libcanberra-gtk-module" "$nghdl_script"; then
                sed -i 's/libcanberra-gtk-module/libcanberra-gtk3-module/g' "$nghdl_script"
            fi
        done

        if [ -f "ghdl-4.1.0.tar.gz" ]; then
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
    fi

    if [[ "$ubuntu_version" == "25.04" ]] && [ -f "install-nghdl-scripts/install-nghdl-24.04.sh" ]; then
        chmod +x install-nghdl-scripts/install-nghdl-24.04.sh
        ./install-nghdl-scripts/install-nghdl-24.04.sh --install
    else
        ./install-nghdl.sh --install       # Install NGHDL
    fi
        
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


function installKicad
{
    echo "Installing KiCad..........................."

    # Detect Ubuntu version
    ubuntu_version=$(lsb_release -rs)

    if [[ "$ubuntu_version" == "25.04" ]]; then
        # Ubuntu 25.04 incompatibility: libgit2-1.8 doesn't exist
        # Both KiCad versions (8.0.8 from Ubuntu repo and 8.0.9 from PPA) require libgit2-1.8
        # Solution: Always use snap which bundles its own dependencies
        echo "Ubuntu 25.04 detected."
        kicad_config_version="9.0"
        
        # Check if KiCad already installed via snap
        if snap list kicad &>/dev/null 2>&1; then
            echo "KiCad is already installed via snap."
            return 0
        fi
        
        # Check if KiCad installed via APT (from previous attempts)
        if dpkg -s kicad &>/dev/null 2>&1; then
            installed_version=$(dpkg-query -W -f='${Version}' kicad | cut -d'.' -f1)
            if [[ "$installed_version" == "8" ]]; then
                echo "KiCad 8.0 is already installed via APT."
                return 0
            else
                echo "Older KiCad version ($installed_version) detected. Removing for snap installation..."
                sudo apt-get remove --purge -y kicad kicad-footprints kicad-libraries kicad-symbols kicad-templates 2>/dev/null || true
                sudo apt-get autoremove -y 2>/dev/null || true
            fi
        fi
        
        # Remove any stale KiCad PPA entries to avoid dependency issues
        if grep -Rqs "kicad" /etc/apt/sources.list /etc/apt/sources.list.d 2>/dev/null; then
            echo "Removing stale KiCad PPA entries..."
            sudo add-apt-repository -r -y "ppa:kicad/kicad-8.0-releases" 2>/dev/null || true
            sudo add-apt-repository -r -y "ppa:kicad/kicad-6.0-releases" 2>/dev/null || true
            sudo rm -f /etc/apt/sources.list.d/kicad-* 2>/dev/null || true
            sudo apt-get update || true
        fi
        
        # Install KiCad via snap
        echo "Installing KiCad 9.0.7 via snap (required for Ubuntu 25.04 due to libgit2 compatibility)..."
        if command -v snap &>/dev/null; then
            sudo snap install kicad --channel=stable
            echo "KiCad installation via snap completed successfully!"
            return 0
        else
            echo "Error: snap is not installed on this system."
            echo "Cannot install KiCad on Ubuntu 25.04 without snap (libgit2-1.8 package missing)."
            return 1
        fi
    else
        # For other Ubuntu versions, use PPA-based installation
        kicadppa="kicad/kicad-6.0-releases"
        
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
        
        # Check if the PPA is already added
        if ! grep -q "^deb .*${kicadppa}" /etc/apt/sources.list /etc/apt/sources.list.d/* 2>/dev/null; then
            echo "Adding KiCad PPA to local apt repository: $kicadppa"
            sudo add-apt-repository -y "ppa:$kicadppa"
            sudo apt-get update || true
        else
            echo "KiCad PPA is already present in sources."
        fi

        # Install KiCad packages via APT
        sudo apt-get install -y --no-install-recommends kicad kicad-footprints kicad-libraries kicad-symbols kicad-templates
        echo "KiCad installation completed successfully!"
    fi
}


function installDependency
{

    set +e      # Temporary disable exit on error
    trap "" ERR # Do not trap on error of any command

    # Update apt repository
    echo "Updating apt index files..................."
    if grep -Rqs "cdrom" /etc/apt/sources.list /etc/apt/sources.list.d 2>/dev/null; then
        sudo sed -i 's|^deb cdrom:|# deb cdrom:|g' /etc/apt/sources.list 2>/dev/null || true
        sudo sed -i 's|^deb .*file:///cdrom|# &|g' /etc/apt/sources.list 2>/dev/null || true
        sudo sed -i '/file:\/cdrom/ s/^/# /' /etc/apt/sources.list.d/*.sources 2>/dev/null || true
        sudo rm -f /etc/apt/sources.list.d/*cdrom*.list /etc/apt/sources.list.d/*cdrom*.sources 2>/dev/null || true
    fi
    sudo apt-get update
    
    set -e      # Re-enable exit on error
    trap error_exit ERR
    
    echo "Instaling virtualenv......................."
    sudo apt install python3-virtualenv
   
    echo "Creating virtual environment to isolate packages "
    sudo mkdir -p "$config_dir"
    sudo chown -R "$user_name":"$user_name" "$config_dir"
    if [ -d "$config_dir/env" ]; then
        echo "Existing virtual environment found. Recreating it to fix permissions."
        sudo rm -rf "$config_dir/env"
    fi
    sudo -u "$user_name" virtualenv "$config_dir/env"
    
    echo "Starting the virtual env..................."
    source $config_dir/env/bin/activate

    echo "Upgrading Pip.............................."
    pip install --upgrade pip

    echo "Installing Gtk Canberra modules..........................."
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

    echo "Installing volare"
    sudo apt-get install xz-utils -y xz-utils
    pip3 install volare
}


function copyKicadLibrary
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

    local kicad_config_dir="$user_home/.config/kicad/${kicad_config_version:-6.0}"

    if [ -d "$kicad_config_dir" ];then
        echo "kicad config folder already exists"
    else 
        echo ".config/kicad/${kicad_config_version:-6.0} does not exist"
        mkdir -p "$kicad_config_dir"
    fi

    # Copy symbol table for eSim custom symbols 
    cp "$kicad_lib_dir/template/sym-lib-table" "$kicad_config_dir/"
    echo "symbol table copied in the directory"

    # Copy KiCad symbols made for eSim
    sudo mkdir -p "$kicad_symbols_dir"
    sudo cp -r "$kicad_lib_dir/eSim-symbols/"* "$kicad_symbols_dir/"

    set +e      # Temporary disable exit on error
    trap "" ERR # Do not trap on error of any command
    
    # Remove extracted KiCad Library - not needed anymore
    if [ "$cleanup_tmp" = true ]; then
        rm -rf kicadLibrary
    fi

    set -e      # Re-enable exit on error
    trap error_exit ERR

    #Change ownership from Root to the User
    sudo chown -R $USER:$USER "$kicad_symbols_dir/"

}


function createDesktopStartScript
{    

    local user_home="$HOME"
    if [ -n "$SUDO_USER" ] && [ -d "/home/$SUDO_USER" ]; then
        user_home="/home/$SUDO_USER"
    fi

    local app_dir=""
    local app_entry=""
    local candidates=(
        "$eSim_Home/src/frontEnd"
        "$eSim_Home/src/FrontEnd"
        "$eSim_Home/frontEnd"
        "$eSim_Home"
    )

    for c in "${candidates[@]}"; do
        if [ -f "$c/Application.py" ]; then
            app_dir="$c"
            break
        fi
    done

    if [ -z "$app_dir" ]; then
        found=$(find "$eSim_Home" -maxdepth 4 -type f -name 'Application.py' -print -quit 2>/dev/null || true)
        if [ -n "$found" ]; then
            app_dir=$(dirname "$found")
        fi
    fi

    if [ -z "$app_dir" ]; then
        echo "Error: eSim application not found under ${eSim_Home}."
        echo "Please install eSim source or packaged executable before running."
        exit 1
    fi

    app_entry="$app_dir/Application.py"

    # Generating new esim-start.sh
    cat > esim-start.sh <<EOF
#!/bin/bash
app_dir="$app_dir"
app_entry="$app_entry"
cd "\$app_dir" || exit 1
source "${config_dir}/env/bin/activate"
python3 "\$app_entry"
EOF

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
    echo "Exec=bash -c 'cd \"$app_dir\" && source \"${config_dir}/env/bin/activate\" && python3 \"$app_entry\" %u'" >> esim.desktop
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
    mkdir -p "$user_home/Desktop"
    cp -vp esim.desktop "$user_home/Desktop/"

    set +e      # Temporary disable exit on error
    trap "" ERR # Do not trap on error of any command

    # Make esim.desktop file as trusted application (best-effort)
    if command -v gio >/dev/null 2>&1; then
        gio set "$user_home/Desktop/esim.desktop" "metadata::trusted" true 2>/dev/null || true
    fi
    # Set Permission and Execution bit
    chmod a+x "$user_home/Desktop/esim.desktop"

    # Remove local copy of esim.desktop file
    rm esim.desktop

    set -e      # Re-enable exit on error
    trap error_exit ERR

    # Copying logo.png to .esim directory to access as icon
    if [ -f images/logo.png ]; then
        cp -vp images/logo.png $config_dir
    else
        echo "Warning: images/logo.png not found. Skipping icon copy."
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

    found_app=$(find "$user_home" -type f -name "Application.py" -print -quit 2>/dev/null || true)
    if [ -n "$found_app" ]; then
        src_dir=""
        current_dir=$(dirname "$found_app")
        while [ "$current_dir" != "/" ]; do
            if [ "$(basename "$current_dir")" = "src" ]; then
                src_dir="$current_dir"
                break
            fi
            current_dir=$(dirname "$current_dir")
        done

        if [ -n "$src_dir" ]; then
            eSim_Home=$(dirname "$src_dir")
        else
            echo "Error: Application.py found at $found_app, but no src directory in its path."
            echo "Please ensure the eSim source is extracted correctly under your home directory."
            exit 1
        fi
    else
        echo "Error: Application.py not found under $user_home."
        echo "Please extract the eSim source within your home directory and retry."
        exit 1
    fi

    createConfigFile
    installDependency
    installKicad
    copyKicadLibrary
    installNghdl
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
        rm -rf "$HOME/.config/kicad/6.0" "$HOME/.config/kicad/9.0"

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
