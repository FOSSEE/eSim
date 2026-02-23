#!/bin/bash
#=====================================================================
#           FILE: install-ihp-openpdk.sh
#
#        USAGE:  ./install-ihp-openpdk.sh --install
#                ./install-ihp-openpdk.sh --uninstall
#
#   DESCRIPTION: Installation script for IHP Open PDK with OpenVAF
#                This script is designed to be called from install-eSim.sh
#                or can be run standalone after eSim/NGHDL is installed.
#
#       OPTIONS: --install, --uninstall
#  REQUIREMENTS: eSim/NGHDL must be installed first (for ngspice with OSDI)
#          BUGS: ---
#         NOTES: ---
#       MENTORS: Sumanto Kar, Varad Patil, Shanti Priya K, Aditya M
#       INTERNS: Akshay Rukade, Haripriyan R
#  ORGANIZATION: eSim Team, FOSSEE, IIT Bombay
#       CREATED: 2026-01-15
#      REVISION: 2026-01-15
#=====================================================================

### CONFIG ###
PDK_DIR="$HOME/ihp"
PDK_ROOT="$PDK_DIR/IHP-Open-PDK"
OPENVAF_DIR="$PDK_DIR/openvaf"
BASHRC="$HOME/.bashrc"
SPICEINIT="$HOME/.spiceinit"
NGHDL_SPINIT="$HOME/nghdl-simulator/install_dir/share/ngspice/scripts/spinit"

export PDK_DIR PDK_ROOT OPENVAF_DIR BASHRC SPICEINIT NGHDL_SPINIT

# Timestamp for backups
sysdate="$(date)"
timestamp=$(echo "$sysdate" | awk '{print $3"_"$2"_"$6"_"$4}')


### ERROR HANDLERS ###
error_exit() {
    echo -e "\n\n❌ Error! Kindly resolve above error(s) and try again."
    echo -e "\nAborting IHP PDK Installation...\n"
}

log() { 
    echo -e "\n👉 $1\n"
}


### HELPER FUNCTIONS ###

# Force reset directory (bulldozer mode)
force_reset_dir() {
    local dir="$1"
    if [[ -d "$dir" ]]; then
        echo "⚠️  Removing existing directory: $dir"
        rm -rf "$dir"
    fi
    mkdir -p "$dir"
}


# Check if ngspice has OSDI support
check_ngspice_osdi() {
    log "Checking if ngspice has OSDI support..."
    
    if ! command -v ngspice &> /dev/null; then
        echo "❌ ngspice not found. Please install eSim/NGHDL first."
        return 1
    fi
    
    # Check ngspice version and OSDI support
    if ngspice -v 2>&1 | grep -qi "osdi\|45"; then
        log "✅ ngspice with OSDI support detected"
        return 0
    else
        echo "⚠️  Warning: ngspice may not have OSDI support."
        echo "   IHP PDK requires ngspice compiled with --enable-osdi"
        read -p "   Continue anyway? (y/n): " choice
        if [[ "$choice" != "y" && "$choice" != "Y" ]]; then
            return 1
        fi
    fi
    return 0
}


### INSTALLATION FUNCTIONS ###

# Install IHP-specific dependencies
install_ihp_dependencies() {
    log "Installing IHP PDK dependencies..."
    
    sudo apt-get update -y
    sudo apt-get install -y \
        build-essential cmake libtool clang \
        python3 python3-dev python3-venv \
        ruby ruby-dev tree git wget \
        klayout
    
    # Install Python packages in eSim's virtualenv if available
    if [[ -d "$HOME/.esim/env" ]]; then
        log "Using existing eSim Python virtualenv"
        source "$HOME/.esim/env/bin/activate"
    else
        log "⚠️ eSim venv not found. Installing packages globally."
    fi
    
    pip install --upgrade pip
    pip install pandas h5py PDKMaster || true
    
    log "✅ IHP dependencies installed."
}


