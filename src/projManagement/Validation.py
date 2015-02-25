
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
import re 


class Validation:
    def __init__(self):
        pass
    
    def validateOpenproj(self,projDir):
        print "Validate openProj called"
        projName = os.path.basename(str(projDir))
        lookProj = os.path.join(str(projDir),projName+".proj")
        #Check existence of project
        if os.path.exists(lookProj):
            return True
        else:
            return False
        
       
        
    
    def validateNewproj(self,projDir):
        print "Validate newProj called"
        print "Project Directory : ",projDir
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
        print "Validation for Kicad components"
        if projDir == None:
            return False
        else:
            return True
        
        


    