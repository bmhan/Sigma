# -------------------------------------------------------------------------------
# Name:        LTE_Waveform_Loading
# Purpose:     Example IQxstream Python Application
#
# Created:     05/15/2017
# Copyright:   (c) Litepoint 2017
# Licence:     All rights reserved
# -------------------------------------------------------------------------------
import socket_interface as scpi

HOST = '192.168.4.51'
PORT = 24000


def play_waveform(rf_port, waveform_file):
    # reset VSG and ROUTe modules
    ret = scpi.send('VSG; MRST; ROUT; MRST; *WAI; SYST:ERR:ALL?')

    # enable port RF1A with VSG
    scpi.send('ROUT; PORT:RES:ADD ' + rf_port + ', VSG')
    scpi.send('VSG; WAVE:LOAD "/USER/' + waveform_file + '"')
    scpi.send('VSG; WAVE:EXEC ON')
    ret = scpi.send('*WAI; SYST:ERR:ALL?')
    print "Status: ", ret


def setup_vsg(frequency, power):
    scpi.send('VSG; FREQ ' + str(frequency))
    scpi.send('POW:LEV ' + str(power))
    ret = scpi.send('*WAI; SYST:ERR:ALL?')
    print "Status: ", ret


def main():
    scpi.init(HOST, PORT)

    play_waveform('RF1A', 'LTE_NS_test_wave.iqvsg')
    setup_vsg(1805e6, -65.0)

if __name__ == '__main__':
    main()