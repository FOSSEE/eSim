import os
import sys

# Setting PYTHONPATH relative to the location of pathmagic.py
frontEnd_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(frontEnd_dir)
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)
