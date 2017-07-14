# =======================================================
# RX Band 13 IPN
# 03/09/2017
# =======================================================
import os
import sys
sys.path.insert(0, os.path.abspath('..\\lib')) #adding directory for libraries

import rlib
import dutlib
import modelib
import speclib
import time

board = '57' #str(raw_input("Enter board number: "))

# enter test parameters
part = str(raw_input("Enter rfic chip number: "))
curr_time = time.strftime("%b%d_%H%M", time.localtime())
#temperature = str(raw_input("Enter temperature: "))
LDO_offset = str(raw_input("Enter LDO offset percentage (3, 0, -3): "))



#---------------------------------------------Start temp 85----------------------------------------------------------------
temp = 85
dutlib.set_temperature(temp)
# open data file
temperature=str(temp)
# open data file
outfp = open('..\\data\\SXR_Band4_PN_LDO_'+LDO_offset+'_chip_'+part+'_temp'+temperature+'.csv', 'w')
outfp.write('Time,BrdNo,PartNo,Temp,')

# open communication
rlib.OpenDevice()
dutlib.selectVersion(2.0)
time.sleep(40)

#initialize
dutlib.rficInit()
dutlib.adjust_2p0_LDO_plus3minus3(0)
dutlib.enableCGEN()
# setup Rx PLL
modelib.setupRxPath(2132.5, Rx_Path=2, FE_Path="H1", adc_option="y", gindex=0, bw=20)
dutlib.writeRxBW(100) # open up Rx filters
bw_array = [20, 15, 10, 5, 3]
# spot phase noise offsets
SPN_offsets = [100,1e3,10e3,50e3,100e3, 200e3, 400e3, 860e3, 1e6, 1.6e6, 10e6, 25.5e6, 71e6, 390e6 ]
# band 13
# lo_range = (7460, 7560, 1)
# rx_lo_range = range(7460,7561) # all lte channels
rx_lo_range = [21100, 21325, 21550]
#lo_range = range(7460, 7481)

import SG5182
sg = SG5182.OpenSG()

## write header first row in datalog
outfp.write('PN@100,PN@1K,PN@10K,PN@50K,PN@100k,PN@200k,PN@400k,PN@860k,PN@1M,PN@1.6M,PN@10M,PN@25.5M,PN@71M,PN@390M,LO(MHz),LO(dBm),CSW,SSB IPN(dBc_Hz)\n')

for bw in bw_array:	
	dutlib.writeRxBW(bw) # open up Rx filters

	for lofac in rx_lo_range: 

		outfp.write('%s,%s,%s,%s,' %(curr_time,board,part,temperature))
	
		RF_Freq_MHz = float(lofac)/10.0 + bw # 20MHz BB_Freq
		lo = float(lofac)/10.0
		print lo
		##Set RX LO on DUT
		csw_high,csw_mid,csw_low,CSWreg = dutlib.sxrSetFreq(lo,52)	
	
		SG5182.SetSgOn(sg, RF_Freq_MHz*1e6, -10) # Set Rx RF in at -55dBm
	
		## set instrument for IPN  ============================
		start_hz = 100
		stop_hz = 400*1e6
		ipn_start_hz = 1e3
		ipn_stop_hz = 20e6
		reflvl = 0

		sa = speclib.setupPN(start_hz, stop_hz)    ## set up instrument for start & stop freq

		# sweep spot phase noise
		for offset in SPN_offsets:

			SPN = speclib.getTxSpotPN(sa, offset)			## read spot phase noise from instrument
					 
			outfp.write("%.1f," %  float(SPN))			## log spot phase noise in data file
			# print "%.1e %.1f" % (float(offset), float(SPN))
	
		time.sleep(2)
		sa = speclib.setupPN(ipn_start_hz, ipn_stop_hz)
		LO_freq, LO_pwr, IPN = speclib.getTxIPN(sa, ipn_start_hz, ipn_stop_hz)  ##Read IPN from instrument

		outfp.write ('%.5f,%.2f,%d,%.2f\n' %(LO_freq/1e6,LO_pwr,csw_mid,float(IPN)))
