import os
import shutil
from xml.etree import ElementTree as ET

from PyQt5 import QtWidgets

from . import TrackWidget


class Convert:
    """
    - This class has all the necessary function required to convert \
      kicad netlist to ngspice netlist.
    - Method List
        - addDeviceLibrary
        - addModelParameter
        - addSourceParameter
        - addSubcircuit
        - analysisInsertor
        - converttosciform
        - defaultvalue
    """

    def __init__(self, sourcelisttrack, source_entry_var,
                 schematicInfo, clarg1):
        self.sourcelisttrack = sourcelisttrack
        self.schematicInfo = schematicInfo
        self.entry_var = source_entry_var
        self.sourcelistvalue = []
        self.clarg1 = clarg1

    def addSourceParameter(self):
        """
        - This function extracts the source details to schematicInfo
        - keywords recognised and parsed -
            - sine
            - pulse
            - pwl
            - ac
            - dc
            - exp
        - Return updated schematic
        """

        self.start = 0
        self.end = 0

        for compline in self.sourcelisttrack:
            self.index = compline[0]
            self.addline = self.schematicInfo[self.index]
            if compline[1] == 'sine':
                try:
                    self.start = compline[2]
                    self.end = compline[3]
                    vo_val = str(self.entry_var[self.start].text()) if len(
                        str(self.entry_var[self.start].text())) > 0 else '0'
                    va_val = str(
                        self.entry_var[self.start + 1].text()
                    ) if len(
                        str(self.entry_var[self.start + 1].text())) \
                        > 0 else '0'
                    freq_val = str(self.entry_var[self.start + 2].text()) \
                        if len(
                        str(self.entry_var[self.start + 2].text())) > \
                        0 else '0'
                    td_val = str(self.entry_var[self.start + 3].text()) if len(
                        str(self.entry_var[self.start + 3].text())) > \
                        0 else '0'
                    theta_val = str(self.entry_var[self.end].text()) if len(
                        str(self.entry_var[self.end].text())) > 0 else '0'
                    self.addline = self.addline.partition(
                        '(')[0] + "(" + vo_val + " " + va_val + " " + \
                        freq_val + " " + td_val + " " + theta_val + ")"
                    self.sourcelistvalue.append([self.index, self.addline])
                except BaseException:
                    print(
                        "Caught an exception in sine voltage source ",
                        self.addline)

            elif compline[1] == 'pulse':
                try:
                    self.start = compline[2]
                    self.end = compline[3]
                    v1_val = str(self.entry_var[self.start].text()) if len(
                        str(self.entry_var[self.start].text())) > 0 else '0'
                    v2_val = str(self.entry_var[self.start + 1].text()) if len(
                        str(self.entry_var[self.start + 1].text())) > \
                        0 else '0'
                    td_val = str(self.entry_var[self.start + 2].text()) \
                        if len(
                        str(self.entry_var[self.start + 2].text())) > \
                        0 else '0'
                    tr_val = str(self.entry_var[self.start + 3].text()) if len(
                        str(self.entry_var[self.start + 3].text())) > \
                        0 else '0'
                    tf_val = str(self.entry_var[self.start + 4].text()) if len(
                        str(self.entry_var[self.start + 4].text())) > \
                        0 else '0'
                    pw_val = str(self.entry_var[self.start + 5].text()) if len(
                        str(self.entry_var[self.start + 5].text())) > \
                        0 else '0'
                    tp_val = str(self.entry_var[self.end].text()) if len(
                        str(self.entry_var[self.end].text())) > 0 else '0'

                    self.addline = self.addline.partition(
                        '(')[0] + "(" + v1_val + " " + v2_val + " " + \
                        td_val + " " + tr_val + " " + tf_val + " " + \
                        pw_val + " " + tp_val + ")"
                    self.sourcelistvalue.append([self.index, self.addline])
                except BaseException:
                    print(
                        "Caught an exception in pulse voltage source ",
                        self.addline)

            elif compline[1] == 'pwl':
                try:
                    self.start = compline[2]
                    self.end = compline[3]
                    t_v_val = str(self.entry_var[self.start].text()) if len(
                        str(self.entry_var[self.start].text())) > 0 else '0 0'
                    self.addline = self.addline.partition(
                        '(')[0] + "(" + t_v_val + ")"
                    self.sourcelistvalue.append([self.index, self.addline])
                except BaseException:
                    print(
                        "Caught an exception in pwl voltage source ",
                        self.addline)

            elif compline[1] == 'ac':
                try:
                    self.start = compline[2]
                    self.end = compline[3]
                    va_val = str(self.entry_var[self.start].text()) if len(
                        str(self.entry_var[self.start].text())) > 0 else '0'
                    ph_val = str(self.entry_var[self.start + 1].text()) if len(
                        str(self.entry_var[self.start + 1].text())) > \
                        0 else '0'
                    self.addline = ' '.join(self.addline.split())
                    self.addline = self.addline.partition(
                        'ac')[0] + " " + 'ac' + " " + va_val + " " + ph_val
                    self.sourcelistvalue.append([self.index, self.addline])
                except BaseException:
                    print(
                        "Caught an exception in ac voltage source ",
                        self.addline)

            elif compline[1] == 'dc':
                try:
                    self.start = compline[2]
                    self.end = compline[3]
                    v1_val = str(self.entry_var[self.start].text()) if len(
                        str(self.entry_var[self.start].text())) > 0 else '0'
                    self.addline = ' '.join(self.addline.split())
                    self.addline = self.addline.partition(
                        'dc')[0] + " " + 'dc' + " " + v1_val
                    self.sourcelistvalue.append([self.index, self.addline])
                except BaseException:
                    print(
                        "Caught an exception in dc voltage source",
                        self.addline)

            elif compline[1] == 'exp':
                try:
                    self.start = compline[2]
                    self.end = compline[3]
                    v1_val = str(self.entry_var[self.start].text()) if len(
                        str(self.entry_var[self.start].text())) > 0 else '0'
                    v2_val = str(self.entry_var[self.start + 1].text()) if len(
                        str(self.entry_var[self.start + 1].text())) > \
                        0 else '0'
                    td1_val = str(self.entry_var[self.start + 2].text()) \
                        if len(
                        str(self.entry_var[self.start + 2].text())) > \
                        0 else '0'
                    tau1_val = str(self.entry_var[self.start + 3].text()) \
                        if len(
                        str(self.entry_var[self.start + 3].text())) > \
                        0 else '0'
                    td2_val = str(self.entry_var[self.start + 4].text()) \
                        if len(
                        str(self.entry_var[self.start + 4].text())) > \
                        0 else '0'
                    tau2_val = str(self.entry_var[self.end].text()) if len(
                        str(self.entry_var[self.end].text())) > 0 else '0'

                    self.addline = self.addline.partition(
                        '(')[0] + "(" + v1_val + " " + v2_val + " " + \
                        td1_val + " " + tau1_val + " " + td2_val + \
                        " " + tau2_val + ")"
                    self.sourcelistvalue.append([self.index, self.addline])
                except BaseException:
                    print(
                        "Caught an exception in exp voltage source ",
                        self.addline)

        # Updating Schematic with source value
        for item in self.sourcelistvalue:
            del self.schematicInfo[item[0]]
            self.schematicInfo.insert(item[0], item[1])

        return self.schematicInfo

    def analysisInsertor(self, ac_entry_var, dc_entry_var, tran_entry_var,
                         set_checkbox, ac_parameter, dc_parameter,
                         tran_parameter, ac_type, op_check):
        """
        This function creates an analysis file in current project
        """
        self.ac_entry_var = ac_entry_var
        self.dc_entry_var = dc_entry_var
        self.tran_entry_var = tran_entry_var
        self.set_checkbox = set_checkbox
        self.ac_parameter = ac_parameter
        self.dc_parameter = dc_parameter
        self.trans_parameter = tran_parameter
        self.ac_type = ac_type
        self.op_check = op_check
        self.no = 0

        self.variable = self.set_checkbox
        self.direct = self.clarg1
        (filepath, filemname) = os.path.split(self.direct)
        self.Fileopen = os.path.join(filepath, "analysis")
        print("======================================================")
        print("FILEOPEN CONVERT ANALYS", self.Fileopen)
        self.writefile = open(self.Fileopen, "w")
        if self.variable == 'AC':
            self.no = 0
            self.writefile.write(".ac" +
                                 ' ' +
                                 self.ac_type +
                                 ' ' +
                                 str(self.defaultvalue(
                                     self.ac_entry_var[self.no + 2].text())) +
                                 ' ' +
                                 str(self.defaultvalue(
                                     self.ac_entry_var[self.no].text())) +
                                 self.ac_parameter[self.no] +
                                 ' ' +
                                 str(self.defaultvalue(
                                     self.ac_entry_var[self.no + 1].text())) +
                                 self.ac_parameter[self.no +
                                                   1])

        elif self.variable == 'DC':
            if self.op_check[-1] == 1:
                self.no = 0
                self.writefile.write(".op")
            elif self.op_check[-1] == 0 or self.op_check[-1] == '0':
                self.no = 0
                self.writefile.write(".dc" +
                                     ' ' +
                                     str(self.dc_entry_var[self.no].text()) +
                                     ' ' +
                                     str(self.defaultvalue(
                                         self.dc_entry_var[self.no +
                                                           1].text())) +
                                     self.converttosciform(
                                         self.dc_parameter[self.no]) +
                                     ' ' +
                                     str(self.defaultvalue(
                                         self.dc_entry_var[self.no +
                                                           3].text())) +
                                     self.converttosciform(
                                         self.dc_parameter[self.no +
                                                           2]) +
                                     ' ' +
                                     str(self.defaultvalue(
                                         self.dc_entry_var[self.no +
                                                           2].text())) +
                                     self.converttosciform(
                                         self.dc_parameter[self.no +
                                                           1]))

                if self.dc_entry_var[self.no + 4].text():
                    self.writefile.write(' ' +
                                         str(self.defaultvalue(
                                             self.dc_entry_var[self.no +
                                                               4].text())) +
                                         ' ' +
                                         str(self.defaultvalue(
                                             self.dc_entry_var[self.no +
                                                               5].text())) +
                                         self.converttosciform(
                                             self.dc_parameter[self.no +
                                                               3]) +
                                         ' ' +
                                         str(self.defaultvalue(
                                             self.dc_entry_var[self.no +
                                                               7].text())) +
                                         self.converttosciform(
                                             self.dc_parameter[self.no +
                                                               5]) +
                                         ' ' +
                                         str(self.defaultvalue(
                                             self.dc_entry_var[self.no +
                                                               6].text())) +
                                         self.converttosciform(
                                             self.dc_parameter[self.no +
                                                               4]))

        elif self.variable == 'TRAN':
            self.no = 0
            self.writefile.write(".tran" +
                                 ' ' +
                                 str(self.defaultvalue(
                                     self.tran_entry_var[self.no +
                                                         1].text())) +
                                 self.converttosciform(
                                     self.trans_parameter[self.no +
                                                          1]) +
                                 ' ' +
                                 str(self.defaultvalue(
                                     self.tran_entry_var[self.no +
                                                         2].text())) +
                                 self.converttosciform(
                                     self.trans_parameter[self.no +
                                                          2]) +
                                 ' ' +
                                 str(self.defaultvalue(
                                     self.tran_entry_var[self.no].text())) +
                                 self.converttosciform(
                                     self.trans_parameter[self.no]))

        else:
            pass
        self.writefile.close()

    def converttosciform(self, string_obj):
        """
        This function is used for scientific conversion.
        """
        self.string_obj = string_obj
        if self.string_obj[0] == 'm':
            return "e-03"
        elif self.string_obj[0] == 'u':
            return "e-06"
        elif self.string_obj[0] == 'n':
            return "e-09"
        elif self.string_obj[0] == 'p':
            return "e-12"
        else:
            return "e-00"

    def defaultvalue(self, value):
        """
        This function select default value as 0
        if Analysis widget do not hold any value.
        """
        self.value = value
        if self.value == '':
            return 0
        else:
            return self.value

    def addModelParameter(self, schematicInfo):
        """
        This function adds the Ngspice Model details to schematicInfo
        """

        # Create object of TrackWidget
        self.obj_track = TrackWidget.TrackWidget()

        # List to store model line
        addmodelLine = []
        modelParamValue = []

        for line in self.obj_track.modelTrack:
            # print "Model Track :",line
            if line[2] == 'transfo':
                try:
                    start = line[7]
                    # end = line[8]
                    num_turns = str(
                        self.obj_track.model_entry_var[start + 1].text())

                    if num_turns == "":
                        num_turns = "310"
                    h_array = "H_array = [ "
                    b_array = "B_array = [ "
                    h1 = str(self.obj_track.model_entry_var[start].text())
                    b1 = str(self.obj_track.model_entry_var[start + 5].text())

                    if len(h1) != 0 and len(b1) != 0:
                        h_array = h_array + h1 + " "
                        b_array = b_array + b1 + " "
                        bh_array = h_array + " ] " + b_array + " ]"
                    else:
                        bh_array = "H_array = [-1000 -500 -375 -250 -188 -125 \
                         -63 0 63 125 188 250 375 500 \
                         1000] B_array = [-3.13e-3 -2.63e-3 -2.33e-3 -1.93e-3\
                          -1.5e-3 -6.25e-4 -2.5e-4 0 2.5e-4 6.25e-4 \
                          1.5e-3 1.93e-3 2.33e-3 2.63e-3 3.13e-3]"
                    area = str(
                        self.obj_track.model_entry_var[start + 2].text())
                    length = str(
                        self.obj_track.model_entry_var[start + 3].text())
                    if area == "":
                        area = "1"
                    if length == "":
                        length = "0.01"
                    num_turns2 = str(
                        self.obj_track.model_entry_var[start + 4].text())
                    if num_turns2 == "":
                        num_turns2 = "620"
                    addmodelLine = ".model " + \
                                   line[3] + \
                                   "_primary lcouple (num_turns= " + \
                                   num_turns + ")"
                    modelParamValue.append(
                        [line[0], addmodelLine, "*primary lcouple"])
                    addmodelLine = ".model " + \
                                   line[3] + "_iron_core core (" + bh_array + \
                                   " area = " + area + " length =" + length + \
                                   ")"
                    modelParamValue.append(
                        [line[0], addmodelLine, "*iron core"])
                    addmodelLine = ".model " + \
                                   line[3] + \
                                   "_secondary lcouple (num_turns =" + \
                                   num_turns2 + ")"
                    modelParamValue.append(
                        [line[0], addmodelLine, "*secondary lcouple"])
                except Exception as e:
                    print("Caught an exception in transfo model ", line[1])
                    print("Exception Message : ", str(e))

            elif line[2] == 'ic':
                try:
                    start = line[7]
                    # end = line[8]
                    for key, value in line[9].items():
                        initVal = str(
                            self.obj_track.model_entry_var[value].text())
                        if initVal == "":
                            initVal = "0"
                        # Extracting node from model line
                        node = line[1].split()[1]
                        addmodelLine = ".ic v(" + node + ")=" + initVal
                        modelParamValue.append(
                            [line[0], addmodelLine, line[4]])
                except Exception as e:
                    print("Caught an exception in initial condition ", line[1])
                    print("Exception Message : ", str(e))

            else:
                try:
                    start = line[7]
                    # end = line[8]
                    addmodelLine = ".model " + line[3] + " " + line[2] + "("
                    for key, value in line[9].items():
                        # Checking for default value and accordingly assign
                        # param and default.
                        if ':' in key:
                            key = key.split(':')
                            param = key[0]
                            default = key[1]
                        else:
                            param = key
                            default = 0
                        # Checking if value is iterable.its for vector
                        if (
                                not isinstance(value, str) and
                                hasattr(value, '__iter__')
                        ):
                            addmodelLine += param + "=["
                            for lineVar in value:
                                if str(
                                        self.obj_track.model_entry_var
                                        [lineVar].text()) == "":
                                    paramVal = default
                                else:
                                    paramVal = str(
                                        self.obj_track.model_entry_var
                                        [lineVar].text())
                                addmodelLine += paramVal + " "
                            addmodelLine += "] "
                        else:
                            if str(
                                    self.obj_track.model_entry_var
                                    [value].text()) == "":
                                paramVal = default
                            else:
                                paramVal = str(
                                    self.obj_track.model_entry_var
                                    [value].text())

                            addmodelLine += param + "=" + paramVal + " "

                    addmodelLine += ") "
                    modelParamValue.append([line[0], addmodelLine, line[4]])
                except Exception as e:
                    print("Caught an exception in model ", line[1])
                    print("Exception Message : ", str(e))

        # Adding it to schematic
        for item in modelParamValue:
            if ".ic" in item[1]:
                schematicInfo.insert(0, item[1])
                schematicInfo.insert(0, item[2])
            else:
                schematicInfo.append(item[2])  # Adding Comment
                schematicInfo.append(item[1])  # Adding model line

        return schematicInfo

    def addMicrocontrollerParameter(self, schematicInfo):
        """
        This function adds the Microcontroller Model details to schematicInfo
        """

        # Create object of TrackWidget
        self.obj_track = TrackWidget.TrackWidget()

        # List to store model line
        addmodelLine = []
        modelParamValue = []

        for line in self.obj_track.microcontrollerTrack:
            # print "Model Track :",line
            try:
                start = line[7]
                # end = line[8]
                addmodelLine = ".model " + line[3] + " " + line[2] + "("
                z = 0
                for key, value in line[9].items():
                    # Checking for default value and accordingly assign
                    # param and default.
                    if ':' in key:
                        key = key.split(':')
                        param = key[0]
                        default = key[1]
                    else:
                        param = key
                        default = 0
                    # Checking if value is iterable.its for vector
                    if (
                            not isinstance(value, str) and
                            hasattr(value, '__iter__')
                    ):
                        addmodelLine += param + "=["
                        for lineVar in value:
                            if str(
                                    self.obj_track.microcontroller_var
                                    [lineVar].text()) == "":
                                paramVal = default
                            else:
                                paramVal = str(
                                    self.obj_track.microcontroller_var
                                    [lineVar].text())
                            # Checks For 5th Parameter(Hex File Path)
                            if z == 4:
                                chosen_file_path = paramVal
                                star_file_path = chosen_file_path
                                star_count = 0
                                for c in chosen_file_path:
                                    # If character is uppercase
                                    if c.isupper():
                                        c_in = chosen_file_path.index(c)
                                        c_in += star_count
                                        # Adding asterisks(*) to the path
                                        # around the character
                                        star_file_path = \
                                            star_file_path[
                                                :c_in] + "*" + star_file_path[
                                                c_in] + "**" + star_file_path[
                                                c_in + 1:]
                                        star_count += 3

                                paramVal = "\"" + star_file_path + "\""

                            addmodelLine += paramVal + " "
                            z = z + 1
                        addmodelLine += "] "
                    else:
                        if str(
                                self.obj_track.microcontroller_var
                                [value].text()) == "":
                            paramVal = default
                        else:
                            paramVal = str(
                                self.obj_track.microcontroller_var
                                [value].text())
                        # Checks For 5th Parameter(Hex File Path)
                        if z == 4:
                            chosen_file_path = paramVal
                            star_file_path = chosen_file_path
                            star_count = 0
                            for c in chosen_file_path:
                                # If character is uppercase
                                if c.isupper():
                                    c_in = chosen_file_path.index(c)
                                    c_in += star_count
                                    # Adding asterisks(*) to the path around
                                    # the character
                                    star_file_path = \
                                        star_file_path[:c_in] + "*" + \
                                        star_file_path[c_in] + "**" + \
                                        star_file_path[c_in + 1:]
                                    star_count += 3

                            paramVal = "\"" + star_file_path + "\""
                        z = z + 1
                        addmodelLine += param + "=" + paramVal + " "

                addmodelLine += ") "
                modelParamValue.append([line[0], addmodelLine, line[4]])
            except Exception as e:
                print("Caught an exception in microcontroller ", line[1])
                print("Exception Message : ", str(e))

        # Adding it to schematic
        for item in modelParamValue:
            if ".ic" in item[1]:
                schematicInfo.insert(0, item[1])
                schematicInfo.insert(0, item[2])
            else:
                schematicInfo.append(item[2])  # Adding Comment
                schematicInfo.append(item[1])  # Adding model line

        return schematicInfo

    def addDeviceLibrary(self, schematicInfo, kicadFile):
        """
        This function add the library details to schematicInfo
        """

        (projpath, filename) = os.path.split(kicadFile)

        deviceLibList = self.obj_track.deviceModelTrack
        deviceLine = {}
        # Key:Index, Value:with its updated line in the form of list
        includeLine = []  # All .include line list

        if not deviceLibList:
            print("No library added in the schematic")
        else:
            for eachline in schematicInfo:
                words = eachline.split()
                if words[0] in deviceLibList:
                    # print("Found Library line")
                    index = schematicInfo.index(eachline)
                    completeLibPath = deviceLibList[words[0]]
                    (libpath, libname) = os.path.split(completeLibPath)
                    # print("Library Path :", libpath)
                    # Copying library from devicemodelLibrary to Project Path
                    # Special case for MOSFET
                    tempStr = libname.split(':')
                    libname = tempStr[0]
                    libAbsPath = os.path.join(libpath, libname)

                    if eachline[0] == 'm':
                        # For mosfet library name come along with MOSFET
                        # dimension information
                        dimension = tempStr[1]
                        # Replace last word with library name
                        # words[-1] = libname.split('.')[0]
                        words[-1] = self.getReferenceName(libname, libpath)
                        # Appending Dimension of MOSFET
                        words.append(dimension)
                        deviceLine[index] = words
                        includeLine.append(".include " + libname)

                        shutil.copy2(libAbsPath, projpath)

                    elif eachline[0:6] == 'scmode':
                        (filepath, filemname) = os.path.split(self.clarg1)
                        self.Fileopen = os.path.join(filepath, ".spiceinit")
                        print("==============================================")
                        print("Writing to the .spiceinit file to " +
                              "make ngspice SKY130 compatible")
                        self.writefile = open(self.Fileopen, "w")
                        self.writefile.write('''
set ngbehavior=hsa     ; set compatibility for reading PDK libs
set ng_nomodcheck      ; don't check the model parameters
set num_threads=8      ; CPU hardware threads available
option noinit          ; don't print operating point data
optran 0 0 0 100p 2n 0 ; don't use dc operating point, but transient op)
''')
                        print("==============================================")

                        libs = '''
sky130_fd_pr__model__diode_pd2nw_11v0.model.spice
sky130_fd_pr__model__diode_pw2nd_11v0.model.spice
sky130_fd_pr__model__inductors.model.spice
sky130_fd_pr__model__linear.model.spice
sky130_fd_pr__model__pnp.model.spice
sky130_fd_pr__model__r+c.model.spice
'''
                        includeLine.append(
                            ".lib \"" + libAbsPath + "\" " + tempStr[1])
                        for i in libs.split():
                            includeLine.append(
                                ".include \"" + libAbsPath.replace(
                                    "sky130.lib.spice", i) + "\"")
                        deviceLine[index] = "*scmode"
                        # words.append(completeLibPath)
                        # deviceLine[index] = words

                    elif eachline[0:2] == 'sc' and eachline[0:6] != 'scmode':
                        words[0] = words[0].replace('sc', 'xsc')
                        words.append(completeLibPath)
                        deviceLine[index] = words

                    else:
                        # Replace last word with library name
                        # words[-1] = libname.split('.')[0]
                        words[-1] = self.getReferenceName(libname, libpath)
                        deviceLine[index] = words
                        includeLine.append(".include " + libname)

                        shutil.copy2(completeLibPath, projpath)

            # Adding device line to schematicInfo
            for index, value in deviceLine.items():
                # Update the device line
                strLine = " ".join(str(item) for item in value)
                schematicInfo[index] = strLine

            # This has to be second i.e after deviceLine details
            # Adding .include line to Schematic Info at the start of line
            for item in list(set(includeLine)):
                schematicInfo.insert(0, item)

        return schematicInfo

    def addSubcircuit(self, schematicInfo, kicadFile):
        """
        This function add the subcircuit to schematicInfo
        """
        (projpath, filename) = os.path.split(kicadFile)

        subList = self.obj_track.subcircuitTrack
        subLine = {}
        # Key:Index, Value:with its updated line in the form of list
        includeLine = []  # All .include line list

        if len(self.obj_track.subcircuitList) != len(
                self.obj_track.subcircuitTrack):
            self.msg = QtWidgets.QErrorMessage()
            self.msg.setModal(True)
            self.msg.setWindowTitle("Error Message")
            self.msg.showMessage(
                "Conversion failed. Please add all Subcircuits.")
            self.msg.exec_()
            raise Exception('All subcircuit directories need to be specified.')
        elif not subList:
            print("No Subcircuit Added in the schematic")
        else:
            for eachline in schematicInfo:
                words = eachline.split()
                if words[0] in subList:
                    print("Found Subcircuit line")
                    index = schematicInfo.index(eachline)
                    completeSubPath = subList[words[0]]
                    (subpath, subname) = os.path.split(completeSubPath)
                    print("Library Path :", subpath)
                    # Copying library from devicemodelLibrary to Project Path

                    # Replace last word with library name
                    words[-1] = subname.split('.')[0]
                    subLine[index] = words
                    includeLine.append(".include " + subname + ".sub")

                    src = completeSubPath
                    dst = projpath
                    print(os.listdir(src))
                    for files in os.listdir(src):
                        if os.path.isfile(os.path.join(src, files)):
                            if files != "analysis":
                                shutil.copy2(os.path.join(src, files), dst)

            # Adding subcircuit line to schematicInfo
            for index, value in subLine.items():
                # Update the subcircuit line
                strLine = " ".join(str(item) for item in value)
                schematicInfo[index] = strLine

            # This has to be second i.e after subcircuitLine details
            # Adding .include line to Schematic Info at the start of line
            for item in list(set(includeLine)):
                schematicInfo.insert(0, item)

        return schematicInfo

    def getReferenceName(self, libname, libpath):
        libname = libname.replace('.lib', '.xml')
        library = os.path.join(libpath, libname)

        # Extracting Value from XML
        libtree = ET.parse(library)
        for child in libtree.iter():
            if child.tag == 'ref_model':
                retVal = child.text

        return retVal
