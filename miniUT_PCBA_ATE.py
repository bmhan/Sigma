#!/usr/bin/env python
# -----------------------------------------------------------------------------
# Name:        MiniUT_GUI_shortened
# Purpose:     A GUI that runs miniUT_PCBA_ATE_script.py
# Created:     8/8/2017
# Last Updated: 8/9/2017
#
# -----------------------------------------------------------------------------


from Tkinter import *
import tkFont
import time
import os
import re
import subprocess
import sys
import json
        
        
        
class LTE_Test:
    def __init__ (self, master):
        self.master = master
        titleFont = tkFont.Font(family = "arial", size = 18, weight = tkFont.BOLD)
        self.bodyFont = tkFont.Font (family = "arial", size = 10)
        Title = Label(master, text="MiniUT PCBA ATE\nEnter key values", font = titleFont )
        Title.grid(row = 0, column = 0, columnspan = 4)
        
        #Run test button
        self.testBtn = Button(master, text="Run Test", command=self.test)
        self.testBtn.grid(row = 4, column = 2, pady=30)
        
        #Labels and Text for SN and HOST
        HOSTLabel = Label (master, text = "HOST for Litepoint: (Enter an IP Address)", font = self.bodyFont)
        HOSTLabel.grid(row = 1, column = 0)
        SNLabel = Label (master, text = "Please enter the Serial Number or Scan the Barcode", font = self.bodyFont)
        SNLabel.grid(row = 4, column = 0, pady=30)
        CABLELabel = Label (master, text = "Please enter the cable loss (in dB) for the LTE connection", font = self.bodyFont)
        CABLELabel.grid(row = 2, column = 0)
        
        self.HOSTWarning = Label (master, text = "Enter numbers and '.' only",
                            fg = self.master.cget('bg'), font = self.bodyFont)
        self.HOSTWarning.grid(row = 1, column = 2, padx = 0)  
        self.CABLEWarning = Label (master, text = "Enter numbers",
                           fg = master.cget('bg'), font = self.bodyFont)
        self.CABLEWarning.grid(row = 2, column = 2) 
        
        self.HOSTText = StringVar()
        self.HOSTText.trace('rw', self.validate)
        self.SNText = StringVar()
        self.SNText.trace('rw', self.validate)
        self.CABLEText = StringVar()
        self.CABLEText.trace('rw', self.validate)     
        
        #Entry for Litepoint HOST     
        HOSTEntry = Entry(master, textvariable = self.HOSTText)
        HOSTEntry.grid (row = 1,column = 1)

        
        #Entry for SN
        SNEntry = Entry(master, textvariable = self.SNText)
        SNEntry.grid (row = 4, column = 1, pady=30)    

        #Entry for CABLE_LOSS
        CABLEEntry = Entry(master, textvariable = self.CABLEText)
        CABLEEntry.grid (row = 2, column = 1)           

        #Reset all entries to default values
        defaultEnable = Button (master, text = "Set all key values to default",
                        command = self.setDefaults)
        defaultEnable.grid (row = 3, column = 3)
       
        #Reset all entries to previous values
        previousEnable = Button (master, text = "Set all key values to previous"
                + " test values",
                        command = self.setPrevious)
        previousEnable.grid (row = 2, column = 3)

        text_frame = Frame (master, width = 700, height = 300)
        text_frame.grid(row = 8, column = 0, columnspan = 4)
        self.text_box = Text(text_frame, state= NORMAL, height = 20, width = 80, relief = "sunken")
        self.text_box.grid (row = 0, column = 0, columnspan = 4)
        scroll_text = Scrollbar (text_frame, command = self.text_box.yview)
        scroll_text.grid(row=0, column=4, sticky='nsew')
        self.text_box['yscrollcommand'] = scroll_text.set


        
    #Restricts the input of the COM and SN to valid inputs
    def validate (self, *dummy):
        
        self.testBtn.config(state=(NORMAL if (re.match("^[A-Za-z0-9]*$", self.SNText.get())
                                          and self.SNText.get()
                                          and re.match("^[.0-9]*$", self.HOSTText.get())
                                          and self.HOSTText.get()
                                          and re.match("^[0-9]*$", self.CABLEText.get()))
                                          and self.CABLEText.get()
                            else DISABLED))  

  
                            
        if (re.match("^[.0-9]*$", self.HOSTText.get())):
            self.HOSTWarning.config(fg = self.master.cget('bg'))
        else:
            self.HOSTWarning.config(fg = 'red')
            
        if (re.match("^[0-9]*$", self.CABLEText.get())):
            self.CABLEWarning.config(fg = self.master.cget('bg'))
        else:
            self.CABLEWarning.config(fg = 'red')            
        

        
    #Sets the variable to default values
    #Runs the LTE Test Script
    def setDefaults(self):
       
        with open ("miniUT.setup", 'rb') as file:
            data = json.load(file)
            self.HOSTText.set(data["DEFAULT_HOST"])
            self.CABLEText.set(data["DEFAULT_CABLE_LOSS_DB"])
            self.SNText.set(data["DEFAULT_SN"])



    #Sets the variable to previous  values
    #Runs the LTE Test Script
    def setPrevious(self):
       
        with open ("miniUT.setup", 'rb') as file:
            data = json.load(file)
            self.HOSTText.set(data["HOST"])
            self.CABLEText.set(data["CABLE_LOSS_DB"])
            self.SNText.set(data["SN"])



    #Sets the variable to default values
    #Runs the LTE Test Script
    def test(self):

        global RESULT
        
        #Disable button during test run
        self.testBtn.grid_remove()

        #Delete old messages
        global num_of_tests 
        if num_of_tests > 0:
            for label in self.master.grid_slaves():
                if int(label.grid_info()["row"]) > 4 and int(label.grid_info()["row"]) < 8:
                    label.grid_forget()
        
        #Increment the number of tests run
        num_of_tests += 1
        
        startTime = time.time()
                   
        
        #Logic for changing SN, CABLE_LOSS_DB, HOST
        with open ("miniUT.setup", 'rb') as file:
            data = json.load(file)
            data["HOST"] = self.HOSTText.get()
            data["CABLE_LOSS_DB"] = self.CABLEText.get()
            data["SN"] = self.SNText.get()
            file.close()

        with open ("miniUT.setup", 'wb') as file:
            json.dump (data, file)
            file.close()
        
        testResult = Label (self.master, text = "Test is now running, please do not click on the screen while test is running.", fg = 'blue', font = self.bodyFont)    
        testResult.grid(row = 5, column = 1)
        
        #Update window before script call
        self.master.update() 
        
        
        #Script call
        #RESULT = tester.main()
        #RESULT = self.run_tester
        child = subprocess.Popen(['python','-u','miniUT_PCBA_ATE_script.py'], stdout = subprocess.PIPE)
        #self.text_box.delete("1.0",END)
        for line in iter(child.stdout.readline,''):
            if 'success' in line or 'Success' in line:
                RESULT = 0
            if 'Failed' in line or 'failed' in line:
                RESULT = -1
            self.text_box.insert(INSERT, line)
            self.text_box.see(END)
            self.text_box.update_idletasks()
            self.master.update()
        child.stdout.close()
        child.wait()
        print RESULT
        
        
        #Success
        if RESULT == 0:
            testResult.config (text = "Test completed", fg = 'green3', font = self.bodyFont)
            
            totalTime = time.time() - startTime
            timeTaken = Label (self.master, text = "Test runtime: " + str(int(totalTime)) + " seconds",
                               font = self.bodyFont )
            timeTaken.grid(row = 6, column = 1) 
            
            global num_of_passes
            num_of_passes += 1
        
        #Failure      
        else:
            testResult.config(text = "Test failed", fg = 'red', font = self.bodyFont)        
  
        
        #Displaying the total number of tests passed over the total number of tests run
        testDone = Label (self.master, text = "Test(s) completed: " + str(num_of_passes) + "/"
                   + str (num_of_tests), font = self.bodyFont)
        testDone.grid(row = 7, column = 1)
        
        #Add button after test is finished
        self.testBtn.grid()

        
RESULT = 0
num_of_tests = 0
num_of_passes = 0        
root = Tk( )
root.state('zoomed')
#root.geometry ("700x600")
root.title("MiniUT PCBA ATE")
lte = LTE_Test(root)
root.mainloop( )
