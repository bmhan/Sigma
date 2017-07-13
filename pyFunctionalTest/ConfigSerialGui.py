

import wx
from wx.lib.scrolledpanel import ScrolledPanel
import serial
import serial.tools.list_ports


class ConfigSerialGui(wx.Panel):
    def __init__(self, *args, **kwds):
        wx.Panel.__init__(self, *args, **kwds)
        gserial = serial.Serial()
        self.label_2 = wx.StaticText(self, -1, "Port")
        self.choice_port = wx.Choice(self, -1, choices=[])
        self.label_1 = wx.StaticText(self, -1, "Baudrate")
        self.combo_box_baudrate = wx.ComboBox(self, -1, choices=[], style=wx.CB_DROPDOWN)
        self.sizer_1_staticbox = wx.StaticBox(self, -1, "Basics")
        self.panel_format = wx.Panel(self, -1)
        self.label_3 = wx.StaticText(self.panel_format, -1, "Data Bits")
        self.choice_databits = wx.Choice(self.panel_format, -1, choices=["choice 1"])
        self.label_4 = wx.StaticText(self.panel_format, -1, "Stop Bits")
        self.choice_stopbits = wx.Choice(self.panel_format, -1, choices=["choice 1"])
        self.label_5 = wx.StaticText(self.panel_format, -1, "Parity")
        self.choice_parity = wx.Choice(self.panel_format, -1, choices=["choice 1"])
        self.sizer_format_staticbox = wx.StaticBox(self.panel_format, -1, "Data Format")
        self.panel_timeout = wx.Panel(self, -1)
        self.checkbox_timeout = wx.CheckBox(self.panel_timeout, -1, "Use Timeout")
        self.text_ctrl_timeout = wx.TextCtrl(self.panel_timeout, -1, "")
        self.label_6 = wx.StaticText(self.panel_timeout, -1, "seconds")
        self.sizer_timeout_staticbox = wx.StaticBox(self.panel_timeout, -1, "Timeout")
        self.panel_flow = wx.Panel(self, -1)
        self.checkbox_rtscts = wx.CheckBox(self.panel_flow, -1, "RTS/CTS")
        self.checkbox_xonxoff = wx.CheckBox(self.panel_flow, -1, "Xon/Xoff")
        
        self.connectCmd = wx.Button(self, wx.ID_OK, "Connect")
        self.Bind(wx.EVT_BUTTON, self.OnConnect)
         
        self.sizer_flow_staticbox = wx.StaticBox(self.panel_flow, -1, "Flow Control")
        self.sizer_flow_staticbox.Lower()


        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        
        sizer_flow = wx.StaticBoxSizer(self.sizer_flow_staticbox, wx.HORIZONTAL)
        self.sizer_timeout_staticbox.Lower()
        sizer_timeout = wx.StaticBoxSizer(self.sizer_timeout_staticbox, wx.HORIZONTAL)
        self.sizer_format_staticbox.Lower()
        sizer_format = wx.StaticBoxSizer(self.sizer_format_staticbox, wx.VERTICAL)
        grid_sizer_1 = wx.FlexGridSizer(3, 2, 0, 0)
        self.sizer_1_staticbox.Lower()
        sizer_1 = wx.StaticBoxSizer(self.sizer_1_staticbox, wx.VERTICAL)
        sizer_basics = wx.FlexGridSizer(3, 2, 0, 0)
        sizer_basics.Add(self.label_2, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
        sizer_basics.Add(self.choice_port, 0, wx.EXPAND, 0)
        sizer_basics.Add(self.label_1, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
        sizer_basics.Add(self.combo_box_baudrate, 0, wx.EXPAND, 0)
        sizer_basics.AddGrowableCol(1)
        sizer_1.Add(sizer_basics, 0, wx.EXPAND, 0)
        
        grid_sizer_1.Add(self.label_3, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
        grid_sizer_1.Add(self.choice_databits, 1, wx.EXPAND | wx.ALIGN_RIGHT, 0)
        grid_sizer_1.Add(self.label_4, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
        grid_sizer_1.Add(self.choice_stopbits, 1, wx.EXPAND | wx.ALIGN_RIGHT, 0)
        grid_sizer_1.Add(self.label_5, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
        grid_sizer_1.Add(self.choice_parity, 1, wx.EXPAND | wx.ALIGN_RIGHT, 0)
        sizer_format.Add(grid_sizer_1, 1, wx.EXPAND, 0)
        self.panel_format.SetSizer(sizer_format)
        
        sizer_timeout.Add(self.checkbox_timeout, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
        sizer_timeout.Add(self.text_ctrl_timeout, 0, 0, 0)
        sizer_timeout.Add(self.label_6, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
        self.panel_timeout.SetSizer(sizer_timeout)
        
        sizer_flow.Add(self.checkbox_rtscts, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
        sizer_flow.Add(self.checkbox_xonxoff, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
        sizer_flow.Add((10, 10), 1, wx.EXPAND, 0)
        self.panel_flow.SetSizer(sizer_flow)
        sizer_2.Add(sizer_1, 0, wx.EXPAND, 0)
        
        sizer_2.Add(self.panel_format, 0, wx.EXPAND, 0)
        sizer_2.Add(self.panel_timeout, 0, wx.EXPAND, 0)
        sizer_2.Add(self.panel_flow, 0, wx.EXPAND, 0)
        sizer_2.Add(self.connectCmd, 0, 0, 0)
		
        
        self.SetSizer( sizer_2 );
        self.Layout();
        #Set property        
        self.choice_port.Clear()
        self.ports = []
        for (portname, desc, hwid) in (sorted(serial.tools.list_ports.comports())):
            self.choice_port.Append(u'{} - {}'.format(portname, desc))
            self.ports.append(portname)
        self.choice_port.SetSelection(0)
        
        self.combo_box_baudrate.Clear()
        for baudrate in gserial.BAUDRATES:
            self.combo_box_baudrate.Append(str(baudrate))
        self.combo_box_baudrate.SetValue(u'{}'.format(gserial.baudrate))

        self.choice_databits.Clear()
        n = 0
        for bytesize in gserial.BYTESIZES:
            self.choice_databits.Append(str(bytesize))
            if gserial.bytesize == bytesize:
                index = n
            n = n + 1
        self.choice_databits.SetSelection(index)
        
        n = 0
        self.choice_stopbits.Clear()
        for stopbits in gserial.STOPBITS:
            self.choice_stopbits.Append(str(stopbits))
            if gserial.stopbits == stopbits:
                index = n
            n = n + 1
        self.choice_stopbits.SetSelection(index)
        
        n = 0
        self.choice_parity.Clear()
        for parity in gserial.PARITIES:
            self.choice_parity.Append(str(serial.PARITY_NAMES[parity]))
            if gserial.parity == parity:
                index = n
        self.choice_parity.SetSelection(index)
        
        if gserial.timeout is None:
            self.checkbox_timeout.SetValue(False)
            self.text_ctrl_timeout.Enable(False)
        else:
            self.checkbox_timeout.SetValue(True)
            self.text_ctrl_timeout.Enable(True)
            self.text_ctrl_timeout.SetValue(str(gserial.timeout))
       
        #export
        #self.connectCmd = connectCmd
        self.serial = gserial
# end of class CmdGenAuto
