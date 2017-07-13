'''
Created on 21/06/2011

@author: aes
'''
import xml.dom.minidom
from struct import *

from Tkinter import *
from SERIAL.CMDHelper import *

import os

class ZWHelper(object):
    '''
    classdocs
    '''
    def getByKey(self,n,key):
        for c in n.childNodes:
            if(c.nodeType==c.ELEMENT_NODE and key == int(c.getAttribute("key"),16) ):
                return c
        return None

    def getByName(self,n,name):
        for c in n.childNodes:
            if(c.nodeType==c.ELEMENT_NODE and name == c.getAttribute("name") ):
                return c
        return None


    def __init__(self):
        if getattr(sys, 'frozen', None):
            basedir = sys._MEIPASS
        else:
            basedir = os.path.dirname(__file__)

        xmlfile = os.path.join(basedir,"Seial_custom_cmd_classes.xml")
        self.x = xml.dom.minidom.parse( xmlfile )
        
        self.classes = dict()
        for c in self.x.getElementsByTagName("cmd_class"):
            cls = int(c.getAttribute("key"),16)
            if (self.classes.has_key(cls)):
                if(int(c.getAttribute("version")) > int(self.classes[cls].getAttribute("version"))):
                    self.classes[cls] = c
            else:
                self.classes[cls] = c

        self.gentype = dict()
        for c in self.x.getElementsByTagName("gen_dev"):
            gen = int(c.getAttribute("key"),16)
            self.gentype[gen] = c


    def ZWToObj(self,zwcmd):
        i=0
        d = dict()        
        
        d["class"] = ord(zwcmd[i])
        d["cmd"] = ord(zwcmd[i+1])
        try:
            cls = self.classes[ord(zwcmd[i])]
        except KeyError:
            cls = None
            
        if(not cls):
            d["data"] = zwcmd[2:].encode("hex")
            return d

        cmd = self.getByKey(cls, ord(zwcmd[i+1]))

        if(not cmd):
            d["data"] = zwcmd[2:].encode("hex")
            return d

       
        offset = 2
        for p in cmd.getElementsByTagName("param"):
            att =  p.getAttribute("name")            
            type = p.getAttribute("type")
            
            if(offset >= len(zwcmd)):
                break

            if(type=="BYTE" or type=="STRUCT_BYTE"):
                d[att] = (ord(zwcmd[offset]))
                offset+=1
            elif(type=="WORD"):
                (v,) = unpack("!H",zwcmd[offset:offset+2])
                d[att] = v
                offset+=2
            elif(type=="DWORD"): 
                (v,) = unpack("!I",zwcmd[offset:offset+4])
                d[att] = v
                offset+=4
            elif(type=="VARIANT"):
                d[att] = zwcmd[offset:].encode("hex")
            else:
                d[att] = zwcmd[offset:].encode("hex")
        return d

    def getClassName(self,c):
        try:
            cls = self.classes[c]
            return cls.getAttribute("name")
        except KeyError:
            return "Unknown"

    def getTypeString(self,gen_type,spec_type):
        gen_name = "Unknown(%02x)" %(gen_type)
        spec_name = "Unknown(%02x)" %(spec_type)
        try:
            cls = self.gentype[gen_type]
            gen_name = cls.getAttribute("name")
            
            for c in cls.getElementsByTagName("spec_dev"):
                if(int(c.getAttribute("key"),16) == spec_type):
                    spec_name = c.getAttribute("name")
                    break
        except KeyError:
            pass
        
        return (gen_name,spec_name)
                
    def GetClassAndCmd(self,zwcmd):
        i=0
        s_class=""
        s_cmd=""
        
        try:
            cls = self.classes[ord(zwcmd[0])]
        except KeyError:
            cls = None
            
        if(not cls):
            s_class = "Unknown"
        s_class = cls.getAttribute("name");
        
        cmd = self.getByKey(cls, ord(zwcmd[1]))
        if(not cmd):
            s_cmd = "Unknown"
        s_cmd = cmd.getAttribute("name")
        return (s_class,s_cmd)
        
    def GetFullCmd(self,zwcmd):
        i=0
        s=""
        try:
            cls = self.classes[ord(zwcmd[i])]
        except KeyError:
            cls = None
            
        if(not cls):
            return s
        cmd = self.getByKey(cls, ord(zwcmd[i+1]))

        if(not cmd):
            return s

        s = cmd.getAttribute("command")
        print("GetFullCmd = " + s)
        return s

    def GetFullHelp(self,zwcmd):
        i=0
        s=""
        try:
            cls = self.classes[ord(zwcmd[i])]
        except KeyError:
            cls = None
            
        if(not cls):
            return s
        cmd = self.getByKey(cls, ord(zwcmd[i+1]))

        if(not cmd):
            return s

        s = cmd.getAttribute("help")
        print("GetFullHelp = " + s)
        return s        

    def ZWToStr(self,zwcmd):
        i=0
        s=""
        try:
            cls = self.classes[ord(zwcmd[i])]
        except KeyError:
            cls = None
            
        if(not cls):
            s+= "Unknown class " + hex(ord(zwcmd[i]))+ "\n"
            s+= "Unknown cmd " + hex(ord(zwcmd[i+1]))+ "\n"
            s+= "data:" + zwcmd[2:].encode("hex")
            return s
            
        s+="Class:" + cls.getAttribute("name")+"\n";
        cmd = self.getByKey(cls, ord(zwcmd[i+1]))

        if(not cmd):
            s+= "Unknown command " + hex(ord(zwcmd[i+1]))+ "  :"
            s+= zwcmd[2:].encode("hex")+"\n"
            return s

        s+="Command:"  +cmd.getAttribute("name")+"\n"
       
        offset = 2
        for p in cmd.getElementsByTagName("param"):
            s+= p.getAttribute("name")+": "
            tt = p.getAttribute("type")
            
            if(offset >= len(zwcmd)):
                s+= "Bad length"
                break
            try:
                if(tt=="BYTE" or tt=="STRUCT_BYTE"):                 
                    s+=hex(ord(zwcmd[offset])) + "\n"
                    offset+=1
                elif(tt=="WORD"):
                    (v,) = unpack("!H",zwcmd[offset:offset+2])
                    s+=hex( v )   + "\n"
                    offset+=2
                elif(tt=="DWORD"): 
                    (v,) = unpack("!I",zwcmd[offset:offset+4])
                    s+=hex(v) + "\n"
                    offset+=4
                elif(tt=="VARIANT"):
                    s+=str(map(hex,map(ord,zwcmd[offset:])))  + "\n"                
                else:
                    s+=str(map(hex,map(ord,zwcmd[offset:])))  + "\n"
            except Exception:
                None
        return s
    
    def getClassNames(self):
        l=[]
        for (c,v) in self.classes.items():
            l.append(v.getAttribute("name"))
        return l


    def getCmdNames(self,clsName):
        for (c,v) in self.classes.items():
            if(clsName == v.getAttribute("name")):
                return  map(lambda x:x.getAttribute("name") ,v.getElementsByTagName("cmd")) 
        return None
    
    def getCmdNode(self,clsName,cmdName):
        for (c,v) in self.classes.items():
            if(clsName == v.getAttribute("name")):
                return self.getByName(v, cmdName)
        None

    def classCmdByName(self,clsName,cmdName):
        for (c,v) in self.classes.items():
            if(clsName == v.getAttribute("name")):
                clv = int(v.getAttribute("key"),16)                
                cmv = int(self.getByName(v, cmdName).getAttribute("key"),16)                
                return (clv,cmv) 
        None

    def printNodeInfo(self,nif):
        print "Generic: ", 
        
    def hexstr2int(self, seq):
        '''
        Take a hex string and convert to list of int.
        E.g. '5c4201' -> [0x5c, 0x42, 0x01]
        '''
        return map(lambda x: int(x, 16), chunker(seq, 2))

        
