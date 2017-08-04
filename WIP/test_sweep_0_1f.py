# -----------------------------------------------------------------------------
# Name:        test_miniUT_crystal_rb
# Purpose:     Get the TXQuality data, sweeping the gains for an rb and rb offset
# Created:     7/24/2017
# Last Updated: 7/24/2017
#
# CHANGE SN BEFORE EVERY TEST!!!
# NOTE: The program uses RF4A as the VSA port and STRM1A as the VSG port.
# test_miniUT_crystal_rb configures the Litepoint IQxstream machine to analyze the
# 782 MHz produced by the board, sweeping the rb values and the gain values. 
# The program begins by calibrating the CSW 
# The program begins by prompting the user for a range of gain values to test.
# The result of the test is printed to terminal, and is stored in two .csv files -
# a sorted and unsorted .csv file
# The program uses the socket_interface.py to initialize
# a connection to the board and send and receive data from IQxstream. The serial
# library is used to communicate to the board for testing.
# -----------------------------------------------------------------------------
import socket_interface as scpi
import serial
import visa
import datetime
import time
import csv
import sys
import os
fieldnames = [
"Crystal","Average Power (dBm)",
"Average Frequency Error (Hz)", "Average IQ Offset (dB)",
"Average Data EVM (%)", "Average Peak Data EVM (%)",
"Average RS EVM (%)","Average Peak RS EVM (%)",
"Average IQ Imbalance Gain (dB)", "Average IQ Imbalance Phase (deg)",
"ACLR E-UTRA Lower (dB)", "ACLR E-UTRA Upper (dB)", "Current (A)"]
HOST = '10.10.14.202'
PORT = 24000
COM = 'COM8'
VSA_FREQ = 782e6
CABLE_LOSS_DB = 11
VOLT = 2.5 #TODO CHANGE
CURR_LIMIT = 2
FREQ_ERROR = 100000
FREQ_DELTA = 2000
FREQ_ACC = 1000
EVM_LIMIT = 6
CSW = ""
#DUT = "miniUT Rev E8"
DUT = "UT PROTO"
#SN = "10" #TODO CHANGE
SN = "UT PROTO 1"
CSV = "RB_50_miniUT_11_Sweep_crystal.csv"
INPUT_CSV = 'input_rb_hex.csv'
GAIN_START = 4
GAIN_STOP = 70
BLOCK_READ_SIZE = 1024
RB = 50
HEX = 1758
table = [0,1,2,3,4,5,10,20,30,40,50,60,70]
#freq_array = ['1f','1e', '1d', '1c', '1b', '1a', '19', '18', '17', '16', '15', '14', '13', '12', '11', '10',
#              'f','d','e','c','b','a', '9', '8', '7', '6', '5', '4', '3', '2', '1', '0']
freq_array = ['0','1','2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', '10', '11', '12',
               '13', '14', '15', '16', '17', '18', '19', '1a', '1b', '1c', '1d', '1e', '1f']
CSW_CENTER = '9'
#freq_array = ['f','e','d','c','b','a']

#Set this value to True if you want more debug statements
DEBUG = False




