# src/frontEnd/esim_paths.py
import os
import sys

def get_base_dir():
    """
    Returns the project root directory.
    - In a frozen PyInstaller .app: sys._MEIPASS (Contents/MacOS/)
    - In development: two levels up from this file (eSim-2.5/)
    """
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

def resource_path(*relative_parts):
    """Build an absolute path to a bundled resource."""
    return os.path.join(get_base_dir(), *relative_parts)