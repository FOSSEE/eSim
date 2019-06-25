# =========================================================================
#
#          FILE: Validation.py
#
#         USAGE: ---
#
#   DESCRIPTION: This module is use to create validation for openProject,
#                newProject and other activity.
#
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Fahim Khan, fahim.elex@gmail.com
#  ORGANIZATION: eSim team at FOSSEE, IIT Bombay.
#       CREATED: Wednesday 12 February 2015
#      REVISION:  ---
# =========================================================================
import os
import re
import distutils.spawn

"""
This is Validation class use for validating Project.
e.g if .proj is present in project directory
or if new project name is already exist in workspace etc
"""


class Validation:

    """
    Takes as input the path of the project and checks if
    projName.proj file exists
    projName is same as the folder selected

    @params
        :projDir    => contains the path of the project folder selected to open

    @return
        True        => If the folder contains the projName.proj file
        False       => If the folder doesn't contain projName.proj file
    """

    def __init__(self):
        pass

    def validateOpenproj(self, projDir):
        """
        This function validate Open Project Information.
        """
        print("Function: Validating Open Project Information")
        projName = os.path.basename(str(projDir))
        lookProj = os.path.join(str(projDir), projName + ".proj")
        # Check existence of project
        if os.path.exists(lookProj):
            return True
        else:
            return False

    """
    Validate new project created

    @params
        :projDir        => Contains path of the new projDir created

    @return
        :"CHECKEXIST"   => If smae project name folder exists
        :"CHECKNAME"    => If space is there in name
        :"VALID"        => If valid project name given
    """

    def validateNewproj(self, projDir):
        """
        This Project Validate New Project Information
        """
        print("Function: Validating New Project Information")

        # Checking existence of project with same name
        if os.path.exists(projDir):
            return "CHECKEXIST"  # Project with name already exist
        else:
            # Check Proper name for project. It should not have space
            if re.search(r"\s", projDir):
                return "CHECKNAME"
            else:
                return "VALID"

    """
    Validate if projDir is set appropriately in the function calling file
    and if Kicad components are present

    @params
        :projDir    => the path of the project directory, passed from
                       the calling function

    @return
        True
        False
    """

    def validateKicad(self, projDir):
        """
        This function validate if Kicad components are present
        """
        print("FUnction : Validating for Kicad components")
        if projDir is None:
            return False
        else:
            return True

    """
    Validate if cir file present in the directory with the appropriate .cir
    file name, same as the project directory base

    @params
        :projDir    => the path to the project diretory

    @return
        True
        False
    """

    def validateCir(self, projDir):
        """
        This function checks if ".cir" file is present.
        """
        projName = os.path.basename(str(projDir))
        lookCir = os.path.join(str(projDir), projName + ".cir")
        # Check existence of project
        if os.path.exists(lookCir):
            return True
        else:
            return False

    def validateSub(self, subDir, givenNum):
        """
        This function checks if ".sub" file is present.
        """
        subName = os.path.basename(str(subDir))
        lookSub = os.path.join(str(subDir), subName + ".sub")
        # Check existence of project
        if os.path.exists(lookSub):
            f = open(lookSub)
            data = f.read()
            f.close()
            netlist = data.splitlines()
            for eachline in netlist:
                eachline = eachline.strip()
                if len(eachline) < 1:
                    continue
                words = eachline.split()
                if words[0] == '.subckt':
                    # The number of ports is specified in this line
                    # eg. '.subckt ua741 6 7 3' has 3 ports (6, 7 and 3).
                    numPorts = len(words) - 2
                    print("Looksub : ", lookSub)
                    print("Given Number of ports : ", givenNum)
                    print("Actual Number of ports :", numPorts)
                    if numPorts != givenNum:
                        return "PORT"
                    else:
                        return "True"
        else:
            return "DIREC"

    def validateCirOut(self, projDir):
        """This function checks if ".cir.out" file is present."""
        projName = os.path.basename(str(projDir))
        lookCirOut = os.path.join(str(projDir), projName + ".cir.out")
        # Check existence of project
        if os.path.exists(lookCirOut):
            return True
        else:
            return False

    def validateTool(self, toolName):
        """This function check if tool is present in the system."""
        return distutils.spawn.find_executable(toolName) is not None

    def validateSubcir(self, projDir):
        """
        This function checks for valid format of .sub file.
            Correct format of file is:
                - File should start with **.subckt <filename>**
                - End with **.ends <filename>**
        Function is passed with the file of path it checks the
        file line by line untill it get .subckt as its first word
        and then check for second word is it <fileName> or not.

        Then it checks for second last line if it is ".ends
        <filename>" it return True if conditions satisfy else
        return False.

        """
        projName = os.path.basename(str(projDir))
        fileName = projName[:-4]
        req_line = ".ends" + " " + str(fileName)
        f = open(projDir, 'r')

        flag1 = False
        flag2 = False

        # Checks if file is empty or not.
        if os.stat(projDir).st_size == 0:
            print("File is empty")
            print("===================")
            return False

        for line in f:
            word = line.split(' ')
            if word[0] == "*":
                continue
            if word[0] == ".subckt":
                word = line.split(' ')
                break

        if word[0] == ".subckt" and word[1] == fileName:
            flag1 = True
        else:
            return False

        with open(projDir, 'r') as m:
            lines = m.read().splitlines()
            last_line = lines[-2]

        if req_line == last_line:
            flag2 = True

        if flag1 is True and flag2 is True:
            return True

        return False
