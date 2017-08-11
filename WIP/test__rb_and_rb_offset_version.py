# -----------------------------------------------------------------------------
# Name:        test_rb_and_rb_offset_version
# Purpose:     Get the TXQuality data, sweeping the gains for an rb and rb offset
# Created:     7/19/2017
# Last Updated: 7/18/2017
#
# NOTE: The program uses RF4A as the VSA port and STRM1A as the VSG port.
# test_gain_rb_version configures the Litepoint IQxstream machine to analyze the
# 782 MHz produced by the board
#
# The program sweeps the rb values and the gain values at a nRB offset inputed
# by the user
#
# The program begins by prompting the user for a range of gain values to test.
# The result of the test is printed to terminal, and is stored in two .csv files -
# a sorted and unsorted .csv file
# The program uses the socket_interface.py to initialize
# a connection to the board and send and receive data from IQxstream. The serial
# library is used to communicate to the board for testing.
# -----------------------------------------------------------------------------
import socket_interface as scpi
import serial
import datetime
import time
import csv
import os

HOST = '10.10.14.202'
PORT = 24000
VSA_FREQ = 782e6
CABLE_LOSS_DB = 11
INPUT_CSV = 'input_rb_hex.csv'
#VSA_REF_LEVEL = 2
GAIN_START = 4
GAIN_STOP = 70
BLOCK_READ_SIZE = 1024

#Set this value if u want more debug statements
DEBUG = True

#RB_ARRAY = [1,2,3,4,5,6,8,9,10,12,15,16,18,20,24,25,27,30,32,36,40,45,48,
#50,54,60,64,72,75,80,81,90,96,100]
#RB_ARRAY = [1,2,6]


