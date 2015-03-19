
from PyQt4 import QtGui
from Processing import PrcocessNetlist

class Source(QtGui.QWidget):
    def __init__(self,kicadfile=None):
        QtGui.QWidget.__init__(self)
        self.obj_proc = PrcocessNetlist()
        
        #Read NetList
        self.kicadNetlist = self.obj_proc.readNetlist(kicadfile)
        print "My Net List ",self.kicadNetlist
        
      
        
