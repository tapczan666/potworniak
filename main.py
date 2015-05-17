__author__ = 'maciek'

import numpy as np
import pyqtgraph as pg
from ui import Interface
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import pyqtSlot
from sampler import Sampler
from worker import Worker
from controller import USBController

app = QtGui.QApplication([])

class Analyzer(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        ### MODE FLAGS ###
        self.RUNNING = False
        self.HF = False
        self.WATERFALL = False

        ### VARIABLES ###
        self.step = 1.8e6
        self.ref = 0

        self.gain = 0
        self.sampRate = 2.4e6

        self.length = 2048
        self.sliceLength = int(np.floor(self.length*(self.step/self.sampRate)))

        self.waterfallHistorySize = 100

        self.ui = Interface()
        self.ui.setupUi(self, self.step, self.ref)

        self.nfft = self.ui.rbwEdit.itemData(self.ui.rbwEdit.currentIndex()).toInt()[0]
        self.numSamples = self.nfft*2

        self.createPlot()

        ### SIGNALS AND SLOTS ###
        self.ui.startButton.clicked.connect(self.onStart)
        self.ui.stopButton.clicked.connect(self.onStop)
        self.ui.plotTabs.currentChanged.connect(self.onMode)
        self.ui.startEdit.valueChanged.connect(self.onStartFreq)
        self.ui.stopEdit.valueChanged.connect(self.onStopFreq)
        self.ui.rbwEdit.activated[int].connect(self.onRbw)
        self.ui.centerEdit.valueChanged.connect(self.onCenter)
        self.ui.spanEdit.valueChanged.connect(self.onSpan)
        self.ui.refEdit.valueChanged.connect(self.onRef)
        self.ui.waterfallCheck.stateChanged.connect(self.onWaterfall)

### PLOT FUNCTIONS ###
    def createPlot(self):
        self.plot = pg.PlotWidget()
        if self.HF == False:
            self.ui.startEdit.setRange(30e6, 1280e6-self.step)
            self.ui.stopEdit.setRange(30e6+self.step, 1280e6)
            self.ui.centerEdit.setRange(30e6+self.step/2, 1280e6-self.step/2)
            self.startFreq = 80e6
            self.stopFreq = 100e6
            self.ui.plotLayout.addWidget(self.plot)
        elif self.HF:
            self.ui.startEdit.setRange(1e6, 30e6-self.step)
            self.ui.stopEdit.setRange(1e6+self.step, 30e6)
            self.ui.centerEdit.setRange(1e6+self.step/2, 30e6-self.step/2)
            self.startFreq = 1e6
            self.stopFreq = 30e6
            self.ui.plotLayout_2.addWidget(self.plot)
        self.plot.showGrid(x=True, y=True)
        self.plot.setMouseEnabled(x=False, y=False)
        self.plot.setYRange(self.ref-100, self.ref)
        self.plot.setXRange(self.startFreq/1e6, self.stopFreq/1e6)
        self.curve = self.plot.plot(pen='y')

        self.span = self.stopFreq - self.startFreq
        self.center = self.startFreq + self.span/2

        # Crosshair
        self.vLine = pg.InfiniteLine(angle=90, movable=False)
        self.hLine = pg.InfiniteLine(angle=0, movable=False)
        self.plot.addItem(self.vLine, ignoreBounds=True)
        self.plot.addItem(self.hLine, ignoreBounds=True)
        self.posLabel = pg.TextItem(anchor=(0,1))
        self.plot.addItem(self.posLabel)
        self.mouseProxy = pg.SignalProxy(self.plot.scene().sigMouseMoved,
                                         rateLimit=60, slot=self.mouseMoved)

        self.updateFreqs()

    def deletePlot(self):
        self.curve.deleteLater()
        self.curve = None
        if self.HF == False:
            self.ui.plotLayout.removeWidget(self.plot)
        else:
            self.ui.plotLayout_2.removeWidget(self.plot)
        self.plot.deleteLater()
        self.plot = None

    def createWaterfall(self):
        self.WATERFALL = True
        self.waterfallPlot = pg.PlotWidget()
        if self.HF == False:
            self.ui.plotLayout.addWidget(self.waterfallPlot)
        else:
            self.ui.plotLayout_2.addWidget(self.waterfallPlot)
        self.waterfallPlot.setYRange(-self.waterfallHistorySize, 0)
        self.waterfallPlot.setXLink(self.plot)
        self.waterfallPlot.setMouseEnabled(x=False, y=False)

        self.waterfallHistogram = pg.HistogramLUTItem(fillHistogram=False)
        self.waterfallHistogram.gradient.loadPreset("flame")
        self.waterfallHistogram.setHistogramRange(self.ref-100, self.ref)

        self.waterfallImg = None

    def deleteWaterfall(self):
        if self.WATERFALL:
            self.WATERFALL = False
            if self.HF == False:
                self.ui.plotLayout.removeWidget(self.waterfallPlot)
            else:
                self.ui.plotLayout_2.removeWidget(self.waterfallPlot)
            self.waterfallPlot.deleteLater()
            self.waterfallPlot = None
            self.waterfallHistogram.deleteLater()
            self.waterfallHistogram = None
            if self.waterfallImg is not None:
                self.waterfallImg.deleteLater()
                self.waterfallImg = None

    def updateFreqs(self):
        self.freqs = np.arange(self.startFreq+self.step/2, self.stopFreq+self.step/2, self.step)
        if self.RUNNING:
            self.sampler.freqs = self.freqs
            self.sampler.BREAK = True

        self.xData = []
        self.yData = []
        self.waterfallImg = None
        self.plot.setXRange(self.startFreq/1e6, self.stopFreq/1e6)

        self.ui.startEdit.setValue(self.startFreq)
        self.ui.stopEdit.setValue(self.stopFreq)
        self.ui.centerEdit.setValue(self.center)
        self.ui.spanEdit.setValue(self.span)
        
    def updateRbw(self):
        self.markerIndex = [None, None, None, None]
        self.deltaIndex = None
        if self.nfft < 200:
            self.numSamples = 256
        else:
            self.numSamples = self.nfft*2
            
        if self.span >=50e6:
            threshold = 200
        elif self.span >= 20e6: 
            threshold = 500
        else:
            threshold = 1000
            
        if self.nfft < threshold:
            self.length = 1024
            self.sliceLength = int(np.floor(self.length*(self.step/self.sampRate)))        
        else:
            self.length = self.nfft
            self.sliceLength = int(np.floor(self.length*(self.step/self.sampRate)))

    @QtCore.pyqtSlot(object)
    def plotUpdate(self, data):
        index = data[0]
        xTemp = data[2]
        yTemp = data[1]
        if len(yTemp) == 0:
                self.xData = xTemp
                self.yData = yTemp
        else:
            self.xData = np.concatenate((self.xData[:index*self.sliceLength], xTemp, self.xData[(index+1)*self.sliceLength:]))
            self.yData = np.concatenate((self.yData[:index*self.sliceLength], yTemp, self.yData[(index+1)*self.sliceLength:]))

        self.curve.setData(self.xData, self.yData)
        if len(self.xData) == self.sliceLength*len(self.freqs):
            if self.WATERFALL:
                self.waterfallUpdate(self.xData, self.yData)

    def waterfallUpdate(self, xData, yData):
        if self.waterfallImg is None:
            self.waterfallImgArray = np.zeros((self.waterfallHistorySize, len(xData)))
            self.waterfallImg = pg.ImageItem()
            self.waterfallImg.scale((xData[-1] - xData[0]) / len(xData), 1)
            self.waterfallImg.setPos(xData[0],-self.waterfallHistorySize)
            self.waterfallPlot.clear()
            self.waterfallPlot.addItem(self.waterfallImg)
            self.waterfallHistogram.setImageItem(self.waterfallImg)
            self.plot.setXRange(self.startFreq/1e6, self.stopFreq/1e6)

        self.waterfallImgArray = np.roll(self.waterfallImgArray, -1, axis=0)
        self.waterfallImgArray[-1] = yData
        self.waterfallImg.setImage(self.waterfallImgArray.T,
                                   autoLevels=True, autoRange=False)
### SETUP SAMPLER AND WORKER
    def setupSampler(self):
        self.samplerThread = QtCore.QThread(self)
        self.sampler = Sampler(self.gain, self.sampRate, self.freqs, self.numSamples)
        self.sampler.moveToThread(self.samplerThread)
        self.samplerThread.started.connect(self.sampler.sampling)
        self.sampler.samplerError.connect(self.onError)
        self.sampler.dataAcquired.connect(self.worker.work)
        #self.ui.gainSlider.valueChanged[int].connect(self.setGain)
        #self.ui.gainSlider.valueChanged[int].connect(self.sampler.changeGain, QtCore.Qt.QueuedConnection)
        self.samplerThread.start(QtCore.QThread.NormalPriority)

    def setupWorker(self):
        self.workerThread = QtCore.QThread(self)
        self.worker = Worker(self.nfft, self.length, self.sliceLength, self.sampRate)
        self.worker.moveToThread(self.workerThread)
        #self.workerThread.started.connect(self.worker.working)
        self.worker.dataReady.connect(self.plotUpdate)
        #self.worker.abort.connect(self.onAbort)
        self.workerThread.start(QtCore.QThread.NormalPriority)


### GUI FUNCTIONS ###
    def mouseMoved(self, evt):
        pos = evt[0]
        if self.plot.sceneBoundingRect().contains(pos):
            mousePoint = self.plot.getViewBox().mapSceneToView(pos)
            self.posLabel.setText("f=%0.1f MHz, P=%0.1f dBm" % (mousePoint.x(),mousePoint.y()))
            self.vLine.setPos(mousePoint.x())
            self.hLine.setPos(mousePoint.y())
            self.posLabel.setPos(mousePoint.x(), mousePoint.y())

    @pyqtSlot()
    def onStart(self):
        self.ui.startButton.setEnabled(False)
        self.ui.stopButton.setEnabled(True)
        self.ui.statusbar.setVisible(False)
        self.ui.statusbar.clearMessage()

        self.setupWorker()
        self.setupSampler()

        self.RUNNING = True

    @pyqtSlot()
    def onStop(self):
        self.ui.startButton.setEnabled(True)
        self.ui.stopButton.setEnabled(False)

        self.samplerThread.exit(0)
        self.sampler.WORKING = False
        self.sampler = None

        self.workerThread.exit(0)
        self.worker = None

        self.RUNNING = False

    @pyqtSlot(int)
    def onMode(self, index):
        if index == 0:
            self.deletePlot()
            self.ui.waterfallCheck.setChecked(False)
            self.HF = False

            self.createPlot()

            self.ui.settingsTabs.setEnabled(True)

        elif index == 1:
            self.deletePlot()
            self.ui.waterfallCheck.setChecked(False)
            self.HF = True

            self.createPlot()

            self.ui.settingsTabs.setEnabled(True)

        elif index == 2:
            self.ui.settingsTabs.setEnabled(True)

        elif index == 3:
            self.ui.settingsTabs.setEnabled(False)

    @pyqtSlot(float)
    def onStartFreq(self, value):
        self.startFreq = value
        if self.startFreq > self.stopFreq - self.step:
            self.stopFreq = self.startFreq + self.step
        self.span = self.stopFreq - self.startFreq
        self.center = self.startFreq + self.span/2
        self.updateFreqs()

    @pyqtSlot(float)
    def onStopFreq(self, value):
        self.stopFreq = value
        if self.stopFreq < self.startFreq + self.step:
            self.startFreq = self.stopFreq - self.step
        self.span = self.stopFreq - self.startFreq
        self.center = self.startFreq + self.span/2
        self.updateFreqs()

    @pyqtSlot(int)
    def onRbw(self, index):
        self.nfft = self.ui.rbwEdit.itemData(index).toInt()[0]
        self.updateRbw()
        if self.RUNNING:
            self.sampler.numSamples = self.numSamples
            self.worker.nfft = self.nfft
            self.worker.length = self.length
            self.worker.sliceLength = self.sliceLength
            self.worker.correction = 0
            self.sampler.BREAK = True

        self.xData = []
        self.yData = []
        self.waterfallImg = None

    @QtCore.pyqtSlot(float)
    def onCenter(self,center):
        self.center = center
        self.startFreq = self.center - self.span/2
        self.stopFreq = self.center + self.span/2
        self.updateFreqs()

    @QtCore.pyqtSlot(float)
    def onSpan(self,span):
        self.span = span
        self.startFreq = self.center - self.span/2
        self.stopFreq = self.center + self.span/2
        self.updateFreqs()

    @QtCore.pyqtSlot(int)
    def onRef(self, ref):
        self.ref = ref
        self.plot.setYRange(self.ref-100, self.ref)

    @pyqtSlot(object)
    def onError(self, errorMsg):
        #self.ui.statusbar.addWidget(QtGui.QLabel(errorMsg))
        self.ui.statusbar.showMessage("ERROR: " + errorMsg)
        self.ui.statusbar.setVisible(True)
        self.ui.stopButton.click()

    @pyqtSlot(int)
    def onWaterfall(self, state):
        if state ==2:
            self.createWaterfall()
        elif state == 0:
            self.deleteWaterfall()

# Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys

    analyzer = Analyzer()
    analyzer.show()

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()