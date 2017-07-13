'''
Created on Aug 16, 2011

@author: aes
'''
from CmdGenAuto import *
from SERIAL.CMDHelper import *
class CmdGen(CmdGenAuto):
    '''
    classdocs
    '''
    def __init__(self,parent,cb):
        CmdGenAuto.__init__(self, parent)
        
        self.zwhelper = ZWHelper()
        names = self.zwhelper.getClassNames()
        shortnames= map(lambda q : q[14:],names)
        self.cmdClass.AppendItems(sorted(shortnames))
        #self.cmdClass.SetStringSelection("BASIC")
        #self.cmdClass.SetStringSelection("UART")
        self.cmdClass.SetSelection(0)
        
        #self.cmdClass.SetMaxSize((200,40))
        #self.cmd.SetMaxSize((200,40))
        
        self.Bind(wx.EVT_CHOICE, self.OnNewClass, self.cmdClass)
        self.Bind(wx.EVT_CHOICE, self.OnNewCmd, self.cmd)
        self.Bind(wx.EVT_BUTTON, self.OnSend)

        self.OnNewClass(None)
        self.cb = cb
        
    def OnNewClass(self, event):
        cmds= self.zwhelper.getCmdNames("COMMAND_CLASS_" + self.cmdClass.GetStringSelection())
        self.cmd.Clear()
        self.cmd.AppendItems(cmds)
        self.cmd.SetSelection(0)
        self.OnNewCmd(None)
        
    def OnNewCmd(self, event):
        n = self.zwhelper.getCmdNode("COMMAND_CLASS_" + self.cmdClass.GetStringSelection(),self.cmd.GetStringSelection())
        c = self.zwhelper.classCmdByName("COMMAND_CLASS_" + self.cmdClass.GetStringSelection(),self.cmd.GetStringSelection())
        pkt = pack("2B",c[0], c[1])
        helpStr = self.zwhelper.GetFullHelp(pkt);    
        self.properties.DestroyChildren()        
                      
        i=0
        self.proplist=[]
        for pn in n.getElementsByTagName("param"):
            
            name = pn.getAttribute("name")
            tt = pn.getAttribute("type")

            label = wx.StaticText(self.properties, -1, name)
            
            if(tt in ["BYTE","STRUCT_BYTE"] ):
                value = wx.TextCtrl(self.properties, -1, '00',  style=wx.TE_RIGHT)
            elif(tt =="WORD"):
                value = wx.TextCtrl(self.properties, -1, '0000',  style=wx.TE_RIGHT)
            elif(tt =="BIT_24"):
                value = wx.TextCtrl(self.properties, -1, '000000',  style=wx.TE_RIGHT)
            elif(tt =="DWORD"):
                value = wx.TextCtrl(self.properties, -1, '00000000',  style=wx.TE_RIGHT)
            elif(tt == "ARRAY"):
                a = pn.getElementsByTagName("arrayattrib")
                l = int(a[0].getAttribute("len"))
                
                value = wx.TextCtrl(self.properties, -1,  style=wx.TE_RIGHT)
                value.SetMaxLength(2*l)
                value.SetValue("00"*l)                
            else:
                value = wx.TextCtrl(self.properties, -1, '0',  style=wx.TE_RIGHT)
            #elif(tt =="STRUCT_BYTE"):
            #    value = wx.FlexGridSizer(cols=1)
            #    for bf in pn.getElementsByTagName("bitflag"):
            #        name = bf.getAttribute("flagname") 
            #        value.Add(wx.CheckBox(self.properties, -1, name))                
            #    for bf in pn.getElementsByTagName("bitfield"):
            #        name = bf.getAttribute("fieldname")                 
            #        value.Add(wx.TextCtrl(self.properties, -1, '00000000',  style=wx.TE_RIGHT))                


            self.prop_sizer.Add(label, 1, wx.EXPAND | wx.ALL, 5)
            self.prop_sizer.Add(value, 1, wx.EXPAND | wx.ALL, 5)
            
            self.proplist.append((name,tt,value))            
            i=i+1
        wx.StaticText( self.m_cmdText, wx.ID_ANY, "                                                                            ");
        wx.StaticText( self.m_cmdText, wx.ID_ANY, helpStr); 			
   
        self.GetParent().Layout()
        self.properties.SetupScrolling()

        
    def OnSend(self,event):
        c = self.zwhelper.classCmdByName("COMMAND_CLASS_" + self.cmdClass.GetStringSelection(),self.cmd.GetStringSelection())
        pkt = pack("2B",c[0], c[1])
        cmdStr = self.zwhelper.GetFullCmd(pkt);
        parStr = ""
        for (_,tt,value) in self.proplist:
            if tt == "INT":
                parStr += " " + str(int(value.GetValue(),10))
            else :
                parStr += " " + str(value.GetValue())
        cmdStr = cmdStr + parStr;
        wx.StaticText( self.m_cmdText, wx.ID_ANY, "                                                                            ");        
        wx.StaticText( self.m_cmdText, wx.ID_ANY, cmdStr);        
        #m_test =  wx.StaticText( self.properties, wx.ID_ANY, cmdStr);
        #m_test.Wrap( -1 );
        #self.bSizer6.Add( self.m_cmdText, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
        #self.bSizer5.Add( self.bSizer6, 0, wx.EXPAND, 5 )
        print("OnSend> " + cmdStr)
        self.cb(cmdStr)
            
        