"""
Function returns a dictionary of information on a given signal.
params:
    freq - The frequency of the VSA
    reference_level - The reference level of VSA
return: 
    Dictionary of information 
"""
def measure_tx(rb, hex, gain, rb_offset): 
    if DEBUG == True:
        print ("Performing Single Analysis...\n")

	
	# setup freq and ref. level
    #scpi.send('VSA; FREQ ' + str(freq))
    #scpi.send('RLEV ' + str(reference_level))

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
    #time.sleep(0.1)
    if (DEBUG == True):
        print ("Capture status: " + ret)

    #Calculating and fetching Average Power
	#Note that this result takes into account cable loss
    result_dict = {}
    scpi.send('LTE; CLE:ALL; CALC:POW 0,20')
    #time.sleep(0.1)
    ret2 = scpi.send('*WAI; SYST:ERR:ALL?')
    if (DEBUG == True):
        print ("Average Power Calculation status: " + ret2)
    power_arr = scpi.send('FETC:POW:AVER?').replace(';', '').split(',')
    result_dict['Average Power (dBm)'] = float(power_arr[1]) + CABLE_LOSS_DB  
	
    
	#Calculating and fetching TXQuality
    scpi.send('CALC:TXQ 0,10')
    #time.sleep(0.1)
    ret3 = scpi.send('*WAI; SYST:ERR:ALL?')
    if (DEBUG == True):
        print ("TXQuality status: " + ret3)
    txq_array = scpi.send('FETC:TXQ:AVER?').replace(';', '').split(',')
    
	
    #Calculating Spectrum and fetching E-UTRA Lower and Upper
    scpi.send('CALC:SPEC 0,20')
    ret4 = scpi.send('*WAI; SYST:ERR:ALL?')
    if (DEBUG == True):
        print ("ACLR status: " + ret4)
    #time.sleep(0.1)
    scpi.send('FORM:READ:DATA ASC')
    aclr_array = scpi.send('FETC:ACLR:AVER?').replace(';', '').split(',')
    
   
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
        print ("Average ACLR E-UTRA Lower (dB): \t\t" + str(float(aclr_array[2])))
        print ("Average ACLR E-UTRA Upper (dB): \t\t" + str(float(aclr_array[3])))

	
	#Storing the results to be written to the .csv file
    result_dict['nRB Value'] = str(rb)
    result_dict['Hex Value'] = str(hex)
    result_dict['Gain Value'] = str(gain)
    result_dict['RB Offset'] = str(rb_offset)
    result_dict['Average IQ Offset (dB)'] = float(txq_array[1])
    result_dict['Average Frequency Error (Hz)'] = float(txq_array[2])
    result_dict['Average Data EVM (%)'] = float(txq_array[3])
    result_dict['Average Peak Data EVM (%)'] = float(txq_array[4])
    result_dict['Average RS EVM (%)'] = float(txq_array[5])
    result_dict['Average Peak RS EVM (%)'] = float(txq_array[6])
    result_dict['Average IQ Imbalance Gain (dB)'] = float(txq_array[7])
    result_dict['Average IQ Imbalance Phase (deg)'] = float(txq_array[8])
    result_dict['Average ACLR E-UTRA Lower (dB)'] = float (aclr_array[2])
    result_dict['Average ACLR E-UTRA Upper (dB)'] = float (aclr_array[3])
    result_dict['Date & Time'] =  datetime.datetime.strftime(
    datetime.datetime.now(), '%B %w, %Y  %H:%M:%S')  
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
    ser = serial.Serial('COM8', 115200, timeout = 5)

	
	
    print ("\nInitializing DUT...\n")
    ser.write("d 9\n")
    print("DUT response: " + ser.read(BLOCK_READ_SIZE))
	
    print ("Writing 2c0...\n")
    #ser.write("wr 2c0 c28\n")
    #ser.write("wr 2c0 12 8 c\n")
    #ser.write("wr 2c0 12 8 d\n")
    ser.write("wr 2c0 a28\n")
    print("DUT response: " + ser.read(BLOCK_READ_SIZE))
    
	
    print ("Tx...\n")
    ser.write("d 20\n")
    print("DUT response: " + ser.read(BLOCK_READ_SIZE))
	
    ser.write("rffe_wrreg f 1 9c\n")
    print("DUT response: " + ser.read(BLOCK_READ_SIZE))
	
	
	#TODO: Put back later after finish testing board 53-0012-01
    #print ("Gain and Offset...\n")
    #ser.write("d 27 -31 -36 904 914 0 -6\n")
    #ser.write("d 27 -14 11 4 14 0 -7\n")
    print("DUT response: " + ser.read(BLOCK_READ_SIZE))
	
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
    time.sleep(0.1)
    
    #User input to get the gain range
    gain_start = input ("Gain start: ")
    gain_stop = input ("Gain stop: ")
    gain_rb_offset = input ("rb_offset: ")
    #this is a simple conceptual calibration procedure
    scpi = setup_connection()
    
    #User input to get the gain range
    #gain_start = input ("Gain start: ")
    #gain_stop = input ("Gain stop: ")
    gain_rb_offset = input ("rb_offset: ")

    
	#Setting up DUT before sending PUSCH signal
    ser = setup_DUT()

	
    #Iterates throught the array of RB values, performing
    #and storing the TX Quality calculations
    with open (INPUT_CSV, "rb") as file:
        reader = csv.DictReader(file)
        for row in reader:
	#for rb in RB_ARRAY:   
		
	    #set RB form: d 34 (your num here) 0\n
        #print ("\nSending PUSCH...\n")
        #ser.write("d 34 " + str(rb) + " 0\n")
        #print("DUT response: " + ser.read(BLOCK_READ_SIZE))
		
            RB = row ['rb']
            HEX = row['hex']
            CSV = "output_rb_" + str(RB) + "_rb_offset_" + str(gain_rb_offset) + "_gain_4_70.csv"
            ORD_CSV = "output_rb_" + str(RB) + "_rb_offset_" + str(gain_rb_offset) + "_gain_4_70_ordered.csv"

            #Sending PUSCH signal with inputed RB, gain, scale
			#Form: d 35 12 0 98ff
            print("PUSCH command...\n")
            ser.write("d 35 " + str(RB) + " " + str(gain_rb_offset) + " "+ str(HEX) + "\n")
            print("DUT response: " + ser.read(BLOCK_READ_SIZE))
       
	        #Second loop to sweep through the gain 
            for gain in xrange (GAIN_START, GAIN_STOP + 1):

                if (DEBUG == True):
                    print ("Setting gain...")

                ser.write("d 26 " + str(gain) + "\n")

                if (DEBUG == True):
                    print("DUT response: " + ser.read(BLOCK_READ_SIZE))

                if (DEBUG == True):
                    print ("Writing to 242...")

                ser.write("wr 242 4444\n")

                if (DEBUG == True):
                    print("DUT response: " + ser.read(BLOCK_READ_SIZE))

	
	            #Measure the avg_power and txquality
                tx_results = measure_tx(RB, HEX, gain, gain_rb_offset)
                
                #Stop procedure (uncomment to use!)
                #Close socket connection to enable GUI access
                #Ask for raw_input to temporarily pause execution
                #scpi.close()    
                #raw_input("\n\n\tPress a key to Continue\t\n\n")
		
                #Writes header if there is none
                if not os.path.isfile(CSV):
                   with open (CSV,'ab') as result:
                       wr = csv.DictWriter(result, tx_results.keys())
                       wr.writeheader()
		
                #Writing the rest of the non-header data to the file
                with open (CSV,'ab') as result:
                    wr = csv.DictWriter(result, tx_results.keys())
			
                    wr.writerow(tx_results)
                   
                
				
    #Trying to reorder the file, by setting the columns
    fieldnames = [
    "nRB Value", "RB Offset", "Hex Value", "Gain Value", "Average Power (dBm)",
    "Average IQ Offset (dB)", "Average Frequency Error (Hz)",
    "Average Data EVM (%)", "Average Peak Data EVM (%)",
    "Average RS EVM (%)","Average Peak RS EVM (%)",
    "Average IQ Imbalance Gain (dB)", "Average IQ Imbalance Phase (deg)",
    "Average ACLR E-UTRA Lower (dB)", "Average ACLR E-UTRA Upper (dB)", "Date & Time"]

    with open(CSV,'rb') as original, open (ORD_CSV, 'wb') as ordered:
        wr = csv.DictWriter(ordered, fieldnames = fieldnames)
        wr.writeheader()
        for row in csv.DictReader(original):
            wr.writerow(row)




"""
    Automatic execution of main method on run of the script
"""
if __name__ == '__main__':
    main()