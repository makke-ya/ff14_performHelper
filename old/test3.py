import clr

clr.AddReference('System.Windows.Forms')
clr.AddReference('Microsoft.DirectX.DirectSound')

from System.Windows.Forms import *
from Microsoft.DirectX.DirectSound import *

class PlaySound(Form):
    def __init__(self, soundFile):
        self.device = Device()
        self.device.SetCooperativeLevel(self, CooperativeLevel.Normal)

        self.buffer = SecondaryBuffer(soundFile, self.device)
        self.buffer.Play(0 ,BufferPlayFlags.Default)

    def Dispose(self, disposing):
        if(disposing):
            if(self.buffer):
                self.buffer.Stop()
                self.buffer.Dispose()

            if(self.device):
                self.device.Dispose()

        Form.Dispose(self, disposing)

Application.Run(PlaySound("wav/a.wav"))