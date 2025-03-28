import os
import subprocess
import json
from datetime import datetime
from logging_setup import log_info, log_error, log_warning

# Load dependencies from the JSON file
def load_dependencies():
    json_path = "install_details.json"
    if not os.path.exists(json_path):
        log_warning(f"Error: {json_path} not found.")
        return []

    try:
        with open(json_path, "r") as f:
            data = json.load(f)
            return data.get("dependencies", [])
    except json.JSONDecodeError as e:
        log_error(f"Error: Failed to parse {json_path}: {e}")
        return []

dependencies = load_dependencies()

# Utility to run a system command
def run_command(command):
    """Run a system command and handle errors"""
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        log_error(f"Error: Command '{e.cmd}' failed with exit code {e.returncode}")

# Install dependencies using Chocolatey
def install_dependencies_with_choco(dependencies):
    log_info("Installing dependencies with Chocolatey...")
    for dep in dependencies:
        log_info(f"Installing {dep}...")
        run_command(f"choco install {dep} -y")

# Update the JSON file for dependencies
def update_dependency_status():
    json_path = "install_details.json"
    if not os.path.exists(json_path):
        log_warning(f"Error: {json_path} not found.")
        return

    try:
        with open(json_path, "r") as f:
            data = json.load(f)

        # Update or add the 'dependencies' status
        updated = False
        for package in data.get("important_packages", []):
            if package.get("package_name") == "dependencies":
                package["installed"] = "Yes"
                package["installed_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                updated = True
                break

        if not updated:
            # Add a new entry for dependencies if it doesn't exist
            data["important_packages"].append({
                "package_name": "dependencies",
                "installed": "Yes",
                "installed_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

        with open(json_path, "w") as f:
            json.dump(data, f, indent=4)
        log_info("install_details.json updated successfully.")
    except json.JSONDecodeError as e:
        log_error(f"Error: Failed to parse {json_path}: {e}")
    except Exception as e:
        log_error(f"Error: {e}")

# Main function to manage dependencies
def manage_dependencies():
    if not dependencies:
        log_warning("No dependencies to install.")
        return

    install_dependencies_with_choco(dependencies)
    update_dependency_status()

if __name__ == "__main__":
    manage_dependencies()
