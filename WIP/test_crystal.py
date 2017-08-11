# -----------------------------------------------------------------------------
# Name:        test_crystal
# Purpose:     Get the TXQuality data, sweeping the RB
# Created:     7/18/2017
# Last Updated: 7/21/2017
#
# NOTE: The program uses RF4A as the VSA port and STRM1A as the VSG port.
# test_crystal configures the Litepoint IQxstream machine to analyze the 782 MHz
# produced by the board.
#
# The program sweeps the values 0 through 1f for the frequency set
# in register 2c0.
#
# The program uses the socket_interface.py to initialize
# a connection to the board and send and receive data from IQxstream. The serial
# library is used to communicate to the board for testing. The visa library is used
# to communicate with the power supply to turn it on for the test and off after test
# is finished.
# -----------------------------------------------------------------------------
import socket_interface as scpi
import serial
import time
import visa
import csv
import sys
import os

HOST = '10.10.14.202'
PORT = 24000
FREQ_ERROR = 100000
VSA_FREQ = 782e6
EVM_LIMIT = 5
INPUT_CSV = 'input_rb_hex.csv'
#VSA_REF_LEVEL = 2
BLOCK_READ_SIZE = 1024
VOLT = 2.5
CURR_LIMIT = 2
freq_array = [0,1,2,3,4,5,6,7,8,9,'a', 'b', 'c', 'd', 'e', 'f', '1f']
#freq_array = ['a', 'b', 'c', 'd', 'e', 'f', '1f']
#RB_ARRAY = [1,2,3,4,5,6,8,9,10,12,15,16,18,20,24,25,27,30,32,36,40,45,48,
#50,54,60,64,72,75,80,81,90,96,100]


"""
Function returns if the signal frequency is within +/- 1000 Hz
return: 
    If the signal frequency is within +/- 1000 Hz 
"""
def measure_tx(): 

    print ("Performing Single Analysis...\n")
    # setup VSA, this can be done just once per signal type
    # assuming immediate trigger at the moment
    scpi.send('VSA; TRIG:SOUR IMM; SRAT 37.5e6; CAPT:TIME 20ms')	
    
	#Settings setup (taken from the SCPI Console)
	#CHAN1;LTE;CONF:RBC AUTO
	#CHAN1;LTE;CONF:BAND13
	#CHAN1;LTE;CONF:EARF:UL:cc1 23180
	#CHAN1;LTE;CONF:CID:cc 10
	#CHAN1;LTE;CONF:RNTI 1
	#VSA1;FREQ:cent 782000000
	#VSA1 ; RLEVel:AUTO
	#CHAN1;LTE;CONF:EARF:DL 5180
	
    scpi.send ('CHAN1;LTE;CONF:RBC AUTO')
    scpi.send('CHAN1;LTE;CONF:BAND 13')
    scpi.send('CHAN1;LTE;CONF:EARF:UL:cc1 23180')
    scpi.send('CHAN1;LTE;CONF:CID:cc 10')
    scpi.send('CHAN1;LTE;CONF:RNTI 1')
    scpi.send('VSA1;FREQ:cent 782000000')
    scpi.send('VSA1 ; RLEVel:AUTO')
    scpi.send('CHAN1;LTE;CONF:EARF:DL 5180')
    ret4 = scpi.send('*WAI; SYST:ERR:ALL?')
    print ("VSA Settings Status: " + ret4)
	
	# setup freq and ref. level
    #scpi.send('VSA; FREQ ' + str(freq))
    #scpi.send('RLEV ' + str(reference_level))

    
    # initiate a capture
    scpi.send('VSA; INIT')
    ret = scpi.send('*WAI; SYST:ERR:ALL?')
    
	#Delay in between initializing capture and calculation
    time.sleep(0.1)
    print ("Capture status: " + ret)

	
    # Calculate and fetch Average Power
	# Note that the result takes into account cable loss
    scpi.send('LTE; CLE:ALL; CALC:POW 0,20')
    time.sleep(0.1)
    ret2 = scpi.send('*WAI; SYST:ERR:ALL?')
	
    scpi.send('CALC:TXQ 0,10')
    time.sleep(0.1)
    ret3 = scpi.send('*WAI; SYST:ERR:ALL?')
    txq_array = scpi.send('FETC:TXQ:AVER?').replace(';', '').split(',')
	
    print ("Average_Frequency_Error: \t" + str(float(txq_array[2])))
    print ("Average_Data_EVM (%): \t\t\t" + str(float(txq_array[3])))
    """
    #Depreciated comparison logic
    #if int(power_arr[0]) == 0 and int(txq_array[0]) == 0:
    if float(txq_array[2]) < 1000 and float (txq_array[2]) > -1000:
        return True	
    else:
        return False
    """
    return (float(txq_array[2]),float(txq_array[3]))
	


