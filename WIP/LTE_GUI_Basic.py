# -----------------------------------------------------------------------------
# Name:        LTE_GUI_Basic
# Purpose:     See if we can run our program using a Tkinter button...
# Created:     7/24/2017
# Last Updated: 7/24/2017
#
# -----------------------------------------------------------------------------
from Tkinter import *
import test_miniUT_gain_rb_version_with_cur as tester

class Example3:
    def __init__ (self, master):
        self.lbl = Label(master, text="Press the button below to run the test!")
        self.lbl.pack()
        self.btn = Button(master, text="Run Test", command=self.test)
        self.btn.pack()

    #Now takes in a parameter
    def test(self):
        tester.main()

root = Tk( )
ex3 = Example3(root)
root.mainloop( )
