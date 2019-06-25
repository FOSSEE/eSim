
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
from utils.logger import logger


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
        projName.proj file exists
        projName is same as the folder selected

        @params
            :projDir    => contains the path of the project folder selected\
                to open

        @return
            True        => If the folder contains the projName.proj file
            False       => If the folder doesn't contain projName.proj file
        """
        logger.info("Function: Validating Open Project Information")
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
        logger.info("Function: Validating New Project Information")

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
        logger.info("FUnction : Validating for Kicad components")
        if projDir is None:
            return False
        else:
            return True

    def validateCir(self, projDir):
        """
        Validate if cir file present in the directory with the appropriate .cir
        file name, same as the project directory base

        @params
            :projDir    => the path to the project directory

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
                    logger.info("Looksub : ", lookSub)
                    logger.info("Given Number of ports : ", givenNum)
                    logger.info("Actual Number of ports :", numPorts)
                    if numPorts != givenNum:
                        return "PORT"
                    else:
                        return "True"
        else:
            return "DIREC"

    def validateCirOut(self, projDir):
        """
        This function checks if ".cir.out" file is present.

        @params
            :projDir    => the path of the project directory, passed from
                        the calling function

        @return
            True
            False
        """
        projName = os.path.basename(str(projDir))
        lookCirOut = os.path.join(str(projDir), projName + ".cir.out")
        # Check existence of project
        if os.path.exists(lookCirOut):
            return True
        else:
            return False

    def validateTool(self, toolName):
        """
        This function check if tool is present in the system,
        Example, nghdl, eeschema...
        """
        return distutils.spawn.find_executable(toolName) is not None
