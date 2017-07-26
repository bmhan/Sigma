# -----------------------------------------------------------------------------
# Name:        MiniUT_GUI_Black
# Purpose:     See if we can run our program using a Tkinter button...
# Created:     7/25/2017
# Last Updated: 7/25/2017
#
# A black box testing GUI that uses our testing script
# -----------------------------------------------------------------------------
from Tkinter import *
import test_miniUT_RB_PS_66311B_copy_9 as tester
import tkFont
import time
import os
import re

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
        
        #Entry for MiniUT COM
        COMLabel = Label (master, text = "COM for MiniUT: (format is 'COM#')", font = self.bodyFont)
        COMLabel.grid(row = 1, column = 0)
        self.COMText = StringVar()
        self.COMText.trace('w', self.validateCOM)
        self.COMWarning = Label (master, text = "Enter 'COM' followed by a digit",
                            fg = self.master.cget('bg'), font = self.bodyFont)
        self.COMWarning.grid(row = 1, column = 2, padx = 0)        
        self.COMText.set ("COM#")
        COMEntry = Entry(master, textvariable = self.COMText)
        COMEntry.grid (row = 1,column = 1)

        
        #SN
        SNLabel = Label (master, text = "Please enter the Serial Number", font = self.bodyFont)
        SNLabel.grid(row = 2, column = 0)
        self.SNText = StringVar()
        self.SNText.trace('w', self.validateSN)
        SNEntry = Entry(master, textvariable = self.SNText)
        SNEntry.grid (row = 2, column = 1)
        self.SNWarning = Label (master, text = "Enter letters and numbers",
                           fg = master.cget('bg'), font = self.bodyFont)
        self.SNWarning.grid(row = 2, column = 2)        


        #Note: Need xterm
        #Trying to make a terminal
        #self.termf = Frame (self.master, height = 400, width = 500)
        #self.termf.grid(row = 3, column = 1)
        #self.wid = self.termf.winfo_id()
        #os.system('xterm -into %d -geometry 40x20 -sb &' % self.wid)
        
    #Restricts the input of the COM to valid inputs
    def validateCOM (self, *dummy):
        
        self.testBtn.config(state=((NORMAL and self.COMWarning.config(fg = self.master.cget('bg'))) 
        if re.match("^(COM)[0-9]*$", self.COMText.get()) else (DISABLED
        and self.COMWarning.config(fg = 'red'))))
    
    
    #Restricts the input of the SN to valid inputs
    def validateSN (self,*dummy):   
        self.testBtn.config(state=((NORMAL and self.SNWarning.config(fg = self.master.cget('bg')))
        if re.match("^[a-z]*[A-Z]*[0-9]*$", self.SNText.get()) else (DISABLED
        and self.SNWarning.config(fg = 'red'))))        
    
    
    #Runs the LTE Test Script
    def test(self):
    
        #Disable button during test run
        self.testBtn.config(state = 'disabled')
        
        #Delete old messages
        global num_of_tests 
        if num_of_tests > 0:
            for label in self.master.grid_slaves():
                if int(label.grid_info()["row"]) > 3:
                    label.grid_forget()
        
        #Increment the number of tests run
        num_of_tests += 1
        
        startTime = time.time()
            
        #Set the COM for the miniUT
        tester.COM = self.COMText.get()
        print tester.COM
        
        #Logic for SN
        print self.SNText.get()
        tester.SN = self.SNText.get()
        
        testResult = Label (self.master, text = "Test is now running, please wait...", fg = 'blue', font = self.bodyFont)    
        testResult.grid(row = 4, column = 1)
        
        #Update window before script call
        self.master.update() 
        
        #Script call
        RESULT = tester.main()
        
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

RESULT = 0 
num_of_tests = 0
num_of_passes = 0        
root = Tk( )
root.geometry ("600x300")
root.title("MiniUT PCBA ATS")
lte = LTE_Test(root)
root.mainloop( )