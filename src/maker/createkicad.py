# ==============================================================================
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
#           AUTHOR: Sumanto Kar, sumantokar@iitb.ac.in, FOSSEE, IIT Bombay
# ACKNOWLEDGEMENTS: Rahul Paknikar, rahulp@iitb.ac.in, FOSSEE, IIT Bombay
#                Digvijay Singh, digvijay.singh@iitb.ac.in, FOSSEE, IIT Bombay
#                Prof. Maheswari R. and Team, VIT Chennai
#     GUIDED BY: Steve Hoover, Founder Redwood EDA
#                Kunal Ghosh, VLSI System Design Corp.Pvt.Ltd
#                Anagha Ghosh, VLSI System Design Corp.Pvt.Ltd
# OTHER CONTRIBUTERS:
#                Prof. Madhuri Kadam, Shree L. R. Tiwari College of Engineering
#                Rohinth Ram, Madras Institue of Technology
#                Charaan S., Madras Institue of Technology
#                Nalinkumar S., Madras Institue of Technology
#                Partha Singha Roy, Kalyani Government Engineering College
#  ORGANIZATION: eSim Team at FOSSEE, IIT Bombay
#       CREATED: Monday 29, November 2021
#      REVISION: Friday 16, June 2023
# ==============================================================================

from . import Appconfig
import re
import os
import xml.etree.cElementTree as ET
from PyQt5 import QtWidgets


