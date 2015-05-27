__author__ = 'maciek'

from PyQt4 import QtCore
from pylab import mlab
from matplotlib.mlab import psd, stride_windows, apply_window
import numpy as np
import time

class Worker(QtCore.QObject):
    abort = QtCore.pyqtSignal()
    dataReady = QtCore.pyqtSignal(object)

    def __init__(self, nfft, length, sliceLength, sampRate, nwelch, parent=None):
        super(Worker, self).__init__(parent)
        self.sampRate = sampRate
        self.nwelch = nwelch
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

        if len(samples)>nfft*(1+self.nwelch)/2:
            samples = samples[:nfft*(1+self.nwelch)/2]

        trash = length - sliceLength
        #print len(samples)
        samples = samples - offset
        samples = samples - np.mean(samples)
        #power, freqs = psd(samples, NFFT=nfft, pad_to=length, noverlap=nfft/2, Fs=sampRate/1e6, detrend=mlab.detrend_mean, window=mlab.window_hanning, sides = 'twosided')
        power, freqs = self.welch(samples, nfft, length, sampRate/1e6)
        power = np.reshape(power, len(power))

        freqs = freqs + center_freq/1e6
        power = power[trash/2:-trash/2]
        freqs = freqs[trash/2:-trash/2]

        power = 10*np.log10(power)
        #power = power - self.correction
        out = [index, power, freqs]
        self.dataReady.emit(out)

    def welch(self, x, nfft, pad_to, sampRate):
        window = mlab.window_hanning
        x = np.asarray(x)

        numFreqs = pad_to
        if pad_to % 2:
            freqcenter = (pad_to - 1)//2 + 1
        else:
            freqcenter = pad_to//2

        # Split input vector into slices
        temp = stride_windows(x, nfft, nfft/2, axis=0)

        # Apply window function
        temp, windowVal = apply_window(temp, window, axis=0, return_window=True)

        # Calculate window normalization
        S_1 = (np.abs(windowVal)).sum()

        # Calculate FFT
        power = np.fft.fft(temp, pad_to, axis=0)[:numFreqs, :]

        freqs = np.fft.fftfreq(pad_to, 1/sampRate)[:numFreqs]

        power = np.conjugate(power) * power
        power /= S_1**2

        freqs = np.concatenate((freqs[freqcenter:], freqs[:freqcenter]))
        power = np.concatenate((power[freqcenter:, :], power[:freqcenter, :]), 0)

        # Average the power spectra
        power = np.mean(power, axis=1)
        power = power.real

        return power, freqs

