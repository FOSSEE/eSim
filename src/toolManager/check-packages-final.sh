#!/bin/bash

# Function to check installed packages and update JSON
check_and_update_packages() {
    JSON_FILE="information.json"
    TEMP_FILE="packages_temp.json"

    jq '.important_packages' "$JSON_FILE" | jq -c '.[]' | while read -r package; do
        PACKAGE_NAME=$(echo "$package" | jq -r '.package_name')

        # Check if the package is installed (using dpkg, which, or version check)
        if dpkg -l | grep -qw "$PACKAGE_NAME" || which "$PACKAGE_NAME" > /dev/null 2>&1 || "$PACKAGE_NAME" --version > /dev/null 2>&1; then
            INSTALLED="Yes"
        else
            INSTALLED="No"
        fi

        # Update JSON with the installation status
        jq --arg name "$PACKAGE_NAME" --arg status "$INSTALLED" '
            (.important_packages[] | select(.package_name == $name) | .installed) = $status
        ' "$JSON_FILE" > "$TEMP_FILE" && mv "$TEMP_FILE" "$JSON_FILE"

    done

    echo "Package check completed. Updated JSON saved in $JSON_FILE."
}

# Execute the function
check_and_update_packages
