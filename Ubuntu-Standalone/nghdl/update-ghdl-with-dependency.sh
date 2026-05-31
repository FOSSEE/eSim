#!/bin/bash

update_dependency() {
    echo "Updating dependencies for the selected GHDL version..."
    
    echo "Updating package lists..."
    sudo apt update -y

    local ghdl_version="$1"

    case "$ghdl_version" in
        "3.0.0")
            llvm_version=12
            gnat_version=10
            clang_version=12
            ;;
        "4.0.0")
            llvm_version=14
            gnat_version=10
            clang_version=14
            ;;
        "4.1.0")
            llvm_version=16
            gnat_version=10
            clang_version=16
            ;;
        "nightly")
            llvm_version=17
            gnat_version=10
            clang_version=17
            ;;
        *)
            echo "No compatible GHDL version detected! Exiting..."
            return 1
            ;;
    esac

    echo "Selected GHDL version: $ghdl_version"
    echo "Installing LLVM version: $llvm_version"
    echo "Installing GNAT version: $gnat_version"
    echo "Installing Clang version: $clang_version"

    echo "Removing older versions of Clang and LLVM..."
    sudo apt remove -y clang llvm llvm-dev
    sudo apt autoremove -y

    echo "Adding official LLVM repository..."
    wget https://apt.llvm.org/llvm.sh -O llvm.sh
    chmod +x llvm.sh
    sudo ./llvm.sh ${llvm_version}
    rm llvm.sh
    
    echo "Installing LLVM-${llvm_version}..."
    sudo apt install -y llvm-${llvm_version} llvm-${llvm_version}-dev

    echo "Setting up LLVM environment variables..."
    export PATH="/usr/lib/llvm-${llvm_version}/bin:$PATH"
    export LD_LIBRARY_PATH="/usr/lib/llvm-${llvm_version}/lib:$LD_LIBRARY_PATH"
    export C_INCLUDE_PATH="/usr/lib/llvm-${llvm_version}/include:$C_INCLUDE_PATH"
    export CPLUS_INCLUDE_PATH="/usr/lib/llvm-${llvm_version}/include:$CPLUS_INCLUDE_PATH"
    
    echo "Installing GNAT-${gnat_version}..."
    sudo apt install -y gnat-${gnat_version}

    echo "Installing Clang-${clang_version}..."
    sudo apt install -y clang-${clang_version}

    echo "Setting Clang-${clang_version} as the default..."
    sudo update-alternatives --install /usr/bin/clang clang /usr/bin/clang-${clang_version} 100
    sudo update-alternatives --install /usr/bin/clang++ clang++ /usr/bin/clang++-${clang_version} 100

    echo "Installing additional dependencies..."
    sudo apt install -y make zlib1g-dev libcanberra-gtk-module libcanberra-gtk3-module libxaw7 libxaw7-dev build-essential g++ gcc libc++-dev libc++abi-dev libstdc++-10-dev

    echo "Setting C++ include path explicitly..."
    export CPLUS_INCLUDE_PATH=/usr/include/c++/12:/usr/include/x86_64-linux-gnu/c++/12:$CPLUS_INCLUDE_PATH

    echo "Dependency installation completed successfully!"

    # Capture Installed Versions
    llvm_installed_version=$(llvm-config --version 2>/dev/null | tr -d '\n')
    gnat_installed_version=$(gnat --version 2>/dev/null | head -n 1 | tr -d '\n')
    clang_installed_version=$(clang --version 2>/dev/null | head -n 1 | tr -d '\n')
    make_installed_version=$(make --version 2>/dev/null | head -n 1 | tr -d '\n')
    zlib_installed_version=$(dpkg -s zlib1g-dev 2>/dev/null | grep 'Version' | awk '{print $2}' | tr -d '\n')
    gtk_canberra_version=$(dpkg -s libcanberra-gtk-module 2>/dev/null | grep 'Version' | awk '{print $2}' | tr -d '\n')
    libxaw7_version=$(dpkg -s libxaw7 2>/dev/null | grep 'Version' | awk '{print $2}' | tr -d '\n')
    libxaw7_dev_version=$(dpkg -s libxaw7-dev 2>/dev/null | grep 'Version' | awk '{print $2}' | tr -d '\n')

    # Update information.json
    jq --arg llvm_version "$llvm_installed_version" \
       --arg gnat_version "$gnat_installed_version" \
       --arg clang_version "$clang_installed_version" \
       --arg make_version "$make_installed_version" \
       --arg zlib_version "$zlib_installed_version" \
       --arg gtk_version "$gtk_canberra_version" \
       --arg libxaw7_version "$libxaw7_version" \
       --arg libxaw7_dev_version "$libxaw7_dev_version" \
       '.nghdl_dependencies |= map(
          if .dependency_name == "llvm" then .version = $llvm_version
          elif .dependency_name == "gnat" then .version = $gnat_version
          elif .dependency_name == "clang" then .version = $clang_version
          elif .dependency_name == "make" then .version = $make_version
          elif .dependency_name == "zlib1g-dev" then .version = $zlib_version
          elif .dependency_name == "libcanberra-gtk-module" then .version = $gtk_version
          elif .dependency_name == "libxaw7" then .version = $libxaw7_version
          elif .dependency_name == "libxaw7-dev" then .version = $libxaw7_dev_version
          else . end)' ./information.json > ./information_tmp.json && mv ./information_tmp.json ./information.json

    echo "Updated dependency versions in information.json!"
}

