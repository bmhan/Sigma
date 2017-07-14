# =======================================================
# SXR locked test, RBB I/Q, Band 13
# =======================================================
import os
import sys
sys.path.insert(0, os.path.abspath('..\\lib')) #adding directory for libraries

import rlib
import dutlib
import modelib
import speclib
import time
import SA9020
import csv
import SG5182
board = "E3" #str(raw_input("Enter board number: "))

# enter test parameters
part = str(raw_input("Enter rfic chip number: "))
curr_time = time.strftime("%b%d_%H%M", time.localtime())
#temperature = str(raw_input("Enter temperature: "))
LDO_offset = str(raw_input("Enter LDO offset percentage (3, 0, -3): "))
#n = int(input("Enter number of times: "))

#---------------------------------------------Start temp 85----------------------------------------------------------------
temp = 85
dutlib.set_temperature(temp)

n = 100#int(input("Enter number of times: "))
# open data file
temperature=str(temp)
outfp = open('..\\data\\SXR_Band13_Locking_LDO_'+LDO_offset+'_chip_'+part+'_temp'+temperature+'.csv', 'w')
outfp.write('Time,BrdNo,PartNo,Temp,Iteration,CMPLO,CMPHO,RX Frequency(MHz),PPM,State,Status, Locked CSW \n')


# open communication
rlib.OpenDevice()
dutlib.selectVersion(2.0)
time.sleep(40)

for i in range(1,n+1,1):
	outfp.write('%s,%s,%s,%s,%i,'%(curr_time,board,part,temperature,i))
	
	#initialize
	dutlib.rficInit()
	dutlib.adjust_2p0_LDO_plus3minus3(0)
	#dutlib.enableCGEN()
	## ENABLE RX
	dutlib.enableCGEN()
	dutlib.enableRxCommon()
	dutlib.enableRx2()
	dutlib.enableRBB2Output()
	dutlib.selectBandRFE2("L2")
	# write gain, bw and corresponding compensation values
	dutlib.loadRxFiltCompVals(0,10) # gain_index = 0 (max gain), bw = 10MHz
	# setup SXR
	csw_high,csw_mid,csw_low,CSWreg = dutlib.sxrSetFreq(751,52)
	
	sg = SG5182.OpenSG()
	SG5182.SetSgOn(sg, 753000000, -70)
	
	sa = SA9020.OpenSA()
	SA9020.Reflevel(sa, 0)
	SA9020.SetSpan(sa, 2e6, 1e6, "MAX")
	SA9020.Peaksearch(sa)
	freq,power = SA9020.GetMarkerFreqPower(sa)
	
	# print freq,power
	SA9020.SetSpan(sa, freq, 2e3, "MAX")
	# raw_input("press enter to proceed ")
	SA9020.Peaksearch(sa)
	freq,power = SA9020.GetMarkerFreqPower(sa)
	print "SXT LO frequency: %.6f \n" %(freq*1e-6)
	ppm=(freq-2000000)/(751)
	
	
	
	pd_comp_register = 0x800598
	pd_comp_bit = 8
	
		
	#turn on comparator
	CMPLO, CMPHO = dutlib.getPLLcompVals("SXR")
	comparator_total = CMPLO + CMPHO

	
	if (comparator_total==1):
		outfp.write('%i,%i,' %(CMPLO,CMPHO))
		outfp.write('%.8f,%.3f,' %(freq*1e-6,ppm))
		outfp.write('%s,' %("Locked"))
		if (abs(ppm) < 10): 
			outfp.write('%s,' %("Pass"))
		else:
			outfp.write('%s,' %("Failed"))
	else:
		outfp.write('%i,%i,' %(CMPLO,CMPHO))
		outfp.write('%.8f,%.3f,' %(freq*1e-6,ppm))
		outfp.write('%s,%s,' %("Not locked","Failed"))
	CSW=csw_mid
	outfp.write('%i,' %(CSW))
	print "Locked CSW: %i \n" %(CSW)	
	
	outfp.write('\n')	
	# turn off comparator
	rlib.WriteRficRegisterBits(pd_comp_register,pd_comp_bit,pd_comp_bit,1)
	rlib.WriteRficRegisterBits(0x80059C,15,15,1) #immediate bit for SXR
	#UNLOCK SXR
	rlib.WriteRficRegisterBits(0x59C, 9, 9, 1) #PD charge pump in main register
	rlib.WriteRficRegisterBits(0x2A2, 0, 0, 1) #PD charge pump