"""
Function returns a dictionary of information on a given signal.
params:
    rb - The RB value
    hex - The scale
    rb_offset - The start rb offset
    power_supply - The power supply
return: 
    Dictionary of information 
"""
def measure_tx(crystal,rb, hex, gain, rb_offset,power_supply): 
    if (power_supply != 0):
        print ("Performing Analysis for rb " + str(rb) + "\tscaling " + str(hex) + "\tgain " + str(gain) + "\trb offset " + str(rb_offset) + "...\n")


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
    if DEBUG == True:
        print ("VSA Settings Status: " + ret4)
        
    # initiate a capture
    scpi.send('VSA; INIT')
    ret = scpi.send('*WAI; SYST:ERR:ALL?')
    
	#Delay in between initializing capture and calculation
    if (DEBUG == True):
        print ("Capture status: " + ret)

    #Calculating and fetching Average Power
	#Note that this result takes into account cable loss
    result_dict = {}
    scpi.send('LTE; CLE:ALL; CALC:POW 0,20')
    ret2 = scpi.send('*WAI; SYST:ERR:ALL?')
    if (DEBUG == True):
        print ("Average Power Calculation status: " + ret2)
    power_arr = scpi.send('FETC:POW:AVER?').replace(';', '').split(',')
    result_dict['Average Power (dBm)'] = round(round(float(power_arr[1]),2),2) + CABLE_LOSS_DB  
	
    
	#Calculating and fetching TXQuality
    scpi.send('CALC:TXQ 0,10')
    ret3 = scpi.send('*WAI; SYST:ERR:ALL?')
    if (DEBUG == True):
        print ("TXQuality status: " + ret3)
    txq_array = scpi.send('FETC:TXQ:AVER?').replace(';', '').split(',')
    
	
    #Calculating Spectrum and fetching E-UTRA Lower and Upper
    scpi.send('CALC:SPEC 0,20')
    ret4 = scpi.send('*WAI; SYST:ERR:ALL?')
    if (DEBUG == True):
        print ("ACLR status: " + ret4)
    scpi.send('FORM:READ:DATA ASC')
    ret5 = scpi.send('*WAI; SYST:ERR:ALL?')
    if (DEBUG == True):
        print ("ACLR status: " + ret5)
    aclr_array = scpi.send('FETC:ACLR?').replace(';', '').split(',')
    
    
    if power_supply != 0: 
        #Measure the voltage
        power_supply.write(":MEAS:VOLT? ")
        time.sleep(0.1)
        voltage = float(power_supply.read())
    
        #Measure the current
        power_supply.write(":MEAS:CURR? ")
        time.sleep(0.1)
        current = float(power_supply.read())
    else:
        current = 0
        voltage = 0
   
    #Printing the result of the TXQuality test to the command line
    if (DEBUG == True):
        print ("\nRB Value: \t\t\t\t" + str(rb))
        print ("\nRB Offset: \t\t\t\t" + str(rb_offset))
        print ("\nHex Value: \t\t\t\t" + str(hex))
        print ("\nGain Value: \t\t\t\t" + str(gain))
        print ("\nStatus Code: \t\t\t\t" + str(float(txq_array[0])))
        print ("\nAverage Power (dBm): \t\t\t" + str(float(result_dict['Average Power (dBm)'])))
        print ("Average_IQ_Offset (dB): \t\t" + str(float(txq_array[1])))
        print ("Average_Frequency_Error (Hz): \t\t" + str(float(txq_array[2])))
        print ("Average_Data_EVM (%): \t\t\t" + str(float(txq_array[3])))
        print ("Average_Peak_Data_EVM (%): \t\t" + str(float(txq_array[4])))
        print ("Average_RS_EVM (%): \t\t\t" + str(float(txq_array[5])))
        print ("Average_Peak_RS_EVM (%): \t\t" + str(float(txq_array[6])))
        print ("Average_Amplitude_Imbalance (dB): \t" + str(float(txq_array[7])))
        print ("Average_Phase_Imbalance (deg): \t\t" + str(float(txq_array[8])))
        print ("ACLR E-UTRA Lower (dB): \t" + str(float(aclr_array[2])))
        print ("ACLR E-UTRA Upper (dB): \t" + str(float(aclr_array[3])))
        print ("Voltage (V): \t\t\t\t" + str(voltage))
        print ("Current (A): \t\t\t\t" + str(current))
        
    #Prints the result of the Power calculation to the command line
    if (power_supply != 0):
        print ("Average Power (dBm): \t\t\t" + str(float(result_dict['Average Power (dBm)'])) + '\n\n')
	
	#Storing the results to be written to the .csv file
    #result_dict['nRB Value'] = rb
    #result_dict['Hex Value'] = hex
    result_dict['Crystal'] = crystal
    #result_dict['Gain Value'] = gain
    #result_dict['RB Offset'] = rb_offset
    result_dict['Average IQ Offset (dB)'] = round(float(txq_array[1]),2)
    result_dict['Average Frequency Error (Hz)'] = round(float(txq_array[2]),2)
    result_dict['Average Data EVM (%)'] = round(float(txq_array[3]),2)
    result_dict['Average Peak Data EVM (%)'] = round(float(txq_array[4]),2)
    result_dict['Average RS EVM (%)'] = round(float(txq_array[5]),2)
    result_dict['Average Peak RS EVM (%)'] = round(float(txq_array[6]),2)
    result_dict['Average IQ Imbalance Gain (dB)'] = round(float(txq_array[7]),2)
    result_dict['Average IQ Imbalance Phase (deg)'] = round(float(txq_array[8]),2)
    result_dict['ACLR E-UTRA Lower (dB)'] = round(float(aclr_array[2]),2)
    result_dict['ACLR E-UTRA Upper (dB)'] = round(float(aclr_array[3]),2)
    #result_dict['Voltage (V)'] = float('{0:.2f}'.format(float(voltage)))
    result_dict['Current (A)'] = round(float(current),2)
    #result_dict['Date & Time'] =  datetime.datetime.strftime(
    #datetime.datetime.now(), '%m/%d/%Y  %H:%M:%S')  
    return result_dict
    

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
	
        # setup VSA, this can be done just once per signal type
    # assuming immediate trigger at the moment
    scpi.send('VSA; TRIG:SOUR IMM; SRAT 37.5e6; CAPT:TIME 20ms')	
    
    return scpi



