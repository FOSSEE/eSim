import subprocess

def check_dependency(command):
    try:
        subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return True
    except FileNotFoundError:
        return False
