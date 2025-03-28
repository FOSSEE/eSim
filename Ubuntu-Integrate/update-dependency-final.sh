#!/bin/bash

function error_exit {
    echo "Error occurred. Exiting..."
    exit 1
}

function updateDependency {
    set +e      # Temporarily disable exit on error
    trap "" ERR # Do not trap on error of any command

    # Ensure jq is installed
    echo "Installing jq (JSON processor) if not already installed..."
    sudo apt-get install -y jq

    # Update apt repository
    echo "Updating apt index files..................."
    sudo apt-get update

    # Upgrade all apt packages to their latest versions
    echo "Upgrading system packages.................."
    sudo apt-get upgrade -y

    set -e      # Re-enable exit on error
    trap error_exit ERR

    # Install/Update required packages
    echo "Installing/Updating xterm.................."
    sudo apt-get install -y xterm
    
    echo "Installing/Updating python3-psutil.................."
    sudo apt-get install -y python3-psutil
    
    echo "Installing/Updating python3-pyqt5.................."
    sudo apt-get install -y python3-pyqt5
    
    echo "Installing/Updating python3-matplotlib.................."
    sudo apt-get install -y python3-matplotlib
    
    echo "Installing/Updating python3-distutils.................."
    sudo apt-get install -y python3-distutils
    
    echo "Installing/Updating python3-pip.................."
    sudo apt-get install -y python3-pip

    # Install/Update Python packages
    echo "Installing/Updating Watchdog..............."
    pip3 install --upgrade watchdog
    
    echo "Installing/Updating Hdlparse..............."
    pip3 install --upgrade https://github.com/hdl/pyhdlparser/tarball/master
    
    echo "Installing/Updating Makerchip.............."
    pip3 install --upgrade makerchip-app
    
    echo "Installing/Updating SandPiper Saas........."
    pip3 install --upgrade sandpiper-saas

    echo "Update process completed successfully."
    
    update_json
}

function update_json {
    json_file="information.json"
    echo "Updating JSON file with package versions..."

    jq --arg xterm_version "$(dpkg-query -W -f='${Version}\n' xterm 2>/dev/null || echo "Not Installed")" \
       --arg psutil_version "$(pip3 show psutil | grep -i version | awk '{print $2}' 2>/dev/null || echo "Not Installed")" \
       --arg pyqt5_version "$(pip3 show PyQt5 | grep -i version | awk '{print $2}' 2>/dev/null || echo "Not Installed")" \
       --arg matplotlib_version "$(pip3 show matplotlib | grep -i version | awk '{print $2}' 2>/dev/null || echo "Not Installed")" \
       --arg distutils_version "$(dpkg-query -W -f='${Version}\n' python3-distutils 2>/dev/null || echo "Not Installed")" \
       --arg pip_version "$(pip3 --version | awk '{print $2}' 2>/dev/null || echo "Not Installed")" \
       --arg watchdog_version "$(pip3 show watchdog | grep -i version | awk '{print $2}' 2>/dev/null || echo "Not Installed")" \
       --arg hdlparse_version "$(pip3 show hdlparse | grep -i version | awk '{print $2}' 2>/dev/null || echo "Not Installed")" \
       --arg makerchip_version "$(pip3 show makerchip-app | grep -i version | awk '{print $2}' 2>/dev/null || echo "Not Installed")" \
       --arg sandpiper_version "$(pip3 show sandpiper-saas | grep -i version | awk '{print $2}' 2>/dev/null || echo "Not Installed")" \
       '.dependencies |= map(if .dependency_name == "xterm" then .version = $xterm_version
        elif .dependency_name == "python3-psutil" then .version = $psutil_version
        elif .dependency_name == "python3-pyqt5" then .version = $pyqt5_version
        elif .dependency_name == "python3-matplotlib" then .version = $matplotlib_version
        elif .dependency_name == "python3-distutils" then .version = $distutils_version
        elif .dependency_name == "python3-pip" then .version = $pip_version
        else . end)
        | .pip_packages |= map(if .pip_package_name == "watchdog" then .version = $watchdog_version
        elif .pip_package_name == "hdlparse" then .version = $hdlparse_version
        elif .pip_package_name == "makerchip-app" then .version = $makerchip_version
        elif .pip_package_name == "sandpiper-saas" then .version = $sandpiper_version
        else . end)' "$json_file" > temp.json && mv temp.json "$json_file"
}

function printVersions {
    json_file="information.json"
    echo -e "\nInstalled package versions:"
    echo "Xterm: $(jq -r '.dependencies[] | select(.dependency_name=="xterm") | .version' "$json_file")"
    echo "Psutil: $(jq -r '.dependencies[] | select(.dependency_name=="python3-psutil") | .version' "$json_file")"
    echo "PyQt5: $(jq -r '.dependencies[] | select(.dependency_name=="python3-pyqt5") | .version' "$json_file")"
    echo "Matplotlib: $(jq -r '.dependencies[] | select(.dependency_name=="python3-matplotlib") | .version' "$json_file")"
    echo "Distutils: $(jq -r '.dependencies[] | select(.dependency_name=="python3-distutils") | .version' "$json_file")"
    echo "Pip3: $(jq -r '.dependencies[] | select(.dependency_name=="python3-pip") | .version' "$json_file")"
    echo "Watchdog: $(jq -r '.pip_packages[] | select(.pip_package_name=="watchdog") | .version' "$json_file")"
    echo "Hdlparse: $(jq -r '.pip_packages[] | select(.pip_package_name=="hdlparse") | .version' "$json_file")"
    echo "Makerchip: $(jq -r '.pip_packages[] | select(.pip_package_name=="makerchip-app") | .version' "$json_file")"
    echo "SandPiper Saas: $(jq -r '.pip_packages[] | select(.pip_package_name=="sandpiper-saas") | .version' "$json_file")"
}

# Run update function
updateDependency

# Print versions
printVersions
