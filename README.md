# Sigma
# Author: Brian Han
# Date Created: July 10, 2017
# Last Updated: July 25, 2017

These files are to be run using Python 2.7.13.
Doing otherwise would use the wrong socket library conventions.
(ASCII v Binary)

Third-Party Python Library Modules Needed for these programs:
        PySerial
        PyVisa

In addition, to PyVisa, you will need to install NI-VISA from 
National Instruments, as well as their drivers for GBIB - USB.
The driver version used for these programs were NI-488.2

In order to use the testing script, the computer must be
connected to the  Agilent 66311B Power Supply through a
GBIB connection and the miniDUT itself through Serial.
The miniDUT connects to the IQxstream machine through
an LTE connection, as well as the power supply.

WIP - A black-box testing GUI that has the main feature
of running the script through a click of a button
rather than through command line. 