#RESET
rlib.WriteRficRegisterBits(0x2d0,8,8,0)	
rlib.WriteRficRegisterBits(0x2d0,8,8,1)		
#---------------------------------------------End temp 85----------------------------------------------------------------


#---------------------------------------------Start temp 25----------------------------------------------------------------
temp = 25
dutlib.set_temperature(temp)
# open data file
temperature=str(temp)
# open data file
outfp = open('..\\data\\SXR_Band4_PN_LDO_'+LDO_offset+'_chip_'+part+'_temp'+temperature+'.csv', 'w')
outfp.write('Time,BrdNo,PartNo,Temp,')

# open communication
rlib.OpenDevice()
dutlib.selectVersion(2.0)
time.sleep(40)

#initialize
dutlib.rficInit()
dutlib.adjust_2p0_LDO_plus3minus3(0)
dutlib.enableCGEN()
# setup Rx PLL
# setup Rx PLL
modelib.setupRxPath(2132.5, Rx_Path=2, FE_Path="H1", adc_option="y", gindex=0, bw=20)
dutlib.writeRxBW(100) # open up Rx filters
bw_array = [20, 15, 10, 5, 3]
# spot phase noise offsets
SPN_offsets = [100,1e3,10e3,50e3,100e3, 200e3, 400e3, 860e3, 1e6, 1.6e6, 10e6, 25.5e6, 71e6, 390e6 ]
# band 13
# lo_range = (7460, 7560, 1)
# rx_lo_range = range(7460,7561) # all lte channels
rx_lo_range = [21100, 21325, 21550]
#lo_range = range(7460, 7481)

import SG5182
sg = SG5182.OpenSG()

## write header first row in datalog
outfp.write('PN@100,PN@1K,PN@10K,PN@50K,PN@100k,PN@200k,PN@400k,PN@860k,PN@1M,PN@1.6M,PN@10M,PN@25.5M,PN@71M,PN@390M,LO(MHz),LO(dBm),CSW,SSB IPN(dBc_Hz)\n')

for bw in bw_array:	
	dutlib.writeRxBW(bw) # open up Rx filters

	for lofac in rx_lo_range: 

		outfp.write('%s,%s,%s,%s,' %(curr_time,board,part,temperature))
	
		RF_Freq_MHz = float(lofac)/10.0 + bw # 20MHz BB_Freq
		lo = float(lofac)/10.0
		print lo
		##Set RX LO on DUT
		csw_high,csw_mid,csw_low,CSWreg = dutlib.sxrSetFreq(lo,52)	
	
		SG5182.SetSgOn(sg, RF_Freq_MHz*1e6, -10) # Set Rx RF in at -55dBm
	
		## set instrument for IPN  ============================
		start_hz = 100
		stop_hz = 400*1e6
		ipn_start_hz = 1e3
		ipn_stop_hz = 20e6
		reflvl = 0

		sa = speclib.setupPN(start_hz, stop_hz)    ## set up instrument for start & stop freq

		# sweep spot phase noise
		for offset in SPN_offsets:

			SPN = speclib.getTxSpotPN(sa, offset)			## read spot phase noise from instrument
					 
			outfp.write("%.1f," %  float(SPN))			## log spot phase noise in data file
			# print "%.1e %.1f" % (float(offset), float(SPN))
	
		time.sleep(2)
		sa = speclib.setupPN(ipn_start_hz, ipn_stop_hz)
		LO_freq, LO_pwr, IPN = speclib.getTxIPN(sa, ipn_start_hz, ipn_stop_hz)  ##Read IPN from instrument

		outfp.write ('%.5f,%.2f,%d,%.2f\n' %(LO_freq/1e6,LO_pwr,csw_mid,float(IPN)))
		
