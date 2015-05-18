__author__ = 'maciek'

from PyQt4 import QtCore
from rtlsdr import RtlSdr
import time
import numpy as np

class Sampler(QtCore.QObject):
    samplerError = QtCore.pyqtSignal(object)
    dataAcquired = QtCore.pyqtSignal(object)

    def __init__(self, gain, sampRate, freqs, numSamples, parent=None):
        super(Sampler, self).__init__(parent)
        self.gain = gain
        self.sampRate = sampRate
        self.freqs = freqs
        self.numSamples = numSamples
        self.offset = 0
        self.sdr = None
        self.errorMsg = None

        self.WORKING = True
        self.BREAK = False
        self.MEASURE = False

        try:
            self.sdr = RtlSdr()
            self.sdr.set_manual_gain_enabled(1)
            self.sdr.gain = self.gain
            self.sdr.sample_rate = self.sampRate
        except IOError:
            self.WORKING = False
            print "Failed to initiate device. Please reconnect."
            self.errorMsg = "Failed to initiate device. Please reconnect."
            self.samplerError.emit(self.errorMsg)

    def sampling(self):
        print 'Starting sampler...'
        while self.WORKING:
            prev = 0
            counter = 0
            gain = self.gain
            numSamples = self.numSamples
            self.BREAK = False
            self.sdr.gain = gain
            start = time.time()
            #print self.sdr.get_gain()
            for i in range(len(self.freqs)):
                if self.BREAK:
                    break
                else:
                    centerFreq = self.freqs[i]
                    #print "frequency: " + str(center_freq/1e6) + "MHz"
                    if centerFreq != prev:
                        try:
                            self.sdr.set_center_freq(centerFreq)
                        except:
                            self.WORKING = False
                            print "Device failure while setting center frequency"
                            self.errorMsg = "Device failure while setting center frequency"
                            self.samplerError.emit(self.errorMsg)
                            break
                        prev = centerFreq
                    else:
                        pass

                    #time.sleep(0.01)
                    try:
                        x = self.sdr.read_samples(2048)
                        data = self.sdr.read_samples(numSamples)

                    except:
                        self.WORKING = False
                        print "Device failure while getting samples"
                        self.errorMsg = "Device failure while getting samples"
                        self.samplerError.emit(self.errorMsg)
                        break

                    if self.MEASURE:
                        self.offset = np.mean(data)

                    counter += 1
                    self.dataAcquired.emit([i, centerFreq, data])

        if self.errorMsg is not None:
            self.samplerError.emit(self.errorMsg)
        if self.sdr is not None:
            self.sdr.close()