class ZWSendCmdGUI():
    def __init__(self, master):
        self.zwhelper = ZWHelper()
    
        frame = Frame(master)
        frame.pack()
                
        self.cls = StringVar(frame)
        self.cls.set("COMMAND_CLASS_BASIC") # initial value   
        self.cls.trace("w",self.classSelected)


        self.cmd = StringVar(frame)
        self.cmd.set("BASIC_GET") # initial value   
        self.cmd.trace("w",self.cmdSelected)
        
        option = OptionMenu(frame, self.cls,*self.zwhelper.getClassNames())
        option.pack()


        self.cmdO = OptionMenu(frame, self.cmd,*self.zwhelper.getCmdNames(self.cls.get()))
        self.cmdO.pack()
        
        self.zwhelper.getCmdNames("COMMAND_CLASS_BASIC")
        
        
    def classSelected(self,*args):
        self.cmdO["menu"].delete(0, END)
        
        names = self.zwhelper.getCmdNames(self.cls.get())
        for i in names: #do magic... http://www.prasannatech.net/2009/06/tkinter-optionmenu-changing-choices.html
            self.cmdO["menu"].add_command(label=i, command=lambda temp = i: self.cmdO.setvar(self.cmdO.cget("textvariable"), value = temp))
        self.cmd.set(names[0])
        
    def cmdSelected(self,*args):
        print "select" , self.cmd.get()
        
        print self.zwhelper.getCmdNode(self.cls.get(),self.cmd.get()).toxml()
        

def chunker(seq, size):
    return (seq[pos:pos + size] for pos in xrange(0, len(seq), size))
       
if __name__ == '__main__':
    zh=ZWHelper()
    print zh.ZWToStr("5204000401000000d31601021402864f234d339834".decode("hex"))
    
    
    root = Tk()
    root.title("Z/IP client")
    app = ZWSendCmdGUI(root)      
    root.mainloop()
