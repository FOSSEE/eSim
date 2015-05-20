from __future__ import division         # Used for decimal division eg 2/3=0.66 and not '0' 6/2=3.0 and 6//2=3
from PyQt4 import QtGui, QtCore
from decimal import Decimal
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure
import tkMessageBox


class plotWindow(QtGui.QMainWindow):
    def __init__(self,fpath,projectName):
        QtGui.QMainWindow.__init__(self)
        self.fpath = fpath
        self.projName = projectName
        self.createMainFrame()
        self.combo = []
        self.combo1 = []
        self.combo1_rev = []
        
    def createMainFrame(self):
        self.main_frame = QtGui.QWidget()
        self.dpi = 100
        #Creating Figure Canvas
        self.fig = Figure((7.0, 7.0), dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)
        self.canvas.setSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
        self.canvas.updateGeometry()
        
        self.axes = self.fig.add_subplot(111)
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)
    
        left_vbox = QtGui.QVBoxLayout()
        left_vbox.addWidget(self.mpl_toolbar)
        left_vbox.addWidget(self.canvas)

        right_vbox = QtGui.QVBoxLayout()
        right_grid = QtGui.QGridLayout()
        top_grid = QtGui.QGridLayout()
        
        ##Processing data file to extract data in proper format
        self.fobj = File_data()
        plot_type = self.fobj.openFile(self.fpath)
        print "Plot Type :",plot_type
        self.fobj.computeAxes()
        self.chkbox=[]
        self.a = self.fobj.numVals()

        print "A :",self.a
        
        ########### Generating list of colours :
        self.full_colors = ['r','b','g','y','c','m','k']#,(0.4,0.5,0.2),(0.1,0.4,0.9),(0.4,0.9,0.2),(0.9,0.4,0.9)]
        self.color = []
        for i in range(0,self.a[0]-1):
            if i%7 == 0:
                self.color.append(self.full_colors[0])
            elif (i-1)%7 == 0:
                self.color.append(self.full_colors[1])
            elif (i-2)%7 == 0:
                self.color.append(self.full_colors[2])
            elif (i-3)%7 == 0:
                self.color.append(self.full_colors[3])
            elif (i-4)%7 == 0:
                self.color.append(self.full_colors[4])
            elif (i-5)%7 == 0:
                self.color.append(self.full_colors[5])
            elif (i-6)%7 == 0:
                self.color.append(self.full_colors[6])

        ###########
                
        self.volts_length = self.a[1]
        #print "I'm Volts length:",self.volts_length
        self.heading1 = QtGui.QLabel()
        top_grid.addWidget(self.heading1,1,0)
        self.heading2 = QtGui.QLabel()
        top_grid.addWidget(self.heading2,self.a[1]+2,0)
        for i in range(0,self.a[1]):#a[0]-1
            self.chkbox.append(QtGui.QCheckBox(self.fobj.butnames[i]))
            self.chkbox[i].setToolTip('<b>Tick Me!</b>' )
            top_grid.addWidget(self.chkbox[i],i+2,0)

        for i in range(self.a[1],self.a[0]-1):#a[0]-1
            self.chkbox.append(QtGui.QCheckBox(self.fobj.butnames[i]))
            self.chkbox[i].setToolTip('<b>Tick Me!</b>' )
            top_grid.addWidget(self.chkbox[i],i+3,0)
    
        self.clear = QtGui.QPushButton("Clear")
        self.Note = QtGui.QLabel()
        self.Note1 = QtGui.QLabel()
        self.Note2 = QtGui.QLabel()
    
        self.btn = QtGui.QPushButton("Plot")
        self.btn.setToolTip('<b>Press</b> to Plot' )
        self.text = QtGui.QLineEdit()
        self.funcLabel = QtGui.QLabel()
        self.palette1 = QtGui.QPalette()
        self.palette2 = QtGui.QPalette()
        self.btn1 = QtGui.QPushButton("Plot Function")
        self.btn1.setToolTip('<b>Press</b> to Plot the function' )

        self.palette1.setColor(QtGui.QPalette.Foreground,QtCore.Qt.blue)
        self.palette2.setColor(QtGui.QPalette.Foreground,QtCore.Qt.red)
        self.Note1.setPalette(self.palette1)
        self.Note2.setPalette(self.palette2)

        right_vbox.addLayout(top_grid)
        right_vbox.addWidget(self.btn)
    
        right_grid.addWidget(self.funcLabel,1,0)
        right_grid.addWidget(self.text,1,1)
        right_grid.addWidget(self.btn1,2,1)    
        right_grid.addWidget(self.clear,2,0)
        right_grid.addWidget(self.Note,3,0)
        right_grid.addWidget(self.Note1,4,0)
        right_grid.addWidget(self.Note2,4,1)
    
        right_vbox.addLayout(right_grid)
        hbox = QtGui.QHBoxLayout()
        hbox.addLayout(left_vbox)
        hbox.addLayout(right_vbox)

        widget = QtGui.QWidget()
        widget.setLayout(hbox)#finalvbox
        self.scrollArea = QtGui.QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(widget)

        finalhbox = QtGui.QHBoxLayout()
        finalhbox.addWidget(self.scrollArea)
        self.main_frame.setLayout(finalhbox)

        self.showMaximized()
    
        self.heading1.setText("<font color='indigo'>List of Nodes:</font>")

        self.heading2.setText("<font color='indigo'>List of Branches:</font>")    

        self.funcLabel.setText("<font color='indigo'>Function:</font>")
    
        self.Note1.setText("<font color='indigo'>Examples:</font>\
        <br><br>Addition:<br>Subtraction:<br>Multiplication:<br>Division:<br>Comparison:")

        self.Note2.setText("\n\n"+self.fobj.butnames[0]+" + "+self.fobj.butnames[1]+"\n"+self.fobj.butnames[0]+" - "+self.fobj.butnames[1]+ \
                           "\n"+self.fobj.butnames[0]+" * "+self.fobj.butnames[1]+"\n"+self.fobj.butnames[0]+" / "+self.fobj.butnames[1]+ \
                           "\n"+self.fobj.butnames[0]+" vs "+self.fobj.butnames[1])
    

        self.connect(self.clear,QtCore.SIGNAL('clicked()'),self.pushedClear)

        self.connect(self.btn1,QtCore.SIGNAL('clicked()'), self.pushedPlotFunc)

        if plot_type[0]==0:
            self.setWindowTitle('AC Analysis')
            if plot_type[1]==1:
                self.connect(self.btn,QtCore.SIGNAL('clicked()'), self.onPush_decade)
            else:
                self.connect(self.btn,QtCore.SIGNAL('clicked()'), self.onPush_ac)

        elif plot_type[0]==1:

            self.setWindowTitle('Transient Analysis')
            self.connect(self.btn,QtCore.SIGNAL('clicked()'), self.onPush_trans)
        else:
            self.setWindowTitle('DC Analysis')
            self.connect(self.btn,QtCore.SIGNAL('clicked()'), self.onPush_dc)
        
        self.setCentralWidget(self.main_frame)    
    

    def pushedPlotFunc(self):
        self.parts = str(self.text.text())
        self.parts = self.parts.split(" ")
        #print self.parts
        if self.parts[len(self.parts)-1] == '':
            self.parts = self.parts[0:-1]
        #print self.parts
        self.values = self.parts
        self.comboAll = []
        self.axes.cla()
        plot_type2 = self.fobj.openFile(self.fpath)

        if len(self.parts) <= 2:
            self.Note.setText("Too few arguments!\nRefer syntax below!")
            QtGui.QMessageBox.about(self, "Warning!!", "Too Few Arguments/SYNTAX Error!\n Refer Examples")
        else:
            self.Note.setText("")

        a = []
        finalResult  = []
        p = 0
        #print "values:",self.values
        #print "parts:",self.parts

        for i in range(len(self.parts)):
            #print "hello"
            if i%2 == 0:
                #print "I'm in:"
                for j in range(len(self.fobj.butnames)):
                    if self.parts[i]==self.fobj.butnames[j]:
                        #print "I got you:",i
                        a.append(j)

        #print "positions",a

        if len(a) != len(self.parts)//2 + 1:
            QtGui.QMessageBox.about(self, "Warning!!", "One of the operands doesn't belong to the above list!!")        

        for i in a:
            self.comboAll.append(self.fobj.y[i])

        #print self.comboAll        

        for i in range(len(a)):
            if a[i] == len(self.fobj.butnames):
                QtGui.QMessageBox.about(self, "Warning!!", "One of the operands doesn't belong to the above list!!")
                self.Note.setText("<font color='red'>To Err Is Human!<br>One of the operands doesn't belong to the above list!!</font>")

        if self.parts[1] == 'vs':
            if len(self.parts) > 3:
                self.Note.setText("Enter two operands only!!")
                QtGui.QMessageBox.about(self, "Warning!!", "Re-check the expression syntax!")
            else:
                self.axes.cla()
                #print "plotting wait"
                for i in range(len(self.fobj.y[a[0]])):
                    self.combo.append(self.fobj.y[a[0]][i]) 
                    self.combo1.append(self.fobj.y[a[1]][i])
            
                '''for i in reversed(self.combo1):
                    self.combo1_rev.append(i)'''     
                #print self.combo
                #print "\ncombo1_rev\n",self.combo1_rev
                self.axes.plot(self.combo,self.combo1,c=self.color[1],label=str(2))#_rev
                if max(a) < self.volts_length:
                    self.axes.set_ylabel('Voltage(V)-->')
                    self.axes.set_xlabel('Voltage(V)-->')
                else:
                    self.axes.set_ylabel('Current(I)-->')
                    self.axes.set_ylabel('Current(I)-->')        


        elif max(a) >= self.volts_length and min(a) < self.volts_length:
            QtGui.QMessageBox.about(self, "Warning!!", "Do not combine Voltage and Current!!")

        else:

            for j in range(len(self.comboAll[0])):
                for i in range(len(self.values)):
                    if i%2==0:
                        self.values[i] = str(self.comboAll[i//2][j])
                        re = " ".join(self.values[:])
                    #print re
            try:
                finalResult.append(eval(re))
            except ArithmeticError:
                QtGui.QMessageBox.about(self, "Warning!!", "Dividing by zero!!")
        ############################################
            if plot_type2[0]==0:
                self.setWindowTitle('AC Analysis')
                if plot_type2[1]==1:
                    self.axes.semilogx(self.fobj.x,finalResult,c=self.color[0],label=str(1))
        
                else:
    
                    self.axes.plot(self.fobj.x,finalResult,c=self.color[0],label=str(1))        
                self.axes.set_xlabel('freq-->')
                if max(a) < self.volts_length:
                    self.axes.set_ylabel('Voltage(V)-->')
                else:
                    self.axes.set_ylabel('Current(I)-->')        


            elif plot_type2[0]==1:
                self.setWindowTitle('Transient Analysis')
                self.axes.plot(self.fobj.x,finalResult,c=self.color[0],label=str(1))    
                self.axes.set_xlabel('time-->')
                if max(a) < self.volts_length:
                    self.axes.set_ylabel('Voltage(V)-->')
                else:
                    self.axes.set_ylabel('Current(I)-->')        
    

            else:

                self.setWindowTitle('DC Analysis')
                self.axes.plot(self.fobj.x,finalResult,c=self.color[0],label=str(1))
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
        #print "succes:",self.parts

    def pushedClear(self):

        self.text.clear()
        self.axes.cla()
        self.canvas.draw()
        QtCore.SLOT('quit()')

    def onPush_ac(self):
        self.axes.cla()
        boxCheck = 0
        for i,j in zip(self.chkbox,range(len(self.chkbox))):
            if i.isChecked():
                boxCheck += 1
                self.axes.plot(self.fobj.x,self.fobj.y[j],c=self.color[j],label=str(j+1))
                self.axes.set_xlabel('freq-->')
                if j < self.volts_length:
                    self.axes.set_ylabel('Voltage(V)-->')
                else:
                    self.axes.set_ylabel('Current(I)-->')
                self.axes.grid(True)
        if boxCheck == 0:
            QtGui.QMessageBox.about(self, "Warning!!","Please select atleast one Node OR Branch")
        self.canvas.draw()
                     

    def onPush_decade(self):
        boxCheck = 0
        self.axes.cla()

        for i,j in zip(self.chkbox,range(len(self.chkbox))):
            if i.isChecked():
                boxCheck += 1
                self.axes.semilogx(self.fobj.x,self.fobj.y[j],c=self.color[j],label=str(j+1))
                if j < self.volts_length:
                    self.axes.set_ylabel('Voltage(V)-->')
                else:
                    self.axes.set_ylabel('Current(I)-->')
                self.axes.set_xlabel('freq-->')
                self.axes.grid(True)
        if boxCheck == 0:
            QtGui.QMessageBox.about(self, "Warning!!","Please select atleast one Node OR Branch")        
        self.canvas.draw()

    def onPush_trans(self):
        boxCheck = 0
        self.axes.cla()
        for i,j in zip(self.chkbox,range(len(self.chkbox))):
            if i.isChecked():
                boxCheck += 1
                #print self.fobj.y[j]
                self.axes.plot(self.fobj.x,self.fobj.y[j],c=self.color[j],label=str(j+1))
                self.axes.set_xlabel('time-->')

            if j < self.volts_length:
                self.axes.set_ylabel('Voltage(V)-->')

            else:
                self.axes.set_ylabel('Current(I)-->')
            self.axes.grid(True)
        if boxCheck == 0:
            QtGui.QMessageBox.about(self,"Warning!!", "Please select atleast one Node OR Branch")
        self.canvas.draw()

    def onPush_dc(self):
        boxCheck = 0
        self.axes.cla()    
        for i,j in zip(self.chkbox,range(len(self.chkbox))):
            if i.isChecked():
                boxCheck += 1
                self.axes.plot(self.fobj.x,self.fobj.y[j],c=self.color[j],label=str(j+1))
                self.axes.set_xlabel('Voltage Sweep(V)-->')

            if j < self.volts_length:
                self.axes.set_ylabel('Voltage(V)-->')
            else:
                self.axes.set_ylabel('Current(I)-->')
            self.axes.grid(True)
        if boxCheck == 0:
            QtGui.QMessageBox.about(self,"Warning!!", "Please select atleast one Node OR Branch")
        self.canvas.draw() 
        
class File_data:
    def __init__(self,parent=None):
        self.data=[]        #consists of all the columns of data belonging to nodes and branches
        self.y=[]        #stores y-axis data
        self.x=[]        #stores x-axis data

    def numberFinder(self,fpath):
        """
        New function for finding no of points to be plotted
        """
        with open (fpath+"/analysis") as f3:
            info = f3.read()
            
        with open (fpath+"/plot_data_v.txt") as f2:
            ilines = f2.read()
            
        p = l = vnumber = inumber = 0
        ilines = ilines.split("\n")
        
        for i in ilines[3:]:
            if "V(" in i or "x1" in i or "u3" in i:    #it has possible names of voltage nodes in ngspice
                vnumber+=1    
                
        # for finding no of branches:
        with open (fpath+"/plot_data_i.txt") as f2:
            current = f2.read()
        
        current = current.split("\n")
        
        for i in current[3:]:
            if "#branch" in i:
                inumber+=1    
                #print "current no:",inumber
    
        dec = 0 
        
        # For AC:
        if info[0][-3:]==".ac":
            if "dec" in info:
                dec = 1

            for i in ilines[3:]:
                p+=1            #'p' gives no. of lines of data for each node/branch 
                if "Index" in i:      
                    l+=1        # 'l' gives the no of partitions for a single voltage node
                #print "l:",l
                if "AC" in i:    #DC for dc files and AC for ac ones
                    break
            analysis_type = 0

        elif ".tran" in info:
            analysis_type = 1
            for i in ilines[3:]:
                p+=1
                if "Index" in i:      
                    l+=1        # 'l' gives the no of partitions for a single voltage node
                #print "l:",l
                if "Transient" in i:    #DC for dc files and AC for ac ones
                    break


        # For DC:
        else:
            for i in ilines[3:]:
                p+=1
                if "Index" in i:      
                    l+=1        # 'l' gives the no of partitions for a single voltage node
                #print "l:",l
                if "DC" in i:    #DC for dc files and AC for ac ones
                    break
            analysis_type = 2
            
        #if ac!=1:
        vnumber = vnumber//l        #vnumber gives the no of voltage nodes
        inumber  = inumber//l        #inumber gives the no of branches
        #print "i'm p:",p
        p=[p,vnumber,analysis_type,dec,inumber]
        #print p
        return p
    
    
    def openFile(self,fpath):
        # For Current:
        try:
            with open (fpath+"/plot_data_i.txt") as f2:       #Checking whether the files Plot_data_i.txt
                I = f2.read()                    #  and plot_data_v.txt are present or not
            I = I.split("\n")
            self.butnamesi = []

            with open (fpath+"/plot_data_v.txt") as f1:
                idata = f1.read()

        except Exception as e:
            tkMessageBox.showinfo("Warning!!", "Click on KI->Ng button before simulation ")
            print "Excpetion MSG :",str(e)
            #exit(1)
    
        try:
            for l in I[3].split(" "):
                if len(l)>0:
                    self.butnamesi.append(l)
            self.butnamesi=self.butnamesi[2:]
            len_bnamesi = len(self.butnamesi)
            #print "length_new",len_bnamesi
            #print self.butnamesi
        except:
            tkMessageBox.showinfo("Warning!!", "Error in Analysis File")    
            
   
        d = self.numberFinder(fpath)
        d1 = int(d[0] + 1)
        #print "I'm D1:", d1  #for debugging
        d2 = int(d[1])
        d3 = d[2]
        d4 = d[4]
        #print "I'm D4:", d4  #for debugging
        dec = [d3,d[3]]
        #print "No. of Nodes:", d2
        self.butnames=[]
        idata=idata.split("\n")
        
        for l in idata[3].split(" "):
            if len(l)>0:
                self.butnames.append(l)
        self.butnames=self.butnames[2:]
        len_bnames = len(self.butnames)
        #print len_bnames
        #print self.butnames

        ivals=[]
        inum = len(idata[5].split("\t"))
        inum_i = len(I[5].split("\t"))
        #print inum
    
        full_data = []
        
        # Creating list of data:
        if d3 < 3 :
            for i in range(1,d2):
                for l in idata[3+i*d1].split(" "):
                    if len(l)>0:
                        self.butnames.append(l)
                self.butnames.pop(len_bnames)
                self.butnames.pop(len_bnames)
                len_bnames = len(self.butnames)
                #print "volts:",self.butnames

            for n in range(1,d4):
                for l in I[3+n*d1].split(" "):
                    if len(l)>0:
                        self.butnamesi.append(l)
                #print "names:",self.butnamesi
                self.butnamesi.pop(len_bnamesi)
                self.butnamesi.pop(len_bnamesi)
                len_bnamesi = len(self.butnamesi)
                #print "current",self.butnamesi
            
            p=0
            k = 0
            m=0

            for i in I[5:d1-1]:
                #print "hello:"
                if len(i.split("\t"))==inum_i:
                    j2=i.split("\t")
                    #print j2
                    j2.pop(0)
                    j2.pop(0)
                    j2.pop()
                    if d3 == 0:       #not in trans
                        j2.pop()
                    #print j2

                    for l in range(1,d4):
                        j3 = I[5+l*d1+k].split("\t")
                        j3.pop(0)
                        j3.pop(0)
                        if d3==0:
                            j3.pop()     #not required for dc
                            j3.pop()
                            j2 = j2 + j3
                            #print j2
                    full_data.append(j2)
                k+=1
                #print full_data        
        

            for i in idata[5:d1-1]:
                if len(i.split("\t"))==inum:
                    j=i.split("\t")
                    j.pop()
                    if d3==0:
                        j.pop()

                    for l in range(1,d2):
                        j1 = idata[5+l*d1+p].split("\t")
                        j1.pop(0)
                        j1.pop(0)
                        if d3==0:
                            j1.pop()     #not required for dc
                        if self.butnames[len(self.butnames)-1] == 'v-sweep':
                            self.butnames.pop()
                            j1.pop()
                        #if l==d2-1 and d3==2:
                            #j1.pop()
                        j1.pop()
                        j = j + j1 
                    #self.volts_length = len(j)-2        
                    j = j + full_data[m]
                    #print j
                    m+=1
                    #print j[:20]            
                    j = "\t".join(j[1:])
                    j = j.replace(",","")
                    ivals.append(j)

                p+=1

            self.data = ivals
            #print self.data

        #print "volts:",self.butnames
        self.volts_length = len(self.butnames)
        #print "volts_length:",self.volts_length
        self.butnames = self.butnames + self.butnamesi
        #print "new butnames:",self.butnames 
    
        #print self.data    
        return dec


    def numVals(self):
        a = self.volts_length        # No of voltage nodes
        b = len(self.data[0].split("\t"))
        #print "numvals:",b
        return [b,a]
    
    def computeAxes(self):
        nums = len(self.data[0].split("\t"))
        #print "i'm nums:",nums
        self.y=[]
        var=self.data[0].split("\t")
        for i in range(1,nums):
            self.y.append([Decimal(var[i])])
        #print self.y
        #print y,nums
        for i in self.data[1:]:
            temp=i.split("\t")
            for j in range(1,nums):
                self.y[j-1].append(Decimal(temp[j]))
        #print len(self.y)
        #print self.y[3]

        for i in self.data:
            temp=i.split("\t")
            self.x.append(Decimal(temp[0]))
"""
app = QtGui.QApplication(sys.argv)
main = plotWindow()
main.show()
sys.exit(app.exec_())
"""