"""
Function sets up socket connection to the IQxstream
"""
def setup_connection ():
    scpi.init(HOST, PORT)
    scpi.send('VSA; MRST; VSG; MRST; ROUT; MRST; LTE; MRST; CHAN1; CRST; *WAI; SYST:ERR:ALL?')

    vsg_port = 'STRM1A'
    vsa_port = 'RF4A'
	
    # setup RF port for VSA/VSG
    scpi.send('ROUT; PORT:RES:ADD ' + vsa_port + ', VSA')
    scpi.send('ROUT; PORT:RES:ADD ' + vsg_port + ', VSG')
	
    return scpi



"""
Function sets up the DUT to transmit the signal
"""
def setup_DUT():

    #Establish connection to DUT
    ser = serial.Serial('COM8', 115200, timeout = 5)

	
	
    print ("\nInitializing DUT...\n")
    ser.write("d 9\n")
    print("DUT response: " + ser.read(BLOCK_READ_SIZE))
	
    print ("Tx...\n")
    ser.write("d 20\n")
    print("DUT response: " + ser.read(BLOCK_READ_SIZE))
		
    #TODO: Put back later when testing board 53-0012-01
    #Set PA Bias Current to 9c 
    #ser.write("rffe_wrreg f 1 9c\n")
    #print("DUT response: " + ser.read(BLOCK_READ_SIZE))
    
    #print ("Gain and Offset...\n")
    #ser.write("d 27 -31 -36 904 914 0 -6\n")
    #ser.write("d 27 -14 11 4 14 0 -7\n")
    #print("DUT response: " + ser.read(BLOCK_READ_SIZE))
	
    return ser
	
	
	
"""
Main method performs the following:
	Set up the DUT board to transmit
	Sweeping through the array of RB values
	Set up the Litepoint machine to analyze 782 MHz
	Measure the average power and TX Quality of the transmitted
	signal.
	Returns the information through the terminal and two .csv
	files
"""
def main():
    
    #Setting up the Power Supply
    rm = visa.ResourceManager()
    power_supply = rm.open_resource('GPIB0::9::INSTR')
    
    print ("Setting output 1...")
    power_supply.write(":INSTrument:SELect OUT1")
    time.sleep(0.1)
    
    #Setting Power Supply current and limit
    power_supply.write(":APPL %f, %f" % (VOLT, CURR_LIMIT))
    time.sleep(0.1)
    
    #Turning on output
    print ("Turning on output...")
    power_supply.write(":OUTPUT:STATE ON")
    time.sleep(1)
    
    #One connection test
    scpi = setup_connection()
    
    freq_curr = FREQ_ERROR
    data_curr = EVM_LIMIT
    freq_char = ''

	#Setting up DUT before sending PUSCH signal
    ser = setup_DUT()

    print("Setting up RB and scale, sending PUSCH signal...\n")
    ser.write("d 35 " + str(16) + " 0 " + "179C\n")
    print("DUT response: " + ser.read(BLOCK_READ_SIZE))
     
    #Put back in when you switch back to "Brian" board
    #print ("Gain and Offset...\n")
    #ser.write("d 27 -14 11 4 14 0 -7\n")
    #print("DUT response: " + ser.read(BLOCK_READ_SIZE))
	
    for CSW_XOSC in freq_array:
        print ("Writing 2c0 "+ str(CSW_XOSC) + "28...\n")
        ser.write("wr 2c0 " + str(CSW_XOSC) + "28\n")
        print("DUT response: " + ser.read(BLOCK_READ_SIZE))		

        #TODO Optional command to check if the registers was actually written
        # ser.write("rd 2c0"\n")
        # print("DUT response: " + ser.read(BLOCK_READ_SIZE))		
	
        
	    #Measure the avg_power and txquality and return a tuple containing
        #the frequency error and the data EVM
        tuple = measure_tx()
		
        #Temporary stop procedure (uncomment to use)
        #Close socket connection to enable GUI access
        #Ask for raw_input to temporarily pause execution
        #scpi.close()    
        #raw_input("\n\n\tPress a key to Continue\t\n\n")

        if abs(tuple[0]) < abs(freq_curr) and abs (tuple[1]) < 5:
            freq_curr = tuple[0]
            data_curr = tuple[1]
            freq_char = CSW_XOSC

    #Turning on output
    print ("Turning off output...")
    power_supply.write(":OUTPUT:STATE OFF")
    time.sleep(3)
    
    #In the case where a right frequency setting is found, exits the entire script
    if (freq_curr == FREQ_ERROR):
        print ("\nNo frequency value found. Now exiting program")
        sys.exit()
    
    
    print ("\nYour frequency set value is " + str(freq_char) + " with an average frequency error of " + str(freq_curr)\
           + " and an average Data EVM of " + str(data_curr) + "\n")
   
    return freq_char

                
				
"""
    Automatic execution of main method on run of the script
"""
if __name__ == '__main__':
    main()