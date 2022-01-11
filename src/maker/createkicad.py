# =========================================================================
#             FILE: createkicad.py
#
#            USAGE: ---
#
#      DESCRIPTION: This define all components of to create the Kicad Library.
#
#          OPTIONS: ---
#     REQUIREMENTS: ---
#             BUGS: ---
#            NOTES: ---
#           AUTHOR: Sumanto Kar, jeetsumanto123@gmail.com, FOSSEE, IIT Bombay
# ACKNOWLEDGEMENTS: Rahul Paknikar, rahulp@iitb.ac.in, FOSSEE, IIT Bombay
#                Digvjay Singh, digvijay.singh@iitb.ac.in, FOSSEE, IIT Bombay
#                Prof. Maheswari R., VIT Chennai
#     GUIDED BY: Steve Hoover, Founder Redwood EDA
#  ORGANIZATION: eSim Team at FOSSEE, IIT Bombay
#       CREATED: Monday 29, November 2021
#      REVISION: Monday 29, November 2021
# =========================================================================

# importing the files and libraries
from . import Appconfig
import re
import os
import sys
import xml.etree.cElementTree as ET
from PyQt5 import QtWidgets

# beginning the AutoSchematic Class


class AutoSchematic:

    # initialising the variables here
    def init(self, modelname, modelpath):
        self.App_obj = Appconfig.Appconfig()
        self.modelname = modelname.split('.')[0]
        self.template = self.App_obj.kicad_lib_template.copy()
        self.xml_loc = self.App_obj.xml_loc
        self.lib_loc = self.App_obj.lib_loc
        self.modelpath = modelpath
        if os.name == 'nt':
            eSim_src = Appconfig.src_home
            inst_dir = eSim_src.replace('\\eSim', '')
            self.kicad_ngveri_lib = \
                inst_dir + '/KiCad/share/kicad/library/eSim_Ngveri.lib'
        else:
            self.kicad_ngveri_lib = '/usr/share/kicad/library/eSim_Ngveri.lib'
        # self.parser = self.App_obj.parser_ngveri

    # creating KiCAD library using this function
    def createkicad(self):

        xmlFound = None
        # read_file = open(self.modelpath+'connection_info.txt', 'r')
        # data = read_file.readlines()
        # print(data)
        xmlFound = None
        for root, dirs, files in os.walk(self.xml_loc):
            if (str(self.modelname) + '.xml') in files:
                xmlFound = root
                print(xmlFound)
        if xmlFound is None:
            self.getPortInformation()
            self.createXML()
            self.createLib()
        elif (xmlFound == os.path.join(self.xml_loc, 'Ngveri')):
            print('Library already exists...')
            ret = QtWidgets.QMessageBox.warning(
                None, "Warning", '''<b>Library files for this model''' +
                ''' already exist. Do you want to overwrite it?</b><br/>
                If yes press ok, else cancel it and ''' +
                '''change the name of your vhdl file.''',
                QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Cancel
            )
            if ret == QtWidgets.QMessageBox.Ok:
                print("Overwriting existing libraries")
                self.getPortInformation()
                self.createXML()
                self.removeOldLibrary()     # Removes the exisitng library
                self.createLib()
            else:
                print("Library Creation Cancelled")
                return "Error"

        else:
            print('Pre existing library...')
            ret = QtWidgets.QMessageBox.critical(
                self.parent, "Error", '''<b>A standard library already ''' +
                '''exists with this name.</b><br/><b>Please change the ''' +
                '''name of your vhdl file and upload it again</b>''',
                QtWidgets.QMessageBox.Ok
            )

    # getting the port information here

    def getPortInformation(self):
        portInformation = PortInfo(self, self.modelpath)
        portInformation.getPortInfo()
        self.portInfo = portInformation.bit_list
        self.input_length = portInformation.input_len
        self.portName = portInformation.port_name

    # creating the XML files in eSim-2.1/library/modelParamXML/Ngveri
    def createXML(self):
        cwd = os.getcwd()
        xmlDestination = os.path.join(self.xml_loc, 'Ngveri')
        self.splitText = ""
        for bit in self.portInfo[:-1]:
            self.splitText += bit + "-V:"
        self.splitText += self.portInfo[-1] + "-V"

        print("changing directory to ", xmlDestination)
        os.chdir(xmlDestination)

        root = ET.Element("model")
        ET.SubElement(root, "name").text = self.modelname
        ET.SubElement(root, "type").text = "Ngveri"
        ET.SubElement(root, "node_number").text = str(len(self.portInfo))
        ET.SubElement(root, "title").text = (
            "Add parameters for " + str(self.modelname))
        ET.SubElement(root, "split").text = self.splitText
        param = ET.SubElement(root, "param")
        ET.SubElement(param, "rise_delay", default="1.0e-9").text = (
            "Enter Rise Delay (default=1.0e-9)")
        ET.SubElement(param, "fall_delay", default="1.0e-9").text = (
            "Enter Fall Delay (default=1.0e-9)")
        ET.SubElement(param, "input_load", default="1.0e-12").text = (
            "Enter Input Load (default=1.0e-12)")
        ET.SubElement(param, "instance_id", default="1").text = (
            "Enter Instance ID (Between 0-99)")

        tree = ET.ElementTree(root)
        tree.write(str(self.modelname) + '.xml')
        print("Leaving the directory ", xmlDestination)
        os.chdir(cwd)

    # Calculates the maximum between input and output ports
    def findBlockSize(self):
        ind = self.input_length
        return max(
            self.char_sum(self.portInfo[:ind]),
            self.char_sum(self.portInfo[ind:])
        )

    def char_sum(self, ls):
        return sum([int(x) for x in ls])

    # removing the old library
    def removeOldLibrary(self):
        cwd = os.getcwd()
        os.chdir(self.lib_loc)
        print("Changing directory to ", self.lib_loc)
        f = open(self.kicad_ngveri_lib)
        lines = f.readlines()
        f.close()

        output = []
        line_reading_flag = False

        for line in lines:
            if line.startswith("DEF"):
                if line.split()[1] == self.modelname:
                    line_reading_flag = True
            if not line_reading_flag:
                output.append(line)
            if line.startswith("ENDDEF"):
                line_reading_flag = False

        f = open(self.kicad_ngveri_lib, 'w')
        for line in output:
            f.write(line)

        os.chdir(cwd)
        print("Leaving directory, ", self.lib_loc)

    # creating the library
    def createLib(self):
        self.dist_port = 100         # Distance between two ports
        self.inc_size = 100          # Increment size of a block
        cwd = os.getcwd()
        os.chdir(self.lib_loc)
        print("Changing directory to ", self.lib_loc)

        lib_file = open(self.kicad_ngveri_lib, "a")
        line1 = self.template["start_def"]
        line1 = line1.split()
        line1 = [w.replace('comp_name', self.modelname) for w in line1]
        self.template["start_def"] = ' '.join(line1)
        if os.stat(self.kicad_ngveri_lib).st_size == 0:
            lib_file.write("EESchema-LIBRARY Version 2.3" + "\n\n")
        # lib_file.write("#encoding utf-8"+ "\n"+ "#"+ "\n" +
        # "#test_compo" + "\n"+ "#"+ "\n")
        lib_file.write(
            self.template["start_def"] + "\n" + self.template["U_field"] + "\n"
        )

        line3 = self.template["comp_name_field"]
        line3 = line3.split()
        line3 = [w.replace('comp_name', self.modelname) for w in line3]
        self.template["comp_name_field"] = ' '.join(line3)

        lib_file.write(self.template["comp_name_field"] + "\n")

        line4 = self.template["blank_field"]
        line4_1 = line4[0]
        line4_2 = line4[1]
        line4_1 = line4_1.split()
        line4_1 = [w.replace('blank_quotes', '""') for w in line4_1]
        line4_2 = line4_2.split()
        line4_2 = [w.replace('blank_quotes', '""') for w in line4_2]
        line4[0] = ' '.join(line4_1)
        line4[1] = ' '.join(line4_2)
        self.template["blank_qoutes"] = line4

        lib_file.write(
            line4[0] + "\n" + line4[1] + "\n" +
            self.template["start_draw"] + "\n"
        )

        draw_pos = self.template["draw_pos"]
        draw_pos = draw_pos.split()
        draw_pos[4] = str(
            int(draw_pos[4]) - self.findBlockSize() * self.inc_size)
        self.template["draw_pos"] = ' '.join(draw_pos)

        lib_file.write(self.template["draw_pos"] + "\n")

        input_port = self.template["input_port"]
        input_port = input_port.split()
        output_port = self.template["output_port"]
        output_port = output_port.split()
        inputs = self.portInfo[0: self.input_length]
        outputs = self.portInfo[self.input_length:]
        inputName = []
        outputName = []

        for i in range(self.input_length):
            for j in range(int(inputs[i])):
                inputName.append(
                    self.portName[i] + str(int(inputs[i]) - j - 1))

        for i in range(self.input_length, len(self.portName)):
            for j in range(int(outputs[i - self.input_length])):
                outputName.append(
                    self.portName[i] +
                    str(int(outputs[i - self.input_length]) - j - 1))

        # print("INPUTS AND OUTPUTS ")
        # print("INPUTS:"+inputName)
        # print("OUTPUTS:"outputName)
        # print(inputs)
        # print(outputs)

        inputs = self.char_sum(inputs)
        outputs = self.char_sum(outputs)

        total = inputs + outputs

        port_list = []
        j = 0
        k = 0
        for i in range(total):
            if (i < inputs):
                input_port[1] = inputName[i]
                input_port[2] = str(i + 1)
                input_port[4] = str(int(input_port[4]) - self.dist_port)
                input_list = ' '.join(input_port)
                port_list.append(input_list)
                j = j + 1

            else:
                output_port[1] = outputName[i - inputs]
                output_port[2] = str(i + 1)
                output_port[4] = str(int(output_port[4]) - self.dist_port)
                output_list = ' '.join(output_port)
                port_list.append(output_list)

        for ports in port_list:
            lib_file.write(ports + "\n")
        lib_file.write(
            self.template["end_draw"] + "\n" +
            self.template["end_def"] + "\n\n\n"
        )

        os.chdir(cwd)


