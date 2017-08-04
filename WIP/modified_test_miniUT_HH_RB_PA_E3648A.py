# -----------------------------------------------------------------------------
# Name:        test_miniUT_RB_PA_E3648A
# Purpose:     Get the TXQuality data, sweeping the PA mode, PA bias, PA vcc,
#              RB, and the Gain.
# Created:     8/2/2017
# Last Updated: 8/3/2017
#
# CHANGE SN BEFORE EVERY TEST!!!
# This program will sweep 5 values: PA_MODE, PA_BIAS, PA_VCC, RB, GAIN
# NOTE: The program uses RF4A as the VSA port and STRM1A as the VSG port.
# The program configures the Litepoint IQxstream machine to analyze the
# 782 MHz produced by the board, sweeping the rb values and the gain values. 
# The program begins by calibrating the CSW 
# The program begins by prompting the user for a range of gain values to test.
# The result of the test is printed to terminal, and is stored in a .csv file.
# The program uses the socket_interface.py to initialize
# a connection to the board and send and receive data from IQxstream. The serial
# library is used to communicate to the board for testing.
# -----------------------------------------------------------------------------
import socket_interface as scpi
import datetime
import time
import visa
import serial
import csv
import sys
import os
#"PA Mode", "PA Bias", "PA VCC (V)","nRB Value", "Scale","Gain Value",
#Order of the .csv columns
fieldnames = [
"Crystal","Average Power (dBm)",
"Average IQ Offset (dB)", "Average Frequency Error (Hz)",
"Average Data EVM (%)", "Average Peak Data EVM (%)",
"Average RS EVM (%)","Average Peak RS EVM (%)",
"Average IQ Imbalance Gain (dB)", "Average IQ Imbalance Phase (deg)",
"ACLR E-UTRA Lower (dB)", "ACLR E-UTRA Upper (dB)", "Current (A)"]

#Instrument setup
HOST = '10.10.14.202'
PORT = 24000
COM = 'COM8'
PS_ADDRESS = 'GPIB0::9::INSTR'
VOLT = 2.5
CURR_LIMIT = 2
EVM_LIMIT = 6

#TX Calculations
VSA_FREQ = 782e6
CABLE_LOSS_DB = 11


#.csv file setup
CSW = ""
#DUT = "miniUT Rev E8"
#SN = "10"
DUT = "UT PROTO 1"
SN = "119"

#Main Looping Logic Variables (in order of appearance)
#freq_array = ['1f','f','d','c','b','a']
freq_array = ['1f','1e', '1d', '1c', '1b', '1a', '19', '18', '17', '16', '15', '14', '13', '12', '11', '10',
             'f','d','e','c','b','a', '9', '8', '7', '6', '5', '4', '3', '2', '1', '0']
LOW_POWER = '7e'
HIGH_POWER = '7c'
#power_modes = [LOW_POWER, HIGH_POWER]
power_modes = [HIGH_POWER]
power_dict =    {
                '7e': 'low power',
                '7c': 'high power'
                }

                
#bias_array = ['0','10','20','30', '7f', '9c']
bias_array = ['9c']


PULL_HIGH = '6a2'
PULL_LOW = '682'
pull_modes = [PULL_LOW, PULL_HIGH]
vcc_dict =  {
            '682682682': 1,
            '6826826a2': 1.5,
            '6826a2682': 2,
            '6826a26a2': 2.5,
            '6a2682682': 2.5,
            '6a26826a2': 3,
            '6a26a2682': 3.5
}
 

INPUT_CSV = 'input_rb_hex.csv'
RB = 0
HEX = 0

GAIN_START = 0
GAIN_STOP = 70 #TODO CHANGE

GAIN_TABLE = [0,1,2,3,4,5,10,20,30,40,50,60,70]

INPUT_SPEC = 'input_spec.txt'
HAS_HEADER = False
BLOCK_READ_SIZE = 1024


#Set this value to True if you want more debug statements
DEBUG = False

#Set this value to True if you want to do step by step testing
STEP_TEST = False

#Set this value to True if you want to log the output to console
LOGGING = True

