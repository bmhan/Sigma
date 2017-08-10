# -----------------------------------------------------------------------------
# Name:        test_miniUT_v2_shortened
# Purpose:     Get the TXQuality data, sweeping the gains for an rb and rb offset
# Created:     8/9/2017
# Last Updated: 8/9/2017
#
# NOTE: The program uses RF4A as the VSA port and STRM1A as the VSG port.
# test_miniUT_shortened configures the Litepoint IQxstream machine to analyze the
# 782 MHz produced by the board, sweeping the rb values and the gain values. 
# The program begins by calibrating the CSW 
# The program begins by prompting the user for a range of gain values to test.
# The program uses the socket_interface.py to initialize
# a connection to the board and send and receive data from IQxstream. The serial
# library is used to communicate to the board for testing.
# -----------------------------------------------------------------------------
import socket_interface as scpi
import datetime
import time
import csv
import sys
import os
import serial
import visa
import re
import ftd2xx as ft
import json

#Order of the .csv columns
fieldnames = [
"nRB Value", "Scale","Gain Value", "Average Power (dBm)",
"Average IQ Offset (dB)", "Average Frequency Error (Hz)",
"Average Data EVM (%)", "Average Peak Data EVM (%)",
"Average RS EVM (%)","Average Peak RS EVM (%)",
"Average IQ Imbalance Gain (dB)", "Average IQ Imbalance Phase (deg)",
"ACLR E-UTRA Lower (dB)", "ACLR E-UTRA Upper (dB)", "Current (A)"]

SETUP = "miniUT.setup"

#Values intialized from spec file
HOST = ""
SN = ""
CABLE_LOSS_DB = ""


PORT = 24000

#Values initalized at runtime
COM = ""
PS_ADDRESS = ""
MM_ADDRESS = ""




VSA_FREQ = 782e6
VOLT = 2.5
VOLT_PROT = 3.5
CURR_LIMIT = 2
LOW_CURR_LIMIT = 0.3
FREQ_ERROR = 100000
FREQ_DELTA = 2000
FREQ_ACC = 1000
EVM_LIMIT = 6
DUT = "miniUT Rev E8"
CSW = ""
INPUT_CSV = 'input_rb_hex.csv'
GAIN_START = 4
GAIN_STOP = 70
BLOCK_READ_SIZE = 1024
RB = 0
HEX = 0
GAIN_TABLE = [0,1,2,3,4,5,10,20,30,40,50]
#freq_array = ['1f','f','d','c','b','a']
freq_array = ['0','1','2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', '10', '11', '12',
               '13', '14', '15', '16', '17', '18', '19', '1a', '1b', '1c', '1d', '1e', '1f']
CSW_CENTER = '9'
SUCCESS = 0
FAIL = 1

#Variables for the relay (Low Current Mode Test)
ON = True
OFF = False
RELAY_1 = 0x01

#Set this value to True if you want more debug statements
DEBUG = ""

#Set this value to True if you want to do step by step testing
STEP_TEST = ""

#Set this value to True if you want to log the output to console
LOGGING = ""
LOG_FILE = "test_miniUT_shortened.log"

#Set this valeu to True if you want to perform a check against
#desired specifications
SPEC_CHECK = ""

#Error Values
FREQ_ERROR = 100000
CALC_ERROR = -200
CONNECTION_ERROR = 202
PS_ERROR = 4
IMPORT_ERROR = 2
SERIAL_ERROR = 77
SPEC_ERROR = 99
NUM_OF_RETEST = 0
MAX_RETESTS = 5

