# -----------------------------------------------------------------------------
# Name:        LTE_GUI_Basic
# Purpose:     See if we can run our program using a Tkinter button...
# Created:     7/24/2017
# Last Updated: 7/25/2017
#
# A grey box testing GUI that uses test_miniUT_RB_PS_66311B as the testing script
# -----------------------------------------------------------------------------
from Tkinter import *
import test_miniUT_RB_PS_66311B as tester
import tkFont
RESULT = False


class LTE_Test:
    def __init__ (self, master):
        self.master = master
        titleFont = tkFont.Font(family = "arial", size = 16, weight = tkFont.BOLD)
        Title = Label(master, text="MiniUT PCBA ATS", font = titleFont )
        Title.grid(row = 0, column = 1)
        
        
        #Debugging Checkbox
        self.debugVal = IntVar()
        Debug = Checkbutton (master, text = "Enable Debugging", variable = self.debugVal)
        Debug.grid (row = 1, column = 0)
        
        #SN
        SNLabel = Label (master, text = "Please enter the Serial Number")
        SNLabel.grid(row = 2, column = 0)
        self.SNText = StringVar()
        self.SNText.set ("N/A")
        SNEntry = Entry(master, textvariable = self.SNText)
        SNEntry.grid (row = 2, column = 1)
 
 
        #Starting gain
        start_Gain_Label = Label (master, text = "Start Gain")
        start_Gain_Label.grid(row = 4, column = 0)
        self.start_Gain_Text = StringVar()
        self.start_Gain_Text.set ("4")
        self.start_Gain_Entry = Entry(master, textvariable = self.start_Gain_Text, state = "disabled")
        self.start_Gain_Entry.grid (row = 4, column = 1)
        
        #End gain
        end_Gain_Label = Label (master, text = "End Gain")
        end_Gain_Label.grid(row = 5, column = 0)
        self.end_Gain_Text = StringVar()
        self.end_Gain_Text.set ("70")
        self.end_Gain_Entry = Entry(master, textvariable = self.end_Gain_Text, state = "disabled")
        self.end_Gain_Entry.grid (row = 5, column = 1)
        
        
        #Customize gain range
        self.gainVal = IntVar()
        gainEnable = Checkbutton (master, text = "Enable Custom Gain Range", variable = self.gainVal,
                     command = lambda v = self.gainVal, s = self.start_Gain_Entry, e = self.end_Gain_Entry:
                     self.naccheck (v,s,e))
        gainEnable.grid (row = 3, column = 0)
        

        #Voltage
        volt_Label = Label (master, text = "Voltage")
        volt_Label.grid(row = 7, column = 0)
        self.volt_Text = StringVar()
        self.volt_Text.set ("2.5")
        self.volt_Entry = Entry(master, textvariable = self.volt_Text, state = "disabled")
        self.volt_Entry.grid (row = 7, column = 1)
        
        #Current
        current_Label = Label (master, text = "Current")
        current_Label.grid(row = 8, column = 0)
        self.current_Text = StringVar()
        self.current_Text.set ("2")
        self.current_Entry = Entry(master, textvariable = self.current_Text, state = "disabled")
        self.current_Entry.grid (row = 8, column = 1)
        
        #Customize power supply
        self.psVal = IntVar()
        psEnable = Checkbutton (master, text = "Enable Custom Power Supply Settings", variable = self.psVal,
                     command = lambda v = self.psVal, s = self.volt_Entry, e = self.current_Entry:
                     self.naccheck (v,s,e))
        psEnable.grid (row = 6, column = 0)
        
        
        #Run test button
        testBtn = Button(master, text="Run Test", command=self.test)
        testBtn.grid(row = 9, column = 1)

        
    def naccheck (self,var,start,end):
        if (var.get()== 0):
            start.config(state = 'disabled')
            end.config(state = 'disabled')
            #self.start_Gain_Entry.config(state = 'disabled')
            #self.end_Gain_Entry.config(state = 'disabled')
        else:
            start.config(state = 'normal')
            end.config(state = 'normal')
            #self.start_Gain_Entry.config(state = 'normal')
            #self.end_Gain_Entry.config(state = 'normal')

            
    #Runs the LTE Test Script
    def test(self):

        
        #Logic for Debugging
        print self.debugVal.get()
        if self.debugVal.get() == 1:
            print ("Calling set_Debug...\n")
            tester.DEBUG = True
        else:
            tester.DEBUG = False
            
        #Logic for SN
        print self.SNText.get()
        tester.SN = self.SNText.get()
        
        #Logic for Gain
        if (self.gainVal.get() == 0):
            tester.GAIN_TABLE = [0,1,2,3,4,5,10,20,30,40,50,60,70]
        else:
            tester.GAIN_TABLE = range (int(self.start_Gain_Text.get()),int(self.end_Gain_Text.get()))
        print tester.GAIN_TABLE
        
        #Logic for the Power Supply
        if (self.psVal.get() == 0):
            tester.VOLT = 2.5
            tester.CURR_LIMIT = 2
        else:
            tester.VOLT = float(self.volt_Text.get())
            tester.CURR_LIMIT = float(self.current_Text.get())
        print (str(tester.VOLT) + " " + str(tester.CURR_LIMIT) + "\n")
        
        #Calling the Test
        testResult = Label (self.master, text = "Test is now running", fg = 'blue')
        testResult.grid(row = 10, column = 1)
        self.master.update() 
        #RESULT = tester.main()
        if RESULT == True:
            testResult.config (text = "Test passed", fg = 'green', bg = 'white')
        else:
            testResult.config(text = "Test failed", fg = 'red', bg = 'white')
        
root = Tk( )
root.geometry ("500x500")
root.title("MiniUT PCBA ATS")
lte = LTE_Test(root)
root.mainloop( )