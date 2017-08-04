# -----------------------------------------------------------------------------
# Name:        test_miniUT_RB_PA_E3648A
# Purpose:     Get the TXQuality data, sweeping the PA mode, PA bias, PA vcc,
#              RB, and the Gain.
# Created:     8/3/2017
# Last Updated: 8/3/2017
#
# Simple Tera Term-like testing script; does not have crystal calibration 
# does not store the result; purely for Litepoint observation
# -----------------------------------------------------------------------------

import serial
import visa
import time
import socket_interface as scpi

DEBUG =  False
RESET_POWER = False
SET_LITEPOINT = False
BLOCK_READ_SIZE = 1024

COM = 'COM8'
PS_ADDRESS = 'GPIB0::9::INSTR'
HOST = '10.10.14.202'
PORT = 24000

#2.5 V for small board, 5 V for big 
VOLT = 2.5
CURR_LIMIT = 2

#From 0 to 1f
CSW = 'c'


#'7e' for low power // '7c' for high power
mode = '7c'

#Bias is '00' to 'fe'
bias = '9c'

#6a2 = pull high, 682 = pull low
ctrl_18 = '6a2'
ctrl_17 = '6a2'
ctrl_16 = '682'

#(In input_hex.txt file) 50 - 1758 // 16 - 179C // 1 - 97A0
RB = 50
HEX = 1758

# 4 - 70 Recommended by Sivan
gain = 0



"""
Method that sets up the power supply, 66311B
return - A power_supply object, or PS_ERROR if a connection to the
         power supply could not be established
"""
def setup_PS():
    #Setting up the Power Supply
    rm = visa.ResourceManager()
    power_supply = rm.open_resource(PS_ADDRESS)

    #Turning off power supply
    print ("Turning off output...")
    power_supply.write(":OUTPUT:STATE OFF")
    time.sleep(1)
    
    #Setting output 1
    #print ("Setting output 1...")
    power_supply.write(":INSTrument:SELect OUT1")
    time.sleep(0.1)  
    
    print ("Setting the voltage...\n")
    power_supply.write(":APPL %f, %f" % (VOLT, CURR_LIMIT))
    time.sleep(0.1)
 
    
    #Turning on output
    print ("Turning on output...")
    power_supply.write(":OUTPUT:STATE ON")
    time.sleep(1)
    
    return power_supply

    
    
"""
Set up connection
"""
def setup_Litepoint ():
    is_connected = scpi.init(HOST, PORT)
        
    scpi.send('VSA; MRST; VSG; MRST; ROUT; MRST; LTE; MRST; CHAN1; CRST; *WAI; SYST:ERR:ALL?')

    vsg_port = 'STRM1A'
    vsa_port = 'RF4A'
	
    # setup RF port for VSA/VSG
    scpi.send('ROUT; PORT:RES:ADD ' + vsa_port + ', VSA')
    scpi.send('ROUT; PORT:RES:ADD ' + vsg_port + ', VSG')
	
        # setup VSA, this can be done just once per signal type
    # assuming immediate trigger at the moment
    scpi.send('VSA; TRIG:SOUR IMM; SRAT 37.5e6; CAPT:TIME 20ms')	
    
    scpi.send ('CHAN1;LTE;CONF:RBC AUTO')
    scpi.send('CHAN1;LTE;CONF:BAND 13')
    scpi.send('CHAN1;LTE;CONF:EARF:UL:cc1 23180')
    scpi.send('CHAN1;LTE;CONF:CID:cc 10')
    scpi.send('CHAN1;LTE;CONF:RNTI 1')
    scpi.send('VSA1;FREQ:cent 782000000')
    scpi.send('VSA1 ; RLEVel:AUTO')
    scpi.send('CHAN1;LTE;CONF:EARF:DL 5180')
    ret4 = scpi.send('*WAI; SYST:ERR:ALL?')
    if DEBUG == True:
        print ("VSA Settings Status: " + ret4)
    
    
    
if (RESET_POWER == True):
    setup_PS()

if SET_LITEPOINT == True:
    setup_Litepoint()

#Establish connection to DUT
ser = serial.Serial(COM, 115200, timeout = 5)


print ("\nInitializing DUT...\n")
ser.write("d 9\n")
print("DUT response: " + ser.read(BLOCK_READ_SIZE))

print ("Tx...\n")
ser.write("d 20\n")
print("DUT response: " + ser.read(BLOCK_READ_SIZE))

print ("Writing 2c0...\n")
ser.write("wr 2c0 " + str(CSW) + "28\n")
if DEBUG == True:
    print("DUT response: " + ser.read(BLOCK_READ_SIZE))

print("Setting PA_Mode...\n")
ser.write("rffe_wrreg f 0 " + mode + "\n")        
if DEBUG == True:    
    print("DUT response: " + ser.read(BLOCK_READ_SIZE))     
    
print ("Setting PA Bias to " + bias + "...\n")
ser.write("rffe_wrreg f 1 " + bias + "\n")
if DEBUG == True:    
    print("DUT response: " + ser.read(BLOCK_READ_SIZE))      
    
#RFFEM_CTRL_18
ser.write ("memwrite A401B158 " + ctrl_18 + "\n")
if DEBUG == True:
    print("DUT response: " + ser.read(BLOCK_READ_SIZE))        

#RFFEM_CTRL_17
ser.write ("memwrite A401B13C " + ctrl_17 + "\n")
if DEBUG == True:
    print("DUT response: " + ser.read(BLOCK_READ_SIZE))       

#RFFEM_CTRL_16
ser.write ("memwrite A401B138 " + ctrl_16 + "\n")
if DEBUG == True:
    print("DUT response: " + ser.read(BLOCK_READ_SIZE))    
    
    
ser.write("d 35 " + str(RB) + " 0 " + str(HEX) + "\n")
if (DEBUG == True):
    print("DUT response: " + ser.read(BLOCK_READ_SIZE))
    
if (DEBUG == True):
    print ("Setting gain...")

ser.write("d 26 " + str(gain) + "\n")

if (DEBUG == True):
    print("DUT response: " + ser.read(BLOCK_READ_SIZE))
    