LOG_FILE = "test_miniUT_RB_PA_E3648A_log.log"

#Error Values
FREQ_ERROR = 100000
CALC_ERROR = -200
CONNECTION_ERROR = 202
PS_ERROR = 4
IMPORT_ERROR = 2
SERIAL_ERROR = 77
SPEC_ERROR = 99
SUCCESS = 0
FAIL = 1
NUM_OF_RETEST = 0
MAX_RETESTS = 5

#Error Messages
ERROR_END = "\n----------------------------------------------------------------\n"
FREQ_ERROR_MESSAGE = "No frequency value found. Retry Test."
CALC_ERROR_MESSAGE = "Litepoint Calculations Failed."
CONNECTION_ERROR_MESSAGE = "Failed to establish connection to Litepoint.\nCheck Host Address."
PS_ERROR_MESSAGE = "Failed to establish connection to 66311B Power Supply.\nCheck COM and PS Address"
IMPORT_ERROR_MESSAGE = "Missing Libraries. Check that you have \npySerial, pyVisa and NI-VISA installed"
SERIAL_ERROR_MESSAGE = "Could not connect to COM. \nCheck that your COM # is correct"
SPEC_ERROR_MESSAGE = "Results are not within specifications."
    
    
"""
Function returns a dictionary of information on a given signal.
params:
    mode - The PA mode
    bias - The PA bias
    vc - the PA VCC in Volts
    rb - The RB value
    hex - The scale
    gain - The gain
    rb_offset - The start rb offset
    power_supply - The power supply
return: 
    Dictionary of information or CALC_ERROR if the calculations were not mades
"""
def measure_tx(crystal,mode, bias, vcc_value, rb, hex, gain, rb_offset,power_supply): 
    if (power_supply != 0):
        print ("Performing Analysis for PA mode " + power_dict[mode] + 
               ", PA bias " + str(bias) + ", PA VCC " + str(vcc_dict[vcc_value]) +
               ", rb " + str(rb)+ ", scaling " + str(hex) +
               ", gain " + str(gain) + ", rb offset " + str(rb_offset) + "...")


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
    #Incremental delay for relatively long command
    time.sleep(0.01)
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
        time.sleep(0.01)
        voltage = float(power_supply.read())
    
        #Measure the current
        power_supply.write(":MEAS:CURR? ")
        time.sleep(0.01)
        current = float(power_supply.read())
    else:
        current = 0
        voltage = 0
   
    #Printing the result of the TXQuality test to the command line
    if (DEBUG == True):
        #print ("\nPA Mode: \t\t\t\t" + power_dict[mode])
        #print ("\nPA Bias: \t\t\t\t" + str(bias))
        #print ("\nPA VCC: \t\t\t\t" + vcc_dict[vcc_value])
        #print ("\nRB Value: \t\t\t\t" + str(rb))
        #print ("\nRB Offset: \t\t\t\t" + str(rb_offset))
        #print ("\nHex Value: \t\t\t\t" + str(hex))
        #print ("\nGain Value: \t\t\t\t" + str(gain))
        print ("\nCrystal: \t\t\t\t" + str(gain))
        print ("\nStatus Code: \t\t\t\t" + str(float(txq_array[0])))
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
    #result_dict['PA Mode'] = power_dict[mode]
    #result_dict['PA Bias'] = str(bias)
    #result_dict['PA VCC (V)'] = vcc_dict[vcc_value]
    #result_dict['nRB Value'] = rb
    #result_dict['Scale'] = '0x' + str(hex)
    #result_dict['Gain Value'] = gain
    #result_dict['RB Offset'] = rb_offset
    result_dict['Crystal'] = crystal
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
            return measure_tx(mode, bias, vcc_value, rb, hex, gain, rb_offset,power_supply)
        return CALC_ERROR
    
    NUM_OF_RETEST = 0
    return result_dict
    
	


