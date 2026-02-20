#!/bin/bash
################################################################################
# eSim AppImage Builder
################################################################################

set -euo pipefail

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
BLUE='\033[0;34m'; CYAN='\033[0;36m'; MAGENTA='\033[0;35m'
BOLD='\033[1m'; NC='\033[0m'

print_header() {
    clear
    echo -e "\n${BOLD}${CYAN}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BOLD}${CYAN}║${NC}  ${BOLD}eSim AppImage ${NC}    ${BOLD}${CYAN}║${NC}"
    echo -e "${BOLD}${CYAN}╚════════════════════════════════════════════════════════════╝${NC}\n"
}

log() { echo -e "${BLUE}[INFO]${NC} $1"; }
step() { echo -e "\n${MAGENTA}${BOLD}▶ STEP $1/10: $2${NC}"; }
progress() { echo -e "${CYAN}  ↳ $1${NC}"; }
ok() { echo -e "${GREEN}[✓]${NC} $1"; }
warn() { echo -e "${YELLOW}[⚠]${NC} $1"; }
die() { echo -e "\n${RED}[✗ ERROR]${NC} $1\n"; cleanup; exit 1; }

ESIM_VERSION="2.5"
ROOT="$(cd "$(dirname "$0")" && pwd)"
BUILD="$ROOT/build-eSim-AppImage"
APPDIR="$BUILD/eSim.AppDir"
DL="$BUILD/downloads"
SUDO_PID=""

# ═══ DISTRO DETECTION VARIABLES ═══
DISTRO=""
DISTRO_FAMILY=""
PKG_MANAGER=""
PYTHON_VERSION=""
SUDO="sudo" 

cleanup() {
    [ -n "$SUDO_PID" ] && kill -0 $SUDO_PID 2>/dev/null && kill $SUDO_PID 2>/dev/null || true
}
trap cleanup EXIT

setup_sudo() {
    # Skip sudo setup if running as root
    if [ "$(id -u)" -eq 0 ]; then
        SUDO_PID=""
        return 0
    fi
    sudo -v || die "This script requires sudo privileges"
    while true; do sudo -n true; sleep 60; done 2>/dev/null &
    SUDO_PID=$!
}

# ═══════════════════════════════════════════════════════════════════════════════
# MULTI-DISTRO DETECTION AND PACKAGE MANAGER SUPPORT
# Supports: Ubuntu, Debian, Fedora, Arch, openSUSE, and derivatives
# ═══════════════════════════════════════════════════════════════════════════════

detect_distro() {
    step 0 "Detecting Linux distribution"
    
    # Read OS information
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        DISTRO="$ID"
        DISTRO_VERSION="${VERSION_ID:-unknown}"
        DISTRO_NAME="${PRETTY_NAME:-$ID}"
    elif [ -f /etc/lsb-release ]; then
        . /etc/lsb-release
        DISTRO="$DISTRIB_ID"
        DISTRO_VERSION="$DISTRIB_RELEASE"
        DISTRO_NAME="$DISTRIB_DESCRIPTION"
    elif command -v lsb_release >/dev/null 2>&1; then
        DISTRO=$(lsb_release -si | tr '[:upper:]' '[:lower:]')
        DISTRO_VERSION=$(lsb_release -sr)
        DISTRO_NAME=$(lsb_release -sd)
    else
        die "Cannot detect Linux distribution. Please install lsb-release or ensure /etc/os-release exists."
    fi
    
    # Normalize distro name to lowercase
    DISTRO=$(echo "$DISTRO" | tr '[:upper:]' '[:lower:]')
    
    # Determine distro family and package manager
    case "$DISTRO" in
        ubuntu|linuxmint|pop|elementary|zorin|neon)
            DISTRO_FAMILY="debian"
            PKG_MANAGER="apt"
            ;;
        debian|raspbian|kali|parrot|mx)
            DISTRO_FAMILY="debian"
            PKG_MANAGER="apt"
            ;;
        fedora|nobara)
            DISTRO_FAMILY="fedora"
            PKG_MANAGER="dnf"
            ;;
        rhel|centos|rocky|almalinux|oracle)
            DISTRO_FAMILY="rhel"
            PKG_MANAGER="dnf"
            # Check if dnf exists, fall back to yum
            command -v dnf >/dev/null 2>&1 || PKG_MANAGER="yum"
            ;;
        arch|manjaro|endeavouros|garuda|artix|arcolinux)
            DISTRO_FAMILY="arch"
            PKG_MANAGER="pacman"
            ;;
        opensuse*|suse|sles)
            DISTRO_FAMILY="suse"
            PKG_MANAGER="zypper"
            ;;
        void)
            DISTRO_FAMILY="void"
            PKG_MANAGER="xbps"
            ;;
        alpine)
            DISTRO_FAMILY="alpine"
            PKG_MANAGER="apk"
            ;;
        *)
            warn "Unknown distribution: $DISTRO"
            # Try to detect package manager
            if command -v apt-get >/dev/null 2>&1; then
                DISTRO_FAMILY="debian"
                PKG_MANAGER="apt"
            elif command -v dnf >/dev/null 2>&1; then
                DISTRO_FAMILY="fedora"
                PKG_MANAGER="dnf"
            elif command -v pacman >/dev/null 2>&1; then
                DISTRO_FAMILY="arch"
                PKG_MANAGER="pacman"
            elif command -v zypper >/dev/null 2>&1; then
                DISTRO_FAMILY="suse"
                PKG_MANAGER="zypper"
            else
                die "Unsupported distribution: $DISTRO. Cannot find a supported package manager."
            fi
            ;;
    esac
    
    # Set SUDO command (empty if running as root)
    if [ "$(id -u)" -eq 0 ]; then
        SUDO=""
    else
        SUDO="sudo"
    fi
    
    ok "Detected: $DISTRO_NAME"
    progress "Distribution family: $DISTRO_FAMILY"
    progress "Package manager: $PKG_MANAGER"
}

# ═══ INSTALL PREREQUISITES (git, python, wget, etc.) ═══
install_prerequisites() {
    step 1 "Installing prerequisites"
    progress "Installing basic build tools and utilities..."
    
    case "$PKG_MANAGER" in
        apt)
            $SUDO apt-get update -qq 2>&1 | tail -2 || true
            $SUDO apt-get install -y -qq \
                wget curl git unzip tar xz-utils zstd \
                python3 python3-pip python3-venv \
                build-essential gcc g++ make \
                file patchelf binutils coreutils \
                2>&1 | tail -3 || die "Failed to install prerequisites with apt"
            ;;
        dnf|yum)
            $SUDO $PKG_MANAGER install -y \
                wget curl git unzip tar xz zstd \
                python3 python3-pip python3-virtualenv \
                gcc gcc-c++ make \
                file patchelf binutils coreutils \
                2>&1 | tail -3 || die "Failed to install prerequisites with $PKG_MANAGER"
            ;;
        pacman)
            # Sync package database
            $SUDO pacman -Sy --noconfirm 2>&1 | tail -2 || true
            $SUDO pacman -S --noconfirm --needed \
                wget curl git unzip tar xz zstd \
                python python-pip python-virtualenv \
                base-devel gcc make \
                file patchelf binutils coreutils \
                2>&1 | tail -3 || die "Failed to install prerequisites with pacman"
            ;;
        zypper)
            $SUDO zypper --non-interactive install \
                wget curl git unzip tar xz zstd \
                python3 python3-pip python3-virtualenv \
                gcc gcc-c++ make \
                file patchelf binutils coreutils \
                2>&1 | tail -3 || die "Failed to install prerequisites with zypper"
            ;;
        xbps)
            $SUDO xbps-install -Sy \
                wget curl git unzip tar xz zstd \
                python3 python3-pip python3-virtualenv \
                base-devel gcc make \
                file patchelf binutils coreutils \
                2>&1 | tail -3 || die "Failed to install prerequisites with xbps"
            ;;
        apk)
            $SUDO apk add --no-cache \
                wget curl git unzip tar xz zstd \
                python3 py3-pip py3-virtualenv \
                build-base gcc g++ make \
                file patchelf binutils coreutils \
                2>&1 | tail -3 || die "Failed to install prerequisites with apk"
            ;;
        *)
            die "Unsupported package manager: $PKG_MANAGER"
            ;;
    esac
    
    # Re-detect Python version after installation
    if command -v python3 >/dev/null 2>&1; then
        PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
        ok "Prerequisites installed (Python $PYTHON_VERSION)"
    else
        die "Python 3 installation failed"
    fi
}

check_system() {
    step 1.5 "System requirements check"
    
    # Check for required commands that should now be installed
    local missing_cmds=""
    for cmd in wget unzip python3 git; do
        command -v "$cmd" >/dev/null || missing_cmds="$missing_cmds $cmd"
    done
    
    if [ -n "$missing_cmds" ]; then
        warn "Missing commands:$missing_cmds - attempting to install..."
        install_prerequisites
    fi
    
    # Final verification
    for cmd in wget unzip python3 git; do
        command -v "$cmd" >/dev/null || die "Missing required command: $cmd"
    done
    
    ok "System check passed"
}

setup_directories() {
    step 2 "Setting up build directories"
    progress "Cleaning previous build (preserving downloads)..."
    # Only clean the AppDir, preserve downloads folder
    rm -rf "$APPDIR"
    mkdir -p "$APPDIR" "$DL"
    ok "Directories ready"
}

install_deps() {
    step 3 "Installing dependencies"
    warn "Installing packages (may take a few minutes)..."
    
    # ═══ SKIP SYSTEM KICAD - We bundle KiCad 6 from AppImage ═══
    progress "Installing eSim dependencies (KiCad 6 will be bundled from AppImage)..."
    
    case "$PKG_MANAGER" in
        apt)
            install_deps_apt
            ;;
        dnf|yum)
            install_deps_dnf
            ;;
        pacman)
            install_deps_pacman
            ;;
        zypper)
            install_deps_zypper
            ;;
        *)
            warn "Unsupported package manager: $PKG_MANAGER - trying apt-like commands..."
            install_deps_apt
            ;;
    esac
    
    ok "Dependencies installed (KiCad 6 will be bundled from AppImage)"
}

# ═══ APT-BASED DISTROS (Ubuntu, Debian, Mint, etc.) ═══
install_deps_apt() {
    # Suppress all interactive prompts
    export DEBIAN_FRONTEND=noninteractive
    export TZ=UTC
    
    $SUDO apt-get update -qq 2>&1 | tail -3 || true
    
    # Core dependencies - use DEBIAN_FRONTEND to prevent prompts
    DEBIAN_FRONTEND=noninteractive $SUDO apt-get install -y -qq \
        ngspice verilator xterm \
        python3-pyqt5 python3-pyqt5.qtsvg python3-pyqt5.qtwebengine \
        python3-numpy python3-scipy python3-lxml python3-matplotlib \
        python3-pip python3-venv git build-essential \
        libqt5gui5 libqt5widgets5 libqt5svg5 libqt5webenginewidgets5 \
        librsvg2-common libgdk-pixbuf2.0-0 gdk-pixbuf2.0-bin \
        adwaita-icon-theme hicolor-icon-theme file patchelf \
        libfuse2 libglu1-mesa mesa-utils \
        libboost-all-dev libglew2.2 libglm-dev \
        libcurl4 libcairo2 libfreetype6 fontconfig fonts-dejavu \
        liblapack-dev libblas-dev liblapack3 libblas3 \
        2>&1 | tail -3 || true
    
    # GHDL - Try ghdl-llvm first, fall back to ghdl-mcode
    # ghdl-llvm is required for NGHDL (linking with C code)
    if $SUDO apt-get install -y -qq ghdl-llvm 2>&1 | tail -1; then
        ok "GHDL-LLVM installed"
        # Install matching LLVM version (try different versions)
        for llvm_ver in 18 17 16 15 14; do
            if $SUDO apt-get install -y -qq libllvm${llvm_ver} 2>&1 | tail -1; then
                ok "LLVM $llvm_ver installed"
                break
            fi
        done
    elif $SUDO apt-get install -y -qq ghdl 2>&1 | tail -1; then
        warn "GHDL-LLVM not available, using GHDL (mcode). NGHDL may have limited functionality."
    else
        warn "GHDL not available in repositories. NGHDL will not work."
    fi
    
    # Ensure libLLVM symlink exists for ghdl-llvm (some systems name it differently)
    for llvm_ver in 18 17 16 15; do
        if [ -f "/usr/lib/x86_64-linux-gnu/libLLVM.so.${llvm_ver}" ] || [ -f "/usr/lib/x86_64-linux-gnu/libLLVM-${llvm_ver}.so" ]; then
            break
        fi
        if [ -f "/usr/lib/x86_64-linux-gnu/libLLVM.so.${llvm_ver}.1" ] && [ ! -f "/usr/lib/x86_64-linux-gnu/libLLVM-${llvm_ver}.so" ]; then
            $SUDO ln -sf "libLLVM.so.${llvm_ver}.1" "/usr/lib/x86_64-linux-gnu/libLLVM-${llvm_ver}.so" 2>/dev/null || true
            $SUDO ldconfig 2>/dev/null || true
            break
        fi
    done
    
    # Python libraries - detect version and install appropriate libpython
    local py_major_minor=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
    $SUDO apt-get install -y -qq "libpython${py_major_minor}" 2>&1 | tail -1 || \
    $SUDO apt-get install -y -qq libpython3-dev 2>&1 | tail -1 || true
    
    # wxWidgets - try different package names for compatibility
    $SUDO apt-get install -y -qq libwxgtk3.2-1t64 libwxbase3.2-1t64 2>&1 | tail -1 || \
    $SUDO apt-get install -y -qq libwxgtk3.2-1 libwxbase3.2-1 2>&1 | tail -1 || \
    $SUDO apt-get install -y -qq libwxgtk3.0-gtk3-0v5 2>&1 | tail -1 || true
    
    # OpenGL - try different package names
    $SUDO apt-get install -y -qq libgl1-mesa-glx 2>&1 | tail -1 || \
    $SUDO apt-get install -y -qq libgl1 2>&1 | tail -1 || true
    
    # Makerchip IDE dependencies (cross-distro compatible)
    progress "Installing Makerchip IDE dependencies..."
    $SUDO apt-get install -y -qq \
        perl python3-tk \
        automake autoconf libtool \
        nodejs npm \
        yosys iverilog \
        2>&1 | tail -1 || warn "Some optional Makerchip packages failed"
    
    # Verilator utilities and additional development tools
    $SUDO apt-get install -y -qq verilator 2>&1 | tail -1 || true
}

# ═══ DNF-BASED DISTROS (Fedora, RHEL, CentOS, Rocky, Alma) ═══
install_deps_dnf() {
    # Enable additional repos for Fedora/RHEL
    if [ "$DISTRO" = "fedora" ]; then
        $SUDO dnf install -y dnf-plugins-core 2>&1 | tail -1 || true
        $SUDO dnf install -y \
            https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm \
            2>&1 | tail -1 || true
    fi
    
    # Core dependencies
    $SUDO $PKG_MANAGER install -y \
        ngspice verilator xterm \
        python3-qt5 python3-qt5-webengine \
        python3-numpy python3-scipy python3-lxml python3-matplotlib \
        python3-pillow python3-watchdog \
        python3-pip python3-virtualenv git \
        gcc gcc-c++ make \
        qt5-qtbase-gui qt5-qtsvg qt5-qtwebengine \
        librsvg2 gdk-pixbuf2 gdk-pixbuf2-modules \
        adwaita-icon-theme hicolor-icon-theme file patchelf \
        fuse fuse-libs mesa-libGLU mesa-dri-drivers \
        boost-devel glew-devel glm-devel \
        libcurl cairo freetype fontconfig dejavu-fonts-common \
        lapack-devel blas-devel lapack blas \
        2>&1 | tail -3 || true
    
    # Verify and reinstall LAPACK/BLAS if needed (Fedora compatibility)
    progress "Verifying LAPACK/BLAS installation..."
    # Better Fedora package detection - check both ways
    if $SUDO $PKG_MANAGER list installed 2>/dev/null | grep -q "^lapack-devel" || \
       $SUDO rpm -q lapack-devel 2>/dev/null >/dev/null; then
        ok "LAPACK/BLAS development packages verified as installed"
    else
        warn "LAPACK/BLAS development packages not detected, attempting reinstall..."
        $SUDO $PKG_MANAGER install -y \
            lapack-devel blas-devel lapack blas \
            2>&1 | grep -v "Nothing to do" | tail -3 || warn "LAPACK/BLAS installation may have issues"
        # Verify again after install attempt
        if $SUDO rpm -q lapack-devel 2>/dev/null >/dev/null; then
            ok "LAPACK/BLAS packages confirmed installed"
        else
            warn "Could not confirm LAPACK/BLAS installation"
        fi
    fi
    
    # GHDL on Fedora - check if already installed first
    progress "Checking GHDL installation..."
    if command -v ghdl >/dev/null 2>&1; then
        GHDL_VERSION=$(ghdl --version 2>&1 | head -1 || echo "unknown")
        ok "GHDL already installed: $GHDL_VERSION"
    else
        progress "GHDL not found, attempting installation..."
        
        # Try to enable COPR for GHDL (may fail on very new Fedora versions)
        progress "Attempting COPR GHDL repository..."
        COPR_RESULT=$($SUDO $PKG_MANAGER copr enable -y "gsmeyer/ghdl" 2>&1 || echo "COPR_FAILED")
        
        # Check if COPR enable succeeded
        if echo "$COPR_RESULT" | grep -q "404\|not found\|COPR_FAILED"; then
            warn "COPR GHDL not available for this Fedora version. Trying fallback installation..."
            # Fallback: Try to install GHDL from standard repos
            if $SUDO $PKG_MANAGER install -y ghdl 2>&1 | grep -v "Nothing to do" | tail -2; then
                if command -v ghdl >/dev/null 2>&1; then
                    ok "GHDL installed from standard repositories"
                else
                    warn "GHDL not available in standard repos. Continuing without GHDL (NGHDL will be limited)."
                fi
            else
                warn "GHDL not available in standard repos. Continuing without GHDL (NGHDL will be limited)."
            fi
        else
            # COPR enabled successfully, try GHDL-LLVM installation
            if $SUDO $PKG_MANAGER install -y ghdl-llvm 2>&1 | grep -v "Nothing to do" | tail -2; then
                if command -v ghdl >/dev/null 2>&1; then
                    ok "GHDL-LLVM installed from COPR"
                fi
            elif $SUDO $PKG_MANAGER install -y ghdl 2>&1 | grep -v "Nothing to do" | tail -2; then
                if command -v ghdl >/dev/null 2>&1; then
                    ok "GHDL installed from COPR"
                fi
            else
                warn "GHDL installation from COPR failed. Continuing with fallback..."
                $SUDO $PKG_MANAGER install -y ghdl 2>&1 | grep -v "Nothing to do" || true
            fi
        fi
        
        # Final verification
        if command -v ghdl >/dev/null 2>&1; then
            GHDL_VERSION=$(ghdl --version 2>&1 | head -1 || echo "unknown")
            ok "GHDL confirmed available: $GHDL_VERSION"
        else
            warn "GHDL installation could not be verified"
        fi
    fi
    
    # LLVM runtime libraries for GHDL-LLVM
    for llvm_ver in 18 17 16 15 14 13; do
        if $SUDO $PKG_MANAGER install -y "llvm${llvm_ver}-libs" 2>&1 | tail -1; then
            ok "LLVM $llvm_ver runtime libs installed"
            break
        fi
    done
    
    # Verilator - required for Ngveri codemodel
    progress "Installing Verilator and C++ build tools..."
    if $SUDO $PKG_MANAGER install -y verilator verilator-devel 2>&1 | tail -1; then
        ok "Verilator installed with development files"
    else
        die "Verilator installation failed"
    fi
    
    # C++ standard library and development files (required for Verilator compilation)
    progress "Installing C++ standard library and headers..."
    for pkg in libstdc++-devel libstdc++ libstdc++-static gcc-c++ gcc-gfortran; do
        $SUDO $PKG_MANAGER install -y "$pkg" 2>&1 | tail -1 || warn "Could not install $pkg"
    done
    
    # wxWidgets
    $SUDO $PKG_MANAGER install -y wxGTK3-devel wxBase3 2>&1 | tail -1 || true
    
    # libfuse2 compatibility (Fedora uses fuse3 by default)
    $SUDO $PKG_MANAGER install -y fuse 2>&1 | tail -1 || true
    
    # Makerchip dependencies (for HDL simulation)
    progress "Installing Makerchip dependencies..."
    $SUDO $PKG_MANAGER install -y perl 2>&1 | tail -1 || true
    
    # Additional C++ development tools for Verilator code generation
    $SUDO $PKG_MANAGER install -y gcc-c++ automake autoconf libtool 2>&1 | tail -1 || true
    
    # Node.js for Makerchip IDE support (optional but recommended)
    $SUDO $PKG_MANAGER install -y nodejs npm 2>&1 | tail -1 || true
    
    # Additional Makerchip IDE tools (Yosys, Iverilog, etc.)
    progress "Installing additional Makerchip IDE synthesis tools..."
    for tool in yosys iverilog gtkwave; do
        $SUDO $PKG_MANAGER install -y "$tool" 2>&1 | tail -1 || warn "Could not install $tool"
    done
    
    # Python3-tk for Makerchip GUI components
    $SUDO $PKG_MANAGER install -y python3-tkinter 2>&1 | tail -1 || true
}

# ═══ PACMAN-BASED DISTROS (Arch, Manjaro, EndeavourOS, etc.) ═══
install_deps_pacman() {
    # Update package database
    $SUDO pacman -Sy --noconfirm 2>&1 | tail -2 || true
    
    # Core build tools and Python packages (must succeed)
    progress "Installing core build tools and Python packages..."
    $SUDO pacman -S --noconfirm --needed \
        python-numpy python-scipy python-lxml python-matplotlib \
        python-pip python-virtualenv git \
        base-devel gcc make \
        curl cairo freetype2 fontconfig ttf-dejavu \
        lapack blas \
        2>&1 | tail -3 || die "Failed to install core packages with pacman"
    
    # Simulation tools
    progress "Installing simulation tools..."
    $SUDO pacman -S --noconfirm --needed \
        ngspice verilator xterm \
        2>&1 | tail -3 || warn "Some simulation tools failed to install"
    
    # PyQt5 - python-pyqt5-webengine and qt5-webengine were dropped from Arch (only Qt6 exists)
    # Do NOT attempt to install them — pacman will print noisy "error: target not found" messages
    progress "Installing PyQt5..."
    $SUDO pacman -S --noconfirm --needed python-pyqt5 2>&1 | tail -1 || \
        warn "python-pyqt5 installation failed"
    
    # Qt5 libraries (webengine is not available on Arch, skip it)
    progress "Installing Qt5 libraries..."
    $SUDO pacman -S --noconfirm --needed qt5-base qt5-svg 2>&1 | tail -1 || true
    
    # Remaining optional libraries
    progress "Installing optional libraries..."
    $SUDO pacman -S --noconfirm --needed \
        librsvg gdk-pixbuf2 \
        adwaita-icon-theme hicolor-icon-theme file patchelf \
        fuse2 glu mesa mesa-utils \
        boost glew glm \
        2>&1 | tail -3 || true
    
    # GHDL - Try AUR first, then fall back to official GitHub binary release
    if command -v ghdl >/dev/null 2>&1; then
        ok "GHDL already installed: $(ghdl --version 2>&1 | head -1)"
    elif command -v yay >/dev/null 2>&1; then
        progress "Installing GHDL from AUR via yay..."
        yay -S --noconfirm ghdl-llvm-git 2>&1 | tail -3 || \
        yay -S --noconfirm ghdl-mcode-git 2>&1 | tail -3 || \
        warn "GHDL AUR installation failed"
    elif command -v paru >/dev/null 2>&1; then
        progress "Installing GHDL from AUR via paru..."
        paru -S --noconfirm ghdl-llvm-git 2>&1 | tail -3 || \
        paru -S --noconfirm ghdl-mcode-git 2>&1 | tail -3 || \
        warn "GHDL AUR installation failed"
    else
        # No AUR helper available — download official pre-built GHDL binary
        progress "Downloading GHDL v5.1.1 (mcode) from GitHub releases..."
        GHDL_VER="5.1.1"
        GHDL_URL="https://github.com/ghdl/ghdl/releases/download/v${GHDL_VER}/ghdl-mcode-${GHDL_VER}-ubuntu24.04-x86_64.tar.gz"
        GHDL_TMP="$BUILD/ghdl_binary"
        mkdir -p "$GHDL_TMP"
        if wget -q "$GHDL_URL" -O "$GHDL_TMP/ghdl.tar.gz" 2>/dev/null; then
            tar -xzf "$GHDL_TMP/ghdl.tar.gz" -C "$GHDL_TMP" 2>/dev/null
            GHDL_DIR=$(find "$GHDL_TMP" -maxdepth 1 -type d -name "ghdl-*" | head -1)
            if [ -n "$GHDL_DIR" ] && [ -f "$GHDL_DIR/bin/ghdl" ]; then
                # Install GHDL to /usr/local
                $SUDO cp -f "$GHDL_DIR/bin/ghdl" /usr/local/bin/
                $SUDO cp -f "$GHDL_DIR/bin/ghwdump" /usr/local/bin/ 2>/dev/null || true
                $SUDO mkdir -p /usr/local/lib /usr/local/include/ghdl
                $SUDO cp -f "$GHDL_DIR/lib/"libghdl*.so* /usr/local/lib/ 2>/dev/null || true
                $SUDO cp -f "$GHDL_DIR/lib/"libghdl*.a /usr/local/lib/ 2>/dev/null || true
                $SUDO cp -f "$GHDL_DIR/lib/"libghw*.so* /usr/local/lib/ 2>/dev/null || true
                $SUDO cp -rf "$GHDL_DIR/lib/ghdl" /usr/local/lib/ 2>/dev/null || true
                $SUDO cp -f "$GHDL_DIR/include/ghdl/"*.h /usr/local/include/ghdl/ 2>/dev/null || true
                $SUDO ldconfig 2>/dev/null || true
                if command -v ghdl >/dev/null 2>&1; then
                    ok "GHDL installed from GitHub: $(ghdl --version 2>&1 | head -1)"
                else
                    warn "GHDL binary copied but not found in PATH"
                fi
            else
                warn "GHDL download extracted but binary not found"
            fi
            rm -rf "$GHDL_TMP"
        else
            warn "Failed to download GHDL from GitHub - NGHDL will not work"
            rm -rf "$GHDL_TMP"
        fi
    fi
    
    # LLVM (usually pulled as dependency)
    $SUDO pacman -S --noconfirm --needed llvm llvm-libs 2>&1 | tail -1 || true
    
    # wxWidgets
    $SUDO pacman -S --noconfirm --needed wxwidgets-gtk3 2>&1 | tail -1 || true
    
    # Makerchip IDE dependencies (Arch-specific)
    # Note: Arch provides tkinter via the 'tk' package, not 'python-tk'
    progress "Installing Makerchip IDE dependencies for Arch-based systems..."
    $SUDO pacman -S --noconfirm --needed \
        perl tk \
        automake autoconf libtool \
        2>&1 | tail -3 || warn "Some Makerchip build tools failed"
    $SUDO pacman -S --noconfirm --needed \
        nodejs npm \
        2>&1 | tail -3 || warn "Node.js/npm not available"
    $SUDO pacman -S --noconfirm --needed \
        yosys iverilog gtkwave \
        2>&1 | tail -3 || warn "Some optional HDL tools failed to install"
}

# ═══ ZYPPER-BASED DISTROS (openSUSE, SLES) ═══
install_deps_zypper() {
    # Core dependencies
    $SUDO zypper --non-interactive install \
        ngspice verilator xterm \
        python3-qt5 python3-qt5-webengine \
        python3-numpy python3-scipy python3-lxml python3-matplotlib \
        python3-pip python3-virtualenv git \
        gcc gcc-c++ make \
        libqt5-qtbase libqt5-qtsvg libqt5-qtwebengine \
        librsvg2 gdk-pixbuf gdk-pixbuf-loader-rsvg \
        adwaita-icon-theme hicolor-icon-theme file patchelf \
        fuse libfuse2 Mesa-libGL1 Mesa-libGLU1 \
        boost-devel libglew2_1 glm-devel \
        libcurl4 libcairo2 libfreetype6 fontconfig dejavu-fonts \
        lapack-devel blas-devel liblapack3 libblas3 \
        2>&1 | tail -3 || true
    
    # GHDL may need to be installed from external repo
    if ! $SUDO zypper --non-interactive install ghdl 2>&1 | tail -1; then
        warn "GHDL not in default repos. Manual installation may be required."
    fi
    
    # wxWidgets
    $SUDO zypper --non-interactive install wxWidgets-3_2-devel libwx_baseu-suse-nostl3_2 2>&1 | tail -1 || true
    
    # Makerchip IDE dependencies (openSUSE-specific)
    progress "Installing Makerchip IDE dependencies for openSUSE..."
    $SUDO zypper --non-interactive install \
        perl python3-tk \
        automake autoconf libtool \
        nodejs npm \
        yosys iverilog gtkwave \
        2>&1 | tail -3 || warn "Some optional Makerchip packages failed"
}


download_tools() {
    step 4 "Downloading tools and bundling NgSpice/NGHDL"
    cd "$DL"
    if [ ! -f appimagetool-x86_64.AppImage ]; then
        progress "Downloading appimagetool..."
        wget -q --show-progress \
            https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage \
            -O appimagetool-x86_64.AppImage 2>&1 | tail -2
        chmod +x appimagetool-x86_64.AppImage
    fi
    if [ ! -f eSim.zip ]; then
        progress "Downloading eSim ${ESIM_VERSION}..."
        wget -q --show-progress \
            https://static.fossee.in/esim/installation-files/eSim-${ESIM_VERSION}.zip \
            -O eSim.zip 2>&1 | tail -2
    fi
    
    # ═══ DOWNLOAD KICAD 6 APPIMAGE ═══
    if [ ! -f kicad6.AppImage ] || [ ! -s kicad6.AppImage ]; then
        rm -f kicad6.AppImage 2>/dev/null || true
        progress "Downloading KiCad 6.0.11 AppImage (for eSim compatibility)..."
        
        # Primary: SourceForge KiCad-AppImage project - v6 folder
        wget --progress=bar:force \
            "https://sourceforge.net/projects/kicad-appimage/files/v6/KiCad-6.0.11.glibc2.29-x86_64.AppImage/download" \
            -O kicad6.AppImage 2>&1 || {
            
            # Fallback 1: Direct SourceForge CDN - v6 folder
            progress "Primary download failed, trying alternate URL..."
            wget --progress=bar:force \
                "https://master.dl.sourceforge.net/project/kicad-appimage/v6/KiCad-6.0.11.glibc2.29-x86_64.AppImage" \
                -O kicad6.AppImage 2>&1 || {
                
                # Fallback 2: Alternative mirror
                progress "Trying another mirror..."
                wget --progress=bar:force \
                    "https://cfhcable.dl.sourceforge.net/project/kicad-appimage/v6/KiCad-6.0.11.glibc2.29-x86_64.AppImage" \
                    -O kicad6.AppImage 2>&1 || warn "KiCad 6 AppImage download failed!"
            }
        }
        
        # Verify download was successful (file should be > 100MB)
        if [ -f kicad6.AppImage ] && [ $(stat -c%s kicad6.AppImage 2>/dev/null || echo 0) -gt 100000000 ]; then
            chmod +x kicad6.AppImage
            ok "KiCad 6.0.11 AppImage downloaded successfully ($(du -h kicad6.AppImage | cut -f1))"
        else
            rm -f kicad6.AppImage 2>/dev/null || true
            die "KiCad 6 AppImage download failed or file is corrupted. Cannot proceed."
        fi
    else
        ok "KiCad 6.0.11 AppImage already downloaded"
    fi
    
    # ═══ BUILD NGSPICE-35 FROM OFFICIAL SOURCE ═══
    progress "Building NgSpice-35 from official source (this may take a few minutes)..."
    mkdir -p "$APPDIR/usr/bin" "$APPDIR/usr/lib/ngspice" "$APPDIR/usr/share/ngspice"
    
    local NGSPICE_BUILD="$BUILD/ngspice-build"
    local NGSPICE_INSTALL="$BUILD/ngspice-install"
    local NGSPICE_VERSION="35"
    local NGSPICE_TAR="ngspice-${NGSPICE_VERSION}.tar.gz"
    local NGSPICE_URL="https://sourceforge.net/projects/ngspice/files/ng-spice-rework/old-releases/${NGSPICE_VERSION}/${NGSPICE_TAR}/download"
    
    # Check if already built with correct version
    if [ -x "$NGSPICE_INSTALL/bin/ngspice" ]; then
        local built_ver=$("$NGSPICE_INSTALL/bin/ngspice" --version 2>&1 | grep -oE "ngspice-[0-9]+" | head -1 || echo "")
        if [ "$built_ver" = "ngspice-${NGSPICE_VERSION}" ]; then
            progress "NgSpice-${NGSPICE_VERSION} already built, reusing cached build..."
        else
            rm -rf "$NGSPICE_BUILD" "$NGSPICE_INSTALL"
        fi
    fi
    
    if [ ! -x "$NGSPICE_INSTALL/bin/ngspice" ]; then
        progress "Installing ngspice build dependencies..."
        
        # Multi-distro support for ngspice build dependencies
        case "$PKG_MANAGER" in
            apt)
                $SUDO apt-get install -y -qq \
                    autoconf automake libtool bison flex libreadline-dev \
                    libxaw7-dev libx11-dev libxext-dev libxmu-dev libxpm-dev libxt-dev \
                    libncurses-dev libfreetype-dev libfontconfig1-dev libxft-dev libxrender-dev \
                    2>&1 | tail -2 || true
                ;;
            dnf|yum)
                $SUDO $PKG_MANAGER install -y \
                    autoconf automake libtool bison flex readline-devel \
                    libXaw-devel libX11-devel libXext-devel libXmu-devel libXpm-devel libXt-devel \
                    ncurses-devel freetype-devel fontconfig-devel libXft-devel libXrender-devel \
                    2>&1 | tail -2 || true
                ;;
            pacman)
                $SUDO pacman -S --noconfirm --needed \
                    autoconf automake libtool bison flex readline \
                    libxaw libx11 libxext libxmu libxpm libxt \
                    ncurses freetype2 fontconfig libxft libxrender \
                    2>&1 | tail -2 || true
                ;;
            zypper)
                $SUDO zypper --non-interactive install \
                    autoconf automake libtool bison flex readline-devel \
                    libXaw-devel libX11-devel libXext-devel libXmu-devel libXpm-devel libXt-devel \
                    ncurses-devel freetype2-devel fontconfig-devel libXft-devel libXrender-devel \
                    2>&1 | tail -2 || true
                ;;
            *)
                warn "Unknown package manager, trying apt-style..."
                $SUDO apt-get install -y -qq \
                    autoconf automake libtool bison flex libreadline-dev \
                    libxaw7-dev libx11-dev libxext-dev libxmu-dev libxpm-dev libxt-dev \
                    libncurses-dev libfreetype-dev libfontconfig1-dev libxft-dev libxrender-dev \
                    2>&1 | tail -2 || true
                ;;
        esac
        
        mkdir -p "$NGSPICE_BUILD" "$NGSPICE_INSTALL"
        cd "$NGSPICE_BUILD"
        
        # Download official ngspice source if not present (with fallback mirrors)
        if [ ! -f "$DL/$NGSPICE_TAR" ]; then
            progress "Downloading ngspice-${NGSPICE_VERSION}..."
            
            # Try primary URL first
            if wget -q --show-progress -O "$DL/$NGSPICE_TAR" "$NGSPICE_URL" 2>/dev/null && [ -s "$DL/$NGSPICE_TAR" ]; then
                ok "Downloaded from primary mirror"
            else
                # Primary failed, try fallback mirrors
                warn "Primary download failed, trying alternate mirrors..."
                rm -f "$DL/$NGSPICE_TAR"
                
                local mirrors=(
                    "https://master.dl.sourceforge.net/project/ngspice/ng-spice-rework/old-releases/${NGSPICE_VERSION}/${NGSPICE_TAR}"
                    "https://cfhcable.dl.sourceforge.net/project/ngspice/ng-spice-rework/old-releases/${NGSPICE_VERSION}/${NGSPICE_TAR}"
                    "https://versaweb.dl.sourceforge.net/project/ngspice/ng-spice-rework/old-releases/${NGSPICE_VERSION}/${NGSPICE_TAR}"
                    "https://phoenixnap.dl.sourceforge.net/project/ngspice/ng-spice-rework/old-releases/${NGSPICE_VERSION}/${NGSPICE_TAR}"
                )
                
                local download_ok=0
                for mirror in "${mirrors[@]}"; do
                    progress "Trying: $(echo $mirror | sed 's|.*/||')"
                    if wget -q --show-progress -O "$DL/$NGSPICE_TAR.tmp" --timeout=30 "$mirror" 2>/dev/null && [ -s "$DL/$NGSPICE_TAR.tmp" ]; then
                        if tar -tzf "$DL/$NGSPICE_TAR.tmp" >/dev/null 2>&1; then
                            mv "$DL/$NGSPICE_TAR.tmp" "$DL/$NGSPICE_TAR"
                            ok "Downloaded from $(echo $mirror | cut -d/ -f3)"
                            download_ok=1
                            break
                        else
                            rm -f "$DL/$NGSPICE_TAR.tmp"
                        fi
                    fi
                done
                
                if [ $download_ok -eq 0 ]; then
                    die "Failed to download ngspice-${NGSPICE_VERSION} from all mirrors. Check internet connection and retry."
                fi
            fi
        fi
        
        # Extract fresh
        progress "Extracting ngspice-${NGSPICE_VERSION} source..."
        rm -rf ngspice-*
        tar -xzf "$DL/$NGSPICE_TAR"
        
        cd "ngspice-${NGSPICE_VERSION}"
        
        # ═══ PATCH NGSPICE FOR NGHDL GHDL SERVER TERMINATION ═══
        # The NGHDL GHDL server expects ngspice to send "CLOSE_FROM_NGSPICE" message
        # when simulation ends. Without this patch, GHDL server exits abruptly with
        # exit(1) causing "Simulation Failed!" even when simulation data is valid.
        progress "Patching ngspice-35 for NGHDL GHDL server clean termination..."
        
        OUTITF_FILE="src/frontend/outitf.c"
        if [ -f "$OUTITF_FILE" ]; then
            # Only patch if not already patched
            if ! grep -q "NGHDL GHDL Server Termination" "$OUTITF_FILE"; then
                # Create a Python script to do the patching properly
                python3 << 'PATCH_SCRIPT'
import re

with open("src/frontend/outitf.c", "r") as f:
    content = f.read()

# 1. Add socket includes after misc_time.h include
include_addition = '''
/* NGHDL GHDL Server Termination - Added for NGHDL compatibility */
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
/* End NGHDL includes */'''

content = re.sub(
    r'(#include\s+"\.\.\/misc\/misc_time\.h")',
    r'\1' + include_addition,
    content
)

# 2. Add close_server() function before plotEnd()
close_server_func = '''
/* NGHDL - Close GHDL server after simulation */
static void close_server(void)
{
    FILE *fptr;
    char ip_filename[100];
    sprintf(ip_filename, "/tmp/NGHDL_COMMON_IP_%d.txt", getpid());
    fptr = fopen(ip_filename, "r");
    if(fptr) {
        char server_ip[20];
        char *message = "CLOSE_FROM_NGSPICE";
        int port = -1, sock = -1, try_limit = 0, skip_flag = 0;
        struct sockaddr_in serv_addr;
        serv_addr.sin_family = AF_INET;
        while(fscanf(fptr, "%s %d", server_ip, &port) == 2) {
            try_limit = 10; skip_flag = 0;
            while(try_limit > 0) {
                if((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
                    usleep(200000);
                    try_limit--;
                    if(try_limit == 0) skip_flag = 1;
                } else break;
            }
            if (skip_flag) continue;
            serv_addr.sin_port = htons(port);
            serv_addr.sin_addr.s_addr = inet_addr(server_ip);
            try_limit = 10; skip_flag = 0;
            while(try_limit > 0) {
                if(connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0) {
                    usleep(200000);
                    try_limit--;
                    if(try_limit == 0) skip_flag = 1;
                } else break;
            }
            if (skip_flag) continue;
            send(sock, message, strlen(message), 0);
            close(sock);
        }
        fclose(fptr);
    }
    remove(ip_filename);
}
/* End NGHDL close_server */

'''

# Find "static void\nplotEnd(runDesc *run)" and insert before it
content = re.sub(
    r'(\nstatic void\nplotEnd\(runDesc \*run\))',
    close_server_func + r'\1',
    content
)

# 3. Add close_server() call at the beginning of plotEnd()
content = re.sub(
    r'(plotEnd\(runDesc \*run\)\s*\{)',
    r'\1\n    /* NGHDL - Close GHDL server */\n    close_server();',
    content
)

with open("src/frontend/outitf.c", "w") as f:
    f.write(content)

print("Patched successfully")
PATCH_SCRIPT
                
                ok "Patched outitf.c for NGHDL GHDL server termination"
            else
                progress "outitf.c already patched for NGHDL"
            fi
        else
            warn "outitf.c not found, GHDL server termination may not work cleanly"
        fi
        
        mkdir -p release && cd release
        
        # GCC 15+ (Fedora 43+) defaults to gnu23 which breaks ngspice-35 old C code
        # Force gnu17 standard and relax pointer type errors for compatibility
        local NGSPICE_CFLAGS=""
        if gcc -dumpversion 2>/dev/null | awk -F. '{exit ($1 >= 14) ? 0 : 1}'; then
            NGSPICE_CFLAGS="-std=gnu17 -Wno-error=incompatible-pointer-types -Wno-error=int-conversion -Wno-error=implicit-function-declaration"
            progress "Detected GCC $(gcc -dumpversion) - adding C17 compatibility flags for ngspice-35"
        fi
        
        progress "Configuring ngspice-${NGSPICE_VERSION} with XSPICE and X11 graphics..."
        ../configure \
            --enable-xspice \
            --with-x \
            --disable-debug \
            --prefix="$NGSPICE_INSTALL" \
            --exec-prefix="$NGSPICE_INSTALL" \
            CFLAGS="$NGSPICE_CFLAGS" 2>&1 | tail -5 || die "NgSpice configure failed"
        
        progress "Building ngspice-${NGSPICE_VERSION} (this takes a few minutes)..."
        make -j$(nproc) 2>&1 | tail -5 || die "NgSpice build failed"
        make install 2>&1 | tail -2 || die "NgSpice install failed"
        ok "NgSpice-${NGSPICE_VERSION} built from official source with X11 graphics"
    fi
    
    # Bundle ngspice-35 binary ONLY - for ABI compatibility with NGHDL codemodels
    # NGHDL compiles ghdl.cm against ngspice-35 source, so we MUST use ngspice-35 binary
    if [ -x "$NGSPICE_INSTALL/bin/ngspice" ]; then
        progress "Bundling ngspice-35 (required for NGHDL compatibility)..."
        cp -L "$NGSPICE_INSTALL/bin/ngspice" "$APPDIR/usr/bin/ngspice"
        chmod +x "$APPDIR/usr/bin/ngspice"
        ok "NgSpice bundled: ngspice-35 (built from source - NGHDL compatible)"
    else
        die "NgSpice-35 build failed - no binary produced"
    fi
    
    # Bundle ONLY ngspice-35 built codemodels - DO NOT mix with system codemodels
    # System codemodels may be from a different ngspice version causing ABI issues
    if [ -d "$NGSPICE_INSTALL/lib/ngspice" ]; then
        cp -r "$NGSPICE_INSTALL/lib/ngspice"/* "$APPDIR/usr/lib/ngspice/" 2>/dev/null || true
        ok "Bundled ngspice-35 codemodels from build"
    fi
    [ -d "$NGSPICE_INSTALL/share/ngspice" ] && cp -r "$NGSPICE_INSTALL/share/ngspice"/* "$APPDIR/usr/share/ngspice/" 2>/dev/null || true
    
    # ═══ SPINIT - USE SYSTEM FALLBACK PATHS ═══
    # NOTE: The esim launcher will generate a runtime spinit with absolute AppImage paths
    # This bundled spinit serves as a fallback if runtime generation fails
    progress "Creating fallback spinit for system paths..."
    SPINIT_FILE="$APPDIR/usr/share/ngspice/scripts/spinit"
    if [ -f "$SPINIT_FILE" ]; then
        cat > "$SPINIT_FILE" << 'SPINITFALLBACK'
* Standard ngspice init file - eSim AppImage fallback version
* Runtime spinit with AppImage paths is generated by launcher
alias exit quit
alias acct rusage all
set x11lineararcs

* comment out if central osdi management is set up
unset osdi_enabled

* Load the codemodels from system paths (fallback)
if $?xspice_enabled

  codemodel /usr/lib/x86_64-linux-gnu/ngspice/analog.cm
  codemodel /usr/lib/x86_64-linux-gnu/ngspice/digital.cm
  codemodel /usr/lib/x86_64-linux-gnu/ngspice/spice2poly.cm
  codemodel /usr/lib/x86_64-linux-gnu/ngspice/xtradev.cm
  codemodel /usr/lib/x86_64-linux-gnu/ngspice/xtraevt.cm
  codemodel /usr/lib/x86_64-linux-gnu/ngspice/table.cm

end

SPINITFALLBACK
        ok "Fallback spinit created (runtime spinit will override)"
    else
        warn "spinit file not found - skipping"
    fi
    
    # Bundle GHDL - check multiple locations
    SYSTEM_GHDL=""
    for ghdl_path in /usr/bin/ghdl /usr/local/bin/ghdl; do
        if [ -x "$ghdl_path" ]; then
            SYSTEM_GHDL="$ghdl_path"
            break
        fi
    done
    
    if [ -n "$SYSTEM_GHDL" ]; then
        progress "Found GHDL at $SYSTEM_GHDL, bundling with backend drivers..."
        
        # Copy ALL GHDL binaries (including ghdl1-llvm, ghdl-mcode, etc.)
        for bin_dir in /usr/bin /usr/local/bin; do
            [ -d "$bin_dir" ] && cp -P "$bin_dir"/ghdl* "$APPDIR/usr/bin/" 2>/dev/null || true
        done
        
        # Ensure the main binary is named ghdl-real for the wrapper
        if [ -x "$APPDIR/usr/bin/ghdl" ]; then
            mv "$APPDIR/usr/bin/ghdl" "$APPDIR/usr/bin/ghdl-real"
        fi
        
        # Copy GHDL libraries from system (multi-arch aware)
        mkdir -p "$APPDIR/usr/lib/ghdl"
        # Copy from multiple possible locations across distros
        for lib_dir in /usr/lib/ghdl /usr/local/lib/ghdl /usr/lib/x86_64-linux-gnu/ghdl \
                       /usr/lib64/ghdl /usr/share/ghdl; do
            [ -d "$lib_dir" ] && cp -r "$lib_dir"/* "$APPDIR/usr/lib/ghdl/" 2>/dev/null || true
        done
        
        # Create GHDL wrapper that prefers system GHDL-LLVM (required for NGHDL C linking)
        # This wrapper detects the correct LLVM version and GHDL backend automatically
        cat > "$APPDIR/usr/bin/ghdl" << 'GHDLWRAPPER'
#!/bin/bash
# GHDL wrapper for eSim AppImage - Multi-Distro Compatible
# MUST use ghdl-llvm for NGHDL simulation (ghdl-mcode cannot link with C code via -Wl option)
# Supports: Ubuntu, Debian, Fedora, Arch, openSUSE and derivatives

SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
APPDIR_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"

# ═══ AUTO-DETECT LLVM VERSION AND SET LD_LIBRARY_PATH ═══
# Different distros have LLVM libraries in different locations and versions
detect_llvm() {
    # Check for LLVM in various locations across distros
    local llvm_dirs=(
        /usr/lib/x86_64-linux-gnu       # Debian/Ubuntu
        /usr/lib64                       # Fedora/RHEL
        /usr/lib                         # Arch
        /usr/lib/llvm/*/lib              # Gentoo/some distros
    )
    
    for dir in "${llvm_dirs[@]}"; do
        # Try each LLVM version from newest to oldest
        for ver in 18 17 16 15 14 13 12 11; do
            for lib in "$dir/libLLVM-${ver}"*.so* "$dir/libLLVM.so.${ver}"* "$dir/llvm-${ver}/lib/libLLVM"*.so*; do
                if [ -f "$lib" ]; then
                    export LD_LIBRARY_PATH="${dir}:${LD_LIBRARY_PATH}"
                    return 0
                fi
            done
        done
        # Also check for unversioned libLLVM
        if [ -f "$dir/libLLVM.so" ]; then
            export LD_LIBRARY_PATH="${dir}:${LD_LIBRARY_PATH}"
            return 0
        fi
    done
    return 1
}

# Set up LLVM for GHDL
detect_llvm

# Find the correct GHDL_PREFIX for LLVM backend first, then mcode
# Check multiple paths used by different distros
for ghdl_lib_base in /usr/lib/ghdl /usr/local/lib/ghdl /usr/lib/x86_64-linux-gnu/ghdl \
                     /usr/lib64/ghdl /usr/share/ghdl /opt/ghdl/lib; do
    # For llvm backend, libraries are at ghdl_lib_base/llvm/vhdl/ieee/
    if [ -d "$ghdl_lib_base/llvm/vhdl/ieee" ]; then
        export GHDL_PREFIX="$ghdl_lib_base/llvm/vhdl"
        break
    # Alternative LLVM path structure
    elif [ -d "$ghdl_lib_base/llvm/lib/ghdl/ieee" ]; then
        export GHDL_PREFIX="$ghdl_lib_base/llvm/lib/ghdl"
        break
    # For mcode backend (fallback)
    elif [ -d "$ghdl_lib_base/mcode/vhdl/ieee" ]; then
        export GHDL_PREFIX="$ghdl_lib_base/mcode/vhdl"
        break
    # Some installs put ieee directly under ghdl_lib_base
    elif [ -d "$ghdl_lib_base/ieee" ]; then
        export GHDL_PREFIX="$ghdl_lib_base"
        break
    # Arch Linux structure
    elif [ -d "$ghdl_lib_base/lib/ghdl/ieee" ]; then
        export GHDL_PREFIX="$ghdl_lib_base/lib/ghdl"
        break
    fi
done

# IMPORTANT: Prefer ghdl-llvm for NGHDL (can link with C code via -Wl option)
# ghdl-mcode does NOT support -Wl for external C linking
# Search in multiple locations used by different distros
for ghdl_bin in /usr/bin/ghdl-llvm /usr/local/bin/ghdl-llvm \
                /usr/bin/ghdl /usr/local/bin/ghdl \
                /opt/ghdl/bin/ghdl /usr/bin/ghdl-mcode /usr/local/bin/ghdl-mcode; do
    if [ -x "$ghdl_bin" ]; then
        # Check if it's llvm or mcode backend
        if "$ghdl_bin" --version 2>/dev/null | grep -qi "llvm"; then
            exec "$ghdl_bin" "$@"
        elif [ "$ghdl_bin" != "/usr/bin/ghdl-mcode" ] && [ "$ghdl_bin" != "/usr/local/bin/ghdl-mcode" ]; then
            # For generic ghdl binary, check backend
            exec "$ghdl_bin" "$@"
        fi
    fi
done

# Fall back to any available ghdl (including mcode as last resort)
for ghdl_bin in /usr/bin/ghdl /usr/local/bin/ghdl /usr/bin/ghdl-mcode; do
    if [ -x "$ghdl_bin" ]; then
        exec "$ghdl_bin" "$@"
    fi
done

# Fall back to bundled GHDL if system not available
BUNDLED_GHDL="$APPDIR_ROOT/usr/bin/ghdl-llvm"
if [ ! -x "$BUNDLED_GHDL" ]; then
    BUNDLED_GHDL="$APPDIR_ROOT/usr/bin/ghdl-mcode"
fi
if [ ! -x "$BUNDLED_GHDL" ]; then
    BUNDLED_GHDL="$APPDIR_ROOT/usr/bin/ghdl-real"
fi
BUNDLED_LIBS="$APPDIR_ROOT/usr/lib/ghdl"

if [ -x "$BUNDLED_GHDL" ]; then
    if [ -d "$BUNDLED_LIBS/llvm/vhdl/ieee" ]; then
        export GHDL_PREFIX="$BUNDLED_LIBS/llvm/vhdl"
    elif [ -d "$BUNDLED_LIBS/mcode/vhdl/ieee" ]; then
        export GHDL_PREFIX="$BUNDLED_LIBS/mcode/vhdl"
    elif [ -d "$BUNDLED_LIBS/ieee" ]; then
        export GHDL_PREFIX="$BUNDLED_LIBS"
    fi
    export LD_LIBRARY_PATH="$APPDIR_ROOT/usr/lib:${LD_LIBRARY_PATH}"
    exec "$BUNDLED_GHDL" "$@"
fi

# Print installation help for different distros
echo "Error: GHDL not found. Please install ghdl-llvm package:" >&2
echo "" >&2
echo "  Ubuntu/Debian: sudo apt install ghdl-llvm" >&2
echo "  Fedora:        $SUDO dnf copr enable openvsx/ghdl && $SUDO dnf install ghdl" >&2
echo "  Arch Linux:    yay -S ghdl-llvm-git" >&2
echo "  openSUSE:      (Manual installation required)" >&2
echo "" >&2
exit 1
GHDLWRAPPER
        chmod +x "$APPDIR/usr/bin/ghdl"
        ok "GHDL wrapper created (uses system GHDL at $SYSTEM_GHDL)"
    else
        warn "GHDL not found (optional for NGHDL)"
    fi
    
    # Bundle Verilator
    if [ -x "/usr/bin/verilator" ]; then
        cp -L /usr/bin/verilator* "$APPDIR/usr/bin/" 2>/dev/null || true
        ok "Verilator bundled"
    fi
    
    # ═══ BUNDLE OPENMODELICA (omc + OMEdit) ═══
    OM_VERSION="1.23.1"
    OM_BASE_URL="https://build.openmodelica.org/omc/builds/linux/releases/${OM_VERSION}/pool/contrib-jammy"
    OM_EXTRACT_DIR="$BUILD/openmodelica"
    
    if [ ! -d "$OM_EXTRACT_DIR/usr" ] || [ ! -f "$OM_EXTRACT_DIR/usr/bin/OMEdit" ]; then
        progress "Downloading OpenModelica ${OM_VERSION} (omc + OMEdit)..."
        mkdir -p "$OM_EXTRACT_DIR"
        cd "$DL"
        
        # Download required OpenModelica packages INCLUDING OMEdit and OMSimulator
        OM_PACKAGES=(
            "omc_${OM_VERSION}-1_amd64.deb"
            "omc-common_${OM_VERSION}-1_all.deb"
            "libomc_${OM_VERSION}-1_amd64.deb"
            "libomcsimulation_${OM_VERSION}-1_amd64.deb"
            "omedit_${OM_VERSION}-1_amd64.deb"
            "libomplot_${OM_VERSION}-1_amd64.deb"
            "omsimulator_${OM_VERSION}-1_amd64.deb"
            "libomsimulator_${OM_VERSION}-1_amd64.deb"
            "omlibrary_${OM_VERSION}-1_all.deb"
        )
        
        for pkg in "${OM_PACKAGES[@]}"; do
            if [ ! -f "$DL/$pkg" ]; then
                wget -q "$OM_BASE_URL/$pkg" -O "$DL/$pkg" 2>/dev/null || {
                    warn "Could not download $pkg"
                    continue
                }
            fi
            # Extract deb package
            cd "$OM_EXTRACT_DIR"
            ar x "$DL/$pkg" 2>/dev/null || true
            [ -f data.tar.xz ] && tar -xJf data.tar.xz 2>/dev/null && rm -f data.tar.xz control.tar.* debian-binary
            [ -f data.tar.zst ] && zstd -d data.tar.zst -o data.tar 2>/dev/null && tar -xf data.tar && rm -f data.tar data.tar.zst control.tar.* debian-binary
            [ -f data.tar.gz ] && tar -xzf data.tar.gz 2>/dev/null && rm -f data.tar.gz control.tar.* debian-binary
        done
        cd "$DL"
        ok "OpenModelica ${OM_VERSION} (omc + OMEdit + OMSimulator) downloaded and extracted"
    else
        ok "OpenModelica ${OM_VERSION} (omc + OMEdit) already extracted, reusing..."
    fi
    
    # Bundle OpenModelica into AppImage
    if [ -d "$OM_EXTRACT_DIR/usr" ]; then
        progress "Bundling OpenModelica into AppImage..."
        
        # Install OMEdit runtime dependencies (OpenSceneGraph, Qt5 WebKit, etc.)
        progress "Installing OMEdit runtime dependencies..."
        case "$PKG_MANAGER" in
            apt)
                $SUDO apt-get install -y -qq \
                    libopenscenegraph-dev libopenthreads-dev \
                    libqt5webkit5 libqt5opengl5 libqt5xmlpatterns5 libqt5concurrent5 \
                    libomniorb4-dev libomnithread4-dev \
                    2>&1 | tail -2 || true
                ;;
            dnf|yum)
                $SUDO $PKG_MANAGER install -y \
                    OpenSceneGraph-devel OpenThreads-devel \
                    qt5-qtwebkit qt5-qtbase-devel qt5-qtxmlpatterns \
                    omniORB-devel \
                    2>&1 | tail -2 || true
                ;;
            pacman)
                # Note: qt5-webkit and openscenegraph are NOT available on Arch
                # They are bundled from Ubuntu .deb archives in the fallback section below
                # Install native Qt5 modules needed by Qt5WebKit (must match system Qt5 ABI)
                $SUDO pacman -S --noconfirm --needed \
                    qt5-base qt5-xmlpatterns \
                    qt5-declarative qt5-sensors qt5-location \
                    2>&1 | tail -2 || true
                ;;
            zypper)
                $SUDO zypper --non-interactive install \
                    libOpenSceneGraph-devel libOpenThreads-devel \
                    libqt5-qtwebkit libqt5-qtbase-devel \
                    2>&1 | tail -2 || true
                ;;
            *)
                warn "Unknown package manager, OMEdit dependencies may be incomplete"
                ;;
        esac
        
        # Copy OpenModelica binaries (including OMEdit)
        [ -d "$OM_EXTRACT_DIR/usr/bin" ] && {
            cp -r "$OM_EXTRACT_DIR/usr/bin/"* "$APPDIR/usr/bin/" 2>/dev/null || true
        }
        
        # Copy OpenModelica include files (needed for simulation compilation)
        [ -d "$OM_EXTRACT_DIR/usr/include" ] && {
            mkdir -p "$APPDIR/usr/include"
            cp -r "$OM_EXTRACT_DIR/usr/include/"* "$APPDIR/usr/include/" 2>/dev/null || true
        }
        
        # Copy OpenModelica libraries (handle nested directory structure)
        [ -d "$OM_EXTRACT_DIR/usr/lib" ] && {
            # Copy all lib content including nested x86_64-linux-gnu directories
            cp -r "$OM_EXTRACT_DIR/usr/lib/"* "$APPDIR/usr/lib/" 2>/dev/null || true
            
            # Copy nested omc libraries to a path in LD_LIBRARY_PATH
            if [ -d "$OM_EXTRACT_DIR/usr/lib/x86_64-linux-gnu/omc" ]; then
                mkdir -p "$APPDIR/usr/lib/x86_64-linux-gnu/omc"
                cp -r "$OM_EXTRACT_DIR/usr/lib/x86_64-linux-gnu/omc/"* "$APPDIR/usr/lib/x86_64-linux-gnu/omc/" 2>/dev/null || true
                # Also copy to main lib path for easier discovery
                cp -r "$OM_EXTRACT_DIR/usr/lib/x86_64-linux-gnu/omc/"*.so* "$APPDIR/usr/lib/" 2>/dev/null || true
            fi
            # Also check lib64 (Fedora/RHEL/Arch)
            if [ -d "$OM_EXTRACT_DIR/usr/lib64/omc" ]; then
                mkdir -p "$APPDIR/usr/lib/x86_64-linux-gnu/omc"
                cp -r "$OM_EXTRACT_DIR/usr/lib64/omc/"* "$APPDIR/usr/lib/x86_64-linux-gnu/omc/" 2>/dev/null || true
                cp -r "$OM_EXTRACT_DIR/usr/lib64/omc/"*.so* "$APPDIR/usr/lib/" 2>/dev/null || true
            fi
            
            # Copy omc share folder inside lib if present
            [ -d "$OM_EXTRACT_DIR/usr/lib/omc" ] && {
                mkdir -p "$APPDIR/usr/lib/omc"
                cp -r "$OM_EXTRACT_DIR/usr/lib/omc/"* "$APPDIR/usr/lib/omc/" 2>/dev/null || true
            }
        }
        
        # Bundle OMEdit runtime library dependencies from system
        # Search in multiple locations for different distros
        progress "Bundling OMEdit library dependencies..."
        for lib in libosg libosgViewer libosgUtil libosgDB libosgGA libOpenThreads \
                   libQt5WebKit libQt5WebKitWidgets libQt5OpenGL libQt5XmlPatterns libQt5Concurrent \
                   libomniORB libomnithread libnsl; do
            # Check multiple lib paths (Debian/Ubuntu, Fedora/RHEL/Arch)
            for libdir in /usr/lib/x86_64-linux-gnu /usr/lib64 /usr/lib; do
                for libpath in ${libdir}/${lib}*.so*; do
                    if [ -f "$libpath" ] && [ ! -f "$APPDIR/usr/lib/$(basename "$libpath")" ]; then
                        cp -L "$libpath" "$APPDIR/usr/lib/" 2>/dev/null || true
                    fi
                done
            done
        done
        
        # ═══ BUNDLE LAPACK AND BLAS LIBRARIES (REQUIRED FOR OPENMODELICA SIMULATION) ═══
        progress "Bundling LAPACK and BLAS libraries for OpenModelica..."
        # Copy LAPACK and BLAS shared libraries from system (multi-distro paths)
        for lib in liblapack libblas libgfortran libquadmath; do
            for libdir in /usr/lib/x86_64-linux-gnu /usr/lib64 /usr/lib; do
                for libpath in ${libdir}/${lib}*.so*; do
                    if [ -f "$libpath" ] && [ ! -f "$APPDIR/usr/lib/$(basename "$libpath")" ]; then
                        cp -L "$libpath" "$APPDIR/usr/lib/" 2>/dev/null || true
                    fi
                done
            done
        done
        # Remove libgfortran and libquadmath from bundle — these are compiler
        # runtime libs that MUST come from the host system (like libstdc++/libgcc_s).
        # They're bundled momentarily to resolve ldd checks but the host provides
        # versions matching its own glibc.
        rm -f "$APPDIR"/usr/lib/libgfortran.so* "$APPDIR"/usr/lib/libquadmath.so* 2>/dev/null
        progress "Removed libgfortran/libquadmath from bundle (will use host system versions)"
        # Create unversioned symlinks if they don't exist (needed for -llapack -lblas linking)
        if [ -f "$APPDIR/usr/lib/liblapack.so.3" ] && [ ! -f "$APPDIR/usr/lib/liblapack.so" ]; then
            ln -sf liblapack.so.3 "$APPDIR/usr/lib/liblapack.so"
        fi
        if [ -f "$APPDIR/usr/lib/libblas.so.3" ] && [ ! -f "$APPDIR/usr/lib/libblas.so" ]; then
            ln -sf libblas.so.3 "$APPDIR/usr/lib/libblas.so"
        fi
        # Also copy from omc lib directory if present in extracted package
        for libpath in "$OM_EXTRACT_DIR/usr/lib/x86_64-linux-gnu/omc/"liblapack*.so* \
                       "$OM_EXTRACT_DIR/usr/lib/x86_64-linux-gnu/omc/"libblas*.so*; do
            if [ -f "$libpath" ]; then
                cp -L "$libpath" "$APPDIR/usr/lib/x86_64-linux-gnu/omc/" 2>/dev/null || true
                cp -L "$libpath" "$APPDIR/usr/lib/" 2>/dev/null || true
            fi
        done
        lapack_count=$(find "$APPDIR/usr/lib/" -maxdepth 1 \( -name 'liblapack*' -o -name 'libblas*' \) 2>/dev/null | wc -l)
        if [ "$lapack_count" -gt 0 ]; then
            ok "LAPACK/BLAS bundled: $lapack_count library files"
        else
            # Check if LAPACK/BLAS are even installed in the system
            if [ ! -f "/usr/lib/liblapack.so" ] && [ ! -f "/usr/lib64/liblapack.so" ] && \
               [ ! -f "/usr/lib/x86_64-linux-gnu/liblapack.so" ]; then
                warn "LAPACK/BLAS not found in AppDir AND not in system"
                warn "Installation instructions:"
                case "$DISTRO_FAMILY" in
                    debian)
                        echo "  $SUDO apt-get install -y liblapack-dev libblas-dev"
                        ;;
                    fedora|rhel)
                        echo "  $SUDO dnf install -y lapack-devel blas-devel"
                        ;;
                    arch)
                        echo "  $SUDO pacman -S lapack blas"
                        ;;
                    suse)
                        echo "  $SUDO zypper install lapack-devel blas-devel"
                        ;;
                    *)
                        echo "  Install lapack-devel blas-devel or equivalent for your distro"
                        ;;
                esac
            else
                warn "LAPACK/BLAS found in system but not copied to AppDir - copying now..."
                # Attempt to find and copy them
                for libdir in /usr/lib/x86_64-linux-gnu /usr/lib64 /usr/lib; do
                    for libpath in ${libdir}/liblapack*.so* ${libdir}/libblas*.so*; do
                        if [ -f "$libpath" ]; then
                            cp -L "$libpath" "$APPDIR/usr/lib/" 2>/dev/null && echo "  ✓ Copied $(basename "$libpath")"
                        fi
                    done
                done
                # Re-count and verify
                lapack_count=$(find "$APPDIR/usr/lib/" -maxdepth 1 \( -name 'liblapack*' -o -name 'libblas*' \) 2>/dev/null | wc -l)
                if [ "$lapack_count" -gt 0 ]; then
                    ok "LAPACK/BLAS now bundled: $lapack_count library files"
                else
                    warn "Still could not bundle LAPACK/BLAS - OpenModelica may have reduced functionality"
                fi
            fi
        fi
        
        # Download ICU 70 libraries from Ubuntu 22.04 (OMEdit is built against ICU 70)
        ICU70_DIR="$BUILD/icu70"
        if [ ! -d "$ICU70_DIR/usr" ]; then
            progress "Downloading ICU 70 libraries for OMEdit compatibility..."
            mkdir -p "$ICU70_DIR"
            cd "$ICU70_DIR"
            wget -q "http://archive.ubuntu.com/ubuntu/pool/main/i/icu/libicu70_70.1-2_amd64.deb" -O libicu70.deb 2>/dev/null || true
            if [ -f libicu70.deb ]; then
                ar x libicu70.deb 2>/dev/null || true
                [ -f data.tar.zst ] && zstd -d data.tar.zst -o data.tar 2>/dev/null && tar -xf data.tar && rm -f data.tar
                [ -f data.tar.xz ] && tar -xJf data.tar.xz 2>/dev/null
                [ -f data.tar.gz ] && tar -xzf data.tar.gz 2>/dev/null
                rm -f *.tar* control.tar.* debian-binary libicu70.deb 2>/dev/null
            fi
            cd "$DL"
        fi
        
        # Bundle ICU 70 libraries
        if [ -d "$ICU70_DIR/usr/lib/x86_64-linux-gnu" ]; then
            for libpath in "$ICU70_DIR/usr/lib/x86_64-linux-gnu/"libicu*.so*; do
                if [ -f "$libpath" ]; then
                    cp -L "$libpath" "$APPDIR/usr/lib/" 2>/dev/null || true
                fi
            done
        fi
        
        # ═══ DOWNLOAD MISSING OMEDIT UBUNTU DEPS AS .DEB FALLBACK ═══
        # OMEdit binary is from Ubuntu 22.04. On non-Ubuntu distros (Arch, Fedora, etc.)
        # the exact soname versions (libosg.so.161, libQt5WebKit.so.5, etc.) don't exist.
        # Download them from Ubuntu archives like we do for ICU 70.
        _bundle_ubuntu_deb() {
            # Usage: _bundle_ubuntu_deb <url> <lib_pattern> <description>
            local _url="$1" _pattern="$2" _desc="$3"
            local _tmpdir="$BUILD/ubuntu_deb_tmp"
            mkdir -p "$_tmpdir"
            local _debfile="$_tmpdir/pkg.deb"
            if wget -q "$_url" -O "$_debfile" 2>/dev/null; then
                cd "$_tmpdir"
                ar x "$_debfile" 2>/dev/null || true
                [ -f data.tar.zst ] && zstd -d data.tar.zst -o data.tar 2>/dev/null && tar -xf data.tar && rm -f data.tar
                [ -f data.tar.xz ] && tar -xJf data.tar.xz 2>/dev/null
                [ -f data.tar.gz ] && tar -xzf data.tar.gz 2>/dev/null
                # Copy matching libs from all lib paths in the extracted deb
                find "$_tmpdir" -name "${_pattern}" -type f 2>/dev/null | while read -r _lib; do
                    cp -L "$_lib" "$APPDIR/usr/lib/" 2>/dev/null || true
                done
                # Also copy symlinks
                find "$_tmpdir" -name "${_pattern}" -type l 2>/dev/null | while read -r _link; do
                    cp -d "$_link" "$APPDIR/usr/lib/" 2>/dev/null || true
                done
                rm -rf "$_tmpdir"
                cd "$DL"
                return 0
            else
                rm -rf "$_tmpdir"
                cd "$DL"
                return 1
            fi
        }
        
        # OpenSceneGraph (libosg.so.161) - needed by OMEdit
        if [ ! -f "$APPDIR/usr/lib/libosg.so.161" ]; then
            progress "Downloading OpenSceneGraph 3.6 from Ubuntu 22.04 for OMEdit..."
            _bundle_ubuntu_deb \
                "http://archive.ubuntu.com/ubuntu/pool/universe/o/openscenegraph/libopenscenegraph161_3.6.5+dfsg1-7build3_amd64.deb" \
                "libosg*.so*" "OpenSceneGraph" && \
            _bundle_ubuntu_deb \
                "http://archive.ubuntu.com/ubuntu/pool/universe/o/openscenegraph/libopenthreads21_3.6.5+dfsg1-7build3_amd64.deb" \
                "libOpenThreads*.so*" "OpenThreads" && \
            ok "OpenSceneGraph bundled from Ubuntu 22.04" || \
            warn "Failed to download OpenSceneGraph - OMEdit may not work"
        fi
        
        # Qt5 WebKit (libQt5WebKit.so.5) - needed by OMEdit
        # Use Jammy (22.04) version which is compatible with our ICU 70
        if [ ! -f "$APPDIR/usr/lib/libQt5WebKit.so.5" ]; then
            progress "Downloading Qt5 WebKit from Ubuntu 22.04 for OMEdit..."
            _bundle_ubuntu_deb \
                "http://archive.ubuntu.com/ubuntu/pool/universe/q/qtwebkit-opensource-src/libqt5webkit5_5.212.0~alpha4-1ubuntu2.1_amd64.deb" \
                "libQt5WebKit*.so*" "Qt5WebKit" && \
            ok "Qt5 WebKit bundled from Ubuntu 22.04" || \
            warn "Failed to download Qt5 WebKit - OMEdit may have reduced functionality"
        fi
        
        # Qt5 WebKit transitive dependencies
        # IMPORTANT: Do NOT bundle Qt5 modules (Quick, Qml, Positioning, Sensors) from Ubuntu
        # They use Qt_5_PRIVATE_API symbols that are ABI-incompatible with the host Qt5.
        # Instead, install them from the native package manager (done in OMEdit deps above).
        # Only bundle Qt5WebChannel from Ubuntu (no standalone package on Arch) and non-Qt libs.
        
        # Qt5WebChannel (not available as standalone package on Arch/Fedora)
        if [ ! -f "$APPDIR/usr/lib/libQt5WebChannel.so.5" ]; then
            _bundle_ubuntu_deb \
                "http://archive.ubuntu.com/ubuntu/pool/universe/q/qtwebchannel-opensource-src/libqt5webchannel5_5.15.3-1_amd64.deb" \
                "libQt5WebChannel*.so*" "Qt5WebChannel" || true
        fi
        # ICU 66 (Qt5WebKit uses versioned symbols like u_strToLower_66)
        if [ ! -f "$APPDIR/usr/lib/libicuuc.so.66" ]; then
            progress "Downloading ICU 66 for Qt5WebKit compatibility..."
            _bundle_ubuntu_deb \
                "http://archive.ubuntu.com/ubuntu/pool/main/i/icu/libicu66_66.1-2ubuntu2.1_amd64.deb" \
                "libicu*.so*" "ICU66" && \
            ok "ICU 66 bundled for Qt5WebKit" || true
        fi
        # woff2 decoder
        if [ ! -f "$APPDIR/usr/lib/libwoff2dec.so.1.0.2" ]; then
            _bundle_ubuntu_deb \
                "http://archive.ubuntu.com/ubuntu/pool/main/w/woff2/libwoff1_1.0.2-1build4_amd64.deb" \
                "libwoff*.so*" "woff2" || true
        fi
        # libwebp6
        if [ ! -f "$APPDIR/usr/lib/libwebp.so.6" ]; then
            _bundle_ubuntu_deb \
                "http://archive.ubuntu.com/ubuntu/pool/main/libw/libwebp/libwebp6_0.6.1-2_amd64.deb" \
                "libwebp*.so*" "webp6" || true
        fi
        # libxml2
        if [ ! -f "$APPDIR/usr/lib/libxml2.so.2" ]; then
            _bundle_ubuntu_deb \
                "http://archive.ubuntu.com/ubuntu/pool/main/libx/libxml2/libxml2_2.9.13+dfsg-1build1_amd64.deb" \
                "libxml2*.so*" "xml2" || true
        fi
        # hyphen
        if [ ! -f "$APPDIR/usr/lib/libhyphen.so.0" ]; then
            _bundle_ubuntu_deb \
                "http://archive.ubuntu.com/ubuntu/pool/main/h/hyphen/libhyphen0_2.8.8-7build2_amd64.deb" \
                "libhyphen*.so*" "hyphen" || true
        fi
        
        progress "Qt5 WebKit dependency chain bundled"
        
        # Qt5 XmlPatterns (libQt5XmlPatterns.so.5) - needed by OMEdit
        if [ ! -f "$APPDIR/usr/lib/libQt5XmlPatterns.so.5" ]; then
            progress "Downloading Qt5 XmlPatterns from Ubuntu 22.04 for OMEdit..."
            _bundle_ubuntu_deb \
                "http://archive.ubuntu.com/ubuntu/pool/universe/q/qtxmlpatterns-opensource-src/libqt5xmlpatterns5_5.15.3-1_amd64.deb" \
                "libQt5XmlPatterns*.so*" "Qt5XmlPatterns" && \
            ok "Qt5 XmlPatterns bundled from Ubuntu 22.04" || \
            warn "Failed to download Qt5 XmlPatterns"
        fi
        
        # omniORB (libomniORB4.so.2) - needed by OMEdit
        if [ ! -f "$APPDIR/usr/lib/libomniORB4.so.2" ]; then
            progress "Downloading omniORB from Ubuntu 22.04 for OMEdit..."
            _bundle_ubuntu_deb \
                "http://archive.ubuntu.com/ubuntu/pool/universe/o/omniorb-dfsg/libomniorb4-2_4.2.5-1_amd64.deb" \
                "libomni*.so*" "omniORB" && \
            _bundle_ubuntu_deb \
                "http://archive.ubuntu.com/ubuntu/pool/universe/o/omniorb-dfsg/libomnithread4_4.2.5-1_amd64.deb" \
                "libomnithread*.so*" "omnithread" && \
            ok "omniORB + omnithread bundled from Ubuntu 22.04" || \
            warn "Failed to download omniORB - OMEdit may not work"
        fi
        
        # libnsl (libnsl.so.2) - needed by OMEdit
        if [ ! -f "$APPDIR/usr/lib/libnsl.so.2" ]; then
            progress "Downloading libnsl from Ubuntu 22.04 for OMEdit..."
            _bundle_ubuntu_deb \
                "http://archive.ubuntu.com/ubuntu/pool/main/libn/libnsl/libnsl2_1.3.0-2build2_amd64.deb" \
                "libnsl*.so*" "libnsl" && \
            ok "libnsl bundled from Ubuntu 22.04" || \
            warn "Failed to download libnsl"
        fi
        
        # Create version compatibility symlinks for OMEdit (built for Ubuntu 22.04)
        # Note: ICU 66 is downloaded above for Qt5WebKit, ICU 70 for OMEdit
        # Both coexist in AppDir/usr/lib (ICU uses versioned function symbols)
        # libomniORB4.so.2 -> .3 (compatible ABI)
        if [ -f "$APPDIR/usr/lib/libomniORB4.so.3" ] && [ ! -f "$APPDIR/usr/lib/libomniORB4.so.2" ]; then
            ln -sf libomniORB4.so.3 "$APPDIR/usr/lib/libomniORB4.so.2"
        fi
        # libomnithread.so.4 if needed
        if [ -f "$APPDIR/usr/lib/libomnithread.so.4" ] && [ ! -f "$APPDIR/usr/lib/libomnithread.so.3" ]; then
            ln -sf libomnithread.so.4 "$APPDIR/usr/lib/libomnithread.so.3"
        fi
        # libnsl.so.2 -> .1 (may work)
        if [ -f "$APPDIR/usr/lib/libnsl.so.1" ] && [ ! -f "$APPDIR/usr/lib/libnsl.so.2" ]; then
            ln -sf libnsl.so.1 "$APPDIR/usr/lib/libnsl.so.2"
        fi
        
        # Also bundle libOMSimulator if available in the extracted package
        if [ -f "$OM_EXTRACT_DIR/usr/lib/x86_64-linux-gnu/libOMSimulator.so" ]; then
            cp -L "$OM_EXTRACT_DIR/usr/lib/x86_64-linux-gnu/libOMSimulator.so"* "$APPDIR/usr/lib/" 2>/dev/null || true
        fi
        
        # Copy OpenModelica share files (libraries, resources)
        [ -d "$OM_EXTRACT_DIR/usr/share/omc" ] && {
            mkdir -p "$APPDIR/usr/share/omc"
            cp -r "$OM_EXTRACT_DIR/usr/share/omc/"* "$APPDIR/usr/share/omc/" 2>/dev/null || true
        }
        
        # Copy Modelica standard library (from usr/share/omlibrary in the package)
        [ -d "$OM_EXTRACT_DIR/usr/share/omlibrary" ] && {
            mkdir -p "$APPDIR/usr/lib/omlibrary"
            cp -r "$OM_EXTRACT_DIR/usr/share/omlibrary/"* "$APPDIR/usr/lib/omlibrary/" 2>/dev/null || true
            
            # Extract the Modelica library zip files and create symlinks for direct access
            if [ -d "$APPDIR/usr/lib/omlibrary/cache" ]; then
                mkdir -p "$APPDIR/usr/lib/omlibrary/extracted"
                cd "$APPDIR/usr/lib/omlibrary/cache"
                for zipfile in *.zip; do
                    [ -f "$zipfile" ] && unzip -qo "$zipfile" -d "$APPDIR/usr/lib/omlibrary/extracted/" 2>/dev/null || true
                done
                cd "$APPDIR/usr/lib/omlibrary"
                # Create symlinks for the Modelica 4.0 library (most common)
                for extracted_dir in extracted/OpenModelica-ModelicaStandardLibrary-*/; do
                    [ -d "${extracted_dir}Modelica" ] && [ ! -e "Modelica" ] && ln -sf "${extracted_dir}Modelica" Modelica
                    [ -f "${extracted_dir}Complex.mo" ] && [ ! -e "Complex.mo" ] && ln -sf "${extracted_dir}Complex.mo" Complex.mo
                    [ -d "${extracted_dir}ModelicaServices" ] && [ ! -e "ModelicaServices" ] && ln -sf "${extracted_dir}ModelicaServices" ModelicaServices
                    [ -d "${extracted_dir}ModelicaReference" ] && [ ! -e "ModelicaReference" ] && ln -sf "${extracted_dir}ModelicaReference" ModelicaReference
                    break  # Use first matching directory
                done
                cd "$DL"
            fi
        }
        # Also check older location (usr/lib/omlibrary)
        [ -d "$OM_EXTRACT_DIR/usr/lib/omlibrary" ] && {
            mkdir -p "$APPDIR/usr/lib/omlibrary"
            cp -r "$OM_EXTRACT_DIR/usr/lib/omlibrary/"* "$APPDIR/usr/lib/omlibrary/" 2>/dev/null || true
        }
        
        # Create OpenModelica wrapper script
        cat > "$APPDIR/usr/bin/omc-wrapper" << 'OMCWRAPPER'
#!/bin/bash
# OpenModelica wrapper for eSim AppImage
SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
HERE="$(dirname "$(dirname "$SCRIPT_DIR")")"

export OPENMODELICAHOME="$HERE/usr"
export OPENMODELICALIBRARY="$HERE/usr/lib/omlibrary:$HERE/usr/share/omc/libraries"
# NOTE: Do NOT prepend $HERE/usr/lib here - AppRun already sets up filtered LD_LIBRARY_PATH
# Just add subdirectories that aren't in the main filtered path
export LD_LIBRARY_PATH="$HERE/usr/lib/x86_64-linux-gnu:$HERE/usr/lib/x86_64-linux-gnu/omc:${LD_LIBRARY_PATH}"
export LIBRARY_PATH="$HERE/usr/lib/x86_64-linux-gnu:$HERE/usr/lib/x86_64-linux-gnu/omc:${LIBRARY_PATH}"
export PATH="$HERE/usr/bin:$PATH"

exec "$HERE/usr/bin/omc" "$@"
OMCWRAPPER
        chmod +x "$APPDIR/usr/bin/omc-wrapper"
        
        # Create OMEdit wrapper script that sets up library paths
        if [ -f "$APPDIR/usr/bin/OMEdit" ]; then
            mv "$APPDIR/usr/bin/OMEdit" "$APPDIR/usr/bin/OMEdit.bin"
            cat > "$APPDIR/usr/bin/OMEdit" << 'OMEDITWRAPPER'
#!/bin/bash
# OMEdit wrapper for eSim AppImage - sets up library paths
SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
HERE="$(dirname "$(dirname "$SCRIPT_DIR")")"

export OPENMODELICAHOME="$HERE/usr"
export OPENMODELICALIBRARY="$HERE/usr/lib/omlibrary:$HERE/usr/share/omc/libraries"
# NOTE: Do NOT prepend $HERE/usr/lib here - AppRun already sets up filtered LD_LIBRARY_PATH
export LD_LIBRARY_PATH="$HERE/usr/lib/x86_64-linux-gnu:$HERE/usr/lib/x86_64-linux-gnu/omc:${LD_LIBRARY_PATH}"
export LIBRARY_PATH="$HERE/usr/lib/x86_64-linux-gnu:$HERE/usr/lib/x86_64-linux-gnu/omc:${LIBRARY_PATH}"
export PATH="$HERE/usr/bin:$PATH"
export QT_QPA_PLATFORM_PLUGIN_PATH="$HERE/usr/lib/qt5/plugins/platforms:${QT_QPA_PLATFORM_PLUGIN_PATH}"

# Use gcc instead of clang for compilation (clang may not be installed)
export CC=gcc
export CXX=g++

exec "$SCRIPT_DIR/OMEdit.bin" "$@"
OMEDITWRAPPER
            chmod +x "$APPDIR/usr/bin/OMEdit"
        fi
        
        # Count what was bundled
        omc_bin_count=$(ls -1 "$APPDIR/usr/bin/omc"* "$APPDIR/usr/bin/OMEdit"* 2>/dev/null | wc -l || echo "0")
        omedit_libs=$(ls -1 "$APPDIR/usr/lib/libosg"* "$APPDIR/usr/lib/libQt5WebKit"* 2>/dev/null | wc -l || echo "0")
        ok "OpenModelica bundled: $omc_bin_count binaries, $omedit_libs OMEdit libs"
    else
        warn "OpenModelica extraction failed - will use system OMC if available"
    fi
    
    # Bundle library dependencies for ngspice and ghdl
    for bin in "$APPDIR/usr/bin/ngspice" "$APPDIR/usr/bin/ghdl"; do
        [ -x "$bin" ] || continue
        while IFS= read -r lib; do
            [ -n "$lib" ] && [ -f "$lib" ] && [ ! -f "$APPDIR/usr/lib/$(basename "$lib")" ] && {
                cp -L "$lib" "$APPDIR/usr/lib/" 2>/dev/null || true
            }
        done < <(ldd "$bin" 2>/dev/null | grep "=>" | awk '{print $3}' | grep -v "^$" || true)
    done
    
    # ═══ CREATE NGHDL WRAPPER SCRIPT ═══
    progress "Creating NGHDL wrapper script..."
    cat > "$APPDIR/usr/bin/nghdl" << 'NGHDLWRAPPER'
#!/bin/bash
# NGHDL launcher wrapper for eSim AppImage
# Sets up proper paths for GHDL/Verilator mixed-signal simulation

SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
HERE="$(dirname "$(dirname "$SCRIPT_DIR")")"

export APPDIR="$HERE"
export NGHDL_HOME="$HERE/usr/share/eSim/nghdl"
export PATH="$HERE/usr/bin:$PATH"
# NOTE: Do NOT prepend $HERE/usr/lib here - AppRun already sets up filtered LD_LIBRARY_PATH
export LD_LIBRARY_PATH="$HERE/lib/x86_64-linux-gnu:${LD_LIBRARY_PATH}"

# Dynamic Python version detection for multi-distro support
_PYVER=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")' 2>/dev/null || echo "3.10")
_BUNDLED_SITE=""
for _pv in $_PYVER 3.13 3.12 3.11 3.10 3.9 3.8; do
    [ -d "$HERE/usr/lib/python$_pv/site-packages" ] && _BUNDLED_SITE="$HERE/usr/lib/python$_pv/site-packages" && break
done
export PYTHONPATH="$HERE/usr/share/eSim/src:$_BUNDLED_SITE:$NGHDL_HOME/src:${PYTHONPATH}"

# ═══ GTK SETTINGS TO SUPPRESS WARNINGS ═══
export GTK_MODULES=""
export GTK3_MODULES=""
export GTK_THEME=Adwaita

# Set compiler paths
export GHDL="$HERE/usr/bin/ghdl"
export VERILATOR="$HERE/usr/bin/verilator"
# GHDL_PREFIX must point to the vhdl directory containing ieee/v93 for ghdl-llvm
export GHDL_PREFIX="$HERE/usr/lib/ghdl/llvm/vhdl"

# Create NGHDL config directory if needed
NGHDL_CONFIG_DIR="$HOME/.nghdl"
mkdir -p "$NGHDL_CONFIG_DIR"

SIMULATOR_ROOT="$HOME/nghdl-simulator"

# Extract simulator source if missing (tar.xz is inside nghdl folder)
# Check for configure script, not just icm directory (which may be created empty)
if [ ! -f "$SIMULATOR_ROOT/configure" ]; then
    echo "Extracting NGHDL simulator source to $SIMULATOR_ROOT..."
    rm -rf "$SIMULATOR_ROOT" 2>/dev/null || true
    mkdir -p "$SIMULATOR_ROOT"
    tar -xJf "$HERE/usr/share/eSim/nghdl/nghdl-simulator-source.tar.xz" -C "$HOME" 2>/dev/null || true
    if [ -d "$HOME/nghdl-simulator-source" ]; then
        cp -r "$HOME/nghdl-simulator-source"/* "$SIMULATOR_ROOT/" 2>/dev/null || true
        rm -rf "$HOME/nghdl-simulator-source"
        echo "[eSim] ✓ NGHDL simulator source extracted"
    fi
fi

# GCC 15+ (Fedora 43+) defaults to gnu23 which breaks ngspice-35 C code (bool keyword conflict)
_NGSPICE_CFLAGS=""
if command -v gcc >/dev/null 2>&1 && gcc -dumpversion 2>/dev/null | awk -F. '{exit ($1 >= 14) ? 0 : 1}'; then
    _NGSPICE_CFLAGS="-std=gnu17 -Wno-error=incompatible-pointer-types -Wno-error=int-conversion -Wno-error=implicit-function-declaration"
    export CFLAGS="$_NGSPICE_CFLAGS"
fi

# Configure nghdl-simulator to generate Makefiles if not already done
# Use --prefix to install code models to user-writable location instead of /usr/local
if [ -f "$SIMULATOR_ROOT/configure" ] && [ ! -f "$SIMULATOR_ROOT/src/xspice/icm/GNUmakefile" ]; then
    echo "Configuring NGHDL simulator (generating Makefiles)..."
    cd "$SIMULATOR_ROOT"
    CFLAGS="$_NGSPICE_CFLAGS" ./configure --with-ngshared --enable-xspice --disable-debug --prefix="$HOME/.nghdl/local" >/dev/null 2>&1 || true
    cd "$HERE"
fi

# Setup cmpp (Code Model PreProcessor) - REQUIRED for ICM compilation
# First try to use bundled cmpp binary, then fallback to building from source
CMPP_PATH="$SIMULATOR_ROOT/src/xspice/cmpp"
BUNDLED_CMPP="$HERE/usr/share/eSim/nghdl/bin/cmpp"

if [ -d "$CMPP_PATH" ] && [ ! -x "$CMPP_PATH/cmpp" ]; then
    if [ -x "$BUNDLED_CMPP" ]; then
        # Use bundled cmpp binary
        echo "[eSim] Installing bundled cmpp binary..."
        cp "$BUNDLED_CMPP" "$CMPP_PATH/cmpp"
        chmod +x "$CMPP_PATH/cmpp"
        echo "[eSim] ✓ cmpp installed from bundled binary"
    else
        # Fallback: try to build from source (requires build tools)
        echo "[eSim] Building cmpp from source (requires build-essential)..."
        cd "$CMPP_PATH"
        # Run autoreconf if needed to fix timestamp issues
        if command -v autoreconf >/dev/null 2>&1; then
            (cd "$SIMULATOR_ROOT" && autoreconf -fi >/dev/null 2>&1) || true
            (cd "$SIMULATOR_ROOT" && CFLAGS="$_NGSPICE_CFLAGS" ./configure --with-ngshared --enable-xspice --disable-debug --prefix="$HOME/.nghdl/local" >/dev/null 2>&1) || true
        fi
        CFLAGS="$_NGSPICE_CFLAGS" make >/dev/null 2>&1 || {
            echo "[eSim] Note: cmpp build failed."
            echo "[eSim]       Install build-essential and automake for full NGHDL support."
        }
        cd "$HERE"
    fi
fi

# Create the installation directory for code models (required by make install)
# ═══ SETUP NGVERI VERILATED OBJECTS ═══
# The Ngveri code model needs verilated_threads.o and verilated.o for Verilator support
# Distro-agnostic compilation strategy: compile from system Verilator at build/runtime
NGVERI_ICM_DIR="$SIMULATOR_ROOT/src/xspice/icm/Ngveri"

# Create the directory if it doesn't exist
mkdir -p "$NGVERI_ICM_DIR" 2>/dev/null || true

# Function: Compile verilated objects for current system (distro-agnostic)
_compile_verilated_system() {
    local OBJECT_NAME="$1"
    local CPP_FILE="$2"
    local OUTPUT_FILE="$3"
    
    [ -f "$CPP_FILE" ] || return 1
    
    echo "[eSim] Compiling $OBJECT_NAME from Verilator sources..."
    
    # Verify C++ compiler and standard library are available
    if ! command -v g++ >/dev/null 2>&1; then
        echo "[eSim] ✗ C++ compiler (g++) not found"
        echo "[eSim]    Install: $SUDO dnf install gcc-c++"
        return 1
    fi
    
    # Check for C++ standard library headers
    if [ ! -d "/usr/include/c++" ]; then
        echo "[eSim] ⚠ C++ standard library headers not found"
        echo "[eSim]   Installing: libstdc++-devel..."
        $SUDO $PKG_MANAGER install -y libstdc++-devel 2>&1 | tail -1 || true
        if [ ! -d "/usr/include/c++" ]; then
            echo "[eSim] ✗ C++ standard library still not available"
            return 1
        fi
    fi
    
    # Detect GCC C++ include paths dynamically
    local GXX_INCLUDE_DIRS=""
    for dir in /usr/include/c++/*; do
        if [ -d "$dir" ]; then
            GXX_INCLUDE_DIRS="-I$dir"
            break
        fi
    done
    for dir in /usr/include/x86_64-linux-gnu/c++/*; do
        if [ -d "$dir" ]; then
            GXX_INCLUDE_DIRS="$GXX_INCLUDE_DIRS -I$dir"
            break
        fi
    done
    
    # Verify Verilator development files exist
    if [ ! -f "/usr/share/verilator/include/verilated.h" ]; then
        echo "[eSim] ✗ Verilator development files not found at /usr/share/verilator/include"
        echo "[eSim]    Install verilator-devel: $SUDO dnf install verilator-devel"
        return 1
    fi
    
    # Compile with comprehensive flags for Fedora/NGHDL compatibility
    local COMPILE_FLAGS="-c -O2 -fPIC -pthread -std=c++14 -DVL_THREADED -fno-lto"
    
    if g++ $COMPILE_FLAGS \
        $GXX_INCLUDE_DIRS \
        -I/usr/share/verilator/include \
        "$CPP_FILE" -o "$OUTPUT_FILE" 2>/tmp/esim_build_veri.log; then
        echo "[eSim] ✓ $OBJECT_NAME compiled successfully"
        return 0
    else
        echo "[eSim] ✗ Failed to compile $OBJECT_NAME"
        if [ -f /tmp/esim_build_veri.log ]; then
            echo "[eSim] Compilation error log:"
            sed 's/^/     /' /tmp/esim_build_veri.log | head -15
        fi
        return 1
    fi
}

# ═══ COMPILE VERILATED OBJECTS FOR NGVERI ═══
# Verify Verilator is available
if ! command -v verilator >/dev/null 2>&1; then
    warn "Verilator not found. Installing..."
    $SUDO $PKG_MANAGER install -y verilator verilator-devel 2>&1 | tail -1 || die "Verilator installation failed"
fi

echo "[eSim] Setting up Ngveri with Verilator support..."

# Compile verilated objects at build time
if [ -d /usr/share/verilator/include ]; then
    # Compile verilated.cpp
    if [ ! -f "$NGVERI_ICM_DIR/verilated.o" ]; then
        _compile_verilated_system "verilated.o" "/usr/share/verilator/include/verilated.cpp" "$NGVERI_ICM_DIR/verilated.o" || \
            warn "Failed to compile verilated.o - will try at link time"
    fi
    
    # Compile verilated_threads.cpp
    if [ ! -f "$NGVERI_ICM_DIR/verilated_threads.o" ]; then
        _compile_verilated_system "verilated_threads.o" "/usr/share/verilator/include/verilated_threads.cpp" "$NGVERI_ICM_DIR/verilated_threads.o" || \
            warn "Failed to compile verilated_threads.o - will try at link time"
    fi
    
    # Verify compiled objects exist
    if [ -f "$NGVERI_ICM_DIR/verilated.o" ] && [ -f "$NGVERI_ICM_DIR/verilated_threads.o" ]; then
        echo "[eSim] ✓ Verilated objects compiled and ready for linking"
    else
        echo "[eSim] ⚠ Some verilated objects were not compiled"
    fi
else
    warn "Verilator development files not found at /usr/share/verilator/include"
    warn "Try: $SUDO $PKG_MANAGER install verilator-devel"
fi

# ═══ UPDATE GHDLMAKEFILE FOR NGVERI BUILD ═══
# Include ghdl and Ngveri in the CMDIRS list
echo "[eSim] Configuring GNUmakefile for ghdl and Ngveri codemodels..."
ICM_MAKEFILE="$SIMULATOR_ROOT/src/xspice/icm/GNUmakefile.in"

if [ -f "$ICM_MAKEFILE" ]; then
    # Add ghdl and Ngveri to CMDIRS if not already present
    if ! grep -q "ghdl" "$ICM_MAKEFILE"; then
        echo "[eSim] Adding ghdl to CMDIRS..."
        sed -i 's/CMDIRS = spice2poly digital analog xtradev xtraevt table/CMDIRS = spice2poly digital analog xtradev xtraevt table ghdl Ngveri/' "$ICM_MAKEFILE"
        echo "[eSim] ✓ CMDIRS updated with ghdl and Ngveri"
    fi
fi

# Also update the generated GNUmakefile if it exists
ICM_MAKEFILE_BUILT="$SIMULATOR_ROOT/src/xspice/icm/GNUmakefile"
if [ -f "$ICM_MAKEFILE_BUILT" ]; then
    if ! grep -q "ghdl" "$ICM_MAKEFILE_BUILT"; then
        echo "[eSim] Adding ghdl to built GNUmakefile CMDIRS..."
        sed -i 's/CMDIRS = spice2poly digital analog xtradev xtraevt table/CMDIRS = spice2poly digital analog xtradev xtraevt table ghdl Ngveri/' "$ICM_MAKEFILE_BUILT"
    fi
    
    # Ensure verilated objects are linked into Ngveri.cm
    if [ -f "$NGVERI_ICM_DIR/verilated.o" ] || [ -f "$NGVERI_ICM_DIR/verilated_threads.o" ]; then
        echo "[eSim] Configuring Ngveri linker to include verilated objects..."
        # Add verilated objects to Ngveri link line in GNUmakefile
        if ! grep -q "Ngveri/verilated" "$ICM_MAKEFILE_BUILT"; then
            # Find the Ngveri linking rule and add verilated objects
            sed -i '/^ifdef cm/,/^endif/{/Ngveri.*\.cm/s|$| Ngveri/verilated.o Ngveri/verilated_threads.o|}' "$ICM_MAKEFILE_BUILT" 2>/dev/null || true
        fi
    fi
fi

echo "[eSim] ✓ Ngveri/GHDL codemodel build configured"

# Generate config.ini with runtime paths including SRC section
cat > "$NGHDL_CONFIG_DIR/config.ini" << EOF
[NGHDL]
NGHDL_HOME = $HOME/nghdl-simulator
DIGITAL_MODEL = $HOME/nghdl-simulator/src/xspice/icm
RELEASE = $HOME/nghdl-simulator

[SRC]
SRC_HOME = $HERE/usr/share/eSim/nghdl
LICENSE = $NGHDL_HOME/LICENSE

[COMPILER]
GHDL = $GHDL
VERILATOR = $VERILATOR
GHDL_PREFIX = $GHDL_PREFIX
MODEL_COMPILER = $GHDL
EOF

# Create simulator directory structure and required files
# NgVeri.py expects: DIGITAL_MODEL/Ngveri/modpath.lst where DIGITAL_MODEL = icm
# NGHDL expects: icm/ghdl/modpath.lst for VHDL models
mkdir -p "$HOME/nghdl-simulator/src/xspice/icm/Ngveri"
mkdir -p "$HOME/nghdl-simulator/src/xspice/icm/ghdl"
mkdir -p "$HOME/nghdl-simulator/src/ghdlserver"

# Create proper modpath.lst files for Ngveri and ghdl codemodels
# These files are required by the cmpp preprocessor
cat > "$HOME/nghdl-simulator/src/xspice/icm/Ngveri/modpath.lst" << 'MODPATH_NGVERI'
MODPATH_NGVERI

cat > "$HOME/nghdl-simulator/src/xspice/icm/Ngveri/udnpath.lst" << 'UDNPATH_NGVERI'
UDNPATH_NGVERI

cat > "$HOME/nghdl-simulator/src/xspice/icm/ghdl/modpath.lst" << 'MODPATH_GHDL'
MODPATH_GHDL

cat > "$HOME/nghdl-simulator/src/xspice/icm/ghdl/udnpath.lst" << 'UDNPATH_GHDL'
UDNPATH_GHDL

echo \"[eSim] ✓ Created modpath.lst and udnpath.lst for Ngveri and ghdl codemodels\"

# Copy ghdlserver source files needed by NGHDL for model generation
# Path in code: os.path.join(self.home, self.src_home) + "/src/ghdlserver/"
# So with SRC_HOME = $HOME/nghdl-simulator, path becomes: ~/nghdl-simulator/src/ghdlserver/
GHDLSERVER_SRC="$NGHDL_HOME/src/ghdlserver"
if [ -d "$GHDLSERVER_SRC" ]; then
    cp -f "$GHDLSERVER_SRC/compile.sh" "$HOME/nghdl-simulator/src/ghdlserver/" 2>/dev/null || true
    cp -f "$GHDLSERVER_SRC/uthash.h" "$HOME/nghdl-simulator/src/ghdlserver/" 2>/dev/null || true
    cp -f "$GHDLSERVER_SRC/ghdlserver.c" "$HOME/nghdl-simulator/src/ghdlserver/" 2>/dev/null || true
    cp -f "$GHDLSERVER_SRC/ghdlserver.h" "$HOME/nghdl-simulator/src/ghdlserver/" 2>/dev/null || true
    cp -f "$GHDLSERVER_SRC/Utility_Package.vhdl" "$HOME/nghdl-simulator/src/ghdlserver/" 2>/dev/null || true
    cp -f "$GHDLSERVER_SRC/Vhpi_Package.vhdl" "$HOME/nghdl-simulator/src/ghdlserver/" 2>/dev/null || true
fi

# ═══ CONFIGURE VERILATOR FOR NGVERI ═══
echo "[eSim] Verifying Verilator configuration for Ngveri..."
VERILATOR_BIN=$(command -v verilator 2>/dev/null || echo "/usr/bin/verilator")

if [ ! -x "$VERILATOR_BIN" ]; then
    die "Verilator not found. Installation failed. Try: $SUDO $PKG_MANAGER install verilator verilator-devel"
fi

# Copy Verilator include files to nghdl-simulator for Ngveri build
mkdir -p "$HOME/nghdl-simulator/verilator-includes"
if [ -d /usr/share/verilator/include ]; then
    cp -r /usr/share/verilator/include/* "$HOME/nghdl-simulator/verilator-includes/" 2>/dev/null || true
    echo "[eSim] ✓ Verilator include files copied to nghdl-simulator"
fi

# ═══ SETUP MAKERCHIP FOR HDL SIMULATION ═══
echo "[eSim] Configuring Makerchip environment with cross-distro compatibility..."
MAKERCHIP_CONFIG="$HOME/.makerchip"
mkdir -p "$MAKERCHIP_CONFIG"
mkdir -p "$MAKERCHIP_CONFIG/work"
mkdir -p "$MAKERCHIP_CONFIG/build"

# Auto-detect tool paths (distro-independent)
VERILATOR_BIN=$(command -v verilator 2>/dev/null || echo "/usr/bin/verilator")
VERILATOR_INCLUDE=$(find /usr/share -name "verilated.h" 2>/dev/null | head -1 | xargs dirname 2>/dev/null || echo "/usr/share/verilator/include")
VERILATOR_LIB=$(find /usr -path "*/verilator/lib" 2>/dev/null | head -1 || echo "/usr/share/verilator/lib")
GHDL_BIN=$(command -v ghdl 2>/dev/null || echo "/usr/bin/ghdl")
YOSYS_BIN=$(command -v yosys 2>/dev/null || echo "/usr/bin/yosys")
IVERILOG_BIN=$(command -v iverilog 2>/dev/null || echo "/usr/bin/iverilog")
GTKWAVE_BIN=$(command -v gtkwave 2>/dev/null || echo "/usr/bin/gtkwave")

# Create comprehensive Makerchip configuration file with auto-detected paths
cat > "$MAKERCHIP_CONFIG/config.ini" << MAKERCHIP_CONFIG
[system]
; Detected Linux distribution and distro family
distro = $DISTRO
distro_family = $DISTRO_FAMILY
distro_version = $DISTRO_VERSION

[tools]
; Auto-detected tool paths (will fall back to defaults if not found)
verilator_bin = $VERILATOR_BIN
ghdl_bin = $GHDL_BIN
yosys_bin = $YOSYS_BIN
iverilog_bin = $IVERILOG_BIN
gtkwave_bin = $GTKWAVE_BIN
nodejs_bin = \$(command -v node 2>/dev/null || echo "/usr/bin/node")

[verilator]
; Path to verilator executable
verilator_bin = $VERILATOR_BIN
; Verilator include directory (auto-detected)
verilator_include = $VERILATOR_INCLUDE
; Verilator library directory (for precompiled objects)
verilator_lib = $VERILATOR_LIB
; Verilator C++ compilation flags
verilator_flags = -DVL_THREADED -fPIC -std=c++14

[ghdl]
; Path to GHDL executable
ghdl_bin = $GHDL_BIN
; GHDL synthesis backend (llvm or mcode)
; Auto-detection: if ghdl-llvm installed use llvm, else use mcode
ghdl_backend = llvm
; GHDL flags for VHDL synthesis
ghdl_flags = --ieee=synopsys --warn-default-binding

[synthesis]
; Yosys for Verilog synthesis
yosys_bin = $YOSYS_BIN
; Iverilog for Verilog simulation
iverilog_bin = $IVERILOG_BIN
; GTKWave for waveform viewing
gtkwave_bin = $GTKWAVE_BIN

[makerchip]
; Working directory for Makerchip projects
work_dir = \$HOME/.makerchip/work
; Temporary build directory
build_dir = \$HOME/.makerchip/build
; Cache directory for compiled modules
cache_dir = \$HOME/.makerchip/cache
; Distro-specific build flags
build_flags = -fPIC -O2 -Wall

[ngveri]
; Ngveri codemodel path
ngveri_path = \$HOME/nghdl-simulator/src/xspice/icm/Ngveri
; Ngveri module path list
ngveri_modpath = \$HOME/nghdl-simulator/src/xspice/icm/Ngveri/modpath.lst
; Verilated object directory
verilated_objs = \$HOME/nghdl-simulator/src/xspice/icm/Ngveri
; Verilator include paths
verilator_includes = $VERILATOR_INCLUDE

[nghdl]
; NGHDL simulator home
nghdl_home = \$HOME/nghdl-simulator
; NGHDL source directory
nghdl_src = \$HOME/nghdl-simulator/src
; GHDL codemodel path
ghdl_path = \$HOME/nghdl-simulator/src/xspice/icm/ghdl
; GHDL module path list
ghdl_modpath = \$HOME/nghdl-simulator/src/xspice/icm/ghdl/modpath.lst
MAKERCHIP_CONFIG

echo "[eSim] ✓ Makerchip configuration created at $MAKERCHIP_CONFIG"

# Validate and create symlinks for Makerchip tools (cross-distro compatible)
echo "[eSim] Validating Makerchip tools availability across distros..."
USER_BIN="$HOME/.local/bin"
mkdir -p "$USER_BIN"

# Tool validation function
_link_tool() {
    local tool_name="$1"
    local tool_path="$(command -v "$tool_name" 2>/dev/null)"
    if [ -n "$tool_path" ]; then
        ln -sf "$tool_path" "$USER_BIN/$tool_name" 2>/dev/null || true
        echo "[eSim] ✓ $tool_name linked to $USER_BIN/$tool_name"
    else
        echo "[eSim] ⚠ $tool_name not found (optional: install for full Makerchip support)"
    fi
}

# Create symlinks for available Makerchip tools
for tool in verilator ghdl yosys iverilog gtkwave node npm perl; do
    _link_tool "$tool"
done

# Ensure $USER_BIN is in PATH for user shell (all shell types)
for rc_file in "$HOME/.bashrc" "$HOME/.zshrc" "$HOME/.kshrc"; do
    if [ -f "$rc_file" ] && ! grep -q "\.local/bin" "$rc_file" 2>/dev/null; then
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$rc_file"
    fi
done

echo "[eSim] ✓ Makerchip tools configured and symlinked to $USER_BIN"

# Summary of cross-distro configurations
echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║ NGHDL/Makerchip Configuration Summary                      ║"
echo "║ (Cross-Distro Compatible)                                  ║"
echo "╠════════════════════════════════════════════════════════════╣"
echo "║ Distro:      $DISTRO_NAME"
echo "║ Family:      $DISTRO_FAMILY"
echo "║ GHDL:        $GHDL_BIN"
echo "║ Verilator:   $VERILATOR_BIN"
echo "║ Yosys:       $YOSYS_BIN"
echo "║ Iverilog:    $IVERILOG_BIN"
echo "║ NGHDL Home:  $SIMULATOR_ROOT"
echo "║ Ngveri:      $NGVERI_ICM_DIR"
echo "║ Makerchip:   $MAKERCHIP_CONFIG"
echo "║ Config:      $NGHDL_CONFIG_DIR/config.ini"
echo "║ Tools PATH:  $USER_BIN"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Check for -e flag (edit mode) to launch GUI
if [ "$1" = "-e" ]; then
    # Launch the NGHDL GUI through Python with proper display
    echo "Launching NGHDL Model Editor..."
    cd "$NGHDL_HOME/src"
    # Use the correct class name: Mainwindow (not MainWindow)
    exec python3 -c "
import sys
sys.path.insert(0, '$NGHDL_HOME/src')
from PyQt5 import QtWidgets
from ngspice_ghdl import Mainwindow
app = QtWidgets.QApplication(sys.argv)
mw = Mainwindow()
mw.show()
sys.exit(app.exec_())
" 2>&1
else
    # Run ngspice_ghdl for command-line mode
    cd "$NGHDL_HOME/src"
    exec python3 "$NGHDL_HOME/src/ngspice_ghdl.py" "$@"
fi
NGHDLWRAPPER
    chmod +x "$APPDIR/usr/bin/nghdl"
    ok "NGHDL wrapper script created"
    
    ok "Downloads and NgSpice/NGHDL bundling complete"
}


prepare_esim() {
    step 5 "Preparing eSim"
    cd "$DL"
    progress "Extracting..."
    unzip -qo eSim.zip
    
    # Detect Python version dynamically
    PYVER=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
    PYVER_MAJOR=$(python3 -c 'import sys; print(sys.version_info.major)')
    progress "Using Python $PYVER for virtual environment"
    
    # Create virtual environment
    python3 -m venv "$BUILD/venv" || {
        # Try alternative venv creation for some distros
        progress "Trying alternative venv creation..."
        python3 -m virtualenv "$BUILD/venv" 2>/dev/null || \
        virtualenv -p python3 "$BUILD/venv" 2>/dev/null || \
        die "Failed to create Python virtual environment"
    }
    source "$BUILD/venv/bin/activate"
    
    # Upgrade pip and install dependencies
    pip install -q --upgrade pip setuptools wheel 2>&1 | tail -2
    
    # Install Python dependencies - these will be bundled in AppImage
    # Using --no-cache-dir to ensure clean install
    progress "Installing Python dependencies..."
    pip install -q --no-cache-dir numpy scipy matplotlib lxml watchdog 2>&1 | tail -2
    
    # makerchip-app and sandpiper-saas are optional (for Makerchip integration)
    pip install -q --no-cache-dir makerchip-app sandpiper-saas 2>&1 | tail -2 || \
        warn "makerchip-app/sandpiper-saas installation failed (optional)"
    
    # Clone and install hdlparse
    if [ ! -d hdlparse ]; then
        git clone --quiet https://github.com/kevinpt/hdlparse.git
    fi
    
    # Find the correct site-packages directory
    SITE_PACKAGES=$(python3 -c "import site; print(site.getsitepackages()[0])" 2>/dev/null || \
                   echo "$BUILD/venv/lib/python${PYVER}/site-packages")
    
    cp -r hdlparse/hdlparse "$SITE_PACKAGES/" 2>/dev/null || \
    cp -r hdlparse/hdlparse "$BUILD/venv/lib/python${PYVER}/site-packages/"
    
    # Fix hdlparse for Python 3 compatibility
    MINILEXER="$SITE_PACKAGES/hdlparse/minilexer.py"
    [ ! -f "$MINILEXER" ] && MINILEXER="$BUILD/venv/lib/python${PYVER}/site-packages/hdlparse/minilexer.py"
    
    if [ -f "$MINILEXER" ]; then
        # Fix Python 2 to Python 3 syntax
        sed -i 's/except \([A-Za-z_][A-Za-z0-9_]*\), \([A-Za-z_][A-Za-z0-9_]*\):/except (\1, \2):/' "$MINILEXER"
        sed -i 's/\.iteritems()/.items()/g; s/\.iterkeys()/.keys()/g; s/\.itervalues()/.values()/g' "$MINILEXER"
    fi
    
    # Create minilexer compatibility module
    mkdir -p "$SITE_PACKAGES/minilexer" 2>/dev/null || \
    mkdir -p "$BUILD/venv/lib/python${PYVER}/site-packages/minilexer"
    
    MINILEXER_INIT="$SITE_PACKAGES/minilexer/__init__.py"
    [ ! -d "$(dirname "$MINILEXER_INIT")" ] && MINILEXER_INIT="$BUILD/venv/lib/python${PYVER}/site-packages/minilexer/__init__.py"
    
    echo 'from hdlparse.minilexer import MiniLexer
__all__ = ["MiniLexer"]' > "$MINILEXER_INIT"
    
    deactivate
    ok "eSim prepared with Python $PYVER"
}

bundle_gtk_resources() {
    step 6 "Bundling GTK resources"
    
    pixbuf_dir=$(pkg-config --variable=gdk_pixbuf_moduledir gdk-pixbuf-2.0 2>/dev/null || echo "/usr/lib/x86_64-linux-gnu/gdk-pixbuf-2.0/2.10.0/loaders")
    mkdir -p "$APPDIR/usr/lib/gdk-pixbuf-2.0/2.10.0/loaders"
    
    if [ -d "$pixbuf_dir" ]; then
        cp "$pixbuf_dir"/*.so "$APPDIR/usr/lib/gdk-pixbuf-2.0/2.10.0/loaders/" 2>/dev/null || true
    fi
    
    cat > "$APPDIR/usr/lib/gdk-pixbuf-2.0/2.10.0/loaders.cache" <<'EOF'
# GdkPixbuf Image Loader Modules file
EOF
    
    for loader in "$APPDIR/usr/lib/gdk-pixbuf-2.0/2.10.0/loaders/"*.so; do
        [ -f "$loader" ] || continue
        case "$(basename "$loader")" in
            *svg*) echo "\"$(basename "$loader")\"
\"svg\" 5 \"gdk-pixbuf\" \"Scalable Vector Graphics\" \"image/svg+xml\" \"\"" >> "$APPDIR/usr/lib/gdk-pixbuf-2.0/2.10.0/loaders.cache" ;;
            *png*) echo "\"$(basename "$loader")\"
\"png\" 5 \"gdk-pixbuf\" \"The PNG image format\" \"image/png\" \"\"" >> "$APPDIR/usr/lib/gdk-pixbuf-2.0/2.10.0/loaders.cache" ;;
        esac
    done
    
    # ═══ BUNDLE GTK3 THEME AND SETTINGS ═══
    progress "Bundling GTK3 Adwaita theme files..."
    mkdir -p "$APPDIR/usr/share/themes/Adwaita/gtk-3.0"
    mkdir -p "$APPDIR/usr/share/gtk-3.0"
    mkdir -p "$APPDIR/etc/gtk-3.0"
    
    # Copy Adwaita GTK3 theme CSS files
    if [ -d "/usr/share/themes/Adwaita/gtk-3.0" ]; then
        cp -r /usr/share/themes/Adwaita/gtk-3.0/* "$APPDIR/usr/share/themes/Adwaita/gtk-3.0/" 2>/dev/null || true
    fi
    
    # Try alternate theme locations
    for theme_dir in "/usr/share/themes/Adwaita" "/usr/share/gnome-themes-extra/themes/Adwaita"; do
        if [ -d "$theme_dir/gtk-3.0" ]; then
            cp -r "$theme_dir/gtk-3.0"/* "$APPDIR/usr/share/themes/Adwaita/gtk-3.0/" 2>/dev/null || true
        fi
    done
    
    # Create GTK3 settings.ini for proper widget rendering
    cat > "$APPDIR/etc/gtk-3.0/settings.ini" << 'GTKSETTINGS'
[Settings]
gtk-theme-name=Adwaita
gtk-icon-theme-name=Adwaita
gtk-fallback-icon-theme=hicolor
gtk-font-name=Sans 10
gtk-cursor-theme-name=Adwaita
gtk-cursor-theme-size=24
gtk-toolbar-style=GTK_TOOLBAR_BOTH_HORIZ
gtk-toolbar-icon-size=GTK_ICON_SIZE_LARGE_TOOLBAR
gtk-button-images=1
gtk-menu-images=1
gtk-enable-event-sounds=0
gtk-enable-input-feedback-sounds=0
gtk-xft-antialias=1
gtk-xft-hinting=1
gtk-xft-hintstyle=hintslight
gtk-xft-rgba=rgb
gtk-application-prefer-dark-theme=0
GTKSETTINGS
    
    # Bundle hicolor icons
    mkdir -p "$APPDIR/usr/share/icons/hicolor" "$APPDIR/usr/share/icons/Adwaita"
    for size in 16x16 22x22 24x24 32x32 48x48 64x64 96x96 128x128 256x256 scalable; do
        [ -d "/usr/share/icons/hicolor/$size/apps" ] && {
            mkdir -p "$APPDIR/usr/share/icons/hicolor/$size"
            cp -r "/usr/share/icons/hicolor/$size/apps" "$APPDIR/usr/share/icons/hicolor/$size/" 2>/dev/null || true
        }
    done
    # Create proper index.theme with Size fields (required for GTK checkboxes)
    cat > "$APPDIR/usr/share/icons/hicolor/index.theme" << 'ICONTHEME'
[Icon Theme]
Name=Hicolor
Comment=Fallback icon theme
Directories=16x16/apps,22x22/apps,24x24/apps,32x32/apps,48x48/apps,scalable/apps,16x16/actions,22x22/actions,24x24/actions,32x32/actions,48x48/actions,scalable/actions,16x16/status,22x22/status,24x24/status,32x32/status,48x48/status,scalable/status

[16x16/apps]
Size=16
Context=Applications
Type=Threshold

[22x22/apps]
Size=22
Context=Applications
Type=Threshold

[24x24/apps]
Size=24
Context=Applications
Type=Threshold

[32x32/apps]
Size=32
Context=Applications
Type=Threshold

[48x48/apps]
Size=48
Context=Applications
Type=Threshold

[scalable/apps]
Size=64
Context=Applications
Type=Scalable
MinSize=16
MaxSize=256

[16x16/actions]
Size=16
Context=Actions
Type=Threshold

[22x22/actions]
Size=22
Context=Actions
Type=Threshold

[24x24/actions]
Size=24
Context=Actions
Type=Threshold

[32x32/actions]
Size=32
Context=Actions
Type=Threshold

[48x48/actions]
Size=48
Context=Actions
Type=Threshold

[scalable/actions]
Size=64
Context=Actions
Type=Scalable
MinSize=16
MaxSize=256

[16x16/status]
Size=16
Context=Status
Type=Threshold

[22x22/status]
Size=22
Context=Status
Type=Threshold

[24x24/status]
Size=24
Context=Status
Type=Threshold

[32x32/status]
Size=32
Context=Status
Type=Threshold

[48x48/status]
Size=48
Context=Status
Type=Threshold

[scalable/status]
Size=64
Context=Status
Type=Scalable
MinSize=16
MaxSize=256
ICONTHEME
    
    # Also copy the actions and status directories for checkbox/toggle icons
    for size in 16x16 22x22 24x24 32x32 48x48 scalable; do
        for context in actions status; do
            [ -d "/usr/share/icons/hicolor/$size/$context" ] && {
                mkdir -p "$APPDIR/usr/share/icons/hicolor/$size"
                cp -r "/usr/share/icons/hicolor/$size/$context" "$APPDIR/usr/share/icons/hicolor/$size/" 2>/dev/null || true
            }
        done
    done
    
    # ═══ BUNDLE COMPLETE ADWAITA ICON THEME ═══
    progress "Bundling complete Adwaita icon theme for checkbox visibility..."
    # Copy ALL Adwaita icon sizes (not just symbolic) for proper checkbox rendering
    for size in 16x16 22x22 24x24 32x32 48x48 64x64 96x96 256x256 scalable symbolic; do
        if [ -d "/usr/share/icons/Adwaita/$size" ]; then
            mkdir -p "$APPDIR/usr/share/icons/Adwaita/$size"
            cp -r "/usr/share/icons/Adwaita/$size"/* "$APPDIR/usr/share/icons/Adwaita/$size/" 2>/dev/null || true
        fi
    done
    
    # Copy Adwaita index.theme and cursors
    [ -f "/usr/share/icons/Adwaita/index.theme" ] && {
        cp "/usr/share/icons/Adwaita/index.theme" "$APPDIR/usr/share/icons/Adwaita/" 2>/dev/null || true
    }
    [ -d "/usr/share/icons/Adwaita/cursors" ] && {
        cp -r "/usr/share/icons/Adwaita/cursors" "$APPDIR/usr/share/icons/Adwaita/" 2>/dev/null || true
    }
    
    # Update icon cache (helps GTK find icons faster)
    [ -x "$(command -v gtk-update-icon-cache)" ] && {
        gtk-update-icon-cache "$APPDIR/usr/share/icons/hicolor" 2>/dev/null || true
        gtk-update-icon-cache "$APPDIR/usr/share/icons/Adwaita" 2>/dev/null || true
    }
    
    local adwaita_count=$(find "$APPDIR/usr/share/icons/Adwaita" -name "*.svg" -o -name "*.png" 2>/dev/null | wc -l || echo "0")
    ok "GTK resources bundled with $adwaita_count Adwaita icons"
}


bundle_kicad() {
    step 6.5 "Bundling complete KiCad 6 installation"
    
    # Helper function to bundle library dependencies
    bundle_library_deps() {
        local binary="$1"
        [ ! -f "$binary" ] && return 0
        progress "Bundling dependencies for $(basename "$binary")..."
        
        # Use process substitution to avoid issues with set -e in pipelines
        while IFS= read -r lib; do
            [ -n "$lib" ] && [ -f "$lib" ] && [ ! -f "$APPDIR/usr/lib/$(basename "$lib")" ] && {
                cp -L "$lib" "$APPDIR/usr/lib/" 2>/dev/null || true
            }
        done < <(ldd "$binary" 2>/dev/null | grep "=>" | awk '{print $3}' | grep -v "^$" || true)
        return 0
    }

    
    mkdir -p "$APPDIR/usr/bin" "$APPDIR/usr/lib" "$APPDIR/usr/share/kicad"
    
    # ═══ EXTRACT KICAD 6 FROM APPIMAGE ═══
    local KICAD6_DIR="$DL/kicad6-extracted"
    if [ -f "$DL/kicad6.AppImage" ]; then
        progress "Extracting KiCad 6 AppImage..."
        cd "$DL"
        if [ ! -d "$KICAD6_DIR" ]; then
            ./kicad6.AppImage --appimage-extract 2>/dev/null || true
            mv squashfs-root "$KICAD6_DIR" 2>/dev/null || true
        fi
        
        if [ -d "$KICAD6_DIR" ]; then
            # ═══ BUNDLE KICAD 6 APPIMAGE DIRECTLY ═══
            # Extracted binaries crash due to hardcoded paths, so bundle the AppImage itself
            progress "Bundling KiCad 6 AppImage directly (for stable operation)..."
            mkdir -p "$APPDIR/usr/share/kicad-appimage"
            cp "$DL/kicad6.AppImage" "$APPDIR/usr/share/kicad-appimage/kicad6.AppImage"
            chmod +x "$APPDIR/usr/share/kicad-appimage/kicad6.AppImage"
            
            # Create wrapper scripts for KiCad tools
            progress "Creating KiCad wrapper scripts..."
            for tool in eeschema pcbnew kicad gerbview pcb_calculator pl_editor bitmap2component; do
                cat > "$APPDIR/usr/bin/$tool" <<WRAPPER
#!/bin/bash
# Wrapper to run $tool from bundled KiCad 6 AppImage
SCRIPT_DIR="\$(dirname "\$(readlink -f "\$0")")"
HERE="\$(dirname "\$(dirname "\$SCRIPT_DIR")")"
KICAD_APPIMAGE="\$HERE/usr/share/kicad-appimage/kicad6.AppImage"
ESIM_LIB="\$HERE/usr/share/eSim/library"

# Extract KiCad AppImage to temp if not already done
KICAD_EXTRACT="/tmp/esim-kicad6-\${UID:-\$(id -u)}"
if [ ! -d "\$KICAD_EXTRACT/squashfs-root/usr/bin" ]; then
    mkdir -p "\$KICAD_EXTRACT"
    cd "\$KICAD_EXTRACT"
    "\$KICAD_APPIMAGE" --appimage-extract >/dev/null 2>&1
fi

# NOTE: eSim libraries are now managed by setup_kicad_libs function
# They are kept in ESIM library folder, not copied to KiCad symbols folder
# This prevents duplicate library entries in sym-lib-table

KICAD_ROOT="\$KICAD_EXTRACT/squashfs-root"

# Set up KiCad environment
export LD_LIBRARY_PATH="\$KICAD_ROOT/usr/lib/x86_64-linux-gnu:\$KICAD_ROOT/lib/x86_64-linux-gnu:\$KICAD_ROOT/usr/lib:\$LD_LIBRARY_PATH"
export KICAD6_3DMODEL_DIR="\$KICAD_ROOT/usr/share/kicad/3dmodels"
export KICAD6_FOOTPRINT_DIR="\$KICAD_ROOT/usr/share/kicad/footprints"
export KICAD6_SYMBOL_DIR="\$KICAD_ROOT/usr/share/kicad/symbols"
export KICAD6_TEMPLATE_DIR="\$KICAD_ROOT/usr/share/kicad/template"
unset GTK3_MODULES

# Run the tool
cd "\$KICAD_ROOT/usr"
exec "./bin/$tool" "\$@"
WRAPPER
                chmod +x "$APPDIR/usr/bin/$tool"
            done
            
            # Copy KiCad 6 symbol libraries (still needed for eSim configuration)
            progress "Copying KiCad 6 symbol libraries..."
            if [ -d "$KICAD6_DIR/usr/share/kicad/symbols" ]; then
                mkdir -p "$APPDIR/usr/share/kicad/symbols"
                cp -r "$KICAD6_DIR/usr/share/kicad/symbols"/* "$APPDIR/usr/share/kicad/symbols/" 2>/dev/null || true
            fi
            
            # Copy KiCad 6 footprint libraries
            progress "Copying KiCad 6 footprint libraries..."
            if [ -d "$KICAD6_DIR/usr/share/kicad/footprints" ]; then
                mkdir -p "$APPDIR/usr/share/kicad/footprints"
                cp -r "$KICAD6_DIR/usr/share/kicad/footprints"/* "$APPDIR/usr/share/kicad/footprints/" 2>/dev/null || true
            fi
            
            # Copy KiCad 6 templates
            if [ -d "$KICAD6_DIR/usr/share/kicad/template" ]; then
                mkdir -p "$APPDIR/usr/share/kicad/template"
                cp -r "$KICAD6_DIR/usr/share/kicad/template"/* "$APPDIR/usr/share/kicad/template/" 2>/dev/null || true
            fi
            
            local kicad6_sym_count=$(ls -1 "$APPDIR/usr/share/kicad/symbols"/*.kicad_sym 2>/dev/null | wc -l || echo "0")
            ok "Bundled KiCad 6 AppImage with $kicad6_sym_count symbol libraries"
        else
            die "KiCad 6 extraction failed - squashfs-root not found after extraction"
        fi
    else
        die "KiCad 6 AppImage not found at $DL/kicad6.AppImage"
    fi
    
    # Verify KiCad 6 wrapper was created
    if [ ! -f "$APPDIR/usr/bin/eeschema" ]; then
        die "KiCad 6 eeschema wrapper not found after bundling"
    fi
    ok "KiCad 6 binaries bundled successfully"

    
    # ═══ SKIP KICAD SHARED LIBRARIES - KiCad runs from bundled AppImage ═══
    # KiCad tools now run from bundled kicad6.AppImage with their own libraries
    progress "Skipping KiCad library copying (KiCad runs from bundled AppImage)..."
    ok "KiCad 6 runs from bundled AppImage with own libraries"
    
    # ═══ KEEP SYSTEM PYTHON FOR ESIM ═══
    # Dynamically detect Python version and copy libpython
    progress "Using system Python for eSim..."
    local py_ver=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
    # Try multiple paths for libpython (different distros)
    for libdir in /lib/x86_64-linux-gnu /usr/lib/x86_64-linux-gnu /usr/lib64 /usr/lib; do
        if [ -f "${libdir}/libpython${py_ver}.so.1.0" ]; then
            cp -L "${libdir}/libpython${py_ver}.so"* "$APPDIR/usr/lib/" 2>/dev/null || true
            break
        elif [ -f "${libdir}/libpython${py_ver}.so" ]; then
            cp -L "${libdir}/libpython${py_ver}.so"* "$APPDIR/usr/lib/" 2>/dev/null || true
            break
        fi
    done
    # Also try to copy from standard python paths
    python3 -c "import sysconfig; print(sysconfig.get_config_var('LIBDIR'))" 2>/dev/null | while read libdir; do
        [ -d "$libdir" ] && cp -L "${libdir}/libpython${py_ver}"*.so* "$APPDIR/usr/lib/" 2>/dev/null || true
    done
    
    # ═══ BUNDLE GDK-PIXBUF LOADERS FOR ESIM GUI ═══
    progress "Copying gdk-pixbuf loaders for eSim..."
    # Use system gdk-pixbuf - search multiple paths for different distros
    mkdir -p "$APPDIR/lib/x86_64-linux-gnu/gdk-pixbuf-2.0/2.10.0/loaders"
    mkdir -p "$APPDIR/usr/lib/gdk-pixbuf-2.0/2.10.0/loaders"
    
    # Try to find gdk-pixbuf loaders in different distro paths
    local pixbuf_loaders_found=0
    for pixbuf_base in /usr/lib/x86_64-linux-gnu/gdk-pixbuf-2.0 /usr/lib64/gdk-pixbuf-2.0 /usr/lib/gdk-pixbuf-2.0; do
        if [ -d "${pixbuf_base}/2.10.0/loaders" ]; then
            cp -L "${pixbuf_base}/2.10.0/loaders/"*.so \
                "$APPDIR/lib/x86_64-linux-gnu/gdk-pixbuf-2.0/2.10.0/loaders/" 2>/dev/null || true
            cp -L "${pixbuf_base}/2.10.0/loaders/"*.so \
                "$APPDIR/usr/lib/gdk-pixbuf-2.0/2.10.0/loaders/" 2>/dev/null || true
            # Copy system loaders.cache if it exists
            [ -f "${pixbuf_base}/2.10.0/loaders.cache" ] && {
                cp -L "${pixbuf_base}/2.10.0/loaders.cache" \
                    "$APPDIR/lib/x86_64-linux-gnu/gdk-pixbuf-2.0/2.10.0/" 2>/dev/null || true
                cp -L "${pixbuf_base}/2.10.0/loaders.cache" \
                    "$APPDIR/usr/lib/gdk-pixbuf-2.0/2.10.0/" 2>/dev/null || true
            }
            pixbuf_loaders_found=1
            break
        fi
    done
    
    local loader_count=$(ls -1 "$APPDIR/lib/x86_64-linux-gnu/gdk-pixbuf-2.0/2.10.0/loaders/"*.so 2>/dev/null | wc -l || echo "0")
    ok "Bundled $loader_count gdk-pixbuf loaders for eSim"
    
    local bundled_libs=$(ls -1 "$APPDIR/usr/lib"/*.so* 2>/dev/null | wc -l || echo "0")
    ok "Bundled $bundled_libs libraries (complete GTK stack)"
    
    # ═══ BUNDLE GRAPHICS LIBRARIES ═══
    progress "Copying graphics libraries (OpenGL, GLU, GLEW)..."
    for lib in libGL.so* libGLU.so* libGLEW.so* libglut.so* libGLX.so* libGLdispatch.so*; do
        # Search in multiple distro lib paths
        for libdir in /usr/lib/x86_64-linux-gnu /usr/lib64 /usr/lib; do
            [ -d "$libdir" ] && find "$libdir" -maxdepth 1 -name "$lib" -exec cp -L {} "$APPDIR/usr/lib/" \; 2>/dev/null || true
        done
    done
    
    # ═══ BUNDLE FUSE LIBRARY ═══
    progress "Copying FUSE library..."
    for lib in libfuse.so*; do
        # Search in multiple distro lib paths
        for libdir in /lib/x86_64-linux-gnu /usr/lib/x86_64-linux-gnu /lib64 /usr/lib64 /usr/lib; do
            [ -d "$libdir" ] && find "$libdir" -maxdepth 1 -name "$lib" -exec cp -L {} "$APPDIR/usr/lib/" \; 2>/dev/null || true
        done
    done
    
    # ═══ KICAD SYMBOL/FOOTPRINT LIBRARIES - ALREADY COPIED FROM APPIMAGE ═══
    # The symbol and footprint libraries were copied during AppImage extraction above
    local symbol_count=$(ls -1 "$APPDIR/usr/share/kicad/symbols"/*.kicad_sym 2>/dev/null | wc -l || echo "0")
    local footprint_count=$(ls -1d "$APPDIR/usr/share/kicad/footprints"/*.pretty 2>/dev/null | wc -l || echo "0")
    ok "KiCad 6 libraries: $symbol_count symbol libs, $footprint_count footprint libs"
    
    # ═══ BUNDLE 3D MODEL LIBRARIES FROM KICAD 6 APPIMAGE ═══
    progress "Copying 3D model libraries from KiCad 6..."
    local model_count=0
    if [ -d "$KICAD6_DIR/usr/share/kicad/3dmodels" ]; then
        mkdir -p "$APPDIR/usr/share/kicad/3dmodels"
        # Copy essential 3D models
        for model_dir in Capacitor_SMD.3dshapes Resistor_SMD.3dshapes Connector_PinHeader_2.54mm.3dshapes \
                         LED_SMD.3dshapes Diode_SMD.3dshapes; do
            [ -d "$KICAD6_DIR/usr/share/kicad/3dmodels/$model_dir" ] && {
                cp -r "$KICAD6_DIR/usr/share/kicad/3dmodels/$model_dir" "$APPDIR/usr/share/kicad/3dmodels/" 2>/dev/null || true
                model_count=$((model_count + 1)) || true
            }
        done
    fi
    ok "Copied $model_count 3D model libraries"

    # ═══ BUNDLE KICAD RESOURCES (images.tar.gz, etc.) ═══
    progress "Copying KiCad 6 resources..."
    if [ -d "$KICAD6_DIR/usr/share/kicad/resources" ]; then
        mkdir -p "$APPDIR/usr/share/kicad/resources"
        cp -r "$KICAD6_DIR/usr/share/kicad/resources"/* "$APPDIR/usr/share/kicad/resources/" 2>/dev/null || true
        ok "KiCad resources copied (images.tar.gz, etc.)"
    fi
    
    # ═══ BUNDLE KICAD TEMPLATES FROM APPIMAGE ═══
    progress "Copying KiCad 6 templates..."
    # Already copied during AppImage extraction, just log count
    local template_count=$(ls -1 "$APPDIR/usr/share/kicad/template"/* 2>/dev/null | wc -l || echo "0")
    ok "KiCad 6 templates: $template_count files"
    
    # ═══ BUNDLE FONT FILES ═══
    progress "Copying font files..."
    mkdir -p "$APPDIR/usr/share/fonts"
    cp -r /usr/share/fonts/truetype/dejavu "$APPDIR/usr/share/fonts/" 2>/dev/null || true
    
    # ═══ CREATE FONT CACHE ═══
    if command -v fc-cache >/dev/null 2>&1; then
        fc-cache "$APPDIR/usr/share/fonts" 2>/dev/null || true
    fi
    
    ok "KiCad 6 bundled completely (binaries + $symbol_count symbols + $footprint_count footprints)"
}


install_esim() {
    step 8 "Installing eSim with full KiCad integration"

    cd "$DL"
    
    PYVER=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
    mkdir -p "$APPDIR/usr/share/eSim" "$APPDIR/usr/bin" "$APPDIR/usr/lib/python${PYVER}/site-packages"
    
    cp -r eSim-${ESIM_VERSION}/* "$APPDIR/usr/share/eSim/"
    
    # ═══ FIX CREATEKICAD.PY BUGS (CRITICAL FOR SYMBOL LIBRARY) ═══
    # This fixes both removeOldLibrary and createSym bugs that corrupt .kicad_sym files
    # AND fixes the path to use user-writable ~/.esim/symbols directory
    progress "Applying createkicad.py bug fixes..."
    
    # Create a standalone patch script (avoids heredoc escaping issues)
    cat > /tmp/patch_createkicad_esim.py << 'PATCHSCRIPT'
#!/usr/bin/env python3
"""Patch createkicad.py for AppImage compatibility"""
import re
import sys
import os

def patch_ngveri(filepath):
    """Patch NgVeri createkicad.py"""
    with open(filepath, 'r') as f:
        content = f.read()
    
    modified = False
    
    # FIX 0: Change path to user-writable ~/.esim/symbols/
    if "'/usr/share/kicad/symbols/eSim_Ngveri.kicad_sym'" in content:
        old_block = """        else:
            self.kicad_ngveri_sym = \\
                '/usr/share/kicad/symbols/eSim_Ngveri.kicad_sym'
        # self.parser = self.App_obj.parser_ngveri"""
        
        new_block = """        else:
            # Patched for AppImage: use user-writable path
            user_sym_dir = os.path.join(os.path.expanduser('~'), '.esim', 'symbols')
            os.makedirs(user_sym_dir, exist_ok=True)
            self.kicad_ngveri_sym = os.path.join(user_sym_dir, 'eSim_Ngveri.kicad_sym')
            # Create empty file if not exists
            if not os.path.exists(self.kicad_ngveri_sym):
                with open(self.kicad_ngveri_sym, 'w') as f:
                    f.write('(kicad_symbol_lib (version 20211014) (generator eSim_ngveri)' + chr(10) + ')')
        # self.parser = self.App_obj.parser_ngveri"""
        
        content = content.replace(old_block, new_block)
        modified = True
        print('[eSim] Fixed path to use ~/.esim/symbols/')
    
    # FIX 1: Rewrite removeOldLibrary function
    if 'lines = lines[0:-2]' in content:
        old_func_pattern = r'(    def removeOldLibrary\(self\):.*?)(    def createSym\(self\):)'
        
        new_func = '''    def removeOldLibrary(self):
        # FIX: Completely rewritten to properly remove symbols
        cwd = os.getcwd()
        os.chdir(self.lib_loc)
        print("Changing directory to ", self.lib_loc)
        
        with open(self.kicad_ngveri_sym, 'r') as f:
            file_content = f.read()
        
        lines = file_content.split('\\n')
        result = []
        skip = False
        depth = 0
        
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('(symbol') and ('"' + self.modelname + '"') in stripped:
                skip = True
                depth = stripped.count('(') - stripped.count(')')
                continue
            if skip:
                depth += stripped.count('(') - stripped.count(')')
                if depth <= 0:
                    skip = False
                continue
            result.append(line)
        
        new_content = '\\n'.join(result).rstrip()
        if not new_content.endswith(')'):
            new_content += '\\n)'
        new_content += '\\n'
        
        with open(self.kicad_ngveri_sym, 'w') as f:
            f.write(new_content)
        
        os.chdir(cwd)
        print("Leaving directory, ", self.lib_loc)

    def createSym(self):'''
        
        match = re.search(old_func_pattern, content, re.DOTALL)
        if match:
            content = content[:match.start()] + new_func + content[match.end():]
            modified = True
            print('[eSim] Fixed removeOldLibrary function')
    
    # FIX 2: Fix createSym file preparation (content_file[:-2] bug)
    if 'new_content_file = content_file[:-2]' in content:
        old_code = '''        # Removing ")" from "eSim_Ngveri.kicad_sym"
        file = open(self.kicad_ngveri_sym, "r")
        content_file = file.read()
        new_content_file = content_file[:-2]
        file.close()
        file = open(self.kicad_ngveri_sym, "w")
        file.write(new_content_file)
        file.close()'''
        
        new_code = '''        # FIX: Properly prepare file for appending new symbol
        with open(self.kicad_ngveri_sym, "r") as file:
            content_file = file.read()
        
        content_file = content_file.rstrip()
        if content_file.endswith(')'):
            content_file = content_file[:-1].rstrip()
        content_file += '\\\\n'
        
        with open(self.kicad_ngveri_sym, "w") as file:
            file.write(content_file)'''
        
        content = content.replace(old_code, new_code)
        modified = True
        print('[eSim] Fixed createSym file preparation')
    
    if modified:
        with open(filepath, 'w') as f:
            f.write(content)
        return True
    else:
        print('[eSim] File already patched or has different format')
        return False

def patch_nghdl(filepath):
    """Patch NgHDL createKicadLibrary.py"""
    with open(filepath, 'r') as f:
        content = f.read()
    
    modified = False
    
    # FIX 0: Change path to user-writable ~/.esim/symbols/
    if "'/usr/share/kicad/symbols/eSim_Nghdl.kicad_sym'" in content:
        old_block = """        else:
            self.kicad_nghdl_sym = \\
                '/usr/share/kicad/symbols/eSim_Nghdl.kicad_sym'"""
        
        new_block = """        else:
            # Patched for AppImage: use user-writable path
            user_sym_dir = os.path.join(os.path.expanduser('~'), '.esim', 'symbols')
            os.makedirs(user_sym_dir, exist_ok=True)
            self.kicad_nghdl_sym = os.path.join(user_sym_dir, 'eSim_Nghdl.kicad_sym')
            # Create empty file if not exists
            if not os.path.exists(self.kicad_nghdl_sym):
                with open(self.kicad_nghdl_sym, 'w') as f:
                    f.write('(kicad_symbol_lib (version 20211014) (generator eSim_nghdl)\\n)')"""
        
        content = content.replace(old_block, new_block)
        modified = True
        print('[eSim] Fixed NgHDL path to use ~/.esim/symbols/')
    
    # FIX 1: Rewrite removeOldLibrary function
    if 'lines = lines[0:-2]' in content:
        old_func_pattern = r'(    def removeOldLibrary\(self\):.*?)(    def createSym\(self\):)'
        
        new_func = '''    def removeOldLibrary(self):
        # FIX: Completely rewritten to properly remove symbols
        cwd = os.getcwd()
        os.chdir(self.lib_loc)
        print("Changing directory to ", self.lib_loc)
        
        with open(self.kicad_nghdl_sym, 'r') as f:
            file_content = f.read()
        
        lines = file_content.split('\\n')
        result = []
        skip = False
        depth = 0
        
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('(symbol') and ('"' + self.modelname + '"') in stripped:
                skip = True
                depth = stripped.count('(') - stripped.count(')')
                continue
            if skip:
                depth += stripped.count('(') - stripped.count(')')
                if depth <= 0:
                    skip = False
                continue
            result.append(line)
        
        new_content = '\\n'.join(result).rstrip()
        if not new_content.endswith(')'):
            new_content += '\\n)'
        new_content += '\\n'
        
        with open(self.kicad_nghdl_sym, 'w') as f:
            f.write(new_content)
        
        os.chdir(cwd)
        print("Leaving directory, ", self.lib_loc)

    def createSym(self):'''
        
        match = re.search(old_func_pattern, content, re.DOTALL)
        if match:
            content = content[:match.start()] + new_func + content[match.end():]
            modified = True
            print('[eSim] Fixed NgHDL removeOldLibrary function')
    
    # FIX 2: Fix createSym file preparation
    if 'new_content_file = content_file[:-2]' in content:
        old_code = '''        # Removing ")" from "eSim_Nghdl.kicad_sym"
        file = open(self.kicad_nghdl_sym, "r")
        content_file = file.read()
        new_content_file = content_file[:-2]
        file.close()
        file = open(self.kicad_nghdl_sym, "w")
        file.write(new_content_file)
        file.close()'''
        
        new_code = '''        # FIX: Properly prepare file for appending new symbol
        with open(self.kicad_nghdl_sym, "r") as file:
            content_file = file.read()
        
        content_file = content_file.rstrip()
        if content_file.endswith(')'):
            content_file = content_file[:-1].rstrip()
        content_file += '\\\\n'
        
        with open(self.kicad_nghdl_sym, "w") as file:
            file.write(content_file)'''
        
        content = content.replace(old_code, new_code)
        modified = True
        print('[eSim] Fixed NgHDL createSym file preparation')
    
    if modified:
        with open(filepath, 'w') as f:
            f.write(content)
        return True
    return False

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: patch_createkicad_esim.py <type> <filepath>")
        print("  type: ngveri or nghdl")
        sys.exit(1)
    
    patch_type = sys.argv[1]
    filepath = sys.argv[2]
    
    if not os.path.exists(filepath):
        print(f"[eSim] Warning: File not found: {filepath}")
        sys.exit(0)
    
    if patch_type == "ngveri":
        patch_ngveri(filepath)
    elif patch_type == "nghdl":
        patch_nghdl(filepath)
    else:
        print(f"Unknown patch type: {patch_type}")
        sys.exit(1)
PATCHSCRIPT
    
    # Apply patches using the standalone script
    NGVERI_FILE="$APPDIR/usr/share/eSim/src/maker/createkicad.py"
    if [ -f "$NGVERI_FILE" ]; then
        python3 /tmp/patch_createkicad_esim.py ngveri "$NGVERI_FILE"
        python3 -m py_compile "$NGVERI_FILE" && ok "NgVeri createkicad.py patched successfully" || warn "NgVeri createkicad.py has syntax errors after patching"
    fi
    
    NGHDL_FILE="$APPDIR/usr/share/eSim/nghdl/src/createKicadLibrary.py"
    if [ -f "$NGHDL_FILE" ]; then
        python3 /tmp/patch_createkicad_esim.py nghdl "$NGHDL_FILE"
        python3 -m py_compile "$NGHDL_FILE" && ok "NgHDL createKicadLibrary.py patched successfully" || warn "NgHDL createKicadLibrary.py has syntax errors after patching"
    fi
    
    rm -f /tmp/patch_createkicad_esim.py
    
    # ═══ BUNDLE NGHDL SIMULATOR SOURCE ═══
    if [ -f "nghdl/nghdl-simulator-source.tar.xz" ]; then
        cp "nghdl/nghdl-simulator-source.tar.xz" "$APPDIR/usr/share/eSim/"
        ok "Bundled nghdl-simulator-source.tar.xz"
        
        # ═══ PRE-BUILD CMPP FOR BUNDLING ═══
        # Build cmpp (Code Model PreProcessor) during AppImage creation
        # so users don't need automake/autoconf installed at runtime
        progress "Building cmpp (Code Model PreProcessor) for bundling..."
        
        NGHDL_BUILD_DIR="$DL/nghdl-build-tmp"
        rm -rf "$NGHDL_BUILD_DIR" 2>/dev/null || true
        mkdir -p "$NGHDL_BUILD_DIR"
        
        tar -xJf "nghdl/nghdl-simulator-source.tar.xz" -C "$NGHDL_BUILD_DIR" 2>/dev/null || true
        
        if [ -d "$NGHDL_BUILD_DIR/nghdl-simulator-source" ]; then
            cd "$NGHDL_BUILD_DIR/nghdl-simulator-source"
            
            # Run autoreconf to fix timestamp issues and generate fresh Makefiles
            if command -v autoreconf >/dev/null 2>&1; then
                autoreconf -fi >/dev/null 2>&1 || true
            fi
            
            # Configure the source
            if [ -f "./configure" ]; then
                ./configure --with-ngshared --enable-xspice --disable-debug \
                    --prefix="$NGHDL_BUILD_DIR/install" >/dev/null 2>&1 || true
            fi
            
            # Build cmpp
            CMPP_DIR="$NGHDL_BUILD_DIR/nghdl-simulator-source/src/xspice/cmpp"
            if [ -d "$CMPP_DIR" ]; then
                cd "$CMPP_DIR"
                make >/dev/null 2>&1 || true
                
                if [ -x "$CMPP_DIR/cmpp" ]; then
                    # Bundle the pre-built cmpp binary
                    mkdir -p "$APPDIR/usr/share/eSim/nghdl/bin"
                    cp "$CMPP_DIR/cmpp" "$APPDIR/usr/share/eSim/nghdl/bin/"
                    ok "Built and bundled cmpp binary"
                else
                    warn "Failed to build cmpp - users will need build-essential and automake"
                fi
            fi
            
            # ═══ PRE-BUILD VERILATED OBJECTS FOR BUNDLING ═══
            # Ubuntu 22.04's Verilator has buggy headers (missing <atomic>, <thread> includes)
            # Pre-compile these on the build system (Debian 12) where headers work properly
            progress "Building verilated objects for NgVeri support..."
            
            VERILATOR_INC=""
            # Find Verilator include directory
            for inc_path in "/usr/share/verilator/include" "/usr/local/share/verilator/include"; do
                if [ -f "$inc_path/verilated_threads.cpp" ]; then
                    VERILATOR_INC="$inc_path"
                    break
                fi
            done
            
            if [ -n "$VERILATOR_INC" ] && command -v g++ >/dev/null 2>&1; then
                mkdir -p "$APPDIR/usr/share/eSim/nghdl/bin"
                
                # Compile verilated_threads.o with C++17 for std::atomic/std::thread
                if g++ -c -O3 -fPIC -std=c++17 -pthread -I"$VERILATOR_INC" \
                    "$VERILATOR_INC/verilated_threads.cpp" \
                    -o "$APPDIR/usr/share/eSim/nghdl/bin/verilated_threads.o" 2>/dev/null; then
                    ok "Built verilated_threads.o"
                else
                    warn "Failed to build verilated_threads.o"
                fi
                
                # Compile verilated.o (also needed for NgVeri)
                if [ -f "$VERILATOR_INC/verilated.cpp" ]; then
                    if g++ -c -O3 -fPIC -std=c++17 -pthread -I"$VERILATOR_INC" \
                        "$VERILATOR_INC/verilated.cpp" \
                        -o "$APPDIR/usr/share/eSim/nghdl/bin/verilated.o" 2>/dev/null; then
                        ok "Built verilated.o"
                    else
                        warn "Failed to build verilated.o"
                    fi
                fi
            else
                warn "Verilator include files not found - NgVeri support may be limited"
            fi
            
            cd "$DL"
        fi
        
        rm -rf "$NGHDL_BUILD_DIR" 2>/dev/null || true
    fi
    
    # Extract KiCad libraries
    if [ -f "$APPDIR/usr/share/eSim/library/kicadLibrary.tar.xz" ]; then
        cd "$APPDIR/usr/share/eSim/library"
        tar -xJf kicadLibrary.tar.xz
        [ -d "kicadLibrary/eSim-symbols" ] && cp -r kicadLibrary/eSim-symbols/* . 2>/dev/null || true
        [ -d "kicadLibrary/kicad_eSim-Library" ] && cp kicadLibrary/kicad_eSim-Library/*.lib . 2>/dev/null || true
        ok "Extracted $(ls -1 eSim_*.{lib,kicad_sym} 2>/dev/null | wc -l) eSim library files"
        cd "$DL"
    fi
    
    # ═══ COPY USER DEVICE MODELS INTO BUNDLE ═══
    # Models saved via Model Editor are stored in ~/.esim/deviceModelLibrary/
    # Copy them into the bundle so they're included in the AppImage
    USER_MODELS="$HOME/.esim/deviceModelLibrary"
    if [ -d "$USER_MODELS" ]; then
        progress "Copying user device models into bundle..."
        user_model_count=0
        for subdir in Diode Transistor MOS JFET IGBT Misc "User Libraries"; do
            if [ -d "$USER_MODELS/$subdir" ]; then
                mkdir -p "$APPDIR/usr/share/eSim/library/deviceModelLibrary/$subdir"
                # Copy .lib and .xml files
                for file in "$USER_MODELS/$subdir"/*.{lib,xml}; do
                    [ -f "$file" ] && {
                        cp "$file" "$APPDIR/usr/share/eSim/library/deviceModelLibrary/$subdir/" 2>/dev/null
                        user_model_count=$((user_model_count + 1)) || true
                    }
                done
            fi
        done
        [ $user_model_count -gt 0 ] && ok "Copied $((user_model_count / 2)) user device models into bundle" || progress "No user device models found"
    fi
    
    # ═══ COPY USER SUBCIRCUITS INTO BUNDLE ═══
    # Subcircuits created via Subcircuit Editor are stored in ~/.esim/SubcircuitLibrary/
    # Copy them into the bundle so they're included in the AppImage
    USER_SUBCIRCUITS="$HOME/.esim/SubcircuitLibrary"
    if [ -d "$USER_SUBCIRCUITS" ]; then
        progress "Copying user subcircuits into bundle..."
        user_subcircuit_count=0
        for subdir in "$USER_SUBCIRCUITS"/*/; do
            [ -d "$subdir" ] || continue
            subcircuit_name=$(basename "$subdir")
            # Skip if it's just the analysis file or empty
            if [ -f "$subdir/$subcircuit_name.sch" ] || [ -f "$subdir/$subcircuit_name.sub" ]; then
                cp -r "$subdir" "$APPDIR/usr/share/eSim/library/SubcircuitLibrary/" 2>/dev/null && {
                    user_subcircuit_count=$((user_subcircuit_count + 1))
                }
            fi
        done
        [ $user_subcircuit_count -gt 0 ] && ok "Copied $user_subcircuit_count user subcircuits into bundle" || progress "No user subcircuits to copy"
    fi
    
    [ -f "$APPDIR/usr/share/eSim/library/sky130_fd_pr.tar.xz" ] && {
        cd "$APPDIR/usr/share/eSim/library"
        tar -xJf sky130_fd_pr.tar.xz 2>/dev/null || true
        cd "$DL"
    }
    
    # ═══ UNZIP NGHDL ═══
    # Always extract nghdl.zip to ensure Example folder and all files are present
    if [ -f "$APPDIR/usr/share/eSim/nghdl.zip" ]; then
        progress "Extracting NGHDL (with VHDL examples)..."
        cd "$APPDIR/usr/share/eSim"
        # Remove existing nghdl folder to ensure clean extraction
        rm -rf nghdl 2>/dev/null || true
        unzip -qo nghdl.zip || { warn "Failed to extract nghdl.zip"; }
        # Verify extraction was successful
        if [ -d "$APPDIR/usr/share/eSim/nghdl/Example" ]; then
            vhdl_count=$(find "$APPDIR/usr/share/eSim/nghdl/Example" -name "*.vhdl" 2>/dev/null | wc -l)
            ok "NGHDL extracted with $vhdl_count VHDL example files"
        else
            warn "NGHDL extraction incomplete - Example folder missing"
        fi
        cd "$DL"
    else
        warn "nghdl.zip not found in $APPDIR/usr/share/eSim/"
    fi
    
    # ═══ FIX GHDLSERVER.C SNPRINTF WARNING ═══
    GHDLSERVER_C="$APPDIR/usr/share/eSim/nghdl/src/ghdlserver/ghdlserver.c"
    if [ -f "$GHDLSERVER_C" ]; then
        progress "Fixing ghdlserver.c snprintf truncation warning..."
        # Fix: sizeof(port_value) returns 8 (pointer size), should use port_width + 1
        if grep -q 'sizeof(port_value)' "$GHDLSERVER_C" 2>/dev/null; then
            sed -i 's/snprintf(port_value, sizeof(port_value), "%s", s->val);/snprintf(port_value, port_width + 1, "%s", s->val);/' "$GHDLSERVER_C"
            ok "Fixed ghdlserver.c snprintf warning"
        else
            ok "ghdlserver.c already patched"
        fi
    fi
    
    # ═══ FIX GHDLSERVER.H VHPI_EXIT DECLARATION ═══
    # Header declares void Vhpi_Exit() but .c defines void Vhpi_Exit(int sig)
    # This causes "conflicting types" errors on GCC 14+/strict C compilers
    GHDLSERVER_H="$APPDIR/usr/share/eSim/nghdl/src/ghdlserver/ghdlserver.h"
    if [ -f "$GHDLSERVER_H" ]; then
        if grep -q 'void   Vhpi_Exit()' "$GHDLSERVER_H" 2>/dev/null; then
            progress "Fixing ghdlserver.h Vhpi_Exit declaration..."
            sed -i 's/void   Vhpi_Exit();/void   Vhpi_Exit(int sig);/' "$GHDLSERVER_H"
            ok "Fixed ghdlserver.h Vhpi_Exit declaration"
        fi
    fi
    
    # ═══ FIX REGEX WARNINGS IN MODEL_GENERATION.PY ═══
    MODEL_GEN_PY="$APPDIR/usr/share/eSim/nghdl/src/model_generation.py"
    if [ -f "$MODEL_GEN_PY" ]; then
        progress "Fixing regex escape sequences in model_generation.py..."
        # Use Python script file for reliable regex string replacement
        cat > /tmp/fix_regex.py << 'REGEXFIX'
import sys

if len(sys.argv) < 2:
    print("No file specified")
    sys.exit(1)

filepath = sys.argv[1]
try:
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Fix: change re.sub("\(" to re.sub(r"\("
    # The issue is using "\(" instead of r"\(" which causes SyntaxWarning
    
    # Pattern 1: with noqa comment
    content = content.replace(
        'item = re.sub("\\(", " ", item, flags=re.I)      # noqa',
        'item = re.sub(r"\\(", " ", item, flags=re.I)'
    )
    content = content.replace(
        'item = re.sub("\\)", " ", item, flags=re.I)      # noqa',
        'item = re.sub(r"\\)", " ", item, flags=re.I)'
    )
    
    # Pattern 2: without noqa comment
    content = content.replace(
        'item = re.sub("\\(", " ", item, flags=re.I)',
        'item = re.sub(r"\\(", " ", item, flags=re.I)'
    )
    content = content.replace(
        'item = re.sub("\\)", " ", item, flags=re.I)',
        'item = re.sub(r"\\)", " ", item, flags=re.I)'
    )
    
    # Also fix any corrupted versions from previous bad patches
    content = content.replace('r"("re.sub(r"\\(", " ", item, flags=re.I)', 
                               'item = re.sub(r"\\(", " ", item, flags=re.I)')
    content = content.replace('r"("re.sub(r"\\)", " ", item, flags=re.I)',
                               'item = re.sub(r"\\)", " ", item, flags=re.I)')
    
    with open(filepath, 'w') as f:
        f.write(content)
    
    print("[eSim] Fixed regex escape sequences in model_generation.py")
except Exception as e:
    print(f"[eSim] Warning: Could not fix regex escapes: {e}")
REGEXFIX
        python3 /tmp/fix_regex.py "$MODEL_GEN_PY"
        rm -f /tmp/fix_regex.py
    fi
    
    # ═══ PATCH MODEL_GENERATION.PY TO USE GHDL-LLVM ═══
    # ghdl-llvm is REQUIRED for NGHDL - ghdl-mcode cannot link with C code (ghdlserver.o)
    if [ -f "$MODEL_GEN_PY" ]; then
        progress "Patching model_generation.py to use ghdl-llvm for NGHDL..."
        cat > /tmp/patch_ghdl_llvm.py << 'GHDL_LLVM_PATCH'
import sys

filepath = sys.argv[1]
try:
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Check if already patched
    if 'GHDL_LLVM_PATCH_V1' in content:
        print("[eSim] model_generation.py already patched for ghdl-llvm")
        sys.exit(0)
    
    # 1. Patch start_server.sh generation to use ghdl-llvm
    # The script currently writes 'ghdl -i *.vhdl &&\n' - we need to add GHDL variable definition
    old_start_server_header = '''start_server.write("#!/bin/bash\\n\\n")
        start_server.write(
            "###This server run ghdl testbench for infinite time till " +'''
    
    new_start_server_header = '''start_server.write("#!/bin/bash\\n\\n")
        # GHDL_LLVM_PATCH_V1: Use ghdl-llvm for linking with C code (ghdl-mcode doesn't support -Wl)
        start_server.write("# Use ghdl-llvm for linking with C code (ghdl-mcode cannot use -Wl option)\\n")
        start_server.write("if [ -x /usr/bin/ghdl-llvm ]; then\\n")
        start_server.write("    GHDL=/usr/bin/ghdl-llvm\\n")
        start_server.write("    export GHDL_PREFIX=/usr/lib/ghdl/llvm/vhdl\\n")
        start_server.write("elif [ -x /usr/local/bin/ghdl-llvm ]; then\\n")
        start_server.write("    GHDL=/usr/local/bin/ghdl-llvm\\n")
        start_server.write("    export GHDL_PREFIX=/usr/local/lib/ghdl/llvm/vhdl\\n")
        start_server.write("else\\n")
        start_server.write("    GHDL=ghdl  # fallback, may not work for NGHDL\\n")
        start_server.write("    export GHDL_PREFIX=/usr/lib/ghdl\\n")
        start_server.write("fi\\n\\n")
        start_server.write(
            "###This server run ghdl testbench for infinite time till " +'''
    
    content = content.replace(old_start_server_header, new_start_server_header)
    
    # 2. Replace all 'ghdl ' commands with '$GHDL ' in the start_server.sh generation
    content = content.replace('start_server.write("ghdl -i', 'start_server.write("$GHDL -i')
    content = content.replace('start_server.write("ghdl -a', 'start_server.write("$GHDL -a')
    content = content.replace('start_server.write("ghdl -e', 'start_server.write("$GHDL -e')
    
    # 3. Fix VHDL compilation order - packages must be compiled before testbench
    # The old code compiles *.vhdl in arbitrary order which fails
    old_compile_order = '''start_server.write("$GHDL -i *.vhdl &&\\n")
        start_server.write("$GHDL -a *.vhdl &&\\n")
        start_server.write("$GHDL -a " + self.fname + " &&\\n")
        start_server.write(
            "ghdl -a " + self.fname.split('.')[0] + "_tb.vhdl  &&\\n"
        )'''
    
    new_compile_order = '''# Clean work library to avoid obsolete package errors (preserve ghdlserver.o)
        start_server.write("# Clean work library but preserve ghdlserver.o\\n")
        start_server.write("rm -f work-obj93.cf " + self.fname.split('.')[0] + "_tb 2>/dev/null\\n\\n")
        # Rebuild ghdlserver.o if missing
        start_server.write("# Rebuild ghdlserver.o if missing\\n")
        start_server.write("if [ ! -f ghdlserver.o ]; then\\n")
        start_server.write("    GHDLSERVER_SRC=\\"$HOME/nghdl-simulator/src/ghdlserver\\"\\n")
        start_server.write("    [ -f \\"$GHDLSERVER_SRC/ghdlserver.c\\" ] && cp \\"$GHDLSERVER_SRC/ghdlserver.c\\" . 2>/dev/null\\n")
        start_server.write("    [ -f ghdlserver.c ] && gcc -c -I. ghdlserver.c -o ghdlserver.o 2>/dev/null\\n")
        start_server.write("fi\\n\\n")
        # Compile VHDL packages in correct dependency order
        start_server.write("# 1. Compile Utility_Package (defines VhpiString type)\\n")
        start_server.write("$GHDL -a Utility_Package.vhdl &&\\n")
        start_server.write("# 2. Compile Vhpi_Package (uses Utility_Package)\\n")
        start_server.write("$GHDL -a Vhpi_Package.vhdl &&\\n")
        start_server.write("# 3. Compile sock_pkg (generated)\\n")
        start_server.write("$GHDL -a sock_pkg.vhdl &&\\n")
        start_server.write("# 4. Compile user VHDL model\\n")
        start_server.write("$GHDL -a " + self.fname + " &&\\n")
        start_server.write("# 5. Compile testbench\\n")
        start_server.write(
            "$GHDL -a " + self.fname.split('.')[0] + "_tb.vhdl  &&\\n"
        )'''
    
    content = content.replace(old_compile_order, new_compile_order)
    
    with open(filepath, 'w') as f:
        f.write(content)
    
    print("[eSim] Patched model_generation.py to use ghdl-llvm")
except Exception as e:
    print(f"[eSim] Warning: Could not patch for ghdl-llvm: {e}")
GHDL_LLVM_PATCH
        python3 /tmp/patch_ghdl_llvm.py "$MODEL_GEN_PY"
        rm -f /tmp/patch_ghdl_llvm.py
    fi
    
    # ═══ PATCH NGSPICE_GHDL.PY FOR APPIMAGE AND GHDL.CM INSTALLATION ═══
    NGSPICE_GHDL_PY="$APPDIR/usr/share/eSim/nghdl/src/ngspice_ghdl.py"
    if [ -f "$NGSPICE_GHDL_PY" ]; then
        progress "Patching ngspice_ghdl.py for AppImage and ghdl.cm installation..."
        
        # Create comprehensive patch using Python to modify the file properly
        cat > /tmp/patch_ngspice_ghdl.py << 'GHDLPATCH'
import sys
import os
import shutil
import tempfile

ngspice_ghdl_file = sys.argv[1]
try:
    with open(ngspice_ghdl_file, 'r') as f:
        content = f.read()
    
    modified = False
    
    # Check if already patched with our comprehensive patch (v2)
    if 'NGHDL_PATCH_V2' in content:
        print("[eSim] ngspice_ghdl.py already patched (v2)")
        sys.exit(0)
    
    # 1. Add required imports
    if 'import tempfile' not in content:
        content = content.replace('import os\n', 'import os\nimport tempfile\nimport shutil\n')
        modified = True

    # 2. Patch runMake to chain to runMakeInstall and enable logs (Linux only)
    old_run_make = '''    def runMake(self):
        print("run Make Called")
        self.release_home = self.parser.get('NGHDL', 'RELEASE')
        path_icm = os.path.join(self.release_home, "src/xspice/icm")
        os.chdir(path_icm)

        try:
            if os.name == 'nt':
                # path to msys bin directory where make is located
                self.msys_home = self.parser.get('COMPILER', 'MSYS_HOME')
                cmd = self.msys_home + "/mingw64/bin/mingw32-make.exe"
            else:
                cmd = " make"

            print("Running Make command in " + path_icm)
            path = os.getcwd()  # noqa
            self.process = QtCore.QProcess(self)
            self.process.start(cmd)
            print("make command process pid ---------- >", self.process.pid())

            if os.name == "nt":
                self.process.finished.connect(self.createSchematicLib)
                self.process \\
                    .readyReadStandardOutput.connect(self.readAllStandard)

        except BaseException:
            print("There is error in 'make' ")
            sys.exit()'''

    new_run_make = '''    def runMake(self):
        """Modified runMake - NGHDL_PATCH_V2"""
        print("run Make Called")
        self.release_home = self.parser.get('NGHDL', 'RELEASE')
        path_icm = os.path.join(self.release_home, "src/xspice/icm")
        os.chdir(path_icm)
        try:
            if os.name == 'nt':
                self.msys_home = self.parser.get('COMPILER', 'MSYS_HOME')
                cmd = self.msys_home + "/mingw64/bin/mingw32-make.exe"
            else:
                cmd = "make"
            print("Running Make command in " + path_icm)
            self.process = QtCore.QProcess(self)
            self.process.readyReadStandardOutput.connect(self.readAllStandard)
            self.process.readyReadStandardError.connect(self.readAllStandard)
            self.process.start(cmd)
            print("make command process pid ---------- >", self.process.pid())
            # Chain to runMakeInstall on Linux, createSchematicLib on Windows
            if os.name == "nt":
                self.process.finished.connect(self.createSchematicLib)
            else:
                self.process.finished.connect(self.runMakeInstall)
        except BaseException as e:
            print(f"There is error in 'make': {e}")
            sys.exit()'''

    if old_run_make in content:
        content = content.replace(old_run_make, new_run_make)
        modified = True

    # 3. Patch runMakeInstall to copy ghdl.cm and enable logs
    old_run_make_install = '''    def runMakeInstall(self):
        print("run Make Install Called")
        try:
            if os.name == 'nt':
                self.msys_home = self.parser.get('COMPILER', 'MSYS_HOME')
                cmd = self.msys_home + "/mingw64/bin/mingw32-make.exe install"
            else:
                cmd = " make install"
            print("Running Make Install")
            path = os.getcwd()  # noqa
            try:
                self.process.close()
            except BaseException:
                pass

            self.process = QtCore.QProcess(self)
            self.process.start(cmd)
            self.process.finished.connect(self.createSchematicLib)
            self.process.readyReadStandardOutput.connect(self.readAllStandard)
            os.chdir(self.cur_dir)

        except BaseException:
            print("There is error in 'make install' ")
            sys.exit()'''

    new_run_make_install = '''    def runMakeInstall(self):
        """Modified runMakeInstall - NGHDL_PATCH_V2"""
        print("run Make Install Called")
        try:
            if os.name == 'nt':
                self.msys_home = self.parser.get('COMPILER', 'MSYS_HOME')
                cmd = self.msys_home + "/mingw64/bin/mingw32-make.exe install"
            else:
                cmd = "make install"
            print("Running Make Install")
            try:
                self.process.close()
            except BaseException:
                pass
            self.process = QtCore.QProcess(self)
            self.process.readyReadStandardOutput.connect(self.readAllStandard)
            self.process.readyReadStandardError.connect(self.readAllStandard)
            self.process.start(cmd)
            self.process.finished.connect(self.copyGhdlCmAndCreateLib)
        except BaseException as e:
            print(f"There is error in 'make install': {e}")
            sys.exit()'''

    if old_run_make_install in content:
        content = content.replace(old_run_make_install, new_run_make_install)
        modified = True

    # 4. Helper method for copying ghdl.cm (NGHDL_CM_COPY)
    if 'def copyGhdlCmAndCreateLib(self):' not in content:
        helper_method = '''
    def copyGhdlCmAndCreateLib(self):
        """Copy ghdl.cm to user dir and create schematic lib - NGHDL_PATCH_V2"""
        print("Copying ghdl.cm to user directory...")
        try:
            release_dir = self.parser.get('NGHDL', 'RELEASE')
            ghdl_cm_src = os.path.join(release_dir, 'lib', 'ngspice', 'ghdl.cm')
            # Alternative: check in model dir if make install didn't move it yet
            alt_src = os.path.join(self.digital_home, 'ghdl', 'ghdl.cm')
            
            user_nghdl_lib = os.path.join(os.path.expanduser('~'), '.esim', 'nghdl', 'lib')
            os.makedirs(user_nghdl_lib, exist_ok=True)
            ghdl_cm_dst = os.path.join(user_nghdl_lib, 'ghdl.cm')
            
            for src in [ghdl_cm_src, alt_src]:
                if os.path.exists(src):
                    shutil.copy2(src, ghdl_cm_dst)
                    print(f"Successfully copied ghdl.cm to {ghdl_cm_dst}")
                    break
        except Exception as e:
            print(f"Warning: Could not copy ghdl.cm: {e}")
        self.createSchematicLib()
'''
        content = content.replace('    def createSchematicLib(self):', helper_method + '    def createSchematicLib(self):')
        modified = True

    # 5. Fix createModelFiles to use writable temp directory
    old_create_model = '''    def createModelFiles(self):
        print("Create Model Files Called")
        os.chdir(self.cur_dir)
        print("Current Working directory changed to " + self.cur_dir)'''
    
    new_create_model = '''    def createModelFiles(self):
        print("Create Model Files Called")
        # PATCHED FOR APPIMAGE: Use temp directory instead of read-only self.cur_dir
        temp_work_dir = tempfile.mkdtemp(prefix='nghdl_vhdl_')
        os.chdir(temp_work_dir)
        print("Current Working directory changed to " + temp_work_dir + " (writable temp)")'''

    if old_create_model in content:
        content = content.replace(old_create_model, new_create_model)
        modified = True

    # 6. Robust shutil.move in createModelFiles
    # If we use temp dir, standard move is fine. But let's make it robust to avoid crash if path exists
    if 'shutil.move("cfunc.mod", path)' in content:
        content = content.replace(
            'shutil.move("cfunc.mod", path)',
            'if os.path.exists(os.path.join(path, "cfunc.mod")): os.remove(os.path.join(path, "cfunc.mod"))\n        shutil.move("cfunc.mod", path)'
        )
        content = content.replace(
            'shutil.move("ifspec.ifs", path)',
            'if os.path.exists(os.path.join(path, "ifspec.ifs")): os.remove(os.path.join(path, "ifspec.ifs"))\n        shutil.move("ifspec.ifs", path)'
        )
        modified = True

    # 6. Force esimFlag = 1 for AppImage
    if 'Appconfig.esimFlag = 1  # Patched' not in content:
        content = content.replace(
            'if Appconfig.esimFlag == 1:',
            'Appconfig.esimFlag = 1  # Patched for AppImage\n        if Appconfig.esimFlag == 1:'
        )
        modified = True

    # 7. Fix duplicate dialog box - remove direct runMakeInstall call from uploadModel
    # Since runMake now connects to runMakeInstall via signal, the direct call causes duplicate execution
    old_upload_model_call = '''                self.runMake()
                if os.name != 'nt':
                    self.runMakeInstall()'''
    new_upload_model_call = '''                self.runMake()
                # Note: runMakeInstall is called via signal handler in runMake() for Linux
                # Do NOT call it directly here as it would cause duplicate execution'''
    if old_upload_model_call in content:
        content = content.replace(old_upload_model_call, new_upload_model_call)
        modified = True
    
    if modified:
        with open(ngspice_ghdl_file, 'w') as f:
            f.write(content)
        print("[eSim] Patched ngspice_ghdl.py with robust NGHDL_PATCH_V2")
    else:
        print("[eSim] ngspice_ghdl.py NOT modified (potential mismatch)")

except Exception as e:
    print(f"[eSim] Warning: Could not patch ngspice_ghdl.py: {e}")
    import traceback
    traceback.print_exc()
GHDLPATCH
        python3 /tmp/patch_ngspice_ghdl.py "$NGSPICE_GHDL_PY"
        rm -f /tmp/patch_ngspice_ghdl.py
        ok "ngspice_ghdl.py patched for AppImage and ghdl.cm installation"
        
        # ═══ PATCH BROWSEFILE TO OPEN EXAMPLE FOLDER ═══
        progress "Patching browseFile to open NGHDL Example folder by default..."
        # Replace the browseFile function to open in Example folder
        cat > /tmp/patch_browsefile.py << 'BROWSEPATCH'
import sys
import os

ngspice_ghdl_file = sys.argv[1] if len(sys.argv) > 1 else None
if not ngspice_ghdl_file:
    print("No file specified")
    sys.exit(1)

try:
    with open(ngspice_ghdl_file, 'r') as f:
        content = f.read()
    
    old_browse = '''    def browseFile(self):
        print("Browse button clicked")
        self.filename = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Open File', '.')[0]
        self.ledit.setText(self.filename)
        print("Vhdl file uploaded to process :", self.filename)'''
    
    new_browse = '''    def browseFile(self):
        print("Browse button clicked")
        # Default to NGHDL Example folder for VHDL examples
        default_dir = '.'
        try:
            # Check if we have APPDIR environment variable (AppImage mode)
            appdir = os.environ.get('APPDIR', '')
            if appdir:
                example_dir = os.path.join(appdir, 'usr', 'share', 'eSim', 'nghdl', 'Example')
                if os.path.isdir(example_dir):
                    default_dir = example_dir
            # Fallback: Try to find Example folder relative to this script
            if default_dir == '.':
                script_dir = os.path.dirname(os.path.abspath(__file__))
                example_dir = os.path.join(os.path.dirname(script_dir), 'Example')
                if os.path.isdir(example_dir):
                    default_dir = example_dir
        except Exception as e:
            print(f"Could not determine Example folder: {e}")
        
        print(f"Opening file browser in: {default_dir}")
        self.filename = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Open VHDL File', default_dir, 'VHDL Files (*.vhdl *.vhd);;All Files (*)')[0]
        self.ledit.setText(self.filename)
        print("Vhdl file uploaded to process :", self.filename)'''
    
    if old_browse in content:
        content = content.replace(old_browse, new_browse)
        with open(ngspice_ghdl_file, 'w') as f:
            f.write(content)
        print("[eSim] browseFile patched to open Example folder")
    elif 'Opening file browser in:' in content:
        print("[eSim] browseFile already patched")
    else:
        print("[eSim] browseFile pattern not found - may need manual patching")
except Exception as e:
    print(f"[eSim] Warning: Could not patch browseFile: {e}")
BROWSEPATCH
        python3 /tmp/patch_browsefile.py "$NGSPICE_GHDL_PY"
        rm -f /tmp/patch_browsefile.py
    fi
    
    # ═══ REWRITE NGHDL APPCONFIG.PY WITH CORRECT TEMPLATE ═══
    # Template must match ADC/DAC bridge format for consistent symbol sizing
    APPCONFIG_PY="$APPDIR/usr/share/eSim/nghdl/src/Appconfig.py"
    if [ -f "$APPCONFIG_PY" ]; then
        progress "Rewriting NGHDL Appconfig.py with corrected symbol template..."
        
        cat > "$APPCONFIG_PY" << 'NGHDL_APPCONFIG_CONTENT'
# NGHDL_APPIMAGE_FIX - Complete rewrite for AppImage with corrected symbol template
import os.path
import os
from configparser import ConfigParser


class Appconfig:
    if os.name == 'nt':
        home = os.path.join('library', 'config')
    else:
        home = os.path.expanduser('~')

    # Reading all variables from eSim config.ini
    parser_esim = ConfigParser()
    parser_esim.read(os.path.join(home, os.path.join('.esim', 'config.ini')))
    try:
        src_home = parser_esim.get('eSim', 'eSim_HOME')
        # Patched for AppImage: use user-writable path
        user_xml_loc = os.path.join(os.path.expanduser('~'), '.esim', 'modelParamXML')
        os.makedirs(os.path.join(user_xml_loc, 'Nghdl'), exist_ok=True)
        xml_loc = user_xml_loc
        lib_loc = os.path.expanduser('~')
    except BaseException:
        src_home = ""
        user_xml_loc = os.path.join(os.path.expanduser('~'), '.esim', 'modelParamXML')
        os.makedirs(os.path.join(user_xml_loc, 'Nghdl'), exist_ok=True)
        xml_loc = user_xml_loc
        lib_loc = os.path.expanduser('~')
    esimFlag = 0

    # Reading all variables from nghdl config.ini
    parser_nghdl = ConfigParser()
    parser_nghdl.read(os.path.join(home, os.path.join('.nghdl', 'config.ini')))

    # KiCad V6 Symbol Template - MATCHED TO ADC/DAC BRIDGE FORMAT
    # Reference: eSim_Hybrid.kicad_sym adc_bridge_1 symbol format
    # Rectangle: (start -10.16 TOP) (end 8.89 BOTTOM)
    # Input pins: (at -15.24 Y 0) with (length 5.08)
    # Output pins: (at 13.97 Y 180) with (length 5.08)
    # Pin spacing: 2.54 mm (standard KiCad grid)
    kicad_sym_template = {
        "start_def": "(symbol \"comp_name\" (pin_names (offset 1.016)) " +
                     "(in_bom yes) (on_board yes)",
        "U_field": "    (property \"Reference\" \"U\" (id 0) (at 0 0 0)\n" +
                   "      (effects (font (size 1.524 1.524)))\n    )",
        "comp_name_field": "    (property \"Value\" \"comp_name\" (id 1) " +
                           "(at 0 3.81 0)\n      (effects (font (size 1.524 1.524)))\n    )",
        "blank_field": [
            "    (property \"Footprint\" blank_quotes (id 2) (at 0 0 0)\n" +
            "      (effects (font (size 1.524 1.524)))\n    )",
            "    (property \"Datasheet\" blank_quotes (id 3) (at 0 0 0)\n" +
            "      (effects (font (size 1.524 1.524)))\n    )"
        ],
        # Rectangle template - will be modified: start_y = 5.08, end_y = -(max_ports * 2.54 - 1.27)
        "draw_pos": "    (symbol \"comp_name\"\n      (rectangle (start -10.16 5.08) " +
                    "(end 8.89 -1.27)\n        (stroke (width 0) (type default) " +
                    "(color 0 0 0 0))\n        (fill (type none))\n      )\n    )",
        "start_draw": "    (symbol",
        # Input pin at X=-15.24 (5.08 length to reach rectangle at -10.16)
        "input_port": "      (pin input line (at -15.24 1.27 0) (length 5.08)\n" +
                      "        (name \"in\" (effects (font (size 1.27 1.27))))\n" +
                      "        (number \"1\" (effects (font (size 1.27 1.27))))\n      )",
        # Output pin at X=13.97 (5.08 length to reach rectangle at 8.89)
        "output_port": "      (pin output line (at 13.97 1.27 180) (length 5.08)\n" +
                       "        (name \"out\" (effects (font (size 1.27 1.27))))\n" +
                       "        (number \"2\" (effects (font (size 1.27 1.27))))\n      )",
        "end_draw": "    )\n  )"
    }
NGHDL_APPCONFIG_CONTENT
        ok "NGHDL Appconfig.py rewritten with ADC/DAC bridge-compatible template"
    fi
    
    # ═══ PATCH MAKER/APPCONFIG.PY FOR NgVeri USER-WRITABLE XML PATHS ═══
    # NgVeri uses a DIFFERENT Appconfig.py at src/maker/Appconfig.py
    MAKER_APPCONFIG_PY="$APPDIR/usr/share/eSim/src/maker/Appconfig.py"
    if [ -f "$MAKER_APPCONFIG_PY" ]; then
        progress "Patching maker/Appconfig.py for NgVeri user-writable XML paths..."
        
        # Check if already patched with full fix
        if grep -q "APPIMAGE_NGVERI_FIX" "$MAKER_APPCONFIG_PY" 2>/dev/null; then
            ok "maker/Appconfig.py already patched"
        else
            # Completely rewrite the Appconfig.py for AppImage compatibility
            # Must set xml_loc ALWAYS, not just in try block
            cat > "$MAKER_APPCONFIG_PY" << 'MAKER_APPCONFIG_CONTENT'
# APPIMAGE_NGVERI_FIX - Patched for AppImage user-writable paths
import os
import os.path
from configparser import ConfigParser


class Appconfig:
    # Always use user-writable paths for AppImage
    home = os.path.expanduser('~')
    
    # User-writable XML location - MUST be set before anything else
    user_xml_loc = os.path.join(home, '.esim', 'modelParamXML')
    os.makedirs(os.path.join(user_xml_loc, 'Ngveri'), exist_ok=True)
    os.makedirs(os.path.join(user_xml_loc, 'Nghdl'), exist_ok=True)
    xml_loc = user_xml_loc
    lib_loc = home
    src_home = ""
    
    # Try to read eSim config for src_home
    parser_esim = ConfigParser()
    try:
        parser_esim.read(os.path.join(home, '.esim', 'config.ini'))
        src_home = parser_esim.get('eSim', 'eSim_HOME')
    except:
        pass
    
    esimFlag = 0

    # KiCad v6 Library Template
    kicad_sym_template = {
        "start_def":    "(symbol \"comp_name\" (pin_names (offset 1.016)) " +
                        "(in_bom yes) (on_board yes)",
        "U_field":  "(property \"Reference\" \"U\" (id 0) (at 12 15 0)" +
                    "(effects (font (size 1.524 1.524))))",
        "comp_name_field":  "(property \"Value\" \"comp_name\" (id 1) " +
                            "(at 12 18 0)(effects (font (size 1.524 1.524))))",
        "blank_field":  [
            "(property \"Footprint\" blank_quotes (id 2) " +
            "(at 72.39 49.53 0)(effects (font (size 1.524 1.524))))",
            "(property \"Datasheet\" blank_quotes (id 3) " +
            "(at 72.39 49.53 0)(effects (font (size 1.524 1.524))))"
        ],
        "draw_pos":     "(symbol \"comp_name\"(rectangle (start 0 0 ) " +
                        "(end 25.40 0 )(stroke (width 0) (type default) " +
                        "(color 0 0 0 0))(fill (type none))))",
        "start_draw":   "(symbol",
        "input_port":   "(pin input line(at -5.08 0 0 )(length 5.08 )" +
                        "(name \"in\" (effects(font(size 1.27 1.27))))" +
                        "(number \"1\" (effects (font (size 1.27 1.27)))))",
        "output_port":  "(pin output line(at 30.48 0 180 )(length 5.08 )" +
                        "(name \"out\" (effects(font(size 1.27 1.27))))" +
                        "(number \"2\" (effects (font (size 1.27 1.27)))))",
        "end_draw":     "))"
    }
MAKER_APPCONFIG_CONTENT
            echo "[eSim] Rewrote maker/Appconfig.py for NgVeri user-writable XML paths"
            ok "maker/Appconfig.py patched for NgVeri user-writable XML paths"
        fi
    fi
    
    # ═══ REWRITE CREATEKICADLIBRARY.PY WITH FIXED SYMBOL GENERATION ═══
    # Complete rewrite to match ADC/DAC bridge symbol format and fix all issues
    CREATEKICAD_PY="$APPDIR/usr/share/eSim/nghdl/src/createKicadLibrary.py"
    if [ -f "$CREATEKICAD_PY" ]; then
        progress "Rewriting createKicadLibrary.py with fixed symbol generation..."
        
        cat > "$CREATEKICAD_PY" << 'CREATEKICADLIBRARY_CONTENT'
# NGHDL_CREATEKICAD_COMPLETE_REWRITE - Fixed symbol generation matching ADC/DAC bridge format
from Appconfig import Appconfig
import re
import os
import xml.etree.cElementTree as ET
from PyQt5 import QtWidgets


class AutoSchematic(QtWidgets.QWidget):

    def __init__(self, parent, modelname):
        QtWidgets.QWidget.__init__(self)
        self.parent = parent
        self.modelname = modelname.split('.')[0]
        self.xml_loc = Appconfig.xml_loc
        self.lib_loc = Appconfig.lib_loc
        
        # Setup user-writable symbol path
        if os.name == 'nt':
            eSim_src = Appconfig.src_home
            inst_dir = eSim_src.replace('\\eSim', '')
            self.kicad_nghdl_sym = \
                inst_dir + '/KiCad/share/kicad/symbols/eSim_Nghdl.kicad_sym'
        else:
            # Use user-writable path
            user_sym_dir = os.path.join(os.path.expanduser('~'), '.esim', 'symbols')
            os.makedirs(user_sym_dir, exist_ok=True)
            self.kicad_nghdl_sym = os.path.join(user_sym_dir, 'eSim_Nghdl.kicad_sym')
            # Create empty file if not exists
            if not os.path.exists(self.kicad_nghdl_sym):
                with open(self.kicad_nghdl_sym, 'w') as f:
                    f.write('(kicad_symbol_lib (version 20211014) (generator eSim_nghdl)\n)\n')
        
        self.parser = Appconfig.parser_nghdl

    def createKicadSymbol(self):
        xmlFound = None
        for root, dirs, files in os.walk(self.xml_loc):
            if (str(self.modelname) + '.xml') in files:
                xmlFound = root
                print(xmlFound)
        if xmlFound is None:
            self.getPortInformation()
            self.createXML()
            self.createSym()
        elif (xmlFound == os.path.join(self.xml_loc, 'Nghdl')):
            print('Library already exists...')
            ret = QtWidgets.QMessageBox.warning(
                self.parent, "Warning", '''<b>Library files for this model''' +
                ''' already exist. Do you want to overwrite it?</b><br/>
                If yes press ok, else cancel it and ''' +
                '''change the name of your vhdl file.''',
                QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Cancel
            )
            if ret == QtWidgets.QMessageBox.Ok:
                print("Overwriting existing libraries")
                self.getPortInformation()
                self.createXML()
                self.removeOldLibrary()
                self.createSym()
            else:
                print("Exiting Nghdl")
                quit()
        else:
            print('Pre existing library...')
            ret = QtWidgets.QMessageBox.critical(
                self.parent, "Error", '''<b>A standard library already ''' +
                '''exists with this name.</b><br/><b>Please change the ''' +
                '''name of your vhdl file and upload it again.</b>''',
                QtWidgets.QMessageBox.Ok
            )

    def getPortInformation(self):
        portInformation = PortInfo(self)
        portInformation.getPortInfo()
        self.portInfo = portInformation.bit_list
        self.input_length = portInformation.input_len

    def createXML(self):
        cwd = os.getcwd()
        xmlDestination = os.path.join(self.xml_loc, 'Nghdl')
        self.splitText = ""
        for bit in self.portInfo[:-1]:
            self.splitText += bit + "-V:"
        self.splitText += self.portInfo[-1] + "-V"

        print("changing directory to ", xmlDestination)
        os.chdir(xmlDestination)

        root = ET.Element("model")
        ET.SubElement(root, "name").text = self.modelname
        ET.SubElement(root, "type").text = "Nghdl"
        ET.SubElement(root, "node_number").text = str(len(self.portInfo))
        ET.SubElement(root, "title").text = (
                            "Add parameters for " + str(self.modelname))
        ET.SubElement(root, "split").text = self.splitText
        param = ET.SubElement(root, "param")
        ET.SubElement(param, "rise_delay", default="1.0e-9").text = (
                                    "Enter Rise Delay (default=1.0e-9)")
        ET.SubElement(param, "fall_delay", default="1.0e-9").text = (
                                    "Enter Fall Delay (default=1.0e-9)")
        ET.SubElement(param, "input_load", default="1.0e-12").text = (
                                    "Enter Input Load (default=1.0e-12)")
        ET.SubElement(param, "instance_id", default="1").text = (
                                    "Enter Instance ID (Between 0-99)")
        tree = ET.ElementTree(root)
        tree.write(str(self.modelname) + '.xml')
        print("Leaving the directory ", xmlDestination)
        os.chdir(cwd)

    def removeOldLibrary(self):
        """Remove existing symbol from library file - completely rewritten"""
        cwd = os.getcwd()
        os.chdir(self.lib_loc)
        print("Changing directory to ", self.lib_loc)
        
        with open(self.kicad_nghdl_sym, 'r') as f:
            content = f.read()
        
        result_lines = []
        in_target_symbol = False
        paren_depth = 0
        
        lines = content.split('\n')
        for line in lines:
            stripped = line.strip()
            
            # Check if this line starts our target symbol
            if stripped.startswith('(symbol') and f'"{self.modelname}"' in stripped:
                in_target_symbol = True
                paren_depth = stripped.count('(') - stripped.count(')')
                continue
            
            if in_target_symbol:
                paren_depth += stripped.count('(') - stripped.count(')')
                if paren_depth <= 0:
                    in_target_symbol = False
                continue
            
            result_lines.append(line)
        
        # Reconstruct the file
        new_content = '\n'.join(result_lines)
        new_content = new_content.rstrip()
        
        # Ensure proper closing
        if not new_content.endswith(')'):
            new_content += '\n)'
        new_content += '\n'
        
        with open(self.kicad_nghdl_sym, 'w') as f:
            f.write(new_content)
        
        os.chdir(cwd)
        print("Leaving directory, ", self.lib_loc)

    def createSym(self):
        """Create KiCad symbol matching ADC/DAC bridge format"""
        # Constants matching ADC/DAC bridge format
        PIN_SPACING = 2.54  # Standard KiCad grid spacing
        RECT_LEFT = -10.16  # Rectangle left edge
        RECT_RIGHT = 8.89   # Rectangle right edge
        RECT_TOP = 5.08     # Rectangle top
        INPUT_PIN_X = -15.24  # Input pin X position (5.08 from rect edge)
        OUTPUT_PIN_X = 13.97  # Output pin X position (5.08 from rect edge)
        PIN_LENGTH = 5.08   # Standard pin length
        
        cwd = os.getcwd()
        os.chdir(self.lib_loc)
        print("Changing directory to ", self.lib_loc)

        # Read existing file and prepare for appending
        with open(self.kicad_nghdl_sym, "r") as f:
            content = f.read()
        
        # Remove trailing ) to append new symbol
        content = content.rstrip()
        if content.endswith(')'):
            content = content[:-1].rstrip()
        content += '\n'
        
        with open(self.kicad_nghdl_sym, "w") as f:
            f.write(content)

        # Calculate port counts
        inputs = self.portInfo[0: self.input_length]
        outputs = self.portInfo[self.input_length:]
        num_inputs = sum([int(x) for x in inputs])
        num_outputs = sum([int(x) for x in outputs])
        total_ports = num_inputs + num_outputs
        max_ports = max(num_inputs, num_outputs)
        
        # Calculate rectangle height based on max ports
        rect_bottom = RECT_TOP - (max_ports * PIN_SPACING) - 1.27
        
        # Calculate starting Y position for pins (centered)
        # First pin at 1.27, subsequent pins spaced by PIN_SPACING going down
        
        # Build the symbol
        sym_lines = []
        sym_lines.append(f'  (symbol "{self.modelname}" (pin_names (offset 1.016)) (in_bom yes) (on_board yes)')
        sym_lines.append(f'    (property "Reference" "U" (id 0) (at 0 0 0)')
        sym_lines.append(f'      (effects (font (size 1.524 1.524)))')
        sym_lines.append(f'    )')
        sym_lines.append(f'    (property "Value" "{self.modelname}" (id 1) (at 0 {RECT_TOP + 2.54:.2f} 0)')
        sym_lines.append(f'      (effects (font (size 1.524 1.524)))')
        sym_lines.append(f'    )')
        sym_lines.append(f'    (property "Footprint" "" (id 2) (at 0 0 0)')
        sym_lines.append(f'      (effects (font (size 1.524 1.524)))')
        sym_lines.append(f'    )')
        sym_lines.append(f'    (property "Datasheet" "" (id 3) (at 0 0 0)')
        sym_lines.append(f'      (effects (font (size 1.524 1.524)))')
        sym_lines.append(f'    )')
        
        # Rectangle (graphical representation)
        sym_lines.append(f'    (symbol "{self.modelname}_0_1"')
        sym_lines.append(f'      (rectangle (start {RECT_LEFT:.2f} {RECT_TOP:.2f}) (end {RECT_RIGHT:.2f} {rect_bottom:.2f})')
        sym_lines.append(f'        (stroke (width 0) (type default) (color 0 0 0 0))')
        sym_lines.append(f'        (fill (type none))')
        sym_lines.append(f'      )')
        sym_lines.append(f'    )')
        
        # Pins
        sym_lines.append(f'    (symbol "{self.modelname}_1_1"')
        
        pin_number = 1
        
        # Input pins - start from top, go down
        input_y = 1.27 + (num_inputs - 1) * PIN_SPACING / 2  # Center inputs vertically
        for i in range(num_inputs):
            y_pos = input_y - (i * PIN_SPACING)
            sym_lines.append(f'      (pin input line (at {INPUT_PIN_X:.2f} {y_pos:.2f} 0) (length {PIN_LENGTH:.2f})')
            sym_lines.append(f'        (name "IN{i+1}" (effects (font (size 1.27 1.27))))')
            sym_lines.append(f'        (number "{pin_number}" (effects (font (size 1.27 1.27))))')
            sym_lines.append(f'      )')
            pin_number += 1
        
        # Output pins - start from top, go down
        output_y = 1.27 + (num_outputs - 1) * PIN_SPACING / 2  # Center outputs vertically
        for i in range(num_outputs):
            y_pos = output_y - (i * PIN_SPACING)
            sym_lines.append(f'      (pin output line (at {OUTPUT_PIN_X:.2f} {y_pos:.2f} 180) (length {PIN_LENGTH:.2f})')
            sym_lines.append(f'        (name "OUT{i+1}" (effects (font (size 1.27 1.27))))')
            sym_lines.append(f'        (number "{pin_number}" (effects (font (size 1.27 1.27))))')
            sym_lines.append(f'      )')
            pin_number += 1
        
        sym_lines.append(f'    )')
        sym_lines.append(f'  )')
        sym_lines.append(f')')
        sym_lines.append('')
        
        # Append to file
        with open(self.kicad_nghdl_sym, "a") as f:
            f.write('\n'.join(sym_lines))
        
        os.chdir(cwd)
        print('Leaving directory, ', self.lib_loc)
        
        QtWidgets.QMessageBox.information(
            self.parent, "Symbol Added",
            '''Symbol details for this model is added to the \'''' +
            '''<b>eSim_Nghdl.kicad_sym</b>\' in ~/.esim/symbols/.''',
            QtWidgets.QMessageBox.Ok
        )


class PortInfo:
    def __init__(self, model):
        self.modelname = model.modelname
        self.model_loc = os.path.join(
            model.parser.get('NGHDL', 'DIGITAL_MODEL'), 'ghdl'
        )
        self.bit_list = []
        self.input_len = 0

    def getPortInfo(self):
        info_loc = os.path.join(self.model_loc, self.modelname + '/DUTghdl/')
        input_list = []
        output_list = []
        read_file = open(info_loc + 'connection_info.txt', 'r')
        data = read_file.readlines()
        read_file.close()

        for line in data:
            if re.match(r'^\s*$', line):
                pass
            else:
                in_items = re.findall(
                    "IN", line, re.MULTILINE | re.IGNORECASE
                )
                out_items = re.findall(
                    "OUT", line, re.MULTILINE | re.IGNORECASE
                )
            if in_items:
                input_list.append(line.split())
            if out_items:
                output_list.append(line.split())

        for in_list in input_list:
            self.bit_list.append(in_list[2])
        self.input_len = len(self.bit_list)
        for out_list in output_list:
            self.bit_list.append(out_list[2])
CREATEKICADLIBRARY_CONTENT
        
        # Verify syntax
        python3 -m py_compile "$CREATEKICAD_PY" && \
            ok "createKicadLibrary.py rewritten with fixed symbol generation" || \
            warn "createKicadLibrary.py may have syntax errors"
    fi
    
    # ═══ PATCH NGVERI CREATEKICAD.PY FOR USER-WRITABLE SYMBOL PATH ═══
    # NgVeri has its own createkicad.py at src/maker/createkicad.py
    NGVERI_CREATEKICAD_PY="$APPDIR/usr/share/eSim/src/maker/createkicad.py"
    if [ -f "$NGVERI_CREATEKICAD_PY" ]; then
        progress "Patching NgVeri createkicad.py for user-writable symbol path..."
        
        # Check if already patched
        if grep -q "user_sym_dir" "$NGVERI_CREATEKICAD_PY" 2>/dev/null; then
            ok "NgVeri createkicad.py already patched"
        else
            # Patch to use user-writable ~/.esim/symbols directory
            python3 << NGVERI_CREATEKICAD_PATCH
createkicad_file = "$NGVERI_CREATEKICAD_PY"
try:
    with open(createkicad_file, 'r') as f:
        content = f.read()
    
    # Replace kicad_ngveri_sym path to use user home directory
    old_path = "self.kicad_ngveri_sym = \\\\\\n                '/usr/share/kicad/symbols/eSim_Ngveri.kicad_sym'"
    new_path = """# Patched for AppImage: use user-writable path for NgVeri symbols
            user_sym_dir = os.path.join(os.path.expanduser('~'), '.esim', 'symbols')
            os.makedirs(user_sym_dir, exist_ok=True)
            self.kicad_ngveri_sym = os.path.join(user_sym_dir, 'eSim_Ngveri.kicad_sym')
            # Create empty file if not exists
            if not os.path.exists(self.kicad_ngveri_sym):
                with open(self.kicad_ngveri_sym, 'w') as f:
                    f.write('(kicad_symbol_lib (version 20211014) (generator eSim_ngveri)' + chr(10) + ')')"""
    
    if "'/usr/share/kicad/symbols/eSim_Ngveri.kicad_sym'" in content:
        content = content.replace(old_path, new_path)
        with open(createkicad_file, 'w') as f:
            f.write(content)
        print("[eSim] Patched NgVeri createkicad.py for user-writable symbol path")
    else:
        print("[eSim] NgVeri createkicad.py has different format, skipping patch")
except Exception as e:
    print("[eSim] Warning: Could not patch NgVeri createkicad.py: " + str(e))
NGVERI_CREATEKICAD_PATCH
            ok "NgVeri createkicad.py patched for user-writable symbol path"
        fi
    fi
    
    # ═══ PATCH REMOVEOLDLIBRARY FUNCTION (ADDITIONAL FIX) ═══
    if [ -f "$NGVERI_CREATEKICAD_PY" ]; then
        # Check if removeOldLibrary needs patching (not already fixed by earlier patch)
        if ! grep -q "REMOVEOLDLIB_COMPLETE_FIX\|FIX: Completely rewritten" "$NGVERI_CREATEKICAD_PY" 2>/dev/null; then
            progress "Patching createkicad.py removeOldLibrary with complete fix..."
            python3 << REMOVEOLDLIB_PATCH
import sys
import re
createkicad_file = "$NGVERI_CREATEKICAD_PY"
try:
    with open(createkicad_file, 'r') as f:
        content = f.read()
    
    # Check if already patched with complete fix
    if 'REMOVEOLDLIB_COMPLETE_FIX' in content:
        print("[eSim] removeOldLibrary already has complete fix")
        sys.exit(0)
    
    # Find and replace the entire removeOldLibrary function
    old_func_pattern = r'(    def removeOldLibrary\\(self\\):.*?)(    def createSym\\(self\\):)'
    
    new_func = '''    def removeOldLibrary(self):
        # REMOVEOLDLIB_COMPLETE_FIX: Completely rewritten to handle all edge cases
        """Remove existing symbol from library file"""
        cwd = os.getcwd()
        os.chdir(self.lib_loc)
        print("Changing directory to ", self.lib_loc)
        
        with open(self.kicad_ngveri_sym, 'r') as f:
            content = f.read()
        
        # Parse symbols and rebuild file without the target symbol
        # Find all top-level symbols
        result_lines = []
        in_target_symbol = False
        paren_depth = 0
        
        lines = content.split('\\\\n')
        i = 0
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()
            
            # Check if this line starts a top-level symbol we want to remove
            if stripped.startswith('(symbol') and f'"{self.modelname}"' in stripped:
                in_target_symbol = True
                paren_depth = stripped.count('(') - stripped.count(')')
                i += 1
                continue
            
            if in_target_symbol:
                paren_depth += stripped.count('(') - stripped.count(')')
                if paren_depth <= 0:
                    in_target_symbol = False
                i += 1
                continue
            
            result_lines.append(line)
            i += 1
        
        # Reconstruct the file
        new_content = '\n'.join(result_lines)
        # Ensure proper closing
        new_content = new_content.rstrip()
        if not new_content.endswith(')'):
            new_content += '\n)'
        new_content += '\n'
        
        with open(self.kicad_ngveri_sym, 'w') as f:
            f.write(new_content)
        
        os.chdir(cwd)
        print("Leaving directory, ", self.lib_loc)

    def createSym(self):'''
    
    match = re.search(old_func_pattern, content, re.DOTALL)
    if match:
        content = content[:match.start()] + new_func + content[match.end():]
        with open(createkicad_file, 'w') as f:
            f.write(content)
        print("[eSim] Completely rewrote removeOldLibrary function")
    else:
        print("[eSim] Could not find removeOldLibrary function to patch")
except Exception as e:
    print("[eSim] Warning: Could not patch removeOldLibrary: " + str(e))
    import traceback
    traceback.print_exc()
REMOVEOLDLIB_PATCH
            ok "createkicad.py removeOldLibrary patched"
        fi
    fi
    
    # ═══ FIX CREATESYM FILE PREPARATION FOR NGVERI ONLY ═══
    # The createSym function corrupts the file when preparing to append new symbols.
    # NGHDL createKicadLibrary.py is completely rewritten, so only fix NgVeri here.
    progress "Patching createSym file preparation in NgVeri createkicad.py..."
    python3 << CREATESYM_FIX_PATCH
import sys
import re

# Only patch NgVeri - NGHDL is completely rewritten
filepath = "$NGVERI_CREATEKICAD_PY"
try:
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Check if already has the complete fix (either marker or actual fix code)
    if 'CREATESYM_FILE_PREP_FIX' in content:
        print(f"[eSim] {filepath} already has createSym fix")
        sys.exit(0)
    
    # Also check if the fix is already applied upstream (without our marker)
    if "content_file.rstrip()" in content and "endswith(')')" in content:
        print(f"[eSim] {filepath} already has createSym fix (upstream)")
        sys.exit(0)
    
    # Pattern to find the file preparation block for NgVeri
    pattern_ngveri = r'(        # Removing "\\)" from "eSim_Ngveri\\.kicad_sym".*?file\\.close\\(\\)\\s*\\n\\s*)(# Appending new schematic block)'
    
    new_block_ngveri = '''        # CREATESYM_FILE_PREP_FIX: Properly prepare file for appending new symbol
        with open(self.kicad_ngveri_sym, "r") as file:
            content_file = file.read()
        
        # Parse the file to properly remove only the final closing ) of kicad_symbol_lib
        content_file = content_file.rstrip()
        if content_file.endswith(')'):
            content_file = content_file[:-1].rstrip()
        # Ensure newline for proper formatting
        content_file += chr(10)
        
        with open(self.kicad_ngveri_sym, "w") as file:
            file.write(content_file)

        # Appending new schematic block'''
    
    match = re.search(pattern_ngveri, content, re.DOTALL)
    if match:
        content = content[:match.start()] + new_block_ngveri + content[match.end():]
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"[eSim] Patched createSym file preparation in {filepath}")
    else:
        print(f"[eSim] Could not find createSym block to patch in {filepath}")
except Exception as e:
    print(f"[eSim] Warning: Could not patch {filepath}: {e}")
CREATESYM_FIX_PATCH
    ok "NgVeri createSym file preparation patched"
    
    # ═══ DIRECT FIX FOR ESCAPED NEWLINE IN NGVERI CREATEKICAD.PY ═══
    # Fix the literal \\n that should be an actual newline
    progress "Fixing escaped newlines in NgVeri createkicad.py..."
    if [ -f "$NGVERI_CREATEKICAD_PY" ]; then
        sed -i "s/content_file += '\\\\\\\\n'/content_file += chr(10)/g" "$NGVERI_CREATEKICAD_PY"
        python3 -m py_compile "$NGVERI_CREATEKICAD_PY" && \
            ok "NgVeri createkicad.py newline escape fixed" || \
            warn "NgVeri createkicad.py may have syntax errors"
    fi
    
    # NOTE: NGHDL createKicadLibrary.py is completely rewritten earlier,
    # so no additional patching needed for removeOldLibrary or createSym
    
    # ═══ BUNDLE CMPP TOOL FOR CODE MODEL COMPILATION ═══
    CMPP_SOURCE="$BUILD/ngspice-build/ngspice-35/release/src/xspice/cmpp/cmpp"
    if [ -f "$CMPP_SOURCE" ]; then
        progress "Bundling cmpp code model preprocessor..."
        mkdir -p "$APPDIR/usr/bin"
        cp "$CMPP_SOURCE" "$APPDIR/usr/bin/cmpp"
        chmod +x "$APPDIR/usr/bin/cmpp"
        ok "cmpp bundled"
    fi
    
    # ═══ BUNDLE NGSPICE HEADERS FOR CODE MODEL COMPILATION ═══
    NGSPICE_SRC="$DL/ngspice-build/ngspice-35/src"
    if [ -d "$NGSPICE_SRC" ]; then
        progress "Bundling NgSpice headers for code model compilation..."
        mkdir -p "$APPDIR/usr/include/ngspice"
        for header in cm.h mifproto.h mifdefs.h miftypes.h cktdefs.h devdefs.h ifsim.h iferrmsg.h gendefs.h ngspice.h cpstd.h bool.h; do
            find "$NGSPICE_SRC" -name "$header" -exec cp {} "$APPDIR/usr/include/ngspice/" \; 2>/dev/null || true
        done
        if [ -d "$DL/ngspice-build/ngspice-35/release/src/include/ngspice" ]; then
            cp "$DL/ngspice-build/ngspice-35/release/src/include/ngspice"/*.h "$APPDIR/usr/include/ngspice/" 2>/dev/null || true
        fi
        ok "NgSpice headers bundled"
    fi
    
    # ═══ FIX PROCESSING.PY - SEARCH USER'S NGHDL MODEL DIRECTORY ═══
    PROCESSING_FILE="$APPDIR/usr/share/eSim/src/kicadtoNgspice/Processing.py"
    if [ -f "$PROCESSING_FILE" ]; then
        progress "Patching Processing.py to search user's NGHDL model directory..."
        
        cat > /tmp/patch_processing.py << 'PROCESSINGPATCH'
import sys
processing_file = sys.argv[1]
try:
    with open(processing_file, 'r') as f:
        content = f.read()
    
    if 'user_model_xml_dir' in content:
        print("[eSim] Processing.py already patched")
        sys.exit(0)
    
    old_all_dir = '''                    all_dir = [x[0]
                               for x in os.walk(PrcocessNetlist.modelxmlDIR)]'''
    
    new_all_dir = '''                    # Also search user's NGHDL/Ngveri model directory
                    user_model_xml_dir = os.path.join(os.path.expanduser('~'), '.esim', 'modelParamXML')
                    all_dir = [x[0] for x in os.walk(PrcocessNetlist.modelxmlDIR)]
                    if os.path.exists(user_model_xml_dir):
                        all_dir.extend([x[0] for x in os.walk(user_model_xml_dir)])'''
    
    if old_all_dir in content:
        content = content.replace(old_all_dir, new_all_dir)
        with open(processing_file, 'w') as f:
            f.write(content)
        print("[eSim] Patched Processing.py to search user's NGHDL model directory")
    elif 'for x in os.walk(PrcocessNetlist.modelxmlDIR)]' in content:
        old_line = 'for x in os.walk(PrcocessNetlist.modelxmlDIR)]'
        new_lines = '''for x in os.walk(PrcocessNetlist.modelxmlDIR)]
                    user_model_xml_dir = os.path.join(os.path.expanduser('~'), '.esim', 'modelParamXML')
                    if os.path.exists(user_model_xml_dir):
                        all_dir.extend([x[0] for x in os.walk(user_model_xml_dir)])'''
        content = content.replace(old_line, new_lines)
        with open(processing_file, 'w') as f:
            f.write(content)
        print("[eSim] Patched Processing.py (alternative method)")
except Exception as e:
    print("[eSim] Warning: Could not patch Processing.py: " + str(e))
PROCESSINGPATCH
        python3 /tmp/patch_processing.py "$PROCESSING_FILE"
        rm -f /tmp/patch_processing.py
        ok "Processing.py patched to search user's NGHDL model directory"
    fi
    
    # ═══ FIX KICADTONGSPICE.PY - UnboundLocalError FOR XML ELEMENTS ═══
    KICAD_NGSPICE_FILE="$APPDIR/usr/share/eSim/src/kicadtoNgspice/KicadtoNgspice.py"
    if [ -f "$KICAD_NGSPICE_FILE" ]; then
        progress "Patching KicadtoNgspice.py to fix UnboundLocalError issues..."
        
        cat > /tmp/patch_kicadngspice.py << 'KICADPATCH'
import sys
import re

kicad_file = sys.argv[1]
try:
    with open(kicad_file, 'r') as f:
        content = f.read()
    
    if 'UnboundLocalError FIX' in content:
        print("[eSim] KicadtoNgspice.py already patched for UnboundLocalError")
        sys.exit(0)
    
    patched = False
    
    # Fix attr_microcontroller
    old_micro = '''        if check == 1:
            for child in attr_parent:
                if child.tag == "microcontroller":
                    attr_microcontroller = child
        i = 0'''
    
    new_micro = '''        if check == 1:
            attr_microcontroller = None  # UnboundLocalError FIX
            for child in attr_parent:
                if child.tag == "microcontroller":
                    attr_microcontroller = child
                    break
            if attr_microcontroller is None:
                attr_microcontroller = ET.SubElement(attr_parent, "microcontroller")
        i = 0'''
    
    if old_micro in content:
        content = content.replace(old_micro, new_micro)
        patched = True
    
    # Fix attr_subcircuit
    old_subckt = '''        if check == 1:
            for child in attr_parent:
                if child.tag == "subcircuit":
                    del child[:]
                    attr_subcircuit = child'''
    
    new_subckt = '''        if check == 1:
            attr_subcircuit = None  # UnboundLocalError FIX
            for child in attr_parent:
                if child.tag == "subcircuit":
                    del child[:]
                    attr_subcircuit = child
                    break
            if attr_subcircuit is None:
                attr_subcircuit = ET.SubElement(attr_parent, "subcircuit")'''
    
    if old_subckt in content:
        content = content.replace(old_subckt, new_subckt)
        patched = True
    
    # Fix attr_model
    old_model = '''        if check == 1:
            for child in attr_parent:
                if child.tag == "model":
                    attr_model = child
        i = 0'''
    
    new_model = '''        if check == 1:
            attr_model = None  # UnboundLocalError FIX
            for child in attr_parent:
                if child.tag == "model":
                    attr_model = child
                    break
            if attr_model is None:
                attr_model = ET.SubElement(attr_parent, "model")
        i = 0'''
    
    if old_model in content:
        content = content.replace(old_model, new_model)
        patched = True
    
    # Fix attr_devicemodel
    old_device = '''        if check == 1:
            for child in attr_parent:
                if child.tag == "devicemodel":
                    del child[:]
                    attr_devicemodel = child'''
    
    new_device = '''        if check == 1:
            attr_devicemodel = None  # UnboundLocalError FIX
            for child in attr_parent:
                if child.tag == "devicemodel":
                    del child[:]
                    attr_devicemodel = child
                    break
            if attr_devicemodel is None:
                attr_devicemodel = ET.SubElement(attr_parent, "devicemodel")'''
    
    if old_device in content:
        content = content.replace(old_device, new_device)
        patched = True
    
    if patched:
        with open(kicad_file, 'w') as f:
            f.write(content)
        print("[eSim] ✓ Patched KicadtoNgspice.py to fix UnboundLocalError issues")
    else:
        print("[eSim] KicadtoNgspice.py format unrecognized, skipping patches")
except Exception as e:
    print("[eSim] Warning: Could not patch KicadtoNgspice.py: " + str(e))
KICADPATCH
        python3 /tmp/patch_kicadngspice.py "$KICAD_NGSPICE_FILE"
        rm -f /tmp/patch_kicadngspice.py
        ok "KicadtoNgspice.py patched for UnboundLocalError fixes"
    fi
    
    # ═══ FIX NGSPICE BINARY RAW FILE PLOTTING ═══
    NGSPICE_WIDGET="$APPDIR/usr/share/eSim/src/ngspiceSimulation/NgspiceWidget.py"
    if [ -f "$NGSPICE_WIDGET" ]; then
        progress "Patching NgspiceWidget.py for individual plot windows..."
        
        # Create the patching Python script
        cat > /tmp/patch_ngspice.py << 'PYPATCHSCRIPT'
import sys

widget_file = sys.argv[1]
try:
    with open(widget_file, 'r') as f:
        content = f.read()
    
    # Original code pattern to find
    old_pattern = '''            else:
                # For Linux: use .raw file in xterm and gaw
                raw_file = os.path.abspath(command.replace(".cir.out", ".raw"))
                commandi = f'cd "{projPath}"; ngspice -p "{raw_file}"'

                xtermArgs = ['-hold', '-e', commandi]'''
    
    # New code with proper ngspice plotting - INDIVIDUAL PLOTS for each signal
    # Parses raw file header to get vector names and creates separate plot for each
    new_code = '''            else:
                # For Linux: use .raw file in xterm with ngspice
                raw_file = os.path.abspath(command.replace(".cir.out", ".raw"))
                
                # Find bundled ngspice - check APPDIR first
                ngspice_bin = "ngspice"
                appdir = os.environ.get("APPDIR", "")
                if appdir:
                    bundled = os.path.join(appdir, "usr", "bin", "ngspice")
                    if os.path.isfile(bundled):
                        ngspice_bin = bundled
                
                # Parse raw file to get available vectors for individual plots
                vectors = []
                try:
                    with open(raw_file, 'rb') as rf:
                        in_header = True
                        for line in rf:
                            try:
                                line_str = line.decode('utf-8', errors='ignore').strip()
                            except:
                                in_header = False
                                break
                            if line_str.startswith('Variables:'):
                                continue
                            if line_str.startswith('Binary:') or line_str.startswith('Values:'):
                                in_header = False
                                break
                            # Parse vector lines like: "0   time    time"
                            parts = line_str.split()
                            if len(parts) >= 2 and parts[0].isdigit():
                                vec_name = parts[1]
                                if vec_name.lower() != 'time':
                                    vectors.append(vec_name)
                except Exception as e:
                    print(f"Warning: Could not parse raw file for vectors: {e}")
                    vectors = []
                
                # Create a proper ngspice control script with individual plots
                plot_script = raw_file.replace(".raw", "_plot.cir")
                with open(plot_script, 'w') as f:
                    f.write('* eSim Plot Script - Individual Plots\\n')
                    f.write('.control\\n')
                    f.write(f'load "{raw_file}"\\n')
                    if vectors:
                        # Create individual plot for each vector
                        for vec in vectors:
                            f.write(f'plot {vec}\\n')
                    else:
                        # Fallback to plot all if no vectors found
                        f.write('plot all\\n')
                    f.write('.endc\\n')
                    f.write('.end\\n')
                
                # Run ngspice directly with the control script file
                # Export PATH and LD_LIBRARY_PATH to ensure bundled ngspice-35 with X11 is found
                appdir_path = os.environ.get("APPDIR", "")
                if appdir_path:
                    env_export = f'export PATH="{appdir_path}/usr/bin:$PATH" && export LD_LIBRARY_PATH="{appdir_path}/usr/lib:{appdir_path}/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH" && '
                else:
                    env_export = ""
                # Suppress stderr (PrinterOnly warnings are cosmetic - plots still work)
                commandi = f'{env_export}cd "{projPath}" && "{ngspice_bin}" "{plot_script}" 2>/dev/null'

                xtermArgs = ['-hold', '-e', 'bash', '-c', commandi]'''
    
    if old_pattern in content:
        content = content.replace(old_pattern, new_code)
        with open(widget_file, 'w') as f:
            f.write(content)
        print("[eSim] Patched NgspiceWidget.py for individual plot windows")
    else:
        # Check if already patched with old 'plot all' version - update to individual plots
        if "'plot all\\\\n'" in content or "f.write('plot all\\\\n')" in content:
            # Replace 'plot all' with individual plots logic
            old_plot_all = "f.write('plot all\\\\n')"
            new_plot_individual = '''if vectors:
                        # Create individual plot for each vector
                        for vec in vectors:
                            f.write(f'plot {vec}\\\\n')
                    else:
                        # Fallback to plot all if no vectors found
                        f.write('plot all\\\\n')'''
            
            # Also need to add vector parsing before the plot script generation
            if "vectors = []" not in content:
                # Find the plot_script line and add vector parsing before it
                old_script_line = "plot_script = raw_file.replace(\".raw\", \"_plot.cir\")"
                new_with_parsing = '''# Parse raw file to get available vectors for individual plots
                vectors = []
                try:
                    with open(raw_file, 'rb') as rf:
                        in_header = True
                        for line in rf:
                            try:
                                line_str = line.decode('utf-8', errors='ignore').strip()
                            except:
                                in_header = False
                                break
                            if line_str.startswith('Variables:'):
                                continue
                            if line_str.startswith('Binary:') or line_str.startswith('Values:'):
                                in_header = False
                                break
                            parts = line_str.split()
                            if len(parts) >= 2 and parts[0].isdigit():
                                vec_name = parts[1]
                                if vec_name.lower() != 'time':
                                    vectors.append(vec_name)
                except Exception as e:
                    print(f"Warning: Could not parse raw file: {e}")
                    vectors = []
                
                plot_script = raw_file.replace(".raw", "_plot.cir")'''
                content = content.replace(old_script_line, new_with_parsing)
            
            if old_plot_all in content:
                content = content.replace(old_plot_all, new_plot_individual)
            with open(widget_file, 'w') as f:
                f.write(content)
            print("[eSim] Updated NgspiceWidget.py to use individual plot windows")
        else:
            print("[eSim] NgspiceWidget.py already patched or has different format")
except Exception as e:
    print(f"[eSim] Warning: Could not patch NgspiceWidget.py: {e}")
PYPATCHSCRIPT
        
        # Run the patching script
        python3 /tmp/patch_ngspice.py "$NGSPICE_WIDGET"
        rm -f /tmp/patch_ngspice.py
    fi
    
    # ═══ FIX MODEL EDITOR READ-ONLY FILESYSTEM ═══
    MODEL_EDITOR="$APPDIR/usr/share/eSim/src/modelEditor/ModelEditor.py"
    if [ -f "$MODEL_EDITOR" ]; then
        progress "Patching ModelEditor.py for writable user library..."
        
        # Create Python patching script
        cat > /tmp/patch_model_editor.py << 'MEPATCH'
import sys
import re

model_editor_file = sys.argv[1]
try:
    with open(model_editor_file, 'r') as f:
        content = f.read()
    
    modified = False
    
    # 1. Add imports for expanduser if not present
    if 'from os.path import expanduser' not in content and 'os.path.expanduser' not in content:
        # Add after existing os import
        content = content.replace('import os\n', 'import os\nfrom os.path import expanduser\n')
        modified = True
    
    # 2. Add the helper method FIRST (before adding the call to it)
    # Insert after the __init__ method ends (before the first other method)
    helper_method = '''
    def _ensure_user_lib_dirs(self):
        """Ensure user library directory structure exists for saving models."""
        subdirs = ['Diode', 'Transistor', 'MOS', 'JFET', 'IGBT', 'Misc', 'User Libraries']
        for subdir in subdirs:
            dir_path = os.path.join(self.user_lib_path, subdir)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path, exist_ok=True)

'''
    
    if 'def _ensure_user_lib_dirs' not in content:
        # Find the opennew method and insert helper before it
        search_str = chr(10) + '    def opennew(self):'
        if search_str in content:
            content = content.replace(search_str, helper_method + '    def opennew(self):')
            modified = True
    
    # 3. Replace the __init__ method to use user-writable paths (adds call to helper)
    # Find and replace the savepathtest initialization
    old_savepath = "self.savepathtest = self.init_path + 'library/deviceModelLibrary'"
    new_savepath = '''# Use user's home directory for writable model library
        self.user_lib_path = os.path.join(os.path.expanduser('~'), '.esim', 'deviceModelLibrary')
        self._ensure_user_lib_dirs()
        self.savepathtest = self.user_lib_path'''
    
    if old_savepath in content:
        content = content.replace(old_savepath, new_savepath)
        modified = True
    
    # 4. Fix createXML to use user_lib_path instead of init_path for saving
    old_savepath_create = "self.savepath = self.init_path + 'library/deviceModelLibrary'"
    new_savepath_create = "self.savepath = self.user_lib_path"
    
    if old_savepath_create in content:
        content = content.replace(old_savepath_create, new_savepath_create)
        modified = True
    
    # 5. Fix converttoxml (Upload) to use user_lib_path
    old_upload_path = "savepath = os.path.join(self.savepathtest, 'User Libraries')"
    new_upload_path = "savepath = os.path.join(self.user_lib_path, 'User Libraries')"
    
    if old_upload_path in content:
        content = content.replace(old_upload_path, new_upload_path)
        modified = True
    
    # 6. Fix savethefile to handle editing read-only bundled models
    # When editing a bundled model (read-only), save to user library instead
    old_savethefile = "def savethefile(self, editfile):"
    new_savethefile = '''def savethefile(self, editfile):
        # Check if file is in read-only location (bundled in AppImage)
        # If so, save to user's writable library instead
        import shutil
        xmlpath, file = os.path.split(editfile)
        filename = os.path.splitext(file)[0]
        
        # Check if source is writable
        if not os.access(xmlpath, os.W_OK):
            # Find component type from path
            for comp_type in ['Diode', 'Transistor', 'MOS', 'JFET', 'IGBT', 'Misc', 'User Libraries']:
                if comp_type in xmlpath:
                    new_dir = os.path.join(self.user_lib_path, comp_type)
                    if not os.path.exists(new_dir):
                        os.makedirs(new_dir, exist_ok=True)
                    xmlpath = new_dir
                    editfile = os.path.join(new_dir, file)
                    self.obj_appconfig.print_info(f'Saving edited model to user library: {editfile}')
                    break'''
    
    if old_savethefile in content and 'os.access(xmlpath, os.W_OK)' not in content:
        content = content.replace(old_savethefile, new_savethefile)
        modified = True
    
    if modified:
        with open(model_editor_file, 'w') as f:
            f.write(content)
        print("[eSim] Patched ModelEditor.py for user-writable library paths")
    else:
        print("[eSim] ModelEditor.py already patched or has different format")

except Exception as e:
    print(f"[eSim] Warning: Could not patch ModelEditor.py: {e}")
MEPATCH
        
        # Run the patching script
        python3 /tmp/patch_model_editor.py "$MODEL_EDITOR"
        rm -f /tmp/patch_model_editor.py
        ok "ModelEditor.py patched for user-writable library"
    fi
    
    # ═══ FIX MODEL EDITOR - REMOVE PROJECT REQUIREMENT ═══
    # DockArea.py requires project selection to open Model Editor
    # Patch it to allow Model Editor to work without a project
    DOCK_AREA="$APPDIR/usr/share/eSim/src/frontEnd/DockArea.py"
    if [ -f "$DOCK_AREA" ]; then
        progress "Patching DockArea.py to allow Model Editor without project..."
        
        cat > /tmp/patch_dockarea.py << 'DAPATCH'
import sys

dock_file = sys.argv[1]
try:
    with open(dock_file, 'r') as f:
        content = f.read()
    
    modified = False
    
    # Find and remove the project requirement check in modelEditor()
    # The original code is:
    # def modelEditor(self):
    #     ...
    #     projDir = self.obj_appconfig.current_project["ProjectName"]
    #     if projDir is None:
    #         self.msg = QtWidgets.QErrorMessage()
    #         ...
    #         return
    #     projName = os.path.basename(projDir)
    #     dockName = f'Model Editor-{projName}-'
    
    old_modeleditor = '''    def modelEditor(self):
        """This function defines UI for model editor."""
        print("in model editor")
        global count

        projDir = self.obj_appconfig.current_project["ProjectName"]
        if projDir is None:
            """ when projDir is None that is clicking on subcircuit icon
                without any project selection """
            self.msg = QtWidgets.QErrorMessage()
            self.msg.setModal(True)
            self.msg.setWindowTitle("Error Message")
            self.msg.showMessage(
                'Please select the project first.'
                ' You can either create new project or open existing project'
            )
            self.msg.exec_()
            return
        projName = os.path.basename(projDir)
        dockName = f'Model Editor-{projName}-\''''
    
    new_modeleditor = '''    def modelEditor(self):
        """This function defines UI for model editor."""
        print("in model editor")
        global count

        # Model Editor can work without a project - use generic dock name
        projDir = self.obj_appconfig.current_project["ProjectName"]
        if projDir is not None:
            projName = os.path.basename(projDir)
            dockName = f'Model Editor-{projName}-'
        else:
            dockName = 'Model Editor-\''''
    
    if old_modeleditor in content:
        content = content.replace(old_modeleditor, new_modeleditor)
        modified = True
    
    if modified:
        with open(dock_file, 'w') as f:
            f.write(content)
        print("[eSim] Patched DockArea.py - Model Editor works without project")
    else:
        print("[eSim] DockArea.py already patched or has different format")

except Exception as e:
    print(f"[eSim] Warning: Could not patch DockArea.py: {e}")
DAPATCH
        
        python3 /tmp/patch_dockarea.py "$DOCK_AREA"
        rm -f /tmp/patch_dockarea.py
        ok "DockArea.py patched - Model Editor works without project"
        
        # ═══ PATCH SUBCIRCUIT EDITOR TO WORK WITHOUT PROJECT ═══
        progress "Patching DockArea.py to allow Subcircuit Editor without project..."
        cat > /tmp/patch_dockarea_subcircuit.py << 'DASUBPATCH'
import sys

dock_file = sys.argv[1]
try:
    with open(dock_file, 'r') as f:
        content = f.read()
    
    modified = False
    
    # Find and patch the subcircuiteditor() function
    old_subcircuit = '''    def subcircuiteditor(self):
        """This function creates a widget for different subcircuit options."""
        global count

        projDir = self.obj_appconfig.current_project["ProjectName"]

        """ Checks projDir variable has valid value 
        & is not None before calling os.path.basename """

        if projDir is not None:
            projName = os.path.basename(projDir)
            dockName = f'Subcircuit-{projName}-'

            self.subcktWidget = QtWidgets.QWidget()
            self.subcktLayout = QtWidgets.QVBoxLayout()
            self.subcktLayout.addWidget(Subcircuit(self))

            self.subcktWidget.setLayout(self.subcktLayout)
            dock[dockName +
                str(count)] = QtWidgets.QDockWidget(dockName
                                                    + str(count))
            dock[dockName + str(count)] \\
                .setWidget(self.subcktWidget)
            self.addDockWidget(QtCore.Qt.TopDockWidgetArea,
                            dock[dockName + str(count)])
            self.tabifyDockWidget(dock['Welcome'],
                                dock[dockName + str(count)])

            # CSS
            dock[dockName + str(count)].setStyleSheet(" \\
            .QWidget { border-radius: 15px; border: 1px solid gray;\\
                padding: 5px; width: 200px; height: 150px;  } \\
            ")

            dock[dockName + str(count)].setVisible(True)
            dock[dockName + str(count)].setFocus()
            dock[dockName + str(count)].raise_()

            count = count + 1

        else:
            """ when projDir is None that is clicking on subcircuit icon
                without any project selection """
            self.msg = QtWidgets.QErrorMessage()
            self.msg.setModal(True)
            self.msg.setWindowTitle("Error Message")
            self.msg.showMessage(
                'Please select the project first.'
                ' You can either create new project or open existing project'
            )
            self.msg.exec_()'''
    
    new_subcircuit = '''    def subcircuiteditor(self):
        """This function creates a widget for different subcircuit options."""
        global count

        # Subcircuit Editor can work without a project
        projDir = self.obj_appconfig.current_project["ProjectName"]
        if projDir is not None:
            projName = os.path.basename(projDir)
            dockName = f'Subcircuit-{projName}-'
        else:
            dockName = 'Subcircuit-'

        self.subcktWidget = QtWidgets.QWidget()
        self.subcktLayout = QtWidgets.QVBoxLayout()
        self.subcktLayout.addWidget(Subcircuit(self))

        self.subcktWidget.setLayout(self.subcktLayout)
        dock[dockName +
            str(count)] = QtWidgets.QDockWidget(dockName
                                                + str(count))
        dock[dockName + str(count)] \\
            .setWidget(self.subcktWidget)
        self.addDockWidget(QtCore.Qt.TopDockWidgetArea,
                        dock[dockName + str(count)])
        self.tabifyDockWidget(dock['Welcome'],
                            dock[dockName + str(count)])

        # CSS
        dock[dockName + str(count)].setStyleSheet(" \\
        .QWidget { border-radius: 15px; border: 1px solid gray;\\
            padding: 5px; width: 200px; height: 150px;  } \\
        ")

        dock[dockName + str(count)].setVisible(True)
        dock[dockName + str(count)].setFocus()
        dock[dockName + str(count)].raise_()

        count = count + 1'''
    
    if old_subcircuit in content:
        content = content.replace(old_subcircuit, new_subcircuit)
        modified = True
    
    if modified:
        with open(dock_file, 'w') as f:
            f.write(content)
        print("[eSim] Patched DockArea.py - Subcircuit Editor works without project")
    else:
        print("[eSim] DockArea.py subcircuit already patched or has different format")

except Exception as e:
    print(f"[eSim] Warning: Could not patch DockArea.py subcircuit: {e}")
DASUBPATCH
        
        python3 /tmp/patch_dockarea_subcircuit.py "$DOCK_AREA"
        rm -f /tmp/patch_dockarea_subcircuit.py
        ok "DockArea.py patched - Subcircuit Editor works without project"
    fi
    
    # ═══ FIX NGVERI.PY - ENSURE CONFIG EXISTS BEFORE READING ═══
    NGVERI_FILE="$APPDIR/usr/share/eSim/src/maker/NgVeri.py"
    if [ -f "$NGVERI_FILE" ]; then
        progress "Patching NgVeri.py for robust config handling..."
        
        # Add config initialization code at the top of NgVeri __init__
        cat > /tmp/patch_ngveri.py << 'NGVERIPATCH'
import sys
import os

ngveri_file = sys.argv[1]
try:
    with open(ngveri_file, 'r') as f:
        content = f.read()
    
    # Check if already patched
    if '_check_config_has_src_section' in content:
        print("[eSim] NgVeri.py already patched")
        sys.exit(0)
    
    # Find the __init__ method after the parser.read line
    old_code = '''        self.parser = ConfigParser()
        self.parser.read(os.path.join(
            self.home, os.path.join('.nghdl', 'config.ini')))
        self.nghdl_home = self.parser.get('NGHDL', 'NGHDL_HOME')
        self.release_dir = self.parser.get('NGHDL', 'RELEASE')
        self.src_home = self.parser.get('SRC', 'SRC_HOME')
        self.licensefile = self.parser.get('SRC', 'LICENSE')
        self.digital_home = self.parser.get('NGHDL', 'DIGITAL_MODEL')'''
    
    new_code = '''        self.parser = ConfigParser()
        config_path = os.path.join(self.home, '.nghdl', 'config.ini')
        
        # Ensure config exists with all required sections for AppImage
        appdir = os.environ.get('APPDIR', '')
        nghdl_home_default = os.path.join(appdir, 'usr', 'share', 'eSim', 'nghdl') if appdir else ''
        
        if not os.path.exists(config_path) or not _check_config_has_src_section(config_path):
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
            # NgVeri.py adds /Ngveri to DIGITAL_MODEL, so DIGITAL_MODEL = icm (not icm/ghdl)
            digital_model_dir = os.path.join(self.home, 'nghdl-simulator', 'src', 'xspice', 'icm')
            os.makedirs(os.path.join(digital_model_dir, 'Ngveri'), exist_ok=True)
            os.makedirs(os.path.join(digital_model_dir, 'ghdl', 'ghdl'), exist_ok=True)
            # Create modpath.lst if not exists
            modpath_file = os.path.join(digital_model_dir, 'Ngveri', 'modpath.lst')
            if not os.path.exists(modpath_file):
                open(modpath_file, 'w').close()
            # Also create modpath.lst for ghdl models
            ghdl_modpath = os.path.join(digital_model_dir, 'ghdl', 'ghdl', 'modpath.lst')
            if not os.path.exists(ghdl_modpath):
                open(ghdl_modpath, 'w').close()
            # Build config content
            release_dir = os.path.join(appdir, 'usr', 'share', 'eSim', 'library', 'deviceModelLibrary', 'NGHDL') if appdir else ''
            src_home = os.path.join(self.home, 'nghdl-simulator', 'src')
            license_file = os.path.join(nghdl_home_default, 'LICENSE')
            
            # Smart GHDL detection: prefer SYSTEM GHDL over bundled
            # Reason: Bundled GHDL may require glibc 2.38 which older distros don't have
            # System GHDL is guaranteed to work with system libraries
            ghdl_path = ''
            ghdl_prefix = ''
            verilator_path = ''
            
            # Try system GHDL first (always compatible with system glibc)
            import shutil as _shutil
            for ghdl_cmd in ['ghdl-llvm', 'ghdl-mcode', 'ghdl']:
                found = _shutil.which(ghdl_cmd)
                if found:
                    ghdl_path = found
                    break
            # Find system GHDL prefix (check where ieee/ directory exists)
            if ghdl_path:
                for prefix_path in ['/usr/lib/ghdl/llvm/vhdl', '/usr/lib/ghdl/llvm', 
                                   '/usr/lib/ghdl/mcode/vhdl', '/usr/lib/ghdl/mcode',
                                   '/usr/local/lib/ghdl/llvm/vhdl', '/usr/local/lib/ghdl/llvm',
                                   '/usr/lib/ghdl']:
                    if os.path.isdir(os.path.join(prefix_path, 'ieee')):
                        ghdl_prefix = prefix_path
                        break
            
            # Fall back to bundled GHDL only if system GHDL not found
            if not ghdl_path and appdir and os.path.isfile(os.path.join(appdir, 'usr', 'bin', 'ghdl')):
                ghdl_path = os.path.join(appdir, 'usr', 'bin', 'ghdl')
                # Find correct prefix for bundled GHDL
                for prefix_suffix in ['llvm/vhdl', 'llvm', 'mcode/vhdl', 'mcode', '']:
                    test_prefix = os.path.join(appdir, 'usr', 'lib', 'ghdl', prefix_suffix) if prefix_suffix else os.path.join(appdir, 'usr', 'lib', 'ghdl')
                    if os.path.isdir(os.path.join(test_prefix, 'ieee')):
                        ghdl_prefix = test_prefix
                        break
            
            # Verilator detection (prefer system)
            verilator_path = _shutil.which('verilator') or ''
            if not verilator_path and appdir and os.path.isfile(os.path.join(appdir, 'usr', 'bin', 'verilator')):
                verilator_path = os.path.join(appdir, 'usr', 'bin', 'verilator')
            if not verilator_path:
                verilator_path = 'verilator'
            config_lines = [
                '[NGHDL]',
                'NGHDL_HOME = ' + nghdl_home_default,
                'DIGITAL_MODEL = ' + digital_model_dir,
                'RELEASE = ' + release_dir,
                '',
                '[SRC]',
                'SRC_HOME = ' + src_home,
                'LICENSE = ' + license_file,
                '',
                '[COMPILER]',
                'GHDL = ' + ghdl_path,
                'VERILATOR = ' + verilator_path,
                'GHDL_PREFIX = ' + ghdl_prefix,
                'MODEL_COMPILER = ' + ghdl_path,
            ]
            with open(config_path, 'w') as cf:
                cf.write('\\n'.join(config_lines))
        
        self.parser.read(config_path)
        self.nghdl_home = self.parser.get('NGHDL', 'NGHDL_HOME')
        self.release_dir = self.parser.get('NGHDL', 'RELEASE')
        self.src_home = self.parser.get('SRC', 'SRC_HOME')
        self.licensefile = self.parser.get('SRC', 'LICENSE')
        self.digital_home = self.parser.get('NGHDL', 'DIGITAL_MODEL')'''
    
    if old_code in content:
        # Define helper function as a module-level function (before the class)
        helper_func = '''
def _check_config_has_src_section(config_path):
    """Check if config file has SRC section"""
    try:
        from configparser import ConfigParser
        p = ConfigParser()
        p.read(config_path)
        return p.has_section('SRC')
    except:
        return False


'''
        # Find where to insert - after the imports, before the class
        class_def = "class NgVeri(QtWidgets.QWidget):"
        if class_def in content:
            # Insert the helper function right before the class definition
            content = content.replace(class_def, helper_func + class_def)
            content = content.replace(old_code, new_code)
            with open(ngveri_file, 'w') as f:
                f.write(content)
            print("[eSim] Patched NgVeri.py for robust config handling")
        else:
            print("[eSim] NgVeri.py class definition not found")
    else:
        print("[eSim] NgVeri.py has different format, skipping patch")

except Exception as e:
    print("[eSim] Warning: Could not patch NgVeri.py: " + str(e))
    import traceback
    traceback.print_exc()
NGVERIPATCH
        
        python3 /tmp/patch_ngveri.py "$NGVERI_FILE"
        rm -f /tmp/patch_ngveri.py
        ok "NgVeri.py patched for robust config handling"
    fi
    
    # ═══ FIX MODELGENERATION.PY - INCLUDE ALL VERILOG DEPENDENCY FILES IN VERILATOR ═══
    # When using "Add dependency folder", the dependency .v files are copied but not
    # included in the verilator command, causing "Cannot find module" errors.
    MODELGEN_FILE="$APPDIR/usr/share/eSim/src/maker/ModelGeneration.py"
    if [ -f "$MODELGEN_FILE" ]; then
        progress "Patching ModelGeneration.py to include all verilog dependencies in verilator..."
        
        cat > /tmp/patch_modelgen.py << 'MODELGENPATCH'
import sys
import os

modelgen_file = sys.argv[1]
try:
    with open(modelgen_file, 'r') as f:
        content = f.read()
    
    # Check if already patched
    if 'all_verilog_files' in content:
        print("[eSim] ModelGeneration.py already patched for verilog dependencies")
        sys.exit(0)
    
    # Find the run_verilator method and patch the verilator command to include all .v files
    # The original code builds the command with only self.fname:
    #   self.cmd = self.cmd + "verilator ... " + self.fname
    # We need to add all other .v files in the modelpath directory AND subdirectories
    # (because "Add dependency folder" may copy a complete folder as a subfolder)
    
    old_code = '''self.cmd = self.cmd + "verilator --stats -O3 -CFLAGS\\
         -O3 -LDFLAGS \\"-static\\" --x-assign fast \\
         --x-initial fast --noassert  --bbox-sys -Wall " + wno + "\\
         --cc --exe --no-MMD --Mdir . -CFLAGS\\
          -fPIC -output-split 0 sim_main_" + \\
            self.fname.split('.')[0] + ".cpp --autoflush  \\
            -DBSV_RESET_FIFO_HEAD -DBSV_RESET_FIFO_ARRAY  " + self.fname'''
    
    new_code = '''# Find all .v files in the model directory AND subdirectories
        # (dependency files from "Add dependency folder" may be in subfolders)
        all_verilog_files = []
        for root, dirs, files in os.walk(self.modelpath):
            for f in files:
                if f.endswith('.v') and f != self.fname:
                    # Get relative path from modelpath
                    rel_path = os.path.relpath(os.path.join(root, f), self.modelpath)
                    all_verilog_files.append(rel_path)
        verilog_files_str = ' '.join(all_verilog_files)
        if verilog_files_str:
            print("Including dependency verilog files: " + verilog_files_str)
        
        self.cmd = self.cmd + "verilator --stats -O3 -CFLAGS\\
         -O3 -LDFLAGS \\"-static\\" --x-assign fast \\
         --x-initial fast --noassert  --bbox-sys -Wall " + wno + "\\
         --cc --exe --no-MMD --Mdir . -CFLAGS\\
          -fPIC -output-split 0 sim_main_" + \\
            self.fname.split('.')[0] + ".cpp --autoflush  \\
            -DBSV_RESET_FIFO_HEAD -DBSV_RESET_FIFO_ARRAY  " + self.fname + " " + verilog_files_str'''
    
    if old_code in content:
        content = content.replace(old_code, new_code)
        with open(modelgen_file, 'w') as f:
            f.write(content)
        print("[eSim] Patched ModelGeneration.py to include all verilog dependencies in verilator")
    else:
        print("[eSim] ModelGeneration.py has different format, trying alternate patch...")
        # Try a simpler pattern match
        if 'DBSV_RESET_FIFO_ARRAY  " + self.fname' in content and 'all_verilog_files' not in content:
            # Insert the file discovery code before the verilator command
            old_simple = 'print("Running Verilator.............")'
            new_simple = '''print("Running Verilator.............")
        
        # Find all .v files in the model directory AND subdirectories
        # (dependency files from "Add dependency folder" may be in subfolders)
        all_verilog_files = []
        for root, dirs, files in os.walk(self.modelpath):
            for f in files:
                if f.endswith('.v') and f != self.fname:
                    rel_path = os.path.relpath(os.path.join(root, f), self.modelpath)
                    all_verilog_files.append(rel_path)
        verilog_files_str = ' '.join(all_verilog_files)
        if verilog_files_str:
            print("Including dependency verilog files: " + verilog_files_str)'''
            
            # Also update the verilator command to append verilog_files_str
            old_cmd_end = 'DBSV_RESET_FIFO_ARRAY  " + self.fname'
            new_cmd_end = 'DBSV_RESET_FIFO_ARRAY  " + self.fname + " " + verilog_files_str'
            
            if old_simple in content:
                content = content.replace(old_simple, new_simple)
                content = content.replace(old_cmd_end, new_cmd_end)
                with open(modelgen_file, 'w') as f:
                    f.write(content)
                print("[eSim] Patched ModelGeneration.py using alternate method")
            else:
                print("[eSim] Could not find insertion point for ModelGeneration.py patch")
        else:
            print("[eSim] ModelGeneration.py format not recognized")

except Exception as e:
    print("[eSim] Warning: Could not patch ModelGeneration.py: " + str(e))
    import traceback
    traceback.print_exc()
MODELGENPATCH
        
        python3 /tmp/patch_modelgen.py "$MODELGEN_FILE"
        rm -f /tmp/patch_modelgen.py
        ok "ModelGeneration.py patched for verilog dependency handling"
        
        # Also patch addfolder() to properly quote paths with spaces
        progress "Patching ModelGeneration.py addfolder() to handle paths with spaces..."
        
        cat > /tmp/patch_addfolder.py << 'ADDFOLDERPATCH'
import sys

modelgen_file = sys.argv[1]
try:
    with open(modelgen_file, 'r') as f:
        content = f.read()
    
    modified = False
    
    # Fix the cp -a command (copy contents only) - add quotes around paths
    old_cp_a = 'self.cmd = "cp -a " + includefolder + "/. " + self.modelpath'
    new_cp_a = 'self.cmd = "cp -a \'" + includefolder + "/.\' \'" + self.modelpath + "\'"'
    
    if old_cp_a in content:
        content = content.replace(old_cp_a, new_cp_a)
        modified = True
    
    # Fix the cp -R command (copy whole folder) - add quotes around paths
    old_cp_r = 'self.cmd = "cp -R " + includefolder + " " + self.modelpath'
    new_cp_r = 'self.cmd = "cp -R \'" + includefolder + "\' \'" + self.modelpath + "\'"'
    
    if old_cp_r in content:
        content = content.replace(old_cp_r, new_cp_r)
        modified = True
    
    if modified:
        with open(modelgen_file, 'w') as f:
            f.write(content)
        print("[eSim] Patched addfolder() to handle paths with spaces")
    else:
        print("[eSim] addfolder() already patched or has different format")

except Exception as e:
    print("[eSim] Warning: Could not patch addfolder(): " + str(e))
ADDFOLDERPATCH
        
        python3 /tmp/patch_addfolder.py "$MODELGEN_FILE"
        rm -f /tmp/patch_addfolder.py
        ok "ModelGeneration.py addfolder() patched for paths with spaces"
    fi

    # ═══ PATCH MODELGENERATION.PY TO COMPILE VERILATED.O AT RUNTIME ═══
    # This ensures cross-distro compatibility - verilated.o is compiled using
    # the TARGET system's g++/glibc instead of being bundled from build system
    if [ -f "$MODELGEN_FILE" ]; then
        progress "Patching ModelGeneration.py for runtime verilated.o compilation..."
        
        cat > /tmp/patch_verilated.py << 'VERILATEDPATCH'
import sys
import os

modelgen_file = sys.argv[1]
try:
    with open(modelgen_file, 'r') as f:
        content = f.read()
    
    # Check if already patched
    if 'ensure_verilated_o_compiled' in content:
        print("[eSim] ModelGeneration.py already patched for verilated.o")
        sys.exit(0)
    
    # Function to add - compiles verilated.o from system Verilator if missing
    helper_func = '''
def ensure_verilated_o_compiled():
    """Compile verilated.o from system Verilator if missing or incompatible.
    This ensures cross-distro compatibility by using target system's g++/glibc."""
    import os
    import subprocess
    home = os.path.expanduser("~")
    ngveri_path = os.path.join(home, "nghdl-simulator", "src", "xspice", "icm", "Ngveri")
    verilated_o = os.path.join(ngveri_path, "verilated.o")
    verilated_threads_o = os.path.join(ngveri_path, "verilated_threads.o")
    
    # Check if verilated.o exists and is compatible (check for glibc 2.38+ symbols)
    recompile = False
    if not os.path.exists(verilated_o):
        recompile = True
    else:
        # Check for incompatible glibc symbols
        try:
            result = subprocess.run(["strings", verilated_o], capture_output=True, text=True)
            if "__isoc23" in result.stdout:
                print("[NGHDL] verilated.o has incompatible glibc symbols, recompiling...")
                recompile = True
        except:
            pass
    
    if recompile:
        # Find Verilator include path
        verilator_includes = [
            "/usr/share/verilator/include",
            "/usr/local/share/verilator/include",
        ]
        verilator_inc = None
        for inc in verilator_includes:
            if os.path.exists(os.path.join(inc, "verilated.cpp")):
                verilator_inc = inc
                break
        
        if verilator_inc:
            print(f"[NGHDL] Compiling verilated.o from {verilator_inc}")
            os.makedirs(ngveri_path, exist_ok=True)
            try:
                subprocess.run(["g++", "-c", "-fPIC", f"-I{verilator_inc}",
                               os.path.join(verilator_inc, "verilated.cpp"),
                               "-o", verilated_o], check=True)
                subprocess.run(["g++", "-c", "-fPIC", f"-I{verilator_inc}",
                               os.path.join(verilator_inc, "verilated_threads.cpp"),
                               "-o", verilated_threads_o], check=True)
                print("[NGHDL] verilated.o compiled successfully")
            except Exception as e:
                print(f"[NGHDL] Warning: Could not compile verilated.o: {e}")
        else:
            print("[NGHDL] Warning: Verilator include path not found")

'''
    
    # Find run_verilator method and add call at the beginning
    import_marker = "from configparser import ConfigParser"
    if import_marker in content:
        # Insert helper function after imports
        content = content.replace(import_marker, import_marker + helper_func)
        
        # Find run_verilator method and add ensure call
        run_verilator_def = "def run_verilator(self):"
        if run_verilator_def in content:
            # Add call to ensure_verilated_o_compiled at start of run_verilator
            old_def = run_verilator_def
            new_def = run_verilator_def + '''
        # Ensure verilated.o is compiled for this system
        ensure_verilated_o_compiled()
'''
            content = content.replace(old_def, new_def)
            with open(modelgen_file, 'w') as f:
                f.write(content)
            print("[eSim] Patched ModelGeneration.py for runtime verilated.o compilation")
        else:
            print("[eSim] run_verilator() not found in ModelGeneration.py")
    else:
        print("[eSim] ModelGeneration.py has different format")

except Exception as e:
    print("[eSim] Warning: Could not patch verilated.o compile: " + str(e))
VERILATEDPATCH
        
        python3 /tmp/patch_verilated.py "$MODELGEN_FILE"
        rm -f /tmp/patch_verilated.py
        ok "ModelGeneration.py patched for runtime verilated.o compilation"
    fi

    # ═══ FIX SUBCIRCUIT EDITOR - REDIRECT TO USER-WRITABLE PATH ═══
    NEWSUB_FILE="$APPDIR/usr/share/eSim/src/subcircuit/newSub.py"
    if [ -f "$NEWSUB_FILE" ]; then
        progress "Patching newSub.py for user-writable SubcircuitLibrary..."
        
        # Patch to use ~/.esim/SubcircuitLibrary instead of read-only AppImage path
        cat > /tmp/patch_newsub.py << 'NEWSUBPATCH'
import sys
newsub_file = sys.argv[1]
try:
    with open(newsub_file, 'r') as f:
        content = f.read()
    
    # Replace the path construction to use user-writable directory
    old_code = '''        self.schematic_path = (
            os.path.join(
                os.path.abspath(init_path + 'library'),
                'SubcircuitLibrary',
                self.create_schematic))'''
    
    new_code = '''        # Use user-writable path for subcircuits
        user_subcircuit_lib = os.path.join(os.path.expanduser('~'), '.esim', 'SubcircuitLibrary')
        os.makedirs(user_subcircuit_lib, exist_ok=True)
        self.schematic_path = os.path.join(user_subcircuit_lib, self.create_schematic)'''
    
    if old_code in content:
        content = content.replace(old_code, new_code)
        with open(newsub_file, 'w') as f:
            f.write(content)
        print("[eSim] Patched newSub.py for user-writable SubcircuitLibrary")
    else:
        print("[eSim] newSub.py already patched or has different format")
except Exception as e:
    print("[eSim] Warning: Could not patch newSub.py: " + str(e))
NEWSUBPATCH
        python3 /tmp/patch_newsub.py "$NEWSUB_FILE"
        rm -f /tmp/patch_newsub.py
        ok "newSub.py patched for user-writable SubcircuitLibrary"
        
        # ═══ FIX EESCHEMA PATH TO USE BUNDLED KICAD 6 ═══
        progress "Patching newSub.py to use bundled KiCad 6 eeschema..."
        cat > /tmp/patch_newsub_eeschema.py << 'EESCHEMA_PATCH'
import sys
newsub_file = sys.argv[1]
try:
    with open(newsub_file, 'r') as f:
        content = f.read()
    
    # Replace the eeschema command to use APPDIR-aware path
    old_cmd = 'self.cmd = "eeschema " + self.schematic + ".sch"'
    
    new_cmd = '''# Use bundled KiCad 6 eeschema from AppImage if available
                appdir = os.environ.get('APPDIR', '')
                if appdir:
                    eeschema_path = os.path.join(appdir, 'usr', 'bin', 'eeschema')
                else:
                    eeschema_path = 'eeschema'
                self.cmd = eeschema_path + " " + self.schematic + ".sch"'''
    
    if old_cmd in content and "os.environ.get('APPDIR'" not in content:
        content = content.replace(old_cmd, new_cmd)
        with open(newsub_file, 'w') as f:
            f.write(content)
        print("[eSim] Patched newSub.py to use bundled KiCad 6 eeschema")
    else:
        print("[eSim] newSub.py eeschema already patched or has different format")
except Exception as e:
    print("[eSim] Warning: Could not patch newSub.py eeschema: " + str(e))
EESCHEMA_PATCH
        python3 /tmp/patch_newsub_eeschema.py "$NEWSUB_FILE"
        rm -f /tmp/patch_newsub_eeschema.py
        ok "newSub.py patched to use bundled KiCad 6 eeschema"
    fi
    
    # Patch uploadSub.py to use user-writable SubcircuitLibrary
    UPLOADSUB_FILE="$APPDIR/usr/share/eSim/src/subcircuit/uploadSub.py"
    if [ -f "$UPLOADSUB_FILE" ]; then
        cat > /tmp/patch_uploadsub.py << 'UPLOADSUBPATCH'
import sys
uploadsub_file = sys.argv[1]
try:
    with open(uploadsub_file, 'r') as f:
        content = f.read()
    
    # Replace the entire path construction to use user-writable directory
    old_code = '''subcircuit_path = os.path.join(
            os.path.abspath(init_path + 'library'),
            'SubcircuitLibrary', create_subcircuit
        )'''
    
    new_code = '''# Use user-writable subcircuit library instead of read-only AppImage path
        user_subcircuit_lib = os.path.join(os.path.expanduser('~'), '.esim', 'SubcircuitLibrary')
        os.makedirs(user_subcircuit_lib, exist_ok=True)
        subcircuit_path = os.path.join(user_subcircuit_lib, create_subcircuit)'''
    
    if old_code in content:
        content = content.replace(old_code, new_code)
        with open(uploadsub_file, 'w') as f:
            f.write(content)
        print("[eSim] Patched uploadSub.py for user-writable SubcircuitLibrary")
    elif "'.esim', 'SubcircuitLibrary'" in content:
        print("[eSim] uploadSub.py already patched")
    else:
        print("[eSim] uploadSub.py has different format, skipping patch")
except Exception as e:
    print("[eSim] Warning: Could not patch uploadSub.py: " + str(e))
UPLOADSUBPATCH
        python3 /tmp/patch_uploadsub.py "$UPLOADSUB_FILE"
        rm -f /tmp/patch_uploadsub.py
        ok "uploadSub.py patched"
    fi
    
    # Patch openSub.py to look in ~/.esim/SubcircuitLibrary
    OPENSUB_FILE="$APPDIR/usr/share/eSim/src/subcircuit/openSub.py"
    if [ -f "$OPENSUB_FILE" ]; then
        cat > /tmp/patch_opensub.py << 'OPENSUBPATCH'
import sys
opensub_file = sys.argv[1]
try:
    with open(opensub_file, 'r') as f:
        content = f.read()
    
    # Replace the path in getExistingDirectory to use user path
    old_code = '''                None, "Open File", init_path + "library/SubcircuitLibrary"'''
    
    new_code = '''                None, "Open File", os.path.join(os.path.expanduser('~'), '.esim', 'SubcircuitLibrary')'''
    
    if old_code in content:
        content = content.replace(old_code, new_code)
        with open(opensub_file, 'w') as f:
            f.write(content)
        print("[eSim] Patched openSub.py for user SubcircuitLibrary")
    else:
        print("[eSim] openSub.py already patched or has different format")
except Exception as e:
    print("[eSim] Warning: Could not patch openSub.py: " + str(e))
OPENSUBPATCH
        python3 /tmp/patch_opensub.py "$OPENSUB_FILE"
        rm -f /tmp/patch_opensub.py
        ok "openSub.py patched for user SubcircuitLibrary"
        
        # ═══ FIX EESCHEMA PATH IN OPENSUB.PY TO USE BUNDLED KICAD 6 ═══
        progress "Patching openSub.py to use bundled KiCad 6 eeschema..."
        cat > /tmp/patch_opensub_eeschema.py << 'OPENSUB_EESCHEMA_PATCH'
import sys
opensub_file = sys.argv[1]
try:
    with open(opensub_file, 'r') as f:
        content = f.read()
    
    # Replace the eeschema command to use APPDIR-aware path
    old_cmd = 'self.cmd = "eeschema " + self.editfile + ".sch "'
    
    new_cmd = '''# Use bundled KiCad 6 eeschema from AppImage if available
            appdir = os.environ.get('APPDIR', '')
            if appdir:
                eeschema_path = os.path.join(appdir, 'usr', 'bin', 'eeschema')
            else:
                eeschema_path = 'eeschema'
            self.cmd = eeschema_path + " " + self.editfile + ".sch "'''
    
    if old_cmd in content and "os.environ.get('APPDIR'" not in content:
        content = content.replace(old_cmd, new_cmd)
        with open(opensub_file, 'w') as f:
            f.write(content)
        print("[eSim] Patched openSub.py to use bundled KiCad 6 eeschema")
    else:
        print("[eSim] openSub.py eeschema already patched or has different format")
except Exception as e:
    print("[eSim] Warning: Could not patch openSub.py eeschema: " + str(e))
OPENSUB_EESCHEMA_PATCH
        python3 /tmp/patch_opensub_eeschema.py "$OPENSUB_FILE"
        rm -f /tmp/patch_opensub_eeschema.py
        ok "openSub.py patched to use bundled KiCad 6 eeschema"
    fi
    
    # ═══ PATCH OPENPROJECT.PY FOR LEGACY PROJECT SUPPORT ═══
    progress "Patching openProject.py for legacy KiCad 5 project support..."
    OPENPROJECT_FILE="$APPDIR/usr/share/eSim/src/projManagement/openProject.py"
    if [ -f "$OPENPROJECT_FILE" ]; then
        cat > /tmp/patch_openproject_legacy.py << 'OPENPROJECT_LEGACY_PATCH'
import sys
import re
filepath = sys.argv[1]
with open(filepath, 'r') as f:
    content = f.read()

# Check if already patched
if 'setup_legacy_project_libs' in content:
    print("[eSim] openProject.py already has legacy project support")
    sys.exit(0)

# Add import for subprocess at top
if 'import subprocess' not in content:
    content = content.replace('import os', 'import os\nimport subprocess\nimport re')

# Add function to setup legacy project libraries with RESCUE support
legacy_support_code = '''
def setup_legacy_project_libs(project_dir):
    """Create project-specific sym-lib-table and rescue library for legacy KiCad 5 projects"""
    import glob
    if not project_dir or not os.path.isdir(project_dir):
        return
    
    # Check for legacy .sch files
    sch_files = glob.glob(os.path.join(project_dir, "*.sch"))
    sym_lib_table = os.path.join(project_dir, "sym-lib-table")
    
    if not sch_files:
        return
    
    # Check if it's a legacy format schematic
    for sch_file in sch_files:
        try:
            with open(sch_file, 'r') as f:
                sch_content = f.read()
                if 'EESchema Schematic' not in sch_content:
                    continue
                    
                print("[eSim] Legacy KiCad 5 project detected...")
                
                # Extract all symbol names used in the schematic
                symbol_refs = re.findall(r'^L\\s+(\\S+)\\s+', sch_content, re.MULTILINE)
                needed_symbols = set(symbol_refs)
                print(f"[eSim] Schematic needs symbols: {needed_symbols}")
                
                # Get eSim library path from environment
                esim_root = os.environ.get('ESIM_ROOT', '')
                esim_lib = os.path.join(esim_root, 'library') if esim_root else ''
                user_nghdl = os.path.expanduser('~/.esim/symbols/eSim_Nghdl.kicad_sym')
                kicad_symbols = os.environ.get('KICAD_SYMBOL_DIR', '')
                
                # Create rescue library with all needed symbols
                rescue_lib_path = os.path.join(project_dir, f"{os.path.basename(project_dir)}-rescue.kicad_sym")
                rescue_symbols = []
                found_symbols = {}
                
                # Search for symbols in all available libraries
                search_libs = []
                if esim_lib and os.path.isdir(esim_lib):
                    search_libs.extend(glob.glob(os.path.join(esim_lib, '*.kicad_sym')))
                if os.path.exists(user_nghdl):
                    search_libs.append(user_nghdl)
                if kicad_symbols and os.path.isdir(kicad_symbols):
                    search_libs.extend(glob.glob(os.path.join(kicad_symbols, '*.kicad_sym')))
                
                for lib_path in search_libs:
                    try:
                        with open(lib_path, 'r') as lf:
                            lib_content = lf.read()
                            for sym_name in needed_symbols:
                                if sym_name in found_symbols:
                                    continue
                                # Look for symbol definition
                                pattern = rf'\\(symbol\\s+"{re.escape(sym_name)}"\\s+'
                                if re.search(pattern, lib_content):
                                    # Extract the full symbol definition
                                    start = lib_content.find(f'(symbol "{sym_name}"')
                                    if start >= 0:
                                        # Find matching closing paren
                                        depth = 0
                                        end = start
                                        for i, c in enumerate(lib_content[start:]):
                                            if c == '(':
                                                depth += 1
                                            elif c == ')':
                                                depth -= 1
                                                if depth == 0:
                                                    end = start + i + 1
                                                    break
                                        sym_def = lib_content[start:end]
                                        rescue_symbols.append(sym_def)
                                        found_symbols[sym_name] = lib_path
                                        print(f"[eSim] Found symbol '{sym_name}' in {os.path.basename(lib_path)}")
                    except Exception as e:
                        pass
                
                # Write rescue library
                if rescue_symbols:
                    with open(rescue_lib_path, 'w') as rf:
                        rf.write('(kicad_symbol_lib (version 20211014) (generator eSim_rescue)\\n')
                        for sym in rescue_symbols:
                            rf.write(sym + '\\n')
                        rf.write(')\\n')
                    print(f"[eSim] Created rescue library with {len(rescue_symbols)} symbols")
                
                # Create or update sym-lib-table
                libs = []
                
                # Add rescue library first (highest priority)
                if os.path.exists(rescue_lib_path):
                    rescue_name = os.path.basename(project_dir) + "-rescue"
                    libs.append(f'  (lib (name "{rescue_name}")(type "KiCad")(uri "{rescue_lib_path}")(options "")(descr "Rescue Library"))')
                
                # Add eSim libraries
                if esim_lib and os.path.isdir(esim_lib):
                    for lib in glob.glob(os.path.join(esim_lib, 'eSim_*.kicad_sym')):
                        name = os.path.basename(lib).replace('.kicad_sym', '')
                        libs.append(f'  (lib (name "{name}")(type "KiCad")(uri "{lib}")(options "")(descr "eSim Library"))')
                
                # Add user NGHDL library
                if os.path.exists(user_nghdl):
                    libs.append(f'  (lib (name "eSim_Nghdl_User")(type "KiCad")(uri "{user_nghdl}")(options "")(descr "User NGHDL Symbols"))')
                
                # Add user NgVeri library
                user_ngveri = os.path.expanduser('~/.esim/symbols/eSim_Ngveri.kicad_sym')
                if os.path.exists(user_ngveri):
                    libs.append(f'  (lib (name "eSim_Ngveri_User")(type "KiCad")(uri "{user_ngveri}")(options "")(descr "User NgVeri Symbols"))')
                
                if libs:
                    with open(sym_lib_table, 'w') as f:
                        f.write("(sym_lib_table\\n")
                        f.write("\\n".join(libs))
                        f.write("\\n)\\n")
                    print("[eSim] Created project sym-lib-table for legacy project")
                
                # Report missing symbols
                missing = needed_symbols - set(found_symbols.keys())
                if missing:
                    print(f"[eSim] WARNING: Could not find symbols: {missing}")
                    print("[eSim] You may need to use KiCad's Rescue Symbols feature")
                
                break
        except Exception as e:
            print(f"[eSim] Warning: Could not process schematic: {e}")
            import traceback
            traceback.print_exc()


'''

# Insert the function before the class definition
content = content.replace('class OpenProjectInfo', legacy_support_code + 'class OpenProjectInfo')

# Add call to setup_legacy_project_libs after project validation
old_code = "self.obj_Appconfig.current_project['ProjectName'] = str(\n                self.projDir)"
new_code = '''self.obj_Appconfig.current_project['ProjectName'] = str(
                self.projDir)
            # Setup legacy project library support
            setup_legacy_project_libs(self.projDir)'''

if old_code in content:
    content = content.replace(old_code, new_code)
    print("[eSim] Patched openProject.py with legacy project support")
else:
    print("[eSim] openProject.py has different format, trying alternate patch...")
    # Try alternate pattern
    alt_old = "self.obj_Appconfig.current_project['ProjectName'] = str("
    if alt_old in content:
        # Find and patch after project name assignment
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if "current_project['ProjectName']" in line and 'projDir' in line:
                # Add call after this line (may be multi-line assignment)
                for j in range(i, min(i+3, len(lines))):
                    if 'projDir)' in lines[j]:
                        indent = len(lines[j]) - len(lines[j].lstrip())
                        lines.insert(j+1, ' ' * indent + '# Setup legacy project library support')
                        lines.insert(j+2, ' ' * indent + 'setup_legacy_project_libs(self.projDir)')
                        content = '\n'.join(lines)
                        print("[eSim] Patched openProject.py with legacy project support (alternate)")
                        break
                break

with open(filepath, 'w') as f:
    f.write(content)
OPENPROJECT_LEGACY_PATCH
        python3 /tmp/patch_openproject_legacy.py "$OPENPROJECT_FILE"
        rm -f /tmp/patch_openproject_legacy.py
        ok "openProject.py patched for legacy KiCad 5 project support"
    fi
    
    # ═══ PATCH MODELICAUI.PY FOR AUTO-DETECTION OF OPENMODELICA PATH ═══
    progress "Patching ModelicaUI.py for auto-detection of OpenModelica path..."
    MODELICA_UI_FILE="$APPDIR/usr/share/eSim/src/ngspicetoModelica/ModelicaUI.py"
    if [ -f "$MODELICA_UI_FILE" ]; then
        cat > /tmp/patch_modelicaui.py << 'MODELICAUIPATCH'
import sys
import os

modelica_ui_file = sys.argv[1]
try:
    with open(modelica_ui_file, 'r') as f:
        content = f.read()
    
    # Check if already patched
    if 'AUTO_DETECT_OMEDIT' in content:
        print("[eSim] ModelicaUI.py already patched")
        sys.exit(0)
    
    modified = False
    
    # 1. Add auto-detection helper function after imports
    imports_end = "BROWSE_LOCATION = '/home'"
    auto_detect_func = '''BROWSE_LOCATION = '/home'

# AUTO_DETECT_OMEDIT - Patched for AppImage compatibility
def _find_omedit():
    """Auto-detect OpenModelica OMEdit installation path."""
    import shutil
    
    # First check if running from AppImage - bundled OMEdit takes priority
    appdir = os.environ.get('APPDIR', '')
    if appdir:
        appimage_omedit = os.path.join(appdir, 'usr', 'bin', 'OMEdit')
        if os.path.isfile(appimage_omedit) and os.access(appimage_omedit, os.X_OK):
            return os.path.join(appdir, 'usr', 'bin')
    
    # Common OMEdit locations to search
    search_paths = [
        # System-wide installations
        '/usr/bin',
        '/usr/local/bin',
        '/opt/openmodelica/bin',
        '/opt/OpenModelica/bin',
        # User installations
        os.path.expanduser('~/.local/bin'),
        os.path.expanduser('~/OpenModelica/bin'),
        # Flatpak/Snap
        '/var/lib/flatpak/exports/bin',
        os.path.expanduser('~/.local/share/flatpak/exports/bin'),
        '/snap/bin',
    ]
    
    # Check OPENMODELICAHOME environment variable
    om_home = os.environ.get('OPENMODELICAHOME', '')
    if om_home:
        om_bin = os.path.join(om_home, 'bin')
        if os.path.isdir(om_bin):
            search_paths.insert(0, om_bin)
    
    # Also check PATH
    path_dirs = os.environ.get('PATH', '').split(':')
    search_paths.extend(path_dirs)
    
    # Try to find OMEdit in these paths
    for search_dir in search_paths:
        if not search_dir or not os.path.isdir(search_dir):
            continue
        omedit_path = os.path.join(search_dir, 'OMEdit')
        if os.path.isfile(omedit_path) and os.access(omedit_path, os.X_OK):
            return os.path.dirname(omedit_path)
    
    # Try using shutil.which as fallback
    omedit = shutil.which('OMEdit')
    if omedit:
        return os.path.dirname(omedit)
    
    return ''

'''
    
    if imports_end in content:
        content = content.replace(imports_end, auto_detect_func)
        modified = True
    
    # 2. Initialize self.OMPath in __init__ with auto-detected path
    old_init_ompathtext = '''        self.OMPathtext = QtWidgets.QLineEdit()
        self.OMPathtext.setText("")'''
    
    new_init_ompathtext = '''        # Auto-detect OpenModelica path
        self.OMPath = _find_omedit()
        self.OMPathtext = QtWidgets.QLineEdit()
        self.OMPathtext.setText(self.OMPath if self.OMPath else "(OpenModelica not found - please browse)")'''
    
    if old_init_ompathtext in content:
        content = content.replace(old_init_ompathtext, new_init_ompathtext)
        modified = True
    
    # 3. Update OMPathbrowseFile to also set self.OMPath
    old_browse = '''    def OMPathbrowseFile(self):
        temp = QtCore.QDir.toNativeSeparators(
            QtWidgets.QFileDialog.getExistingDirectory(
                self, "Open OpenModelica Directory", "home"
            )
        )

        if temp:
            self.OMPath = temp
            self.OMPathtext.setText(self.OMPath)'''
    
    new_browse = '''    def OMPathbrowseFile(self):
        # Start from current OMPath or /usr
        start_dir = self.OMPath if self.OMPath and os.path.isdir(self.OMPath) else "/usr"
        temp = QtCore.QDir.toNativeSeparators(
            QtWidgets.QFileDialog.getExistingDirectory(
                self, "Open OpenModelica Directory (containing OMEdit)", start_dir
            )
        )

        if temp:
            self.OMPath = temp
            self.OMPathtext.setText(self.OMPath)'''
    
    if old_browse in content:
        content = content.replace(old_browse, new_browse)
        modified = True
    
    # 4. Fix callOMEdit to handle missing OMEdit gracefully AND properly quote paths with spaces
    old_call_omedit = '''    def callOMEdit(self):

        try:
            modelFiles = glob.glob(self.modelicaNetlist)
            modelFiles = ' '.join(file for file in modelFiles)
            self.cmd2 = self.OMPath+"/OMEdit " + modelFiles'''
    
    new_call_omedit = '''    def callOMEdit(self):

        try:
            # Validate OMEdit exists
            if not self.OMPath:
                raise FileNotFoundError("OpenModelica path not set")
            
            omedit_bin = os.path.join(self.OMPath, "OMEdit")
            if not os.path.isfile(omedit_bin):
                raise FileNotFoundError(f"OMEdit not found at: {omedit_bin}")
            
            modelFiles = glob.glob(self.modelicaNetlist)
            # Quote each file path to handle spaces and special characters
            modelFiles = ' '.join(f'"{file}"' for file in modelFiles)
            self.cmd2 = f'"{omedit_bin}" {modelFiles}' '''
    
    if old_call_omedit in content:
        content = content.replace(old_call_omedit, new_call_omedit)
        modified = True
    
    # Also try to patch if already partially patched (without path quoting)
    old_call_omedit_v2 = '''            modelFiles = glob.glob(self.modelicaNetlist)
            modelFiles = ' '.join(file for file in modelFiles)
            self.cmd2 = omedit_bin + " " + modelFiles'''
    
    new_call_omedit_v2 = '''            modelFiles = glob.glob(self.modelicaNetlist)
            # Quote each file path to handle spaces and special characters
            modelFiles = ' '.join(f'"{file}"' for file in modelFiles)
            self.cmd2 = f'"{omedit_bin}" {modelFiles}' '''
    
    if old_call_omedit_v2 in content:
        content = content.replace(old_call_omedit_v2, new_call_omedit_v2)
        modified = True
    
    if modified:
        with open(modelica_ui_file, 'w') as f:
            f.write(content)
        print("[eSim] Patched ModelicaUI.py for auto-detection of OpenModelica path")
    else:
        print("[eSim] ModelicaUI.py already patched or has different format")

except Exception as e:
    print(f"[eSim] Warning: Could not patch ModelicaUI.py: {e}")
    import traceback
    traceback.print_exc()
MODELICAUIPATCH
        python3 /tmp/patch_modelicaui.py "$MODELICA_UI_FILE"
        rm -f /tmp/patch_modelicaui.py
        ok "ModelicaUI.py patched for auto-detection of OpenModelica path"
    fi
    
    # Patch Worker.py to use shlex.split() instead of str.split() for proper handling of quoted paths
    WORKER_PY="$APPDIR/usr/share/eSim/src/projManagement/Worker.py"
    if [ -f "$WORKER_PY" ]; then
        # Add shlex import if not present
        if ! grep -q "import shlex" "$WORKER_PY"; then
            sed -i 's/^import subprocess$/import subprocess\nimport shlex/' "$WORKER_PY"
        fi
        # Replace command.split() with shlex.split(command) for proper quote handling
        sed -i 's/proc = subprocess.Popen(command.split())/proc = subprocess.Popen(shlex.split(command))/' "$WORKER_PY"
        ok "Worker.py patched to handle quoted paths with shlex.split()"
    fi
    
    # Python path patching - Use ORIGINAL source file, not the one that might be already patched in AppDir
    ORIGINAL_APP_PY="$DL/eSim-${ESIM_VERSION}/src/frontEnd/Application.py"
    TARGET_APP_PY="$APPDIR/usr/share/eSim/src/frontEnd/Application.py"
    if [ -f "$ORIGINAL_APP_PY" ]; then
        cat > "$TARGET_APP_PY" <<'PYCODE'
#!/usr/bin/env python3
import os, sys
_script_dir = os.path.dirname(os.path.abspath(__file__))
_esim_root = os.path.dirname(os.path.dirname(_script_dir))
ESIM_IMAGE_PATH = os.path.join(_esim_root, 'images')
ESIM_LIBRARY_PATH = os.path.join(_esim_root, 'library')
_original_join = os.path.join

def _fix_path(path):
    if not path or not isinstance(path, str) or os.path.exists(path): return path
    basename = os.path.basename(path)
    if any(x in path for x in ['.html', 'browser', 'library']):
        for loc in [_original_join(ESIM_LIBRARY_PATH, 'browser', basename), _original_join(_esim_root, 'library', 'browser', basename)]:
            if os.path.exists(loc): return loc
    if any(ext in path.lower() for ext in ['.png', '.jpg', '.svg', '.ico', '.gif']):
        for loc in [_original_join(ESIM_IMAGE_PATH, basename), _original_join(ESIM_IMAGE_PATH, 'browser', basename)]:
            if os.path.exists(loc): return loc
    if '../' in path or './' in path:
        clean_path = path.replace('../', '').replace('./', '')
        for loc in [_original_join(_esim_root, clean_path), _original_join(os.path.dirname(_script_dir), clean_path)]:
            if os.path.exists(loc): return loc
    return path

os.path.join = lambda *args: _fix_path(_original_join(*args))

try:
    from PyQt5.QtGui import QPixmap as _OrigQPixmap, QIcon as _OrigQIcon
    from PyQt5.QtCore import QUrl as _OrigQUrl
    class QPixmap(_OrigQPixmap):
        def __init__(self, *args, **kwargs):
            if args and isinstance(args[0], str): args = (_fix_path(args[0]),) + args[1:]
            super().__init__(*args, **kwargs)
        def load(self, fileName, *args, **kwargs): return super().load(_fix_path(fileName), *args, **kwargs)
    class QIcon(_OrigQIcon):
        def __init__(self, *args, **kwargs):
            if args and isinstance(args[0], str): args = (_fix_path(args[0]),) + args[1:]
            super().__init__(*args, **kwargs)
        def addFile(self, fileName, *args, **kwargs): return super().addFile(_fix_path(fileName), *args, **kwargs)
    class QUrl(_OrigQUrl):
        def __init__(self, *args, **kwargs):
            if args and isinstance(args[0], str):
                fixed = _fix_path(args[0])
                if not fixed.startswith(('file://', 'http')) and os.path.isabs(fixed): fixed = 'file://' + fixed
                args = (fixed,) + args[1:]
            super().__init__(*args, **kwargs)
        @staticmethod
        def fromLocalFile(localFile): return _OrigQUrl.fromLocalFile(_fix_path(localFile))
    import PyQt5.QtGui, PyQt5.QtCore
    PyQt5.QtGui.QPixmap = QPixmap; PyQt5.QtGui.QIcon = QIcon; PyQt5.QtCore.QUrl = QUrl
    sys.modules['PyQt5.QtGui'].QPixmap = QPixmap; sys.modules['PyQt5.QtGui'].QIcon = QIcon; sys.modules['PyQt5.QtCore'].QUrl = QUrl
    # Also override in QtWidgets for splash screen
    import PyQt5.QtWidgets
    _OrigQSplashScreen = PyQt5.QtWidgets.QSplashScreen
    class QSplashScreen(_OrigQSplashScreen):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
    PyQt5.QtWidgets.QSplashScreen = QSplashScreen; sys.modules['PyQt5.QtWidgets'].QSplashScreen = QSplashScreen
except ImportError: pass

# Override init_path at module level - will be used by splash screen
_esim_init_path = _esim_root + os.sep

PYCODE
        # Append the ORIGINAL source file (not the already-patched one in AppDir)
        grep -v "^#!/" "$ORIGINAL_APP_PY" >> "$TARGET_APP_PY" 2>/dev/null || \
            cat "$ORIGINAL_APP_PY" >> "$TARGET_APP_PY"
        
        # Patch init_path to use absolute path from our _esim_init_path variable
        # This ensures splash screen and icons load correctly in AppImage
        sed -i "s/init_path = '\\.\\.\\/'/_orig_init_path = '..\\//g" "$TARGET_APP_PY"
        sed -i "s/init_path = ''/_orig_init_path = ''/g" "$TARGET_APP_PY"
        # Make init_path use our absolute path
        sed -i "/^[[:space:]]*_orig_init_path = /a\\    init_path = _esim_init_path" "$TARGET_APP_PY"
        
        chmod +x "$TARGET_APP_PY"
    fi
    
    [ -f "$APPDIR/usr/share/eSim/images/logo.png" ] && {
        # Install icon at multiple sizes for proper taskbar/dock display
        for size in 48 128 256; do
            mkdir -p "$APPDIR/usr/share/icons/hicolor/${size}x${size}/apps"
            if command -v convert >/dev/null 2>&1; then
                convert "$APPDIR/usr/share/eSim/images/logo.png" -resize ${size}x${size} \
                    "$APPDIR/usr/share/icons/hicolor/${size}x${size}/apps/eSim.png" 2>/dev/null || \
                    cp "$APPDIR/usr/share/eSim/images/logo.png" "$APPDIR/usr/share/icons/hicolor/${size}x${size}/apps/eSim.png"
            else
                cp "$APPDIR/usr/share/eSim/images/logo.png" "$APPDIR/usr/share/icons/hicolor/${size}x${size}/apps/eSim.png"
            fi
        done
        # Also copy to AppDir root for AppImage
        cp "$APPDIR/usr/share/eSim/images/logo.png" "$APPDIR/eSim.png"
        # Create .DirIcon symlink
        ln -sf eSim.png "$APPDIR/.DirIcon" 2>/dev/null || true
        ok "eSim icons installed at multiple sizes"
    }
    
    cp -r "$BUILD/venv/lib/python${PYVER}/site-packages/"* "$APPDIR/usr/lib/python${PYVER}/site-packages/"
    
    # ═══ REMOVE C-EXTENSION PACKAGES ═══
    # These packages contain compiled .so files that are Python-version-specific.
    # They WILL NOT work on systems with different Python versions (e.g. 3.11 vs 3.12).
    # Instead, we install them via pip at runtime to ~/.esim/python-packages/
    # This ensures the correct version is used for the host's Python interpreter.
    progress "Removing Python-version-specific packages (will be installed at runtime)..."
    
    # Packages with C extensions that must match Python version
    # NOTE: PIL is the actual package directory for Pillow
    C_EXT_PACKAGES="numpy scipy matplotlib lxml contourpy kiwisolver pillow PIL fontTools"
    
    for pkg in $C_EXT_PACKAGES; do
        # Remove from primary Python version
        rm -rf "$APPDIR/usr/lib/python${PYVER}/site-packages/${pkg}" \
               "$APPDIR/usr/lib/python${PYVER}/site-packages/${pkg}-"*.dist-info \
               "$APPDIR/usr/lib/python${PYVER}/site-packages/${pkg,,}" \
               "$APPDIR/usr/lib/python${PYVER}/site-packages/${pkg,,}-"*.dist-info \
               2>/dev/null || true
        # Also remove from ALL Python version directories
        for pyv in 3.8 3.9 3.10 3.11 3.12 3.13; do
            rm -rf "$APPDIR/usr/lib/python${pyv}/site-packages/${pkg}" \
                   "$APPDIR/usr/lib/python${pyv}/site-packages/${pkg}-"*.dist-info \
                   "$APPDIR/usr/lib/python${pyv}/site-packages/${pkg,,}" \
                   "$APPDIR/usr/lib/python${pyv}/site-packages/${pkg,,}-"*.dist-info \
                   2>/dev/null || true
        done
    done
    
    # Also remove the compiled .so files from any remaining packages
    find "$APPDIR/usr/lib/python${PYVER}/site-packages" -name "*.cpython-*.so" -delete 2>/dev/null || true
    
    ok "Removed C-extension packages (will be installed via pip at first run)"
    
    # ═══ MULTI-DISTRO PYTHON: Bundle pure-Python packages for other versions ═══
    # Compiled .so extensions are ABI-specific and won't work across Python versions.
    # Copy ONLY pure-Python packages (no .so files) to a fallback directory for
    # distros with different Python versions (e.g. Ubuntu 22.04 has 3.10, 24.04 has 3.12)
    for alt_py in 3.8 3.9 3.10 3.11 3.12 3.13; do
        [ "$alt_py" = "$PYVER" ] && continue
        alt_dir="$APPDIR/usr/lib/python${alt_py}/site-packages"
        mkdir -p "$alt_dir"
        # Copy only pure-Python packages (dirs without .so files)
        for pkg_dir in "$APPDIR/usr/lib/python${PYVER}/site-packages/"*/; do
            pkg_name=$(basename "$pkg_dir")
            # Skip dist-info, __pycache__, and packages with compiled extensions
            case "$pkg_name" in *.dist-info|*.egg-info|__pycache__) continue ;; esac
            if ! find "$pkg_dir" -name '*.so' -print -quit 2>/dev/null | grep -q .; then
                cp -r "$pkg_dir" "$alt_dir/" 2>/dev/null || true
            fi
        done
        # Copy standalone .py files (argparse.py, etc)
        cp "$APPDIR/usr/lib/python${PYVER}/site-packages/"*.py "$alt_dir/" 2>/dev/null || true
        cp "$APPDIR/usr/lib/python${PYVER}/site-packages/"*.pth "$alt_dir/" 2>/dev/null || true
    done
    ok "Pure-Python packages replicated for multi-distro support"
    mkdir -p "$APPDIR/usr/share/eSim/library/ngspicetoModelica"
    # Copy actual Mapping.json content (contains Sources, Devices, Components mappings)
    if [ -f "$APPDIR/usr/share/eSim/library/ngspicetoModelica/Mapping.json" ]; then
        cp "$APPDIR/usr/share/eSim/library/ngspicetoModelica/Mapping.json" "$APPDIR/usr/share/eSim/library/ngspicetoModelica/modelica_map.json"
    else
        # Fallback: Copy from source if available
        [ -f "$DL/eSim-${ESIM_VERSION}/library/ngspicetoModelica/Mapping.json" ] && \
            cp "$DL/eSim-${ESIM_VERSION}/library/ngspicetoModelica/Mapping.json" "$APPDIR/usr/share/eSim/library/ngspicetoModelica/modelica_map.json"
    fi
    
    # ═══════════════ FULL KICAD + ESIM LIBRARY INTEGRATION ═══════════════
    progress "Creating launcher with FULL KiCad + eSim library configuration..."
    cat > "$APPDIR/usr/bin/esim" <<'LAUNCHER'
#!/bin/bash
SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
HERE="$(dirname "$(dirname "$SCRIPT_DIR")")"

export APPDIR="$HERE"
export PATH="$HERE/usr/bin:$HOME/.local/bin:$PATH"

# ═══ SUPPRESS CONTAINER/MINIMAL ENVIRONMENT WARNINGS ═══
# Create machine-id if missing (prevents dconf warnings in containers)
if [ ! -f /etc/machine-id ]; then
    if command -v dbus-uuidgen >/dev/null 2>&1; then
        dbus-uuidgen --ensure=/etc/machine-id 2>/dev/null || true
    elif command -v systemd-machine-id-setup >/dev/null 2>&1; then
        systemd-machine-id-setup 2>/dev/null || true
    else
        # Fallback: generate a random machine-id
        cat /proc/sys/kernel/random/uuid 2>/dev/null | tr -d '-' > /etc/machine-id 2>/dev/null || true
    fi
fi
# Suppress accessibility bus warnings (not available in containers/headless)
export NO_AT_BRIDGE=1
# Set XDG_RUNTIME_DIR if not set (containers often lack this)
[ -z "$XDG_RUNTIME_DIR" ] && export XDG_RUNTIME_DIR="/tmp/runtime-$(id -u)" && mkdir -p "$XDG_RUNTIME_DIR" 2>/dev/null

# NOTE: Do NOT prepend $HERE/usr/lib here - AppRun already sets up filtered LD_LIBRARY_PATH
# Just add subdirectories that may need to be in the path
export LD_LIBRARY_PATH="$HERE/lib/x86_64-linux-gnu:$HERE/usr/lib/kicad:${LD_LIBRARY_PATH}"

# Dynamic Python version detection for multi-distro support
_PYVER=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")' 2>/dev/null || echo "3.10")
_BUNDLED_SITE=""
for _pv in $_PYVER 3.13 3.12 3.11 3.10 3.9 3.8; do
    [ -d "$HERE/usr/lib/python$_pv/site-packages" ] && _BUNDLED_SITE="$HERE/usr/lib/python$_pv/site-packages" && break
done
export PYTHONPATH="$HERE/usr/share/eSim/src:$_BUNDLED_SITE"

# ═══ SETUP NGHDL/NGVERI CONFIG ═══
# Create NGHDL config with consistent paths for both eSim and NGHDL
NGHDL_HOME_DIR="$HOME/.nghdl"
ESIM_NGHDL_HOME="$HERE/usr/share/eSim/nghdl"
SIMULATOR_ROOT="$HOME/nghdl-simulator"

# Extract simulator source if missing (tar.xz is inside nghdl folder)
# Check for configure script, not just icm directory (which may be created empty)
if [ ! -f "$SIMULATOR_ROOT/configure" ]; then
    echo "Extracting NGHDL simulator source to $SIMULATOR_ROOT..."
    rm -rf "$SIMULATOR_ROOT" 2>/dev/null || true
    mkdir -p "$SIMULATOR_ROOT"
    tar -xJf "$HERE/usr/share/eSim/nghdl/nghdl-simulator-source.tar.xz" -C "$HOME" 2>/dev/null || true
    if [ -d "$HOME/nghdl-simulator-source" ]; then
        cp -r "$HOME/nghdl-simulator-source"/* "$SIMULATOR_ROOT/" 2>/dev/null || true
        rm -rf "$HOME/nghdl-simulator-source"
        echo "[eSim] ✓ NGHDL simulator source extracted"
    fi
fi

# GCC 15+ (Fedora 43+) defaults to gnu23 which breaks ngspice-35 C code (bool keyword conflict)
_NGSPICE_CFLAGS=""
if command -v gcc >/dev/null 2>&1 && gcc -dumpversion 2>/dev/null | awk -F. '{exit ($1 >= 14) ? 0 : 1}'; then
    _NGSPICE_CFLAGS="-std=gnu17 -Wno-error=incompatible-pointer-types -Wno-error=int-conversion -Wno-error=implicit-function-declaration"
    export CFLAGS="$_NGSPICE_CFLAGS"
fi

# Configure nghdl-simulator to generate Makefiles if not already done
# Use --prefix to install code models to user-writable location instead of /usr/local
if [ -f "$SIMULATOR_ROOT/configure" ] && [ ! -f "$SIMULATOR_ROOT/src/xspice/icm/GNUmakefile" ]; then
    echo "Configuring NGHDL simulator (generating Makefiles)..."
    cd "$SIMULATOR_ROOT"
    CFLAGS="$_NGSPICE_CFLAGS" ./configure --with-ngshared --enable-xspice --disable-debug --prefix="$HOME/.nghdl/local" >/dev/null 2>&1 || true
    cd "$HERE"
fi

# Setup cmpp (Code Model PreProcessor) - REQUIRED for ICM compilation
# First try to use bundled cmpp binary, then fallback to building from source
CMPP_PATH="$SIMULATOR_ROOT/src/xspice/cmpp"
BUNDLED_CMPP="$HERE/usr/share/eSim/nghdl/bin/cmpp"

if [ -d "$CMPP_PATH" ] && [ ! -x "$CMPP_PATH/cmpp" ]; then
    if [ -x "$BUNDLED_CMPP" ]; then
        # Use bundled cmpp binary
        echo "[eSim] Installing bundled cmpp binary..."
        cp "$BUNDLED_CMPP" "$CMPP_PATH/cmpp"
        chmod +x "$CMPP_PATH/cmpp"
        echo "[eSim] ✓ cmpp installed from bundled binary"
    else
        # Fallback: try to build from source (requires build tools)
        echo "[eSim] Building cmpp from source (requires build-essential)..."
        cd "$CMPP_PATH"
        # Run autoreconf if needed to fix timestamp issues
        if command -v autoreconf >/dev/null 2>&1; then
            (cd "$SIMULATOR_ROOT" && autoreconf -fi >/dev/null 2>&1) || true
            (cd "$SIMULATOR_ROOT" && CFLAGS="$_NGSPICE_CFLAGS" ./configure --with-ngshared --enable-xspice --disable-debug --prefix="$HOME/.nghdl/local" >/dev/null 2>&1) || true
        fi
        CFLAGS="$_NGSPICE_CFLAGS" make >/dev/null 2>&1 || {
            echo "[eSim] Note: cmpp build failed."
            echo "[eSim]       Install build-essential and automake for full NGHDL support."
        }
        cd "$HERE"
    fi
fi

# Create the installation directory for code models (required by make install)
mkdir -p "$HOME/.nghdl/local/lib/ngspice"

# Create Ngveri directory at correct path (DIGITAL_MODEL/Ngveri where DIGITAL_MODEL = icm)
mkdir -p "$NGHDL_HOME_DIR" "$SIMULATOR_ROOT/src/xspice/icm/Ngveri" "$SIMULATOR_ROOT/src/xspice/icm/ghdl"
touch "$SIMULATOR_ROOT/src/xspice/icm/Ngveri/modpath.lst"
touch "$SIMULATOR_ROOT/src/xspice/icm/ghdl/modpath.lst"

# ═══ SETUP NGVERI VERILATED OBJECTS ═══
NGVERI_ICM_DIR="$SIMULATOR_ROOT/src/xspice/icm/Ngveri"
BUNDLED_VERILATED_DIR="$HERE/usr/share/eSim/nghdl/bin"

# Setup verilated_threads.o - try bundled first
if [ -d "$NGVERI_ICM_DIR" ] && [ ! -f "$NGVERI_ICM_DIR/verilated_threads.o" ]; then
    if [ -f "$BUNDLED_VERILATED_DIR/verilated_threads.o" ]; then
        cp "$BUNDLED_VERILATED_DIR/verilated_threads.o" "$NGVERI_ICM_DIR/"
        echo "[eSim] ✓ verilated_threads.o installed from bundled"
    else
        # Fallback: try to compile from source
        if command -v g++ >/dev/null 2>&1; then
            CXX_FLAGS="-std=c++17 -pthread"
            for inc_path in "$HERE/usr/share/verilator/include" "/usr/share/verilator/include"; do
                if [ -f "$inc_path/verilated_threads.cpp" ]; then
                    g++ -c -O3 -fPIC $CXX_FLAGS -I"$inc_path" "$inc_path/verilated_threads.cpp" \
                        -o "$NGVERI_ICM_DIR/verilated_threads.o" 2>/dev/null && \
                        echo "[eSim] verilated_threads.o compiled successfully" && break
                fi
            done
        fi
    fi
fi

# Setup verilated.o
if [ -d "$NGVERI_ICM_DIR" ] && [ ! -f "$NGVERI_ICM_DIR/verilated.o" ]; then
    if [ -f "$BUNDLED_VERILATED_DIR/verilated.o" ]; then
        cp "$BUNDLED_VERILATED_DIR/verilated.o" "$NGVERI_ICM_DIR/"
        echo "[eSim] ✓ verilated.o installed from bundled"
    fi
fi

cat > "$NGHDL_HOME_DIR/config.ini" << NGHDLCFG
[NGHDL]
NGHDL_HOME = $HOME/nghdl-simulator
DIGITAL_MODEL = $HOME/nghdl-simulator/src/xspice/icm
RELEASE = $HOME/nghdl-simulator

[SRC]
SRC_HOME = $HERE/usr/share/eSim/nghdl
LICENSE = $ESIM_NGHDL_HOME/LICENSE

[COMPILER]
GHDL = $HERE/usr/bin/ghdl
VERILATOR = $HERE/usr/bin/verilator
GHDL_PREFIX = $HERE/usr/lib/ghdl/llvm/vhdl
MODEL_COMPILER = $HERE/usr/bin/ghdl
NGHDLCFG

# ═══ GENERATE RUNTIME SPINIT WITH ABSOLUTE PATHS ═══
# Create spinit at runtime with resolved AppImage paths (critical for code model loading)
mkdir -p "$HOME/.esim"
RUNTIME_SPINIT="$HOME/.esim/spinit"

cat > "$RUNTIME_SPINIT" << SPINIT_HEADER
* Runtime-generated spinit for eSim AppImage
* Generated with absolute paths from: $HERE
alias exit quit
alias acct rusage all
set x11lineararcs
unset osdi_enabled

* Load code models with absolute AppImage paths (unconditionally)
SPINIT_HEADER

# Dynamically add all available code models from the AppImage
MODELS_DIR="$HERE/usr/lib/ngspice"
if [ -d "$MODELS_DIR" ]; then
    for cm in "$MODELS_DIR"/*.cm; do
        if [ -f "$cm" ]; then
            echo "codemodel $cm" >> "$RUNTIME_SPINIT"
        fi
    done
else
    # Fallback to hardcoded list if dir not found (unlikely in AppImage)
    for model in analog digital spice2poly xtradev xtraevt table; do
        [ -f "$HERE/usr/lib/ngspice/${model}.cm" ] && echo "codemodel $HERE/usr/lib/ngspice/${model}.cm" >> "$RUNTIME_SPINIT"
    done
fi


# Load NGHDL ghdl.cm from user's installation directory
# Check multiple possible locations where NGHDL might have installed ghdl.cm
NGHDL_CM_FOUND=""
for cm_path in \
    "$HOME/.nghdl/local/lib/ngspice/ghdl.cm" \
    "$HOME/.esim/nghdl/lib/ghdl.cm" \
    "$HOME/.nghdl/lib/ngspice/ghdl.cm" \
    "/usr/local/lib/ngspice/ghdl.cm"; do
    if [ -f "$cm_path" ]; then
        NGHDL_CM_FOUND="$cm_path"
        break
    fi
done

if [ -n "$NGHDL_CM_FOUND" ]; then
    echo "" >> "$RUNTIME_SPINIT"
    echo "* Load user NGHDL code model" >> "$RUNTIME_SPINIT"
    echo "codemodel $NGHDL_CM_FOUND" >> "$RUNTIME_SPINIT"
    echo "[eSim] Found NGHDL ghdl.cm at: $NGHDL_CM_FOUND" >&2
fi

# Load NgVeri code model (Ngveri.cm) for Verilog-based simulations
NGVERI_CM_FOUND=""
for cm_path in \
    "$HOME/.nghdl/local/lib/ngspice/Ngveri.cm" \
    "$HOME/.esim/ngveri/lib/Ngveri.cm" \
    "$HOME/.ngveri/lib/ngspice/Ngveri.cm" \
    "/usr/local/lib/ngspice/Ngveri.cm"; do
    if [ -f "$cm_path" ]; then
        NGVERI_CM_FOUND="$cm_path"
        break
    fi
done

if [ -n "$NGVERI_CM_FOUND" ]; then
    echo "" >> "$RUNTIME_SPINIT"
    echo "* Load user NgVeri code model" >> "$RUNTIME_SPINIT"
    echo "codemodel $NGVERI_CM_FOUND" >> "$RUNTIME_SPINIT"
    echo "[eSim] Found NgVeri Ngveri.cm at: $NGVERI_CM_FOUND" >&2
fi

# Tell ngspice to use our runtime-generated spinit
export SPICE_SCRIPTS="$HOME/.esim"

# Set GHDL_PREFIX for GHDL backend (inherited by subprocesses like compile.sh)
export GHDL_PREFIX="$HERE/usr/lib/ghdl"

# Create user NGHDL code model directory
mkdir -p "$HOME/.esim/nghdl/lib"

# ═══ GENERATE GDK-PIXBUF LOADERS.CACHE AT RUNTIME ═══
# Create loaders.cache with absolute paths based on actual mount point
LOADER_DIR="$HERE/lib/x86_64-linux-gnu/gdk-pixbuf-2.0/2.10.0/loaders"
LOADER_CACHE="/tmp/esim-loaders-$$.cache"
if [ -d "$LOADER_DIR" ]; then
    # Start with header
    echo "# GdkPixbuf Image Loader Modules file - Generated at runtime" > "$LOADER_CACHE"
    
    # Only add loaders that actually exist
    for loader in "$LOADER_DIR"/*.so; do
        if [ -f "$loader" ]; then
            basename_loader=$(basename "$loader")
            case "$basename_loader" in
                libpixbufloader-svg.so)
                    cat >> "$LOADER_CACHE" <<SVGEOF

"$loader"
"svg" 6 "gdk-pixbuf" "Scalable Vector Graphics" "LGPL"
"image/svg+xml" "image/svg" ""
"svg" "svgz" ""
" <svg" "*    " 100
SVGEOF
                    ;;
                libpixbufloader-gif.so)
                    cat >> "$LOADER_CACHE" <<GIFEOF

"$loader"
"gif" 4 "gdk-pixbuf" "GIF" "LGPL"
"image/gif" ""
"gif" ""
"GIF8" "" 100
GIFEOF
                    ;;
                libpixbufloader-bmp.so)
                    cat >> "$LOADER_CACHE" <<BMPEOF

"$loader"
"bmp" 5 "gdk-pixbuf" "BMP" "LGPL"
"image/bmp" "image/x-bmp" ""
"bmp" ""
"BM" "" 100
BMPEOF
                    ;;
                libpixbufloader-xpm.so)
                    cat >> "$LOADER_CACHE" <<XPMEOF

"$loader"
"xpm" 4 "gdk-pixbuf" "XPM" "LGPL"
"image/x-xpixmap" ""
"xpm" ""
"/* XPM */" "" 100
XPMEOF
                    ;;
                libpixbufloader-ico.so)
                    cat >> "$LOADER_CACHE" <<ICOEOF

"$loader"
"ico" 5 "gdk-pixbuf" "Windows icon" "LGPL"
"image/x-icon" ""
"ico" "cur" ""
"  \001   " "zz znz" 100
ICOEOF
                    ;;
                libpixbufloader-tiff.so)
                    cat >> "$LOADER_CACHE" <<TIFFEOF

"$loader"
"tiff" 5 "gdk-pixbuf" "TIFF" "LGPL"
"image/tiff" ""
"tiff" "tif" ""
"MM\000*" "" 100
"II*\000" "" 100
TIFFEOF
                    ;;
            esac
        fi
    done
    # Don't export GDK_PIXBUF_MODULE_FILE - modern systems have PNG/JPEG built into libgdk_pixbuf
    # export GDK_PIXBUF_MODULE_FILE="$LOADER_CACHE"
fi
# export GDK_PIXBUF_MODULEDIR="$LOADER_DIR"

export XDG_DATA_DIRS="$HERE/usr/share:${XDG_DATA_DIRS:-/usr/local/share:/usr/share}"
export GTK_DATA_PREFIX="$HERE/usr"
export GTK_EXE_PREFIX="$HERE/usr"
export GTK_THEME=Adwaita
# Disable canberra-gtk-module to prevent "Failed to load module" warning
export GTK_MODULES=""
export GTK3_MODULES=""
export GTK_PATH="$HERE/usr/lib/gtk-3.0"
# Point to bundled GTK settings
export GTK3_EXE_PREFIX="$HERE/usr"
[ -f "$HERE/etc/gtk-3.0/settings.ini" ] && export GTK_SETTINGS_SCHEMA_DIR="$HERE/usr/share/glib-2.0/schemas"
export QT_QPA_PLATFORMTHEME=gtk3
export ESIM_ROOT="$HERE/usr/share/eSim"

# ═══ OPENMODELICA ENVIRONMENT VARIABLES ═══
# Configure bundled OpenModelica for eSim's Modelica converter
export OPENMODELICAHOME="$HERE/usr"
export OPENMODELICALIBRARY="$HERE/usr/lib/omlibrary:$HERE/usr/share/omc/libraries"
# Add bundled omc to PATH (it should already be there from earlier PATH setting)

# ═══ KICAD ENVIRONMENT VARIABLES ═══
# Set root paths for KiCad to find all resources
export KICAD="$HERE/usr/share/kicad"
export KICAD6="$HERE/usr/share/kicad"
export KICAD_DATA="$HERE/usr/share/kicad"
export KICAD6_DATA="$HERE/usr/share/kicad"

export KICAD_SYMBOL_DIR="$HERE/usr/share/kicad/symbols"
export KICAD_FOOTPRINT_DIR="$HERE/usr/share/kicad/footprints"
export KICAD_TEMPLATE_DIR="$HERE/usr/share/kicad/template"
export KICAD_3DMODEL_DIR="$HERE/usr/share/kicad/3dmodels"
export KICAD6_SYMBOL_DIR="$KICAD_SYMBOL_DIR"
export KICAD7_SYMBOL_DIR="$KICAD_SYMBOL_DIR"
export KICAD6_FOOTPRINT_DIR="$KICAD_FOOTPRINT_DIR"
export KICAD7_FOOTPRINT_DIR="$KICAD_FOOTPRINT_DIR"
export KICAD6_TEMPLATE_DIR="$KICAD_TEMPLATE_DIR"
export KICAD7_TEMPLATE_DIR="$KICAD_TEMPLATE_DIR"
export KICAD6_3DMODEL_DIR="$KICAD_3DMODEL_DIR"
export KICAD7_3DMODEL_DIR="$KICAD_3DMODEL_DIR"


# ═══ AUTO CONFIGURE ALL KICAD + ESIM LIBRARIES ═══
configure_all_libraries() {
    local kc=""
    # Check for existing KiCad config directories (different versions)
    for v in 8.0 7.0 6.0 5.0 ""; do
        [ -d "$HOME/.config/kicad${v:+/$v}" ] && { kc="$HOME/.config/kicad${v:+/$v}"; break; }
    done
    
    # If no config dir exists, create one for the bundled KiCad version
    if [ -z "$kc" ]; then
        # Bundled KiCad is version 6.x, so create 6.0 config dir
        kc="$HOME/.config/kicad/6.0"
        mkdir -p "$kc"
        echo "[eSim] Creating KiCad library configuration at: $kc" >&2
    fi
    
    # ALWAYS regenerate sym-lib-table if paths point to stale AppImage mount
    # AppImage mount points change on each launch (/tmp/.mount_eSim-XXXXX)
    local needs_regen=false
    if [ -f "$kc/sym-lib-table" ]; then
        # Check if any path points to a non-existent AppImage mount
        if grep -q "/tmp/.mount_" "$kc/sym-lib-table" 2>/dev/null; then
            local old_mount=$(grep -o "/tmp/.mount_[^/]*" "$kc/sym-lib-table" 2>/dev/null | head -1)
            if [ -n "$old_mount" ] && [ ! -d "$old_mount" ]; then
                echo "[eSim] Stale AppImage mount detected ($old_mount), regenerating library config..." >&2
                needs_regen=true
            fi
        fi
        
        # Also check if current mount matches
        if [ "$needs_regen" = "false" ] && grep -q "eSim_Sources" "$kc/sym-lib-table" 2>/dev/null; then
            local current_esim_path=$(grep "eSim_Sources" "$kc/sym-lib-table" | grep -o 'uri "[^"]*"' | sed 's/uri "//;s/"//')
            if [ -n "$current_esim_path" ] && [ ! -f "$current_esim_path" ]; then
                echo "[eSim] eSim library path invalid, regenerating..." >&2
                needs_regen=true
            fi
        fi
    else
        needs_regen=true
    fi
    
    # If paths are valid, just ensure user NGHDL library is added
    if [ "$needs_regen" = "false" ] && [ -f "$kc/sym-lib-table" ]; then
        if grep -q "eSim_Sources" "$kc/sym-lib-table" 2>/dev/null && \
           grep -q "Device" "$kc/sym-lib-table" 2>/dev/null; then
            # Already configured, just ensure user NGHDL library is added
            if [ -f "$HOME/.esim/symbols/eSim_Nghdl.kicad_sym" ] && \
               ! grep -q "eSim_Nghdl_User" "$kc/sym-lib-table" 2>/dev/null; then
                # Add user NGHDL library without regenerating everything
                sed -i 's/)$/  (lib (name "eSim_Nghdl_User")(type "KiCad")(uri "'"$HOME"'\/.esim\/symbols\/eSim_Nghdl.kicad_sym")(options "")(descr "User NGHDL Converted Symbols"))\n)/' "$kc/sym-lib-table" 2>/dev/null || true
            fi
            if [ -f "$HOME/.esim/symbols/eSim_Ngveri.kicad_sym" ] && \
               ! grep -q "eSim_Ngveri_User" "$kc/sym-lib-table" 2>/dev/null; then
                # Add user NgVeri library without regenerating everything
                sed -i 's/)$/  (lib (name "eSim_Ngveri_User")(type "KiCad")(uri "'"$HOME"'\/.esim\/symbols\/eSim_Ngveri.kicad_sym")(options "")(descr "User NgVeri Converted Symbols"))\n)/' "$kc/sym-lib-table" 2>/dev/null || true
            fi
            return 0
        fi
    fi
    
    # Extract eSim libraries if needed
    [ -f "$ESIM_ROOT/library/kicadLibrary.tar.xz" ] && [ ! -f "$ESIM_ROOT/library/eSim_Sources.lib" ] && {
        cd "$ESIM_ROOT/library"
        tar -xJf kicadLibrary.tar.xz 2>/dev/null || true
        [ -d "kicadLibrary/eSim-symbols" ] && cp kicadLibrary/eSim-symbols/*.{lib,kicad_sym} . 2>/dev/null || true
        [ -d "kicadLibrary/kicad_eSim-Library" ] && cp kicadLibrary/kicad_eSim-Library/*.lib . 2>/dev/null || true
    }
    
    # Find eSim libraries
    local esim_libs=() esim_type=""
    if compgen -G "$ESIM_ROOT/library/eSim_*.kicad_sym" > /dev/null 2>&1; then
        esim_libs=("$ESIM_ROOT/library"/eSim_*.kicad_sym)
        esim_type="KiCad"
    elif compgen -G "$ESIM_ROOT/library/eSim_*.lib" > /dev/null 2>&1; then
        esim_libs=("$ESIM_ROOT/library"/eSim_*.lib)
        esim_type="Legacy"
    fi
    
    
    # Find KiCad libraries - PRIORITIZE BUNDLED AND EXTRACTED LIBRARIES
    local kicad_sym_dir=""
    local kicad_extract="/tmp/esim-kicad6-${UID:-$(id -u)}/squashfs-root"
    for dir in \
        "$kicad_extract/usr/share/kicad/symbols" \
        "$HERE/usr/share/kicad/symbols" \
        "$KICAD_SYMBOL_DIR" \
        "/usr/share/kicad/symbols" \
        "/usr/share/kicad/library" \
        "/usr/share/kicad-nightly/symbols" \
        "$(find /usr/share/kicad* -type d -name "symbols" 2>/dev/null | head -1)"; do
        [ -d "$dir" ] && [ -n "$(ls -A "$dir" 2>/dev/null)" ] && { kicad_sym_dir="$dir"; break; }
    done

    
    # Backup existing config
    [ -f "$kc/sym-lib-table" ] && cp "$kc/sym-lib-table" "$kc/sym-lib-table.backup.$(date +%s)" 2>/dev/null || true
    
    # Create comprehensive configuration
    {
        echo "(sym_lib_table"
        
        # ═══ ADD ALL KICAD DEFAULT LIBRARIES ═══
        if [ -n "$kicad_sym_dir" ]; then
            # Priority libraries with descriptions
            declare -A kicad_libs=(
                ["power"]="Power Symbols - PWR_FLAG, VCC, GND, +5V, +3V3"
                ["Device"]="Basic Devices - R, C, L, D, Q, Fuse, etc"
                ["Connector"]="Connectors - Headers, Terminals, USB, etc"
                ["Connector_Generic"]="Generic Connectors - Pin Headers, Sockets"
                ["MCU_Module"]="Microcontroller Modules - Arduino, ESP32, etc"
                ["Amplifier_Operational"]="Operational Amplifiers - LM324, TL071, etc"
                ["Transistor_BJT"]="Bipolar Junction Transistors"
                ["Transistor_FET"]="Field Effect Transistors - MOSFET, JFET"
                ["Diode"]="Diodes - 1N4148, 1N4007, LED, Zener"
                ["LED"]="Light Emitting Diodes"
                ["Regulator_Linear"]="Linear Voltage Regulators - 7805, LM317"
                ["Regulator_Switching"]="Switching Regulators"
                ["Switch"]="Switches - Push Button, Toggle, DIP"
                ["Relay"]="Relays"
                ["Sensor"]="Sensors - Temperature, Pressure, Motion"
                ["Timer"]="Timer ICs - 555, etc"
                ["Logic_74xx"]="74xx Series Logic ICs"
                ["Memory_RAM"]="RAM ICs"
                ["Memory_EEPROM"]="EEPROM ICs"
                ["Oscillator"]="Oscillators and Crystals"
                ["RF"]="RF Components"
                ["Interface"]="Interface ICs - RS232, CAN, etc"
                ["Display_Character"]="Character Displays - LCD, OLED"
                ["Driver_Motor"]="Motor Drivers"
                ["Mechanical"]="Mechanical Components - Mounting Holes, etc"
            )
            
            for lib_name in "${!kicad_libs[@]}"; do
                local lib_file=""
                local lib_type="KiCad"
                
                # Try .kicad_sym first (modern), then .lib (legacy)
                if [ -f "$kicad_sym_dir/$lib_name.kicad_sym" ]; then
                    lib_file="$kicad_sym_dir/$lib_name.kicad_sym"
                elif [ -f "$kicad_sym_dir/$lib_name.lib" ]; then
                    lib_file="$kicad_sym_dir/$lib_name.lib"
                    lib_type="Legacy"
                fi
                
                if [ -n "$lib_file" ]; then
                    echo "  (lib (name \"$lib_name\")(type \"$lib_type\")(uri \"$lib_file\")(options \"\")(descr \"${kicad_libs[$lib_name]}\"))"
                fi
            done
            
            # Add all other KiCad libraries not in priority list
            for lib_file in "$kicad_sym_dir"/*.{kicad_sym,lib}; do
                [ -f "$lib_file" ] || continue
                local base_name=$(basename "$lib_file" .kicad_sym)
                base_name=$(basename "$base_name" .lib)
                
                # Skip if already added
                [[ " ${!kicad_libs[@]} " =~ " $base_name " ]] && continue
                
                local lib_type="KiCad"
                [[ "$lib_file" == *.lib ]] && lib_type="Legacy"
                
                echo "  (lib (name \"$base_name\")(type \"$lib_type\")(uri \"$lib_file\")(options \"\")(descr \"KiCad Standard Library\"))"
            done
        fi
        
        # ═══ ADD ESIM CUSTOM LIBRARIES ═══
        for lib in "${esim_libs[@]}"; do
            local n=$(basename "$lib" .kicad_sym); n=$(basename "$n" .lib)
            local d="eSim Component Library"
            case "$n" in
                *Sources*) d="eSim Signal Sources - SINE, PWL, PULSE, AC, DC" ;;
                *Plot*) d="eSim Plot Components - plot_v1, plot_v2, plot_i" ;;
                *Power*) d="eSim Custom Power Symbols" ;;
                *Devices*) d="eSim Passive Devices - R, C, L" ;;
                *Analog*) d="eSim Analog Components" ;;
                *Digital*) d="eSim Digital Logic" ;;
                *Hybrid*) d="eSim Hybrid Components" ;;
                *Miscellaneous*) d="eSim Miscellaneous" ;;
                *Subckt*) d="eSim Subcircuits" ;;
                *User*) d="eSim User Libraries" ;;
            esac
            echo "  (lib (name \"$n\")(type \"$esim_type\")(uri \"$lib\")(options \"\")(descr \"$d\"))"
        done
        
        # ═══ ADD USER NGHDL SYMBOLS LIBRARY ═══
        # User-converted NGHDL symbols are stored in ~/.esim/symbols/
        local user_nghdl_lib="\$HOME/.esim/symbols/eSim_Nghdl.kicad_sym"
        if [ -f "$HOME/.esim/symbols/eSim_Nghdl.kicad_sym" ]; then
            echo "  (lib (name \"eSim_Nghdl_User\")(type \"KiCad\")(uri \"$HOME/.esim/symbols/eSim_Nghdl.kicad_sym\")(options \"\")(descr \"User NGHDL Converted Symbols\"))"
        fi
        
        # ═══ ADD USER NGVERI SYMBOLS LIBRARY ═══
        # User-converted NgVeri symbols are stored in ~/.esim/symbols/
        if [ -f "$HOME/.esim/symbols/eSim_Ngveri.kicad_sym" ]; then
            echo "  (lib (name \"eSim_Ngveri_User\")(type \"KiCad\")(uri \"$HOME/.esim/symbols/eSim_Ngveri.kicad_sym\")(options \"\")(descr \"User NgVeri Converted Symbols\"))"
        fi
        
        echo ")"
    } > "$kc/sym-lib-table"
    
    local total_libs=$(grep -c "(lib (name" "$kc/sym-lib-table" 2>/dev/null || echo "0")
    echo "[eSim] ✓ Configured $total_libs symbol libraries (KiCad + eSim) at: $kc/sym-lib-table" >&2
    
    # ═══ CONFIGURE FOOTPRINT LIBRARIES ═══
    # Check if already configured
    [ -f "$kc/fp-lib-table" ] && grep -q "$HERE" "$kc/fp-lib-table" 2>/dev/null && return 0
    
    # Find KiCad footprint libraries - PRIORITIZE BUNDLED
    local kicad_fp_dir=""
    for dir in \
        "$HERE/usr/share/kicad/footprints" \
        "$KICAD_FOOTPRINT_DIR" \
        "/usr/share/kicad/footprints" \
        "/usr/share/kicad/modules"; do
        [ -d "$dir" ] && [ -n "$(ls -A "$dir" 2>/dev/null)" ] && { kicad_fp_dir="$dir"; break; }
    done
    
    [ -z "$kicad_fp_dir" ] && return 0
    
    # Backup existing footprint config
    [ -f "$kc/fp-lib-table" ] && cp "$kc/fp-lib-table" "$kc/fp-lib-table.backup.$(date +%s)" 2>/dev/null || true
    
    # Create footprint library table
    {
        echo "(fp_lib_table"
        
        # Add all footprint libraries
        for fp_lib in "$kicad_fp_dir"/*.pretty; do
            [ -d "$fp_lib" ] || continue
            local fp_name=$(basename "$fp_lib" .pretty)
            local fp_desc="KiCad Footprint Library"
            
            # Add descriptions for common libraries
            case "$fp_name" in
                *Capacitor_SMD*) fp_desc="SMD Capacitor Footprints" ;;
                *Resistor_SMD*) fp_desc="SMD Resistor Footprints" ;;
                *LED_SMD*) fp_desc="SMD LED Footprints" ;;
                *Diode_SMD*) fp_desc="SMD Diode Footprints" ;;
                *Connector*) fp_desc="Connector Footprints" ;;
                *Package_SO*) fp_desc="Small Outline IC Packages" ;;
                *Package_DIP*) fp_desc="Dual In-line IC Packages" ;;
                *Package_QFP*) fp_desc="Quad Flat Package ICs" ;;
                *Package_BGA*) fp_desc="Ball Grid Array Packages" ;;
            esac
            
            echo "  (lib (name \"$fp_name\")(type \"KiCad\")(uri \"$fp_lib\")(options \"\")(descr \"$fp_desc\"))"
        done
        
        echo ")"
    } > "$kc/fp-lib-table"
    
    local total_fps=$(grep -c "(lib (name" "$kc/fp-lib-table" 2>/dev/null || echo "0")
    echo "[eSim] ✓ Configured $total_fps footprint libraries at: $kc/fp-lib-table" >&2
}

configure_all_libraries 2>/dev/null || true

# ═══ LEGACY PROJECT SUPPORT ═══
# Create project-specific sym-lib-table for legacy KiCad 5 projects
# This helps KiCad 6 find symbols in eSim libraries when opening legacy .sch files
setup_legacy_project_libs() {
    local project_dir="$1"
    [ -z "$project_dir" ] && return 0
    [ ! -d "$project_dir" ] && return 0
    
    # Check if project has legacy .sch files but no sym-lib-table
    if [ -f "$project_dir"/*.sch ] 2>/dev/null && [ ! -f "$project_dir/sym-lib-table" ]; then
        # Check if it's a legacy format schematic
        local sch_file=$(ls -1 "$project_dir"/*.sch 2>/dev/null | head -1)
        if [ -f "$sch_file" ] && grep -q "^EESchema Schematic" "$sch_file" 2>/dev/null; then
            echo "[eSim] Legacy KiCad 5 project detected, creating project sym-lib-table..." >&2
            
            # Create project-specific sym-lib-table with all eSim libraries
            {
                echo "(sym_lib_table"
                
                # Add eSim libraries from bundled location
                for lib in "$ESIM_ROOT/library"/eSim_*.kicad_sym; do
                    [ -f "$lib" ] || continue
                    local n=$(basename "$lib" .kicad_sym)
                    echo "  (lib (name \"$n\")(type \"KiCad\")(uri \"$lib\")(options \"\")(descr \"eSim Library\"))"
                done
                
                # Add user NGHDL symbols if they exist
                if [ -f "$HOME/.esim/symbols/eSim_Nghdl.kicad_sym" ]; then
                    echo "  (lib (name \"eSim_Nghdl_User\")(type \"KiCad\")(uri \"$HOME/.esim/symbols/eSim_Nghdl.kicad_sym\")(options \"\")(descr \"User NGHDL Converted Symbols\"))"
                fi
                
                # Add user NgVeri symbols if they exist
                if [ -f "$HOME/.esim/symbols/eSim_Ngveri.kicad_sym" ]; then
                    echo "  (lib (name \"eSim_Ngveri_User\")(type \"KiCad\")(uri \"$HOME/.esim/symbols/eSim_Ngveri.kicad_sym\")(options \"\")(descr \"User NgVeri Converted Symbols\"))"
                fi
                
                echo ")"
            } > "$project_dir/sym-lib-table"
            echo "[eSim] ✓ Created project-specific sym-lib-table for legacy project" >&2
        fi
    fi
}

# Create .esim config.ini for Modelica and internal paths
ESIM_HOME="$HOME/.esim"
mkdir -p "$ESIM_HOME"
# IMPORTANT: Use absolute path for modelica_map.json, not relative!
# The Python code opens this file directly, so it must be a full path.
cat > "$ESIM_HOME/config.ini" << CFGEOF
[eSim]
modelica_map_json = $ESIM_HOME/modelica_map.json
eSim_HOME = $ESIM_ROOT
[NGHDL]
NGHDL_HOME = $ESIM_ROOT/nghdl
CFGEOF
# Copy actual Mapping.json (with Sources, Devices, Components) if user file doesn't exist or is empty/invalid
if [ ! -f "$ESIM_HOME/modelica_map.json" ] || [ ! -s "$ESIM_HOME/modelica_map.json" ] || ! grep -q 'Sources' "$ESIM_HOME/modelica_map.json" 2>/dev/null; then
    if [ -f "$ESIM_ROOT/library/ngspicetoModelica/Mapping.json" ]; then
        cp "$ESIM_ROOT/library/ngspicetoModelica/Mapping.json" "$ESIM_HOME/modelica_map.json"
    elif [ -f "$ESIM_ROOT/library/ngspicetoModelica/modelica_map.json" ]; then
        cp "$ESIM_ROOT/library/ngspicetoModelica/modelica_map.json" "$ESIM_HOME/modelica_map.json"
    fi
fi

# Change to eSim frontEnd directory so UI files can be found
cd "$ESIM_ROOT/src/frontEnd"
python3 "$ESIM_ROOT/src/frontEnd/Application.py" "$@" 2>&1 | \
    grep -v "Cannot access Modelica map file" | grep -v "No option 'modelica_map_json'" | \
    grep -v "Unable to import Axes3D" | grep -v "iCCP: known incorrect sRGB profile" || true
LAUNCHER
    
    chmod +x "$APPDIR/usr/bin/esim"
    ok "Launcher created with FULL KiCad + eSim library auto-configuration"
    
    # Desktop integration with proper StartupWMClass for icon
    cat > "$APPDIR/eSim.desktop" <<'EOF'
[Desktop Entry]
Type=Application
Name=eSim
GenericName=Circuit Simulator
Comment=Electronic Circuit Design and Simulation with KiCad integration
Exec=esim %F
Icon=eSim
StartupWMClass=eSim
StartupNotify=true
Categories=Education;Science;Electronics;Engineering;
MimeType=application/x-kicad-schematic;
Terminal=false
EOF
    
    cat > "$APPDIR/AppRun" <<'EOF'
#!/bin/bash
# eSim AppImage AppRun - Multi-Distro Compatible
# Supports: Ubuntu, Debian, Fedora, Arch, openSUSE and derivatives

SELF=$(readlink -f "$0")
HERE=${SELF%/*}
export APPDIR="$HERE"

# ═══ GLIBC COMPATIBILITY: RUNTIME LIBRARY FILTERING ═══
# The AppImage bundles libraries from Ubuntu 24.04 (GLIBC 2.38+).
# On older distros (e.g. Debian 12 with GLIBC 2.36), bundled libs that
# require GLIBC > host version fail with "version `GLIBC_X.XX' not found".
#
# Solution: On older systems, scan bundled libs and REMOVE any that require
# a higher GLIBC than the host. The system will then provide those libs.
# For read-only mounts (actual AppImage), we exclude the bundled lib path
# entirely and rely only on system libs.

_ESIM_LIB_DIR="${HERE}/usr/lib"   # default: use bundled libs directly
_ESIM_USE_BUNDLED_LIBS=true       # flag: whether to include bundled libs in LD_LIBRARY_PATH

_setup_compat_libs() {
    # Detect system glibc version
    local _sys_glibc
    _sys_glibc=$(ldd --version 2>&1 | head -1 | grep -oE '[0-9]+\.[0-9]+$')
    [ -z "$_sys_glibc" ] && return 0

    # If system glibc >= 2.38, all bundled libs are compatible — use directly
    local _oldest
    _oldest=$(printf '%s\n2.38\n' "$_sys_glibc" | sort -V | head -1)
    [ "$_oldest" = "2.38" ] && return 0

    # ── System glibc < 2.38: need to filter incompatible libraries ──
    echo "[eSim] System glibc ${_sys_glibc} < 2.38 — filtering bundled libraries for compatibility"
    
    # Check if bundled lib directory is writable (extracted AppImage vs mounted)
    if [ -w "${HERE}/usr/lib" ]; then
        # WRITABLE: Directly remove incompatible libs (they'll be provided by system)
        echo "[eSim] Extracted AppImage detected — removing incompatible bundled libraries"
        
        local _removed=0
        local _f _max_needed _lower
        
        for _f in "${HERE}"/usr/lib/*.so*; do
            [ -f "$_f" ] || continue
            [ -L "$_f" ] && continue  # Skip symlinks, process actual files
            
            # Get max GLIBC version required by this library
            _max_needed=$(strings "$_f" 2>/dev/null | grep -oE 'GLIBC_[0-9]+\.[0-9]+' | \
                          sed 's/GLIBC_//' | sort -V | tail -1)
            [ -z "$_max_needed" ] && continue
            
            # Compare: if needed > system, remove it
            _lower=$(printf '%s\n%s\n' "$_sys_glibc" "$_max_needed" | sort -V | head -1)
            if [ "$_lower" != "$_max_needed" ]; then
                rm -f "$_f" 2>/dev/null && {
                    _removed=$((_removed + 1))
                    # Also remove any symlinks pointing to this file
                    local _basename=$(basename "$_f")
                    rm -f "${HERE}/usr/lib/${_basename%.so*}"*.so* 2>/dev/null
                }
            fi
        done
        
        [ $_removed -gt 0 ] && echo "[eSim] Removed $_removed incompatible libraries (system will provide)"
        
        # Always remove core glibc family if present (must come from host)
        rm -f "${HERE}"/usr/lib/libc.so* "${HERE}"/usr/lib/libm.so* \
              "${HERE}"/usr/lib/libpthread.so* "${HERE}"/usr/lib/libdl.so* \
              "${HERE}"/usr/lib/librt.so* "${HERE}"/usr/lib/libresolv.so* \
              "${HERE}"/usr/lib/libnss_*.so* "${HERE}"/usr/lib/ld-linux*.so* \
              "${HERE}"/usr/lib/libmvec.so* "${HERE}"/usr/lib/libanl.so* \
              2>/dev/null
        
        # Always remove C++ and Fortran runtime libs (must come from host for ABI compatibility)
        # This ensures locally-built code models (Ngveri.cm, ghdl.cm) and numpy/scipy work correctly
        rm -f "${HERE}"/usr/lib/libstdc++.so* "${HERE}"/usr/lib/libgcc_s.so* \
              "${HERE}"/usr/lib/libgfortran.so* "${HERE}"/usr/lib/libquadmath.so* \
              2>/dev/null
    else
        # READ-ONLY: Cannot modify libs, so exclude bundled lib dir from LD_LIBRARY_PATH
        # The esim launcher and other scripts will NOT add ${HERE}/usr/lib
        echo "[eSim] Read-only AppImage detected — using system libraries only"
        _ESIM_USE_BUNDLED_LIBS=false
        _ESIM_LIB_DIR=""  # Empty = don't add to LD_LIBRARY_PATH
    fi
}

_setup_compat_libs

# ═══ RUNTIME PYTHON PACKAGE INSTALLER ═══
# Python packages with C extensions (numpy, scipy, matplotlib, lxml) must match
# the system Python version. Instead of bundling version-specific packages,
# we install them at first run to ~/.esim/python-packages/
# Pure-Python packages (hdlparse, minilexer) are bundled in the AppImage.

_ESIM_PYDIR="$HOME/.esim/python-packages"

_ensure_python_packages() {
    # Check if critical packages are available (either system or our installed)
    if python3 -c "import numpy, matplotlib, lxml" 2>/dev/null; then
        # Already installed (system or ~/.esim), just add our dir to path
        export PYTHONPATH="${_ESIM_PYDIR}:${PYTHONPATH}"
        return 0
    fi
    
    # Need to install packages
    echo "[eSim] Installing Python dependencies for $(python3 --version 2>&1)..."
    echo "[eSim] This only happens once. Please wait..."
    
    mkdir -p "$_ESIM_PYDIR"
    
    # On Fedora, install matplotlib with Qt5 support from system first
    if command -v dnf >/dev/null 2>&1; then
        echo "[eSim] Installing system packages for Fedora..."
        dnf install -y python3-matplotlib-qt5 python3-pyqt5 2>&1 | tail -1 || true
    fi
    
    # Install required packages to user directory
    # These are the packages with C extensions that must match Python version
    local _pip_cmd="python3 -m pip install --target $_ESIM_PYDIR --upgrade --quiet"
    
    # Core scientific packages (do NOT include PyQt5 or matplotlib here on systems
    # where system packages provide them with proper Qt5 support)
    if command -v dnf >/dev/null 2>&1; then
        # Fedora: skip matplotlib, use system python3-matplotlib-qt5 instead
        $_pip_cmd numpy scipy lxml watchdog pillow pyqt5-sip 2>&1 | grep -v "already satisfied" | tail -3
    else
        # Other distros: try to install matplotlib via pip
        $_pip_cmd numpy scipy matplotlib lxml watchdog pillow pyqt5-sip 2>&1 | grep -v "already satisfied" | tail -3
    fi
    
    # Try pip-installing PyQt5 only if system doesn't have it
    # (PyPI wheels only exist up to ~Python 3.12)
    if ! python3 -c "import PyQt5" 2>/dev/null; then
        # Try pip first (works on older Python versions)
        if ! $_pip_cmd PyQt5 2>/dev/null; then
            # pip failed — try installing system package automatically
            echo "[eSim] PyQt5 not available via pip, trying system package..."
            if command -v dnf >/dev/null 2>&1; then
                dnf install -y python3-qt5 python3-qt5-base python3-matplotlib-qt5 2>&1 | tail -2 || true
            elif command -v apt-get >/dev/null 2>&1; then
                apt-get install -y -qq python3-pyqt5 python3-matplotlib 2>&1 | tail -2 || true
            elif command -v pacman >/dev/null 2>&1; then
                pacman -S --noconfirm python-pyqt5 python-matplotlib 2>&1 | tail -2 || true
            elif command -v zypper >/dev/null 2>&1; then
                zypper --non-interactive install python3-qt5 python3-matplotlib-qt5 2>&1 | tail -2 || true
            fi
            # Final check
            if ! python3 -c "import PyQt5" 2>/dev/null; then
                echo "[eSim] Warning: PyQt5 not found. Install system package:"
                echo "[eSim]   Debian/Ubuntu: sudo apt install python3-pyqt5 python3-matplotlib"
                echo "[eSim]   Fedora:        sudo dnf install python3-qt5 python3-matplotlib-qt5"
                echo "[eSim]   Arch:          sudo pacman -S python-pyqt5"
            fi
        fi
    fi
    
    # Check installation success
    if ! python3 -c "import sys; sys.path.insert(0, '$_ESIM_PYDIR'); import numpy" 2>/dev/null; then
        echo "[eSim] Warning: Some Python packages failed to install."
        echo "[eSim] Try: pip install --user numpy scipy matplotlib lxml watchdog"
    else
        echo "[eSim] ✓ Python packages installed successfully"
    fi
    
    # Verify matplotlib has Qt5 backend support
    if ! python3 -c "from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg" 2>/dev/null; then
        echo "[eSim] Note: matplotlib Qt5 backend not available. Installing system packages..."
        if command -v dnf >/dev/null 2>&1; then
            # Fedora: must use system package, not pip
            dnf install -y python3-matplotlib-qt5 2>&1 | tail -1 || true
            # Verify again
            if ! python3 -c "from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg" 2>/dev/null; then
                echo "[eSim] ✓ Matplotlib Qt5 backend installed from system"
            fi
        elif command -v apt-get >/dev/null 2>&1; then
            apt-get install -y -qq python3-matplotlib 2>&1 | tail -1 || true
        elif command -v pacman >/dev/null 2>&1; then
            pacman -S --noconfirm python-matplotlib 2>&1 | tail -1 || true
        fi
        
        # Final verification
        if ! python3 -c "from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg" 2>/dev/null; then
            echo "[eSim] ⚠ Warning: matplotlib Qt5 backend still not available"
            echo "[eSim] Try: sudo dnf install python3-matplotlib-qt5 (Fedora)"
            echo "[eSim] Or:   sudo apt install python3-matplotlib (Debian/Ubuntu)"
        fi
    fi
    
    export PYTHONPATH="${_ESIM_PYDIR}:${PYTHONPATH}"
}

_ensure_python_packages

# ═══ NGHDL AUTO-CONFIGURATION ═══
# The NGHDL config file (~/.nghdl/config.ini) may have paths from a different system.
# This function detects if GHDL paths are valid and regenerates config if needed.

_setup_nghdl_config() {
    local NGHDL_CONFIG="$HOME/.nghdl/config.ini"
    
    # Skip if no config exists (NGHDL not set up yet)
    [ -f "$NGHDL_CONFIG" ] || return 0
    
    # Check if configured GHDL path exists
    local CONFIGURED_GHDL
    CONFIGURED_GHDL=$(grep "^GHDL = " "$NGHDL_CONFIG" 2>/dev/null | cut -d'=' -f2 | tr -d ' ')
    
    # If configured GHDL exists and works, keep existing config
    if [ -n "$CONFIGURED_GHDL" ] && [ -x "$CONFIGURED_GHDL" ]; then
        return 0
    fi
    
    # ── Need to regenerate config with correct paths ──
    echo "[eSim] Updating NGHDL config for current system..."
    
    # Find GHDL (prefer bundled, fallback to system)
    local GHDL_BIN=""
    local GHDL_PREFIX=""
    
    if [ -x "${HERE}/usr/bin/ghdl" ]; then
        GHDL_BIN="${HERE}/usr/bin/ghdl"
        GHDL_PREFIX="${HERE}/usr/lib/ghdl/llvm"
    elif command -v ghdl-llvm >/dev/null 2>&1; then
        GHDL_BIN=$(command -v ghdl-llvm)
        GHDL_PREFIX="/usr/lib/ghdl/llvm"
    elif command -v ghdl >/dev/null 2>&1; then
        GHDL_BIN=$(command -v ghdl)
        # Try to detect prefix from ghdl itself
        GHDL_PREFIX=$(dirname $(dirname "$GHDL_BIN"))/lib/ghdl
        [ -d "$GHDL_PREFIX/llvm" ] && GHDL_PREFIX="$GHDL_PREFIX/llvm"
    fi
    
    # Find Verilator
    local VERILATOR_BIN=""
    if [ -x "${HERE}/usr/bin/verilator" ]; then
        VERILATOR_BIN="${HERE}/usr/bin/verilator"
    elif command -v verilator >/dev/null 2>&1; then
        VERILATOR_BIN=$(command -v verilator)
    fi
    
    # Preserve existing NGHDL_HOME and DIGITAL_MODEL paths
    local NGHDL_HOME=$(grep "^NGHDL_HOME = " "$NGHDL_CONFIG" 2>/dev/null | cut -d'=' -f2 | tr -d ' ')
    local DIGITAL_MODEL=$(grep "^DIGITAL_MODEL = " "$NGHDL_CONFIG" 2>/dev/null | cut -d'=' -f2 | tr -d ' ')
    local RELEASE=$(grep "^RELEASE = " "$NGHDL_CONFIG" 2>/dev/null | cut -d'=' -f2 | tr -d ' ')
    
    # Use defaults if not found
    [ -z "$NGHDL_HOME" ] && NGHDL_HOME="$HOME/nghdl-simulator"
    [ -z "$DIGITAL_MODEL" ] && DIGITAL_MODEL="$NGHDL_HOME/src/xspice/icm"
    [ -z "$RELEASE" ] && RELEASE="$NGHDL_HOME"
    
    # Write updated config
    cat > "$NGHDL_CONFIG" << NGHDL_EOF
[NGHDL]
NGHDL_HOME = $NGHDL_HOME
DIGITAL_MODEL = $DIGITAL_MODEL
RELEASE = $RELEASE

[SRC]
SRC_HOME = ${HERE}/usr/share/eSim/nghdl
LICENSE = ${HERE}/usr/share/eSim/nghdl/LICENSE

[COMPILER]
GHDL = $GHDL_BIN
VERILATOR = $VERILATOR_BIN
GHDL_PREFIX = $GHDL_PREFIX
MODEL_COMPILER = $GHDL_BIN
NGHDL_EOF

    echo "[eSim] ✓ NGHDL config updated (GHDL: $GHDL_BIN)"
    
    # Check if code models need rebuilding (they contain hardcoded paths)
    local CM_DIR="$HOME/.nghdl/local/lib/ngspice"
    if [ -d "$CM_DIR" ] && [ "$(ls -A "$CM_DIR"/*.cm 2>/dev/null)" ]; then
        echo "[eSim] Note: NGHDL code models may need rebuilding via eSim NGHDL menu"
    fi
}

_setup_nghdl_config

# ═══ RUNTIME CODE MODEL COMPILATION ═══
# Compile NGHDL code models (ghdl.cm, ngveri.cm, etc.) at runtime
# This ensures cross-distro compatibility by using target system's compiler
_compile_code_models() {
    local CM_DIR="$HOME/.nghdl/local/lib/ngspice"
    local ICM_SRC="$HOME/nghdl-simulator/src/xspice/icm"
    local NGVERI_DIR="$ICM_SRC/Ngveri"
    
    # Skip if nghdl-simulator source doesn't exist
    [ -d "$ICM_SRC" ] || return 0
    
    # ═══ CRITICAL: Clean clk_gate BEFORE ANY PROCESSING ═══
    # This must happen BEFORE configure runs, otherwise clk_gate will be included in CMDIRS
    echo "[eSim] Cleaning up Ngveri build environment..."
    
    # Ensure Ngveri directory exists first
    mkdir -p "$NGVERI_DIR" 2>/dev/null || true
    
    rm -rf "$NGVERI_DIR/clk_gate" 2>/dev/null || true
    find "$NGVERI_DIR" \( -name "sim_main_*.cpp" -o -name "sim_main_*.h" -o -name "sim_main_*.o" \) -delete 2>/dev/null || true
    echo "" > "$NGVERI_DIR/modpath.lst" 2>/dev/null || true
    echo "" > "$NGVERI_DIR/udnpath.lst" 2>/dev/null || true
    
    # Check if code models exist and are compatible
    local NEED_COMPILE=0
    
    # Check for missing essential code models
    if [ ! -f "$CM_DIR/ghdl.cm" ] || [ ! -f "$CM_DIR/analog.cm" ]; then
        NEED_COMPILE=1
    fi
    
    # Check for incompatible glibc symbols in existing code models
    if [ "$NEED_COMPILE" -eq 0 ] && [ -f "$CM_DIR/ghdl.cm" ]; then
        if strings "$CM_DIR/ghdl.cm" 2>/dev/null | grep -q "__isoc23"; then
            echo "[eSim] Code models have incompatible glibc symbols, recompiling..."
            NEED_COMPILE=1
        fi
    fi
    
    # Check if Ngveri needs compilation (requires verilated objects)
    if [ "$NEED_COMPILE" -eq 0 ] && [ ! -f "$CM_DIR/Ngveri.cm" ] || [ ! -f "$NGVERI_DIR/verilated_threads.o" ] || [ ! -f "$NGVERI_DIR/verilated.o" ]; then
        echo "[eSim] Ngveri code model or verilated objects missing, recompiling..."
        NEED_COMPILE=1
    fi
    
    # Compile if needed
    if [ "$NEED_COMPILE" -eq 1 ]; then
        # Check for required build tools
        if ! command -v make >/dev/null 2>&1; then
            echo "[eSim] Note: 'make' not found. Install build-essential for NGHDL support."
            return 0
        fi
        if ! command -v gcc >/dev/null 2>&1; then
            echo "[eSim] Note: 'gcc' not found. Install build-essential for NGHDL support."
            return 0
        fi
        
        # Create default Ngveri modpath.lst with clk_gate example model
        # First remove any old clk_gate directory to ensure clean rebuild
        if [ -d "$ICM_SRC/Ngveri/clk_gate" ]; then
            rm -rf "$ICM_SRC/Ngveri/clk_gate"
        fi
        
        if [ ! -f "$ICM_SRC/Ngveri/modpath.lst" ]; then
            echo "[eSim] Setting up Ngveri build environment..."
            mkdir -p "$ICM_SRC/Ngveri"
            # Create empty modpath.lst - users will add their own models here
            touch "$ICM_SRC/Ngveri/modpath.lst"
        else
            # Completely clear modpath.lst to prevent cmpp from processing unwanted models
            echo "" > "$ICM_SRC/Ngveri/modpath.lst" 2>/dev/null || true
        fi
        
        # Create empty udnpath.lst if doesn't exist (allows cmpp to continue)
        if [ ! -f "$ICM_SRC/Ngveri/udnpath.lst" ]; then
            echo "[eSim] Creating Ngveri udnpath.lst..."
            echo "" > "$ICM_SRC/Ngveri/udnpath.lst"
        else
            # Clear udnpath.lst as well
            echo "" > "$ICM_SRC/Ngveri/udnpath.lst" 2>/dev/null || true
        fi
        
        # Note: Ngveri template files (clk_gate.v, cfunc.mod, ifspec.ifs) are removed
        # Users add their own Verilog models directly through eSim UI
        # The build system will handle Verilator compilation and cmpp for user models

        
        # ═══ DISTRO-AGNOSTIC VERILATED OBJECT COMPILATION ═══
        echo "[eSim] Preparing verilated objects for this system..."
        mkdir -p "$NGVERI_DIR"
        
        # Check if Verilator is available on this system
        if [ ! -d /usr/share/verilator/include ]; then
            echo "[eSim] ⚠ Verilator not found at /usr/share/verilator/include"
            echo "[eSim]   Install: sudo apt install verilator (Debian/Ubuntu) or sudo dnf install verilator (Fedora)"
            echo "[eSim]   Ngveri code model will NOT be available"
        else
            # Auto-detect C++ stdlib path - check multiple locations for container compatibility
            local CXX_INCLUDE_PATH=""
            
            # Check bundled paths first (for AppImage/container)
            for bundled_path in "$APPDIR/usr/include/c++" "/usr/include/c++" "$APPDIR/include/c++"; do
                if [ -d "$bundled_path" ]; then
                    CXX_INCLUDE_PATH="$bundled_path"
                    break
                fi
            done
            
            # If not found in bundled paths, search system paths
            if [ -z "$CXX_INCLUDE_PATH" ]; then
                for cpp_version in 13 12 11 10 9 8; do
                    if [ -d "/usr/include/c++/$cpp_version" ]; then
                        CXX_INCLUDE_PATH="/usr/include/c++/$cpp_version"
                        break
                    fi
                done
            fi
            
            if [ -z "$CXX_INCLUDE_PATH" ]; then
                echo "[eSim] ⚠ C++ standard library not found in system or AppImage"
                echo "[eSim]   Install development packages:"
                if command -v apt-get >/dev/null 2>&1; then
                    echo "[eSim]   sudo apt-get install build-essential g++"
                elif command -v dnf >/dev/null 2>&1; then
                    echo "[eSim]   sudo dnf install gcc-c++ libstdc++-devel"
                elif command -v pacman >/dev/null 2>&1; then
                    echo "[eSim]   sudo pacman -S base-devel"
                else
                    echo "[eSim]   Install C++ development tools for your distro"
                fi
                echo "[eSim]   Ngveri will be disabled until C++ headers are available"
            else
                # Build compiler flags using detected path
                local CXXFLAGS="-O2 -fPIC -pthread -std=c++14 -DVL_THREADED"
                CXXFLAGS="$CXXFLAGS -I$CXX_INCLUDE_PATH"
                
                # Add architecture-specific paths if available
                local ARCH_CXX_PATH=""
                if [ -d "/usr/include/x86_64-linux-gnu/c++" ]; then
                    for cpp_version in 13 12 11 10 9 8; do
                        if [ -d "/usr/include/x86_64-linux-gnu/c++/$cpp_version" ]; then
                            ARCH_CXX_PATH="/usr/include/x86_64-linux-gnu/c++/$cpp_version"
                            CXXFLAGS="$CXXFLAGS -I$ARCH_CXX_PATH"
                            break
                        fi
                    done
                fi
                
                # Compile verilated_threads.o
                if [ ! -f "$NGVERI_DIR/verilated_threads.o" ]; then
                    echo "[eSim] Compiling verilated_threads.o with flags: $CXXFLAGS"
                    if g++ -c $CXXFLAGS -I/usr/share/verilator/include /usr/share/verilator/include/verilated_threads.cpp -o "$NGVERI_DIR/verilated_threads.o" 2>"/tmp/veri_threads_err.log"; then
                        echo "[eSim] ✓ verilated_threads.o compiled successfully"
                    else
                        echo "[eSim] ✗ Failed to compile verilated_threads.o"
                        echo "[eSim] Error details:"
                        cat "/tmp/veri_threads_err.log" | head -20 | sed 's/^/    /'
                    fi
                fi
                
                # Compile verilated.o
                if [ ! -f "$NGVERI_DIR/verilated.o" ]; then
                    echo "[eSim] Compiling verilated.o with flags: $CXXFLAGS"
                    if g++ -c $CXXFLAGS -I/usr/share/verilator/include /usr/share/verilator/include/verilated.cpp -o "$NGVERI_DIR/verilated.o" 2>"/tmp/veri_verilated_err.log"; then
                        echo "[eSim] ✓ verilated.o compiled successfully"
                    else
                        echo "[eSim] ✗ Failed to compile verilated.o"
                        echo "[eSim] Error details:"
                        cat "/tmp/veri_verilated_err.log" | head -20 | sed 's/^/    /'
                    fi
                fi
                
                # Final status
                if [ -f "$NGVERI_DIR/verilated_threads.o" ] && [ -f "$NGVERI_DIR/verilated.o" ]; then
                    echo "[eSim] ✓ Verilated objects ready for Ngveri"
                else
                    echo "[eSim] ⚠ Verilated objects incomplete - Ngveri.cm may fail to link"
                    echo "[eSim]   Check: ls -l $NGVERI_DIR/*.o"
                fi
            fi
        fi
        
        echo "[eSim] Compiling NGHDL code models for this system..."
        
        # Patch Verilator lint_off.txt to remove unsupported flags based on verilator version
        # This ensures compatibility across different Verilator versions
        if command -v verilator >/dev/null 2>&1; then
            local _VERILATOR_VERSION=$(verilator --version 2>/dev/null | awk '{print $2}' | sed 's/\.//g' | head -c 4)
            if [ -n "$_VERILATOR_VERSION" ] && [ "$_VERILATOR_VERSION" -ge 4200 ]; then
                # Verilator 4.2+ doesn't support some older warning flags
                # Patch all lint_off.txt files to ensure compatibility
                for _LINT_FILE in "$APPDIR/usr/share/eSim/library/tlv/lint_off.txt" \
                                  "$SRCDIR/../downloads/eSim-2.5/library/tlv/lint_off.txt" \
                                  "$ICM_SRC/../../../library/tlv/lint_off.txt"; do
                    if [ -f "$_LINT_FILE" ]; then
                        echo "[eSim] Patching Verilator flags in $_LINT_FILE for version compatibility"
                        # LATCH warning is not available in newer Verilator, remove it
                        sed -i '/^LATCH$/d' "$_LINT_FILE" 2>/dev/null || true
                        # Remove any other unsupported warnings
                        sed -i '/^UNOPTFLAT$/d' "$_LINT_FILE" 2>/dev/null || true
                    fi
                done
            fi
        fi
        
        # GCC 15+ needs -std=gnu17 to avoid bool keyword conflict in ngspice/bool.h
        local _CM_CFLAGS=""
        if command -v gcc >/dev/null 2>&1 && gcc -dumpversion 2>/dev/null | awk -F. '{exit ($1 >= 14) ? 0 : 1}'; then
            _CM_CFLAGS="-std=gnu17 -Wno-error=incompatible-pointer-types -Wno-error=int-conversion -Wno-error=implicit-function-declaration"
        fi
        
        # If verilated objects are missing, skip Ngveri (it's optional)
        if [ -f "$NGVERI_DIR/verilated_threads.o" ] && [ -f "$NGVERI_DIR/verilated.o" ]; then
            # Objects are present, Ngveri can be built
            # Patch GNUmakefile to:
            # 1. Include Verilator headers
            # 2. Link with verilated objects
            if [ -f "$ICM_SRC/GNUmakefile" ]; then
                echo "[eSim] Configuring GNUmakefile for Ngveri with Verilator support..."
                
                # Add Verilator include path to all C++ compilations
                sed -i 's/^INCLUDES = /INCLUDES = -I\/usr\/share\/verilator\/include /' "$ICM_SRC/GNUmakefile" 2>/dev/null || true
                
                # Also ensure CXXFLAGS includes Verilator path (for g++ compilations of sim_main files)
                if ! grep -q "CXXFLAGS.*verilator" "$ICM_SRC/GNUmakefile"; then
                    sed -i '/^INCLUDES =/a CXXFLAGS := $(CXXFLAGS) -I/usr/share/verilator/include' "$ICM_SRC/GNUmakefile" 2>/dev/null || true
                fi
                
                # Add verilated objects to EXTRA_OBJS for linking
                sed -i "/^COMPILE = /a EXTRA_VERILATED_OBJS = $NGVERI_DIR/verilated_threads.o $NGVERI_DIR/verilated.o" "$ICM_SRC/GNUmakefile" 2>/dev/null || true
                
                # Link verilated objects with Ngveri.cm (patch the linking line for Ngveri)
                sed -i 's/^\(\s*gcc.*-shared.*-o ngveri\/ngveri.cm\)/\1 '"$NGVERI_DIR"'\/verilated_threads.o '"$NGVERI_DIR"'\/verilated.o/' "$ICM_SRC/GNUmakefile" 2>/dev/null || true
            fi
        else
            if [ -f "$ICM_SRC/GNUmakefile" ]; then
                echo "[eSim] ⚠ Verilated objects missing - excluding Ngveri from code model build"
                # Remove Ngveri from CMDIRS line
                sed -i 's/ Ngveri$//' "$ICM_SRC/GNUmakefile"
                # Also patch all for loops that mention Ngveri
                sed -i 's/ Ngveri//g' "$ICM_SRC/GNUmakefile"
            fi
        fi
        
        # Compile code models
        # Note: Pass CFLAGS as make variable (not environment var) to override makedefs
        
        # First, verify nghdl-simulator structure
        if [ ! -d "$ICM_SRC" ]; then
            echo "[eSim] ⚠ NGHDL simulator source not found at $ICM_SRC"
            return 0
        fi
        
        if [ -f "$ICM_SRC/GNUmakefile" ] || [ -f "$ICM_SRC/../../../src/xspice/configure" ] || [ -f "$ICM_SRC/../../../configure" ]; then
            # Delete old GNUmakefile to force reconfiguration
            rm -f "$ICM_SRC/GNUmakefile" 2>/dev/null || true
            
            # Try to reconfigure ngspice with xspice support
            local configure_found=false
            
            # Check multiple possible configure locations
            if [ -f "$ICM_SRC/../../../configure" ]; then
                echo "[eSim] Reconfiguring ngspice with xspice support..."
                (cd "$ICM_SRC/../../../" && \
                    CFLAGS="$_CM_CFLAGS" ./configure --with-ngshared --enable-xspice --disable-debug --prefix="$HOME/.nghdl/local" >/dev/null 2>&1) && configure_found=true
            elif [ -f "$ICM_SRC/../../../src/xspice/configure" ]; then
                echo "[eSim] Reconfiguring xspice modules..."
                (cd "$ICM_SRC/../../../src/xspice" && \
                    CFLAGS="$_CM_CFLAGS" ./configure --enable-xspice --with-ngshared --prefix="$HOME/.nghdl/local" >/dev/null 2>&1) && configure_found=true
            fi
            
            # If reconfigure didn't work or GNUmakefile still missing, skip code model build
            if [ ! -f "$ICM_SRC/GNUmakefile" ]; then
                if [ "$configure_found" = false ]; then
                    echo "[eSim] ⚠ ngspice/xspice configure script not found"
                    echo "[eSim]    This is normal for pre-compiled nghdl-simulator"
                    echo "[eSim]    The 7 core code models are already compiled and available"
                else
                    echo "[eSim] ⚠ GNUmakefile generation failed"
                fi
            fi
            
            # For Ngveri: pass Verilator include and object paths to make
            local _VERILATOR_INCLUDE="/usr/share/verilator/include"
            local _VERILATOR_OBJ="$NGVERI_DIR"
            local _EXTRA_CFLAGS="$_CM_CFLAGS"
            
            # Add Verilator include path if Ngveri objects exist
            if [ -f "$_VERILATOR_OBJ/verilated.o" ] && [ -d "$_VERILATOR_INCLUDE" ]; then
                _EXTRA_CFLAGS="$_EXTRA_CFLAGS -I$_VERILATOR_INCLUDE"
                # Export as environment variables for make to use
                export VERILATOR_INCLUDE="$_VERILATOR_INCLUDE"
                export VERILATOR_OBJ="$_VERILATOR_OBJ"
                export CPATH="$_VERILATOR_INCLUDE:${CPATH:-}"
            fi
            
            # Build code models - only if GNUmakefile exists
            if [ -f "$ICM_SRC/GNUmakefile" ]; then
                if (cd "$ICM_SRC" && \
                    export CFLAGS="$_EXTRA_CFLAGS" && \
                    export CXXFLAGS="$_EXTRA_CFLAGS -I$_VERILATOR_INCLUDE" && \
                    export CPATH="$_VERILATOR_INCLUDE:${CPATH:-}" && \
                    make CFLAGS="$_EXTRA_CFLAGS" CXXFLAGS="$_EXTRA_CFLAGS -I$_VERILATOR_INCLUDE" CXX="g++ -I$_VERILATOR_INCLUDE" VERILATOR_INCLUDE="$_VERILATOR_INCLUDE" VERILATOR_OBJ="$_VERILATOR_OBJ" -j$(nproc) 2>&1 | tee /tmp/code_model_compile.log); then
                    # Install compiled code models
                    mkdir -p "$CM_DIR"
                    local cm_count=0
                    for cm in "$ICM_SRC"/*/*.cm; do
                        [ -f "$cm" ] && cp "$cm" "$CM_DIR/" && cm_count=$((cm_count + 1))
                    done
                    
                    if [ "$cm_count" -gt 0 ]; then
                        echo "[eSim] ✓ $cm_count code models compiled and installed"
                    else
                        echo "[eSim] ⚠ No code models found after compilation"
                    fi
                else
                    echo "[eSim] ✗ Code model compilation failed"
                    tail -50 /tmp/code_model_compile.log 2>/dev/null | head -30
                fi
            else
                echo "[eSim] ⚠ GNUmakefile not found - pre-compiled core code models available"
            fi
        else
            echo "[eSim] ⚠ Code model source files not found"
        fi
    fi
}

# Only compile code models if NGHDL is being used (check for nghdl-simulator dir)
[ -d "$HOME/nghdl-simulator" ] && _compile_code_models

# ═══ AUTO-DETECT PYTHON VERSION ═══
# Different distros have different Python versions (3.10, 3.11, 3.12, 3.13, etc.)
detect_python() {
    if command -v python3 >/dev/null 2>&1; then
        PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
        PYTHON_MAJOR=$(python3 -c 'import sys; print(sys.version_info.major)')
    else
        # Fallback
        PYTHON_VERSION="3.12"
        PYTHON_MAJOR="3"
    fi
}
detect_python

# ═══ AUTO-DETECT LIBRARY PATHS ═══
# Different distros have libraries in different locations
detect_lib_paths() {
    # Default paths
    local sys_lib_paths=""
    
    # Debian/Ubuntu style
    [ -d "/usr/lib/x86_64-linux-gnu" ] && sys_lib_paths="/usr/lib/x86_64-linux-gnu:${sys_lib_paths}"
    
    # Fedora/RHEL/Arch style
    [ -d "/usr/lib64" ] && sys_lib_paths="/usr/lib64:${sys_lib_paths}"
    
    # Generic
    [ -d "/usr/lib" ] && sys_lib_paths="/usr/lib:${sys_lib_paths}"
    
    echo "$sys_lib_paths"
}
SYS_LIB_PATHS=$(detect_lib_paths)

# Include ~/.local/bin for pipx-installed tools like makerchip
export PATH="${HERE}/usr/bin:${HOME}/.local/bin:${PATH}"

# ═══ CHECK AND SETUP MAKERCHIP ═══
# Makerchip IDE is an external tool that must be installed via pipx
# This provides a first-run setup helper
setup_makerchip() {
    # Check if makerchip is available
    if ! command -v makerchip >/dev/null 2>&1; then
        # Not installed - show first-time notice (only once)
        if [ ! -f "$HOME/.esim/makerchip_notice_shown" ]; then
            echo ""
            echo "[eSim] Makerchip IDE not found."
            echo "[eSim] To use Makerchip features, install it with:"
            echo ""
            echo "    pipx install makerchip-app"
            echo "    pipx runpip makerchip-app install setuptools"
            echo ""
            echo "[eSim] Or with pip:"
            echo "    pip install --user makerchip-app"
            echo ""
            mkdir -p "$HOME/.esim"
            touch "$HOME/.esim/makerchip_notice_shown"
        fi
    else
        # Check if pkg_resources issue exists (setuptools missing)
        if ! makerchip --help >/dev/null 2>&1; then
            if makerchip --help 2>&1 | grep -q "pkg_resources"; then
                echo "[eSim] Fixing Makerchip setuptools dependency..."
                if command -v pipx >/dev/null 2>&1; then
                    pipx runpip makerchip-app install setuptools >/dev/null 2>&1 || true
                else
                    pip install --user setuptools >/dev/null 2>&1 || true
                fi
            fi
        fi
    fi
}
setup_makerchip 2>/dev/null

# LD_LIBRARY_PATH with multi-distro support
# Uses ${_ESIM_LIB_DIR} which is either the bundled dir (on glibc >= 2.38 or after filtering)
# or empty (on read-only mount with old glibc) to rely on system libs only
if [ -n "${_ESIM_LIB_DIR}" ]; then
    export LD_LIBRARY_PATH="${_ESIM_LIB_DIR}:${HERE}/lib/x86_64-linux-gnu:${HERE}/usr/lib/kicad:${HERE}/usr/lib/x86_64-linux-gnu:${HERE}/usr/lib/x86_64-linux-gnu/omc:${SYS_LIB_PATHS}${LD_LIBRARY_PATH}"
    export LIBRARY_PATH="${_ESIM_LIB_DIR}:${HERE}/usr/lib/x86_64-linux-gnu:${HERE}/usr/lib/x86_64-linux-gnu/omc:${SYS_LIB_PATHS}${LIBRARY_PATH}"
else
    # Read-only mode with old GLIBC: exclude bundled libs, use system only
    export LD_LIBRARY_PATH="${HERE}/lib/x86_64-linux-gnu:${HERE}/usr/lib/kicad:${SYS_LIB_PATHS}${LD_LIBRARY_PATH}"
    export LIBRARY_PATH="${SYS_LIB_PATHS}${LIBRARY_PATH}"
fi

# PYTHONPATH with dynamic Python version detection
# Priority: 1. Runtime-installed packages (correct Python version)
#           2. eSim source code
#           3. Bundled pure-Python packages (hdlparse, etc.)
#           4. System site-packages (for PyQt5, etc. installed by distro package manager)
BUNDLED_SITE_PACKAGES=""
for pyver in "$PYTHON_VERSION" 3.14 3.13 3.12 3.11 3.10 3.9 3.8; do
    if [ -d "${HERE}/usr/lib/python${pyver}/site-packages" ]; then
        BUNDLED_SITE_PACKAGES="${HERE}/usr/lib/python${pyver}/site-packages"
        break
    fi
done

# Detect system Python site-packages (needed for distro-installed PyQt5, etc.)
# Fedora/RHEL use /usr/lib64/pythonX.Y, Debian/Ubuntu use /usr/lib/python3/dist-packages
SYSTEM_SITE_PACKAGES=""
PYTHON_VERSION_DETECTED=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")' 2>/dev/null || echo "")
if [ -n "$PYTHON_VERSION_DETECTED" ]; then
    for sp in "/usr/lib64/python${PYTHON_VERSION_DETECTED}/site-packages" \
              "/usr/lib/python${PYTHON_VERSION_DETECTED}/site-packages" \
              "/usr/lib/python3/dist-packages" \
              "/usr/lib/python${PYTHON_VERSION_DETECTED}/dist-packages"; do
        if [ -d "$sp" ]; then
            SYSTEM_SITE_PACKAGES="${SYSTEM_SITE_PACKAGES:+${SYSTEM_SITE_PACKAGES}:}${sp}"
        fi
    done
fi

export PYTHONPATH="${_ESIM_PYDIR}:${HERE}/usr/share/eSim/src:${BUNDLED_SITE_PACKAGES}${SYSTEM_SITE_PACKAGES:+:${SYSTEM_SITE_PACKAGES}}"

# Generate loaders.cache at runtime - only for loaders that exist
LOADER_DIR="${HERE}/lib/x86_64-linux-gnu/gdk-pixbuf-2.0/2.10.0/loaders"
LOADER_CACHE="/tmp/esim-apprun-loaders-$$.cache"
if [ -d "$LOADER_DIR" ]; then
    echo "# GdkPixbuf loaders - runtime generated" > "$LOADER_CACHE"
    # Only add SVG, GIF, BMP, XPM, ICO, TIFF loaders that are actually bundled
    for loader in "$LOADER_DIR"/libpixbufloader-*.so; do
        [ -f "$loader" ] || continue
        name=$(basename "$loader" .so | sed 's/libpixbufloader-//')
        case "$name" in
            svg)  printf '\n"%s"\n"svg" 6 "gdk-pixbuf" "SVG" "LGPL"\n"image/svg+xml" ""\n"svg" "svgz" ""\n" <svg" "*    " 100\n' "$loader" >> "$LOADER_CACHE" ;;
            gif)  printf '\n"%s"\n"gif" 4 "gdk-pixbuf" "GIF" "LGPL"\n"image/gif" ""\n"gif" ""\n"GIF8" "" 100\n' "$loader" >> "$LOADER_CACHE" ;;
            bmp)  printf '\n"%s"\n"bmp" 5 "gdk-pixbuf" "BMP" "LGPL"\n"image/bmp" ""\n"bmp" ""\n"BM" "" 100\n' "$loader" >> "$LOADER_CACHE" ;;
            xpm)  printf '\n"%s"\n"xpm" 4 "gdk-pixbuf" "XPM" "LGPL"\n"image/x-xpixmap" ""\n"xpm" ""\n"/* XPM */" "" 100\n' "$loader" >> "$LOADER_CACHE" ;;
            ico)  printf '\n"%s"\n"ico" 5 "gdk-pixbuf" "ICO" "LGPL"\n"image/x-icon" ""\n"ico" "cur" ""\n' "$loader" >> "$LOADER_CACHE" ;;
            tiff) printf '\n"%s"\n"tiff" 5 "gdk-pixbuf" "TIFF" "LGPL"\n"image/tiff" ""\n"tiff" "tif" ""\n' "$loader" >> "$LOADER_CACHE" ;;
        esac
    done
    # Don't override - use system's built-in PNG/JPEG support
    # export GDK_PIXBUF_MODULE_FILE="$LOADER_CACHE"
fi
# export GDK_PIXBUF_MODULEDIR="$LOADER_DIR"

export XDG_DATA_DIRS="${HERE}/usr/share:${XDG_DATA_DIRS:-/usr/local/share:/usr/share}"
export GTK_DATA_PREFIX="${HERE}/usr"
export GTK_EXE_PREFIX="${HERE}/usr"
export GTK_THEME=Adwaita
# Disable canberra-gtk-module to prevent "Failed to load module" warning
export GTK_MODULES=""
export GTK3_MODULES=""
export GTK_PATH="${HERE}/usr/lib/gtk-3.0"
export QT_QPA_PLATFORMTHEME=gtk3

# ═══ NGSPICE AND NGHDL ENVIRONMENT VARIABLES ═══
# Generate runtime spinit with absolute AppImage paths for ngspice codemodels
mkdir -p "$HOME/.esim"
RUNTIME_SPINIT="$HOME/.esim/spinit"
cat > "$RUNTIME_SPINIT" << SPINIT_EOF
* Runtime-generated spinit for eSim AppImage
* Generated with absolute paths from: ${HERE}
alias exit quit
alias acct rusage all
set x11lineararcs
unset osdi_enabled

* Load code models with absolute AppImage paths
codemodel ${HERE}/usr/lib/ngspice/analog.cm
codemodel ${HERE}/usr/lib/ngspice/digital.cm
codemodel ${HERE}/usr/lib/ngspice/spice2poly.cm
codemodel ${HERE}/usr/lib/ngspice/table.cm
codemodel ${HERE}/usr/lib/ngspice/xtradev.cm
codemodel ${HERE}/usr/lib/ngspice/xtraevt.cm
SPINIT_EOF

# Add user NGHDL code model if it exists
if [ -f "$HOME/.nghdl/local/lib/ngspice/ghdl.cm" ]; then
    echo "" >> "$RUNTIME_SPINIT"
    echo "* Load user NGHDL code model" >> "$RUNTIME_SPINIT"
    echo "codemodel $HOME/.nghdl/local/lib/ngspice/ghdl.cm" >> "$RUNTIME_SPINIT"
fi

# Add user NgVeri code model if it exists (for Verilog-based simulations)
if [ -f "$HOME/.nghdl/local/lib/ngspice/Ngveri.cm" ]; then
    echo "" >> "$RUNTIME_SPINIT"
    echo "* Load user NgVeri code model" >> "$RUNTIME_SPINIT"
    echo "codemodel $HOME/.nghdl/local/lib/ngspice/Ngveri.cm" >> "$RUNTIME_SPINIT"
fi

# Tell ngspice where to find spinit
export SPICE_SCRIPTS="$HOME/.esim"

# ═══ AUTO-DETECT GHDL_PREFIX ═══
# Set GHDL_PREFIX for GHDL backend (needed for compile.sh subprocess)
# Search multiple locations used by different distros
detect_ghdl_prefix() {
    for ghdl_lib_base in "${HERE}/usr/lib/ghdl" /usr/lib/ghdl /usr/local/lib/ghdl \
                         /usr/lib/x86_64-linux-gnu/ghdl /usr/lib64/ghdl /usr/share/ghdl; do
        if [ -d "$ghdl_lib_base/llvm/vhdl/ieee" ]; then
            echo "$ghdl_lib_base/llvm/vhdl"
            return
        elif [ -d "$ghdl_lib_base/mcode/vhdl/ieee" ]; then
            echo "$ghdl_lib_base/mcode/vhdl"
            return
        elif [ -d "$ghdl_lib_base/ieee" ]; then
            echo "$ghdl_lib_base"
            return
        fi
    done
    echo "${HERE}/usr/lib/ghdl"
}
export GHDL_PREFIX=$(detect_ghdl_prefix)

# ═══ UPDATE NGHDL CONFIG.INI WITH CURRENT APPIMAGE MOUNT PATH ═══
# This MUST be regenerated on every launch because the AppImage mount point changes
mkdir -p "$HOME/.nghdl"

# Find verilator (may be in different locations)
VERILATOR_BIN="/usr/bin/verilator"
for vpath in /usr/bin/verilator /usr/local/bin/verilator "${HERE}/usr/bin/verilator"; do
    [ -x "$vpath" ] && { VERILATOR_BIN="$vpath"; break; }
done

cat > "$HOME/.nghdl/config.ini" << NGHDLCFG
[NGHDL]
NGHDL_HOME = $HOME/nghdl-simulator
DIGITAL_MODEL = $HOME/nghdl-simulator/src/xspice/icm
RELEASE = $HOME/nghdl-simulator

[SRC]
SRC_HOME = ${HERE}/usr/share/eSim/nghdl
LICENSE = ${HERE}/usr/share/eSim/nghdl/LICENSE

[COMPILER]
GHDL = ${HERE}/usr/bin/ghdl
VERILATOR = ${VERILATOR_BIN}
GHDL_PREFIX = ${GHDL_PREFIX}
MODEL_COMPILER = ${HERE}/usr/bin/ghdl
NGHDLCFG

# Create essential directories for NGHDL/NgVeri if they don't exist
mkdir -p "$HOME/nghdl-simulator/src/xspice/icm/Ngveri"
mkdir -p "$HOME/nghdl-simulator/src/xspice/icm/ghdl"
touch "$HOME/nghdl-simulator/src/xspice/icm/Ngveri/modpath.lst" 2>/dev/null
touch "$HOME/nghdl-simulator/src/xspice/icm/ghdl/modpath.lst" 2>/dev/null

# KiCad root paths for resources
export KICAD="${HERE}/usr/share/kicad"
export KICAD6="${HERE}/usr/share/kicad"
export KICAD_DATA="${HERE}/usr/share/kicad"
export KICAD6_DATA="${HERE}/usr/share/kicad"

export KICAD_SYMBOL_DIR="${HERE}/usr/share/kicad/symbols"
export KICAD_FOOTPRINT_DIR="${HERE}/usr/share/kicad/footprints"
export KICAD_TEMPLATE_DIR="${HERE}/usr/share/kicad/template"
export KICAD_3DMODEL_DIR="${HERE}/usr/share/kicad/3dmodels"
export KICAD6_SYMBOL_DIR="$KICAD_SYMBOL_DIR"
export KICAD7_SYMBOL_DIR="$KICAD_SYMBOL_DIR"

# ═══ ENSURE USER NGHDL/NGVERI LIBRARIES ARE REGISTERED IN KICAD ═══
# This runs on every launch to ensure user-converted symbols are accessible
ensure_user_libs() {
    local kc=""
    for v in 8.0 7.0 6.0 5.0 ""; do
        [ -d "$HOME/.config/kicad${v:+/$v}" ] && { kc="$HOME/.config/kicad${v:+/$v}"; break; }
    done
    [ -z "$kc" ] && return 0
    [ ! -f "$kc/sym-lib-table" ] && return 0
    
    # Create user symbol directory if it doesn't exist
    mkdir -p "$HOME/.esim/symbols"
    
    # Ensure empty symbol files exist for registration
    [ ! -f "$HOME/.esim/symbols/eSim_Nghdl.kicad_sym" ] && \
        echo '(kicad_symbol_lib (version 20211014) (generator eSim_nghdl))' > "$HOME/.esim/symbols/eSim_Nghdl.kicad_sym"
    [ ! -f "$HOME/.esim/symbols/eSim_Ngveri.kicad_sym" ] && \
        echo '(kicad_symbol_lib (version 20211014) (generator eSim_ngveri))' > "$HOME/.esim/symbols/eSim_Ngveri.kicad_sym"
    
    # Add eSim_Nghdl_User if not present
    if ! grep -q "eSim_Nghdl_User" "$kc/sym-lib-table" 2>/dev/null; then
        # Use Python for reliable file manipulation
        python3 -c "
import sys
try:
    with open('$kc/sym-lib-table', 'r') as f:
        content = f.read()
    if 'eSim_Nghdl_User' not in content:
        content = content.rstrip()
        if content.endswith(')'):
            content = content[:-1].rstrip()
        content += '\n  (lib (name \"eSim_Nghdl_User\")(type \"KiCad\")(uri \"$HOME/.esim/symbols/eSim_Nghdl.kicad_sym\")(options \"\")(descr \"User NGHDL Converted Symbols\"))\n)\n'
        with open('$kc/sym-lib-table', 'w') as f:
            f.write(content)
except: pass
" 2>/dev/null
    fi
    
    # Add eSim_Ngveri_User if not present
    if ! grep -q "eSim_Ngveri_User" "$kc/sym-lib-table" 2>/dev/null; then
        python3 -c "
import sys
try:
    with open('$kc/sym-lib-table', 'r') as f:
        content = f.read()
    if 'eSim_Ngveri_User' not in content:
        content = content.rstrip()
        if content.endswith(')'):
            content = content[:-1].rstrip()
        content += '\n  (lib (name \"eSim_Ngveri_User\")(type \"KiCad\")(uri \"$HOME/.esim/symbols/eSim_Ngveri.kicad_sym\")(options \"\")(descr \"User NgVeri Converted Symbols\"))\n)\n'
        with open('$kc/sym-lib-table', 'w') as f:
            f.write(content)
except: pass
" 2>/dev/null
    fi
}
ensure_user_libs 2>/dev/null &

exec "${HERE}/usr/bin/esim" "$@"
EOF
    
    chmod +x "$APPDIR/AppRun"
    ok "eSim installed"
}

create_appimage() {
    step 10 "Creating AppImage"
    cd "$BUILD"
    
    # ═══ CRITICAL: REMOVE GLIBC CORE LIBRARIES ═══
    # These MUST come from the host system - bundling them breaks cross-distro compatibility
    # glibc symbols like __tunable_is_initialized differ between versions
    # NOTE: Globs MUST be outside quotes to expand properly!
    progress "Removing bundled glibc libraries (must use host system's glibc)..."
    GLIBC_BEFORE=$(find "$APPDIR" -maxdepth 3 \( -name "libc.so*" -o -name "libm.so*" -o -name "libpthread.so*" -o -name "libdl.so*" -o -name "librt.so*" \) -type f 2>/dev/null | wc -l)
    rm -f "$APPDIR"/usr/lib/libc.so* "$APPDIR"/usr/lib/libm.so* \
          "$APPDIR"/usr/lib/libpthread.so* "$APPDIR"/usr/lib/libdl.so* \
          "$APPDIR"/usr/lib/librt.so* "$APPDIR"/usr/lib/libresolv.so* \
          "$APPDIR"/usr/lib/libnss_*.so* "$APPDIR"/usr/lib/ld-linux*.so* \
          "$APPDIR"/lib/libc.so* "$APPDIR"/lib/libm.so* \
          "$APPDIR"/lib/x86_64-linux-gnu/libc.so* "$APPDIR"/lib/x86_64-linux-gnu/libm.so* \
          2>/dev/null || true
    [ "$GLIBC_BEFORE" -gt 0 ] && ok "Removed $GLIBC_BEFORE bundled glibc libraries"

    # ═══ REMOVE INCOMPATIBLE LIBPYTHON ═══
    # Only keep libpython for the build system's Python version.
    # Other distros will use their own system libpython.
    PYVER_BUILD=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")' 2>/dev/null || echo "3.12")
    for pylib in "$APPDIR"/usr/lib/libpython*.so*; do
        [ -f "$pylib" ] || continue
        case "$(basename "$pylib")" in
            libpython${PYVER_BUILD}*) ;; # Keep the build system's version
            *) rm -f "$pylib" 2>/dev/null; progress "Removed incompatible $(basename "$pylib")" ;;
        esac
    done

    # Create actual directories at AppDir root for KiCad path resolution
    # Symlinks don't work properly in AppImage squashfs - use hardlinks instead
    mkdir -p "$APPDIR/share/kicad/resources"
    mkdir -p "$APPDIR/share/kicad/symbols"
    mkdir -p "$APPDIR/share/kicad/footprints"
    mkdir -p "$APPDIR/share/kicad/template"
    
    # Copy resources (small files, hardlinks won't work across build directories)
    cp -r "$APPDIR/usr/share/kicad/resources"/* "$APPDIR/share/kicad/resources/" 2>/dev/null || true
    
    # Create symlinks within share for large directories
    cd "$APPDIR/share/kicad"
    ln -sf ../../usr/share/kicad/symbols symbols 2>/dev/null || rm -rf symbols && ln -sf ../../usr/share/kicad/symbols symbols
    ln -sf ../../usr/share/kicad/footprints footprints 2>/dev/null || rm -rf footprints && ln -sf ../../usr/share/kicad/footprints footprints  
    ln -sf ../../usr/share/kicad/template template 2>/dev/null || rm -rf template && ln -sf ../../usr/share/kicad/template template
    cd "$BUILD"
    
    progress "Created share/kicad structure for KiCad resource paths"
    
    # Run appimagetool with --appimage-extract-and-run for container/distrobox compatibility
    # (FUSE may not be available in containers)
    ARCH=x86_64 "$DL/appimagetool-x86_64.AppImage" --appimage-extract-and-run "$APPDIR" "eSim-${ESIM_VERSION}.AppImage" 2>&1 | tail -5 || true
    [ -f "eSim-${ESIM_VERSION}.AppImage" ] || die "AppImage creation failed"
    chmod +x "eSim-${ESIM_VERSION}.AppImage"
    ok "AppImage created ($(du -h "eSim-${ESIM_VERSION}.AppImage" | cut -f1))"
}

show_success() {
    echo ""
    echo -e "${GREEN}${BOLD}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}${BOLD}║  ✓ eSim ${ESIM_VERSION}           ║${NC}"
    echo -e "${GREEN}${BOLD}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${BOLD}📦 File:${NC} ${CYAN}$BUILD/eSim-${ESIM_VERSION}.AppImage${NC}"
    echo -e "${BOLD}📏 Size:${NC} $(du -h "$BUILD/eSim-${ESIM_VERSION}.AppImage" | cut -f1)"
    echo ""
    echo ""
    echo -e "${BOLD}🚀 Usage:${NC}"
    echo -e "   ${CYAN}./build-eSim-AppImage/eSim-${ESIM_VERSION}.AppImage${NC}"
    echo ""
    echo -e "${BOLD}💡 Quick Start:${NC}"
    echo -e "   1. Launch: ${CYAN}./build-eSim-AppImage/eSim-${ESIM_VERSION}.AppImage${NC}"
    echo -e "   2. Open KiCad from eSim"
    echo -e "   3. Create new schematic → Press ${YELLOW}'A'${NC} to add component"
    echo -e "   4. Search for any component (PWR_FLAG, resistor, 555, etc)"
    echo -e "   5. All libraries are ready to use!"
    echo ""
    echo -e "${BOLD}📤 Distribution:${NC}"
    echo -e "   This AppImage runs on any Linux distribution!"
    echo -e "   Share it with others - libraries auto-configure for everyone."
    echo ""
    echo -e "${BOLD}🔧 Optional: Makerchip IDE (for TL-Verilog):${NC}"
    echo -e "   Makerchip is an external cloud-based IDE for digital design."
    echo -e "   To use Makerchip features in eSim, install it separately:"
    echo ""
    echo -e "   ${CYAN}# Using pipx (recommended):${NC}"
    echo -e "   ${YELLOW}pipx install makerchip-app${NC}"
    echo -e "   ${YELLOW}pipx runpip makerchip-app install setuptools${NC}"
    echo ""
    echo -e "   ${CYAN}# Or using pip:${NC}"
    echo -e "   ${YELLOW}pip install --user makerchip-app${NC}"
    echo ""
}

main() {
    print_header
    detect_distro         
    install_prerequisites 
    check_system
    setup_sudo
    setup_directories
    install_deps
    download_tools
    prepare_esim
    bundle_gtk_resources
    bundle_kicad
    install_esim
    create_appimage
    show_success
}

main "$@"