from Appconfig import Appconfig
import re
import os
import xml.etree.cElementTree as ET
from PyQt5 import QtWidgets


class AutoSchematic(QtWidgets.QWidget):

    def __init__(self, parent, modelname):
        QtWidgets.QWidget.__init__(self)
        self.parent = parent
        self.modelname = modelname.split('.')[0]
        self.template = Appconfig.kicad_sym_template.copy()
        self.xml_loc = Appconfig.xml_loc
        self.lib_loc = Appconfig.lib_loc
        if os.name == 'nt':
            eSim_src = Appconfig.src_home
            inst_dir = eSim_src.replace('\\eSim', '')
            self.kicad_nghdl_sym = \
                inst_dir + '/KiCad/share/kicad/symbols/eSim_Nghdl.kicad_sym'
        else:
            self.kicad_nghdl_sym = \
                '/usr/share/kicad/symbols/eSim_Nghdl.kicad_sym'
        self.parser = Appconfig.parser_nghdl

    def createKicadSymbol(self):
        xmlFound = None
        for root, dirs, files in os.walk(self.xml_loc):
            if (str(self.modelname) + '.xml') in files:
                xmlFound = root
                print(xmlFound)
        if xmlFound is None:
            self.getPortInformation()
            self.createXML()
            self.createSym()
        elif (xmlFound == os.path.join(self.xml_loc, 'Nghdl')):
            print('Library already exists...')
            ret = QtWidgets.QMessageBox.warning(
                self.parent, "Warning", '''<b>Library files for this model''' +
                ''' already exist. Do you want to overwrite it?</b><br/>
                If yes press ok, else cancel it and ''' +
                '''change the name of your vhdl file.''',
                QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Cancel
            )
            if ret == QtWidgets.QMessageBox.Ok:
                print("Overwriting existing libraries")
                self.getPortInformation()
                self.createXML()
                self.removeOldLibrary()     # Removes the existng library
                self.createSym()
            else:
                print("Exiting Nghdl")
                quit()
        else:
            print('Pre existing library...')
            ret = QtWidgets.QMessageBox.critical(
                self.parent, "Error", '''<b>A standard library already ''' +
                '''exists with this name.</b><br/><b>Please change the ''' +
                '''name of your vhdl file and upload it again.</b>''',
                QtWidgets.QMessageBox.Ok
            )

            # quit()

    def getPortInformation(self):
        '''
            getting the port information here
        '''
        portInformation = PortInfo(self)
        portInformation.getPortInfo()
        self.portInfo = portInformation.bit_list
        self.input_length = portInformation.input_len

    def createXML(self):
        '''
            creating the XML files in eSim /library/modelParamXML/Nghdl
        '''
        cwd = os.getcwd()
        xmlDestination = os.path.join(self.xml_loc, 'Nghdl')
        self.splitText = ""
        for bit in self.portInfo[:-1]:
            self.splitText += bit + "-V:"
        self.splitText += self.portInfo[-1] + "-V"

        print("changing directory to ", xmlDestination)
        os.chdir(xmlDestination)

        root = ET.Element("model")
        ET.SubElement(root, "name").text = self.modelname
        ET.SubElement(root, "type").text = "Nghdl"
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
        sym_file = open(self.kicad_nghdl_sym)
        lines = sym_file.readlines()
        lines = lines[0:-2]
        sym_file.close()

        output = []
        line_reading_flag = False

        for line in lines:
            if line.startswith("(symbol"):      # Eeschema template start
                if line.split()[1] == f"\"{self.modelname}\"":
                    line_reading_flag = True
            if not line_reading_flag:
                output.append(line)
            if line.startswith("))"):           # Eeschema template end
                line_reading_flag = False

        sym_file = open(self.kicad_nghdl_sym, 'w')
        for line in output:
            sym_file.write(line)
        sym_file.close()
        os.chdir(cwd)
        print("Leaving directory, ", self.lib_loc)

    def createSym(self):
        self.dist_port = 2.54         # Distance between two ports (mil)
        self.inc_size = 2.54          # Increment size of a block (mil)
        cwd = os.getcwd()
        os.chdir(self.lib_loc)
        print("Changing directory to ", self.lib_loc)

        # Removing ")" from "eSim_Nghdl.kicad_sym"
        file = open(self.kicad_nghdl_sym, "r")
        content_file = file.read()
        new_content_file = content_file[:-2]
        file.close()
        file = open(self.kicad_nghdl_sym, "w")
        file.write(new_content_file)
        file.close()

        # Appending new schematic block
        sym_file = open(self.kicad_nghdl_sym, "a")
        line1 = self.template["start_def"]
        line1 = line1.split()
        line1 = [w.replace('comp_name', self.modelname) for w in line1]
        self.template["start_def"] = ' '.join(line1)

        if os.stat(self.kicad_nghdl_sym).st_size == 0:
            sym_file.write(
                "(kicad_symbol_lib (version 20211014) " +
                "(generator kicad_symbol_editor)" + "\n\n"
            )  # Eeschema starter code

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
        draw_pos[8] = str(
            float(draw_pos[8]) + float(self.findBlockSize() * self.inc_size)
        )
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

        inputs = self.char_sum(inputs)
        outputs = self.char_sum(outputs)

        total = inputs + outputs

        port_list = []

        # Set input & output port
        input_port[4] = draw_pos_rec
        output_port[4] = draw_pos_rec

        for i in range(total):
            if (i < inputs):
                input_port[9] = f"\"in{str(i + 1)}\""
                input_port[13] = f"\"{str(i + 1)}\""
                input_port[4] = \
                    str(float(input_port[4]) - float(self.dist_port))
                input_list = ' '.join(input_port)
                port_list.append(input_list)

            else:
                output_port[9] = f"\"out{str(i - inputs + 1)}\""
                output_port[13] = f"\"{str(i + 1)}\""
                output_port[4] = \
                    str(float(output_port[4]) - float(self.dist_port))
                output_list = ' '.join(output_port)
                port_list.append(output_list)

        for ports in port_list:
            sym_file.write(ports + "\n")
        sym_file.write(
            self.template["end_draw"] + "\n\n" + ")"
        )
        sym_file.close()
        os.chdir(cwd)

        print('Leaving directory, ', self.lib_loc)
        QtWidgets.QMessageBox.information(
            self.parent, "Symbol Added",
            '''Symbol details for this model is added to the \'''' +
            '''<b>eSim_Nghdl.kicad_sym</b>\' in the KiCad shared directory.''',
            QtWidgets.QMessageBox.Ok
        )


class PortInfo:
    '''
        The class contains port information
    '''
    def __init__(self, model):
        self.modelname = model.modelname
        self.model_loc = os.path.join(
            model.parser.get('NGHDL', 'DIGITAL_MODEL'), 'ghdl'
        )
        self.bit_list = []
        self.input_len = 0

    def getPortInfo(self):
        info_loc = os.path.join(self.model_loc, self.modelname + '/DUTghdl/')
        input_list = []
        output_list = []
        read_file = open(info_loc + 'connection_info.txt', 'r')
        data = read_file.readlines()
        read_file.close()

        for line in data:
            if re.match(r'^\s*$', line):
                pass
            else:
                in_items = re.findall(
                    "IN", line, re.MULTILINE | re.IGNORECASE
                )
                out_items = re.findall(
                    "OUT", line, re.MULTILINE | re.IGNORECASE
                )
            if in_items:
                input_list.append(line.split())
            if out_items:
                output_list.append(line.split())

        for in_list in input_list:
            self.bit_list.append(in_list[2])
        self.input_len = len(self.bit_list)
        for out_list in output_list:
            self.bit_list.append(out_list[2])
