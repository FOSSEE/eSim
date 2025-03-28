from PyQt5 import QtWidgets, QtCore
from PyQt5.Qt import QTableWidgetItem
import xml.etree.ElementTree as ET
from configuration.Appconfig import Appconfig
import os


class ModelEditorclass(QtWidgets.QWidget):
    '''
    - Initialise the layout for dockarea
    - Use QVBoxLayout, QSplitter, QGridLayout to define the layout
    - Initalise directory to save new models,
      savepathtest = 'library/deviceModelLibrary'
    - Initialise buttons and options ====>
        - Name            Function Called
    ========================================
        - New             opennew
        - Edit            openedit
        - Save            savemodelfile
        - Upload          converttoxml
        - Add             addparameters
        - Remove          removeparameter
        - Diode           diode_click
        - BJT             bjt_click
        - MOS             mos_click
        - JFET            jfet_click
        - IGBT            igbt_click
        - Magnetic Core   magnetic_click
    '''

    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        self.init_path = '../../'
        if os.name == 'nt':
            self.init_path = ''

        self.savepathtest = self.init_path + 'library/deviceModelLibrary'
        self.obj_appconfig = Appconfig()
        self.newflag = 0
        self.layout = QtWidgets.QVBoxLayout()
        self.splitter = QtWidgets.QSplitter()
        self.grid = QtWidgets.QGridLayout()
        self.splitter.setOrientation(QtCore.Qt.Vertical)

        # Initialise the table view
        self.modeltable = QtWidgets.QTableWidget()

        self.newbtn = QtWidgets.QPushButton('New')
        self.newbtn.setToolTip('<b>Creating new Model Library</b>')
        self.newbtn.clicked.connect(self.opennew)
        self.editbtn = QtWidgets.QPushButton('Edit')
        self.editbtn.setToolTip('<b>Editing current Model Library</b>')
        self.editbtn.clicked.connect(self.openedit)
        self.savebtn = QtWidgets.QPushButton('Save')
        self.savebtn.setToolTip('<b>Saves the Model Library</b>')
        self.savebtn.setDisabled(True)
        self.savebtn.clicked.connect(self.savemodelfile)
        self.removebtn = QtWidgets.QPushButton('Remove')
        self.removebtn.setHidden(True)
        self.removebtn.clicked.connect(self.removeparameter)
        self.addbtn = QtWidgets.QPushButton('Add')
        self.addbtn.setHidden(True)
        self.addbtn.clicked.connect(self.addparameters)
        self.uploadbtn = QtWidgets.QPushButton('Upload')
        self.uploadbtn.setToolTip(
            '<b>Uploading external .lib file to eSim</b>')
        self.uploadbtn.clicked.connect(self.converttoxml)
        self.grid.addWidget(self.newbtn, 1, 2)
        self.grid.addWidget(self.editbtn, 1, 3)
        self.grid.addWidget(self.savebtn, 1, 4)
        self.grid.addWidget(self.uploadbtn, 1, 5)
        self.grid.addWidget(self.removebtn, 8, 4)
        self.grid.addWidget(self.addbtn, 5, 4)

        self.radiobtnbox = QtWidgets.QButtonGroup()
        self.diode = QtWidgets.QRadioButton('Diode')
        self.diode.setDisabled(True)
        self.bjt = QtWidgets.QRadioButton('BJT')
        self.bjt.setDisabled(True)
        self.mos = QtWidgets.QRadioButton('MOS')
        self.mos.setDisabled(True)
        self.jfet = QtWidgets.QRadioButton('JFET')
        self.jfet.setDisabled(True)
        self.igbt = QtWidgets.QRadioButton('IGBT')
        self.igbt.setDisabled(True)
        self.magnetic = QtWidgets.QRadioButton('Magnetic Core')
        self.magnetic.setDisabled(True)

        self.radiobtnbox.addButton(self.diode)
        self.diode.clicked.connect(self.diode_click)
        self.radiobtnbox.addButton(self.bjt)
        self.bjt.clicked.connect(self.bjt_click)
        self.radiobtnbox.addButton(self.mos)
        self.mos.clicked.connect(self.mos_click)
        self.radiobtnbox.addButton(self.jfet)
        self.jfet.clicked.connect(self.jfet_click)
        self.radiobtnbox.addButton(self.igbt)
        self.igbt.clicked.connect(self.igbt_click)
        self.radiobtnbox.addButton(self.magnetic)
        self.magnetic.clicked.connect(self.magnetic_click)

        # Dropdown for various types supported by that element, ex bjt -> npn
        self.types = QtWidgets.QComboBox()
        self.types.setHidden(True)

        self.grid.addWidget(self.types, 2, 2, 2, 3)
        self.grid.addWidget(self.diode, 3, 1)
        self.grid.addWidget(self.bjt, 4, 1)
        self.grid.addWidget(self.mos, 5, 1)
        self.grid.addWidget(self.jfet, 6, 1)
        self.grid.addWidget(self.igbt, 7, 1)
        self.grid.addWidget(self.magnetic, 8, 1)
        self.setLayout(self.grid)
        self.show()

    def opennew(self):
        '''
        - To create New Model file
        - Change state of other buttons accordingly, ex. enable diode, bjt, ...
        - Validate filename created, to check if one already exists
        '''
        self.addbtn.setHidden(True)
        try:
            self.removebtn.setHidden(True)
            self.modeltable.setHidden(True)
        except BaseException:
            pass

        # Opens new dialog box
        text, ok = QtWidgets.QInputDialog.getText(
            self, 'New Model', 'Enter Model Name:'
        )

        if ok:
            if not text:
                print("Model name cannot be empty")
                print("==================")
                msg = QtWidgets.QErrorMessage(self)
                msg.setModal(True)
                msg.setWindowTitle("Error Message")
                msg.showMessage('The model name cannot be empty')
                msg.exec_()
                return

            self.newflag = 1
            self.diode.setDisabled(False)
            self.bjt.setDisabled(False)
            self.mos.setDisabled(False)
            self.jfet.setDisabled(False)
            self.igbt.setDisabled(False)
            self.magnetic.setDisabled(False)
            self.modelname = (str(text))
        else:
            return

        # Validate if the file created exists already or not
        # Show error accordingly
        self.validation(text)

    def diode_click(self):
        '''
        - Call function, openfiletype, which opens the table view\
            for Diode specs
        - Set states for other elements
        - Diode has no types, so hide that
        '''
        self.openfiletype('Diode')
        self.types.setHidden(True)

    def bjt_click(self):
        '''
        - Set states for other elements
        - Initialise types combo box elements
        - - NPN
        - - PNP
        - Open the default type in the table
        - Add an event listener for type-selection event
        '''
        self.types.setHidden(False)
        self.types.clear()
        self.types.addItem('NPN')
        self.types.addItem('PNP')
        # Open in table default
        filetype = str(self.types.currentText())
        self.openfiletype(filetype)
        # When element selected from combo box, call setfiletype
        self.types.activated[str].connect(self.setfiletype)

    def mos_click(self):
        '''
        - Set states for other elements
        - Initialise types combo box elements
        - - NMOS(Level-1 5um)
        - - NMOS(Level-3 0.5um)
        - - ...
        - Open the default type in the table
        - Add an event listener for type-selection event
        '''
        self.types.setHidden(False)
        self.types.clear()
        self.types.addItem('NMOS(Level-1 5um)')
        self.types.addItem('NMOS(Level-3 0.5um)')
        self.types.addItem('NMOS(Level-8 180um)')
        self.types.addItem('PMOS(Level-1 5um)')
        self.types.addItem('PMOS(Level-3 0.5um)')
        self.types.addItem('PMOS(Level-8 180um)')
        filetype = str(self.types.currentText())
        self.openfiletype(filetype)
        self.types.activated[str].connect(self.setfiletype)

    def jfet_click(self):
        '''
        - Set states for other elements
        - Initialise types combo box elements
        - - N-JFET
        - - P-JFET
        - Open the default type in the table
        - Add an event listener for type-selection event
        '''
        self.types.setHidden(False)
        self.types.clear()
        self.types.addItem('N-JFET')
        self.types.addItem('P-JFET')
        filetype = str(self.types.currentText())
        self.openfiletype(filetype)
        self.types.activated[str].connect(self.setfiletype)

    def igbt_click(self):
        '''
        - Set states for other elements
        - Initialise types combo box elements
        - - N-IGBT
        - - P-IGBT
        - Open the default type in the table
        - Add an event listener for type-selection event
        '''
        self.types.setHidden(False)
        self.types.clear()
        self.types.addItem('N-IGBT')
        self.types.addItem('P-IGBT')
        filetype = str(self.types.currentText())
        self.openfiletype(filetype)
        self.types.activated[str].connect(self.setfiletype)

    def magnetic_click(self):
        '''
        - Set states for other elements
        - Initialise types combo box elements
        - Open the default type in the table
        - Add an event listener for type-selection event
        - No types here, only one view
        '''
        self.openfiletype('Magnetic Core')
        self.types.setHidden(True)

    def setfiletype(self, text):
        '''
        - Triggered when each type selected
        - Get the type clicked, from text
        - Open appropriate table using openfiletype(filetype)
        '''
        self.filetype = str(text)
        self.openfiletype(self.filetype)

    def openfiletype(self, filetype):
        '''
        - Select path for the filetype passed
        - Accordingly call `createtable(path)` to draw tables usingg QTable
        - Check for the state of button before rendering
        '''
        self.path = self.init_path + 'library/deviceModelLibrary/Templates'
        if self.diode.isChecked():
            if filetype == 'Diode':
                path = os.path.join(self.path, 'D.xml')
                self.createtable(path)
        if self.bjt.isChecked():
            if filetype == 'NPN':
                path = os.path.join(self.path, 'NPN.xml')
                self.createtable(path)
            elif filetype == 'PNP':
                path = os.path.join(self.path, 'PNP.xml')
                self.createtable(path)
        if self.mos.isChecked():
            if filetype == 'NMOS(Level-1 5um)':
                path = os.path.join(self.path, 'NMOS-5um.xml')
                self.createtable(path)
            elif filetype == 'NMOS(Level-3 0.5um)':
                path = os.path.join(self.path, 'NMOS-0.5um.xml')
                self.createtable(path)
            elif filetype == 'NMOS(Level-8 180um)':
                path = os.path.join(self.path, 'NMOS-180nm.xml')
                self.createtable(path)
            elif filetype == 'PMOS(Level-1 5um)':
                path = os.path.join(self.path, 'PMOS-5um.xml')
                self.createtable(path)
            elif filetype == 'PMOS(Level-3 0.5um)':
                path = os.path.join(self.path, 'PMOS-0.5um.xml')
                self.createtable(path)
            elif filetype == 'PMOS(Level-8 180um)':
                path = os.path.join(self.path, 'PMOS-180nm.xml')
                self.createtable(path)
        if self.jfet.isChecked():
            if filetype == 'N-JFET':
                path = os.path.join(self.path, 'NJF.xml')
                self.createtable(path)
            elif filetype == 'P-JFET':
                path = os.path.join(self.path, 'PJF.xml')
                self.createtable(path)
        if self.igbt.isChecked():
            if filetype == 'N-IGBT':
                path = os.path.join(self.path, 'NIGBT.xml')
                self.createtable(path)
            elif filetype == 'P-IGBT':
                path = os.path.join(self.path, 'PIGBT.xml')
                self.createtable(path)
        if self.magnetic.isChecked():
            if filetype == 'Magnetic Core':
                path = os.path.join(self.path, 'CORE.xml')
                self.createtable(path)

    def openedit(self):
        '''
        - When `Edit` button clicked, this function called
        - Set states for other buttons accordingly
        - Open the file selector box with path as deviceModelLibrary
        and filetype set as .lib, save it in `self.editfile`
        - Create table for the selected .lib file using\
            `self.createtable(path)`
        - Handle exception of no file selected
        '''
        self.newflag = 0
        self.addbtn.setHidden(True)
        self.types.setHidden(True)
        self.diode.setDisabled(True)
        self.mos.setDisabled(True)
        self.jfet.setDisabled(True)
        self.igbt.setDisabled(True)
        self.bjt.setDisabled(True)
        self.magnetic.setDisabled(True)
        try:
            self.editfile = QtCore.QDir.toNativeSeparators(
                QtWidgets.QFileDialog.getOpenFileName(
                    self, "Open Library Directory",
                    self.init_path + "library/deviceModelLibrary", "*.lib"
                )[0]
            )

            if self.editfile:
                self.createtable(self.editfile)
        except BaseException:
            print("No File selected for edit")

    def createtable(self, modelfile):
        '''
        - Set states for other components
        - Initialise QTable widget
        - Set options for QTable widget
        - Place QTable widget, using `self.grid.addWidget`
        - Select the `.xml` file from the modelfile passed as `.lib`
        - Use ET (xml.etree.ElementTree) to parse the xml file
        - Extract data from the XML and store it in `modeldict`
        - Show the extracted data in QTableWidget
        - Can edit QTable inplace, connect `edit_modeltable`\
            function for editing
        '''
        self.savebtn.setDisabled(False)
        self.addbtn.setHidden(False)
        self.removebtn.setHidden(False)
        self.modelfile = modelfile
        self.modeldict = {}
        self.modeltable = QtWidgets.QTableWidget()
        self.modeltable.resizeColumnsToContents()
        self.modeltable.setColumnCount(2)
        self.modeltable.resizeRowsToContents()
        self.modeltable.resize(200, 200)
        self.grid.addWidget(self.modeltable, 3, 2, 8, 2)
        filepath, filename = os.path.split(self.modelfile)
        base, ext = os.path.splitext(filename)
        self.modelfile = os.path.join(filepath, base + '.xml')
        print("Model File used for creating table : ", self.modelfile)
        self.tree = ET.parse(self.modelfile)
        self.root = self.tree.getroot()
        for elem in self.tree.iter(tag='ref_model'):
            self.ref_model = elem.text
        for elem in self.tree.iter(tag='model_name'):
            self.model_name = elem.text
        row = 0
        # get data from XML and store to dictionary (self.modeldict)
        for params in self.tree.findall('param'):
            for paramlist in params:
                self.modeldict[paramlist.tag] = paramlist.text
                row = row + 1
        self.modeltable.setRowCount(row)
        count = 0
        # setItem in modeltable, for each item in modeldict
        for tags, values in list(self.modeldict.items()):
            self.modeltable.setItem(count, 0, QTableWidgetItem(tags))
            try:
                valueitem = QTableWidgetItem(values)
            except BaseException:
                pass
            self.modeltable.setItem(count, 1, valueitem)
            count = count + 1
        self.modeltable.setHorizontalHeaderLabels(
            ("Parameters;Values").split(";")
        )
        self.modeltable.show()
        self.modeltable.itemChanged.connect(self.edit_modeltable)

    def edit_modeltable(self):
        '''
        - Called when editing model inplace in QTableWidget
        - Set states of other components
        - Get data from the modeltable of the selected row
        - Edit name and value as per needed
        - Add the val name pair in the modeldict
        '''

        self.savebtn.setDisabled(False)
        try:
            indexitem = self.modeltable.currentItem()
            name = str(indexitem.data(0))
            rowno = indexitem.row()
            para = self.modeltable.item(rowno, 0)
            val = str(para.data(0))
            self.modeldict[val] = name
        except BaseException:
            pass

    def addparameters(self):
        '''
        - Called when `Add` button clicked beside QTableWidget
        - Open up dialog box to enter parameter and value accordingly
        - Validate if parameter already in list of parameters
        - Accordingly add parameter and value in modeldict as well as table
        - text1 => parameter, text2 => value
        '''
        text1, ok = QtWidgets.QInputDialog.getText(
            self, 'Parameter', 'Enter Parameter'
        )
        if ok:
            if not text1:
                print("Parameter name cannot be empty")
                print("==================")
                msg = QtWidgets.QErrorMessage(self)
                msg.setModal(True)
                msg.setWindowTitle("Error Message")
                msg.showMessage('The parameter name cannot be empty')
                msg.exec_()
                return
            elif text1 in list(self.modeldict.keys()):
                self.msg = QtWidgets.QErrorMessage(self)
                self.msg.setModal(True)
                self.msg.setWindowTitle("Error Message")
                self.msg.showMessage(
                    "The paramaeter " + text1 + " is already in the list"
                )
                self.msg.exec_()
                return
            text2, ok = QtWidgets.QInputDialog.getText(
                self, 'Value', 'Enter Value'
            )
            if ok:
                if not text2:
                    print("Value cannot be empty")
                    print("==================")
                    msg = QtWidgets.QErrorMessage(self)
                    msg.setModal(True)
                    msg.setWindowTitle("Error Message")
                    msg.showMessage('Value cannot be empty')
                    msg.exec_()
                    return

                currentRowCount = self.modeltable.rowCount()
                self.modeltable.insertRow(currentRowCount)
                self.modeltable.setItem(
                    currentRowCount, 0, QTableWidgetItem(text1)
                )
                self.modeltable.setItem(
                    currentRowCount, 1, QTableWidgetItem(text2)
                )
                self.modeldict[str(text1)] = str(text2)

    def savemodelfile(self):
        '''
        - Called when save functon clicked
        - If new file created, call `createXML` file
        - Else call `savethefile`
        '''
        if self.newflag == 1:
            self.createXML(self.model_name)
        else:
            self.savethefile(self.editfile)

    def createXML(self, model_name):
        '''
        - Create .xml and .lib file if new model is being created
        - Save it in the corresponding compoenent directory,\
            example Diode, IGBT..
        - For each component, separate folder is there
        - Check the contents of .lib and .xml file to\
            understand their structure
        '''
        root = ET.Element("library")
        ET.SubElement(root, "model_name").text = model_name
        ET.SubElement(root, "ref_model").text = self.modelname
        param = ET.SubElement(root, "param")
        for tags, text in list(self.modeldict.items()):
            ET.SubElement(param, tags).text = text
        tree = ET.ElementTree(root)
        defaultcwd = os.getcwd()
        self.savepath = self.init_path + 'library/deviceModelLibrary'
        if self.diode.isChecked():
            savepath = os.path.join(self.savepath, 'Diode')
            os.chdir(savepath)
            txtfile = open(self.modelname + '.lib', 'w')
            txtfile.write(
                '.MODEL ' +
                self.modelname +
                ' ' +
                self.model_name +
                '(')
            for tags, text in list(self.modeldict.items()):
                txtfile.write(' ' + tags + '=' + text)
            txtfile.write(' )\n')
            tree.write(self.modelname + ".xml")
            self.obj_appconfig.print_info(
                'New ' +
                self.modelname +
                ' ' +
                self.model_name +
                ' library created at ' +
                os.getcwd())
        if self.mos.isChecked():
            savepath = os.path.join(self.savepath, 'MOS')
            os.chdir(savepath)
            txtfile = open(self.modelname + '.lib', 'w')
            txtfile.write(
                '.MODEL ' +
                self.modelname +
                ' ' +
                self.model_name +
                '(')
            for tags, text in list(self.modeldict.items()):
                txtfile.write(' ' + tags + '=' + text)
            txtfile.write(' )\n')
            tree.write(self.modelname + ".xml")
            self.obj_appconfig.print_info(
                'New ' +
                self.modelname +
                ' ' +
                self.model_name +
                ' library created at ' +
                os.getcwd())
        if self.jfet.isChecked():
            savepath = os.path.join(self.savepath, 'JFET')
            os.chdir(savepath)
            txtfile = open(self.modelname + '.lib', 'w')
            txtfile.write(
                '.MODEL ' +
                self.modelname +
                ' ' +
                self.model_name +
                '(')
            for tags, text in list(self.modeldict.items()):
                txtfile.write(' ' + tags + '=' + text)
            txtfile.write(' )\n')
            tree.write(self.modelname + ".xml")
            self.obj_appconfig.print_info(
                'New ' +
                self.modelname +
                ' ' +
                self.model_name +
                ' library created at ' +
                os.getcwd())
        if self.igbt.isChecked():
            savepath = os.path.join(self.savepath, 'IGBT')
            os.chdir(savepath)
            txtfile = open(self.modelname + '.lib', 'w')
            txtfile.write(
                '.MODEL ' +
                self.modelname +
                ' ' +
                self.model_name +
                '(')
            for tags, text in list(self.modeldict.items()):
                txtfile.write(' ' + tags + '=' + text)
            txtfile.write(' )\n')
            tree.write(self.modelname + ".xml")
            self.obj_appconfig.print_info(
                'New ' +
                self.modelname +
                ' ' +
                self.model_name +
                ' library created at ' +
                os.getcwd())
        if self.magnetic.isChecked():
            savepath = os.path.join(self.savepath, 'Misc')
            os.chdir(savepath)
            txtfile = open(self.modelname + '.lib', 'w')
            txtfile.write(
                '.MODEL ' +
                self.modelname +
                ' ' +
                self.model_name +
                '(')
            for tags, text in list(self.modeldict.items()):
                txtfile.write(' ' + tags + '=' + text)
            txtfile.write(' )\n')
            tree.write(self.modelname + ".xml")
            self.obj_appconfig.print_info(
                'New ' +
                self.modelname +
                ' ' +
                self.model_name +
                ' library created at ' +
                os.getcwd())
        if self.bjt.isChecked():
            savepath = os.path.join(self.savepath, 'Transistor')
            os.chdir(savepath)
            txtfile = open(self.modelname + '.lib', 'w')
            txtfile.write(
                '.MODEL ' +
                self.modelname +
                ' ' +
                self.model_name +
                '(')
            for tags, text in list(self.modeldict.items()):
                txtfile.write(' ' + tags + '=' + text)
            txtfile.write(' )\n')
            tree.write(self.modelname + ".xml")
            self.obj_appconfig.print_info(
                'New ' +
                self.modelname +
                ' ' +
                self.model_name +
                ' library created at ' +
                os.getcwd())
        txtfile.close()

        msg = "Model saved successfully!"
        QtWidgets.QMessageBox.information(
            self, "Information", msg, QtWidgets.QMessageBox.Ok
        )

        os.chdir(defaultcwd)

    def validation(self, text):
        '''
        - This function checks if the file (xml type) with the name\
            already exists
        - Accordingly show error message
        '''
        newfilename = text + '.xml'

        all_dir = [x[0] for x in os.walk(self.savepathtest)]
        for each_dir in all_dir:
            all_files = os.listdir(each_dir)
            if newfilename in all_files:
                self.msg = QtWidgets.QErrorMessage(self)
                self.msg.setModal(True)
                self.msg.setWindowTitle("Error Message")
                self.msg.showMessage(
                    'The file with name ' + text + ' already exists.')
                self.msg.exec_()

    def savethefile(self, editfile):
        '''
        - This function save the editing in the model table
        - Create .lib and .xml file for the editfile path and replace them
        - Also print Updated Library with libpath in the command window
        '''
        xmlpath, file = os.path.split(editfile)
        filename = os.path.splitext(file)[0]
        libpath = os.path.join(xmlpath, filename + '.lib')
        libfile = open(libpath, 'w')
        libfile.write(
            '.MODEL ' +
            self.ref_model +
            ' ' +
            self.model_name +
            '(')
        for tags, text in list(self.modeldict.items()):
            libfile.write(' ' + tags + '=' + text)
        libfile.write(' )\n')
        libfile.close()

        root = ET.Element("library")
        ET.SubElement(root, "model_name").text = self.model_name
        ET.SubElement(root, "ref_model").text = self.ref_model
        param = ET.SubElement(root, "param")
        for tags, text in list(self.modeldict.items()):
            ET.SubElement(param, tags).text = text
        tree = ET.ElementTree(root)

        tree.write(os.path.join(xmlpath, filename + ".xml"))

        self.obj_appconfig.print_info('Updated library ' + libpath)

        msg = "Model saved successfully!"
        QtWidgets.QMessageBox.information(
            self, "Information", msg, QtWidgets.QMessageBox.Ok
        )

    def removeparameter(self):
        '''
        - Get the index of the current selected item
        - Remove the whole row from QTable Widget
        - Remove the param,value pair from modeldict
        '''
        self.savebtn.setDisabled(False)
        index = self.modeltable.currentIndex()
        remove_item = self.modeltable.item(index.row(), 0)

        if remove_item:
            remove_item = remove_item.text()
            self.modeltable.removeRow(index.row())
            del self.modeldict[str(remove_item)]
        else:
            print("No parameter selected to remove")
            print("==================")
            msg = QtWidgets.QErrorMessage(self)
            msg.setModal(True)
            msg.setWindowTitle("Error Message")
            msg.showMessage('No parameter selected to remove')
            msg.exec_()

    def converttoxml(self):
        '''
        - Called when upload button clicked
        - Used to read file form a certain location for .lib extension
        - Accordingly parse it and extract modelname and modelref
        - Also extract param value pairs
        - Take input the name of the library you want to save it as
        - Save it in `User Libraries` with the given name,
        and input from uploaded file
        '''
        self.addbtn.setHidden(True)
        self.removebtn.setHidden(True)
        self.modeltable.setHidden(True)
        model_dict = {}
        stringof = []

        self.libfile = QtCore.QDir.toNativeSeparators(
            QtWidgets.QFileDialog.getOpenFileName(
                self, "Open Library Directory",
                self.init_path + "library/deviceModelLibrary", "*.lib"
            )[0]
        )

        if not self.libfile:
            return

        libopen = open(self.libfile)
        filedata = libopen.read().split()
        modelcount = 0
        for words in filedata:
            modelcount = modelcount + 1
            if words.lower() == '.model':
                break
        ref_model = filedata[modelcount]
        model_name = filedata[modelcount + 1]
        model_name = list(model_name)
        modelnamecnt = 0
        flag = 0
        for chars in model_name:
            modelnamecnt = modelnamecnt + 1
            if chars == '(':
                flag = 1
                break
        if flag == 1:
            model_name = ''.join(model_name[0:modelnamecnt - 1])
        else:
            model_name = ''.join(model_name)

        libopen1 = open(self.libfile)
        while True:
            char = libopen1.read(1)
            if not char:
                break
            stringof.append(char)

        count = 0
        for chars in stringof:
            count = count + 1
            if chars == '(':
                break
        count1 = 0
        for chars in stringof:
            count1 = count1 + 1
            if chars == ')':
                break
        stringof = stringof[count:count1 - 1]
        stopcount = []
        listofname = []
        stopcount.append(0)
        count = 0
        for chars in stringof:
            count = count + 1
            if chars == '=':
                stopcount.append(count)
        stopcount.append(count)

        i = 0
        for no in stopcount:
            try:
                listofname.append(
                    ''.join(stringof[int(stopcount[i]):int(stopcount[i + 1])]))
                i = i + 1
            except BaseException:
                pass
        listoflist = []
        listofname2 = [
            el.replace(
                '\t',
                '').replace(
                '\n',
                ' ').replace(
                '+',
                '').replace(
                    ')',
                    '').replace(
                        '=',
                '') for el in listofname]
        listofname = []
        for item in listofname2:
            listofname.append(item.rstrip().lstrip())
        for values in listofname:
            valuelist = values.split(' ')
            listoflist.append(valuelist)
        for i in range(1, len(listoflist)):
            model_dict[listoflist[0][0]] = listoflist[1][0]
            try:
                model_dict[listoflist[i][-1]] = listoflist[i + 1][0]
            except BaseException:
                pass
        root = ET.Element("library")
        ET.SubElement(root, "model_name").text = model_name
        ET.SubElement(root, "ref_model").text = ref_model
        param = ET.SubElement(root, "param")
        for tags, text in list(model_dict.items()):
            ET.SubElement(param, tags).text = text
        tree = ET.ElementTree(root)

        defaultcwd = os.getcwd()
        savepath = os.path.join(self.savepathtest, 'User Libraries')
        os.chdir(savepath)
        text, ok1 = QtWidgets.QInputDialog.getText(
            self, 'Model Name', 'Enter Model Library Name'
        )
        if ok1:
            if not text:
                print("Model library name cannot be empty")
                print("==================")
                msg = QtWidgets.QErrorMessage(self)
                msg.setModal(True)
                msg.setWindowTitle("Error Message")
                msg.showMessage('The model library name cannot be empty')
                msg.exec_()
            else:
                tree.write(text + ".xml")
                fileopen = open(text + ".lib", 'w')
                f = open(self.libfile)
                fileopen.write(f.read())
                f.close()
                fileopen.close()

        os.chdir(defaultcwd)
        libopen.close()
        libopen1.close()
