
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
    
    def validateOpenproj(self,proj_directory):
        print "Validate openProj called"
        projName = os.path.basename(str(proj_directory))
        lookProj = os.path.join(str(proj_directory),projName+".proj")
        #Check existence of project
        if os.path.exists(lookProj):
            return True
        else:
            return False
        
       
        
    
    def validateNewproj(self,project_dir):
        print "Validate newProj called"
        print "Project Directory : ",project_dir
        #Checking existence of project with same name
        
        if os.path.exists(project_dir):
            return "CHECKEXIST" #Project with name already exist
        else:
                                   
            #Check Proper name for project. It should not have space
            
            if re.search(r"\s",project_dir ):
                return "CHECKNAME"
            else:
                return "VALID"
        
        


    