install_ghdl() {
    local ghdl_version="$1"

    if [ -z "$ghdl_version" ]; then
        echo "Error: No GHDL version specified!"
        exit 1
    fi

    local package_dir="./nghdl/packages"
    local json_file="./information.json"

    echo "Selected GHDL version: $ghdl_version"

    update_dependency "$ghdl_version"

    echo "Removing previous GHDL installation..."
    sudo apt-get remove --purge -y ghdl
    sudo apt-get autoremove -y
    sudo apt-get autoclean

    package_path="$package_dir/ghdl-$ghdl_version.tar.gz"
    extract_path="$package_dir/ghdl-$ghdl_version"

    if [ ! -f "$package_path" ]; then
        echo "Error: $package_path not found. Ensure the file exists."
        exit 1
    fi

    if [ -d "$extract_path" ]; then
        echo "Removing existing extracted folder: $extract_path"
        rm -rf "$extract_path"
    fi

    echo "Extracting ghdl-$ghdl_version..."
    tar -xzf "$package_path" -C "$package_dir" || {
        echo "Error extracting $package_path. Please check the file format."
        exit 1
    }

    cd "$extract_path" || exit 1

    llvm_detected_version=$(llvm-config --version 2>/dev/null | cut -d. -f1)

    if [ -z "$llvm_detected_version" ]; then
        echo "Error: LLVM is not installed or detected."
        exit 1
    fi

    echo "Detected LLVM version: $llvm_detected_version"

    echo "Configuring ghdl-$ghdl_version build..."
    chmod +x configure
    ./configure --with-llvm-config="/usr/bin/llvm-config-$llvm_detected_version"

    echo "Building and installing ghdl-$ghdl_version..."
    make && sudo make install || {
        echo "Error during installation."
        exit 1
    }

    cd ../..

    if ! command -v ghdl &>/dev/null; then
        echo "GHDL binary not found in PATH. Adding it now."
        export PATH=$PATH:/usr/local/bin
    fi

    if command -v ghdl &>/dev/null; then
        installed_version=$(ghdl --version | head -n 1 | awk '{print $2}')
        echo "GHDL installation successful! Installed version: $installed_version"
        update_ghdl_json "$installed_version"
    else
        echo "Error: GHDL was not installed correctly."
        exit 1
    fi

    # ✅ Remove extracted folder after successful installation
    echo "Cleaning up extracted files..."
    rm -rf "./$extract_path"

    echo "ghdl-$ghdl_version installed successfully."
}


update_ghdl_json() {
    local ghdl_version="$1"
    local install_date=$(date '+%Y-%m-%d %H:%M:%S')

    if [[ -z "$ghdl_version" ]]; then
        echo "Error: GHDL version is empty. JSON not updated."
        return 1
    fi

    jq --arg version "$ghdl_version" --arg date "$install_date" \
       '(.important_packages[] | select(.package_name == "ghdl")) |= (.version = $version | .installed_date = $date)' \
       "../information.json" > "./information_tmp.json" && mv "./information_tmp.json" "../information.json"

    echo "Updated GHDL version to $ghdl_version in information.json"
}

install_ghdl "$1"
