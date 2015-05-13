__author__ = 'maciek'

from PyQt4 import QtCore
from rtlsdr import RtlSdr
import time
import numpy as np

class Sampler(QtCore.QObject):
    samplerError = QtCore.pyqtSignal(object)

    def __init__(self, gain, samp_rate, freqs, num_samples, parent=None):
        super(Sampler, self).__init__(parent)
        self.gain = gain
        self.samp_rate = samp_rate
        self.freqs = freqs
        self.num_samples = num_samples
        self.offset = 0

        self.WORKING = True
        self.BREAK = False
        self.MEASURE = False

        try:
            self.sdr = RtlSdr()
            self.sdr.set_manual_gain_enabled(1)
            self.sdr.gain = self.gain
            self.sdr.sample_rate = self.samp_rate
        except IOError:
            self.WORKING = False
            print "Failed to initiate device. Please reconnect."
            self.samplerError.emit("Failed to initiate device. Please reconnect.")