#Error Messages
ERROR_END = "\n----------------------------------------------------------------\n"
FREQ_ERROR_MESSAGE = "Failed to perform test sweep. No frequency value found. Retry Test."
CALC_ERROR_MESSAGE = "Litepoint Calculations Failed."
CONNECTION_ERROR_MESSAGE = "Failed to establish connection to Litepoint.\nCheck Host Address."
PS_ERROR_MESSAGE = "Failed to establish connection to 66311B Power Supply.\nCheck COM and PS Address"
IMPORT_ERROR_MESSAGE = "Missing Libraries. Check that you have \npySerial, pyVisa and NI-VISA installed"
SERIAL_ERROR_MESSAGE = "Failed connect to COM.\nCheck that your COM # is correct"
SPEC_ERROR_MESSAGE = "Test failed. Results are not within specifications."    
SPEC_SUCCESS = "Test was a success! Results are within specifications."
    
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
def measure_tx(rb, hex, gain, rb_offset,power_supply): 
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
    result_dict['Average Power (dBm)'] = round(round(float(power_arr[1]) + float(CABLE_LOSS_DB),2),2)
	
    
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
        

	
	#Storing the results to be written to the .csv file
    result_dict['nRB Value'] = rb
    result_dict['Scale'] = hex
    result_dict['Gain Value'] = gain
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
    

    global NUM_OF_RETEST
    global MAX_RETESTS
    
    #In the case of calculation failure
    if (power_supply != 0 and (int(power_arr[0]) != 0 or int(txq_array[0]) != 0 or int(aclr_array[0]) != 0)):
        print "Power calculation error code:\t" + power_arr[0]
        print "TXQ calculation error code:\t" + txq_array[0]
        print "SPEC calculation error code:\t" + aclr_array[0]
        
        #Attempt to redo the test up to MAX_RETESTS number of times
        if (NUM_OF_RETEST < MAX_RETESTS):
            scpi.close()
            setup_connection()
            NUM_OF_RETEST += 1
            print "\nRetest number " + str(NUM_OF_RETEST) + "...\n"
            return measure_tx(rb, hex, gain, rb_offset,power_supply)
        return CALC_ERROR
    
    NUM_OF_RETEST = 0        
    return result_dict
    
	


"""
Function plays a .iqvsg file as the VSG
param:
    waveform_file - The nameof the waveform file to play
"""
def play_waveform(waveform_file):
    # enable port RF1A with VSG
    print ("Loading the waveform " + waveform_file + "...\n")
    scpi.send('VSG; WAVE:LOAD "/USER/' + waveform_file + '"')
    scpi.send('VSG; WAVE:EXEC ON')
    ret = scpi.send('*WAI; SYST:ERR:ALL?')
    print ("Status: ", ret)



"""
Function setups the vsg
param:
    frequency - frequency to set the VSG
    power - power to set the VSG
"""
def setup_vsg(frequency, power):
    print ("Setting up the VSG with frequency " + str(frequency) +
    " and power " + str(power) + "...\n")
    scpi.send('VSG; FREQ ' + str(frequency))
    scpi.send('POW:LEV ' + str(power))
    ret = scpi.send('*WAI; SYST:ERR:ALL?')
    print ("Status: ", ret)



"""
Function sets up socket connection to the IQxstream
"""
def setup_connection ():
    is_connected = scpi.init(HOST, PORT)
    
    if (is_connected == CONNECTION_ERROR):
        return CONNECTION_ERROR
        
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
    global COM
    COM = ""
    rm = visa.ResourceManager()
    rm_list = rm.list_resources()
    
    print "Finding COM for the DUT"
    
    #Loop to find the COM for the DUT
    for device in rm_list:
        if 'ASRL' in device or 'COM' in device:
            
            #Extract the COM number from the port
            COM_NUM = re.sub("[^0-9]","",device)
            
            try:
                ser = serial.Serial('COM' + COM_NUM, 115200, timeout = 5)
                ser.write('Message received\n')
                response = ser.read(16)
                print response
                if len(response) > 0:
                    COM = "COM" + str(COM_NUM)
                    print "The DUT is using " + COM
                    ser.close()
                    break
                else:
                    print "COM" + COM_NUM + " is not the one\n" 
                
            except:
               print "COM" + COM_NUM + " is not the one\n" 
            
            ser.close()
               
    time.sleep(0.5)
    
    #Establish connection to DUT
    try:
        print ("COM: " + COM) 
        ser = serial.Serial(COM, 115200, timeout = 5)
    except:
        return (SERIAL_ERROR, SERIAL_ERROR)

    print ("\nEnabling Log Responses from DUT...\n")
    ser.write("log 2\n")
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
    
    #In case of failure
    if (CSW == FREQ_ERROR):
        return (FREQ_ERROR,FREQ_ERROR)
    
    print ("Writing 2c0...\n")
    ser.write("wr 2c0 " + str(CSW) + "28\n")
    if DEBUG == True:
        print("DUT response: " + ser.read(BLOCK_READ_SIZE))    	

    return (ser,CSW)
	

    