#---------------------------------------------Start temp 85----------------------------------------------------------------	
	
	
#---------------------------------------------Start temp 25----------------------------------------------------------------
temp = 25
dutlib.set_temperature(temp)

n = 100#int(input("Enter number of times: "))
# open data file
temperature=str(temp)
outfp = open('..\\data\\SXR_Band13_Locking_LDO_'+LDO_offset+'_chip_'+part+'_temp'+temperature+'.csv', 'w')
outfp.write('Time,BrdNo,PartNo,Temp,Iteration,CMPLO,CMPHO,RX Frequency(MHz),PPM,State,Status, Locked CSW \n')


# open communication
rlib.OpenDevice()
dutlib.selectVersion(2.0)
time.sleep(40)

for i in range(1,n+1,1):
	outfp.write('%s,%s,%s,%s,%i,'%(curr_time,board,part,temperature,i))
	
	#initialize
	dutlib.rficInit()
	dutlib.adjust_2p0_LDO_plus3minus3(0)
	#dutlib.enableCGEN()
	## ENABLE RX
	dutlib.enableCGEN()
	dutlib.enableRxCommon()
	dutlib.enableRx2()
	dutlib.enableRBB2Output()
	dutlib.selectBandRFE2("L2")
	# write gain, bw and corresponding compensation values
	dutlib.loadRxFiltCompVals(0,10) # gain_index = 0 (max gain), bw = 10MHz
	# setup SXR
	csw_high,csw_mid,csw_low,CSWreg = dutlib.sxrSetFreq(751,52)
	
	sg = SG5182.OpenSG()
	SG5182.SetSgOn(sg, 753000000, -70)
	
	sa = SA9020.OpenSA()
	SA9020.Reflevel(sa, 0)
	SA9020.SetSpan(sa, 2e6, 1e6, "MAX")
	SA9020.Peaksearch(sa)
	freq,power = SA9020.GetMarkerFreqPower(sa)
	
	# print freq,power
	SA9020.SetSpan(sa, freq, 2e3, "MAX")
	# raw_input("press enter to proceed ")
	SA9020.Peaksearch(sa)
	freq,power = SA9020.GetMarkerFreqPower(sa)
	print "SXT LO frequency: %.6f \n" %(freq*1e-6)
	ppm=(freq-2000000)/(751)
	
	
	
	pd_comp_register = 0x800598
	pd_comp_bit = 8
	
		
	#turn on comparator
	CMPLO, CMPHO = dutlib.getPLLcompVals("SXR")
	comparator_total = CMPLO + CMPHO

	
	if (comparator_total==1):
		outfp.write('%i,%i,' %(CMPLO,CMPHO))
		outfp.write('%.8f,%.3f,' %(freq*1e-6,ppm))
		outfp.write('%s,' %("Locked"))
		if (abs(ppm) < 10): 
			outfp.write('%s,' %("Pass"))
		else:
			outfp.write('%s,' %("Failed"))
	else:
		outfp.write('%i,%i,' %(CMPLO,CMPHO))
		outfp.write('%.8f,%.3f,' %(freq*1e-6,ppm))
		outfp.write('%s,%s,' %("Not locked","Failed"))
	CSW=csw_mid
	outfp.write('%i,' %(CSW))
	print "Locked CSW: %i \n" %(CSW)	
	
	outfp.write('\n')	
	# turn off comparator
	rlib.WriteRficRegisterBits(pd_comp_register,pd_comp_bit,pd_comp_bit,1)
	rlib.WriteRficRegisterBits(0x80059C,15,15,1) #immediate bit for SXR
	#UNLOCK SXR
	rlib.WriteRficRegisterBits(0x59C, 9, 9, 1) #PD charge pump in main register
	rlib.WriteRficRegisterBits(0x2A2, 0, 0, 1) #PD charge pump
