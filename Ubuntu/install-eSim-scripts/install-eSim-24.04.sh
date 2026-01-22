#!/bin/bash
set -e
set -E

# ================== GLOBAL PATH RESOLUTION ==================
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
UBUNTU_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
ESIM_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

config_dir="$HOME/.esim"
config_file="config.ini"
eSim_Home="$ESIM_ROOT"

echo "==========================================="
echo "eSim Root   = $ESIM_ROOT"
echo "Ubuntu Dir  = $UBUNTU_DIR"
echo "Script Dir  = $SCRIPT_DIR"
echo "==========================================="

# ============================================================

error_exit() {
    echo -e "\n\n❌ ERROR — installation aborted\n"
    exit 1
}
trap error_exit ERR

# ============================================================
createConfigFile() {
    mkdir -p "$config_dir"
    rm -f "$config_dir/$config_file"
    touch "$config_dir/$config_file"

    cat <<EOF >> "$config_dir/$config_file"
[eSim]
eSim_HOME = $eSim_Home
LICENSE = %(eSim_HOME)s/LICENSE
KicadLib = %(eSim_HOME)s/Ubuntu/library/kicadLibrary.tar.xz
IMAGES = %(eSim_HOME)s/Ubuntu/images
VERSION = %(eSim_HOME)s/VERSION
MODELICA_MAP_JSON = %(eSim_HOME)s/Ubuntu/library/ngspicetoModelica/Mapping.json
EOF
}

# ============================================================
installNghdl() {
    echo "Installing NGHDL..."

    cd "$UBUNTU_DIR"

    if [ ! -f nghdl.zip ]; then
        echo "ERROR: nghdl.zip missing in $UBUNTU_DIR"
        exit 1
    fi

    unzip -o nghdl.zip

    if [ ! -d nghdl ]; then
        echo "ERROR: nghdl folder missing after unzip"
        exit 1
    fi

    cd nghdl
    chmod +x install-nghdl.sh
    ./install-nghdl.sh --install
    cd "$ESIM_ROOT"
}

# ============================================================
copyKicadLibrary() {
    echo "Installing KiCad libraries..."

    LIB="$UBUNTU_DIR/library/kicadLibrary.tar.xz"
    cd "$UBUNTU_DIR"

    if [ ! -f "$LIB" ]; then
        echo "ERROR: $LIB not found"
        exit 1
    fi

    tar -xJf "$LIB"

    mkdir -p ~/.config/kicad/6.0
    cp kicadLibrary/template/sym-lib-table ~/.config/kicad/6.0/

    sudo cp -r kicadLibrary/eSim-symbols/* /usr/share/kicad/symbols/
    sudo chown -R $USER:$USER /usr/share/kicad/symbols/

    rm -rf kicadLibrary
    cd "$ESIM_ROOT"
}

# ============================================================
installKicad() {
    echo "Installing KiCad..."

    sudo rm -f /etc/apt/sources.list.d/kicad*
    sudo apt update

    UBUNTU_VER=$(lsb_release -rs)

    if [[ "$UBUNTU_VER" == 25.* ]]; then
        sudo apt install -y kicad kicad-footprints kicad-libraries kicad-symbols kicad-templates
        return
    fi

    if [[ "$UBUNTU_VER" == "24.04" ]]; then
        PPA="kicad/kicad-8.0-releases"
    else
        PPA="kicad/kicad-6.0-releases"
    fi

    sudo add-apt-repository -y "ppa:$PPA"
    sudo apt update
    sudo apt install -y kicad kicad-footprints kicad-libraries kicad-symbols kicad-templates
}

# ============================================================
installDependencies() {
    sudo apt update
    sudo apt install -y python3-virtualenv python3-pip python3-psutil python3-pyqt5 python3-matplotlib python3-setuptools xterm xz-utils

    virtualenv "$config_dir/env"
    source "$config_dir/env/bin/activate"

    pip install --upgrade pip
    pip install watchdog makerchip-app sandpiper-saas hdlparse matplotlib PyQt5 volare
    pip install https://github.com/hdl/pyhdlparser/tarball/master
}

# ============================================================
createDesktop() {
    cat <<EOF > esim-start.sh
#!/bin/bash
cd $ESIM_ROOT/src/frontEnd
source $config_dir/env/bin/activate
python3 Application.py
EOF

    chmod +x esim-start.sh
    sudo cp esim-start.sh /usr/bin/esim
    rm esim-start.sh
}

# ============================================================
# MAIN
# ============================================================

if [ "$1" != "--install" ]; then
    echo "Usage: ./install-eSim.sh --install"
    exit 1
fi

createConfigFile
installDependencies
installKicad
copyKicadLibrary
installNghdl
createDesktop

echo "==========================================="
echo "eSim installed successfully"
echo "Run:  esim"
echo "==========================================="

