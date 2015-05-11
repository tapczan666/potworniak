__author__ = 'maciek'
import pyqtgraph as pg
from PyQt4 import QtCore, QtGui, Qt
import numpy as np

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Interface(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1000, 600)
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))

### MAIN LAYOUT ###
        self.horizontalLayout_1 = QtGui.QHBoxLayout(self.centralWidget)
        self.horizontalLayout_1.setObjectName(_fromUtf8("horizontalLayout_1"))

### LEFT SIDE LAYOUT ###
        self.verticalLayout_1 = QtGui.QVBoxLayout()
        self.verticalLayout_1.setObjectName(_fromUtf8("verticalLayout_1"))

    ### PLOT LAYOUT ###
        self.plotBox = QtGui.QGroupBox(self.centralWidget)
        self.plotBox.setObjectName(_fromUtf8("plotBox"))
        self.plotLayout = QtGui.QVBoxLayout(self.plotBox)
        self.verticalLayout_1.addWidget(self.plotBox)

    ### FREQ SETTINGS LAYOUT ###
        self.freqBox = QtGui.QGroupBox(self.centralWidget)
        self.freqBox.setObjectName(_fromUtf8("freqBox"))
        self.freqVLayout_1 = QtGui.QVBoxLayout(self.freqBox)

        self.freqHLayout_1 = QtGui.QHBoxLayout()
        self.freqHLayout_1.setObjectName(_fromUtf8("freqHLayout_1"))
        self.freqVLayout_1.addLayout(self.freqHLayout_1)

        # Start frequency setting
        self.startLayout = QtGui.QFormLayout()
        self.startLayout.setObjectName(_fromUtf8("startLayout"))
        self.startLabel = QtGui.QLabel(self.freqBox)
        self.startLabel.setObjectName(_fromUtf8("startLabel"))
        self.startLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.startLabel)

        self.startEdit = pg.SpinBox(self.freqBox, suffix='Hz', siPrefix=True)
        self.startEdit.setObjectName(_fromUtf8("startEdit"))
        self.startEdit.setDecimals(2)
        self.startEdit.setRange(1e6, 1280e6)
        self.startEdit.setSingleStep(1e5)
        self.startEdit.setKeyboardTracking(False)
        self.startLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.startEdit)
        self.freqHLayout_1.addLayout(self.startLayout)

        # Stop frequency setting
        self.stopLayout = QtGui.QFormLayout()
        self.stopLayout.setObjectName(_fromUtf8("stopLayout"))
        self.stopLabel = QtGui.QLabel(self.freqBox)
        self.stopLabel.setObjectName(_fromUtf8("stopLabel"))
        self.stopLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.stopLabel)

        self.stopEdit = pg.SpinBox(self.freqBox, suffix='Hz', siPrefix=True)
        self.stopEdit.setObjectName(_fromUtf8("stopEdit"))
        self.stopEdit.setDecimals(2)
        self.stopEdit.setRange(1e6, 1280e6)
        self.stopEdit.setSingleStep(1e5)
        self.stopEdit.setKeyboardTracking(False)
        self.stopLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.stopEdit)
        self.freqHLayout_1.addLayout(self.stopLayout)

        # RBW setting
        self.rbwLayout = QtGui.QFormLayout()
        self.rbwLayout.setObjectName(_fromUtf8("rbwLayout"))
        self.rbwLabel = QtGui.QLabel(self.freqBox)
        self.rbwLabel.setObjectName(_fromUtf8("rbwLabel"))
        self.rbwLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.rbwLabel)

        self.rbwEdit = pg.ComboBox(self.freqBox)
        self.rbwEdit.setObjectName(_fromUtf8("rbwEdit"))
        self.rbwEdit.addItem('0,21 kHz', 16384)
        self.rbwEdit.addItem('0,42 kHz', 8192)
        self.rbwEdit.addItem('0,84 kHz', 4096)
        self.rbwEdit.addItem('1,69 kHz', 2048)
        self.rbwEdit.addItem('3,38 kHz', 1024)
        self.rbwEdit.addItem('6,75 kHz', 512)
        self.rbwEdit.addItem('13,5 kHz', 256)
        self.rbwEdit.addItem('27 kHz', 128)
        self.rbwEdit.addItem('54 kHz', 64)
        self.rbwEdit.addItem('108 kHz', 32)
        self.rbwEdit.addItem('216 kHz', 16)
        self.rbwEdit.addItem('432 kHz', 8)
        self.rbwEdit.setCurrentIndex(4)
        self.rbwLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.rbwEdit)
        self.freqHLayout_1.addLayout(self.rbwLayout)

        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.freqHLayout_1.addItem(spacerItem)

        self.verticalLayout_1.addWidget(self.freqBox)
        self.horizontalLayout_1.addLayout(self.verticalLayout_1)

### RIGHT SIDE LAYOUT ###
        self.settingsBox = QtGui.QGroupBox(self.centralWidget)
        self.settingsBox.setMaximumSize(QtCore.QSize(250, 16777215))
        self.settingsBox.setObjectName(_fromUtf8("settingsBox"))
        self.settingsVLayout_1 = QtGui.QVBoxLayout(self.settingsBox)
        self.settingsVLayout_1.setObjectName(_fromUtf8("settingsVLayout_1"))

        # Start button
        self.settingsHLayout_1 = QtGui.QHBoxLayout()
        self.startButton = QtGui.QPushButton()
        self.startButton.setText('START')
        self.settingsHLayout_1.addWidget(self.startButton)

        # Stop button
        self.stopButton = QtGui.QPushButton()
        self.stopButton.setText('STOP')
        self.settingsHLayout_1.addWidget(self.stopButton)
        self.settingsVLayout_1.addLayout(self.settingsHLayout_1)

        self.horizontalLayout_1.addWidget(self.settingsBox)

### MISC Qt FUNCTIONS ###
        MainWindow.setCentralWidget(self.centralWidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 847, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        #self.statusbar.addWidget(self.peakStatus)
        self.statusbar.setVisible(False)

        self.retlanslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def retlanslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Spectrum Analyzer", None))
        self.freqBox.setTitle(_translate("MainWindow", "Frequency", None))
        self.plotBox.setTitle(_translate("MainWindow", "Spectrum", None))
        self.startLabel.setText(_translate("MainWindow", "START:", None))
        self.stopLabel.setText(_translate("MainWindow", "STOP:", None))
        self.rbwLabel.setText(_translate("MainWindow", "RBW:", None))
        self.settingsBox.setTitle(_translate("MainWindow", "Settings", None))
        # self.gainLabel.setText(_translate("MainWindow", "Gain:", None))
        # self.refLabel.setText(_translate("MainWindow", "REF:", None))
        # self.holdLabel.setText(_translate("MainWindow", "Max HOLD:", None))
        # self.centerLabel.setText(_translate("MainWindow", "Center [MHz]:", None))
        # self.spanLabel.setText(_translate("MainWindow", "Span [MHz]:", None))
        # self.avgLabel.setText(_translate("MainWindow", "Average:", None))
        # self.avgLabel_2.setText(_translate("MainWindow", "Avg traces:", None))
        # self.peakLabel.setText(_translate("MainWindow", "Peak search:", None))
        # self.markerLabel.setText(_translate("MainWindow", "Marker 1:", None))
        # self.markerLabel_2.setText(_translate("MainWindow", "Marker 2:", None))
        # self.markerLabel_3.setText(_translate("MainWindow", "Marker 3:", None))
        # self.markerLabel_4.setText(_translate("MainWindow", "Marker 4:", None))
        # self.deltaLabel.setText(_translate("MainWindow", "Delta 1:", None))