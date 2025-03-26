import os
import sys

# Setting PYTHONPATH
cwd = os.getcwd()
(setPath, fronEnd) = os.path.split(cwd)
sys.path.append(setPath)