"""
    Method that controls the voltage.
    Each parameter is expected to have the value
    PULL_HIGH or PULL_LOW
"""
def setup_PA_VCC(ctrl_16, ctrl_17, ctrl_18):
    print ("Controlling output VCC...\n")
    
    #RFFEM_CTRL_18
    ser.write ("memwrite A401B158 " + ctrl_18 + "\n")
        
    #RFFEM_CTRL_17
    ser.write ("memwrite A401B13C " + ctrl_17 + "\n")
       
    #RFFEM_CTRL_16
    ser.write ("memwrite A401B138 " + ctrl_16 + "\n")


    
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
    ser.write("d 35 " + str(16) + " 0 " + "179C\n")
    if (DEBUG == True):
        print("DUT response: " + ser.read(BLOCK_READ_SIZE))
        
        
    ####################################################################
    #Logic to test for the optimal CSW quickly (four - test process)

    print ("Writing 2c0 "+ str(CSW_CENTER) + "28...\n")
    ser.write("wr 2c0 " + str(CSW_CENTER) + "28\n")
    print("DUT response: " + ser.read(BLOCK_READ_SIZE))	 

    #Perform the calculation, look at the center data evm and freq error
    #tx_results = measure_tx(CSW_CENTER,0,0,16,0,0)
    tx_results = measure_tx(0,0,16,0,0)
    
    #Writing the rest of the non-header data to the file
    #with open (CSV,'ab') as result:
    #    wr = csv.DictWriter(result, fieldnames = fieldnames)
    #    wr.writerow(tx_results)
        
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
        #tx_results = measure_tx(CSW_CENTER,0,0,16,0,0)
        tx_results = measure_tx(0,0,16,0,0)
        freq_curr = tx_results['Average Frequency Error (Hz)']
        data_curr = tx_results['Average Data EVM (%)']         
    
        #Writing the rest of the non-header data to the file
        #with open (CSV,'ab') as result:
        #    wr = csv.DictWriter(result, fieldnames = fieldnames)
        #    wr.writerow(tx_results)
            
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
            #tx_results = measure_tx(CSW_CENTER,0,0,16,0,0)
            tx_results = measure_tx(0,0,16,0,0)
            freq_curr = tx_results['Average Frequency Error (Hz)']
            data_curr = tx_results['Average Data EVM (%)']         
        
            #Writing the rest of the non-header data to the file
            #with open (CSV,'ab') as result:
            #    wr = csv.DictWriter(result, fieldnames = fieldnames)
            #    wr.writerow(tx_results)    
            
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
                #tx_results = measure_tx(CSW_CENTER,0,0,16,0,0)
                tx_results = measure_tx(0,0,16,0,0)
                freq_curr = tx_results['Average Frequency Error (Hz)']
                data_curr = tx_results['Average Data EVM (%)']         
            
                #Writing the rest of the non-header data to the file
                #with open (CSV,'ab') as result:
                #    wr = csv.DictWriter(result, fieldnames = fieldnames)
                #    wr.writerow(tx_results)    
            
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
            print ("Checking crystal value: " + CSW_XOSC + "\n")
            #tx_results = measure_tx(CSW_CENTER,0,0,16,0,0)
            tx_results = measure_tx(0,0,16,0,0)
        
            #Compare the recent calculations to what we have currently
            if (abs (tx_results['Average Frequency Error (Hz)']) < abs(freq_curr) and
                abs (tx_results['Average Data EVM (%)']) < data_curr):
                freq_curr = tx_results['Average Frequency Error (Hz)']
                data_curr = tx_results['Average Data EVM (%)']
                freq_char = CSW_XOSC
       
    #In the case where a right frequency setting is not found, exits the entire script 
    if (freq_curr == FREQ_ERROR):
        print (FREQ_ERROR_MESSAGE)
        print ("Turning off output...")
        power_supply.write("OUTP OFF")
        time.sleep(1)
        print (ERROR_END)
        return FREQ_ERROR
        
    print ("\nYour frequency set value is " + str(freq_char) + " with an average frequency error of " + str(freq_curr)\
           + " and an average Data EVM of " + str(data_curr) + "\n")
   
    return freq_char

        
