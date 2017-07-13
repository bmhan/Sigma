# -----------------------------------------------------------------------------
# Name:        LTE_Waveform_Loading
# Purpose:     Example IQxstream Python Application
#
# Created:     7/11/2017
#
#
# my_calibration.py is based on the sample_tx_rx_calibration.py sample code,
# and uses the socket_interface.py code to perform a series of 4 tests. The 
# program currently uses two RF ports to produce and analyze a signal. The
# "TODO" functionality is for programming for the DUT.
# -----------------------------------------------------------------------------
import socket_interface as scpi


HOST = '10.10.14.202'
PORT = 24000



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
    scpi.send('VSA; TRIG:SOUR IMM; CAPT:TIME 10ms') 
    	
    """
    # setup freq and ref. level
    scpi.send('VSA; FREQ ' + str(freq))
    scpi.send('RLEV ' + str(reference_level))
	"""
    # initiate a capture
    scpi.send('VSA; INIT')
    ret = scpi.send('*WAI; SYST:ERR:ALL?')
    print ("Capture status " + ret)

    # analyze the LTE signal - 1 subframe for example
    result_dict = {}
    scpi.send('LTE; CLE:ALL; CALC:POW 0,2')
    ret2 = scpi.send('*WAI; SYST:ERR:ALL?')
    print ("Capture status again" + ret2)
    power_arr = scpi.send('FETC:POW:AVER?').replace(';', '').split(',')
    result_dict['Average_Power'] = power_arr[1]
    
    scpi.send('CALC:TXQ 0,1')
    ret3 = scpi.send('*WAI; SYST:ERR:ALL?')
    print ("Capture status again" + ret3)
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
	
    # setup RF ports for VSA/VSG
    # Now a two antenna example
	
    scpi.send('ROUT; PORT:RES:ADD ' + vsa_port + ', VSA')
    scpi.send('ROUT; PORT:RES:ADD ' + vsg_port + ', VSG')



"""
Main method performs 4 tests
    1) Measures the frequency error 
    2) Sweep power levels
    3) Sweep power vs. frequency
    4) RX calibration over level (or frequency)
"""
def main():
    # this is a simple conceptual calibration procedure
    setup_connection()
    setup_vsg(2500e6, -10)
    waveform = 'LTE_FDD_UL_10MHZ_50RB_QPSK_LP.iqvsg'
    
	# 1st - measure frequency error
    freq = 1747.5e6
    play_waveform(waveform)
    
	
	# TODO: insert DUT control, dut_start_tx(freq, 20.0)
    tx_results = measure_tx(freq, 29)
    """
	freq_err = tx_results['Average_Frequency_Offset']
	
    # TODO: calculate and correct frequency error
    # 2nd - sweep power levels
    sweep_power_levels = range(23, -55, -1)
    power_offset = {}

    for power_level in sweep_power_levels:
        # TODO: insert DUT control, dut_start_tx(freq, power_level)
        
        setup_connection()

        ref_level = power_level + 9.0 # adding user margin to VSA reference level
        tx_results = measure_tx(freq, ref_level)
        power_offset[power_level] = power_level - float(tx_results['Average_Power'])

    # TODO: calculate results from power_offset and store calibration data to the DUT
    
	
    # 3rd - sweep power vs. frequency
    power_level = 20.0
    frequencies = [1710e6, 1747.5e6, 1785e6]
    ref_level = power_level + 9.0  # adding user margin to VSA reference level
    power_vs_freq_offset = {}
    for freq in frequencies:
        # TODO: insert DUT control, dut_start_tx(freq, power_level)

        setup_connection()

        tx_results = measure_tx(freq, ref_level)
        power_vs_freq_offset[freq] = power_level - float(tx_results['Average_Power'])
    # TODO: calculate results from power_vs_freq_offset and store calibration data to the DUT
    # TODO: insert DUT control, dut_stop_tx()

    #lte_calibration_waveform = 'dummy_lte_calibration_waveform.iqvsg'
    lte_calibration_waveform = 'HHtest.iqvsg'
    # TODO: confirm which LTE calibration waveform to use
    
    # 4th - rx calibration over level (or frequency)
    sweep_power_levels = range(-60, -110, -10)
    #freq = 1747.5
    freq = 1747.5e6
    rssi_offset = {}

    for power_level in sweep_power_levels:

        setup_connection()

        setup_vsg(freq, power_level)
        # TODO: insert DUT control, dut_start_rx(freq)
        # TODO: fetch DUT RSSI, dut_report_rssi()
        play_waveform(lte_calibration_waveform)       
        rssi = -9.91e37 # rssi = dut_report_rssi()
        rssi_offset[power_level] = power_level - rssi

    # TODO: calculate results from rssi_offset and store calibration to the DUT

    # TODO: reboot the DUT
    """


"""
    Automatic execution of main method on run of the script
"""
if __name__ == '__main__':
    main()