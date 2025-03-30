# =========================================================================
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
#      MODIFIED: Rahul Paknikar, rahulp@iitb.ac.in
#  ORGANIZATION: eSim team at FOSSEE, IIT Bombay.
#       CREATED: Wednesday 12 February 2015
#      REVISION: Friday 14 February 2020
# =========================================================================

import os
import re
import distutils.spawn


class Validation:
    """
    This is Validation class use for validating Project.
    e.g if .proj is present in project directory
    or if new project name is already exist in workspace etc
    """

    def __init__(self):
        pass

    def validateOpenproj(self, projDir):
        """
        Takes as input the path of the project and checks if
        projName.proj file exists or not

        @params
            :projDir    => contains the path of the project selected to open

        @return
            True        => If the folder contains the projName.proj file
            False       => If the folder doesn't contain projName.proj file
        """
        print("Function: Validating Open Project Information")
        projName = os.path.basename(str(projDir))
        lookProj = os.path.join(str(projDir), projName + ".proj")
        # Check existence of project
        if os.path.exists(lookProj):
            return True
        else:
            return False

    def validateNewproj(self, projDir):
        """
        Validate new project created

        @params
            :projDir        => Contains path of the new projDir created

        @return
            :"CHECKEXIST"   => If smae project name folder exists
            :"CHECKNAME"    => If space is there in name
            :"VALID"        => If valid project name given
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

    def validateKicad(self, projDir):
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
        print("Function : Validating for Kicad components")
        if projDir is None:
            return False
        else:
            return True

    def validateCir(self, projDir):
        """
        Validate if cir file present in the directory with the appropriate .cir
        file name, same as the project directory base

        @params
            :projDir    => the path to the project diretory

        @return
            True
            False
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
        Also, if subckt file is present check for ports and check if equal

        @params
            :subDir    => the path of the subcircuit directory
            :giveNum   => the number of port calculated and passed for\
                validation

        @return
            True
            PORT
            DIREC
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

    def validateSubcir(self, projDir, fileName):
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

        first = True
        last_line = []

        # Checks if file is empty or not.
        if os.stat(projDir).st_size == 0:
            print("File is empty")
            return False

        with open(projDir, 'r') as f:
            for line in f:
                word = line.split()
                if len(word) == 0 or word[0][0] == "*":
                    continue
                if first:
                    if word[0] == ".subckt" and word[1] == fileName:
                        first = False
                    else:
                        print("First line not found:", word)
                        return False
                else:
                    last_line = word

        if first is True:
            print("First line not found")
            return False

        if len(last_line) >= 2 and last_line[0] == ".ends" and \
                last_line[1] == fileName:
            return True

        print("Last line not found:", last_line)
        return False
