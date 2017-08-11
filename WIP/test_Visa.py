# -----------------------------------------------------------------------------
# Name:        test_Visa
# Purpose:     Look at the list of devices and determine which ones are needed
#              for the test
# Created:     8/2/2017
# Last Updated: 8/2/2017
#
# My personal test script, that contains logic to sweep all the connected 
# devices, and from IDN identification determine which ones are which power
# supply, multimeter.
# Sweeping DUT involves writing a command, and checking if their is a response
# from the board (or lack of a board).
# -----------------------------------------------------------------------------
import visa
import time
import serial
import re
    
power_supply1 = ""
power_supply2 = ""
power_supply3 = ""
com_num = ""
rm = visa.ResourceManager()
rm_list = rm.list_resources()
print (rm_list)
print (rm_list[0])

for item in rm_list:
    print item

for device in rm_list:
    if 'GPIB' in device:
        my_instrument = rm.open_resource(device)
        id = my_instrument.query('*IDN?')
    
        if '8845A' in id:
            power_supply1 = device
        if '66311B' in id:
            power_supply2 = device
        if 'E3648A' in id:
            power_supply3 = device

        
for device in rm_list:
    if 'ASRL' in device or 'COM' in device:
        
        COM_NUM = re.sub("[^0-9]","",device)
        print COM_NUM
        ser = serial.Serial('COM' + COM_NUM, 115200, timeout = 5)
        try:
            ser.write('hello?\n')
            response = ser.read(6)
            print response
            if len(response) > 0:
                com_num = COM_NUM
        except:
           print device + " is not the one" 
        
print "uArt: " + 'COM' + com_num
print "PS 1: " + power_supply1
print "PS 2: " + power_supply2
print "PS 3: " + power_supply3
