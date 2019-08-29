from Appconfig import Appconfig
import re
import os
import xml.etree.cElementTree as ET
from PyQt4 import QtGui, QtCore


class AutoSchematic(QtGui.QWidget):

    def __init__(self, modelname):
        QtGui.QWidget.__init__(self)
        self.modelname = modelname.split('.')[0]
        self.template = Appconfig.kicad_lib_template
        self.xml_loc = Appconfig.xml_loc
        self.lib_loc = Appconfig.lib_loc
        self.kicad_nghdl_lib = 'eSim_kicad.lib'
        self.parser = Appconfig.parser_nghdl
        
    def createKicadLibrary(self):
        xmlFound = None
        for root, dirs, files in os.walk(self.xml_loc):
            if (str(self.modelname) + '.xml') in files:
                xmlFound = root
                print(xmlFound)
        if (xmlFound == None):
            self.getPortInformation()
            self.createXML()
            self.createLib()
        elif (xmlFound == self.xml_loc + '/Nghdl'):
            print 'Library already exists...'
            ret = QtGui.QMessageBox.critical(self, "Critical",'''<b>The Libraries of this model already exist.Do you want to overwrite it?</b><br/>
                    <b>If yes press ok else cancel it and change the name of your vhdl file</b>''', QtGui.QMessageBox.Ok, QtGui.QMessageBox.Cancel)
            if ret == QtGui.QMessageBox.Ok:
                print "Overwriting existing libraries"
                self.getPortInformation()
                self.createXML()
                self.removeOldLibrary()     #Removes the exisitng library
                self.createLib()
            else:
                print "Exiting Nghdl"
                quit()
        else:
            print 'Pre existing library...'
            ret = QtGui.QMessageBox.critical(self, "Error",'''<b>A standard library already exists in this name.</b><br/>
                    <b>Please change the name of your vhdl file and upload it again</b>''', QtGui.QMessageBox.Ok)

            # quit()

    def getPortInformation(self):
        portInformation = PortInfo(self)
        portInformation.getPortInfo()
        self.portInfo = portInformation.bit_list
        self.input_length = portInformation.input_len

    def createXML(self):
        cwd = os.getcwd()
        xmlDestination = os.path.join(self.xml_loc, 'Nghdl')
        self.splitText = ""
        for bit in self.portInfo[:-1]:
            self.splitText += bit + "-V:"
        self.splitText += self.portInfo[-1] + "-V"

        print "changing directory to ", (xmlDestination)
        os.chdir(xmlDestination)

        root = ET.Element("model")
        ET.SubElement(root, "name").text = self.modelname
        ET.SubElement(root, "type").text = "Nghdl"
        ET.SubElement(root, "node_number").text = str(len(self.portInfo))
        ET.SubElement(root, "title").text = "Add parameters for " + str(self.modelname)
        ET.SubElement(root, "split").text = self.splitText
        param = ET.SubElement(root, "param")
        ET.SubElement(param, "rise_delay", default = "1.0e-9").text = "Enter Rise Delay (default=1.0e-9)"
        ET.SubElement(param ,"fall_delay", default ="1.0e-9").text = "Enter Fall Delay (default=1.0e-9)"
        ET.SubElement(param ,"input_load", default ="1.0e-12").text = "Enter Input Load (default=1.0e-12)"
        ET.SubElement(param ,"instance_id", default ="1").text = "Enter Instance ID (Between 0-99)"
        ET.SubElement(param ,"stop_time", default ="90e-9").text = "Enter the stop time to end the simulation (default=90e-9)"
        tree = ET.ElementTree(root)
        tree.write(str(self.modelname) + '.xml')
        print "Leaving the directory ", (xmlDestination)
        os.chdir(cwd)

    #Calculates the maximum between input and output ports
    def findBlockSize(self):
        ind = self.input_length
        return max(self.char_sum(self.portInfo[:ind]), self.char_sum(self.portInfo[ind:]))

    def char_sum(self, ls):
        return sum([int(x) for x in ls])

    def removeOldLibrary(self):
        cwd = os.getcwd()
        os.chdir(self.lib_loc)
        print "Changing directory to ", self.lib_loc
        f = open(self.kicad_nghdl_lib)
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

        f = open(self.kicad_nghdl_lib, 'w')
        for line in output:
            f.write(line)

        os.chdir(cwd)
        print "Leaving directory, ", self.lib_loc

    def createLib(self):
        self.dist_port = 100         #distance between two ports
        self.inc_size = 100          #Increment size of a block
        cwd = os.getcwd()
        os.chdir(self.lib_loc)
        print "Changing directory to ", self.lib_loc

        lib_file = open(self.kicad_nghdl_lib,"a")
        line1 = self.template["start_def"]
        line1 = line1.split()
        line1 = [w.replace('comp_name', self.modelname) for w in line1]
        self.template["start_def"] = ' '.join(line1)
        if os.stat(self.kicad_nghdl_lib).st_size == 0:
            lib_file.write("EESchema-LIBRARY Version 2.3"+ "\n\n")
        #lib_file.write("#encoding utf-8"+ "\n"+ "#"+ "\n" + "#test_compo" + "\n"+ "#"+ "\n")
        lib_file.write(self.template["start_def"]+ "\n"+self.template["U_field"]+"\n")

        line3 = self.template["comp_name_field"]
        line3 = line3.split()
        line3 = [w.replace('comp_name', self.modelname) for w in line3]
        self.template["comp_name_field"] = ' '.join(line3)

        lib_file.write(self.template["comp_name_field"]+ "\n")

        line4 = self.template["blank_field"]
        line4_1 = line4[0]
        line4_2 = line4[1]
        line4_1 = line4_1.split()
        line4_1 = [w.replace('blank_quotes','""') for w in line4_1]
        line4_2 = line4_2.split()
        line4_2 = [w.replace('blank_quotes','""') for w in line4_2]
        line4[0] = ' '.join(line4_1)
        line4[1] = ' '.join(line4_2)
        self.template["blank_qoutes"] = line4

        lib_file.write(line4[0]+"\n" + line4[1]+"\n"+ self.template["start_draw"]+ "\n")

        draw_pos = self.template["draw_pos"]
        draw_pos = draw_pos.split()
        draw_pos[4] = str(int(draw_pos[4])- self.findBlockSize() * self.inc_size)
        self.template["draw_pos"] = ' '.join(draw_pos)

        lib_file.write(self.template["draw_pos"]+"\n")

        input_port = self.template["input_port"]
        input_port = input_port.split()
        output_port = self.template["output_port"]
        output_port = output_port.split()
        inputs = self.portInfo[0: self.input_length]
        outputs = self.portInfo[self.input_length:]

        print "INPUTS AND OUTPUTS "
        print inputs
        print outputs

        inputs = self.char_sum(inputs)
        outputs= self.char_sum(outputs)
 
        total = inputs+outputs

        port_list = []

        for i in xrange(total):
            if (i < inputs):
                input_port[1] = "in"+str(i+1)
                input_port[2] = str(i+1)
                input_port[4] = str(int(input_port[4])-self.dist_port)
                input_list = ' '.join(input_port)
                port_list.append(input_list)

            else:
                output_port[1] = "out"+str(i- inputs+1)
                output_port[2] = str(i+1)
                output_port[4] = str(int(output_port[4])-self.dist_port)
                output_list = ' '.join(output_port)
                port_list.append(output_list)

        for ports in port_list:
                lib_file.write(ports+"\n")
        lib_file.write(self.template["end_draw"]+"\n"+ self.template["end_def"] + "\n\n\n")

        os.chdir(cwd)
        print 'Leaving directory, ', self.lib_loc
        QtGui.QMessageBox.information(self, "Library added", '''Library details for this model is added to the <b>eSim-kicad.lib</b> in the home directory''', QtGui.QMessageBox.Ok)


class PortInfo:
    def __init__(self, model):
        self.modelname = model.modelname
        self.model_loc = model.parser.get('NGSPICE', 'DIGITAL_MODEL')
        self.bit_list = []
        self.input_len = 0

    def getPortInfo(self):
        info_loc = os.path.join(self.model_loc, self.modelname+'/DUTghdl/')
        input_list = []
        output_list = []
        read_file=open(info_loc + 'connection_info.txt','r')
        data=read_file.readlines()
        read_file.close()

        for line in data:
            if re.match(r'^\s*$', line):
                pass
            else:
                in_items=re.findall("IN",line,re.MULTILINE|re.IGNORECASE)
                out_items=re.findall("OUT",line,re.MULTILINE|re.IGNORECASE)
            if in_items:
                input_list.append(line.split())
            if out_items:
                output_list.append(line.split())

        for in_list in input_list:
            self.bit_list.append(in_list[2])
        self.input_len = len(self.bit_list)
        for out_list in output_list:
            self.bit_list.append(out_list[2])


