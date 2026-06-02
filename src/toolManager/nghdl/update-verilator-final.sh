#!/bin/bash
set -e  # Stop on first error
set -x  # Debugging: Print commands before execution

update_verilator_full() {
    local package_dir="./nghdl/packages"
    local json_file="../information.json"
    local verilator_versions=("verilator-4.228.tar.gz" "verilator-5.020.tar.gz" "verilator-5.026.tar.gz" "verilator-5.030.tar.gz")

    # Ensure the script is called with an argument
    if [ -z "$1" ]; then
        echo "Error: No Verilator version specified!"
        exit 1
    fi

    local selected_version="verilator-$1.tar.gz"

    # Validate the version exists in the array
    if [[ ! " ${verilator_versions[@]} " =~ " ${selected_version} " ]]; then
        echo "Error: Invalid Verilator version specified!"
        exit 1
    fi

    echo "Installing Verilator version: $1"

    remove_old_verilator() {
        echo "Removing existing Verilator installation..."
        sudo rm -rf /usr/local/bin/verilator /usr/local/share/verilator /usr/local/include/verilator /usr/local/lib/verilator*
        echo "Old Verilator removed successfully."
    }

    install_verilator() {
        local verilator_tarball="$package_dir/$selected_version"
        local verilator_version=$(basename "$verilator_tarball" .tar.gz)
        local script_dir="$(cd "$(dirname "$0")" && pwd)"

        echo "Installing dependencies for $verilator_version..."
        if command -v apt &>/dev/null; then
            sudo apt update
            sudo apt install -y make autoconf g++ flex bison ccache help2man perl python3 jq
        elif command -v yum &>/dev/null; then
            sudo yum install -y make autoconf flex bison which
            sudo yum groupinstall -y 'Development Tools'
        else
            echo "Unsupported package manager. Please install dependencies manually."
            exit 1
        fi

        mkdir -p "$package_dir"
        tar -xzf "$verilator_tarball" -C "$package_dir"

        if [[ ! -d "$package_dir/$verilator_version" ]]; then
            verilator_version=$(tar -tf "$verilator_tarball" | head -1 | cut -d '/' -f1)
        fi

        cd "$package_dir/$verilator_version" || exit 1

        if [[ ! -f configure ]]; then
            echo "'configure' not found. Running bootstrap..."
            [[ -f autogen.sh ]] && chmod +x autogen.sh && ./autogen.sh || autoreconf -i
        fi

        chmod +x configure
        ./configure
        make -j$(nproc)
        sudo make install

        if command -v verilator &>/dev/null; then
            echo "Verilator installed successfully!"
        else
            echo "Error: Verilator installation failed."
            exit 1
        fi

        # Remove unnecessary files to save space
        rm -rf docs examples include test_regress bin ci nodist autom4te.cache
        find . -type f ! -name "config.status" ! -name "configure.ac" ! -name "Makefile.in" ! -name "verilator.1" ! -name "configure" ! -name "Makefile" ! -name "src" ! -name "verilator.pc" -delete

        export PATH="/usr/local/bin:$PATH"

        cd "$script_dir"
        echo "Current directory before JSON update: $(pwd)"

        update_verilator_json "$verilator_version"

        # Remove extracted folder after installation
        # echo "Cleaning up extracted files..."
        # rm -rf "./packages/$verilator_version"

        echo "Verilator $verilator_version installed successfully!"
    }

    update_verilator_json() {
        local verilator_version="$1"
        local install_date=$(date '+%Y-%m-%d %H:%M:%S')

        if [[ -z "$verilator_version" ]]; then
            echo "Error: Verilator version is empty. JSON not updated."
            exit 1
        fi

        if ! command -v jq &>/dev/null; then
            echo "Installing jq for JSON updates..."
            if command -v apt &>/dev/null; then
                sudo apt install -y jq
            elif command -v yum &>/dev/null; then
                sudo yum install -y jq
            else
                echo "Error: jq is required but cannot be installed automatically."
                exit 1
            fi
        fi

        jq --arg version "$verilator_version" --arg date "$install_date" \
           '(.important_packages[] | select(.package_name == "verilator")) |= (.version = $version | .installed_date = $date)' \
           "$json_file" > temp.json && mv temp.json "$json_file"

        echo "Updated Verilator version to $verilator_version in $json_file"
    }

    remove_old_verilator
    install_verilator
}

update_verilator_full "$1"