"""
Function sets up the DUT to transmit the signal
"""
def setup_DUT():

    #Establish connection to DUT
    ser = serial.Serial(COM, 115200, timeout = 5)
    
    print ("\n Enable debug messages if firmware requires...\n")
    ser.write ("log 2\n")
    print("DUT response: " + ser.read(BLOCK_READ_SIZE))
    
    print ("\nInitializing DUT...\n")
    ser.write("d 9\n")
    print("DUT response: " + ser.read(BLOCK_READ_SIZE))
    
    print ("Tx...\n")
    ser.write("d 20\n")
    print("DUT response: " + ser.read(BLOCK_READ_SIZE))
	
    #Setting up 2c0 (crystal)
    print ("Setting up 2c0 (crystal)...\n")
    CSW = setup_crystal(ser)

    
    print ("Writing 2c0...\n")
    ser.write("wr 2c0 " + str(CSW) + "28\n")
    if DEBUG == True:
        print("DUT response: " + ser.read(BLOCK_READ_SIZE))
    
	#Set the PA bias to 9c
    #ser.write("rffe_wrreg f 1 9c\n")
    #print("DUT response: " + ser.read(BLOCK_READ_SIZE))
	
    return (ser,CSW)
	
    
    
"""
Helper method to find CSW to write to 2c0
param - 
    ser - The serial socket connection
return - The CSW value to calibrate the crystal
"""
def setup_crystal(ser):
    freq_curr = FREQ_ERROR
    data_curr = EVM_LIMIT
    freq_char = ''
    
    if (DEBUG == True):
        print("Sending PUSCH signal for crystal ...\n")
    ser.write("d 35 " + str(RB) + " 0 " + str(HEX) + "\n")
    print("DUT response: " + ser.read(BLOCK_READ_SIZE))   
    
    ####################################################################
    #Logic to test for the optimal CSW quickly (four - test process)

    print ("Writing 2c0 "+ str(CSW_CENTER) + "28...\n")
    ser.write("wr 2c0 " + str(CSW_CENTER) + "28\n")
    print("DUT response: " + ser.read(BLOCK_READ_SIZE))	 

    #Perform the calculation, look at the center data evm and freq error
    tx_results = measure_tx(CSW_CENTER,0,0,16,0,0)

    #Writing the rest of the non-header data to the file
    with open (CSV,'ab') as result:
        wr = csv.DictWriter(result, fieldnames = fieldnames)
        wr.writerow(tx_results)
        
    freq_curr = tx_results['Average Frequency Error (Hz)']
    data_curr = tx_results['Average Data EVM (%)']
    freq_char = CSW_CENTER
    
    #Check if the center is our value
    if (abs(freq_curr) < FREQ_ACC and data_curr < EVM_LIMIT):
        return freq_char
        
    #Performs another check based off FREQ_DELTA seen in data
    elif (abs(freq_curr) < FREQ_ERROR):
        #Determines index of next char to test the crystal, hopefully our optimal
        #CSW
        freq_offset = int(freq_curr / FREQ_DELTA)
        freq_char = freq_array[int(freq_array.index(CSW_CENTER) + freq_offset)]    

        print ("Writing 2c0 "+ str(freq_char) + "28...\n")
        ser.write("wr 2c0 " + str(freq_char) + "28\n")
        if (DEBUG == True):
            print("DUT response: " + ser.read(BLOCK_READ_SIZE))	 
        
        #Measure and record the new frequency error and data EVM 
        tx_results = measure_tx(freq_char,0,0,16,0,0)
        freq_curr = tx_results['Average Frequency Error (Hz)']
        data_curr = tx_results['Average Data EVM (%)']         
    
            #Writing the rest of the non-header data to the file
        with open (CSV,'ab') as result:
            wr = csv.DictWriter(result, fieldnames = fieldnames)
            wr.writerow(tx_results)
            
        #Performs check in case of one-off frequency
        if (abs(freq_curr) > FREQ_ACC and abs(freq_curr) < FREQ_ACC * 2):
            #Determines index of next char to test the crystal, hopefully our optimal
            #CSW
            freq_offset = 1 if freq_curr > 0 else -1
            freq_char = freq_array[int(freq_array.index(freq_char) - freq_offset)]    

            print ("Writing 2c0 "+ str(freq_char) + "28...\n")
            ser.write("wr 2c0 " + str(freq_char) + "28\n")
            if (DEBUG == True):
                print("DUT response: " + ser.read(BLOCK_READ_SIZE))	 
            
            #Measure and record the new frequency error and data EVM 
            tx_results = measure_tx(freq_char,0,0,16,0,0)
            freq_curr = tx_results['Average Frequency Error (Hz)']
            data_curr = tx_results['Average Data EVM (%)']         
        
                #Writing the rest of the non-header data to the file
            with open (CSV,'ab') as result:
                wr = csv.DictWriter(result, fieldnames = fieldnames)
                wr.writerow(tx_results)    
            
            #Performs check one last one-off check in the opposite direction
            if (abs(freq_curr) > FREQ_ACC):
                #Determines index of next char to test the crystal, hopefully our optimal
                #CSW
                freq_offset = -2 if freq_curr > 0 else 2
                freq_char = freq_array[int(freq_array.index(freq_char) - freq_offset)]    

                print ("Writing 2c0 "+ str(freq_char) + "28...\n")
                ser.write("wr 2c0 " + str(freq_char) + "28\n")
                if (DEBUG == True):
                    print("DUT response: " + ser.read(BLOCK_READ_SIZE))	 
                
                #Measure and record the new frequency error and data EVM 
                tx_results = measure_tx(freq_char,0,0,16,0,0)
                freq_curr = tx_results['Average Frequency Error (Hz)']
                data_curr = tx_results['Average Data EVM (%)']         
            
                    #Writing the rest of the non-header data to the file
                with open (CSV,'ab') as result:
                    wr = csv.DictWriter(result, fieldnames = fieldnames)
                    wr.writerow(tx_results)    
            
    ###########################################################################
    #In case the quick check failed
    if abs(freq_curr) > FREQ_ACC:
        for CSW_XOSC in freq_array:
            if (DEBUG == True):
                print ("Writing 2c0 "+ str(CSW_XOSC) + "28...\n")
            ser.write("wr 2c0 " + str(CSW_XOSC) + "28\n")
            if (DEBUG == True):
                print("DUT response: " + ser.read(BLOCK_READ_SIZE))	
            
            #Perform the calculation, want to look at the data evm and freq error
            print (CSW_XOSC + "\n")
            tx_results = measure_tx(CSW_XOSC,0,0,16,0,0)            
        
            #Writing the rest of the non-header data to the file
            with open (CSV,'ab') as result:
                wr = csv.DictWriter(result, fieldnames = fieldnames)
                wr.writerow(tx_results)
                
            #Compare the recent calculations to what we have currently
            if (abs (tx_results['Average Frequency Error (Hz)']) < abs(freq_curr) and
                abs (tx_results['Average Data EVM (%)']) < data_curr):
                freq_curr = tx_results['Average Frequency Error (Hz)']
                data_curr = tx_results['Average Data EVM (%)']
                freq_char = CSW_XOSC
       
    #In the case where a right frequency setting is found, exits the entire script 
    if (freq_curr == FREQ_ERROR):
        print ("\nNo frequency value found. Now exiting program")
        sys.exit()
        
    print ("\nYour frequency set value is " + str(freq_char) + " with an average frequency error of " + str(freq_curr)\
           + " and an average Data EVM of " + str(data_curr) + "\n")
   
    return freq_char

        
        
