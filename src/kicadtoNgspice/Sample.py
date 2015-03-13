from PyQt4 import QtGui,QtCore

import sys
import re
import datetime
################################################################
def main():
    app = QtGui.QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec_())

################################################################
class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        # create stuff
        self.rw = ReportWidget()
        self.setCentralWidget(self.rw)
        self.sw = StartWindow()
        self.createActions()
        self.createMenus()
        self.createStatusBar()

        # create progress bar
        self.pb = QtGui.QProgressBar(self.statusBar())
        self.statusBar().addPermanentWidget(self.pb)

        # connections
        self.connect(self.sw, QtCore.Qt.SIGNAL("okClicked"),
                    self.rw.create)
        self.connect(self.rw.table, QtCore.Qt.SIGNAL("progressChanged"),
                     self.update_progress)
        self.connect(self.rw.table, QtCore.Qt.SIGNAL("displayFinished"),
                     self.hide_progress_bar)

        # format the main window
        self.setGeometry(100,100,750,550)

        # show windows
        self.show()
        self.sw.show()

    def update_progress(self, n, nrows):
        self.pb.show()
        self.pb.setRange(0, nrows)
        self.pb.setValue(n)
        self.statusBar().showMessage(self.tr("Parsing eventlog data..."))

    def hide_progress_bar(self):
        self.pb.hide()
        self.statusBar().showMessage(self.tr("Finished"))

    def about(self):
        QtGui.QMessageBox.about(self, self.tr("About AIS Audit Tool"),
            self.tr("AIS Audit Tool\n\n"
                    "%s\n"
                    "%s\n"
                    "%s" % (__author__, __version__, __date__)))

    def createActions(self):
        self.exitAct = QtGui.QAction(self.tr("E&xit;"), self)
        self.exitAct.setShortcut(self.tr("Ctrl+Q"))
        self.exitAct.setStatusTip(self.tr("Exit the application"))
        self.connect(self.exitAct, QtCore.Qt.SIGNAL("triggered()"), self, QtCore.Qt.SLOT("close()"))

        self.aboutAct = QtGui.QAction(self.tr("&About;"), self)
        self.aboutAct.setStatusTip(self.tr("Show the application's About box"))
        self.connect(self.aboutAct, QtCore.Qt.SIGNAL("triggered()"), self.about)

        self.aboutQtAct = QtGui.QAction(self.tr("About &Qt;"), self)
        self.aboutQtAct.setStatusTip(self.tr("Show the Qt library's About box"))
        self.connect(self.aboutQtAct, QtCore.Qt.SIGNAL("triggered()"), qApp, QtCore.Qt.SLOT("aboutQt()"))

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu(self.tr("&File;"))
        self.fileMenu.addAction(self.exitAct)

        self.helpMenu = self.menuBar().addMenu(self.tr("&Help;"))
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

    def createStatusBar(self):
        sb = QtGui.QStatusBar()
        sb.setFixedHeight(18)
        self.setStatusBar(sb)
        self.statusBar().showMessage(self.tr("Ready"))

################################################################
class StartWindow(QtGui.QWidget):
    def __init__(self, *args):
        QtGui.QWidget.__init__(self, *args)

        # date box
        self.label_date = QtGui.QLabel()
        self.label_date.setText("Set date of last audit:")
        default = datetime.date.today() - datetime.timedelta(DEFAULT_DAYS_FROM_LAST_AUDIT)
        self.datebox = QtGui.QDateEdit(QtCore.Qt.QDate(default.year, default.month, default.day))

        # buttons
        spacer = QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.button_ok = QtGui.QPushButton()
        self.button_ok.setText("OK")
        self.button_ok.setDefault(True)
        button_cancel = QtGui.QPushButton()
        button_cancel.setText("Cancel")

        # layout
        layout_right = QtGui.QVBoxLayout(self)
        layout_right.addWidget(self.label_date)
        layout_right.addWidget(self.datebox)
        layout_right.addItem(spacer)
        layout_right.addWidget(self.button_ok)
        layout_right.addWidget(button_cancel)

        # connections
        self.connect(button_cancel, QtCore.Qt.SIGNAL("clicked(bool)"),
                    self.close)
        self.connect(self.button_ok, QtCore.Qt.SIGNAL("clicked(bool)"),
                    self.ok_clicked)

    def ok_clicked(self):
        self.close()
        year = self.datebox.date().year()
        month = self.datebox.date().month()
        day = self.datebox.date().day()
        dateobj = datetime.date(int(year),int(month),int(day))
        self.emit(QtCore.Qt.SIGNAL("okClicked"), dateobj)

################################################################
class ReportWidget(QtGui.QWidget):
    def __init__(self, *args):
        QtGui.QWidget.__init__(self, *args)
        self.cbUsers = QtGui.QCheckBox("Hide SYSTEM users")
        self.cbSorting = QtGui.QCheckBox("Sorting enabled")
        self.table = MyTable()
        self.textbrowser = QtGui.QTextBrowser()
        self.textbrowser.setFontFamily("Courier")
        self.textbrowser.setFontPointSize(10)
        hlayout = QtGui.QHBoxLayout()
        hlayout.addWidget(self.cbUsers)
        hlayout.addWidget(self.cbSorting)
        vlayout = QtGui.QVBoxLayout()
        vlayout.setMargin(2)
        vlayout.addLayout(hlayout)
        vlayout.addWidget(self.table)
        self.setLayout(vlayout)
        self.setGeometry(100,100,750,550)

        # connections
        self.connect(self.cbUsers, QtCore.Qt.SIGNAL("stateChanged(int)"),
                     self.cbUsersChanged)
        self.connect(self.cbSorting, QtCore.Qt.SIGNAL("stateChanged(int)"),
                     self.cbSortingChanged)

    def create(self, dateobj):
        """ Parses the eventlog data, displays it in a table, and
            displays the user login/logout also """
        self.table.display_data(dateobj)

    def cbUsersChanged(self):
        state = self.cbUsers.checkState()
        if state == 0:
            self.table.show_system_users()
        elif state == 2:
            self.table.hide_system_users()

    def cbSortingChanged(self):
        state = self.cbSorting.checkState()
        if state == 0:
            self.table.setSortingEnabled(False)
        elif state == 2:
            self.table.setSortingEnabled(True)

