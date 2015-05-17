__author__ = 'maciek'

from PyQt4 import QtCore
from pylab import mlab
from matplotlib.mlab import psd
import numpy as np
import time

class Worker(QtCore.QObject):
    abort = QtCore.pyqtSignal()
    dataReady = QtCore.pyqtSignal(object)

    def __init__(self, nfft, length, slice_length, samp_rate, parent=None):
        super(Worker, self).__init__(parent)
        self.samp_rate = samp_rate
        self.nfft = nfft
        self.length = length
        self.slice_length = slice_length
        self.WORKING = True
        self.offset = 0
        self.correction = 0

    def work(self, data):
        nfft = self.nfft
        length = self.length
        slice_length = self.slice_length
        samp_rate = self.samp_rate
        offset = self.offset
        index = data[0]
        center_freq = data[1]
        samples = data[2]
        if len(samples)>2*length:
            samples = samples[:2*length]
        trash = length - slice_length
        #print len(samples)
        samples = samples - offset
        samples = samples - np.mean(samples)
        power, freqs = psd(samples, NFFT=nfft, pad_to=length, noverlap=self.nfft/2, Fs=samp_rate/1e6, detrend=mlab.detrend_none, window=mlab.window_hanning, sides = 'twosided')
        power = np.reshape(power, len(power))
        freqs = freqs + center_freq/1e6
        power = power[trash/2:-trash/2]
        freqs = freqs[trash/2:-trash/2]
        power = 10*np.log10(power)
        power = power - self.correction
        out = [index, power, freqs]
        self.dataReady.emit(out)
