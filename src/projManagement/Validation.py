
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
        tempStr = proj_directory.split('/')
        projName = tempStr[len(tempStr)-1]  
        if os.path.exists(proj_directory+"/"+projName+".proj"):
            return True
        else:
            return False
        
    
    def validateNewproj(self):
        print "Valid new Proj called"


    