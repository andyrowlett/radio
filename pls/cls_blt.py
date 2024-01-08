import os

class Blue:

    def __init__(self) :
        self.device = False
        self.marsh = '03:58:B6:D3:AA:8D'
        self.square = '00:11:67:AA:1D:61'
        os.system("bluetoothctl agent on")

    def connect(self, device):
        os.system("bluetoothctl connect %s" % device)
        self.device = device

    def disconnect(self):
        if self.device:
            os.system("bluetoothctl disconnect %s" % self.device)