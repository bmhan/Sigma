# ======================================
# 02_27_2017 v1
# Rx Gain Sweep measurements
# L2, RX2, Q2
# Apply RF input to appropriate LNA port
# Observe RBB output at Q2
# Sweep gain, input temp & bw
# ======================================

import os
import sys
# adding directory path for lib
sys.path.insert(0, os.path.abspath('..\lib')) 

import rlib
import speclib
import readlib
import dutlib
import modelib
import time

# BB frequencies for filter sweep in kHz - start, stop, step
# range1 = range(300, 500, 50)
# range2 = range(500, 1000, 100)
# range3 = range(1000, 3000, 200)
# range4 = range(3000, 10000, 500)
# range5 = range(10000, 40000, 1000)
# bb_freq_array = range1+range2+range3+range4+range5
# 300kHz only measurement
bb_freq_array = [300]

# Gain indices: 24, 30, 36 + 42, 45, .., 93, 96
gain_array = range(24, 42, 6) + range(42, 99, 3)

# enter test parameters
board = "57"#str(raw_input("Enter board number: "))
part = str(raw_input("Enter rfic chip number: "))
curr_time = time.strftime("%b%d_%H%M", time.localtime())
LDO_offset = str(raw_input("Enter LDO offset percentage (3, 0, -3): "))
# temperature
#temperature = str(raw_input("Enter temperature: "))
# bandwidth
#bw = float(input("Enter BW in MHz: "))
bw = 20.0 #float(input("Enter BW in MHz: "))

#---------------------------------------------Start temp 85----------------------------------------------------------------
temp = 85
dutlib.set_temperature(temp)
# open data file
temperature=str(temp)
file_name = '..\\data\\RX_HighGainSweep_B4_LDO'+LDO_offset+'_chip'+part+'_temp'+temperature+'_bw'+str(bw)+'.csv'
#file_name = '..\\data\\RX_HighGainSweep_temp'+temperature+'_bw'+str(bw)+'.csv'
outfp = open(file_name, 'w')
outfp.write('Time, BrdNo, PartNo, Temperature, Rx_Path, FE_Path, LO(MHz), BW, Offset from LO (MHz), index, Gain(dB)\n')

# RX parameters from user
LO_Freq_MHz = 2132.5#float(input("Enter LO frequency in MHz: "))
Rx_Path = 2#int(input("Enter 1 for RX1 (Primary), 2 for RX2 (Div) and 3 for both: "))
FE_Path  = "H2"#str(raw_input("Enter front end path - L1 or L2 or H1 or H2: "))
adc_option = "n" #str(raw_input('Enter "y" to enable ADC: '))

# open communication
rlib.OpenDevice()
dutlib.selectVersion(2.0)
time.sleep(40)
#initialize
dutlib.rficInit()
dutlib.adjust_2p0_LDO_plus3minus3(LDO_offset)
dutlib.enableCGEN()

# setup Rx path in max gain
modelib.setupRxPath(LO_Freq_MHz, Rx_Path, FE_Path, adc_option, 0, 10)

# RFIC Parameters
BB_Freq_MHz = 0.25
Pin_dBm = -70

#loss_table_name = "..\\tables\\Calibrations_Daughter_NoTuner.csv"
loss_table_name = "..\\tables\\Calibrations_SingleFreq_NoTuner.csv"
 
read_freq, band_name, band_type, cable_loss, trace_loss, tuner_loss, baseband_loss = readlib.read_loss(LO_Freq_MHz,loss_table_name)


for gain_index in gain_array:

	dutlib.loadRxFiltCompVals(gain_index,bw)
	
	for bb_kHz in bb_freq_array:
		
		BB_Freq_MHz = bb_kHz/1e3
		RF_Freq_MHz = LO_Freq_MHz + BB_Freq_MHz
		
		# Read input power from the gain table
		gain_table_name = "..\\tables\\RxGainTable_HighGain.csv"
		# CSV file data in a 2 x 2 array
		table1 = dutlib.getColumns(gain_table_name)

		Pin_dBm = float(table1[gain_index+1][1])

		if Pin_dBm<-70:
			Pin_dBm = -70

		outfp.write('%s,%s,%s,%s,%d,%s,%.1f,' %(curr_time,board,part,temperature,Rx_Path,FE_Path,LO_Freq_MHz))
		outfp.write('%.1f,%.2f,%d,' %(bw,BB_Freq_MHz,gain_index))

		snr,gain,nf = speclib.getRxSNRGainNF(LO_Freq_MHz, BB_Freq_MHz, Pin_dBm)

		Gain_dB = gain + cable_loss + trace_loss + tuner_loss + baseband_loss
		SSBNF_dB = nf - trace_loss - tuner_loss - cable_loss
		DSBNF_dB = SSBNF_dB - 3

		outfp.write('%.2f\n' %(Gain_dB))
		print "index and Gain are %d,%.2f\n" %(gain_index,Gain_dB)
		# print "Gain is %.2fdB" %(Gain_dB)
		
