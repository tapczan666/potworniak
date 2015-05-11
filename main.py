__author__ = 'maciek'

import numpy as np
import pyqtgraph as pg
from ui import Interface
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import pyqtSlot

app = QtGui.QApplication([])

class Analyzer(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.ui = Interface()
        self.ui.setupUi(self)

        self.createPlot()

### PLOT FUNCTIONS ###
    def createPlot(self):
        self.plot = pg.PlotWidget()
        self.ui.plotLayout.addWidget(self.plot)
        self.plot.showGrid(x=True, y=True)
        self.plot.setYRange(0, 100)
        self.curve = self.plot.plot(pen='y')

    def createWaterfall(self):
        self.waterfallPlot = pg.PlotWidget()
        self.ui.plotLayout.addWidget(self.waterfallPlot)
        self.waterfallPlot.setYRange(-self.waterfallHistorySize, 0)
        self.waterfallPlot.setXLink(self.plot)

        self.waterfallHistogram = pg.HistogramLUTItem()
        self.waterfallHistogram.gradient.loadPreset("flame")

        self.waterfallImg = None

### GUI FUNCTIONS ###
    @pyqtSlot()
    def onStart(self):
        pass

    @pyqtSlot()
    def onStop(self):
        pass

    @pyqtSlot()
    def onRbw(self):
        pass

# Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys

    analyzer = Analyzer()
    analyzer.show()

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()