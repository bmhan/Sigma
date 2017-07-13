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

HOST = '10.10.14.202'
PORT = 24000
VSA_FREQ = 782e6
VSA_REF_LEVEL = 2
BLOCK_READ_SIZE = 1024


"""
Function returns a dictionary of information on a given signal.
params:
    freq - The frequency of the VSA
    reference_level - The reference level of VSA
return: 
    Dictionary of information 
"""
def measure_tx(freq, reference_level):
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
    result_dict['Average_Power'] = power_arr[1]  
	
    
    
    scpi.send('CALC:TXQ 0,1')
    ret3 = scpi.send('*WAI; SYST:ERR:ALL?')
    print ("TXQuality status: " + ret3)
    txq_array = scpi.send('FETC:TXQ:AVER?').replace(';', '').split(',')
    result_dict['Status_Code'] = txq_array[0]
    result_dict['Average_IQ_Offset'] = txq_array[1]
    result_dict['Average_Frequency_Offset'] = txq_array[2]
    result_dict['Average_Data_EVM'] = txq_array[3]
    result_dict['Average_Peak_Data_EVM'] = txq_array[4]
    result_dict['Average_RS_EVM'] = txq_array[5]
    result_dict['Average_Peak_RS_EVM'] = txq_array[6]
    result_dict['Average_Amplitude_Imbalance'] = txq_array[7]
    result_dict['Average_Phase_Imbalance'] = txq_array[8]
    
	
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

    print ("Initializing DUT...\n")
    ser.write("d 9\n")
    print("DUT response: " + ser.read(BLOCK_READ_SIZE))
	
    print ("Writing 2c0")
    ser.write("wr 2c0 c28\n")
	
    print ("Tx...\n")
    ser.write("d 20\n")
    print("DUT response: " + ser.read(BLOCK_READ_SIZE))
	
    print ("Gain and Offset\n")
    ser.write("d 27 -31 -36 904 914 0 -6\n")
    print("DUT response: " + ser.read(BLOCK_READ_SIZE))
	
    print ("Send PUSCH\n")
    ser.write("d 34 12 0\n")

	
	
"""
Main method performs the following:
	Set up the DUT board to transmit
	Set up the Litepoint machine to analyze 782 MHz
	Measure the average power of the transmitted signal
"""
def main():
    #this procedure sets up the DUT to transmit a signal
    setup_DUT()
    
	# this is a simple conceptual calibration procedure
    setup_connection()
	
	#Measure the avg_power and txquality
    tx_results = measure_tx(VSA_FREQ, VSA_REF_LEVEL)
	
	#TODO procedure finished; reset DUT



"""
    Automatic execution of main method on run of the script
"""
if __name__ == '__main__':
    main()