"""
Method that sets up the power supply, 66311B
"""
def setup_PS():
    global PS_ADDRESS
    PS_ADDRESS = ""    
    rm = visa.ResourceManager()
    rm_list = rm.list_resources()
    
    print ("Establishing connection to power supply...\n")
    
    #Loop to find the power supply 66311B
    for device in rm_list:
        if 'GPIB' in device:
        
            my_instrument = rm.open_resource(device)
            id = my_instrument.query('*IDN?')
        
            if '66311B' in id:
                PS_ADDRESS = device
                print "The 66311B power supply is at address " + PS_ADDRESS + "\n"
            
            my_instrument.control_ren(6)            
            my_instrument.close()


    try:
        power_supply = rm.open_resource(PS_ADDRESS)
    except:
        return PS_ERROR
   
    
    #print ("Setting voltage protection")
    #power_supply.write ("VOLT:PROT " + str(VOLT_PROT) + "\n")
    #time.sleep(0.1)
        
    #Turning off output
    print ("Turning off PS output...\n")
    power_supply.write("OUTP OFF")
    time.sleep(1)
    
    print ("Setting the voltage...\n")
    power_supply.write("VOLT " + str(VOLT) + "\n")
    time.sleep(0.1)
    
    print ("Setting the current to low current...\n")
    power_supply.write("CURR " + str(LOW_CURR_LIMIT) + "\n")
    time.sleep(0.1)
    
    return power_supply
    
    
    
