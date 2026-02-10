import os

def is_in_path(executable):
    for path in os.environ.get("PATH", "").split(os.pathsep):
        if os.path.exists(os.path.join(path, executable)):
            return True
    return False
