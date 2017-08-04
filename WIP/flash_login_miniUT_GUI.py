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
from threading import *
from Tkinter import *
import tkFileDialog
import tkFont
COM = 'COM8'
BLOCK_READ_SIZE = 1024
instruction = ("Before the program begins, make sure you put your firmware file"
                " in the same location as where you are \nrunning this program")
FW_FILE = "bin files"
FW_TYPE = "*.bin"
ALL_FILE = "all files"
ALL_TYPE = "*.*"

current_window = None

class Log_In:
    def __init__ (self):
        global current_window
        current_window = Toplevel (root)
        current_window.wm_protocol ("WM_DELETE_WINDOW", root.destroy)
        self.label = Label (current_window, text = "Example log in screen")
        self.label.grid (row = 0, column = 1)
        self.button = Button (current_window, text = "Log in", command = self.new_window)
        self.button.grid (row = 1, column = 1)
    
    def new_window(self):
        current_window.destroy()
        FW_Test()   
        
        
class FW_Test:
    def __init__ (self):
        global current_window
        current_window = Toplevel(root)
        
        #if the user kills the window using the window manager, exit the program
        current_window.wm_protocol ("WM_DELETE_WINDOW", root.destroy)
        
        #self.current_window = current_window
        titleFont = tkFont.Font(family = "arial", size = 18, weight = tkFont.BOLD)
        self.bodyFont = tkFont.Font (family = "arial", size = 10)
        Title = Label(current_window, text="Update Firmware", font = titleFont )
        Title.grid(row = 0, column = 1)
        
        FileLabel = Label (current_window, text = "Firmware file: ", font = self.bodyFont)
        FileLabel.grid(row = 1, column = 0)
        self.start_File_Text = StringVar()
        self.start_File_Text.set ("Enter filename here")
        FileEntry = Entry (current_window, textvariable = self.start_File_Text)
        FileEntry.grid(row = 1, column = 1)
        self.fileBtn = Button (current_window, text = "Select firmware file", command = self.openFile)
        self.fileBtn.grid(row = 1, column = 2)
        
        Instruction = Label (current_window, text = instruction, font = self.bodyFont)
        Instruction.grid(row = 2, column = 0, columnspan = 3) 

        #updateFirmware
        self.testBtn = Button (current_window, text = "update Firmware",command = self.update_FW)
        self.testBtn.grid(row = 3, column = 1)
        
        self.text_box = Text(current_window, state = NORMAL, height = 20, width = 80,
                              relief = "sunken")
        self.text_box.grid (row = 4, column = 0, columnspan = 3)
        
    def openFile(self):
        self.FW_name = tkFileDialog.askopenfilename (initialdir = "/", 
        title = "Select firmware file", filetypes = ((FW_FILE,FW_TYPE),(ALL_FILE,ALL_TYPE)))
        self.start_File_Text.set(self.FW_name)
        
    def set_FW(self):
        #Establish connection to DUT
        
        ser = serial.Serial(COM, 115200, timeout = 5, xonxoff = True)
        self.testBtn.config(state = 'disabled')
        
        #Update window before script call
        self.current_window.update()
        
        self.text_box.insert(INSERT,"\nEnabling all log print statements\n")
        ser.write("log 2\n")
        self.text_box.insert(INSERT,"DUT response: " + ser.read(BLOCK_READ_SIZE))
        self.text_box.insert(INSERT,"Trying to update fw\n")
        ser.write("updatefw\n")
        self.text_box.insert(INSERT,"DUT response: " + ser.read(BLOCK_READ_SIZE))

        self.text_box.insert(INSERT,"\nSending the file. Please wait 60 seconds for transfer to finish\n")
        #ser.write(open("fw_20173107-1921.bin","rb").read())
        ser.write(open(self.start_File_Text.get(),"rb").read())
        result = ser.read(BLOCK_READ_SIZE)
        self.text_box.insert (INSERT,"DUT Response: " + result)
        if ('success' in result):
            self.text_box.insert (INSERT,"Firmware Update succeeded!\n")
            self.text_box.insert (INSERT,"Please reset the miniUT now to use the new firmware")
        else:
            self.text_box.insert (INSERT,"Firmware Update failed. Try again")
            
        #Enable button after test is finished
        self.testBtn.config(state = 'normal')
  
    
    def update_FW (self):

        t = Thread (target = self.set_FW,args = ())
        t.start()

root = Tk( )
root.geometry ("700x600")
root.title("Update miniUT Firmware")
root.withdraw()
window = Log_In()
root.mainloop( )