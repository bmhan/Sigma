# -----------------------------------------------------------------------------
# Name:        test_3648A
# Purpose:     Test out the 3648A functionality
# Created:     7/20/2017
# Last Updated: 7/20/2017
#
# Testing out the commands we can use with the 3648A Power Supply
# More commands can be found on page 68 of the manual:
# http://www.fer.unizg.hr/_download/repository/Manual_E3646-90001.pdf
# -----------------------------------------------------------------------------

import visa
import time
VOLT = 2.5
CURR_LIMIT = 2

#Shows list of connected devices
rm = visa.ResourceManager()
print (rm.list_resources())

#Power Supply
my_instrument = rm.open_resource('GPIB0::9::INSTR')

#The command below is the same as:
#my_instrument.write('*IDN?')
#print(my_instrument.read())
print(my_instrument.query('*IDN?'))



#Select output 1
print ("Setting output 1...")
my_instrument.write(":INSTrument:SELect OUT1")
time.sleep(0.1)

#Select output 2
print ("Setting output 2...")
my_instrument.write(":INSTrument:SELect OUT2")
time.sleep(0.1)

#Set output on
print ("Turning on output...")
my_instrument.write(":OUTPUT:STATE ON")
time.sleep(0.1)

#Command to set the voltage and current limit
my_instrument.write(":APPL %f, %f" % (VOLT, CURR_LIMIT))
time.sleep(0.1)

#Measure voltage
print ("Measuring voltage...")
my_instrument.write(":MEAS:VOLT? ")
time.sleep(0.1)
print("My voltage is: " + my_instrument.read())

#Measure current
print ("Measuring current...")
my_instrument.write(":MEAS:CURR? ")
time.sleep(0.1)
print("My current is: " + my_instrument.read())

#Set output off
print ("Turning off output...")
my_instrument.write(":OUTPUT:STATE OFF")


