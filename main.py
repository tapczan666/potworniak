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
        self.MARKERS = [False, False, False, False]
        self.DELTA = False
        self.HOLD = False
        self.AVERAGE = False
        self.PEAK = False
        self.SAVE = [False, False, False]

        ### VARIABLES ###
        self.step = 1.8e6
        self.ref = 0

        self.gain = 0
        self.sampRate = 2.4e6

        self.waterfallHistorySize = 100
        self.markers = [None, None, None, None]
        self.markerIndex = [None, None, None, None]
        self.markerValue = [None, None, None, None]
        self.markerText = [None, None, None, None]
        self.deltaIndex = None
        self.deltaValue = None
        self.saveCurves = [None, None, None]
        self.penColors = ['g', 'c', 'm']

        self.ui = Interface()
        self.ui.setupUi(self, self.step, self.ref)

        self.nwelch = 15
        self.nfft = self.ui.rbwEdit.itemData(self.ui.rbwEdit.currentIndex()).toInt()[0]
        self.numSamples = self.nfft*(1+self.nwelch)/2
        self.length = self.nfft
        self.sliceLength = int(np.floor(self.length*(self.step/self.sampRate)))

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
        self.ui.markerCheck_1.stateChanged.connect(self.onMarker_1)
        self.ui.markerEdit_1.valueChanged.connect(self.onMarkerEdit_1)
        self.ui.deltaCheck.stateChanged.connect(self.onDelta)
        self.ui.deltaEdit.valueChanged.connect(self.onDeltaEdit)
        self.ui.holdCheck.stateChanged.connect(self.onHold)
        self.ui.avgCheck.stateChanged.connect(self.onAvg)
        self.ui.avgEdit.valueChanged.connect(self.onAvgEdit)
        self.ui.peakCheck.stateChanged.connect(self.onPeak)
        self.ui.traceButton_1.clicked.connect(self.onSave_1)
        self.ui.traceButton_2.clicked.connect(self.onSave_2)
        self.ui.traceButton_3.clicked.connect(self.onSave_3)
        self.ui.waterfallCheck.stateChanged.connect(self.onWaterfall)

        #self.usb = USBController()

