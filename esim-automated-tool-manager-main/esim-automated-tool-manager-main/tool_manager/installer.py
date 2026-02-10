import platform
import subprocess
from tool_manager.logger import log_info, log_error

def install_tool(tool_name):
    os_type = platform.system()

    try:
        if os_type == "Linux":
            if tool_name.lower() == "ngspice":
                subprocess.run(["sudo", "apt", "install", "-y", "ngspice"])
            elif tool_name.lower() == "kicad":
                subprocess.run(["sudo", "apt", "install", "-y", "kicad"])
            log_info(f"{tool_name} installation attempted on Linux")

        elif os_type == "Windows":
            print(f"[INFO] Please install {tool_name} manually or using Chocolatey.")
            log_info(f"{tool_name} installation guidance shown for Windows")

        else:
            print(f"[WARN] OS not supported for automatic install.")
            log_error("Unsupported OS")

    except Exception as e:
        log_error(f"Installation failed for {tool_name}: {str(e)}")
