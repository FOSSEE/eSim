import os
import sys

# Calculate absolute path to the 'src' directory relative to this file
# __file__ is src/frontEnd/pathmagic.py, its parent is 'src/frontEnd', and its grandparent is 'src'
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.abspath(os.path.join(current_dir, '..'))

if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# Also add the project root directory to sys.path
root_dir = os.path.abspath(os.path.join(src_dir, '..'))
if root_dir not in sys.path:
    sys.path.append(root_dir)
