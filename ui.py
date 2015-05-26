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
    def setupUi(self, MainWindow, step, ref):
        self.step = step
        self.ref = ref
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
        self.plotTabs = QtGui.QTabWidget(self.centralWidget)
        self.verticalLayout_1.addWidget(self.plotTabs)

        self.plotTab_1 = QtGui.QWidget()
        self.plotTab_1.setObjectName(_fromUtf8("plotTab_1"))
        self.plotLayout = QtGui.QVBoxLayout(self.plotTab_1)
        self.plotTabs.addTab(self.plotTab_1, "Wideband")

        self.plotTab_2 = QtGui.QWidget()
        self.plotTab_2.setObjectName(_fromUtf8("plotTab_2"))
        self.plotLayout_2 = QtGui.QVBoxLayout(self.plotTab_2)
        self.plotTabs.addTab(self.plotTab_2, "HF")

        # self.plotTab_3 = QtGui.QWidget()
        # self.plotTab_3.setObjectName(_fromUtf8("plotTab_3"))
        # self.plotLayout_3 = QtGui.QVBoxLayout(self.plotTab_3)
        # self.plotTabs.addTab(self.plotTab_3, "RTSA")
        #
        # self.plotTab_4 = QtGui.QWidget()
        # self.plotTab_4.setObjectName(_fromUtf8("plotTab_4"))
        # self.plotLayout_4 = QtGui.QVBoxLayout(self.plotTab_4)
        # self.plotTabs.addTab(self.plotTab_4, "IQ")

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

        self.startEdit = pg.SpinBox(self.freqBox, suffix=' MHz', siPrefix=False)
        self.startEdit.setObjectName(_fromUtf8("startEdit"))
        self.startEdit.setDecimals(2)
        self.startEdit.setSingleStep(0.1)
        self.startEdit.setKeyboardTracking(False)
        self.startLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.startEdit)
        self.freqHLayout_1.addLayout(self.startLayout)

        # Stop frequency setting
        self.stopLayout = QtGui.QFormLayout()
        self.stopLayout.setObjectName(_fromUtf8("stopLayout"))
        self.stopLabel = QtGui.QLabel(self.freqBox)
        self.stopLabel.setObjectName(_fromUtf8("stopLabel"))
        self.stopLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.stopLabel)

        self.stopEdit = pg.SpinBox(self.freqBox, suffix=' MHz', siPrefix=False, decimals=2)
        self.stopEdit.setObjectName(_fromUtf8("stopEdit"))
        #self.stopEdit.setDecimals(2)
        self.stopEdit.setSingleStep(0.1)
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

        self.freqHLayout_2 = QtGui.QHBoxLayout()
        self.freqHLayout_2.setObjectName(_fromUtf8("freqHLayout_2"))
        self.freqVLayout_1.addLayout(self.freqHLayout_2)

        # Center frequency setting
        self.centerLayout = QtGui.QFormLayout()
        self.centerLayout.setObjectName(_fromUtf8("centerLayout"))
        self.centerLabel = QtGui.QLabel(self.freqBox)
        self.centerLabel.setObjectName(_fromUtf8("centerLabel"))
        self.centerLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.centerLabel)

        self.centerEdit = pg.SpinBox(self.freqBox, suffix=' MHz', siPrefix=False)
        self.centerEdit.setObjectName(_fromUtf8("centerEdit"))
        self.centerEdit.setDecimals(2)
        self.centerEdit.setSingleStep(1)
        self.centerEdit.setKeyboardTracking(False)
        self.centerLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.centerEdit)
        self.freqHLayout_2.addLayout(self.centerLayout)

        # Span setting
        self.spanLayout = QtGui.QFormLayout()
        self.spanLayout.setObjectName(_fromUtf8("spanLayout"))
        self.spanLabel = QtGui.QLabel(self.freqBox)
        self.spanLabel.setObjectName(_fromUtf8("spanLabel"))
        self.spanLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.spanLabel)

        self.spanEdit = pg.SpinBox(self.freqBox, suffix=' MHz', siPrefix=False)
        self.spanEdit.setObjectName(_fromUtf8("spanEdit"))
        self.spanEdit.setDecimals(2)
        self.spanEdit.setRange(self.step/1e6, 1250)
        self.spanEdit.setSingleStep(0.1)
        self.spanEdit.setKeyboardTracking(False)
        self.spanLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.spanEdit)
        self.freqHLayout_2.addLayout(self.spanLayout)
        self.freqHLayout_2.addItem(spacerItem)

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
        self.stopButton.setEnabled(False)
        self.settingsHLayout_1.addWidget(self.stopButton)
        self.settingsVLayout_1.addLayout(self.settingsHLayout_1)

        # Gain slider
        self.gainLayout = QtGui.QFormLayout()
        self.gainLayout.setObjectName(_fromUtf8("gainLayout"))
        self.gainLabel = QtGui.QLabel(self.settingsBox)
        self.gainLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.gainLabel.setObjectName(_fromUtf8("gainLabel"))
        self.gainLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.gainLabel)
        self.gainSlider = QtGui.QSlider(self.settingsBox)
        self.gainSlider.setMaximum(49)
        self.gainSlider.setSingleStep(1)
        self.gainSlider.setProperty("value", 20)
        self.gainSlider.setOrientation(QtCore.Qt.Horizontal)
        self.gainSlider.setObjectName(_fromUtf8("gainSlider"))
        self.gainLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.gainSlider)
        self.settingsVLayout_1.addLayout(self.gainLayout)

        # Gain display
        self.gainDisp = QtGui.QLCDNumber(self.settingsBox)
        self.gainDisp.setSegmentStyle(QtGui.QLCDNumber.Flat)
        self.settingsVLayout_1.addWidget(self.gainDisp)

        # Reference level setting
        self.refLayout = QtGui.QFormLayout()
        self.refLayout.setObjectName(_fromUtf8("refLayout"))
        self.refLabel = QtGui.QLabel(self.settingsBox)
        self.refLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.refLabel.setObjectName(_fromUtf8("refLabel"))
        self.refLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.refLabel)
        self.refEdit = QtGui.QDoubleSpinBox(self.settingsBox)
        self.refEdit.setObjectName(_fromUtf8("refEdit"))
        self.refEdit.setValue(self.ref)
        self.refEdit.setDecimals(0)
        self.refEdit.setRange(-50, 50)
        self.refEdit.setKeyboardTracking(False)
        self.refLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.refEdit)
        self.settingsVLayout_1.addLayout(self.refLayout)

        spacerItem1 = QtGui.QSpacerItem(158, 304, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.settingsVLayout_1.addItem(spacerItem1)

    ### Settings tabs ###
        self.settingsTabs = QtGui.QTabWidget(self.settingsBox)
        self.settingsVLayout_1.addWidget(self.settingsTabs)
        self.settingsTabs.setEnabled(False)

        # Misc. options
        self.tab_1 = QtGui.QWidget()
        self.settingsTabs.addTab(self.tab_1, "Misc.")

        self.miscLayout = QtGui.QVBoxLayout()
        self.saveButton = QtGui.QPushButton(self.settingsBox)
        self.saveButton.setText("Save plot")
        self.miscLayout.addWidget(self.saveButton)

        self.avgLayout_1 = QtGui.QFormLayout()
        self.avgLayout_1.setObjectName(_fromUtf8("avgLayout_1"))
        self.avgLabel_1 = QtGui.QLabel(self.settingsBox)
        self.avgLabel_1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.avgLabel_1.setObjectName(_fromUtf8("avgLabel"))
        self.avgLayout_1.setWidget(0, QtGui.QFormLayout.LabelRole, self.avgLabel_1)
        self.avgCheck = QtGui.QCheckBox(self.settingsBox)
        self.avgLayout_1.setWidget(0, QtGui.QFormLayout.FieldRole, self.avgCheck)
        self.miscLayout.addLayout(self.avgLayout_1)

        self.avgLayout_2 = QtGui.QFormLayout()
        self.avgLabel_2 = QtGui.QLabel(self.settingsBox)
        self.avgLabel_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.avgLabel_2.setObjectName(_fromUtf8("avgLabel_2"))
        self.avgLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.avgLabel_2)
        self.avgEdit = QtGui.QDoubleSpinBox(self.settingsBox)
        self.avgEdit.setDecimals(0)
        self.avgEdit.setRange(1, 100)
        self.avgEdit.setKeyboardTracking(False)
        self.avgEdit.setValue(10)
        self.avgLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.avgEdit)
        self.miscLayout.addLayout(self.avgLayout_2)

        self.holdLayout = QtGui.QFormLayout()
        self.holdLayout.setObjectName(_fromUtf8("holdLayout"))
        self.holdLabel = QtGui.QLabel(self.settingsBox)
        self.holdLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.holdLabel.setObjectName(_fromUtf8("holdLabel"))
        self.holdLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.holdLabel)
        self.holdCheck = QtGui.QCheckBox(self.settingsBox)
        self.holdLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.holdCheck)
        self.miscLayout.addLayout(self.holdLayout)

        self.peakLayout = QtGui.QFormLayout()
        self.peakLayout.setObjectName(_fromUtf8("peakLayout"))
        self.peakLabel = QtGui.QLabel(self.settingsBox)
        self.peakLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.peakLabel.setObjectName(_fromUtf8("peakLabel"))
        self.peakLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.peakLabel)
        self.peakCheck = QtGui.QCheckBox(self.settingsBox)
        self.peakLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.peakCheck)
        self.miscLayout.addLayout(self.peakLayout)

        self.waterfallLayout = QtGui.QFormLayout()
        self.waterfallLayout.setObjectName(_fromUtf8("waterfallLayout"))
        self.waterfallLabel = QtGui.QLabel(self.settingsBox)
        self.waterfallLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.waterfallLabel.setObjectName(_fromUtf8("waterfallLabel"))
        self.waterfallLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.waterfallLabel)
        self.waterfallCheck = QtGui.QCheckBox(self.settingsBox)
        self.waterfallLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.waterfallCheck)
        self.miscLayout.addLayout(self.waterfallLayout)

        self.correctButton = QtGui.QPushButton(self.settingsBox)
        self.correctButton.setText("Correction")
        self.miscLayout.addWidget(self.correctButton)

        self.tab_1.setLayout(self.miscLayout)

        # Traces
        self.tab_2 = QtGui.QWidget()
        self.settingsTabs.addTab(self.tab_2, "Traces")

        self.traceLayout = QtGui.QVBoxLayout()
        self.traceButton_1 = QtGui.QPushButton(self.settingsBox)
        self.traceButton_1.setText("Save trace 1")
        self.traceLayout.addWidget(self.traceButton_1)

        self.traceButton_2 = QtGui.QPushButton(self.settingsBox)
        self.traceButton_2.setText("Save trace 2")
        self.traceLayout.addWidget(self.traceButton_2)

        self.traceButton_3 = QtGui.QPushButton(self.settingsBox)
        self.traceButton_3.setText("Save trace 3")
        self.traceLayout.addWidget(self.traceButton_3)

        self.traces = [self.traceButton_1, self.traceButton_2, self.traceButton_3]

        self.tab_2.setLayout(self.traceLayout)

        # Markers
        self.tab_3 = QtGui.QWidget()
        self.settingsTabs.addTab(self.tab_3, "Markers")

        self.markerLayout = QtGui.QGridLayout()
        self.markerLabel_1 = QtGui.QLabel(self.settingsBox)
        self.markerLabel_1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.markerLayout.addWidget(self.markerLabel_1, 0,0)
        self.markerCheck_1 = QtGui.QCheckBox(self.settingsBox)
        self.markerLayout.addWidget(self.markerCheck_1, 0,1)
        self.markerEdit_1 = QtGui.QDoubleSpinBox(self.settingsBox)
        self.markerEdit_1.setDecimals(2)
        self.markerEdit_1.setKeyboardTracking(False)
        self.markerEdit_1.setDisabled(True)
        self.markerEdit_1.setSingleStep(0.1)
        self.markerLayout.addWidget(self.markerEdit_1, 0,2)

        self.markerLabel_2 = QtGui.QLabel(self.settingsBox)
        self.markerLabel_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.markerLayout.addWidget(self.markerLabel_2, 2,0)
        self.markerCheck_2 = QtGui.QCheckBox(self.settingsBox)
        self.markerLayout.addWidget(self.markerCheck_2, 2,1)
        self.markerEdit_2 = QtGui.QDoubleSpinBox(self.settingsBox)
        self.markerEdit_2.setDecimals(2)
        self.markerEdit_2.setKeyboardTracking(False)
        self.markerEdit_2.setDisabled(True)
        self.markerEdit_2.setSingleStep(0.1)
        self.markerLayout.addWidget(self.markerEdit_2, 2,2)

        self.markerLabel_3 = QtGui.QLabel(self.settingsBox)
        self.markerLabel_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.markerLayout.addWidget(self.markerLabel_3, 3,0)
        self.markerCheck_3 = QtGui.QCheckBox(self.settingsBox)
        self.markerLayout.addWidget(self.markerCheck_3, 3,1)
        self.markerEdit_3 = QtGui.QDoubleSpinBox(self.settingsBox)
        self.markerEdit_3.setDecimals(2)
        self.markerEdit_3.setKeyboardTracking(False)
        self.markerEdit_3.setDisabled(True)
        self.markerEdit_3.setSingleStep(0.1)
        self.markerLayout.addWidget(self.markerEdit_3, 3,2)

        self.markerLabel_4 = QtGui.QLabel(self.settingsBox)
        self.markerLabel_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.markerLayout.addWidget(self.markerLabel_4, 4,0)
        self.markerCheck_4 = QtGui.QCheckBox(self.settingsBox)
        self.markerLayout.addWidget(self.markerCheck_4, 4,1)
        self.markerEdit_4 = QtGui.QDoubleSpinBox(self.settingsBox)
        self.markerEdit_4.setDecimals(2)
        self.markerEdit_4.setKeyboardTracking(False)
        self.markerEdit_4.setDisabled(True)
        self.markerEdit_4.setSingleStep(0.1)
        self.markerLayout.addWidget(self.markerEdit_4, 4,2)

        self.deltaLabel = QtGui.QLabel(self.settingsBox)
        self.deltaLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.markerLayout.addWidget(self.deltaLabel, 1,0)
        self.deltaCheck = QtGui.QCheckBox(self.settingsBox)
        self.markerLayout.addWidget(self.deltaCheck, 1,1)
        self.deltaEdit = QtGui.QDoubleSpinBox(self.settingsBox)
        self.deltaEdit.setDecimals(2)
        self.deltaEdit.setSingleStep(0.1)
        self.deltaEdit.setKeyboardTracking(False)
        self.deltaEdit.setDisabled(True)
        self.markerLayout.addWidget(self.deltaEdit, 1,2)
        self.deltaCheck.setDisabled(True)

        self.tab_3.setLayout(self.markerLayout)

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
        #self.plotBox.setTitle(_translate("MainWindow", "Spectrum", None))
        self.startLabel.setText(_translate("MainWindow", "START:", None))
        self.stopLabel.setText(_translate("MainWindow", "STOP:", None))
        self.rbwLabel.setText(_translate("MainWindow", "RBW:", None))
        self.settingsBox.setTitle(_translate("MainWindow", "Settings", None))
        self.gainLabel.setText(_translate("MainWindow", "Gain:", None))
        self.refLabel.setText(_translate("MainWindow", "REF:", None))
        self.holdLabel.setText(_translate("MainWindow", "Max HOLD:", None))
        self.centerLabel.setText(_translate("MainWindow", "Center:", None))
        self.spanLabel.setText(_translate("MainWindow", "Span:", None))
        self.avgLabel_1.setText(_translate("MainWindow", "Average:", None))
        self.avgLabel_2.setText(_translate("MainWindow", "Avg traces:", None))
        self.peakLabel.setText(_translate("MainWindow", "Peak search:", None))
        self.waterfallLabel.setText(_translate("MainWindow", "Waterfall:", None))
        self.markerLabel_1.setText(_translate("MainWindow", "Marker 1:", None))
        self.markerLabel_2.setText(_translate("MainWindow", "Marker 2:", None))
        self.markerLabel_3.setText(_translate("MainWindow", "Marker 3:", None))
        self.markerLabel_4.setText(_translate("MainWindow", "Marker 4:", None))
        self.deltaLabel.setText(_translate("MainWindow", "Delta 1:", None))