### PLOT FUNCTIONS ###
    def createPlot(self):
        self.plot = pg.PlotWidget()
        if self.HF == False:
            self.ui.startEdit.setRange(30, 1280-self.step/1e6)
            self.ui.stopEdit.setRange(30+self.step/1e6, 1280)
            self.ui.centerEdit.setRange(30+self.step/2e6, 1280-self.step/2e6)
            self.startFreq = 80e6
            self.stopFreq = 100e6
            self.ui.plotLayout.addWidget(self.plot)
        elif self.HF:
            self.ui.startEdit.setRange(1, 30-self.step/1e6)
            self.ui.stopEdit.setRange(1+self.step/1e6, 30)
            self.ui.centerEdit.setRange(1+self.step/2e6, 30-self.step/2e6)
            self.startFreq = 1e6
            self.stopFreq = 30e6
            self.ui.plotLayout_2.addWidget(self.plot)
        self.plot.showGrid(x=True, y=True)
        self.plot.setMouseEnabled(x=False, y=False)
        self.plot.setYRange(self.ref-100, self.ref, padding=0)
        self.plot.setXRange(self.startFreq/1e6, self.stopFreq/1e6, padding=0)
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
                                         rateLimit=20, slot=self.mouseMoved)

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
        self.markerIndex = [None, None, None, None]
        self.deltaIndex = None
        self.peakIndex = None
        self.holdData = None
        self.avgArray = None
        self.avgCounter = 0
        self.saveCurves = [None, None, None]

        if self.RUNNING:
            self.sampler.freqs = self.freqs
            self.sampler.BREAK = True

        self.xData = []
        self.yData = []
        self.waterfallImg = None
        self.plot.setXRange(self.startFreq/1e6, self.stopFreq/1e6, padding=0)

        self.ui.startEdit.setValue(self.startFreq/1e6)
        self.ui.stopEdit.setValue(self.stopFreq/1e6)
        self.ui.centerEdit.setValue(self.center/1e6)
        self.ui.spanEdit.setValue(self.span/1e6)


        
    def updateRbw(self):
        self.markerIndex = [None, None, None, None]
        self.deltaIndex = None
        self.holdData = None
        self.avgArray = None
        self.avgCounter = 0
        self.saveCurves = [None, None, None]

        self.numSamples = self.nfft*(1+self.nwelch)/2
        if self.numSamples < 200:
            self.numSamples = 256
            
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

        yData = self.yData

        if len(self.xData) == self.sliceLength*len(self.freqs):
            if self.AVERAGE:
                if self.avgCounter == 0:
                    if self.avgArray is None:
                        self.avgArray = np.array([self.yData])

                    elif self.avgArray.shape[0] < self.numAvg:
                        self.avgArray = np.append(self.avgArray, np.array([self.yData]), axis=0)

                    else:
                        self.avgArray = np.roll(self.avgArray, -1, axis=0)
                        self.avgArray[-1] = self.yData
                    self.avgData = np.average(self.avgArray, axis=0)
                    #self.curve.setData(self.xData, yData)
                    self.avgCounter = len(self.freqs)
                else:
                    self.avgCounter -= 1
                yData = self.avgData

            for i in range(len(self.MARKERS)):
                if self.MARKERS[i]:
                    if self.markerIndex[i] == None:
                        index = np.argmin(np.abs(self.xData-self.markerValue[i]))
                        self.markerIndex[i] = index
                    self.markers[i].setIndex(self.markerIndex[i])
                    self.markerText[i].setText("Mk1:\nf=%0.1f MHz\nP=%0.1f dBm" % (self.xData[self.markerIndex[i]], yData[self.markerIndex[i]]))

            if self.DELTA:
                if self.deltaIndex == None:
                    index = np.argmin(np.abs(self.xData-self.deltaValue))
                    self.deltaIndex = index
                self.delta.setIndex(self.deltaIndex)
                dx = self.xData[self.deltaIndex] - self.xData[self.markerIndex[0]]
                dy = yData[self.deltaIndex] - yData[self.markerIndex[0]]
                self.deltaText.setText("Delta:\ndf=%0.1f MHz\ndP=%0.1f dB" % (dx, dy))

            if self.HOLD:
                if self.holdData is None:
                    self.holdData = yData
                else:
                    self.holdData = np.amax([self.holdData, yData], axis=0)
                self.holdCurve.setData(self.xData, self.holdData)

            if self.PEAK:
                self.peakIndex = np.argmax(yData)
                self.peak.setIndex(self.peakIndex)
                self.peakText.setText("Peak:\nf=%0.1f MHz\nP=%0.1f dBm" % (self.xData[self.peakIndex], yData[self.peakIndex]))

            for i in range(len(self.SAVE)):
                if self.SAVE[i]:
                    if self.saveCurves[i] is None:
                        self.saveCurves[i] = self.plot.plot(pen=self.penColors[i])
                        self.plot.addItem(self.saveCurves[i])
                        self.saveCurves[i].setData(self.xData, yData)

                    else:
                        self.plot.removeItem(self.saveCurves[i])
                        self.saveCurves[i] = None

                    self.SAVE[i] = False

            if self.WATERFALL:
                self.waterfallUpdate(self.xData, yData)
        #print len(yData)
        self.curve.setData(self.xData, yData)

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
        self.samplerThread.start(QtCore.QThread.NormalPriority)

    def setupWorker(self):
        self.workerThread = QtCore.QThread(self)
        self.worker = Worker(self.nfft, self.length, self.sliceLength, self.sampRate, self.nwelch)
        self.worker.moveToThread(self.workerThread)
        self.worker.dataReady.connect(self.plotUpdate)
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
        self.ui.settingsTabs.setEnabled(True)

        self.setupWorker()
        self.setupSampler()

        self.RUNNING = True

    @pyqtSlot()
    def onStop(self):
        self.ui.startButton.setEnabled(True)
        self.ui.stopButton.setEnabled(False)
        self.ui.settingsTabs.setEnabled(False)

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
        self.startFreq = value*1e6
        if self.startFreq > self.stopFreq - self.step:
            self.stopFreq = self.startFreq + self.step
        self.span = self.stopFreq - self.startFreq
        self.center = self.startFreq + self.span/2
        self.updateFreqs()

    @pyqtSlot(float)
    def onStopFreq(self, value):
        self.stopFreq = value*1e6
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
        print self.numSamples
        print self.nfft

    @pyqtSlot(float)
    def onCenter(self, center):
        self.center = center*1e6
        self.startFreq = self.center - self.span/2
        self.stopFreq = self.center + self.span/2
        self.updateFreqs()

    @pyqtSlot(float)
    def onSpan(self,span):
        self.span = span*1e6
        self.startFreq = self.center - self.span/2
        self.stopFreq = self.center + self.span/2
        self.updateFreqs()

    @pyqtSlot(int)
    def onRef(self, ref):
        self.ref = ref
        self.plot.setYRange(self.ref-100, self.ref)
        if self.WATERFALL:
            self.waterfallHistogram.setHistogramRange(self.ref-100, self.ref)

    # Markers
    @pyqtSlot(int)
    def onMarker_1(self, state):
        if state == 2:
            self.MARKERS[0] = True
            self.ui.deltaCheck.setEnabled(True)
            self.ui.markerEdit_1.setEnabled(True)
            self.ui.markerEdit_1.setRange(1, 1280)
            self.ui.markerEdit_1.setValue(self.center/1e6)
            self.markerValue[0] = self.ui.markerEdit_1.value()

            self.marker_1 = pg.CurvePoint(self.curve)
            self.plot.addItem(self.marker_1)
            self.markers[0] = self.marker_1
            self.markerArrow_1 = pg.ArrowItem(angle=270)
            self.markerArrow_1.setParentItem(self.marker_1)
            self.markerText_1 = pg.TextItem("Mk1", anchor=(0.5, 1.5))
            self.markerText_1.setParentItem(self.marker_1)
            self.markerText[0] = self.markerText_1

        elif state == 0:
            self.MARKERS[0] = False
            self.markerIndex[0] = None
            self.markerValue[0] = None
            self.markerText[0] = None
            self.ui.markerEdit_1.setDisabled(True)
            self.ui.deltaCheck.setDisabled(True)
            self.plot.removeItem(self.marker_1)
            self.marker_1.deleteLater()
            self.marker_1 = None

    @pyqtSlot(float)
    def onMarkerEdit_1(self, freq):
        self.markerIndex[0] = None
        self.markerValue[0] = freq

    @pyqtSlot(int)
    def onDelta(self, state):
        if state == 2:
            self.DELTA = True
            self.ui.deltaEdit.setEnabled(True)
            self.ui.deltaEdit.setRange(1, 1280)
            self.ui.deltaEdit.setValue(self.center/1e6)
            self.deltaValue = self.ui.deltaEdit.value()

            self.delta = pg.CurvePoint(self.curve)
            self.plot.addItem(self.delta)
            self.deltaArrow = pg.ArrowItem(angle=270)
            self.deltaArrow.setParentItem(self.delta)
            self.deltaText = pg.TextItem("Delta:", anchor=(0.5, 1.5))
            self.deltaText.setParentItem(self.delta)

        elif state == 0:
            self.DELTA = False
            self.ui.deltaEdit.setDisabled(True)
            self.plot.removeItem(self.delta)
            self.delta.deleteLater()
            self.delta = None

    @pyqtSlot(float)
    def onDeltaEdit(self, freq):
        self.deltaIndex = None
        self.deltaValue = freq

    # MAX HOLD
    @pyqtSlot(int)
    def onHold(self, state):
        if state == 2:
            self.HOLD = True
            self.holdCurve = self.plot.plot(pen='r')
            self.plot.addItem(self.holdCurve)
            self.holdData = None
        elif state == 0:
            self.HOLD = False
            self.holdData = None
            self.plot.removeItem(self.holdCurve)

    # AVERAGE
    @pyqtSlot(int)
    def onAvg(self, state):
        if state == 2:
            self.AVERAGE = True
            self.numAvg = self.ui.avgEdit.value()
            self.avgArray = None
            self.avgCounter = 0
        elif state == 0:
            self.AVERAGE = False
            self.numAvg = None
            self.avg = []

    @pyqtSlot(float)
    def onAvgEdit(self, num):
        self.numAvg = num
        self.avgArray = None
        self.avgCounter = 0

    # PEAK
    @pyqtSlot(int)
    def onPeak(self, state):
        if state == 2:
            self.PEAK = True
            self.peak = pg.CurvePoint(self.curve)
            self.plot.addItem(self.peak)
            self.peakArrow = pg.ArrowItem(angle=270)
            self.peakArrow.setParentItem(self.peak)
            self.peakText = pg.TextItem("Peak:", anchor=(0.5, 1.5))
            self.peakText.setParentItem(self.peak)

        elif state == 0:
            self.PEAK = False
            self.plot.removeItem(self.peak)
            self.peak.deleteLater()
            self.peak = None

    @QtCore.pyqtSlot()
    def onSave_1(self):
        self.SAVE[0] = True
        self.ui.traceButton_1.setDown(True)

    @QtCore.pyqtSlot()
    def onSave_2(self):
        self.SAVE[1] = True
        self.ui.traceButton_2.setDown(True)

    @QtCore.pyqtSlot()
    def onSave_3(self):
        self.SAVE[2] = True
        self.ui.traceButton_3.setDown(True)

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