"""
Function plays a .iqvsg file as the VSG
param:
    waveform_file - The name of the waveform file to play
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
return - A passing value or CONNECTION_ERROR if the connection to the 
         Litepoint machine could not be established.
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
    
    return is_connected



"""
Function sets up the DUT to transmit the signal
return - A tuple containing two values:
            1) The serial object
            2) The CSW to optimize the crystal
         or a tuple of FREQ_ERROR or SERIAL_ERROR if
         the crystal could not be optimized or a serial
         connection could not be established respectively
"""
def setup_DUT():

    #Establish connection to DUT
    try:
        ser = serial.Serial(COM, 115200, timeout = 5)
    except:
        return (SERIAL_ERROR, SERIAL_ERROR)

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
    
    
    
	#Deprecated code: done in main loop
    #Set the PA bias to 9c
    #ser.write("rffe_wrreg f 1 9c\n")
    #print("DUT response: " + ser.read(BLOCK_READ_SIZE))
	
	#Deprecated Code: done in main loop
    #TODO: Remove later when testing board 53-0012-01
    #print ("Gain and Offset...\n")
    #ser.write("d 27 -31 -36 904 914 0 -6\n")
    #ser.write("d 27 -14 11 4 14 0 -7\n")
    #print("DUT response: " + ser.read(BLOCK_READ_SIZE))
	
    return (ser,CSW)
	
    
    
"""
    Method that controls the voltage.
    Each parameter is expected to have the value
    PULL_HIGH or PULL_LOW
"""
def setup_PA_VCC(ser, ctrl_18, ctrl_17, ctrl_16):
    print ("Controlling output VCC...\n")
    
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
Helper method to find CSW to write to 2c0
param - 
    ser - The serial socket connection
return - The CSW value to calibrate the crystal or
         FREQ_ERROR if a CSW value could not be found
"""
def setup_crystal(ser, CSV, power_supply):
    freq_curr = FREQ_ERROR
    data_curr = EVM_LIMIT
    freq_char = ''
    
    if (DEBUG == True):
        print("Sending PUSCH signal for crystal ...\n")
    ser.write("d 35 " + str(16) + " 0 " + "179C\n")
    if (DEBUG == True):
        print("DUT response: " + ser.read(BLOCK_READ_SIZE))
    
    for CSW_XOSC in freq_array:
        if (DEBUG == True):
            print ("Writing 2c0 "+ str(CSW_XOSC) + "28...\n")
        ser.write("wr 2c0 " + str(CSW_XOSC) + "28\n")
        if (DEBUG == True):
            print("DUT response: " + ser.read(BLOCK_READ_SIZE))	
        
        #Perform the calculation, want to look at the data evm and freq error
        tx_results = measure_tx(CSW_XOSC, HIGH_POWER,0,'682682682',0,0,0,0,power_supply)
    
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
        print (FREQ_ERROR_MESSAGE)
        print ("Turning off output...")
        power_supply.write(":OUTPUT:STATE OFF")
        time.sleep(1)
        return FREQ_ERROR
        
    print ("\nYour frequency set value is " + str(freq_char) + " with an average frequency error of " + str(freq_curr)\
           + " and an average Data EVM of " + str(data_curr) + "\n")
   
    return freq_char

        
