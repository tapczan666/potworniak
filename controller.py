__author__ = 'maciek'

from pylibftdi import BitBangDevice
from PyQt4 import QtCore

class USBController():
    usbError = QtCore.pyqtSignal(object)

    def __init__(self):
        try:
            self.bb = BitBangDevice()
            self.bb.port = 0xFF
            self.state = self.bb.read_pins()
            self.attenuation = 0
            self.switch_1 = 1
            self.switch_2 = 1
            print self.state
        except:
            print "Failed to initialize USB controller. Please reconnect."
            errorMsg = "Failed to initialize USB controller. Please reconnect."
            #self.usbError.emit(errorMsg)


    def set_att(self, att):
        if att >=0 and att <=31:
            self.attenuation = att
            value = self.switch_1*32 + self.switch_2*64 + self.attenuation^0b11111
            self.bb.port = value
            self.state = self.bb.read_pins()
        else:
            print "Attenuation value out of range"


    def set_switches(self, a, b):
        if a in [0,1] and b in [0,1]:
            self.switch_1 = a
            self.switch_2 = b

            value = self.switch_1*32 + self.switch_2*64 + self.attenuation^0b11111
            self.bb.port = value
            self.state = self.bb.read_pins()
        else:
            print "Incorrent switch setting. Enter 0 or 1."