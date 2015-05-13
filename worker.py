__author__ = 'maciek'

from PyQt4 import QtCore
from pylab import mlab
from matplotlib.mlab import psd
import numpy as np
import time

class Worker(QtCore.QObject):
    abort = QtCore.pyqtSignal()

    def __init__(self, nfft, length, slice_length, samp_rate, parent=None):
        super(Worker, self).__init__(parent)
        self.samp_rate = samp_rate
        self.nfft = nfft
        self.length = length
        self.slice_length = slice_length
        self.WORKING = True
        self.offset = 0
        self.correction = 0