# =======================================================
# Functions =============================================
# =======================================================
import os
import sys
sys.path.insert(0, os.path.abspath('..\\lib')) #adding directory for libraries

import rlib
import dutlib
import modelib
import speclib
import time

# open data file
#outfp = open('..\\data\\SXT_VCO_openloop.csv', 'w')

board = "E3"

# enter test parameters
part = str(raw_input("Enter rfic chip number: "))
curr_time = time.strftime("%b%d_%H%M", time.localtime())
LDO_offset = str(raw_input("Enter LDO offset percentage (3, 0, -3): "))
#temperature = str(raw_input("Enter temperature: "))


#---------------------------------------------Start temp 85----------------------------------------------------------------
temp = 85
dutlib.set_temperature(temp)
# open data file
temperature=str(temp)
outfpl = open('..\\data\\SXT_VCOL_openloop_LDO'+LDO_offset+'_chip'+part+'_temp'+temperature+'.csv', 'w')
outfph = open('..\\data\\SXT_VCOH_openloop_LDO'+LDO_offset+'_chip'+part+'_temp'+temperature+'.csv', 'w')
outfpl.write('Time,BrdNo,PartNo,Temp,VCOHorL,CSW,VCOFreq(MHz)\n')
outfph.write('Time,BrdNo,PartNo,Temp,VCOHorL,CSW,VCOFreq(MHz)\n')

# open communication
rlib.OpenDevice()
dutlib.selectVersion(2.0)
time.sleep(40)

#initialize
dutlib.rficInit()
dutlib.adjust_2p0_LDO_plus3minus3(0)
dutlib.enableCGEN()

modelib.setupTxPath(LO_Freq_MHz=710, bw=10, dac_option="n", agc=0, pad=6, TBB_Freq_MHz=0)

dutlib.sxtUnlockPLL()
for CSW in range(1024):
	outfpl.write('%s,%s,%s,%s,VCOL,' %(curr_time,board,part,temperature))
	dutlib.sxtWriteCSW(CSW)
	freq,power = speclib.getsxtLOFreq()
	print freq, power
	outfpl.write('%d,%.2f\n' %(CSW,freq*1e-6*6))
	print "VCOL CSW out of 0 to 1023 %d\n" %(CSW)
# close data file
outfpl.close()


#initialize
dutlib.rficInit()
dutlib.adjust_2p0_LDO_plus3minus3(0)
dutlib.enableCGEN()
#TXVCOH (VCOH/4)
modelib.setupTxPath(LO_Freq_MHz=782, bw=10, dac_option="n", agc=0, pad=6, TBB_Freq_MHz=0)
#exit() # added on 2/28/2017 by Sivan as per Raghu's email

dutlib.sxtUnlockPLL()

for CSW in range(1024):
	outfph.write('%s,%s,%s,%s,VCOH,' %(curr_time,board,part,temperature))
	dutlib.sxtWriteCSW(CSW)
	freq,power = speclib.getsxtLOFreq()
	print freq, power
	outfph.write('%d,%.2f\n' %(CSW,freq*1e-6*4))
	print "VCOH CSW out of 0 to 1023 %d\n" %(CSW)
# TXVCOL (VCOL/6)
outfph.close()
#RESET
rlib.WriteRficRegisterBits(0x2d0,8,8,0)	
rlib.WriteRficRegisterBits(0x2d0,8,8,1)			
#---------------------------------------------End temp 85----------------------------------------------------------------


#---------------------------------------------Start temp 25----------------------------------------------------------------
temp = 25
dutlib.set_temperature(temp)
# open data file
temperature=str(temp)
outfpl = open('..\\data\\SXT_VCOL_openloop_LDO'+LDO_offset+'_chip'+part+'_temp'+temperature+'.csv', 'w')
outfph = open('..\\data\\SXT_VCOH_openloop_LDO'+LDO_offset+'_chip'+part+'_temp'+temperature+'.csv', 'w')
outfpl.write('Time,BrdNo,PartNo,Temp,VCOHorL,CSW,VCOFreq(MHz)\n')
outfph.write('Time,BrdNo,PartNo,Temp,VCOHorL,CSW,VCOFreq(MHz)\n')

# open communication
rlib.OpenDevice()
dutlib.selectVersion(2.0)
time.sleep(40)

#initialize
dutlib.rficInit()
dutlib.adjust_2p0_LDO_plus3minus3(0)
dutlib.enableCGEN()

modelib.setupTxPath(LO_Freq_MHz=710, bw=10, dac_option="n", agc=0, pad=6, TBB_Freq_MHz=0)

