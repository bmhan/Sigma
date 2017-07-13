#!/usr/bin/python
'''
Created on Jun 28, 2011

@author: aes
'''
import sys
from SERIAL.CMDHelper import *
import wx
from wx import xrc
import wx.lib.agw.toasterbox as toasterbox
#from wx._misc import ToolTip

from CmdGen import *
from ConfigSerial import *
from wx.lib.agw.toasterbox import TB_CAPTION


EVT_PACKAGE_SHOW = wx.NewEventType()
EVT_PKG_SHOW_EVENT = wx.PyEventBinder(EVT_PACKAGE_SHOW, 1)

#EVT_DISCOVER = wx.NewEventType()
#EVT_DISCOVER_EVENT = wx.PyEventBinder(EVT_DISCOVER, 1)


    
class ZWEvent(wx.PyCommandEvent):
    """Event to signal that a count value is ready"""
    def __init__(self, etype, eid, value=None):
        """Creates the event object"""
        wx.PyCommandEvent.__init__(self, etype, eid)
        self._value = value

    def GetValue(self):
        """Returns the value from the event.
        @return: the value of this event

        """
        return self._value

class MyToolBar(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, wx.Size(940, 700))
        #self.SetIcon(wx.Icon(os.path.realpath(os.path.dirname(sys.argv[0]))+'/App.ico', wx.BITMAP_TYPE_ICO))

        #self.serial = serial.Serial()
        vbox = wx.BoxSizer(wx.VERTICAL)        
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)

       
        self.configCmd = ConfigSerial(self)
        hbox2.Add(self.configCmd,1,wx.ALL | wx.EXPAND,5)
        
        genCmd = CmdGen(self,self.OnSendZWCmd)
        hbox2.Add(genCmd,1,wx.ALL | wx.EXPAND,5)
        
        vbox.Add(hbox2,1,wx.EXPAND,5)

        # The Text box        
        self.display = wx.TextCtrl(self, -1, '',wx.DefaultPosition, size=(-1, 100),  style=wx.TE_MULTILINE)
        vbox.Add(self.display,1,wx.ALL | wx.EXPAND,5)

        # The status bar
        self.SetSizer(vbox)
        self.SetAutoLayout(1)
        self.statusbar = self.CreateStatusBar()
        self.Centre()
        
        self.Bind(wx.EVT_TOOL, self.OnExit, id=8)

        self.Bind(wx.EVT_CLOSE, self.OnClose)
        
        self.Bind(EVT_PKG_SHOW_EVENT, self.displayPktEv)
                
        #init variables
        self.nm = None
        self.zc = None
        self.lastHost = ""
        self.zwhelper = ZWHelper()
        self.connections = []

    def BlockingWait(self,title,timeout=30,nolock=False):
        #''
        #Wait for operation to complete, will return true if the operation was cancled
        #''
        progress = wx.ProgressDialog(title, "Status", timeout*2, style=wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME)
        keepGoing = True;
        self.lock = True
        i=0
        while ((self.lock or nolock) and keepGoing and i < timeout*2):
            if wx.VERSION < (2,7,1,1):
                keepGoing = progress.Update(i)
            else:
                (keepGoing, skip) = progress.Update(i)
            wx.Usleep(500)
            i+=1
        progress.Destroy()
        self.lock=False
        return not keepGoing

    def BlockingWaitDone(self,pkt):   
        self.displayPkt(pkt)
        print "Unlock"
        self.lock = False
        
    def SetDefaultWaitDone(self, pkt, **kwargs):   
        self.displayPkt(pkt)
        src_ip = kwargs['source_ip']
        print 'new ip is', src_ip
        self.combo.SetSelection(self.combo.Append(src_ip))
        print "Unlock"
        self.lock = False
    def OnExit(self, event):
        self.Close()

    def OnClose(self,event):
        print "Bye bye"
        self.configCmd.OnClose()
        if(self.nm): self.nm.stop();
        self.Destroy()

    def displayPkt(self,pkt):
        evt = ZWEvent(EVT_PACKAGE_SHOW, -1, pkt)
        wx.PostEvent(self, evt)

        
    def displayPktEv(self,evt):
        pkt = evt.GetValue()
        #Refresh node list just to be sure       
        #print "displayPkt" 
        self.statusbar.SetStatusText("Got reply")
        self.display.AppendText("\n-----------------------------------\n" +self.zwhelper.ZWToStr(pkt))
        #self.OnNodeList(None)

    def OnSendZWCmd(self, cmdStr):
        print("OnSendZWCmd write cmd> " + cmdStr)
        if self.configCmd.serial.isOpen():
            self.configCmd.serial.write(str(cmdStr) + "\n")
class MyApp(wx.App):
    def OnInit(self):        
        frame = MyToolBar(None, -1, 'Py Peripheral Functional Test')
        frame.Show(True)        
        return True


if __name__ == '__main__':
    app = MyApp(0)
    app.MainLoop()
    