#close file
outfp.close()
#RESET
rlib.WriteRficRegisterBits(0x2d0,8,8,0)	
rlib.WriteRficRegisterBits(0x2d0,8,8,1)		
#---------------------------------------------End temp 85--------------------------------------------------------------			

#---------------------------------------------Start temp 25----------------------------------------------------------------
temp = 25
dutlib.set_temperature(temp)
# open data file
temperature=str(temp)
file_name = '..\\data\\RX_HighGainSweep_B4_LDO'+LDO_offset+'_chip'+part+'_temp'+temperature+'_bw'+str(bw)+'.csv'
#file_name = '..\\data\\RX_HighGainSweep_temp'+temperature+'_bw'+str(bw)+'.csv'
outfp = open(file_name, 'w')
outfp.write('Time, BrdNo, PartNo, Temperature, Rx_Path, FE_Path, LO(MHz), BW, Offset from LO (MHz), index, Gain(dB)\n')

# RX parameters from user
LO_Freq_MHz = 2132.5#float(input("Enter LO frequency in MHz: "))
Rx_Path = 2#int(input("Enter 1 for RX1 (Primary), 2 for RX2 (Div) and 3 for both: "))
FE_Path  = "H2"#str(raw_input("Enter front end path - L1 or L2 or H1 or H2: "))
adc_option = "n" #str(raw_input('Enter "y" to enable ADC: '))

# open communication
rlib.OpenDevice()
dutlib.selectVersion(2.0)
time.sleep(40)
#initialize
dutlib.rficInit()
dutlib.adjust_2p0_LDO_plus3minus3(LDO_offset)
dutlib.enableCGEN()

# setup Rx path in max gain
modelib.setupRxPath(LO_Freq_MHz, Rx_Path, FE_Path, adc_option, 0, 10)

# RFIC Parameters
BB_Freq_MHz = 0.25
Pin_dBm = -70

#loss_table_name = "..\\tables\\Calibrations_Daughter_NoTuner.csv"
loss_table_name = "..\\tables\\Calibrations_SingleFreq_NoTuner.csv"
 
read_freq, band_name, band_type, cable_loss, trace_loss, tuner_loss, baseband_loss = readlib.read_loss(LO_Freq_MHz,loss_table_name)


for gain_index in gain_array:

	dutlib.loadRxFiltCompVals(gain_index,bw)
	
	for bb_kHz in bb_freq_array:
		
		BB_Freq_MHz = bb_kHz/1e3
		RF_Freq_MHz = LO_Freq_MHz + BB_Freq_MHz
		
		# Read input power from the gain table
		gain_table_name = "..\\tables\\RxGainTable_HighGain.csv"
		# CSV file data in a 2 x 2 array
		table1 = dutlib.getColumns(gain_table_name)

		Pin_dBm = float(table1[gain_index+1][1])

		if Pin_dBm<-70:
			Pin_dBm = -70

		outfp.write('%s,%s,%s,%s,%d,%s,%.1f,' %(curr_time,board,part,temperature,Rx_Path,FE_Path,LO_Freq_MHz))
		outfp.write('%.1f,%.2f,%d,' %(bw,BB_Freq_MHz,gain_index))

		snr,gain,nf = speclib.getRxSNRGainNF(LO_Freq_MHz, BB_Freq_MHz, Pin_dBm)

		Gain_dB = gain + cable_loss + trace_loss + tuner_loss + baseband_loss
		SSBNF_dB = nf - trace_loss - tuner_loss - cable_loss
		DSBNF_dB = SSBNF_dB - 3

		outfp.write('%.2f\n' %(Gain_dB))
		print "index and Gain are %d,%.2f\n" %(gain_index,Gain_dB)
		# print "Gain is %.2fdB" %(Gain_dB)
		