#---------------------------------------------Start temp 25----------------------------------------------------------------		

#---------------------------------------------Start temp 0----------------------------------------------------------------
temp = 0
dutlib.set_temperature(temp)

n = 100#int(input("Enter number of times: "))
# open data file
temperature=str(temp)
outfp = open('..\\data\\SXR_Band13_Locking_LDO_'+LDO_offset+'_chip_'+part+'_temp'+temperature+'.csv', 'w')
outfp.write('Time,BrdNo,PartNo,Temp,Iteration,CMPLO,CMPHO,RX Frequency(MHz),PPM,State,Status, Locked CSW \n')


# open communication
rlib.OpenDevice()
dutlib.selectVersion(2.0)
time.sleep(40)

for i in range(1,n+1,1):
	outfp.write('%s,%s,%s,%s,%i,'%(curr_time,board,part,temperature,i))
	
	#initialize
	dutlib.rficInit()
	dutlib.adjust_2p0_LDO_plus3minus3(0)
	#dutlib.enableCGEN()
	## ENABLE RX
	dutlib.enableCGEN()
	dutlib.enableRxCommon()
	dutlib.enableRx2()
	dutlib.enableRBB2Output()
	dutlib.selectBandRFE2("L2")
	# write gain, bw and corresponding compensation values
	dutlib.loadRxFiltCompVals(0,10) # gain_index = 0 (max gain), bw = 10MHz
	# setup SXR
	csw_high,csw_mid,csw_low,CSWreg = dutlib.sxrSetFreq(751,52)
	
	sg = SG5182.OpenSG()
	SG5182.SetSgOn(sg, 753000000, -70)
	
	sa = SA9020.OpenSA()
	SA9020.Reflevel(sa, 0)
	SA9020.SetSpan(sa, 2e6, 1e6, "MAX")
	SA9020.Peaksearch(sa)
	freq,power = SA9020.GetMarkerFreqPower(sa)
	
	# print freq,power
	SA9020.SetSpan(sa, freq, 2e3, "MAX")
	# raw_input("press enter to proceed ")
	SA9020.Peaksearch(sa)
	freq,power = SA9020.GetMarkerFreqPower(sa)
	print "SXT LO frequency: %.6f \n" %(freq*1e-6)
	ppm=(freq-2000000)/(751)
	
	
	
	pd_comp_register = 0x800598
	pd_comp_bit = 8
	
		
	#turn on comparator
	CMPLO, CMPHO = dutlib.getPLLcompVals("SXR")
	comparator_total = CMPLO + CMPHO

	
	if (comparator_total==1):
		outfp.write('%i,%i,' %(CMPLO,CMPHO))
		outfp.write('%.8f,%.3f,' %(freq*1e-6,ppm))
		outfp.write('%s,' %("Locked"))
		if (abs(ppm) < 10): 
			outfp.write('%s,' %("Pass"))
		else:
			outfp.write('%s,' %("Failed"))
	else:
		outfp.write('%i,%i,' %(CMPLO,CMPHO))
		outfp.write('%.8f,%.3f,' %(freq*1e-6,ppm))
		outfp.write('%s,%s,' %("Not locked","Failed"))
	CSW=csw_mid
	outfp.write('%i,' %(CSW))
	print "Locked CSW: %i \n" %(CSW)	
	
	outfp.write('\n')	
	# turn off comparator
	rlib.WriteRficRegisterBits(pd_comp_register,pd_comp_bit,pd_comp_bit,1)
	rlib.WriteRficRegisterBits(0x80059C,15,15,1) #immediate bit for SXR
	#UNLOCK SXR
	rlib.WriteRficRegisterBits(0x59C, 9, 9, 1) #PD charge pump in main register
	rlib.WriteRficRegisterBits(0x2A2, 0, 0, 1) #PD charge pump
#---------------------------------------------Start temp 0----------------------------------------------------------------	