# beginning the PortInfo Class containing Port Information
class PortInfo:

    # initialising the variables
    def __init__(self, model, modelpath):
        self.modelname = model.modelname
        # self.model_loc = model.parser.get('NGVERI', 'DIGITAL_MODEL')
        self.bit_list = []
        self.port_name = []
        self.input_len = 0
        self.modelpath = modelpath

    # getting the port information from connection_info.txt
    def getPortInfo(self):
        input_list = []
        output_list = []
        read_file = open(self.modelpath + 'connection_info.txt', 'r')
        data = read_file.readlines()
        # print(data)
        read_file.close()

        for line in data:
            if re.match(r'^\s*$', line):
                pass
            else:
                in_items = re.findall(
                    "INPUT", line, re.MULTILINE | re.IGNORECASE
                )
                inout_items = re.findall(
                    "INOUT", line, re.MULTILINE | re.IGNORECASE
                )

                out_items = re.findall(
                    "OUTPUT", line, re.MULTILINE | re.IGNORECASE
                )
            if in_items:
                input_list.append(line.split())
            if inout_items:
                input_list.append(line.split())
            if out_items:
                output_list.append(line.split())
        # print(input_list)
        # print(output_list)
        for in_list in input_list:
            self.bit_list.append(in_list[2])
            self.port_name.append(in_list[0])
        self.input_len = len(self.bit_list)
        for out_list in output_list:
            self.bit_list.append(out_list[2])
            self.port_name.append(out_list[0])