################################################################
class MyTable(QtGui.QTableWidget):
    """ Creates a custom table widget """
    def __init__(self, *args):
        QtGui.QTableWidget.__init__(self, *args)
        self.setSelectionMode(self.ContiguousSelection)
        self.setGeometry(0,0,700,400)
        self.setShowGrid(False)
        self.other_users_list = []

    def hide_system_users(self):
        for n in self.other_users_list:
            self.setRowHidden(n, True)

    def show_system_users(self):
        for n in self.other_users_list:
            self.setRowHidden(n, False)

    def display_data(self, dateobj):
        """ Reads in data as a 2D list and formats and displays it in
            the table """

        print "Fetching data..."
        ep = EventlogParser()
        data = ep.parse_log(dateobj)
        print "Done."

        if len(data)==0:
            data = ["No data for this date range."]

        nrows = len(data)
        ncols = len(data[0])
        self.setRowCount(nrows)
        self.setColumnCount(ncols)
        self.setHorizontalHeaderLabels(['No.', 'Date','Time','Type','Event','User','Computer'])

        for i in xrange(len(data)):
            # update progress dialog
            if (i%20) == 0:
                self.emit(QtCore.Qt.SIGNAL("progressChanged"), i, nrows)
                qApp.processEvents()

            # set each cell to be a QTableWidgetItem from the _process_row method
            items = self._process_row(data[i])
            for j in range(len(items)):
                self.setItem(i, j, items[j])
            self.setRowHeight(i, 16)

            # set column width first time through
            if i == 0:
                self.resizeColumnsToContents()
                self.setColumnWidth(4, 250)

        # format column width
        self.resizeColumnsToContents()
        self.setColumnWidth(4, 250)

        # emit signal for finished processing
        self.emit(QtCore.Qt.SIGNAL("displayFinished"))

    def _process_row(self, row):
        """ Formats items in the row of the 2-D list data
            Input: the row of data from the EventlogParser in a list
            Returns a list of QTableWidgetItems to be one row in the table
        """

        icon = []
        for i in xrange(len(row)):
            # general formatting for all cells (may be overwritten)
            icon.append(QtGui.QIcon())
            computer = row[6]

            # time processing
            if i == 2:
                try:
                    hour = int(re.split(r":", row[i])[0])
                except:
                    raise
                if hour <= EARLY_HOUR or hour >= LATE_HOUR:
                    backcolor_time = QtGui.QColor(0,0,102)
                else:
                    backcolor_time = QtGui.QColor("white")

            # success or failure processing
            elif i == 3:
                if row[i] == "8":
                    row[i] = "Success"
                    icon[i] = QtGui.QIcon("success.png")
                elif row[i] == "16":
                    row[i] = "Failure"
                    icon[i] = QtGui.QIcon("failure.png")
                else:
                    row[i] = "Unknown"
                    icon[i] = QtGui.QIcon("unknown.png")

            # event processing
            elif i == 4:
                backcolor = QtGui.QColor("white")
                if row[i] in RED_EVENTIDS:
                    backcolor = QtGui.QColor("red")
                elif row[i] in ORANGE_EVENTIDS:
                    backcolor = QtGui.QColor("orange")
                elif row[i] in YELLOW_EVENTIDS:
                    backcolor = QtGui.QColor("yellow")
                elif row[i] in GREEN_EVENTIDS:
                    pass
                elif row[i] in OTHER_EVENTIDS:
                    backcolor = QtGui.QColor("blue")
                try:
                    row[i] = row[i] + ": " + EVENT_DESC[row[i]]
                except:
                    pass

            # user processing
            elif i == 5:
                if row[i] in (computer, "", "SYSTEM", "NETWORK SERVICE", "LOCAL SERVICE", "ANONYMOUS LOGON"):
                    font = QtGui.QFont("Arial", 8)
                    font.setBold(False)
                    textcolor = QtGui.QColor("gray")
                    user = 'other'
                else:
                    font = QtGui. QFont("Arial", 8)
                    font.setBold(True)
                    textcolor = QtGui.QColor("black")
                    user = 'user'

        # create table widget item
        tableitem_list = []
        for i in xrange(len(row)):
            tableitem = QtGui.QTableWidgetItem(row[i])
            if i == 2:
                tableitem.setBackgroundColor(backcolor_time)
            else:
                tableitem.setBackgroundColor(backcolor)
            tableitem.setTextColor(textcolor)
            tableitem.setFont(font)
            tableitem.setTextAlignment(QtCore.Qt.AlignTop)
            tableitem.setToolTip(row[i])
            tableitem.setIcon(icon[i])
            tableitem_list.append(tableitem)

        return tableitem_list

################################################################
if __name__ == "__main__":
    main()
