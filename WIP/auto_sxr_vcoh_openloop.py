# =======================================================
# SXR VCOH open loop using RBB ==========================
# =======================================================
import os
import sys
sys.path.insert(0, os.path.abspath('..\\lib')) #adding directory for libraries

import rlib
import dutlib
import modelib
import speclib
import time

board = 57 #str(raw_input("Enter board number: "))

# enter test parameters
part = str(raw_input("Enter rfic chip number: "))
curr_time = time.strftime("%b%d_%H%M", time.localtime())
temperature = str(raw_input("Enter temperature: "))
LDO_offset = str(raw_input("Enter LDO offset percentage (3, 0, -3): "))

# open data file
outfp = open('..\\data\\SXR_VCOH_openloop_'+LDO_offset+'_chip'+part+'_temp'+temperature+'.csv', 'w')
outfp.write('Time,BrdNo,PartNo,Temp,VCOHorL,CSW,CSWhex,RF_Freq(MHz),BB_Freq(MHz),Pout(dBm),VCOFreq(MHz)\n')

temp=float(temperature)
dutlib.set_temperature(temp)
# open communication
rlib.OpenDevice()
dutlib.selectVersion(2.0)
time.sleep(40)
#initialize
dutlib.rficInit()
dutlib.adjust_2p0_LDO_plus3minus3(LDO_offset)
dutlib.enableCGEN()

# setup Rx PLL
modelib.setupRxPath(740, Rx_Path=2, FE_Path="L2", adc_option="y", gindex=0, bw=20)
# dutlib.sxrSetFreq(806,52) VCOL/4
# dutlib.sxrSetFreq(740,52) VCOH/6
dutlib.sxrUnlockPLL()
# dutlib.writeRxBW(100) # open up Rx filters

import SG5182
sg = SG5182.OpenSG()

# using RBB
for CSW in range(0,512,1):
	outfp.write('%s,%s,%s,%s,VCOH,' %(curr_time,board,part,temperature))
	dutlib.sxrWriteCSW(CSW)

	table1 = dutlib.getColumns('..\\tables\\SXRVCO_1p0_VCOH_CSW_vs_LOFreq.csv')
	RF_Freq_MHz = float(table1[CSW+1][2]) - 40.0 # offset from 1.0 measurements
												 # giving RF higher by 5 MHz 	
	if CSW>450:
		RF_Freq_MHz = RF_Freq_MHz - 29-25 # 28
	elif CSW>400:
		RF_Freq_MHz = RF_Freq_MHz - 22-15 #
	elif CSW>350:
		RF_Freq_MHz = RF_Freq_MHz - 17-15 #	15
	elif CSW>300:
		RF_Freq_MHz = RF_Freq_MHz - 15-10 # 15
	elif CSW>250:
		RF_Freq_MHz = RF_Freq_MHz - 10-10 # 9
	elif CSW>200:
		RF_Freq_MHz = RF_Freq_MHz - 10 # 5 is also ok
	elif CSW>100:
		RF_Freq_MHz = RF_Freq_MHz - 10 #
	elif CSW>50:
		RF_Freq_MHz = RF_Freq_MHz - 3 #
		
	SG5182.SetSgOn(sg, RF_Freq_MHz*1e6, -60) # Set Rx RF in
	
	bbfreq,power = speclib.getsxrBBFreq()
	freq = RF_Freq_MHz*1e6 - bbfreq
	print "CSW, RF inp Freq_MHz, BB freq, LO Freq %d,%0.1f,%d,%d\n" %(CSW,RF_Freq_MHz,bbfreq, freq)
	# print bbfreq*1e-6, power, freq*1e-6
	outfp.write('%d,%x,%.1f,%.1f,%.1f,%.2f\n' %(CSW,CSW,RF_Freq_MHz,bbfreq*1e-6,power,freq*1e-6*6))
	# print "VCOL CSW out of 0 to 1023 %d\n" %(CSW)
	
# for CSW in range(10):
	
	# dutlib.sxrWriteCSW(CSW)
	# freq,power = speclib.getsxrVCODIVFreq()
	# count=SA9020.getCountValue(sa)
	# time.sleep(0.5)
	# print "%.2f\t%.2f\n" % (freq*1e-6*6*740.0/52.0, power)
	# outfp.write('%d,%.2f,%.2f\n' %(CSW,count*1e-6*6*740.0/52.0,freq*1e-6*6*740.0/52.0))

# close communication
dutlib.set_temperature(25)
#RESET
rlib.WriteRficRegisterBits(0x2d0,8,8,0)	
rlib.WriteRficRegisterBits(0x2d0,8,8,1)
outfp.close()
rlib.CloseDevice()
sys.exit(0)