#---------------------------------------------Start temp -40----------------------------------------------------------------
temp = -40
dutlib.set_temperature(temp)

n = 100#int(input("Enter number of times: "))
# open data file
temperature=str(temp)
outfp = open('..\\data\\SXR_Band13_Locking_LDO_'+LDO_offset+'_chip_'+part+'_temp'+temperature+'.csv', 'w')
outfp.write('Time,BrdNo,PartNo,Temp,Iteration,CMPLO,CMPHO,RX Frequency(MHz),PPM,State,Status, Locked CSW \n')


# open communication
rlib.OpenDevice()
dutlib.selectVersion(2.0)
time.sleep(40)

for i in range(1,n+1,1):
	outfp.write('%s,%s,%s,%s,%i,'%(curr_time,board,part,temperature,i))
	
	#initialize
	dutlib.rficInit()
	dutlib.adjust_2p0_LDO_plus3minus3(0)
	#dutlib.enableCGEN()
	## ENABLE RX
	dutlib.enableCGEN()
	dutlib.enableRxCommon()
	dutlib.enableRx2()
	dutlib.enableRBB2Output()
	dutlib.selectBandRFE2("L2")
	# write gain, bw and corresponding compensation values
	dutlib.loadRxFiltCompVals(0,10) # gain_index = 0 (max gain), bw = 10MHz
	# setup SXR
	csw_high,csw_mid,csw_low,CSWreg = dutlib.sxrSetFreq(751,52)
	
	sg = SG5182.OpenSG()
	SG5182.SetSgOn(sg, 753000000, -70)
	
	sa = SA9020.OpenSA()
	SA9020.Reflevel(sa, 0)
	SA9020.SetSpan(sa, 2e6, 1e6, "MAX")
	SA9020.Peaksearch(sa)
	freq,power = SA9020.GetMarkerFreqPower(sa)
	
	# print freq,power
	SA9020.SetSpan(sa, freq, 2e3, "MAX")
	# raw_input("press enter to proceed ")
	SA9020.Peaksearch(sa)
	freq,power = SA9020.GetMarkerFreqPower(sa)
	print "SXT LO frequency: %.6f \n" %(freq*1e-6)
	ppm=(freq-2000000)/(751)
	
	
	
	pd_comp_register = 0x800598
	pd_comp_bit = 8
	
		
	#turn on comparator
	CMPLO, CMPHO = dutlib.getPLLcompVals("SXR")
	comparator_total = CMPLO + CMPHO

	
	if (comparator_total==1):
		outfp.write('%i,%i,' %(CMPLO,CMPHO))
		outfp.write('%.8f,%.3f,' %(freq*1e-6,ppm))
		outfp.write('%s,' %("Locked"))
		if (abs(ppm) < 10): 
			outfp.write('%s,' %("Pass"))
		else:
			outfp.write('%s,' %("Failed"))
	else:
		outfp.write('%i,%i,' %(CMPLO,CMPHO))
		outfp.write('%.8f,%.3f,' %(freq*1e-6,ppm))
		outfp.write('%s,%s,' %("Not locked","Failed"))
	CSW=csw_mid
	outfp.write('%i,' %(CSW))
	print "Locked CSW: %i \n" %(CSW)	
	
	outfp.write('\n')	
	# turn off comparator
	rlib.WriteRficRegisterBits(pd_comp_register,pd_comp_bit,pd_comp_bit,1)
	rlib.WriteRficRegisterBits(0x80059C,15,15,1) #immediate bit for SXR
	#UNLOCK SXR
	rlib.WriteRficRegisterBits(0x59C, 9, 9, 1) #PD charge pump in main register
	rlib.WriteRficRegisterBits(0x2A2, 0, 0, 1) #PD charge pump
#---------------------------------------------Start temp -40----------------------------------------------------------------	


# close communication
dutlib.set_temperature(25)
#RESET
rlib.WriteRficRegisterBits(0x2d0,8,8,0)	
rlib.WriteRficRegisterBits(0x2d0,8,8,1)
outfp.close()
rlib.CloseDevice()
sys.exit(0)