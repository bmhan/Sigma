# -------------------------------------------------------------------------------
# Name:        LTE_Waveform_Loading
# Purpose:     Example IQxstream Python Application
#
# Created:     05/18/2017
# Copyright:   (c) Litepoint 2017
# Licence:     All rights reserved
# -------------------------------------------------------------------------------
import socket_interface as scpi

HOST = '10.10.14.202'
PORT = 24000


def measure_tx(freq, reference_level):
    # setup VSA, this can be done just once per signal type
    scpi.send('VSA; TRIG:SOUR IMM; SRAT 37.5e6; CAPT:TIME 20ms')  # assuming immediate trigger at the moment

    # setup freq and ref. level
    scpi.send('VSA; FREQ ' + str(freq))
    scpi.send('RLEV ' + str(reference_level))
	
    # initiate a capture
    scpi.send('VSA; INIT')
    ret = scpi.send('*WAI; SYST:ERR:ALL?')
    print ("Capture status " + ret)

    # analyze the LTE signal - 1 subframe for example
    result_dict = {}
    scpi.send('LTE; CLE:ALL; CALC:POW 0,1; CALC:TXQ 0,1')
    power_arr = scpi.send('FETC:POW:AVER?').replace(';', '').split(',')
    result_dict['Average_Power'] = power_arr[1]

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


def play_waveform(waveform_file):
    # enable port RF1A with VSG
   
    scpi.send('VSG; WAVE:LOAD "/USER/' + waveform_file + '"')
    scpi.send('VSG; WAVE:EXEC ON')
    ret = scpi.send('*WAI; SYST:ERR:ALL?')
    print ("Status: ", ret)


def setup_vsg(frequency, power):
    scpi.send('VSG; FREQ ' + str(frequency))
    scpi.send('POW:LEV ' + str(power))
    ret = scpi.send('*WAI; SYST:ERR:ALL?')
    print ("Status: ", ret)


def main():
    # this is a simple conceptual calibration procedure
    scpi.init(HOST, PORT)
    scpi.send('VSA; MRST; VSG; MRST; ROUT; MRST; LTE; MRST; CHAN1; CRST; *WAI; SYST:ERR:ALL?')

    vsg_port = 'STRM1A'
    vsa_port = 'RF4A'
	
    # setup RF ports for VSA/VSG
    # Now a two antenna example
	
    scpi.send('ROUT; PORT:RES:ADD ' + vsa_port + ', VSA')
    scpi.send('ROUT; PORT:RES:ADD ' + vsg_port + ', VSG')

    # 1st - measure frequency error
    freq = 1747.5e6

    # TODO: insert DUT control, dut_start_tx(freq, 20.0)
    tx_results = measure_tx(freq, 29)
    freq_err = tx_results['Average_Frequency_Offset']

    # TODO: calculate and correct frequency error
    '''
    # 2nd - sweep power levels
    sweep_power_levels = range(23, -55, -1)
    power_offset = {}

    for power_level in sweep_power_levels:
        # TODO: insert DUT control, dut_start_tx(freq, power_level)
        
        scpi.init(HOST, PORT)
        scpi.send('VSA; MRST; VSG; MRST; ROUT; MRST; LTE; MRST; CHAN1; CRST; *WAI; SYST:ERR:ALL?')

        vsg_port = 'STRM1A'
        vsa_port = 'RF4A'
	
        # setup RF ports for VSA/VSG
        # Now a two antenna example
	
        scpi.send('ROUT; PORT:RES:ADD ' + vsa_port + ', VSA')
        scpi.send('ROUT; PORT:RES:ADD ' + vsg_port + ', VSG')
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

        scpi.init(HOST, PORT)
        scpi.send('VSA; MRST; VSG; MRST; ROUT; MRST; LTE; MRST; CHAN1; CRST; *WAI; SYST:ERR:ALL?')

        vsg_port = 'STRM1A'
        vsa_port = 'RF4A'
	
        # setup RF ports for VSA/VSG
        # Now a two antenna example
	
        scpi.send('ROUT; PORT:RES:ADD ' + vsa_port + ', VSA')
        scpi.send('ROUT; PORT:RES:ADD ' + vsg_port + ', VSG')
	
        tx_results = measure_tx(freq, ref_level)
        power_vs_freq_offset[freq] = power_level - float(tx_results['Average_Power'])
    '''
    # TODO: calculate results from power_vs_freq_offset and store calibration data to the DUT
    # TODO: insert DUT control, dut_stop_tx()

    #lte_calibration_waveform = 'dummy_lte_calibration_waveform.iqvsg'
    lte_calibration_waveform = 'HHtest.iqvsg'
    # TODO: confirm which LTE calibration waveform to use
    
    # 4th - rx calibration over level (or frequency)
    #play_waveform('RF1A', lte_calibration_waveform)
    #play_waveform(lte_calibration_waveform)
    sweep_power_levels = range(-60, -110, -10)
    #freq = 1747.5
    freq = 1747.5e6
    rssi_offset = {}

    for power_level in sweep_power_levels:

        scpi.init(HOST, PORT)
        scpi.send('VSA; MRST; VSG; MRST; ROUT; MRST; LTE; MRST; CHAN1; CRST; *WAI; SYST:ERR:ALL?')

        vsg_port = 'STRM1A'
        vsa_port = 'RF4A'
	
        # setup RF ports for VSA/VSG
        # Now a two antenna example
	
        scpi.send('ROUT; PORT:RES:ADD ' + vsa_port + ', VSA')
        scpi.send('ROUT; PORT:RES:ADD ' + vsg_port + ', VSG')
		
        setup_vsg(freq, power_level)
        # TODO: insert DUT control, dut_start_rx(freq)
        # TODO: fetch DUT RSSI, dut_report_rssi()
        play_waveform(lte_calibration_waveform)       
        rssi = -9.91e37 # rssi = dut_report_rssi()
        rssi_offset[power_level] = power_level - rssi

    # TODO: calculate results from rssi_offset and store calibration to the DUT

    # TODO: reboot the DUT

if __name__ == '__main__':
    main()