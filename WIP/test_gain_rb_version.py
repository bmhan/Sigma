# -----------------------------------------------------------------------------
# Name:        test_rb_version
# Purpose:     Get the TXQuality data, sweeping the RB
# Created:     7/13/2017
# Last Updated: 7/14/2017
#
# NOTE: The program uses RF4A as the VSA port and STRM1A as the VSG port.
# test_rb_version configures the Litepoint IQxstream machine to analyze the 782 MHz
# produced by the board, sweeping the rb values. The result of the test is printed
# to terminal, and is stored in two .csv files - test_rb_result.csv and the sorted
# version test_rb_result_ordered.csv.
# The program uses the socket_interface.py to initialize
# a connection to the board and send and receive data from IQxstream. The serial
# library is used to communicate to the board for testing.
# -----------------------------------------------------------------------------
import socket_interface as scpi
import serial
import time
import csv
import os

HOST = '10.10.14.202'
PORT = 24000
VSA_FREQ = 782e6
CABLE_LOSS_DB = 11
INPUT_CSV = 'input_rb_hex.csv'
#VSA_REF_LEVEL = 2
BLOCK_READ_SIZE = 1024
CSV = 'test_rb_result.csv'
ORD_CSV = 'test_rb_result_ordered.csv'
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
def measure_tx(rb, hex, gain): 
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

    # analyze the LTE signal - 1 subframe for example
    result_dict = {}
    scpi.send('LTE; CLE:ALL; CALC:POW 0,2')
    ret2 = scpi.send('*WAI; SYST:ERR:ALL?')
    print ("Average Power Calculation status: " + ret2)
    power_arr = scpi.send('FETC:POW:AVER?').replace(';', '').split(',')
    result_dict['Average Power (dBm)'] = float(power_arr[1]) + CABLE_LOSS_DB  
	
    
    scpi.send('CALC:TXQ 0,1')
    ret3 = scpi.send('*WAI; SYST:ERR:ALL?')
    print ("TXQuality status: " + ret3)
    txq_array = scpi.send('FETC:TXQ:AVER?').replace(';', '').split(',')
    
    
    scpi.send('CALC:SPEC 0,2')
    ret4 = scpi.send('*WAI; SYST:ERR:ALL?')
    time.sleep(0.1)
    """
    print ("ACLR status: " + ret4)
    eutra_lower = scpi.send('FETC:ACLR:LLIMit?').replace(';', '').split(',')
    result_dict['E-UTRA Lower(dB)'] = float (eutra_lower[1])
    eutra_upper = scpi.send('FETC:ACLR:HLIMit?').replace(';', '').split(',')
    result_dict['E-UTRA Upper(dB)'] = float (eutra_upper[1])
    """
	
    #Printing the result of the TXQuality test to the command line
    print ("\nRB Value: \t\t\t" + str(rb))
    print ("\nHex Value: \t\t\t" + str(hex))
    print ("\nGain Value: \t\t\t" + str(gain))
    print ("\nStatus Code: \t\t\t" + str(float(txq_array[0])))
    print ("\nAverage Power: \t" + str(float(result_dict['Average Power (dBm)'])))
    print ("Average_IQ_Offset: \t\t" + str(float(txq_array[1])))
    print ("Average_Frequency_Error: \t" + str(float(txq_array[2])))
    print ("Average_Data_EVM: \t\t" + str(float(txq_array[3])))
    print ("Average_Peak_Data_EVM: \t\t" + str(float(txq_array[4])))
    print ("Average_RS_EVM: \t\t" + str(float(txq_array[5])))
    print ("Average_Peak_RS_EVM: \t\t" + str(float(txq_array[6])))
    print ("Average_Amplitude_Imbalance: \t" + str(float(txq_array[7])))
    print ("Average_Phase_Imbalance: \t" + str(float(txq_array[8])))
    #print ("E-UTRA Lower: \t" + str(float(aclr_array[1])))
    #print ("E-UTRA Upper: \t" + str(float(aclr_array[2])))
    #print ("E-UTRA Lower: \t" + eutra_lower[1])
    #print ("E-UTRA Upper: \t" + eutra_upper[1])
	
    #result_dict['Status_Code'] = txq_array[0]
    result_dict['nRB Value'] = str(rb)
    result_dict['Hex Value'] = str(hex)
    result_dict['Gain Value'] = str(gain)
    result_dict['Average IQ Offset (dB)'] = float(txq_array[1])
    result_dict['Average Frequency Error (Hz)'] = float(txq_array[2])
    result_dict['Average Data EVM (%)'] = float(txq_array[3])
    result_dict['Average Peak Data EVM (%)'] = float(txq_array[4])
    result_dict['Average RS EVM (%)'] = float(txq_array[5])
    result_dict['Average Peak RS EVM (%)'] = float(txq_array[6])
    result_dict['Average IQ Imbalance Gain (dB)'] = float(txq_array[7])
    result_dict['Average IQ Imbalance Phase (deg)'] = float(txq_array[8])

    
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



