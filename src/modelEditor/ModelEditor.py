from PyQt4 import QtGui, QtCore
from PyQt4.Qt import QTableWidgetItem
import xml.etree.ElementTree as ET
from configuration.Appconfig import Appconfig
import os


class ModelEditorclass(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.savepathtest = '../deviceModelLibrary'
        self.obj_appconfig = Appconfig()
        self.newflag=0
        self.layout = QtGui.QVBoxLayout()
        self.splitter= QtGui.QSplitter()
        self.grid= QtGui.QGridLayout()
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        
        self.modeltable = QtGui.QTableWidget()

        self.newbtn = QtGui.QPushButton('New')
        self.newbtn.clicked.connect(self.opennew)
        self.editbtn = QtGui.QPushButton('Edit')
        self.editbtn.clicked.connect(self.openedit)
        self.savebtn = QtGui.QPushButton('Save')
        self.savebtn.setDisabled(True)
        self.savebtn.clicked.connect(self.savemodelfile)
        self.removebtn = QtGui.QPushButton('Remove')
        self.removebtn.setHidden(True)
        self.removebtn.clicked.connect(self.removeparameter)
        self.addbtn = QtGui.QPushButton('Add')
        self.addbtn.setHidden(True)
        self.addbtn.clicked.connect(self.addparameters)
        self.uploadbtn = QtGui.QPushButton('Upload')
        self.uploadbtn.clicked.connect(self.converttoxml)
        self.grid.addWidget(self.newbtn, 1,2)
        self.grid.addWidget(self.editbtn, 1,3)
        self.grid.addWidget(self.savebtn, 1,4)
        self.grid.addWidget(self.uploadbtn, 1,5)
        self.grid.addWidget(self.removebtn, 8,4)
        self.grid.addWidget(self.addbtn, 5,4)
    
        self.radiobtnbox = QtGui.QButtonGroup()
        self.diode = QtGui.QRadioButton('Diode')
        self.diode.setDisabled(True)
        self.bjt = QtGui.QRadioButton('BJT')
        self.bjt.setDisabled(True)
        self.mos = QtGui.QRadioButton('MOS')
        self.mos.setDisabled(True)
        self.jfet = QtGui.QRadioButton('JFET')
        self.jfet.setDisabled(True)
        self.igbt = QtGui.QRadioButton('IGBT')
        self.igbt.setDisabled(True)
        self.magnetic = QtGui.QRadioButton('Magnetic Core')
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
        
        self.types= QtGui.QComboBox()
        self.types.setHidden(True)
          
        self.grid.addWidget(self.types,2,2,2,3)
        self.grid.addWidget(self.diode, 3,1)
        self.grid.addWidget(self.bjt,4,1)
        self.grid.addWidget(self.mos,5,1)
        self.grid.addWidget(self.jfet,6,1)
        self.grid.addWidget(self.igbt,7,1)
        self.grid.addWidget(self.magnetic,8,1)
        self.setLayout(self.grid)
        self.show()
    
    '''To create New Model file '''
    def opennew(self):
        self.addbtn.setHidden(True)
        try:
            self.modeltable.setHidden(True)
        except:
            pass
        os.chdir(self.savepathtest)
        text, ok = QtGui.QInputDialog.getText(self, 'New Model','Enter Model Name:')
        if ok:
            self.newflag=1
            self.diode.setDisabled(False)
            self.bjt.setDisabled(False)
            self.mos.setDisabled(False)
            self.jfet.setDisabled(False)
            self.igbt.setDisabled(False)
            self.magnetic.setDisabled(False)
            self.modelname = (str(text))
        else:
            pass
        
        self.validation(text)
            
    def diode_click(self):
        self.openfiletype('Diode')
        self.types.setHidden(True)
        '''
        self.types.clear()
        self.types.addItem('Diode')
        filetype = str(self.types.currentText())
        self.types.activated[str].connect(self.setfiletype)
    '''
    def bjt_click(self):
        self.types.setHidden(False)
        self.types.clear()
        self.types.addItem('NPN')
        self.types.addItem('PNP')
        filetype = str(self.types.currentText())
        self.openfiletype(filetype)
        self.types.activated[str].connect(self.setfiletype)

    def mos_click(self):
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
        self.types.setHidden(False)
        self.types.clear()
        self.types.addItem('N-JFET')
        self.types.addItem('P-JFET')
        filetype = str(self.types.currentText())
        self.openfiletype(filetype)
        self.types.activated[str].connect(self.setfiletype)
        
    def igbt_click(self):
        self.types.setHidden(False)
        self.types.clear()
        self.types.addItem('N-IGBT')
        self.types.addItem('P-IGBT')
        filetype = str(self.types.currentText())
        self.openfiletype(filetype)
        self.types.activated[str].connect(self.setfiletype)
        
    def magnetic_click(self):
        self.openfiletype('Magnetic Core')
        self.types.setHidden(True)
        '''
        self.types.clear()
        self.types.addItem('Magnetic Core')
        filetype = str(self.types.currentText())
        self.types.activated[str].connect(self.setfiletype)
        '''
    def setfiletype(self,text):
        self.filetype = str(text)
        self.openfiletype(self.filetype)
    
    '''Select the path of the file to be opened depending upon selected file type '''
    def openfiletype(self,filetype):
        self.path = '../deviceModelLibrary/Templates'
        if self.diode.isChecked():
            if filetype == 'Diode':
                path = os.path.join(self.path,'D.xml')
                self.createtable(path)
        if self.bjt.isChecked():
            if filetype == 'NPN':
                path = os.path.join(self.path,'NPN.xml')
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
        else :
            pass
        
    def openedit(self):
        os.chdir(self.savepathtest)
        self.newflag=0
        self.addbtn.setHidden(True)
        self.types.setHidden(True)
        self.diode.setDisabled(True)
        self.mos.setDisabled(True)
        self.jfet.setDisabled(True)
        self.igbt.setDisabled(True)
        self.bjt.setDisabled(True)
        self.magnetic.setDisabled(True)
        self.editfile=str(QtGui.QFileDialog.getOpenFileName(self,"Open Library Directory","../deviceModelLibrary","*.lib"))
        self.createtable(self.editfile)
        
    '''Creates the model table by parsing th .xml file '''
    def createtable(self, modelfile):
        self.savebtn.setDisabled(False)
        self.addbtn.setHidden(False)
        self.removebtn.setHidden(False)
        self.modelfile = modelfile
        self.modeldict = {}
        self.modeltable = QtGui.QTableWidget()
        self.modeltable.resizeColumnsToContents()
        self.modeltable.setColumnCount(2)
        self.modeltable.resizeRowsToContents()
        self.modeltable.resize(200,200)
        self.grid.addWidget(self.modeltable, 3,2,8,2)
        filepath, filename = os.path.split(self.modelfile)
        print"file selected is",filename
        print filepath
        base, ext= os.path.splitext(filename)      
        print base
        print ext
        self.modelfile = os.path.join(filepath, base+'.xml')
        print"modelfile",self.modelfile
        self.tree = ET.parse(self.modelfile)
        self.root= self.tree.getroot()
        for elem in self.tree.iter(tag='ref_model'):
            self.ref_model = elem.text
        for elem in self.tree.iter(tag='model_name'):
            self.model_name = elem.text
        row=0
        for params in self.tree.findall('param'):
            for paramlist in params:
                self.modeldict[paramlist.tag]= paramlist.text
                row= row+1
        self.modeltable.setRowCount(row)
        count =0
        for tags, values in self.modeldict.items():
            self.modeltable.setItem(count,0, QTableWidgetItem(tags))
            try:
                valueitem = QTableWidgetItem(values)
            except:
                pass
            self.modeltable.setItem(count,1, valueitem)
            count= count +1
        self.modeltable.setHorizontalHeaderLabels(QtCore.QString("Parameters;Values").split(";")) 
        self.modeltable.show()
        self.modeltable.itemChanged.connect(self.edit_modeltable)
        
    def edit_modeltable(self):
        self.savebtn.setDisabled(False)
        try:
            indexitem = self.modeltable.currentItem()
            name = str(indexitem.data(0).toString())
            rowno = indexitem.row()
            para = self.modeltable.item(rowno,0)
            val = str(para.data(0).toString())
            self.modeldict[val]= name
        except:
            pass
        
    ''' new parameters can be added in the table '''
    def addparameters(self):
        text1, ok = QtGui.QInputDialog.getText(self, 'Parameter','Enter Parameter')
        if ok:
            if text1 in self.modeldict.keys():
                self.msg = QtGui.QErrorMessage(self)
                self.msg.showMessage("The paramaeter " + text1 + " is already in the list")
                self.msg.setWindowTitle("Error Message")
                return
            text2, ok = QtGui.QInputDialog.getText(self, 'Value','Enter Value')
            if ok :
                currentRowCount = self.modeltable.rowCount()
                self.modeltable.insertRow(currentRowCount)
                self.modeltable.setItem(currentRowCount, 0, QTableWidgetItem(text1))
                self.modeltable.setItem(currentRowCount, 1, QTableWidgetItem(text2))
                self.modeldict[str(text1)]= str(text2)
            else:
                pass
        else:
            pass
        
        
    def savemodelfile(self):
        if self.newflag== 1:
            self.createXML(self.model_name)
        else:
            self.savethefile(self.editfile)
        
    '''creates an .xml an .lib files from the model table'''  
    def createXML(self,model_name):
        root = ET.Element("library")
        ET.SubElement(root, "model_name").text = model_name
        ET.SubElement(root, "ref_model").text = self.modelname
        param = ET.SubElement(root, "param")
        for tags, text in self.modeldict.items():
            ET.SubElement(param, tags).text = text
        tree = ET.ElementTree(root)
        defaultcwd = os.getcwd()
        self.savepath = '../deviceModelLibrary'
        if self.diode.isChecked():
            savepath = os.path.join(self.savepath, 'Diode')  
            os.chdir(savepath)
            txtfile = open(self.modelname+'.lib', 'w')
            txtfile.write('.MODEL ' + self.modelname +' ' + self.model_name + '(\n' )
            for tags, text in self.modeldict.items():
                txtfile.write('+ ' + tags + '=' + text +'\n')
            txtfile.write(')')
            tree.write(self.modelname +".xml")
            self.obj_appconfig.print_info('New ' + self.modelname + ' ' + self.model_name + ' library created at ' + os.getcwd())
        if self.mos.isChecked():
            savepath = os.path.join(self.savepath, 'MOS')  
            os.chdir(savepath)
            txtfile = open(self.modelname+'.lib', 'w')
            txtfile.write('.MODEL ' + self.modelname +' ' + self.model_name + '(\n' )
            for tags, text in self.modeldict.items():
                txtfile.write('+ ' + tags + '=' + text +'\n')
            txtfile.write(')')
            tree.write(self.modelname +".xml")
            self.obj_appconfig.print_info('New ' + self.modelname + ' ' + self.model_name + ' library created at ' + os.getcwd())
        if self.jfet.isChecked():
            savepath = os.path.join(self.savepath, 'JFET')  
            os.chdir(savepath)
            txtfile = open(self.modelname+'.lib', 'w')
            txtfile.write('.MODEL ' + self.modelname +' ' + self.model_name + '(\n' )
            for tags, text in self.modeldict.items():
                txtfile.write('+ ' + tags + '=' + text +'\n')
            txtfile.write(')')
            tree.write(self.modelname +".xml")
            self.obj_appconfig.print_info('New ' + self.modelname + ' ' + self.model_name + ' library created at ' + os.getcwd())
        if self.igbt.isChecked():
            savepath = os.path.join(self.savepath, 'IGBT')  
            os.chdir(savepath)
            txtfile = open(self.modelname+'.lib', 'w')
            txtfile.write('.MODEL ' + self.modelname +' ' + self.model_name + '(\n' )
            for tags, text in self.modeldict.items():
                txtfile.write('+ ' + tags + '=' + text +'\n')
            txtfile.write(')')
            tree.write(self.modelname +".xml")
            self.obj_appconfig.print_info('New ' + self.modelname + ' ' + self.model_name + ' library created at ' + os.getcwd())
        if self.magnetic.isChecked():
            savepath = os.path.join(self.savepath, 'Misc')  
            os.chdir(savepath)
            txtfile = open(self.modelname+'.lib', 'w')
            txtfile.write('.MODEL ' + self.modelname +' ' + self.model_name + '(\n' )
            for tags, text in self.modeldict.items():
                txtfile.write('+ ' + tags + '=' + text +'\n')
            txtfile.write(')')
            tree.write(self.modelname +".xml")
            self.obj_appconfig.print_info('New ' + self.modelname + ' ' + self.model_name + ' library created at ' + os.getcwd())
        if self.bjt.isChecked():
            savepath = os.path.join(self.savepath, 'Transistor')  
            os.chdir(savepath)
            txtfile = open(self.modelname+'.lib', 'w')
            txtfile.write('.MODEL ' + self.modelname +' ' + self.model_name + '(\n' )
            for tags, text in self.modeldict.items():
                txtfile.write('+ ' + tags + '=' + text +'\n')
            txtfile.write(')')
            tree.write(self.modelname +".xml")
            self.obj_appconfig.print_info('New ' + self.modelname + ' ' + self.model_name + ' library created at ' + os.getcwd())
        txtfile.close()
        os.chdir(defaultcwd)
        
    '''Checks if the file with the name already exists'''
    def validation(self,text):
        newfilename = text+'.xml'
        
        all_dir = [x[0] for x in os.walk(self.savepathtest)]
        for each_dir in all_dir:
            all_files = os.listdir(each_dir)
            if newfilename in all_files:
                self.msg = QtGui.QErrorMessage(self)
                self.msg.showMessage('The file with name ' + text+ ' already exists.')
                self.msg.setWindowTitle("Error Message")

    '''save the editing in the model table '''
    def savethefile(self,editfile):
        
        xmlpath, file = os.path.split(editfile)
        filename = os.path.splitext(file)[0]
        libpath = os.path.join(xmlpath,filename+'.lib')
        libfile = open(libpath, 'w')
        libfile.write('.MODEL ' + self.ref_model +' ' + self.model_name + '(\n' )
        for tags, text in self.modeldict.items():
            libfile.write('+  ' + tags + '=' + text +'\n')
        libfile.write(')')
        libfile.close()
        for params in self.tree.findall('param'):
            self.root.remove(params)
        param = ET.SubElement(self.root,'param') 
        for tags, text in self.modeldict.items():
            ET.SubElement(param, tags).text = text
        self.tree.write(editfile)
        self.obj_appconfig.print_info('Updated library ' + libpath)
        
    def removeparameter(self):
        self.savebtn.setDisabled(False)
        index = self.modeltable.currentIndex()
        param = index.data().toString()
        remove_item = self.modeltable.item(index.row(),0).text()
        self.modeltable.removeRow(index.row())
        del self.modeldict[str(remove_item)]
        
    def converttoxml(self):
        os.chdir(self.savepathtest)
        self.addbtn.setHidden(True)
        self.removebtn.setHidden(True)
        self.modeltable.setHidden(True)
        model_dict = {}
        stringof = []
        self.libfile = str(QtGui.QFileDialog.getOpenFileName(self,"Open Library Directory","../deviceModelLibrary","*.lib"))
        libopen = open(self.libfile)
        filedata = libopen.read().split()
        modelcount=0
        for words in filedata:
            modelcount= modelcount +1
            if words.lower() == '.model':
                print "model found"
                break
        ref_model = filedata[modelcount]
        model_name = filedata[modelcount+1]
        model_name = list(model_name)
        modelnamecnt= 0
        flag= 0
        for chars in model_name:
            modelnamecnt = modelnamecnt +1
            if chars == '(':
                flag = 1
                break
        if flag == 1 :
            model_name = ''.join(model_name[0:modelnamecnt-1])
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
            count = count +1
            if chars == '(':
                break
        count1=0
        for chars in stringof:
            count1 = count1 +1
            if chars == ')':
                break
        stringof = stringof[count:count1-1]
        stopcount=[]
        listofname = [] 
        stopcount.append(0)
        count = 0
        for chars in stringof:
            count = count +1
            if chars == '=':
                stopcount.append(count) 
        stopcount.append(count)
        
        i = 0
        for no in stopcount:
            try:
                listofname.append(''.join(stringof[int(stopcount[i]):int(stopcount[i+1])]))
                i = i +1
            except:
                pass
        listoflist =[]
        listofname2 = [el.replace('\t', '').replace('\n', ' ').replace('+', '').replace(')', '').replace('=', '') for el in listofname]
        listofname=[]
        for item in listofname2:
            listofname.append(item.rstrip().lstrip())
        for values in listofname:
            valuelist = values.split(' ')
            listoflist.append(valuelist)
        for i in range(1, len(listoflist)):
            model_dict[listoflist[0][0]]=listoflist[1][0]
            try:
                model_dict[listoflist[i][-1]]= listoflist[i+1][0]
            except:
                pass
        root = ET.Element("library")
        ET.SubElement(root, "model_name").text = model_name
        ET.SubElement(root, "ref_model").text = ref_model
        param = ET.SubElement(root, "param")
        for tags, text in model_dict.items():
            ET.SubElement(param, tags).text = text
        tree = ET.ElementTree(root)

        defaultcwd = os.getcwd()
        savepath = os.path.join(self.savepathtest, 'User Libraries')  
        savefilepath= os.path.join(savepath, model_name +".xml")
        #self.obj_valid.validateNewproj(savepath)
        #self.reply = self.obj_valid.validateNewproj(savefilepath)
        os.chdir(savepath)
        text, ok1 = QtGui.QInputDialog.getText(self, 'Model Name','Enter Model Library Name')
        if ok1:
            tree.write(text+".xml")
            fileopen = open(text+".lib",'w')
            f = open(self.libfile)
            fileopen.write(f.read())
            f.close()
            fileopen.close()
        os.chdir(defaultcwd)
        libopen.close()
        libopen1.close()