class AutoSchematic:
    def init(self, modelname, modelpath):
        self.App_obj = Appconfig.Appconfig()
        self.modelname = modelname.split('.')[0]
        self.template = self.App_obj.kicad_sym_template.copy()
        self.xml_loc = self.App_obj.xml_loc
        self.lib_loc = self.App_obj.lib_loc
        self.modelpath = modelpath
        if os.name == 'nt':
            eSim_src = self.App_obj.src_home
            inst_dir = eSim_src.replace('\\eSim', '')
            self.kicad_ngveri_sym = \
                inst_dir + '/KiCad/share/kicad/symbols/eSim_Ngveri.kicad_sym'
        else:
            self.kicad_ngveri_sym = \
                '/usr/share/kicad/symbols/eSim_Ngveri.kicad_sym'
        # self.parser = self.App_obj.parser_ngveri

    def createKicadSymbol(self):
        '''
            creating KiCad library using this function
        '''
        xmlFound = None
        for root, dirs, files in os.walk(self.xml_loc):
            if (str(self.modelname) + '.xml') in files:
                xmlFound = root
                print(xmlFound)
                break

        if xmlFound is None:
            self.getPortInformation()
            self.createXML()
            self.createSym()

        elif (xmlFound == os.path.join(self.xml_loc, 'Ngveri')):
            print('Library already exists...')
            ret = QtWidgets.QMessageBox.warning(
                None, "Warning", '''<b>Library files for this model''' +
                ''' already exist. Do you want to overwrite it?</b><br/>
                If yes press ok, else cancel it and ''' +
                '''change the name of your verilog model.''',
                QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Cancel
            )

            if ret == QtWidgets.QMessageBox.Ok:
                print("Overwriting existing libraries")
                self.getPortInformation()
                self.createXML()
                self.removeOldLibrary()     # Removes the existing library
                self.createSym()
            else:
                print("Library Creation Cancelled")
                return "Error"

        else:
            print('Pre-existing library...')
            ret = QtWidgets.QMessageBox.critical(
                self.parent, "Error", '''<b>A standard library already ''' +
                '''exists with this name.</b><br/><b>Please change the ''' +
                '''name of your verilog model and add it again.</b>''',
                QtWidgets.QMessageBox.Ok
            )

    def getPortInformation(self):
        '''
            getting the port information here
        '''
        portInformation = PortInfo(self, self.modelpath)
        portInformation.getPortInfo()
        self.portInfo = portInformation.bit_list
        self.input_length = portInformation.input_len
        self.portName = portInformation.port_name

    def createXML(self):
        '''
            creating the XML files at `library/modelParamXML/Ngveri`
        '''
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

    def findBlockSize(self):
        '''
            Calculates the maximum between input and output ports
        '''
        ind = self.input_length
        return max(
            self.char_sum(self.portInfo[:ind]),
            self.char_sum(self.portInfo[ind:])
        )

    def char_sum(self, ls):
        return sum([int(x) for x in ls])

    def removeOldLibrary(self):
        '''
            removing the old library
        '''
        cwd = os.getcwd()
        os.chdir(self.lib_loc)
        print("Changing directory to ", self.lib_loc)
        sym_file = open(self.kicad_ngveri_sym)
        lines = sym_file.readlines()
        sym_file.close()
        lines = lines[0:-2]
        output = []
        line_reading_flag = False

        for line in lines:
            if line.startswith("(symbol"):    # Eeschema Template start
                if line.split()[1] == f"\"{self.modelname}\"":
                    line_reading_flag = True
            if not line_reading_flag:
                output.append(line)
            if line.startswith("))"):        # Eeschema Template end
                line_reading_flag = False

        sym_file = open(self.kicad_ngveri_sym, 'w')
        for line in output:
            sym_file.write(line)

        os.chdir(cwd)
        print("Leaving directory, ", self.lib_loc)

    def createSym(self):
        '''
            creating the symbol
        '''
        self.dist_port = 2.54         # Distance between two ports (mil)
        self.inc_size = 2.54          # Increment size of a block (mil)
        cwd = os.getcwd()
        os.chdir(self.lib_loc)
        print("Changing directory to ", self.lib_loc)

        # Removing ")" from "eSim_Ngveri.kicad_sym"
        file = open(self.kicad_ngveri_sym, "r")
        content_file = file.read()
        new_content_file = content_file[:-2]
        file.close()
        file = open(self.kicad_ngveri_sym, "w")
        file.write(new_content_file)
        file.close()

        # Appending new schematic block
        sym_file = open(self.kicad_ngveri_sym, "a")
        line1 = self.template["start_def"]
        line1 = line1.split()
        line1 = [w.replace('comp_name', self.modelname) for w in line1]
        self.template["start_def"] = ' '.join(line1)

        if os.stat(self.kicad_ngveri_sym).st_size == 0:
            sym_file.write(
                "(kicad_symbol_lib (version 20211014) " +
                "(generator kicad_symbol_editor)" +
                "\n\n"
            )                       # Eeschema starter code

        # sym_file.write("#encoding utf-8"+ "\n"+ "#"+ "\n" +
        # "#test_compo" + "\n"+ "#"+ "\n")
        sym_file.write(
            self.template["start_def"] + "\n" + self.template["U_field"] + "\n"
        )

        line3 = self.template["comp_name_field"]
        line3 = line3.split()
        line3 = [w.replace('comp_name', self.modelname) for w in line3]
        self.template["comp_name_field"] = ' '.join(line3)

        sym_file.write(self.template["comp_name_field"] + "\n")

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

        sym_file.write(line4[0] + "\n" + line4[1] + "\n")

        draw_pos = self.template["draw_pos"]
        draw_pos = draw_pos.split()

        draw_pos = \
            [w.replace('comp_name', f"{self.modelname}_0_1") for w in draw_pos]
        draw_pos[8] = str(float(draw_pos[8]) +           # previously it is (-)
                          float(self.findBlockSize() * self.inc_size))
        draw_pos_rec = draw_pos[8]

        self.template["draw_pos"] = ' '.join(draw_pos)

        sym_file.write(
            self.template["draw_pos"] + "\n" + self.template["start_draw"] +
            " \"" + f"{self.modelname}_1_1\"" + "\n"
        )

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

        inputs = self.char_sum(inputs)
        outputs = self.char_sum(outputs)

        total = inputs + outputs

        port_list = []

        # Set input & output port
        input_port[4] = draw_pos_rec
        output_port[4] = draw_pos_rec

        j = 0
        for i in range(total):
            if (i < inputs):
                input_port[9] = f"\"{inputName[i]}\""
                input_port[13] = f"\"{str(i + 1)}\""
                input_port[4] = \
                    str(float(input_port[4]) - float(self.dist_port))
                input_list = ' '.join(input_port)
                port_list.append(input_list)
                j = j + 1

            else:
                output_port[9] = f"\"{outputName[i - inputs]}\""
                output_port[13] = f"\"{str(i + 1)}\""
                output_port[4] = \
                    str(float(output_port[4]) - float(self.dist_port))
                output_list = ' '.join(output_port)
                port_list.append(output_list)

        for ports in port_list:
            sym_file.write(ports + "\n")
        sym_file.write(
            self.template["end_draw"] + "\n\n\n"+")"
        )
        sym_file.close()
        os.chdir(cwd)


class PortInfo:
    '''
        The class contains port information
    '''
    def __init__(self, model, modelpath):
        self.modelname = model.modelname
        self.bit_list = []
        self.port_name = []
        self.input_len = 0
        self.modelpath = modelpath

    def getPortInfo(self):
        '''
            getting the port information from `connection_info.txt`
        '''
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

        for in_list in input_list:
            self.bit_list.append(in_list[2])
            self.port_name.append(in_list[0])
        self.input_len = len(self.bit_list)
        for out_list in output_list:
            self.bit_list.append(out_list[2])
            self.port_name.append(out_list[0])
