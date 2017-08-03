# -----------------------------------------------------------------------------
# Name:        flash_miniUT_GUI
# Purpose:     GUI to flash the miniUT
# Created:     8/3/2017
# Last Updated: 8/3/2017
#
# Here are some relevant links:
# How to send the file (workaround...)
# https://stackoverflow.com/questions/34299777/send-file-over-serial-port-from-python
# -----------------------------------------------------------------------------

import serial
from Tkinter import *
import tkFont
COM = 'COM8'
BLOCK_READ_SIZE = 1024
instruction = ("Before the program begins, make sure you put your firmware file"
                " in the same location as where you are \nrunning this program")
#Establish connection to DUT
ser = serial.Serial(COM, 115200, timeout = 5, xonxoff = True)


class FW_Test:
    def __init__ (self, master):   
        self.master = master
        titleFont = tkFont.Font(family = "arial", size = 18, weight = tkFont.BOLD)
        self.bodyFont = tkFont.Font (family = "arial", size = 10)
        Title = Label(master, text="Update Firmware", font = titleFont )
        Title.grid(row = 0, column = 1)
        Instruction = Label (master, text = instruction, font = self.bodyFont)
        Instruction.grid(row = 1, column = 0, columnspan = 3) 
        self.testBtn = Button (master, text = "update Firmware", command = self.update_FW)
        self.testBtn.grid(row = 2, column = 1)
        
        self.text_box = Text(master, state = NORMAL, height = 20, width = 80,
                              relief = "sunken")
        self.text_box.grid (row = 3, column = 0, columnspan = 3)
        
                                

    def update_FW (self):

        self.testBtn.config(state = 'disabled')
        
        #Update window before script call
        self.master.update()
        
        self.text_box.insert(INSERT,"Enabling all log print statements\n")
        ser.write("log 2\n")
        self.text_box.insert(INSERT,"DUT response: " + ser.read(BLOCK_READ_SIZE))
        self.text_box.insert(INSERT,"Trying to update fw\n")
        ser.write("updatefw\n")
        self.text_box.insert(INSERT,"DUT response: " + ser.read(BLOCK_READ_SIZE))

        self.text_box.insert(INSERT,"\nSending the file. Please wait 60 seconds for transfer to finish\n")
        ser.write(open("fw_20173107-1921.bin","rb").read())
        result = ser.read(BLOCK_READ_SIZE)
        self.text_box.insert (INSERT,"DUT Response: " + result)
        if ('success' in result):
            self.text_box.insert (INSERT,"Firmware Update succeeded!")
            self.text_box.insert (INSERT,"Please reset the miniUT now to use the new firmware")
        else:
            self.text_box.insert (INSERT,"Firmware Update failed. Try again")
            
        #Enable button after test is finished
        self.testBtn.config(state = 'normal')

root = Tk( )
root.geometry ("700x600")
root.title("Update miniUT Firmware")
lte = FW_Test(root)
root.mainloop( )