#RESET
rlib.WriteRficRegisterBits(0x2d0,8,8,0)	
rlib.WriteRficRegisterBits(0x2d0,8,8,1)			
#---------------------------------------------End temp 25----------------------------------------------------------------


#---------------------------------------------Start temp 0----------------------------------------------------------------
temp = 0
dutlib.set_temperature(temp)
# open data file
temperature=str(temp)
# open data file
outfp = open('..\\data\\SXR_Band4_PN_LDO_'+LDO_offset+'_chip_'+part+'_temp'+temperature+'.csv', 'w')
outfp.write('Time,BrdNo,PartNo,Temp,')

# open communication
rlib.OpenDevice()
dutlib.selectVersion(2.0)
time.sleep(40)

#initialize
dutlib.rficInit()
dutlib.adjust_2p0_LDO_plus3minus3(0)
dutlib.enableCGEN()
# setup Rx PLL
modelib.setupRxPath(2132.5, Rx_Path=2, FE_Path="H1", adc_option="y", gindex=0, bw=20)
dutlib.writeRxBW(100) # open up Rx filters
bw_array = [20, 15, 10, 5, 3]
# spot phase noise offsets
SPN_offsets = [100,1e3,10e3,50e3,100e3, 200e3, 400e3, 860e3, 1e6, 1.6e6, 10e6, 25.5e6, 71e6, 390e6 ]
# band 13
# lo_range = (7460, 7560, 1)
# rx_lo_range = range(7460,7561) # all lte channels
rx_lo_range = [21100, 21325, 21550]
#lo_range = range(7460, 7481)

import SG5182
sg = SG5182.OpenSG()

## write header first row in datalog
outfp.write('PN@100,PN@1K,PN@10K,PN@50K,PN@100k,PN@200k,PN@400k,PN@860k,PN@1M,PN@1.6M,PN@10M,PN@25.5M,PN@71M,PN@390M,LO(MHz),LO(dBm),CSW,SSB IPN(dBc_Hz)\n')

for bw in bw_array:	
	dutlib.writeRxBW(bw) # open up Rx filters

	for lofac in rx_lo_range: 

		outfp.write('%s,%s,%s,%s,' %(curr_time,board,part,temperature))
	
		RF_Freq_MHz = float(lofac)/10.0 + bw # 20MHz BB_Freq
		lo = float(lofac)/10.0
		print lo
		##Set RX LO on DUT
		csw_high,csw_mid,csw_low,CSWreg = dutlib.sxrSetFreq(lo,52)	
	
		SG5182.SetSgOn(sg, RF_Freq_MHz*1e6, -10) # Set Rx RF in at -55dBm
	
		## set instrument for IPN  ============================
		start_hz = 100
		stop_hz = 400*1e6
		ipn_start_hz = 1e3
		ipn_stop_hz = 20e6
		reflvl = 0

		sa = speclib.setupPN(start_hz, stop_hz)    ## set up instrument for start & stop freq

		# sweep spot phase noise
		for offset in SPN_offsets:

			SPN = speclib.getTxSpotPN(sa, offset)			## read spot phase noise from instrument
					 
			outfp.write("%.1f," %  float(SPN))			## log spot phase noise in data file
			# print "%.1e %.1f" % (float(offset), float(SPN))
	
		time.sleep(2)
		sa = speclib.setupPN(ipn_start_hz, ipn_stop_hz)
		LO_freq, LO_pwr, IPN = speclib.getTxIPN(sa, ipn_start_hz, ipn_stop_hz)  ##Read IPN from instrument

		outfp.write ('%.5f,%.2f,%d,%.2f\n' %(LO_freq/1e6,LO_pwr,csw_mid,float(IPN)))
		
#RESET
rlib.WriteRficRegisterBits(0x2d0,8,8,0)	
rlib.WriteRficRegisterBits(0x2d0,8,8,1)			
#---------------------------------------------End temp 0----------------------------------------------------------------