#close file
outfp.close()
#RESET
rlib.WriteRficRegisterBits(0x2d0,8,8,0)	
rlib.WriteRficRegisterBits(0x2d0,8,8,1)		
#---------------------------------------------End temp 25--------------------------------------------------------------	

#---------------------------------------------Start temp -40----------------------------------------------------------------
temp = -40
dutlib.set_temperature(temp)
# open data file
temperature=str(temp)
file_name = '..\\data\\RX_HighGainSweep_B4_LDO'+LDO_offset+'_chip'+part+'_temp'+temperature+'_bw'+str(bw)+'.csv'
#file_name = '..\\data\\RX_HighGainSweep_temp'+temperature+'_bw'+str(bw)+'.csv'
outfp = open(file_name, 'w')
outfp.write('Time, BrdNo, PartNo, Temperature, Rx_Path, FE_Path, LO(MHz), BW, Offset from LO (MHz), index, Gain(dB)\n')

# RX parameters from user
LO_Freq_MHz = 2132.5#float(input("Enter LO frequency in MHz: "))
Rx_Path = 2#int(input("Enter 1 for RX1 (Primary), 2 for RX2 (Div) and 3 for both: "))
FE_Path  = "H2"#str(raw_input("Enter front end path - L1 or L2 or H1 or H2: "))
adc_option = "n" #str(raw_input('Enter "y" to enable ADC: '))

# open communication
rlib.OpenDevice()
dutlib.selectVersion(2.0)
time.sleep(40)
#initialize
dutlib.rficInit()
dutlib.adjust_2p0_LDO_plus3minus3(LDO_offset)
dutlib.enableCGEN()

# setup Rx path in max gain
modelib.setupRxPath(LO_Freq_MHz, Rx_Path, FE_Path, adc_option, 0, 10)

# RFIC Parameters
BB_Freq_MHz = 0.25
Pin_dBm = -70

#loss_table_name = "..\\tables\\Calibrations_Daughter_NoTuner.csv"
loss_table_name = "..\\tables\\Calibrations_SingleFreq_NoTuner.csv"
 
read_freq, band_name, band_type, cable_loss, trace_loss, tuner_loss, baseband_loss = readlib.read_loss(LO_Freq_MHz,loss_table_name)


for gain_index in gain_array:

	dutlib.loadRxFiltCompVals(gain_index,bw)
	
	for bb_kHz in bb_freq_array:
		
		BB_Freq_MHz = bb_kHz/1e3
		RF_Freq_MHz = LO_Freq_MHz + BB_Freq_MHz
		
		# Read input power from the gain table
		gain_table_name = "..\\tables\\RxGainTable_HighGain.csv"
		# CSV file data in a 2 x 2 array
		table1 = dutlib.getColumns(gain_table_name)

		Pin_dBm = float(table1[gain_index+1][1])

		if Pin_dBm<-70:
			Pin_dBm = -70

		outfp.write('%s,%s,%s,%s,%d,%s,%.1f,' %(curr_time,board,part,temperature,Rx_Path,FE_Path,LO_Freq_MHz))
		outfp.write('%.1f,%.2f,%d,' %(bw,BB_Freq_MHz,gain_index))

		snr,gain,nf = speclib.getRxSNRGainNF(LO_Freq_MHz, BB_Freq_MHz, Pin_dBm)

		Gain_dB = gain + cable_loss + trace_loss + tuner_loss + baseband_loss
		SSBNF_dB = nf - trace_loss - tuner_loss - cable_loss
		DSBNF_dB = SSBNF_dB - 3

		outfp.write('%.2f\n' %(Gain_dB))
		print "index and Gain are %d,%.2f\n" %(gain_index,Gain_dB)
		# print "Gain is %.2fdB" %(Gain_dB)
		
#close file
outfp.close()
#RESET
rlib.WriteRficRegisterBits(0x2d0,8,8,0)	
rlib.WriteRficRegisterBits(0x2d0,8,8,1)		
#---------------------------------------------End temp -40------------------------------------------------------------	
# close communication
dutlib.set_temperature(25)
#RESET
rlib.WriteRficRegisterBits(0x2d0,8,8,0)	
rlib.WriteRficRegisterBits(0x2d0,8,8,1)
outfp.close()
rlib.CloseDevice()
sys.exit(0)