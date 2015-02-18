
#===============================================================================
#
#          FILE: Validation.py
# 
#         USAGE: --- 
# 
#   DESCRIPTION: This module is use to create validation for openProject,newProject and other activity. 
# 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Fahim Khan, fahim.elex@gmail.com
#  ORGANIZATION: ecSim team at FOSSEE, IIT Bombay.
#       CREATED: Wednesday 12 February 2015 
#      REVISION:  ---
#===============================================================================
import os


class Validation:
    def __init__(self):
        pass
    
    def validateOpenproj(self,proj_directory):
        print "Valid open Proj called"
        projName = os.path.basename(str(proj_directory))
        lookProj = os.path.join(str(proj_directory),projName+".proj")
        if os.path.exists(lookProj):
            return True
        else:
            return False
        
    
    def validateNewproj(self):
        print "Valid new Proj called"


    