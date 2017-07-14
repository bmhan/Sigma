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
CSV = 'test_rb_result.csv'
#RB_ARRAY = [1,2,3,4,5,6,8,9,10,12,15,16,18,20,24,25,27,30,32,36,40,45,48,
#50,54,60,64,72,75,80,81,90,96,100]
RB_ARRAY =[1,2,6]


"""
Function returns a dictionary of information on a given signal.
params:
    freq - The frequency of the VSA
    reference_level - The reference level of VSA
return: 
    Dictionary of information 
"""
#def measure_tx(freq, reference_level):
def measure_tx(rb): 
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
    result_dict['Average Power'] = power_arr[1]  
	
    
    
    scpi.send('CALC:TXQ 0,1')
    ret3 = scpi.send('*WAI; SYST:ERR:ALL?')
    print ("TXQuality status: " + ret3)
    txq_array = scpi.send('FETC:TXQ:AVER?').replace(';', '').split(',')
    
    print ("\nRB Value: \t\t\t" + str(rb))
    print ("\nStatus Code: \t\t\t" + str(txq_array[0]))
    print ("Average_IQ_Offset: \t\t" + str(txq_array[1]))
    print ("Average_Frequency_Error: \t" + str(txq_array[2]))
    print ("Average_Data_EVM: \t\t" + str(txq_array[3]))
    print ("Average_Peak_Data_EVM: \t\t" + str(txq_array[4]))
    print ("Average_RS_EVM: \t\t" + str(txq_array[5]))
    print ("Average_Peak_RS_EVM: \t\t" + str(txq_array[6]))
    print ("Average_Amplitude_Imbalance: \t" + str(txq_array[7]))
    print ("Average_Phase_Imbalance: \t" + str(txq_array[8]))

	#The dictionary TODO to be put into the .csv file
    #result_dict['Status_Code'] = txq_array[0]
    result_dict['nRB Value'] = str(rb)
    result_dict['Average IQ Offset'] = txq_array[1]
    result_dict['Average Frequency Error'] = txq_array[2]
    result_dict['Average Data EVM'] = txq_array[3]
    result_dict['Average Peak_Data EVM'] = txq_array[4]
    result_dict['Average RS EVM'] = txq_array[5]
    result_dict['Average Peak RS EVM'] = txq_array[6]
    result_dict['Average IQ Imbalance Gain'] = txq_array[7]
    result_dict['Average IQ Imbalance Phase'] = txq_array[8]
    
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
	
    """
	Old initialization
    print ("Initializing DUT...\n")
    ser.write("d 9\n")
    print("DUT response: " + ser.read(BLOCK_READ_SIZE))
	
    print ("Calibrating DUT...\n")
    ser.write("d 1\n")
    time.sleep(5)
    print("DUT response: " + ser.read(BLOCK_READ_SIZE))
	
    print ("Tx...\n")
    ser.write("d 20\n")
    print("DUT response: " + ser.read(BLOCK_READ_SIZE))
    
    print("Generating Tone...\n")
    ser.write("d 22 2000\n")
    print("DUT response: " + ser.read(BLOCK_READ_SIZE))
    """

    print ("\nInitializing DUT...\n")
    ser.write("d 9\n")
    print("DUT response: " + ser.read(BLOCK_READ_SIZE))
	
    print ("Writing 2c0...\n")
    #ser.write("wr 2c0 c28\n")
    ser.write("wr 2c0 12 8 c\n")
    print("DUT response: " + ser.read(BLOCK_READ_SIZE))
    
    print ("Tx...\n")
    ser.write("d 20\n")
    print("DUT response: " + ser.read(BLOCK_READ_SIZE))
	
    print ("Gain and Offset...\n")
    ser.write("d 27 -31 -36 904 914 0 -6\n")
    print("DUT response: " + ser.read(BLOCK_READ_SIZE))
	
    #set RB form: d 34 (your num here) 0\n
    #print ("Sending PUSCH...\n")
    #ser.write("d 34 " + str(rb_num) + " 0\n")
    #print("DUT response: " + ser.read(BLOCK_READ_SIZE))
	
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
	
    for rb in RB_ARRAY:   
        #this procedure sets up the DUT to transmit a signal
        #setup_DUT(rb)
    
	    #Establish connection to DUT
        #ser = serial.Serial('COM4', 115200, timeout = 5)
		
	    #set RB form: d 34 (your num here) 0\n
        print ("\nSending PUSCH...\n")
        ser.write("d 34 " + str(rb) + " 0\n")
        print("DUT response: " + ser.read(BLOCK_READ_SIZE))
		
	    # this is a simple conceptual calibration procedure
        setup_connection()
	
	    #Measure the avg_power and txquality
        tx_results = measure_tx(rb)

        #Writes header if there is none
        if not os.path.isfile(CSV):
            with open (CSV,'a') as result:
                wr = csv.DictWriter(result, tx_results.keys())
                wr.writeheader()
		
        #Writing the rest of the data to the file
        with open (CSV,'a') as result:
            wr = csv.DictWriter(result, tx_results.keys())
			
			#Write nRB to file
            #file = open (CSV, 'a')
            #file.write(str(rb) + ",")
            #file.close()
			
            #Writes the rest of the information
            wr.writerow(tx_results)

	#TODO procedure finished; reset DUT



"""
    Automatic execution of main method on run of the script
"""
if __name__ == '__main__':
    main()