"""
Function sets up the DUT to transmit the signal
"""
def setup_DUT():

    #Establish connection to DUT
    ser = serial.Serial('COM5', 115200, timeout = 5)

	
	
    print ("\nInitializing DUT...\n")
    ser.write("d 9\n")
    print("DUT response: " + ser.read(BLOCK_READ_SIZE))
	
    print ("Writing 2c0...\n")
    #ser.write("wr 2c0 c28\n")
    #ser.write("wr 2c0 12 8 c\n")
    #ser.write("wr 2c0 12 8 d\n")
    ser.write("wr 2c0 d28\n")
    print("DUT response: " + ser.read(BLOCK_READ_SIZE))
    
	
    print ("Tx...\n")
    ser.write("d 20\n")
    print("DUT response: " + ser.read(BLOCK_READ_SIZE))
	
    print ("Gain and Offset...\n")
    #ser.write("d 27 -31 -36 904 914 0 -6\n")
    ser.write("d 27 -14 11 4 14 0 -7\n")
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

    gain_start = input ("Gain start: ")
    gain_stop = input ("Gain stop: ")
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
			#d 35 12 0 98ff
            ser.write("d 35 " + str(RB) + " 0 " + str(HEX) + "\n")
            print("DUT response: " + ser.read(BLOCK_READ_SIZE))
       
	        #Second loop to sweep through the gain 
			
            for gain in xrange (gain_start, gain_stop + 1):
                ser.write("d 26 " + str(gain) + "\n")
			
			    # this is a simple conceptual calibration procedure
                setup_connection()
	
        
	            #Measure the avg_power and txquality
                tx_results = measure_tx(RB, HEX, gain)
                
        
                #Writes header if there is none
                if not os.path.isfile(CSV):
                   with open (CSV,'ab') as result:
                       wr = csv.DictWriter(result, tx_results.keys())
                       wr.writeheader()
		
                #Writing the rest of the data to the file
                with open (CSV,'ab') as result:
                    wr = csv.DictWriter(result, tx_results.keys())
			
                    wr.writerow(tx_results)
                   
                
				
    #Trying to reorder the file, by setting the columns
    fieldnames = [
    "nRB Value", "Hex Value", "Gain Value", "Average Power (dBm)", "Average IQ Offset (dB)",
    "Average Frequency Error (Hz)","Average Data EVM (%)",
    "Average Peak Data EVM (%)",
    "Average RS EVM (%)","Average Peak RS EVM (%)", "Average IQ Imbalance Gain (dB)",
    "Average IQ Imbalance Phase (deg)", "E-UTRA Lower (dB)", "E-UTRA Upper (dB)"]

    with open(CSV,'rb') as original, open (ORD_CSV, 'ab') as ordered:
        wr = csv.DictWriter(ordered, fieldnames = fieldnames)
        wr.writeheader()
        for row in csv.DictReader(original):
            wr.writerow(row)
	#TODO procedure finished; reset DUT



"""
    Automatic execution of main method on run of the script
"""
if __name__ == '__main__':
    main()