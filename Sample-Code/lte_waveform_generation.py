# -------------------------------------------------------------------------------
# Name:        LTE Non-Signalling Waveform Generation Example
# Purpose:     Example IQxstream Python Application
#
# Created:     05/15/2017
# Copyright:   (c) Litepoint 2017
# Licence:     All rights reserved
# -------------------------------------------------------------------------------
import socket_interface as scpi

HOST = '192.168.4.51'
PORT = 24000

def main():
    scpi.init(HOST, PORT)
    ret = scpi.send('LTE; MRST; CHAN1; CRST; *WAI; SYST:ERR:ALL?')

    #Example FDD, QPSK, 10MHz, 50RB, 8 frames waveform configuration:
    scpi.send('CONFigure:WAVE:NFRames 8;') # number of frames 8 for Rx
    scpi.send('CONFigure:WAVE:PSYMbols (3);')
    scpi.send('CONFigure:WAVE:PDCCh:DCISetup1:FORMat DCI_0;')
    scpi.send('CONFigure:WAVE:PDCCh:DCISetup2:FORMat DCI_1;')

    # TPC 2 to be ALL_UP
    scpi.send('CONFigure:WAVE:PDCCh:DCISetup1:TPC:ARRay (2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2);')
    scpi.send('CONFigure:WAVE:PDCCh:DCISetup2:TPC:ARRay (2);')

    # QPSK
    scpi.send('CONFigure:WAVE:PDCCh:DCISetup1:MCS:ARRay (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);')
    scpi.send('CONFigure:WAVE:PDCCh:DCISetup2:MCS:ARRay (5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5);')

    # RB offset 0, RB 50 to occupy complete 10MHz channel
    scpi.send('CONFigure:WAVE:PDCCh:DCISetup1:RBOFfset:ARRay (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);')
    scpi.send('CONFigure:WAVE:PDCCh:DCISetup2:RBOFfset:ARRay (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);')
    scpi.send('CONFigure:WAVE:PDCCh:DCISetup1:RBDuration:ARRay (50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50);')
    scpi.send('CONFigure:WAVE:PDCCh:DCISetup2:RBDuration:ARRay (50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50);')
    scpi.send('CONFigure:WAVE:PDCCh:DCISetup1:NDI:ARRay (1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0);')
    scpi.send('CONFigure:WAVE:PDCCh:DCISetup2:NDI:ARRay (1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0);')
    scpi.send('CONFigure:WAVE:PDCCh:DCISetup1:HARQ:ARRay (0,1,2,3,4,5,6,7);')
    scpi.send('CONFigure:WAVE:PDCCh:DCISetup2:HARQ:ARRay (0,1,2,3,4,5,6,7,0,1,2,3,4,5,6,7,0,1,2,3,4,5,6,7,0,1,2,3,4,5,6,7,0,1,2,3,4,5,6,7,0,1,2,3,4,5,6,7,0,1,2,3,4,5,6,7,0,1,2,3,4,5,6,7,0,1,2,3,4,5,6,7,0,1,2,3,4,5,6,7,0,1,2,3,4,5,6,7);')

    # Radio Network Temporary Identifier
    scpi.send('CONFigure:WAVE:RNTI 14;')

    # Cell ID
    scpi.send('CONFigure:WAVE:CID 0;')

    # Downlink Bandwidth
    scpi.send('CONFigure:WAVE:DBW 10000000;')
    scpi.send('CONFigure:WAVE:PGValue VALUE_1_6;')
    scpi.send('CONFigure:WAVE:PDType NORMAL;')

    #  OCNG (OFDMA channel-noise generation) state for LTE wave generation.
    scpi.send('CONFigure:WAVE:OCNG:STATe ON;')

    # FDD Waveform
    scpi.send('CONFigure:WAVE:FTYPe 0;')

    scpi.send('WAVE:GEN:MMEM "/USER/LTE_NS_test_wave.iqvsg";')

    ret = scpi.send('*WAI; SYST:ERR:ALL?')
    print "Status: ", ret

    pass

if __name__ == '__main__':
    main()