#---------------------------------------------Start temp -40----------------------------------------------------------------
temp = -40
dutlib.set_temperature(temp)
# open data file
temperature=str(temp)
# open data file
outfp = open('..\\data\\SXR_Band4_PN_LDO_'+LDO_offset+'_chip_'+part+'_temp'+temperature+'.csv', 'w')
outfp.write('Time,BrdNo,PartNo,Temp,')

# open communication
rlib.OpenDevice()
dutlib.selectVersion(2.0)
time.sleep(40)

#initialize
dutlib.rficInit()
dutlib.adjust_2p0_LDO_plus3minus3(0)
dutlib.enableCGEN()
# setup Rx PLL
modelib.setupRxPath(2132.5, Rx_Path=2, FE_Path="H1", adc_option="y", gindex=0, bw=20)
dutlib.writeRxBW(100) # open up Rx filters
bw_array = [20, 15, 10, 5, 3]
# spot phase noise offsets
SPN_offsets = [100,1e3,10e3,50e3,100e3, 200e3, 400e3, 860e3, 1e6, 1.6e6, 10e6, 25.5e6, 71e6, 390e6 ]
# band 13
# lo_range = (7460, 7560, 1)
# rx_lo_range = range(7460,7561) # all lte channels
rx_lo_range = [21100, 21325, 21550]
#lo_range = range(7460, 7481)

import SG5182
sg = SG5182.OpenSG()

## write header first row in datalog
outfp.write('PN@100,PN@1K,PN@10K,PN@50K,PN@100k,PN@200k,PN@400k,PN@860k,PN@1M,PN@1.6M,PN@10M,PN@25.5M,PN@71M,PN@390M,LO(MHz),LO(dBm),CSW,SSB IPN(dBc_Hz)\n')

for bw in bw_array:	
	dutlib.writeRxBW(bw) # open up Rx filters

	for lofac in rx_lo_range: 

		outfp.write('%s,%s,%s,%s,' %(curr_time,board,part,temperature))
	
		RF_Freq_MHz = float(lofac)/10.0 + bw # 20MHz BB_Freq
		lo = float(lofac)/10.0
		print lo
		##Set RX LO on DUT
		csw_high,csw_mid,csw_low,CSWreg = dutlib.sxrSetFreq(lo,52)	
	
		SG5182.SetSgOn(sg, RF_Freq_MHz*1e6, -10) # Set Rx RF in at -55dBm
	
		## set instrument for IPN  ============================
		start_hz = 100
		stop_hz = 400*1e6
		ipn_start_hz = 1e3
		ipn_stop_hz = 20e6
		reflvl = 0

		sa = speclib.setupPN(start_hz, stop_hz)    ## set up instrument for start & stop freq

		# sweep spot phase noise
		for offset in SPN_offsets:

			SPN = speclib.getTxSpotPN(sa, offset)			## read spot phase noise from instrument
					 
			outfp.write("%.1f," %  float(SPN))			## log spot phase noise in data file
			# print "%.1e %.1f" % (float(offset), float(SPN))
	
		time.sleep(2)
		sa = speclib.setupPN(ipn_start_hz, ipn_stop_hz)
		LO_freq, LO_pwr, IPN = speclib.getTxIPN(sa, ipn_start_hz, ipn_stop_hz)  ##Read IPN from instrument

		outfp.write ('%.5f,%.2f,%d,%.2f\n' %(LO_freq/1e6,LO_pwr,csw_mid,float(IPN)))
		
#RESET
rlib.WriteRficRegisterBits(0x2d0,8,8,0)	
rlib.WriteRficRegisterBits(0x2d0,8,8,1)			
#---------------------------------------------End temp -40----------------------------------------------------------------
		
		# close communication
dutlib.set_temperature(25)
#RESET
rlib.WriteRficRegisterBits(0x2d0,8,8,0)	
rlib.WriteRficRegisterBits(0x2d0,8,8,1)
outfp.close()
rlib.CloseDevice()
sys.exit(0)