def setup_PS():
    #Setting up the Power Supply
    rm = visa.ResourceManager()
    power_supply = rm.open_resource('GPIB0::9::INSTR')
    
    #Setting output 1
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
    
    return power_supply
    
    
    
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
    starttime = time.time()
    #Setting up the power supply
    print ("Turning on the power supply...\n")
    power_supply = setup_PS()
    
    
    #Setting up connection to Litepoint
    #this is a simple conceptual calibration procedure
    scpi = setup_connection()
    
    #User input to get the rb offset
    #gain_rb_offset = input ("Set rb_offset to: ")
    gain_rb_offset = 0
        
    file = open(CSV, 'wb')
    file.write("Date & Time of Test:\t" + datetime.datetime.strftime(datetime.datetime.now(), '%m/%d/%Y  %H:%M:%S') + "\n") 
    file.write ("DUT:\t\t\t\t\t"+ DUT + "\n")
    file.write("SN:\t\t\t\t\t\t" + SN + "\n")
    #file.write ("CSW(2c0):\t\t\t\t" + str(CSW) + "28\n")
    #file.write ("RB:\t\t\t\t\t\t" + str(RB)+ "\n")
    #file.write("Scale:\t\t\t\t\t0x" + str(HEX) + "\n")
    file.write ("RB Offset:\t\t\t\t" + str(gain_rb_offset) + "\n")
    file.write("VSS_2V0_3V3:\t\t\t" + str(VOLT) + "V\n")
    #file.write("\n")
    file.close()
    with open (CSV,'ab') as result:
        wr = csv.DictWriter(result, fieldnames = fieldnames)
        wr.writeheader()
	#Setting up DUT before sending PUSCH signal
    #Makes a call to setup_crystal
    tuple = setup_DUT()
    ser = tuple[0]
    CSW = tuple [1]
    
    
    print ("Time taken is: " + str(time.time() - starttime))
    #Turning on output
    print ("Turning off output...")
    power_supply.write(":OUTPUT:STATE OFF")
    time.sleep(1)
    
    """
    #Optional statements that may be implemented
    mode = '7c'
    print("Setting PA_Mode...\n")
    ser.write("rffe_wrreg f 0 " + mode + "\n")        
    if DEBUG == True:    
        print("DUT response: " + ser.read(BLOCK_READ_SIZE)
    
    bias = '9c'
    print ("Setting PA Bias to " + bias + "...\n")
    ser.write("rffe_wrreg f 1 " + bias + "\n")
    if DEBUG == True:    
        print("DUT response: " + ser.read(BLOCK_READ_SIZE))    
    
    ctrl_18 = PULL_HIGH
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
    """
    
    




"""
    Automatic execution of main method on run of the script
"""
if __name__ == '__main__':
    main()