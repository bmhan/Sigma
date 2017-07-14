# -----------------------------------------------------------------------------
# Name:        test_power
# Purpose:     Get the average power from the board.
# Created:     7/13/2017
# Last Updated: 7/13/2017
#
# test_power configures the Litepoint IQxstream machine to analyze the 782 MHz
# produced by the board. The program uses the socket_interface.py to initialize
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
VSA_REF_LEVEL = 2
BLOCK_READ_SIZE = 1024
INPUT_CSV = 'input_5c4_5bc.csv'
CSV = 'test_5C4_5BC_result.csv'
ORD_CSV = 'test_5C4_5BC_result_ordered.csv'
RB_VAL = 1
 

"""
Function returns a dictionary of information on a given signal.
params:
    freq - The frequency of the VSA
    reference_level - The reference level of VSA
return: 
    Dictionary of information 
"""
#def measure_tx(freq, reference_level):
def measure_tx(rb, val5c4, val5bc): 
    print ("Performing Single Analysis...\n")
    # setup VSA, this can be done just once per signal type
    # assuming immediate trigger at the moment
    scpi.send('VSA; TRIG:SOUR IMM; SRAT 37.5e6; CAPT:TIME 20ms')	
    
	#Settings setup
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
    print ("Capture status: " + ret)

    # analyze the LTE signal - 1 subframe for example
    result_dict = {}
    scpi.send('LTE; CLE:ALL; CALC:POW 0,2')
    ret2 = scpi.send('*WAI; SYST:ERR:ALL?')
    print ("Average Power Calculation status: " + ret2)
    power_arr = scpi.send('FETC:POW:AVER?').replace(';', '').split(',')
    result_dict['Average Power (dBm)'] = float(power_arr[1])  
	
    
    
    scpi.send('CALC:TXQ 0,1')
    ret3 = scpi.send('*WAI; SYST:ERR:ALL?')
    print ("TXQuality status: " + ret3)
    txq_array = scpi.send('FETC:TXQ:AVER?').replace(';', '').split(',')
    
    print ("\n5c4 Value: \t\t\t" + str(val5c4))
    print ("5bc Value: \t\t\t" + str(val5bc) + "\n")
    print ("RB Value: \t\t\t" + str(rb))
    print ("\nStatus Code: \t\t\t" + str(float(txq_array[0])))
    print ("Average_IQ_Offset: \t\t" + str(float(txq_array[1])))
    print ("Average_Frequency_Error: \t" + str(float(txq_array[2])))
    print ("Average_Data_EVM: \t\t" + str(float(txq_array[3])))
    print ("Average_Peak_Data_EVM: \t\t" + str(float(txq_array[4])))
    print ("Average_RS_EVM: \t\t" + str(float(txq_array[5])))
    print ("Average_Peak_RS_EVM: \t\t" + str(float(txq_array[6])))
    print ("Average_Amplitude_Imbalance: \t" + str(float(txq_array[7])))
    print ("Average_Phase_Imbalance: \t" + str(float(txq_array[8])))

	#The dictionary TODO to be put into the .csv file
    #result_dict['Status_Code'] = txq_array[0]
    result_dict['5c4 Value'] = str(val5c4)
    result_dict['5bc Value'] = str(val5bc)
    result_dict['nRB Value'] = str(rb)
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
    ser = serial.Serial('COM4', 115200, timeout = 5)

    print ("\nInitializing DUT...\n")
    ser.write("d 9\n")
    print("DUT response: " + ser.read(BLOCK_READ_SIZE))
	
    print ("Writing 2c0...\n")
    #ser.write("wr 2c0 c28\n")
    ser.write("wr 2c0 12 8 c\n")
    print("DUT response: " + ser.read(BLOCK_READ_SIZE))
    
	
    print ("Writing to 0x800242...\n")
    ser.write ("wr 242 5B5B\n")
    print("DUT response: " + ser.read(BLOCK_READ_SIZE))
	
    print ("Tx...\n")
    ser.write("d 20\n")
    print("DUT response: " + ser.read(BLOCK_READ_SIZE))
	
    print("Enabling PA High Power Mode...")
    ser.write("rffe_wrreg f 0 7c\n")
    print("DUT response: " + ser.read(BLOCK_READ_SIZE))
	
    print("Setting Bias Current to 254...\n")
    ser.write("rffe_wrreg f 1 fe\n")
    print("DUT response: " + ser.read(BLOCK_READ_SIZE))	

    print ("Setting Gain and Offset...\n")
    ser.write("d 27 -31 -36 904 914 0 -6\n")
    print("DUT response: " + ser.read(BLOCK_READ_SIZE))
	
    #set RB form: d 34 (your num here) 0\n
	#TODO may need to move this into the looping body
    print ("\nSending PUSCH...\n")
    ser.write("d 34 " + str(RB_VAL) + " 0\n")
    print("DUT response: " + ser.read(BLOCK_READ_SIZE))
	
    return ser
	
	
	
"""
Main method performs the following:
	Set up the DUT board to transmit
	Set up the Litepoint machine to analyze 782 MHz
	Measure the average power of the transmitted signal
"""
def main():
    #Writing the header of the .csv file
    '''
    with open ('test_rb_result.csv', 'wb') as result:
        wr = csv.DictWriter (result, fieldnames = [
        "nRB", "Average Power", "Average IQ Offset",
        "Average Frequency Error","Average Data EVM","Average Peak Data EVM",
        "Average RS EVM","Average Peak RS EVM", "Average IQ Imbalance Gain",
        "Average IQ Imbalance Phase"])
        wr.writeheader()
    '''
	
	#Setting up DUT before sending PUSCH signal
    ser = setup_DUT()
	
	#TODO possible type mismatch with register values
    with open (INPUT_CSV, "rb") as file:
        reader = csv.DictReader(file)
        for row in reader:
            VAL5C4 = row['5c4']
            VAL5BC = row['5bc']
			 
            #this procedure sets up the DUT to transmit a signal
            #setup_DUT(rb)
    
            print ("Setting up 5c4...\n")
            ser.write("wr 5c4 " + str(VAL5C4) + "\n") 
            print("DUT response: " + ser.read(BLOCK_READ_SIZE))

            print ("Setting up 5bc...\n")
            ser.write ("wr 5bc 2 0 " + str(VAL5BC) + "\n") 		
            print("DUT response: " + ser.read(BLOCK_READ_SIZE))
		
	        # this is a simple conceptual calibration procedure
            setup_connection()
	
	        #Measure the avg_power and txquality
            tx_results = measure_tx(RB_VAL, VAL5C4, VAL5BC)

            #Writes header if there is none
            if not os.path.isfile(CSV):
                with open (CSV,'ab') as result:
                    wr = csv.DictWriter(result, tx_results.keys())
                    wr.writeheader()
		
            #Writing the rest of the data to the file
            with open (CSV,'ab') as result:
                wr = csv.DictWriter(result, tx_results.keys())
			
			    #Write nRB to file
                #file = open (CSV, 'a')
                #file.write(str(rb) + ",")
                #file.close()
			
                #Writes the rest of the information
                wr.writerow(tx_results)
            
    #Trying to reorder the file
    fieldnames = [
    "5c4 Value", "5bc Value","nRB Value", "Average Power (dBm)", "Average IQ Offset (dB)",
    "Average Frequency Error (Hz)","Average Data EVM (%)",
    "Average Peak Data EVM (%)",
    "Average RS EVM (%)","Average Peak RS EVM (%)", "Average IQ Imbalance Gain (dB)",
    "Average IQ Imbalance Phase (deg)"]

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