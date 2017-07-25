# -----------------------------------------------------------------------------
# Name:        LTE_GUI_Basic
# Purpose:     See if we can run our program using a Tkinter button...
# Created:     7/24/2017
# Last Updated: 7/24/2017
#
# -----------------------------------------------------------------------------
from Tkinter import *
import test_miniUT_crystal_rb as tester
RESULT = False


class LTE_Test:
    def __init__ (self, master):
        self.master = master
        Title = Label(master, text="LTE Test")
        Title.grid(row = 2, column = 1)
        testBtn = Button(master, text="Run Test", command=self.test)
        testBtn.grid(row = 4, column = 1)
        testRes = Label (master, text = "", fg = 'blue')
        testRes.grid(row = 6, column = 1)
        
        
    #Now takes in a parameter
    def test(self):
        testRes = Label (self.master, text = "Test is now running", fg = 'blue')
        testRes.grid(row = 6, column = 1)
        self.master.update() 
        RESULT = tester.main()
        if RESULT == True:
            testRes.config (text = "Test passed", fg = 'green', fb = 'white')
        else:
            testRes.config(text = "Test failed", fg = 'red', fb = 'white')
        
root = Tk( )
lte = LTE_Test(root)
root.mainloop( )