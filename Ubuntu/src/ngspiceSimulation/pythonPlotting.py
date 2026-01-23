from __future__ import division  # Used for decimal division
# eg: 2/3=0.66 and not '0' 6/2=3.0 and 6//2=3
import os
from PyQt5 import QtGui, QtCore, QtWidgets
from decimal import Decimal, getcontext
from matplotlib.backends.backend_qt5agg\
    import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg\
    import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from configuration.Appconfig import Appconfig
import numpy as np


# This class creates Python Plotting window
class plotWindow(QtWidgets.QMainWindow):
    """
    This class defines python plotting window, its features, buttons,
    colors, AC and DC analysis, plotting etc.
    """

    def __init__(self, fpath, projectName):
        """This create constructor for plotWindow class."""
        QtWidgets.QMainWindow.__init__(self)
        self.fpath = fpath
        self.projectName = projectName
        self.obj_appconfig = Appconfig()
        print("Complete Project Path : ", self.fpath)
        print("Project Name : ", self.projectName)
        self.obj_appconfig.print_info(
            'Ngspice simulation is called : ' + self.fpath)
        self.obj_appconfig.print_info(
            'PythonPlotting is called : ' + self.fpath)
        self.combo = []
        self.combo1 = []
        self.combo1_rev = []
        # Creating Frame
        self.createMainFrame()

    def createMainFrame(self):
        self.mainFrame = QtWidgets.QWidget()
        self.dpi = 100
        self.fig = Figure((7.0, 7.0), dpi=self.dpi)
        # Creating Canvas which will figure
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.mainFrame)
        self.axes = self.fig.add_subplot(111)
        self.navToolBar = NavigationToolbar(self.canvas, self.mainFrame)

        # LeftVbox hold navigation tool bar and canvas
        self.left_vbox = QtWidgets.QVBoxLayout()
        self.left_vbox.addWidget(self.navToolBar)
        self.left_vbox.addWidget(self.canvas)

        # right VBOX is main Layout which hold right grid(bottom part) and top
        # grid(top part)
        self.right_vbox = QtWidgets.QVBoxLayout()
        self.right_grid = QtWidgets.QGridLayout()
        self.top_grid = QtWidgets.QGridLayout()

        # Get DataExtraction Details
        self.obj_dataext = DataExtraction()
        self.plotType = self.obj_dataext.openFile(self.fpath)

        self.obj_dataext.computeAxes()
        self.a = self.obj_dataext.numVals()

        self.chkbox = []

        # Generating list of colors :
        # ,(0.4,0.5,0.2),(0.1,0.4,0.9),(0.4,0.9,0.2),(0.9,0.4,0.9)]
        self.full_colors = ['r', 'b', 'g', 'y', 'c', 'm', 'k']
        self.color = []
        for i in range(0, self.a[0] - 1):
            if i % 7 == 0:
                self.color.append(self.full_colors[0])
            elif (i - 1) % 7 == 0:
                self.color.append(self.full_colors[1])
            elif (i - 2) % 7 == 0:
                self.color.append(self.full_colors[2])
            elif (i - 3) % 7 == 0:
                self.color.append(self.full_colors[3])
            elif (i - 4) % 7 == 0:
                self.color.append(self.full_colors[4])
            elif (i - 5) % 7 == 0:
                self.color.append(self.full_colors[5])
            elif (i - 6) % 7 == 0:
                self.color.append(self.full_colors[6])

        # Color generation ends here

        # Total number of voltage source
        self.volts_length = self.a[1]
        self.analysisType = QtWidgets.QLabel()
        self.top_grid.addWidget(self.analysisType, 0, 0)
        self.listNode = QtWidgets.QLabel()
        self.top_grid.addWidget(self.listNode, 1, 0)
        self.listBranch = QtWidgets.QLabel()
        self.top_grid.addWidget(self.listBranch, self.a[1] + 2, 0)
        for i in range(0, self.a[1]):  # a[0]-1
            self.chkbox.append(QtWidgets.QCheckBox(self.obj_dataext.NBList[i]))
            self.chkbox[i].setStyleSheet('color')
            self.chkbox[i].setToolTip('<b>Check To Plot</b>')
            self.top_grid.addWidget(self.chkbox[i], i + 2, 0)
            self.colorLab = QtWidgets.QLabel()
            self.colorLab.setText('____')
            self.colorLab.setStyleSheet(
                self.colorName(
                    self.color[i]) +
                '; font-weight = bold;')
            self.top_grid.addWidget(self.colorLab, i + 2, 1)

        for i in range(self.a[1], self.a[0] - 1):  # a[0]-1
            self.chkbox.append(QtWidgets.QCheckBox(self.obj_dataext.NBList[i]))
            self.chkbox[i].setToolTip('<b>Check To Plot</b>')
            self.top_grid.addWidget(self.chkbox[i], i + 3, 0)
            self.colorLab = QtWidgets.QLabel()
            self.colorLab.setText('____')
            self.colorLab.setStyleSheet(
                self.colorName(
                    self.color[i]) +
                '; font-weight = bold;')
            self.top_grid.addWidget(self.colorLab, i + 3, 1)

        # Buttons for Plot, multimeter, plotting function.
        self.clear = QtWidgets.QPushButton("Clear")
        self.warnning = QtWidgets.QLabel()
        self.funcName = QtWidgets.QLabel()
        self.funcExample = QtWidgets.QLabel()

        self.plotbtn = QtWidgets.QPushButton("Plot")
        self.plotbtn.setToolTip('<b>Press</b> to Plot')
        self.multimeterbtn = QtWidgets.QPushButton("Multimeter")
        self.multimeterbtn.setToolTip(
            '<b>RMS</b> value of the current and voltage is displayed')
        self.text = QtWidgets.QLineEdit()
        self.funcLabel = QtWidgets.QLabel()
        self.palette1 = QtGui.QPalette()
        self.palette2 = QtGui.QPalette()
        self.plotfuncbtn = QtWidgets.QPushButton("Plot Function")
        self.plotfuncbtn.setToolTip('<b>Press</b> to Plot the function')

        self.palette1.setColor(QtGui.QPalette.Foreground, QtCore.Qt.blue)
        self.palette2.setColor(QtGui.QPalette.Foreground, QtCore.Qt.red)
        self.funcName.setPalette(self.palette1)
        self.funcExample.setPalette(self.palette2)
        # Widgets for grid, plot button and multimeter button.
        self.right_vbox.addLayout(self.top_grid)
        self.right_vbox.addWidget(self.plotbtn)
        self.right_vbox.addWidget(self.multimeterbtn)

        self.right_grid.addWidget(self.funcLabel, 1, 0)
        self.right_grid.addWidget(self.text, 1, 1)
        self.right_grid.addWidget(self.plotfuncbtn, 2, 1)
        self.right_grid.addWidget(self.clear, 2, 0)
        self.right_grid.addWidget(self.warnning, 3, 0)
        self.right_grid.addWidget(self.funcName, 4, 0)
        self.right_grid.addWidget(self.funcExample, 4, 1)
        self.right_vbox.addLayout(self.right_grid)

        self.hbox = QtWidgets.QHBoxLayout()
        self.hbox.addLayout(self.left_vbox)
        self.hbox.addLayout(self.right_vbox)

        self.widget = QtWidgets.QWidget()
        self.widget.setLayout(self.hbox)  # finalvbox
        self.scrollArea = QtWidgets.QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.widget)
        '''
        Right side box containing checkbox for different inputs and
        options of plot, multimeter and plot function.
        '''
        self.finalhbox = QtWidgets.QHBoxLayout()
        self.finalhbox.addWidget(self.scrollArea)
        # Right side window frame showing list of nodes and branches.
        self.mainFrame.setLayout(self.finalhbox)
        self.showMaximized()

        self.listNode.setText("<font color='indigo'>List of Nodes:</font>")
        self.listBranch.setText(
            "<font color='indigo'>List of Branches:</font>")
        self.funcLabel.setText("<font color='indigo'>Function:</font>")
        self.funcName.setText(
            "<font color='indigo'>Standard functions</font>\
                <br><br>Addition:<br>Subtraction:<br>\
                Multiplication:<br>Division:<br>Comparison:"
        )
        self.funcExample.setText(
            "\n\nNode1 + Node2\nNode1 - Node2\nNode1 * Node2\nNode1 / Node2\
                \nNode1 vs Node2")

        # Connecting to plot and clear function
        self.clear.clicked.connect(self.pushedClear)
        self.plotfuncbtn.clicked.connect(self.pushedPlotFunc)
        self.multimeterbtn.clicked.connect(self.multiMeter)

        # for AC analysis
        if self.plotType[0] == 0:
            self.analysisType.setText("<b>AC Analysis</b>")
            if self.plotType[1] == 1:
                self.plotbtn.clicked.connect(self.onPush_decade)
            else:
                self.plotbtn.clicked.connect(self.onPush_ac)
        # for transient analysis
        elif self.plotType[0] == 1:
            self.analysisType.setText("<b>Transient Analysis</b>")
            self.plotbtn.clicked.connect(self.onPush_trans)
        else:
            # For DC analysis
            self.analysisType.setText("<b>DC Analysis</b>")
            self.plotbtn.clicked.connect(self.onPush_dc)

        self.setCentralWidget(self.mainFrame)

    # definition of functions pushedClear, pushedPlotFunc.
    def pushedClear(self):
        self.text.clear()
        self.axes.cla()
        self.canvas.draw()

    def pushedPlotFunc(self):
        self.parts = str(self.text.text())
        self.parts = self.parts.split(" ")

        if self.parts[len(self.parts) - 1] == '':
            self.parts = self.parts[0:-1]

        self.values = self.parts
        self.comboAll = []
        self.axes.cla()

        self.plotType2 = self.obj_dataext.openFile(self.fpath)

        if len(self.parts) <= 2:
            self.warnning.setText("Too few arguments!\nRefer syntax below!")
            QtWidgets.QMessageBox.about(
                self, "Warning!!", "Too Few Arguments/SYNTAX Error!\
                    \n Refer Examples")
            return
        else:
            self.warnning.setText("")

        a = []
        finalResult = []
        # p = 0

        for i in range(len(self.parts)):
            if i % 2 == 0:
                for j in range(len(self.obj_dataext.NBList)):
                    if self.parts[i] == self.obj_dataext.NBList[j]:
                        a.append(j)

        if len(a) != len(self.parts) // 2 + 1:
            QtWidgets.QMessageBox.about(
                self, "Warning!!",
                "One of the operands doesn't belong to "
                "the above list of Nodes!!"
            )
            return

        for i in a:
            self.comboAll.append(self.obj_dataext.y[i])

        for i in range(len(a)):

            if a[i] == len(self.obj_dataext.NBList):
                QtWidgets.QMessageBox.about(
                    self, "Warning!!", "One of the operands doesn't belong " +
                    "to the above list!!"
                )
                self.warnning.setText(
                    "<font color='red'>To Err Is Human!<br>One of the " +
                    "operands doesn't belong to the above list!!</font>"
                )
                return

        if self.parts[1] == 'vs':
            if len(self.parts) > 3:
                self.warnning.setText("Enter two operands only!!")
                QtWidgets.QMessageBox.about(
                    self, "Warning!!", "Recheck the expression syntax!"
                )
                return
            else:
                self.axes.cla()

                for i in range(len(self.obj_dataext.y[a[0]])):
                    self.combo.append(self.obj_dataext.y[a[0]][i])
                    self.combo1.append(self.obj_dataext.y[a[1]][i])

                self.axes.plot(
                    self.combo,
                    self.combo1,
                    c=self.color[1],
                    label=str(2))  # _rev

                if max(a) < self.volts_length:
                    self.axes.set_ylabel('Voltage(V)-->')
                    self.axes.set_xlabel('Voltage(V)-->')
                else:
                    self.axes.set_ylabel('Current(I)-->')
                    self.axes.set_ylabel('Current(I)-->')

        elif max(a) >= self.volts_length and min(a) < self.volts_length:
            QtWidgets.QMessageBox.about(
                self, "Warning!!", "Do not combine Voltage and Current!!"
            )
            return

        else:
            for j in range(len(self.comboAll[0])):
                for i in range(len(self.values)):
                    if i % 2 == 0:
                        self.values[i] = str(self.comboAll[i // 2][j])
                        re = " ".join(self.values[:])
                try:
                    finalResult.append(eval(re))
                except ArithmeticError:
                    QtWidgets.QMessageBox.about(
                        self, "Warning!!", "Dividing by zero!!"
                    )
                    return

            if self.plotType2[0] == 0:
                # self.setWindowTitle('AC Analysis')
                if self.plotType2[1] == 1:
                    self.axes.semilogx(
                        self.obj_dataext.x,
                        finalResult,
                        c=self.color[0],
                        label=str(1))
                else:
                    self.axes.plot(
                        self.obj_dataext.x,
                        finalResult,
                        c=self.color[0],
                        label=str(1))

                self.axes.set_xlabel('freq-->')

                if max(a) < self.volts_length:
                    self.axes.set_ylabel('Voltage(V)-->')
                else:
                    self.axes.set_ylabel('Current(I)-->')

            elif self.plotType2[0] == 1:
                # self.setWindowTitle('Transient Analysis')
                self.axes.plot(
                    self.obj_dataext.x,
                    finalResult,
                    c=self.color[0],
                    label=str(1))
                self.axes.set_xlabel('time-->')
                if max(a) < self.volts_length:
                    self.axes.set_ylabel('Voltage(V)-->')
                else:
                    self.axes.set_ylabel('Current(I)-->')

            else:
                # self.setWindowTitle('DC Analysis')
                self.axes.plot(
                    self.obj_dataext.x,
                    finalResult,
                    c=self.color[0],
                    label=str(1))
                self.axes.set_xlabel('I/P Voltage-->')
                if max(a) < self.volts_length:
                    self.axes.set_ylabel('Voltage(V)-->')
                else:
                    self.axes.set_ylabel('Current(I)-->')

        self.axes.grid(True)
        self.canvas.draw()
        self.combo = []
        self.combo1 = []
        self.combo1_rev = []

    # definition of functions onPush_decade, onPush_ac, onPush_trans,\
    # onPush_dc, color and multimeter and getRMSValue.
    def onPush_decade(self):
        boxCheck = 0
        self.axes.cla()

        for i, j in zip(self.chkbox, list(range(len(self.chkbox)))):
            if i.isChecked():
                boxCheck += 1
                self.axes.semilogx(
                    self.obj_dataext.x,
                    self.obj_dataext.y[j],
                    c=self.color[j],
                    label=str(
                        j + 1))
                self.axes.set_xlabel('freq-->')
                if j < self.volts_length:
                    self.axes.set_ylabel('Voltage(V)-->')
                else:
                    self.axes.set_ylabel('Current(I)-->')

                self.axes.grid(True)
        if boxCheck == 0:
            QtWidgets.QMessageBox.about(
                self, "Warning!!", "Please select at least one Node OR Branch"
            )
            return

        self.canvas.draw()

    def onPush_ac(self):
        self.axes.cla()
        boxCheck = 0
        for i, j in zip(self.chkbox, list(range(len(self.chkbox)))):
            if i.isChecked():
                boxCheck += 1
                self.axes.plot(
                    self.obj_dataext.x,
                    self.obj_dataext.y[j],
                    c=self.color[j],
                    label=str(
                        j + 1))
                self.axes.set_xlabel('freq-->')
                if j < self.volts_length:
                    self.axes.set_ylabel('Voltage(V)-->')
                else:
                    self.axes.set_ylabel('Current(I)-->')
                self.axes.grid(True)
        if boxCheck == 0:
            QtWidgets.QMessageBox.about(
                self, "Warning!!", "Please select at least one Node OR Branch"
            )
            return

        self.canvas.draw()

    def onPush_trans(self):
        self.axes.cla()
        boxCheck = 0
        for i, j in zip(self.chkbox, list(range(len(self.chkbox)))):
            if i.isChecked():
                boxCheck += 1
                self.axes.plot(
                    self.obj_dataext.x,
                    self.obj_dataext.y[j],
                    c=self.color[j],
                    label=str(
                        j + 1))
                self.axes.set_xlabel('time-->')
                if j < self.volts_length:
                    self.axes.set_ylabel('Voltage(V)-->')
                else:
                    self.axes.set_ylabel('Current(I)-->')
                self.axes.grid(True)
        if boxCheck == 0:
            QtWidgets.QMessageBox.about(
                self, "Warning!!", "Please select at least one Node OR Branch"
            )
            return
        self.canvas.draw()

    def onPush_dc(self):
        boxCheck = 0
        self.axes.cla()
        for i, j in zip(self.chkbox, list(range(len(self.chkbox)))):
            if i.isChecked():
                boxCheck += 1
                self.axes.plot(
                    self.obj_dataext.x,
                    self.obj_dataext.y[j],
                    c=self.color[j],
                    label=str(
                        j + 1))
                self.axes.set_xlabel('Voltage Sweep(V)-->')

                if j < self.volts_length:
                    self.axes.set_ylabel('Voltage(V)-->')
                else:
                    self.axes.set_ylabel('Current(I)-->')
                self.axes.grid(True)
        if boxCheck == 0:
            QtWidgets.QMessageBox.about(
                self, "Warning!!", "Please select atleast one Node OR Branch"
            )
            return

        self.canvas.draw()

    def colorName(self, letter):
        return {
            'r': 'color:red',
            'b': 'color:blue',
            'g': 'color:green',
            'y': 'color:yellow',
            'c': 'color:cyan',
            'm': 'color:magenta',
            'k': 'color:black'
        }[letter]

    def multiMeter(self):
        print("Function : MultiMeter")
        self.obj = {}
        boxCheck = 0
        loc_x = 300
        loc_y = 300

        for i, j in zip(self.chkbox, list(range(len(self.chkbox)))):
            if i.isChecked():
                print("Check box", self.obj_dataext.NBList[j])
                boxCheck += 1
                if self.obj_dataext.NBList[j] in self.obj_dataext.NBIList:
                    voltFlag = False
                else:
                    voltFlag = True
                # Initializing Multimeter
                self.obj[j] = MultimeterWidgetClass(
                    self.obj_dataext.NBList[j], self.getRMSValue(
                        self.obj_dataext.y[j]), loc_x, loc_y, voltFlag)
                loc_x += 50
                loc_y += 50
                # Adding object of multimeter to dictionary
                (
                    self.obj_appconfig.
                    dock_dict[
                        self.obj_appconfig.current_project['ProjectName']].
                    append(self.obj[j])
                )

        if boxCheck == 0:
            QtWidgets.QMessageBox.about(
                self, "Warning!!", "Please select at least one Node OR Branch"
            )

    def getRMSValue(self, dataPoints):
        getcontext().prec = 5
        return np.sqrt(np.mean(np.square(dataPoints)))


class MultimeterWidgetClass(QtWidgets.QWidget):
    def __init__(self, node_branch, rmsValue, loc_x, loc_y, voltFlag):
        QtWidgets.QWidget.__init__(self)

        self.multimeter = QtWidgets.QWidget(self)
        if voltFlag:
            self.node_branchLabel = QtWidgets.QLabel("Node")
            self.rmsValue = QtWidgets.QLabel(str(rmsValue) + " Volts")
        else:
            self.node_branchLabel = QtWidgets.QLabel("Branch")
            self.rmsValue = QtWidgets.QLabel(str(rmsValue) + " Amp")

        self.rmsLabel = QtWidgets.QLabel("RMS Value")
        self.nodeBranchValue = QtWidgets.QLabel(str(node_branch))

        self.layout = QtWidgets.QGridLayout(self)
        self.layout.addWidget(self.node_branchLabel, 0, 0)
        self.layout.addWidget(self.rmsLabel, 0, 1)
        self.layout.addWidget(self.nodeBranchValue, 1, 0)
        self.layout.addWidget(self.rmsValue, 1, 1)

        self.multimeter.setLayout(self.layout)
        self.setGeometry(loc_x, loc_y, 200, 100)
        self.setGeometry(loc_x, loc_y, 300, 100)
        self.setWindowTitle("MultiMeter")
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.show()


class DataExtraction:
    def __init__(self):
        self.obj_appconfig = Appconfig()
        self.data = []
        # consists of all the columns of data belonging to nodes and branches
        self.y = []  # stores y-axis data
        self.x = []  # stores x-axis data

    def numberFinder(self, fpath):
        # Opening Analysis file
        with open(os.path.join(fpath, "analysis")) as f3:
            self.analysisInfo = f3.read()
        self.analysisInfo = self.analysisInfo.split(" ")

        # Reading data file for voltage
        with open(os.path.join(fpath, "plot_data_v.txt")) as f2:
            self.voltData = f2.read()

        self.voltData = self.voltData.split("\n")

        # Initializing variable
        # 'p' gives no. of lines of data for each node/branch
        # 'npv' gives the no of partitions for a single voltage node
        # 'vnumber' gives total number of voltage
        # 'inumber' gives total number of current

        p = npv = vnumber = inumber = 0

        # Finding totla number of voltage node
        for i in self.voltData[3:]:
            # it has possible names of voltage nodes in NgSpice
            if "Index" in i:  # "V(" in i or "x1" in i or "u3" in i:
                vnumber += 1

        # Reading Current Source Data
        with open(os.path.join(fpath, "plot_data_i.txt")) as f1:
            self.currentData = f1.read()
        self.currentData = self.currentData.split("\n")

        # Finding Number of Branch
        for i in self.currentData[3:]:
            if "#branch" in i:
                inumber += 1

        self.dec = 0

        # For AC
        if self.analysisInfo[0][-3:] == ".ac":
            self.analysisType = 0
            if "dec" in self.analysisInfo:
                self.dec = 1

            for i in self.voltData[3:]:
                p += 1  # 'p' gives no. of lines of data for each node/branch
                if "Index" in i:
                    npv += 1
                # 'npv' gives the no of partitions for a single voltage node
                # print("npv:", npv)
                if "AC" in i:  # DC for dc files and AC for ac ones
                    break

        elif ".tran" in self.analysisInfo:
            self.analysisType = 1
            for i in self.voltData[3:]:
                p += 1
                if "Index" in i:
                    npv += 1
                # 'npv' gives the no of partitions for a single voltage node
                # print("npv:", npv)
                if "Transient" in i:  # DC for dc files and AC for ac ones
                    break

        # For DC:
        else:
            self.analysisType = 2
            for i in self.voltData[3:]:
                p += 1
                if "Index" in i:
                    npv += 1
                # 'npv' gives the no of partitions for a single voltage node
                # print("npv:", npv)
                if "DC" in i:  # DC for dc files and AC for ac ones
                    break

        vnumber = vnumber // npv  # vnumber gives the no of voltage nodes
        inumber = inumber // npv  # inumber gives the no of branches

        p = [p, vnumber, self.analysisType, self.dec, inumber]

        return p

    def openFile(self, fpath):
        try:
            with open(os.path.join(fpath, "plot_data_i.txt")) as f2:
                alli = f2.read()

            alli = alli.split("\n")
            self.NBIList = []

            with open(os.path.join(fpath, "plot_data_v.txt")) as f1:
                allv = f1.read()

        except Exception as e:
            print("Exception Message : ", str(e))
            self.obj_appconfig.print_error('Exception Message :' + str(e))
            self.msg = QtWidgets.QErrorMessage()
            self.msg.setModal(True)
            self.msg.setWindowTitle("Error Message")
            self.msg.showMessage('Unable to open plot data files.')
            self.msg.exec_()

        try:
            for l in alli[3].split(" "):
                if len(l) > 0:
                    self.NBIList.append(l)
            self.NBIList = self.NBIList[2:]
            len_NBIList = len(self.NBIList)
        except Exception as e:
            print("Exception Message : ", str(e))
            self.obj_appconfig.print_error('Exception Message :' + str(e))
            self.msg = QtWidgets.QErrorMessage()
            self.msg.setModal(True)
            self.msg.setWindowTitle("Error Message")
            self.msg.showMessage('Unable to read Analysis File.')
            self.msg.exec_()

        d = self.numberFinder(fpath)
        d1 = int(d[0] + 1)
        d2 = int(d[1])
        d3 = d[2]
        d4 = d[4]

        dec = [d3, d[3]]
        self.NBList = []
        allv = allv.split("\n")
        for l in allv[3].split(" "):
            if len(l) > 0:
                self.NBList.append(l)
        self.NBList = self.NBList[2:]
        len_NBList = len(self.NBList)
        print("NBLIST", self.NBList)

        ivals = []
        inum = len(allv[5].split("\t"))
        inum_i = len(alli[5].split("\t"))

        full_data = []

        # Creating list of data:
        if d3 < 3:
            for i in range(1, d2):
                for l in allv[3 + i * d1].split(" "):
                    if len(l) > 0:
                        self.NBList.append(l)
                self.NBList.pop(len_NBList)
                self.NBList.pop(len_NBList)
                len_NBList = len(self.NBList)

            for n in range(1, d4):
                for l in alli[3 + n * d1].split(" "):
                    if len(l) > 0:
                        self.NBIList.append(l)
                self.NBIList.pop(len_NBIList)
                self.NBIList.pop(len_NBIList)
                len_NBIList = len(self.NBIList)

            p = 0
            k = 0
            m = 0

            for i in alli[5:d1 - 1]:
                if len(i.split("\t")) == inum_i:
                    j2 = i.split("\t")
                    j2.pop(0)
                    j2.pop(0)
                    j2.pop()
                    if d3 == 0:  # not in trans
                        j2.pop()

                    for l in range(1, d4):
                        j3 = alli[5 + l * d1 + k].split("\t")
                        j3.pop(0)
                        j3.pop(0)
                        if d3 == 0:
                            j3.pop()  # not required for dc
                        j3.pop()
                        j2 = j2 + j3

                    full_data.append(j2)

                k += 1

            for i in allv[5:d1 - 1]:
                if len(i.split("\t")) == inum:
                    j = i.split("\t")
                    j.pop()
                    if d3 == 0:
                        j.pop()
                    for l in range(1, d2):
                        j1 = allv[5 + l * d1 + p].split("\t")
                        j1.pop(0)
                        j1.pop(0)
                        if d3 == 0:
                            j1.pop()  # not required for dc
                        if self.NBList[len(self.NBList) - 1] == 'v-sweep':
                            self.NBList.pop()
                            j1.pop()

                        j1.pop()
                        j = j + j1
                    j = j + full_data[m]
                    m += 1

                    j = "\t".join(j[1:])
                    j = j.replace(",", "")
                    ivals.append(j)

                p += 1

            self.data = ivals

        self.volts_length = len(self.NBList)
        self.NBList = self.NBList + self.NBIList

        print(dec)
        return dec

    def numVals(self):
        a = self.volts_length        # No of voltage nodes
        b = len(self.data[0].split("\t"))
        return [b, a]

    def computeAxes(self):
        nums = len(self.data[0].split("\t"))
        self.y = []
        var = self.data[0].split("\t")
        for i in range(1, nums):
            self.y.append([Decimal(var[i])])
        for i in self.data[1:]:
            temp = i.split("\t")
            for j in range(1, nums):
                self.y[j - 1].append(Decimal(temp[j]))
        for i in self.data:
            temp = i.split("\t")
            self.x.append(Decimal(temp[0]))
