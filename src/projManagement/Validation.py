
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
#  ORGANIZATION: eSim team at FOSSEE, IIT Bombay.
#       CREATED: Wednesday 12 February 2015 
#      REVISION:  ---
#===============================================================================
import os
import re 


class Validation:
    """
    This is Validation class use for validating Project.
    e.g if .proj is present in project directory
    or if new project name is already exist in workspace etc
    """
    def __init__(self):
        pass
    
    def validateOpenproj(self,projDir):
        """
        This function validate Open Project Information.
        """
        print "Validating Open Project Information"
        projName = os.path.basename(str(projDir))
        lookProj = os.path.join(str(projDir),projName+".proj")
        #Check existence of project
        if os.path.exists(lookProj):
            return True
        else:
            return False
       
        
    
    def validateNewproj(self,projDir):
        """This Project Validate New Project Information
        """
        print "Validating New Project Information"
        #print "Project Directory : ",projDir
        #Checking existence of project with same name
        
        if os.path.exists(projDir):
            return "CHECKEXIST" #Project with name already exist
        else:
            #Check Proper name for project. It should not have space
            if re.search(r"\s",projDir ):
                return "CHECKNAME"
            else:
                return "VALID"
            
    def validateKicad(self,projDir):
        """
        This function validate if Kicad components are present
        """
        print "Validation for Kicad components"
        if projDir == None:
            return False
        else:
            return True
        
    def validateCir(self,projDir):
        """
        This function checks if ".cir" file is present.
        """
        #print "Checking if .cir file is present or not"
        projName = os.path.basename(str(projDir))
        lookCir = os.path.join(str(projDir),projName+".cir")
        #Check existence of project
        if os.path.exists(lookCir):
            return True
        else:
            return False
        
        


    