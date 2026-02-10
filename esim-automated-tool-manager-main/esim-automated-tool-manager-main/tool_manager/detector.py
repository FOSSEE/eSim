import subprocess
from tool_manager.logger import log_info, log_error

def check_tool(tool_name, command):
    try:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        output = result.stdout.strip() or result.stderr.strip()
        log_info(f"{tool_name} detected: {output}")
        return True, output
    except FileNotFoundError:
        log_error(f"{tool_name} not found")
        return False, None