"""
Method that checks if the results are within specifications
"""
def test_spec (CSV):
    toReturn = 0
    with open (SETUP,'rb') as file:
        data = json.load(file)
        specs = data["specs"]
        
    with open (CSV, 'rb') as results:
        for line in results:
            if 'Current' in line:
                break;
        reader = csv.DictReader(results)
        for row in reader:
            if ((float(row ['Average Power (dBm)']) < specs['POWER_LOWER_LIMIT']) or \
             (float(row ['Average Power (dBm)']) > specs['POWER_UPPER_LIMIT'])):
                toReturn = SPEC_ERROR
                print('Average Power (dBm) is ' + str(row ['Average Power (dBm)']))
                print('Expected Average Power (dBm) is between ' + str(specs['POWER_LOWER_LIMIT'])
                + " and " + str(specs['POWER_UPPER_LIMIT']))
                
            if ((float(row ['Average IQ Offset (dB)']) < specs['IQ_OFFSET_LOWER_LIMIT']) or \
             (float(row ['Average IQ Offset (dB)']) > specs['IQ_OFFSET_UPPER_LIMIT'])):
                toReturn = SPEC_ERROR
                print('Average IQ Offset (dB) is ' + str(row ['Average IQ Offset (dB)']))
                print('Expected Average IQ Offset (dB) is between ' + str(specs['IQ_OFFSET_LOWER_LIMIT'])
                + " and " + str(specs['IQ_OFFSET_UPPER_LIMIT']))       
             
            if ((float(row ['Average Frequency Error (Hz)']) < specs['FREQ_ERROR_LOWER_LIMIT']) or \
             (float(row ['Average Frequency Error (Hz)']) > specs['FREQ_ERROR_UPPER_LIMIT'])):
                toReturn = SPEC_ERROR
                print('Average Frequency Error (Hz) is ' + str(row ['Average Frequency Error (Hz)']))
                print('Expected Average Frequency Error (Hz) is between ' + str(specs['FREQ_ERROR_LOWER_LIMIT'])
                + " and " + str(specs['FREQ_ERROR_UPPER_LIMIT']))  

            if ((float(row ['Average Data EVM (%)']) < specs['DATA_EVM_LOWER_LIMIT']) or \
             (float(row ['Average Data EVM (%)']) > specs['DATA_EVM_UPPER_LIMIT'])):
                toReturn = SPEC_ERROR
                print('Average Data EVM (%) is ' + str(row ['Average Data EVM (%)']))
                print('Expected Average Data EVM (%) is between ' + str(specs['DATA_EVM_LOWER_LIMIT'])
                + " and " + str(specs['DATA_EVM_UPPER_LIMIT']))      

            if ((float(row ['Average Peak Data EVM (%)']) < specs['PEAK_DATA_EVM_LOWER_LIMIT']) or \
             (float(row ['Average Peak Data EVM (%)']) > specs['PEAK_DATA_EVM_UPPER_LIMIT'])):
                toReturn = SPEC_ERROR
                print('Average Peak Data EVM (%) is ' + str(row ['Average Peak Data EVM (%)']))
                print('Expected Average Peak Data EVM (%) is between ' + str(specs['PEAK_DATA_EVM_LOWER_LIMIT'])
                + " and " + str(specs['PEAK_DATA_EVM_UPPER_LIMIT']))      

            if ((float(row ['Average RS EVM (%)']) < specs['RS_EVM_LOWER_LIMIT']) or \
             (float(row ['Average RS EVM (%)']) > specs['RS_EVM_UPPER_LIMIT'])):
                toReturn = SPEC_ERROR
                print('Average RS EVM (%) is ' + str(row ['Average RS EVM (%)']))
                print('Expected Average RS EVM (%) is between ' + str(specs['RS_EVM_LOWER_LIMIT'])
                + " and " + str(specs['RS_EVM_UPPER_LIMIT']))

            if ((float(row ['Average IQ Imbalance Gain (dB)']) < specs['IQ_IMBALANCE_GAIN_LOWER_LIMIT']) or \
             (float(row ['Average IQ Imbalance Gain (dB)']) > specs['IQ_IMBALANCE_GAIN_UPPER_LIMIT'])):
                toReturn = SPEC_ERROR
                print('Average IQ Imbalance Gain (dB) is ' + str(row ['Average IQ Imbalance Gain (dB)']))
                print('Expected Average IQ Imbalance Gain (dB) is between ' + str(specs['IQ_IMBALANCE_GAIN_LOWER_LIMIT'])
                + " and " + str(specs['IQ_IMBALANCE_GAIN_UPPER_LIMIT']))     

            if ((float(row ['Average IQ Imbalance Phase (deg)']) < specs['IQ_IMBALANCE_PHASE_LOWER_LIMIT']) or \
             (float(row ['Average IQ Imbalance Phase (deg)']) > specs['IQ_IMBALANCE_PHASE_UPPER_LIMIT'])):
                toReturn = SPEC_ERROR
                print('Average IQ Imbalance Phase (deg) is ' + str(row ['Average IQ Imbalance Phase (deg)']))
                print('Expected Average IQ Imbalance Phase (deg) is between ' + str(specs['IQ_IMBALANCE_PHASE_LOWER_LIMIT'])
                + " and " + str(specs['IQ_IMBALANCE_PHASE_UPPER_LIMIT']))       

            if ((float(row ['ACLR E-UTRA Lower (dB)']) < specs['ACLR_EUTRA_L_LOWER_LIMIT']) or \
             (float(row ['ACLR E-UTRA Lower (dB)']) > specs['ACLR_EUTRA_L_UPPER_LIMIT'])):
                toReturn = SPEC_ERROR
                print('ACLR E-UTRA Lower (dB) is ' + str(row ['ACLR E-UTRA Lower (dB)']))
                print('Expected ACLR E-UTRA Lower (dB) is between ' + str(specs['ACLR_EUTRA_L_LOWER_LIMIT'])
                + " and " + str(specs['ACLR_EUTRA_L_UPPER_LIMIT']))     

            if ((float(row ['ACLR E-UTRA Upper (dB)']) < specs['ACLR_EUTRA_U_LOWER_LIMIT']) or \
             (float(row ['ACLR E-UTRA Upper (dB)']) > specs['ACLR_EUTRA_U_UPPER_LIMIT'])):
                toReturn = SPEC_ERROR
                print('ACLR E-UTRA Upper (dB) is ' + str(row ['ACLR E-UTRA Upper (dB)']))
                print('Expected ACLR E-UTRA Upper (dB) is between ' + str(specs['ACLR_EUTRA_U_LOWER_LIMIT'])
                + " and " + str(specs['ACLR_EUTRA_U_UPPER_LIMIT']))      

            if ((float(row ['Current (A)']) < specs['CURRENT_LOWER_LIMIT']) or \
             (float(row ['Current (A)']) > specs['CURRENT_UPPER_LIMIT'])):
                toReturn = SPEC_ERROR
                print('Current (A) is ' + str(row ['Current (A)']))
                print('Expected Current (A) is between ' + str(specs['CURRENT_LOWER_LIMIT'])
                + " and " + str(specs['CURRENT_UPPER_LIMIT']))   
    return toReturn
   
   