# Clone IHP Open PDK
install_openpdk() {
    log "Cloning IHP Open-PDK..."
    
    force_reset_dir "$PDK_DIR"
    cd "$PDK_DIR"
    
    git clone --recursive https://github.com/IHP-GmbH/IHP-Open-PDK.git "$PDK_ROOT"
    cd "$PDK_ROOT"
    git checkout dev
    
    # Add environment variables to .bashrc (if not already present)
    if ! grep -q "IHP Open PDK" "$BASHRC"; then
        echo '
# --- IHP Open PDK Environment Variables ---
export PDK_ROOT="'"$PDK_ROOT"'"
export PDK="ihp-sg13g2"
export KLAYOUT_PATH="$HOME/.klayout:$PDK_ROOT/$PDK/libs.tech/klayout"
export KLAYOUT_HOME="$HOME/.klayout"
# --- End IHP Open PDK ---
' >> "$BASHRC"
        log "Added IHP PDK environment variables to ~/.bashrc"
    fi
    
    log "✅ IHP Open PDK cloned successfully."
}


# Install OpenVAF (Verilog-A compiler)
install_openvaf() {
    log "Installing OpenVAF..."
    
    mkdir -p "$OPENVAF_DIR"
    cd "$OPENVAF_DIR"
    
    # Download OpenVAF binary
    wget -q https://openva.fra1.cdn.digitaloceanspaces.com/openvaf_23_5_0_linux_amd64.tar.gz
    tar -xzf openvaf_23_5_0_linux_amd64.tar.gz
    rm openvaf_23_5_0_linux_amd64.tar.gz
    
    OPENVAF_BIN="$OPENVAF_DIR/openvaf"
    
    if [[ ! -f "$OPENVAF_BIN" ]]; then
        echo "❌ OpenVAF binary not found after extraction"
        find "$OPENVAF_DIR" -type f
        exit 1
    fi
    
    # Create symlink (remove old one first)
    sudo rm -rf /usr/bin/openvaf
    sudo ln -s "$OPENVAF_BIN" /usr/bin/openvaf
    
    # Verify installation
    if openvaf --version &> /dev/null; then
        log "✅ OpenVAF installed successfully"
        log "   Symlink: /usr/bin/openvaf → $OPENVAF_BIN"
    else
        echo "❌ OpenVAF installation verification failed"
        exit 1
    fi
}