"""
Method that sets up the power supply, 66311B
return - A power_supply object, or PS_ERROR if a connection to the
         power supply could not be established
"""
def setup_PS():
    #Setting up the Power Supply
    rm = visa.ResourceManager()
    try:
        global power_supply
        power_supply = rm.open_resource(PS_ADDRESS)
    except:
        return PS_ERROR
    
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
Method that checks if the results are within specifications
return - 0 if the specs are within range, SPEC_ERROR otherwise
"""
def test_spec (CSV):
    toReturn = 0
    specs = {}
    
    #Initialize specs dictionary
    with open (INPUT_SPEC, 'rb') as file:
        #Ignore header
        file.readline()
        for line in file:
            splitLine = line.split()
            specs[splitLine[0]] = float(splitLine[1])
        
    #Comparing results with spec values
    with open (CSV, 'rb') as results:
        for line in results:
            if 'VSS' in line:
                break
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
Main method performs the following:
	Set up the DUT board to transmit
	Sweeping through the array of RB values
	Set up the Litepoint machine to analyze 782 MHz
	Measure the average power and TX Quality of the transmitted
	signal.
	Returns the information through the terminal and two .csv
	files
return - 0 if the test was successful, error values otherwise that 
         vary depending on what the error was
"""
def main():
    gain_rb_offset = 0
    
    CSV = DUT + "_SN_" + str(SN) + ".csv"

    
    #Setting up the power supply
    print ("Turning on the power supply...\n")
    power_supply = setup_PS()
    
    #Setting up connection to Litepoint
    #this is a simple conceptual calibration procedure
    connection_result = setup_connection() 
    
    #Setting up DUT before sending PUSCH signal
    #Makes a call to setup_crystal
        #Establish connection to DUT
    ser = serial.Serial(COM, 115200, timeout = 5)


    print ("\nInitializing DUT...\n")
    ser.write("d 9\n")
    print("DUT response: " + ser.read(BLOCK_READ_SIZE))
    
    print ("Tx...\n")
    ser.write("d 20\n")
    print("DUT response: " + ser.read(BLOCK_READ_SIZE))

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
        
    #Setting up 2c0 (crystal)
    print ("Setting up 2c0 (crystal)...\n")
    CSW = setup_crystal(ser, CSV, power_supply)
    
    

    """
    print ("\nRunning miniUT test...\n")

    #Enable Logging if set
    if LOGGING == True:
        sys.stdout = Logger()
        
        
    #Setting file name
    CSV = DUT + "_SN_" + str(SN) + ".csv"
    ORD_CSV = DUT + "_SN_" + str(SN) +  "_ordered.csv"
    
    
    #Setting up the power supply
    print ("Turning on the power supply...\n")
    power_supply = setup_PS()
    
    if power_supply == PS_ERROR:
        print (PS_ERROR_MESSAGE)
        print ("Turning off output...")
        power_supply.write(":OUTPUT:STATE OFF")
        time.sleep(1)
        print (ERROR_END)
        return PS_ERROR
        
    #Setting up connection to Litepoint
    #this is a simple conceptual calibration procedure
    connection_result = setup_connection()
    
    if connection_result == CONNECTION_ERROR:
        print (CONNECTION_ERROR_MESSAGE)
        print ("Turning off output...")
        power_supply.write(":OUTPUT:STATE OFF")
        time.sleep(1)
        print (ERROR_END)
        return CONNECTION_ERROR
        
    #Set the gain rb_offset for the PUSCH signal
    gain_rb_offset = 0
    
	#Setting up DUT before sending PUSCH signal
    #Makes a call to setup_crystal
    tuple = setup_DUT()
    ser = tuple[0]
    CSW = tuple [1]
    
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
    file.write("VSS_2V0_3V3:\t\t\t" + str(VOLT) + "V\n")
    #file.write("\n")
    file.close()
    with open (CSV,'ab') as result:
        wr = csv.DictWriter(result, fieldnames = fieldnames)
        wr.writeheader()    
        
    if tuple[0] == SERIAL_ERROR:
        print (SERIAL_ERROR_MESSAGE)
        print ("Turning off output...")
        power_supply.write(":OUTPUT:STATE OFF")
        time.sleep(1)
        print (ERROR_END)
        return SERIAL_ERROR
        
    if tuple[0] == FREQ_ERROR:
        print (FREQ_ERROR_MESSAGE)
        print ("Turning off output...")
        power_supply.write(":OUTPUT:STATE OFF")
        time.sleep(1)
        print (ERROR_END)
        return FREQ_ERROR

  
    #Iterates throught PA_Mode, PA_Bias, PA_VCC, RB, Gain
    #and storing the TX Quality calculations
        
    #PA_MODE Loop (#1)
    for mode in  power_modes:
        print("Setting PA_Mode...\n")
        ser.write("rffe_wrreg f 0 " + mode + "\n")        
        if DEBUG == True:    
            print("DUT response: " + ser.read(BLOCK_READ_SIZE))  
    
    
        #PA_Bias Loop (#2)
        for bias in bias_array:
            print ("Setting PA Bias to " + bias + "...\n")
            ser.write("rffe_wrreg f 1 " + bias + "\n")
            if DEBUG == True:    
                print("DUT response: " + ser.read(BLOCK_READ_SIZE))    

            #PA_VCC Loop (#3)
            for pull_18 in pull_modes:
                for pull_17 in pull_modes:
                    for pull_16 in pull_modes:
                        if (pull_18 == PULL_HIGH and pull_17 == PULL_HIGH and pull_16 == PULL_HIGH):
                            continue
                        print ("Setting the VCC to " + pull_18 + " " + pull_17
                                + " " + pull_16 + ",where 6a2 is high and 682 is low\n...")
                        #setup_PA_VCC(ser,pull_18,pull_17,pull_16)
                        #vcc_value = pull_18 + pull_17 + pull_16
                        setup_PA_VCC(ser,PULL_HIGH,PULL_HIGH,PULL_LOW)
                        vcc_value = PULL_HIGH + PULL_HIGH + PULL_LOW
                        with open (INPUT_CSV, "rb") as file:
                            reader = csv.DictReader(file)
        
                            #RB Loop (#4)
                            for row in reader:
                            #for rb in RB_ARRAY:   
		
                                RB = row ['rb']
                                HEX = row['hex']
            

            
                                #Sending PUSCH signal with inputed RB, gain, scale
                                #Form: d 35 12 0 98ff
                                print("PUSCH command...\n")
                                ser.write("d 35 " + str(RB) + " " + str(gain_rb_offset) + " "+ str(HEX) + "\n")
                                if DEBUG == True:
                                    print("DUT response: " + ser.read(BLOCK_READ_SIZE))
                                else:
                                    ser.read()
            
                                #Command to allow delay
                                ser.write ("rd 2c0\n")
                                if DEBUG == True:
                                    print("DUT response: " + ser.read(BLOCK_READ_SIZE))
                                else:
                                    ser.read()                                   
                                
                                #Delay for the PUSCH command
                                time.sleep(1)
                                
                                #Gain Loop (#5) 
                                #Switch back to user input with xrange if you want more data points
                                #for gain in xrange (GAIN_START, GAIN_STOP + 1):
                                for gain in GAIN_TABLE:

                                    if (DEBUG == True):
                                        print ("Setting gain...")
      
                                    ser.write("d 26 " + str(gain) + "\n")
                
                                    if (DEBUG == True):
                                        print("DUT response: " + ser.read(BLOCK_READ_SIZE))
                                    else:
                                        ser.read()
                                    
   
                                    
                                    #Measure the avg_power and txquality
                                    tx_results = measure_tx(mode, bias, vcc_value, RB, HEX, gain, gain_rb_offset, power_supply)
                
                                    #Exit early in the case of calculation error
                                    if (tx_results == CALC_ERROR):
                                        print (CALC_ERROR_MESSAGE)
                                        print ("Turning off output...")
                                        power_supply.write(":OUTPUT:STATE OFF")
                                        time.sleep(1)
                                        print (ERROR_END)
                                        return CALC_ERROR
                
                                    #Stop procedure
                                    #Close socket connection to enable GUI access
                                    #Ask for raw_input to temporarily pause execution
                                    if (STEP_TEST == True):
                                        scpi.close()    
                                        raw_input("\n\n\tPress a key to Continue\t\n\n")
                                        setup_connection()
		
		
                                    #Writing the rest of the non-header data to the file
                                    with open (CSV,'ab') as result:
                                        wr = csv.DictWriter(result, fieldnames = fieldnames)
                                        wr.writerow(tx_results)
              
    
    #Turn off the output
    power_supply.write(":OUTPUT:STATE OFF")
    time.sleep(0.1)
	
    
    #Check if the data is in line with the specs
    spec_result = test_spec(CSV)
    if (spec_result == SPEC_ERROR):
        print (SPEC_ERROR_MESSAGE)
        print ("Turning off output...")
        power_supply.write(":OUTPUT:STATE OFF")
        time.sleep(1)
        print (ERROR_END)
        return SPEC_ERROR
        
    return SUCCESS
    """

    
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