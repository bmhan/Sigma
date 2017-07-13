
import threading
from serial import SerialException
from ConfigSerialGui import *
class ConfigSerial(ConfigSerialGui):
    def __init__(self,parent):
        ConfigSerialGui.__init__(self, parent)
        self.Bind(wx.EVT_BUTTON, self.OnConnect)
        self.alive = threading.Event()
        self.thread = None
        self.parent = parent
        
    def OnConnect(self, events):
        success = True
        self.serial.port = self.ports[self.choice_port.GetSelection()]
        try:
            b = int(self.combo_box_baudrate.GetValue())
        except ValueError:
            with wx.MessageDialog(
                    self,
                    'Baudrate must be a numeric value',
                    'Value Error',
                    wx.OK | wx.ICON_ERROR) as dlg:
                dlg.ShowModal()
            success = False
        else:
            self.serial.baudrate = b

        self.serial.bytesize = self.serial.BYTESIZES[self.choice_databits.GetSelection()]
        self.serial.stopbits = self.serial.STOPBITS[self.choice_stopbits.GetSelection()]
        self.serial.parity = self.serial.PARITIES[self.choice_parity.GetSelection()]

        self.serial.rtscts = self.checkbox_rtscts.GetValue()
        self.serial.xonxoff = self.checkbox_xonxoff.GetValue()
        if success:
            if not self.serial.isOpen():
                print("Connected to Uart")
                try:
                    self.serial.open()
                    self.connectCmd.SetLabel('Disconnect')
                    self.StartThread()
                except SerialException:
                    with wx.MessageDialog(
                            self,
                            'Port already open',
                            'Value Error',
                            wx.OK | wx.ICON_ERROR) as dlg:
                        dlg.ShowModal()
            else:
                print("Disconnect to Uart")
                self.StopThread()
                self.serial.close()
                self.connectCmd.SetLabel('Connect')

    #thread to read uart
    def ComPortThread(self):
        while self.alive.isSet():
            response = self.serial.readline()
            response = unicode(response, errors='ignore')
            self.parent.display.AppendText(response)

    def StartThread(self):
        print("StartThread")
        self.thread = threading.Thread(target=self.ComPortThread)
        self.thread.setDaemon(1)
        self.alive.set()
        self.thread.start()
        self.serial.rts = True
        self.serial.dtr = True

    def StopThread(self):
        print("Stop Thread")
        if self.thread is not None:
            self.alive.clear()          # clear alive event for thread
            #self.thread.join()          # wait until thread has finished
            self.thread = None
    def OnClose(self):
        print("OnClose")
        self.StopThread()
        if self.serial.isOpen():
            self.serial.close()
