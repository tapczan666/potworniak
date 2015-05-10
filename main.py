__author__ = 'maciek'

import numpy as np
import pyqtgraph as pg
from ui import Interface
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import pyqtSlot

class Analyzer():
    def __init__(self):
        pass

    def setupUi(self):
        self.ui = Interface()


###INTERFACE FUNCTIONS###
    @pyqtSlot()
    def onStart(self):
        pass

    @pyqtSlot()
    def onStop(self):
        pass
