"""
File:	HelloSerial.py
Author: Brian Han
Date Created: 7/12/17

Basic read and write testing for the PySerial Python class	
"""
import serial
import io
import time

ser = serial.Serial('COM4', 115200, timeout = 5)
print (ser.name)

"""
Example code from the PySerial documentation

sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))

sio.write(unicode("hello\n"))
sio.flush() # it is buffering. required to get the data out *now*
hello = sio.readline()
print (hello.encode('utf-8'))
print(hello == unicode("hello\n"))
"""

# Writes hello world to the chip, and checks the return value to be the same
ser.write ("hello\n")
ser.flush()
hello = ser.readline()
print (hello)
print(hello == "hello\n")

#Writes the d 9 command to the chip, and returns the output
ser.write ("d 9\n")
output = ser.read(1024)
print (output)
print ("Command is done")

#For loop that accepts user input and sends it to the chip, and
# returns the output
while 1:
	input1 = raw_input ("Enter what you want to say: ")
	if input1 == "q":
		break
	ser.write (input1 + "\n")
	output = ser.read(1024)
	print (output)

