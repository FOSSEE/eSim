import os
import glob
import traceback
from PyQt5 import QtWidgets, QtCore
from configuration.Appconfig import Appconfig
from projManagement import Worker
from projManagement.Validation import Validation
from .NgspicetoModelica import NgMoConverter

BROWSE_LOCATION = '/home'


class OpenModelicaEditor(QtWidgets.QWidget):

    def __init__(self, dir=None):
        QtWidgets.QWidget.__init__(self)
        self.obj_validation = Validation()
        self.obj_appconfig = Appconfig()
        self.projDir = dir
        self.projName = os.path.basename(self.projDir)
        self.ngspiceNetlist = os.path.join(
            self.projDir, self.projName + ".cir.out")
        self.modelicaNetlist = os.path.join(self.projDir, "*.mo")
        self.map_json = Appconfig.modelica_map_json

        self.grid = QtWidgets.QGridLayout()
        self.FileEdit = QtWidgets.QLineEdit()
        self.FileEdit.setText(self.ngspiceNetlist)
        self.grid.addWidget(self.FileEdit, 0, 0)

        self.browsebtn = QtWidgets.QPushButton("Browse Netlist (*.cir.out)")
        self.browsebtn.clicked.connect(self.browseFile)
        self.grid.addWidget(self.browsebtn, 0, 1)

        self.convertbtn = QtWidgets.QPushButton("Convert")
        self.convertbtn.clicked.connect(self.callConverter)
        self.grid.addWidget(self.convertbtn, 2, 1)

        self.loadOMbtn = QtWidgets.QPushButton("Load OMEdit")
        self.loadOMbtn.clicked.connect(self.callOMEdit)
        self.grid.addWidget(self.loadOMbtn, 3, 1)

        self.OMPathtext = QtWidgets.QLineEdit()
        self.OMPathtext.setText("")
        self.grid.addWidget(self.OMPathtext, 4, 0)

        self.OMPathbrowsebtn = QtWidgets.QPushButton("Browse OM")
        self.OMPathbrowsebtn.clicked.connect(self.OMPathbrowseFile)
        self.grid.addWidget(self.OMPathbrowsebtn, 4, 1)

        # self.setGeometry(300, 300, 350, 300)
        self.setLayout(self.grid)
        self.show()

    def OMPathbrowseFile(self):
        temp = QtCore.QDir.toNativeSeparators(
            QtWidgets.QFileDialog.getExistingDirectory(
                self, "Open OpenModelica Directory", "home"
            )
        )

        if temp:
            self.OMPath = temp
            self.OMPathtext.setText(self.OMPath)

    def browseFile(self):
        temp = QtCore.QDir.toNativeSeparators(
            QtWidgets.QFileDialog.getOpenFileName(
                self, 'Open Ngspice Netlist', BROWSE_LOCATION
            )[0]
        )

        if temp:
            self.ngspiceNetlist = temp
            self.FileEdit.setText(self.ngspiceNetlist)

    def callConverter(self):

        dir_name = os.path.dirname(os.path.realpath(self.ngspiceNetlist))
        # file_basename = os.path.basename(self.ngspiceNetlist)

        cwd = os.getcwd()
        os.chdir(dir_name)

        obj_NgMoConverter = NgMoConverter(self.map_json)

        try:
            # Getting all the require information
            lines = obj_NgMoConverter.readNetlist(self.ngspiceNetlist)
            # print("Complete Lines of Ngspice netlist : " +
            # "lines ---------------->", lines)
            optionInfo, schematicInfo = \
                obj_NgMoConverter.separateNetlistInfo(lines)
            # print("All option details like analysis,subckt,.ic,.model  :" +
            # "OptionInfo------------------->", optionInfo)
            # print("Schematic connection info :schematicInfo", schematicInfo)
            modelName, modelInfo, subcktName, paramInfo, transInfo,\
                inbuiltModelDict = (
                    obj_NgMoConverter.addModel(optionInfo)
                )
            # print("Name of Model : " +
            # "modelName-------------------->", modelName)
            # print("Model Information : " +
            # "modelInfo--------------------->", modelInfo)
            # print("Subcircuit Name : " +
            # "subcktName------------------------>", subcktName)
            # print("Parameter Information : " +
            # "paramInfo---------------------->", paramInfo)
            # print("InBuilt Model ---------------------->", inbuiltModelDict)

            modelicaParamInit = obj_NgMoConverter.processParam(paramInfo)
            # print("Make modelicaParamInit from paramInfo : " +
            # "processParamInit------------->", modelicaParamInit)
            compInfo, plotInfo = obj_NgMoConverter.separatePlot(schematicInfo)
            # print("Plot info like plot,print etc :plotInfo",plotInfo)
            IfMOS = '0'

            for eachline in compInfo:
                # words = eachline.split()
                if eachline[0] == 'm':
                    IfMOS = '1'
                    break

            node, nodeDic, pinInit, pinProtectedInit = \
                obj_NgMoConverter.nodeSeparate(
                    compInfo, '0', [], subcktName, []
                )
            # print("All nodes in the netlist :node---------------->", node)
            # print("NodeDic which will be used for modelica :" +
            # "nodeDic------------->", nodeDic)
            # print("PinInit-------------->", pinInit)
            # print("pinProtectedInit----------->", pinProtectedInit)

            modelicaCompInit, numNodesSub = obj_NgMoConverter.compInit(
                compInfo,
                node,
                modelInfo,
                subcktName,
                dir_name,
                transInfo,
                inbuiltModelDict
            )
            # print("ModelicaComponents :" +
            # "modelicaCompInit----------->", modelicaCompInit)
            # print("SubcktNumNodes :" +
            # "numNodesSub---------------->", numNodesSub)

            connInfo = obj_NgMoConverter.connectInfo(
                compInfo, node, nodeDic, numNodesSub, subcktName)

            # print("ConnInfo------------------>", connInfo)

            # After Sub Ckt Func
            if len(subcktName) > 0:
                data, subOptionInfo, subSchemInfo, subModel, subModelInfo,\
                    subsubName, subParamInfo, modelicaSubCompInit,\
                    modelicaSubParam, nodeSubInterface, nodeSub, nodeDicSub,\
                    pinInitSub, connSubInfo = (
                        obj_NgMoConverter.procesSubckt(
                            subcktName, numNodesSub, dir_name
                        )
                    )  # Adding 'numNodesSub' by Fahim

            # Creating Final Output file
            fileDir = os.path.dirname(self.ngspiceNetlist)
            newfile = os.path.basename(self.ngspiceNetlist)
            newfilename = os.path.join(fileDir, newfile.split('.')[0])
            outfile = newfilename + ".mo"

            out = open(outfile, "w")
            out.writelines('model ' + os.path.basename(newfilename))
            out.writelines('\n')
            if IfMOS == '0':
                out.writelines('import Modelica.Electrical.*;')
            elif IfMOS == '1':
                out.writelines('import BondLib.Electrical.*;')
                # out.writelines('import Modelica.Electrical.*;')
            out.writelines('\n')

            for eachline in modelicaParamInit:
                if len(paramInfo) == 0:
                    continue
                else:
                    out.writelines(eachline)
                    out.writelines('\n')
            for eachline in modelicaCompInit:
                if len(compInfo) == 0:
                    continue
                else:
                    out.writelines(eachline)
                    out.writelines('\n')

            out.writelines('protected')
            out.writelines('\n')
            out.writelines(pinInit)
            out.writelines('\n')
            out.writelines('equation')
            out.writelines('\n')

            for eachline in connInfo:
                if len(connInfo) == 0:
                    continue
                else:
                    out.writelines(eachline)
                    out.writelines('\n')

            out.writelines('end ' + os.path.basename(newfilename) + ';')
            out.writelines('\n')

            out.close()

            os.chdir(cwd)

            self.msg = QtWidgets.QMessageBox()
            self.msg.setText(
                "Ngspice netlist successfully converted to OpenModelica " +
                "netlist"
            )
            self.obj_appconfig.print_info(
                "Ngspice netlist successfully converted to OpenModelica " +
                "netlist"
            )
            self.msg.exec_()

        except BaseException as e:
            traceback.print_exc()
            print("================")
            self.msg = QtWidgets.QErrorMessage()
            self.msg.setModal(True)
            self.msg.setWindowTitle("Conversion Error")
            self.msg.showMessage(
                'Unable to convert Ngspice netlist to Modelica netlist. ' +
                'Check the netlist : ' + repr(e)
            )

    def callOMEdit(self):

        try:
            modelFiles = glob.glob(self.modelicaNetlist)
            modelFiles = ' '.join(file for file in modelFiles)
            self.cmd2 = self.OMPath+"/OMEdit " + modelFiles
            print(self.cmd2)
            self.obj_workThread2 = Worker.WorkerThread(self.cmd2)
            self.obj_workThread2.start()
            print("OMEdit called")
            self.obj_appconfig.print_info("OMEdit called")

        except BaseException:
            self.msg = QtWidgets.QMessageBox()
            self.msgContent = (
                "There was an error while opening OMEdit.<br/>"
                "Please make sure OpenModelica is installed in your"
                " system.<br/>"
                "To install it on Linux : Go to <a href="
                "https://www.openmodelica.org/download/download-linux"
                ">OpenModelica Linux</a> and install nightly build"
                " release.<br/>"
                "To install it on Windows : Go to <a href="
                "https://www.openmodelica.org/download/download-windows"
                ">OpenModelica Windows</a> and install latest version.<br/>"
                )
            self.msg.setTextFormat(QtCore.Qt.RichText)
            self.msg.setText(self.msgContent)
            self.msg.setWindowTitle("Missing OpenModelica")
            self.obj_appconfig.print_info(self.msgContent)
            self.msg.exec_()