dutlib.sxtUnlockPLL()
for CSW in range(1024):
	outfpl.write('%s,%s,%s,%s,VCOL,' %(curr_time,board,part,temperature))
	dutlib.sxtWriteCSW(CSW)
	freq,power = speclib.getsxtLOFreq()
	print freq, power
	outfpl.write('%d,%.2f\n' %(CSW,freq*1e-6*6))
	print "VCOL CSW out of 0 to 1023 %d\n" %(CSW)
# close data file
outfpl.close()


#initialize
dutlib.rficInit()
dutlib.adjust_2p0_LDO_plus3minus3(0)
dutlib.enableCGEN()
#TXVCOH (VCOH/4)
modelib.setupTxPath(LO_Freq_MHz=782, bw=10, dac_option="n", agc=0, pad=6, TBB_Freq_MHz=0)
#exit() # added on 2/28/2017 by Sivan as per Raghu's email

dutlib.sxtUnlockPLL()

for CSW in range(1024):
	outfph.write('%s,%s,%s,%s,VCOH,' %(curr_time,board,part,temperature))
	dutlib.sxtWriteCSW(CSW)
	freq,power = speclib.getsxtLOFreq()
	print freq, power
	outfph.write('%d,%.2f\n' %(CSW,freq*1e-6*4))
	print "VCOH CSW out of 0 to 1023 %d\n" %(CSW)
# TXVCOL (VCOL/6)
outfph.close()
#RESET
rlib.WriteRficRegisterBits(0x2d0,8,8,0)	
rlib.WriteRficRegisterBits(0x2d0,8,8,1)			
#---------------------------------------------End temp 25----------------------------------------------------------------



#---------------------------------------------Start temp -40----------------------------------------------------------------
temp = -40
dutlib.set_temperature(temp)
# open data file
temperature=str(temp)
outfpl = open('..\\data\\SXT_VCOL_openloop_LDO'+LDO_offset+'_chip'+part+'_temp'+temperature+'.csv', 'w')
outfph = open('..\\data\\SXT_VCOH_openloop_LDO'+LDO_offset+'_chip'+part+'_temp'+temperature+'.csv', 'w')
outfpl.write('Time,BrdNo,PartNo,Temp,VCOHorL,CSW,VCOFreq(MHz)\n')
outfph.write('Time,BrdNo,PartNo,Temp,VCOHorL,CSW,VCOFreq(MHz)\n')

# open communication
rlib.OpenDevice()
dutlib.selectVersion(2.0)
time.sleep(40)

#initialize
dutlib.rficInit()
dutlib.adjust_2p0_LDO_plus3minus3(0)
dutlib.enableCGEN()

modelib.setupTxPath(LO_Freq_MHz=710, bw=10, dac_option="n", agc=0, pad=6, TBB_Freq_MHz=0)

dutlib.sxtUnlockPLL()
for CSW in range(1024):
	outfpl.write('%s,%s,%s,%s,VCOL,' %(curr_time,board,part,temperature))
	dutlib.sxtWriteCSW(CSW)
	freq,power = speclib.getsxtLOFreq()
	print freq, power
	outfpl.write('%d,%.2f\n' %(CSW,freq*1e-6*6))
	print "VCOL CSW out of 0 to 1023 %d\n" %(CSW)
# close data file
outfpl.close()


#initialize
dutlib.rficInit()
dutlib.adjust_2p0_LDO_plus3minus3(0)
dutlib.enableCGEN()
#TXVCOH (VCOH/4)
modelib.setupTxPath(LO_Freq_MHz=782, bw=10, dac_option="n", agc=0, pad=6, TBB_Freq_MHz=0)
#exit() # added on 2/28/2017 by Sivan as per Raghu's email

dutlib.sxtUnlockPLL()

for CSW in range(1024):
	outfph.write('%s,%s,%s,%s,VCOH,' %(curr_time,board,part,temperature))
	dutlib.sxtWriteCSW(CSW)
	freq,power = speclib.getsxtLOFreq()
	print freq, power
	outfph.write('%d,%.2f\n' %(CSW,freq*1e-6*4))
	print "VCOH CSW out of 0 to 1023 %d\n" %(CSW)
# TXVCOL (VCOL/6)
outfph.close()
#RESET
rlib.WriteRficRegisterBits(0x2d0,8,8,0)	
rlib.WriteRficRegisterBits(0x2d0,8,8,1)			
#---------------------------------------------End temp -40----------------------------------------------------------------

# close communication
dutlib.set_temperature(25)
#RESET
rlib.WriteRficRegisterBits(0x2d0,8,8,0)	
rlib.WriteRficRegisterBits(0x2d0,8,8,1)
rlib.CloseDevice()
sys.exit(0)