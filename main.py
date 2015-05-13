__author__ = 'maciek'

import numpy as np
import pyqtgraph as pg
from ui import Interface
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import pyqtSlot
from sampler import Sampler
from worker import Worker

app = QtGui.QApplication([])

class Analyzer(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        ### MODE FLAGS ###
        self.HF = False

        ### VARIABLES ###
        self.startFreq = 80e6
        self.stopFreq = 100e6

        self.waterfallHistorySize = 100

        self.ui = Interface()
        self.ui.setupUi(self)

        self.createPlot()

        ### SIGNALS AND SLOTS ###
        self.ui.startButton.clicked.connect(self.onStart)
        self.ui.stopButton.clicked.connect(self.onStop)

### PLOT FUNCTIONS ###
    def createPlot(self):
        self.plot = pg.PlotWidget()
        if self.HF == False:
            self.ui.plotLayout.addWidget(self.plot)
        else:
            self.ui.plotLayout_2.addWidget(self.plot)
        self.plot.showGrid(x=True, y=True)
        self.plot.setYRange(0, 100)
        self.plot.setXRange(self.startFreq/1e6, self.stopFreq/1e6)
        self.curve = self.plot.plot(pen='y')

    def createWaterfall(self):
        self.waterfallPlot = pg.PlotWidget()
        if self.HF == False:
            self.ui.plotLayout.addWidget(self.waterfallPlot)
        else:
            self.ui.plotLayout_2.addWidget(self.waterfallPlot)
        self.waterfallPlot.setYRange(-self.waterfallHistorySize, 0)
        self.waterfallPlot.setXLink(self.plot)

        self.waterfallHistogram = pg.HistogramLUTItem()
        self.waterfallHistogram.gradient.loadPreset("flame")

        self.waterfallImg = None

### SETUP SAMPLER AND WORKER
    def setupSampler(self):
        self.samplerThread = QtCore.QThread(self)
        self.sampler = Sampler(self.gain, self.samp_rate, self.freqs, self.num_samples)
        self.sampler.moveToThread(self.samplerThread)
        self.samplerThread.started.connect(self.sampler.sampling)
        self.sampler.samplerError.connect(self.onError)
        #self.ui.gainSlider.valueChanged[int].connect(self.setGain)
        #self.ui.gainSlider.valueChanged[int].connect(self.sampler.changeGain, QtCore.Qt.QueuedConnection)
        self.samplerThread.start(QtCore.QThread.NormalPriority)

    def setupWorker(self):
        self.workerThread = QtCore.QThread(self)
        self.worker = Worker(self.nfft, self.length, self.slice_length, self.samp_rate)
        self.worker.moveToThread(self.workerThread)
        self.workerThread.started.connect(self.worker.working)
        #self.worker.abort.connect(self.onAbort)
        self.workerThread.start(QtCore.QThread.NormalPriority)


### GUI FUNCTIONS ###
    @pyqtSlot()
    def onStart(self):
        self.ui.startButton.setEnabled(False)
        self.ui.stopButton.setEnabled(True)

        self.setupWorker()
        self.setupSampler()

    @pyqtSlot()
    def onStop(self):
        self.ui.startButton.setEnabled(True)
        self.ui.stopButton.setEnabled(False)

        self.samplerThread.exit(0)
        self.sampler = None
        self.workerThread.exit(0)
        self.worker = None

    @pyqtSlot()
    def onRbw(self):
        pass

    @pyqtSlot(object)
    def onError(self, errorMsg):
        self.ui.statusbar.addWidget(QtGui.QLabel(errorMsg))

# Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys

    analyzer = Analyzer()
    analyzer.show()

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()