# Compile Verilog-A models to OSDI
compile_verilog_models() {
    log "Compiling Verilog-A models to OSDI format..."
    
    cd "$PDK_ROOT/ihp-sg13g2/libs.tech/verilog-a"
    
    # Make compile script executable
    chmod +x openvaf-compile-va.sh
    ./openvaf-compile-va.sh
    
    # Verify OSDI files were created
    OSDI_DIR="$PDK_ROOT/ihp-sg13g2/libs.tech/ngspice/osdi"
    if ls "$OSDI_DIR"/*.osdi &> /dev/null; then
        osdi_count=$(ls -1 "$OSDI_DIR"/*.osdi 2>/dev/null | wc -l)
        log "✅ Compiled $osdi_count OSDI models successfully"
    else
        echo "❌ OSDI compilation failed - no .osdi files found"
        exit 1
    fi
}


# Configure ngspice to load IHP OSDI models (adds to NGHDL spinit only)
configure_spiceinit() {
    log "Configuring ngspice to load IHP OSDI models..."
    
    # Add to NGHDL's spinit if it exists
    if [[ -f "$NGHDL_SPINIT" ]]; then
        # Enable OSDI if not already enabled
        if grep -q "^unset osdi_enabled" "$NGHDL_SPINIT" 2>/dev/null; then
            sed -i 's/^unset osdi_enabled/set osdi_enabled/' "$NGHDL_SPINIT"
            log "Enabled OSDI support in spinit"
        fi
        
        if ! grep -q "IHP-Open-PDK" "$NGHDL_SPINIT" 2>/dev/null; then
            # Add OSDI loading after the existing osdi block
            echo "" >> "$NGHDL_SPINIT"
            echo "* ========== IHP-Open-PDK OSDI Models ==========" >> "$NGHDL_SPINIT"
            echo "if \$?osdi_enabled" >> "$NGHDL_SPINIT"
            
            # Add each OSDI file from IHP
            for osdi_file in "$PDK_ROOT/ihp-sg13g2/libs.tech/ngspice/osdi"/*.osdi; do
                if [[ -f "$osdi_file" ]]; then
                    echo " osdi $osdi_file" >> "$NGHDL_SPINIT"
                fi
            done
            
            echo "end" >> "$NGHDL_SPINIT"
            echo "* ========== End IHP-Open-PDK ==========" >> "$NGHDL_SPINIT"
            log "Added IHP OSDI models to NGHDL spinit"
        else
            log "IHP models already configured in NGHDL spinit"
        fi
    else
        log "⚠️ NGHDL spinit not found at $NGHDL_SPINIT"
        log "   Please install NGHDL first, then re-run IHP installation"
    fi
    
    log "✅ Spiceinit configuration complete"
}


### UNINSTALL FUNCTION ###

uninstall_ihp() {
    log "🧹 Removing IHP Open PDK installation..."
    
    # Remove PDK directory
    if [[ -d "$PDK_DIR" ]]; then
        rm -rf "$PDK_DIR"
        echo "Removed $PDK_DIR"
    fi
    
    # Remove OpenVAF symlink
    if [[ -L "/usr/bin/openvaf" ]]; then
        sudo rm -f /usr/bin/openvaf
        echo "Removed /usr/bin/openvaf symlink"
    fi
    
    # Clean up .bashrc (remove IHP section)
    if grep -q "IHP Open PDK" "$BASHRC"; then
        sed -i '/# --- IHP Open PDK/,/# --- End IHP Open PDK ---/d' "$BASHRC"
        echo "Removed IHP entries from ~/.bashrc"
    fi
    
    # Clean up NGHDL spinit (remove IHP section)
    if [[ -f "$NGHDL_SPINIT" ]] && grep -q "IHP-Open-PDK" "$NGHDL_SPINIT"; then
        sed -i '/IHP-Open-PDK/,/End IHP-Open-PDK/d' "$NGHDL_SPINIT"
        echo "Removed IHP entries from NGHDL spinit"
    fi
    
    log "✅ IHP Open PDK uninstalled successfully"
}


#####################################################################
#                       MAIN ENTRY POINT                            #
#####################################################################

# Check command line arguments
if [[ "$#" -ne 1 ]]; then
    echo "USAGE:"
    echo "  ./install-ihp-openpdk.sh --install"
    echo "  ./install-ihp-openpdk.sh --uninstall"
    exit 1
fi

case "$1" in
    --install)
        set -e  # Exit on error
        set -E  # Inherit ERR trap
        trap error_exit ERR
        
        echo ""
        echo "╔══════════════════════════════════════════════════════════╗"
        echo "║         IHP Open PDK Installation for eSim               ║"
        echo "╚══════════════════════════════════════════════════════════╝"
        echo ""
        
        # Check prerequisites
        check_ngspice_osdi || exit 1
        
        # Run installation steps
        install_ihp_dependencies
        install_openpdk
        install_openvaf
        compile_verilog_models
        configure_spiceinit
        
        # Deactivate virtualenv if active
        [[ -n "$VIRTUAL_ENV" ]] && deactivate
        
        echo ""
        echo "╔══════════════════════════════════════════════════════════╗"
        echo "║     🎉 IHP Open PDK Installed Successfully! 🎉          ║"
        echo "╚══════════════════════════════════════════════════════════╝"
        echo ""
        echo "➡️  Reload your terminal: source ~/.bashrc"
        echo "➡️  Or restart your terminal"
        echo ""
        echo "To test IHP PDK in ngspice:"
        echo "  1. Open ngspice"
        echo "  2. Load an IHP testbench"
        echo ""
        ;;
        
    --uninstall)
        uninstall_ihp
        ;;
        
    *)
        echo "Invalid option: $1"
        echo "USAGE:"
        echo "  ./install-ihp-openpdk.sh --install"
        echo "  ./install-ihp-openpdk.sh --uninstall"
        exit 1
        ;;
esac

exit 0
