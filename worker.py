__author__ = 'maciek'

from PyQt4 import QtCore
from pylab import mlab
from matplotlib.mlab import psd, stride_windows
import numpy as np
import time

class Worker(QtCore.QObject):
    abort = QtCore.pyqtSignal()
    dataReady = QtCore.pyqtSignal(object)

    def __init__(self, nfft, length, sliceLength, sampRate, parent=None):
        super(Worker, self).__init__(parent)
        self.sampRate = sampRate
        self.nfft = nfft
        self.length = length
        self.sliceLength = sliceLength
        self.WORKING = True
        self.offset = 0
        self.correction = 0

    def work(self, data):
        nfft = self.nfft
        length = self.length
        sliceLength = self.sliceLength
        sampRate = self.sampRate
        offset = self.offset
        index = data[0]
        center_freq = data[1]
        samples = data[2]
        if len(samples)>2*length:
            samples = samples[:2*length]
        trash = length - sliceLength
        #print len(samples)
        samples = samples - offset
        #samples = samples - np.mean(samples)
        power, freqs = psd(samples, NFFT=nfft, pad_to=length, noverlap=nfft/2, Fs=sampRate/1e6, detrend=mlab.detrend_mean, window=mlab.window_hanning, sides = 'twosided')
        self.welch(samples, nfft, nfft/2)
        power = np.reshape(power, len(power))
        freqs = freqs + center_freq/1e6
        power = power[trash/2:-trash/2]
        freqs = freqs[trash/2:-trash/2]
        power = 20*np.log10(power)
        power = power - self.correction
        out = [index, power, freqs]
        self.dataReady.emit(out)

    def welch(self, x, nfft, noverlap):
        #window = mlab.window_hanning(nfft)

        # Split input vector into slices
        temp = stride_windows(x, nfft, noverlap, axis=1)
        print temp.shape
        # Apply window function

        # Calculate FFT

        # Correct for loss of power due to windowing

        # Average the power spectra