"""
    Method that checks for current leakage
    by using the 8845A multimeter
    We will be initalizing a multimeter and a relay connection
    return - The current draw from the board when it is in
             low power mode
"""
def check_current_leakage(power_supply) :
    #Credit goes to the Amazon guy
    #Function defined here to turn on and off the relay
    
    print "Checking low current mode using FLUKE"
    
    print ("Turning off output...")
    power_supply.write("OUTP OFF")
    
    #Switch the relay first before turning on power and performing measurement
    #Establish connection to the relay
    try:
        my_relay = ft.open(0) # Opens the device, if it's connected
    except:
        print "Couldn't be opened!"
    
    #Enables Bit Bang Mode
    my_relay.setBitMode(0xFF,0x01)
    
    def setRelay (relay,state):
        # Get the current state of the relays
        relayStates = my_relay.getBitMode() 
        if state == ON:
            # Turn on relay(s) (without messing with the others)
            my_relay.write( chr(relayStates | relay) ) 
        # The .write() method requires a CHARACTER, so we
        # type-cast our selected state INT to a chr()
        elif state == OFF:
            # Turn off relay(s) (again without killing the others)
            my_relay.write( chr(relayStates & ~relay) )
    
    #Turn the relay on for the low power mode
    print "\nTurning on the relay..."
    setRelay (RELAY_1, ON)
    time.sleep(1)
    
    #Turning on power supply to perform low power measurement
    print ("Turning on output...")
    power_supply.write("OUTP ON")
    time.sleep(3)
    
 
    power_supply.write(":MEAS:CURR? ")
    time.sleep(0.1)
    low_curr = float(power_supply.read())
    
    print("My current from the power supply is: " + str(low_curr) + "A")
    global MM_ADDRESS
    MM_ADDRESS = ""    
    rm = visa.ResourceManager()
    rm_list = rm.list_resources()
    
    print ("Establishing connection to multimeter...\n")
    
    #Loop to find the multimeter address
    for device in rm_list:
        if 'GPIB' in device:
        
            my_instrument = rm.open_resource(device)
            id = my_instrument.query('*IDN?')
        
            if '8845A' in id:
                MM_ADDRESS = device
                print "The 8845A multimeter is at address " + MM_ADDRESS + "\n"
            
            my_instrument.close()
            
    #Establish connection to the multimeter, Fluke 8845A
    rm = visa.ResourceManager()
    multimeter = rm.open_resource(MM_ADDRESS)

    #Setup and measure the current 
    print "\nSetting range to be 1A..."
    multimeter.write("CURR:RANG 1")
    time.sleep(1)
    multimeter.write("CURR:RANG?")
    time.sleep(1)
    print("Current range is: " + multimeter.read())         
    print ("Measuring current...")
    multimeter.write("MEAS:CURR:DC?")
    time.sleep(1)
    low_curr = float(multimeter.read())
    
    print ("The current drawn from the multimeter is: " + str(low_curr) + "A")
    
    #Turn off power supply 
    print ("Turning off output...")
    power_supply.write("OUTP OFF")
    time.sleep(1)
    
    #Turn the relay off now that test is done
    setRelay (RELAY_1, OFF)
    time.sleep(1)
    
    #Set power supply to normal current
    print ("Setting the current to normal current...\n")
    power_supply.write("CURR " + str(CURR_LIMIT) + "\n")
    time.sleep(0.1)
    
    #Turn on power supply and resume rest of the testing
    print ("Turning on output...")
    power_supply.write("OUTP ON")
    time.sleep(1)
    
    return low_curr

    #print ("Current was too high; current_leakage test could not be done")   
        
        
        
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


    #Load in some variables from setup file; not all of them yet
    global HOST
    global SN
    global CABLE_LOSS_DB
    global DEBUG
    global STEP_TEST
    global LOGGING
    global SPEC_CHECK
    with open (SETUP, 'rb') as file:
        
        data = json.load(file)
        HOST = data["HOST"]
        CABLE_LOSS_DB = data["CABLE_LOSS_DB"]
        SN = data["SN"]
        rb_and_scale = data["rb_and_scale"]

        DEBUG = data["DEBUG"]
        STEP_TEST = data ["STEP_TEST"]
        LOGGING = data["LOGGING"]
        SPEC_CHECK = data["SPEC_CHECK"]
        file.close()
        
    print ("\nRunning miniUT test...\n")
    
    #Enable Logging if set
    if LOGGING == True:
        sys.stdout = Logger()
        
    #Setting file name
    CSV = DUT + "_SN_" + str(SN) + ".csv"    
    
    #Setting up the power supply
    print ("Turning on the power supply...\n")
    power_supply = setup_PS()
    
    
    #Check low current mode using FLUKE
    low_current_mode = check_current_leakage(power_supply)
        
    if power_supply == PS_ERROR:
        print (PS_ERROR_MESSAGE)
        print ("Turning off output...")
        power_supply.write("OUTP OFF")
        time.sleep(1)
        print (ERROR_END)
        return PS_ERROR
        
    
    #Setting up connection to Litepoint
    #this is a simple conceptual calibration procedure
    scpi = setup_connection()
    
    if scpi == CONNECTION_ERROR:
        print (CONNECTION_ERROR_MESSAGE)
        print ("Turning off output...")
        power_supply.write("OUTP OFF")
        time.sleep(1)
        print (ERROR_END)
        return -1
    
    
    #User input to get the rb offset
    #gain_rb_offset = input ("Set rb_offset to: ")
    gain_rb_offset = 0
    
	#Setting up DUT before sending PUSCH signal
    #Makes a call to setup_crystal
    tuple = setup_DUT()
    ser = tuple[0]
    CSW = tuple [1]

    if tuple[0] == SERIAL_ERROR:
        print (SERIAL_ERROR_MESSAGE)
        print ("Turning off output...")
        power_supply.write("OUTP OFF")
        time.sleep(1)
        print (ERROR_END)
        return SERIAL_ERROR    
        
    if tuple[0] == FREQ_ERROR:
        print (FREQ_ERROR_MESSAGE)
        print ("Turning off output...")
        power_supply.write("OUTP OFF")
        time.sleep(1)
        print (ERROR_END)
        return FREQ_ERROR

    #Delete previous .csv file if it exists
    if os.path.isfile(CSV):
        os.remove(CSV)  
        
    #Writes the header of the .csv file    
    file = open(CSV, 'wb')
    file.write("Date & Time of Test:\t" + datetime.datetime.strftime(datetime.datetime.now(), '%m/%d/%Y  %H:%M:%S') + "\n") 
    file.write ("DUT:\t\t\t\t\t"+ DUT + "\n")
    file.write("SN:\t\t\t\t\t\t" + SN + "\n")
    file.write ("CSW(2c0):\t\t\t\t" + str(CSW) + "28\n")
    #file.write ("RB:\t\t\t\t\t\t" + str(RB)+ "\n")
    #file.write("Scale:\t\t\t\t\t0x" + str(HEX) + "\n")
    file.write ("RB Offset:\t\t\t\t" + str(gain_rb_offset) + "\n")
    file.write ("Cable Loss:\t\t\t\t" + str(CABLE_LOSS_DB) + " dB\n")
    file.write("VSS_2V0_3V3:\t\t\t" + str(VOLT) + " V\n")
    file.write("Low Current Mode:\t\t" + str(low_current_mode) + " A\n")
    file.close()
    with open (CSV,'ab') as result:
        wr = csv.DictWriter(result, fieldnames = fieldnames)
        wr.writeheader()  
        result.close()
        
    #Iterates throught the array of RB values, performings
    #and storing the TX Quality calculations
    #with open (INPUT_CSV, "rb") as file:
    #    reader = csv.DictReader(file)
    #    for row in reader:
	#for rb in RB_ARRAY:   
    for pairs in rb_and_scale:	    
        RB = pairs[0]
        HEX = pairs[1]
        
        #Sending PUSCH signal with inputed RB, gain, scale
        #Form: d 35 12 0 98ff
        print("PUSCH command...\n")
        ser.write("d 35 " + str(RB) + " " + str(gain_rb_offset) + " "+ str(HEX) + "\n")
        if DEBUG == True:
            print("DUT response: " + ser.read(BLOCK_READ_SIZE))
        else:
            ser.read()
   
        #Necessary delay for the very first reading
        time.sleep(1)
        
        #Second loop to sweep through the gain 
        #TODO : Switch back to user input with xrange if you want more data points
        #for gain in xrange (GAIN_START, GAIN_STOP + 1):
        for gain in GAIN_TABLE:

            if (DEBUG == True):
                print ("Setting gain...")

            ser.write("d 26 " + str(gain) + "\n")

            
            if (DEBUG == True):
                print("DUT response: " + ser.read(BLOCK_READ_SIZE))
            else:
                ser.read()

            """
            #Adjust fine gain to 4444 - Uncomment to use
            if (DEBUG == True):
                print ("Writing to 242...")

            ser.write("wr 242 4444\n")

            if (DEBUG == True):
                print("DUT response: " + ser.read(BLOCK_READ_SIZE))
            """

            #Measure the avg_power and txquality
            tx_results = measure_tx(RB, HEX, gain, gain_rb_offset, power_supply)
            
            #Exit early in the case of calculation error
            if (tx_results == CALC_ERROR):
                print (CALC_ERROR_MESSAGE)
                print ("Turning off output...")
                power_supply.write("OUTP OFF")
                time.sleep(1)
                print (ERROR_END)
                return CALC_ERROR
            
            #Stop procedure (uncomment to use!)
            #Close socket connection to enable GUI access
            #Ask for raw_input to temporarily pause execution
            if (STEP_TEST == True):
                scpi.close()    
                raw_input("\n\n\tPress a key to Continue\t\n\n")
                scpi = setup_connection()
        
            #Writing the non-header data to the file
            with open (CSV,'ab') as result:
                wr = csv.DictWriter(result, fieldnames = fieldnames)			
                wr.writerow(tx_results)
                        
            ##############################################################
            #Marks end of the rb and gain sweep
            
    #Turn off the output
    power_supply.write("OUTP OFF")
    time.sleep(0.1)

    
    #Does Specification check if enabled
    #Check if the data is in line with the specs
    if SPEC_CHECK == True:
        spec_result = test_spec(CSV)
        if (spec_result == SPEC_ERROR):
            print (SPEC_ERROR_MESSAGE)
            print ("Turning off output...")
            power_supply.write(":OUTPUT:STATE OFF")
            time.sleep(1)
            print (ERROR_END)
            return SPEC_ERROR
        else:
            print (SPEC_SUCCESS)
            print ("Turning off output...")
            power_supply.write(":OUTPUT:STATE OFF")
            time.sleep(1)
    
    return SUCCESS


    
""" 
    Class used to log output to stdout and a logfile
"""
class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
        self.log = open(LOG_FILE, "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)  
  

  
"""
    Automatic execution of main method on run of the script
"""
if __name__ == '__main__':
    main()