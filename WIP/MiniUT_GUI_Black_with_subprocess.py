# -----------------------------------------------------------------------------
# Name:        MiniUT_GUI_Black
# Purpose:     See if we can run our program using a Tkinter button...
# Created:     7/25/2017
# Last Updated: 7/26/2017
#
# A black box testing GUI that uses our testing script
# -----------------------------------------------------------------------------
from Tkinter import *
import test_miniUT_RB_PS_66311B_copy_9 as tester
import tkFont
import time
import os
import re
import subprocess

import sys
class StdRedirector():
    def __init__(self, text_widget):
        self.text_space = text_widget

    def write(self, string):
        self.text_space.config(state= NORMAL)
        self.text_space.insert("end", string)
        self.text_space.see("end")
        #self.text_space.config(state= DISABLED)
        
class LTE_Test:
    def __init__ (self, master):
        self.master = master
        titleFont = tkFont.Font(family = "arial", size = 18, weight = tkFont.BOLD)
        self.bodyFont = tkFont.Font (family = "arial", size = 10)
        Title = Label(master, text="MiniUT PCBA ATS", font = titleFont )
        Title.grid(row = 0, column = 1)
        
        #Run test button
        self.testBtn = Button(master, text="Run Test", command=self.test)
        self.testBtn.grid(row = 3, column = 1)
        
        #Labels and Text for SN and COM
        COMLabel = Label (master, text = "COM for MiniUT: (format is 'COM#')", font = self.bodyFont)
        COMLabel.grid(row = 1, column = 0)
        SNLabel = Label (master, text = "Please enter the Serial Number", font = self.bodyFont)
        SNLabel.grid(row = 2, column = 0)
        
        self.COMWarning = Label (master, text = "Enter 'COM' followed by a digit",
                            fg = self.master.cget('bg'), font = self.bodyFont)
        self.COMWarning.grid(row = 1, column = 2, padx = 0)  
        self.SNWarning = Label (master, text = "Enter numbers",
                           fg = master.cget('bg'), font = self.bodyFont)
        self.SNWarning.grid(row = 2, column = 2) 
        
        self.COMText = StringVar()
        self.COMText.set ("COM#")
        self.COMText.trace('rw', self.validate)
        self.SNText = StringVar()
        self.SNText.trace('w', self.validate)
             
        
        #Entry for MiniUT COM       
        COMEntry = Entry(master, textvariable = self.COMText)
        COMEntry.grid (row = 1,column = 1)

        
        #Entry for SN
        SNEntry = Entry(master, textvariable = self.SNText)
        SNEntry.grid (row = 2, column = 1)       


        #Note: Need xterm
        #Trying to make a terminal
        #self.termf = Frame (self.master, height = 400, width = 500)
        #self.termf.grid(row = 11, column = 1)
        #self.wid = self.termf.winfo_id()
        #os.system('xterm -into %d -geometry 40x20 -sb &' % self.wid)
        
        #TODO TESTING
        text_frame = Frame (master, width = 700, height = 300)
        text_frame.grid(row = 8, column = 0, columnspan = 3)
        #text_box = Text(master, state= DISABLED, height = 20, width = 80)
        self.text_box = Text(text_frame, state= NORMAL, height = 20, width = 80, relief = "sunken")
        self.text_box.grid (row = 0, column = 0, columnspan = 3)
        scroll_text = Scrollbar (text_frame, command = self.text_box.yview)
        scroll_text.grid(row=0, column=4, sticky='nsew')
        self.text_box['yscrollcommand'] = scroll_text.set

        #sys.stdout = StdRedirector(self.text_box)
        #sys.stderr = StdRedirector(self.text_box)
        #######################################################
        
    #Restricts the input of the COM and SN to valid inputs
    def validate (self, *dummy):
        
        self.testBtn.config(state=(NORMAL if (re.match("^[0-9]*$", self.SNText.get())
                                          and self.SNText.get()
                                          and re.match("^(COM)[0-9]$", self.COMText.get()))
                            else DISABLED))  

  
                            
        if (re.match("^(COM)[0-9]$", self.COMText.get())):
            self.COMWarning.config(fg = self.master.cget('bg'))
        else:
            self.COMWarning.config(fg = 'red')

            
        if (re.match("^[0-9]*$", self.SNText.get()) and self.SNText.get()):
            self.SNWarning.config(fg = self.master.cget('bg'))
        else:
            self.SNWarning.config(fg = 'red')
    
    """
    def run_tester (self):
 
        child = subprocess.Popen(['python','-u','test_miniUT_RB_PS_66311B_copy_9.py'], stdout = subprocess.PIPE)
        #self.text_box.delete("1.0",END)
        print "Done!"
        for line in iter(child.stdout.readline,''):
        
            print "Done!"
            self.text_box.insert(INSERT, line)
            self.text_box.see(END)
            self.text_box.update_idletasks()
            child.stdout.close()
            child.wait()

        return child.returncode
    """    
        
    #Runs the LTE Test Script
    def test(self):
        print "Done!"   
        #Disable button during test run
        self.testBtn.config(state = 'disabled')
        
        #Delete old messages
        global num_of_tests 
        if num_of_tests > 0:
            for label in self.master.grid_slaves():
                if int(label.grid_info()["row"]) > 3 and int(label.grid_info()["row"]) < 8:
                    label.grid_forget()
        
        #Increment the number of tests run
        num_of_tests += 1
        
        startTime = time.time()
            
        #Set the COM for the miniUT
        tester.COM = self.COMText.get()
        #print tester.COM
        
        #Logic for SN
        #print self.SNText.get()
        tester.SN = self.SNText.get()
        
        testResult = Label (self.master, text = "Test is now running, please wait...", fg = 'blue', font = self.bodyFont)    
        testResult.grid(row = 4, column = 1)
        
        #Update window before script call
        self.master.update() 
        
        #Script call
        #RESULT = tester.main()
        #RESULT = self.run_tester
        child = subprocess.Popen(['python','-u','test_miniUT_RB_PS_66311B_copy_9.py'], stdout = subprocess.PIPE)
        #self.text_box.delete("1.0",END)
        for line in iter(child.stdout.readline,''):
            self.text_box.insert(INSERT, line)
            self.text_box.see(END)
            self.text_box.update_idletasks()
        
        child.stdout.close()
        RESULT = child.wait()
        print RESULT
        
        #Success
        if RESULT == 0:
            testResult.config (text = "Test passed", fg = 'green3', font = self.bodyFont)
            
            totalTime = time.time() - startTime
            timeTaken = Label (self.master, text = "Test runtime: " + str(int(totalTime)) + " seconds",
                               font = self.bodyFont )
            timeTaken.grid(row = 5, column = 1) 
            
            global num_of_passes
            num_of_passes += 1
            
        elif RESULT == tester.FREQ_ERROR:
            testResult.config(text = "Test failed", fg = 'red', font = self.bodyFont)
            errorLabel = Label (self.master, text = tester.FREQ_ERROR_MESSAGE, fg = 'red', font = self.bodyFont)
            errorLabel.grid(row = 5, column = 1)
        
        elif RESULT == tester.CALC_ERROR:
            testResult.config(text = "Test failed", fg = 'red', font = self.bodyFont)
            errorLabel = Label (self.master, text = tester.CALC_ERROR_MESSAGE, fg = 'red', font = self.bodyFont)
            errorLabel.grid(row = 5, column = 1)
            
        elif RESULT == tester.CONNECTION_ERROR:
            testResult.config(text = "Test failed", fg = 'red', font = self.bodyFont)
            errorLabel = Label (self.master, text = tester.CONNECTION_ERROR_MESSAGE, fg = 'red', font = self.bodyFont)
            errorLabel.grid(row = 5, column = 1)
        
        elif RESULT == tester.PS_ERROR:
            testResult.config(text = "Test failed", fg = 'red', font = self.bodyFont)
            errorLabel = Label (self.master, text = tester.PS_ERROR_MESSAGE, fg = 'red', font = self.bodyFont)
            errorLabel.grid(row = 5, column = 1)
        
        elif RESULT == tester.SERIAL_ERROR:
            testResult.config(text = "Test failed", fg = 'red', font = self.bodyFont)
            errorLabel = Label (self.master, text = tester.SERIAL_ERROR_MESSAGE, fg = 'red', font = self.bodyFont)
            errorLabel.grid(row = 5, column = 1)
            
        elif RESULT == tester.SPEC_ERROR:
            testResult.config(text = "Test failed", fg = 'red', font = self.bodyFont)
            errorLabel = Label (self.master, text = tester.SPEC_ERROR_MESSAGE, fg = 'red', font = self.bodyFont)
            errorLabel.grid(row = 5, column = 1)
            
        else:
            testResult.config(text = "Test failed", fg = 'red', font = self.bodyFont)        
        """    
        elif RESULT == tester.IMPORT_ERROR:
            testResult.config(text = "Test failed", fg = 'red', font = self.bodyFont)
            errorLabel = Label (self.master, text = tester.IMPORT_ERROR_MESSAGE, fg = 'red', font = self.bodyFont)
            errorLabel.grid(row = 4, column = 1)            
        """      
        
        #Displaying the total number of tests passed over the total number of tests run
        testDone = Label (self.master, text = "Test(s) passed: " + str(num_of_passes) + "/"
                   + str (num_of_tests), font = self.bodyFont)
        testDone.grid(row = 6, column = 1)
        
        #Enable button after test is finished
        self.testBtn.config(state = 'normal')

RESULT = 1 
num_of_tests = 0
num_of_passes = 0        
root = Tk( )
root.geometry ("700x600")
root.title("MiniUT PCBA ATS")
lte = LTE_Test(root)
root.mainloop( )