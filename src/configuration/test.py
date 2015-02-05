'''
Created on 04-Feb-2015

@author: fahim
'''
import sys
from PyQt4 import QtGui, QtCore


class MainWindow(QtGui.QMainWindow):

    def __init__(self, *args):
        apply(QtGui.QMainWindow.__init__, (self, ) + args)
        self.setCaption("Adding and deleting widgets")
        self.setName("main window")
        self.mainWidget=QtGui.QWidget(self) 
        self.setCentralWidget(self.mainWidget)
        self.mainLayout=QtGui.QVBoxLayout(self.mainWidget, 5, 5, "main")
        self.buttonLayout=QtGui.QHBoxLayout(self.mainLayout, 5, "button")
        self.widgetLayout=QtGui.QVBoxLayout(self.mainLayout, 5, "widget")

        self.bnAdd=QtGui.QPushButton("Add widget", self.mainWidget, "add")
        self.connect(self.bnAdd, QtCore.SIGNAL("clicked()"),
                     self.slotAddWidget)

        self.bnRemove=QtGui.QPushButton("Remove widget",
                                  self.mainWidget, "remove")
        self.connect(self.bnRemove, QtCore.SIGNAL("clicked()"),
                     self.slotRemoveWidget)

        self.buttonLayout.addWidget(self.bnAdd)
        self.buttonLayout.addWidget(self.bnRemove)

        self.buttons = []

    def slotAddWidget(self):
        widget=QtGui.QPushButton("test", self.mainWidget)
        self.widgetLayout.addWidget(widget)
        self.buttons.append(widget)
        widget.show()

    def slotRemoveWidget(self):
        self.widgetLayout.parent().removeChild(self.widgetLayout)
        self.widgetLayout=QtGui.QVBoxLayout(self.mainLayout, 5, "widget")
        self.buttons[-1].parent().removeChild(self.buttons[-1])
        del self.buttons[-1:]


def main(args):
    app=QtGui.QApplication(args)
    win=MainWindow()
    win.show()
    app.connect(app, QtCore.SIGNAL("lastWindowClosed()")
                                 , app
                                 ,QtCore.SLOT("quit()")
                                 )
    app.exec_loop()

if __name__=="__main__":
    main(sys.argv)
          
