#!/bin/bash

# Variables
nghdl="nghdl-simulator"
verilator="verilator-4.210"
config_dir="$HOME/.nghdl"
config_file="config.ini"
src_dir=$(pwd)

# Timestamp (for backups if needed)
sysdate="$(date)"
timestamp=$(echo "$sysdate" | awk '{print $3"_"$2"_"$6"_"$4 }')

# Exit handler
error_exit() {
    echo -e "\n\nError occurred! Kindly resolve the above issue(s) and try again."
    echo -e "\nAborting installation...\n"
    exit 1
}

# Install Verilator
installVerilator() {
    echo -e "\nInstalling $verilator..."

    if [ ! -f "$verilator.tar.xz" ]; then
        echo "Error: $verilator.tar.xz not found in current directory."
        error_exit
    fi

    tar -xJf "$verilator.tar.xz"
    echo "$verilator extracted successfully"

    cd "$verilator"
    chmod +x configure
    ./configure
    make -j$(nproc)
    sudo make install

    echo "Cleaning up unnecessary Verilator files..."
    rm -rf docs examples include test_regress bin
    ls -1 | grep -Ev 'config.status|configure.ac|Makefile.in|verilator.1|configure|Makefile|src|verilator.pc' | xargs rm -f
    cd "$src_dir"

    echo "Verilator installed successfully"
}

# Install NGHDL
installNGHDL() {
    echo -e "\nInstalling NGHDL..."

    if [ ! -f "$nghdl-source.tar.xz" ]; then
        echo "Error: $nghdl-source.tar.xz not found in current directory."
        error_exit
    fi

    tar -xJf "$nghdl-source.tar.xz" -C "$HOME"
    mv "$HOME/$nghdl-source" "$HOME/$nghdl"

    echo "NGHDL extracted to $HOME"

    cd "$HOME/$nghdl"
    mkdir -p install_dir release
    cd release

    chmod +x ../configure
    ../configure --enable-xspice --disable-debug \
        --prefix="$HOME/$nghdl/install_dir" \
        --exec-prefix="$HOME/$nghdl/install_dir"

    make -j$(nproc)
    make install

    sudo chmod 755 "$HOME/$nghdl/install_dir/bin/ngspice"

    echo "Removing any previously installed ngspice..."
    set +e
    trap "" ERR
    sudo apt-get purge -y ngspice
    set -e
    trap error_exit ERR

    echo "Creating symlink to installed Ngspice..."
    sudo rm -f /usr/bin/ngspice
    sudo ln -sf "$HOME/$nghdl/install_dir/bin/ngspice" /usr/bin/ngspice

    echo "NGHDL installed successfully"
}

# Create softlink for ngspice_ghdl.py
createSoftLink() {
    sudo chmod 755 "$src_dir/src/ngspice_ghdl.py"

    if [[ -L /usr/local/bin/nghdl ]]; then
        echo "Existing NGHDL symlink found. Removing..."
        sudo unlink /usr/local/bin/nghdl
    fi

    sudo ln -sf "$src_dir/src/ngspice_ghdl.py" /usr/local/bin/nghdl
    echo "Softlink created for NGHDL"
}

# Uninstall NGHDL and Verilator
uninstallAll() {
    echo -e "\nUninstalling NGHDL and Verilator...\n"

    echo "Removing Verilator..."
    sudo rm -f /usr/local/bin/verilator
    sudo rm -rf "$src_dir/$verilator"

    echo "Removing NGHDL files and binaries..."
    sudo rm -f /usr/bin/ngspice
    sudo rm -f /usr/local/bin/nghdl
    rm -rf "$HOME/$nghdl"

    echo "Removing NGHDL config files..."
    rm -rf "$config_dir"

    echo -e "\nUninstallation complete."
}

# Main control flow
if [ "$#" -ne 1 ]; then
    echo "Usage:"
    echo "  ./install-nghdl.sh --install      # To install NGHDL and Verilator"
    echo "  ./install-nghdl.sh --uninstall    # To uninstall NGHDL and Verilator"
    exit 1
fi

if [ "$1" == "--install" ]; then
    set -e
    set -E
    trap error_exit ERR

    installVerilator
    installNGHDL
    createSoftLink

elif [ "$1" == "--uninstall" ]; then
    uninstallAll

else
    echo "Invalid option. Use:"
    echo "  ./install-nghdl.sh --install"
    echo "  ./install-nghdl.sh --uninstall"
    exit 1
fi
