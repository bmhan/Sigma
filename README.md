### Sigma
### Author: Brian Han
### Date Created: July 10, 2017
### Last Updated: August 10, 2017

# README

- This repo contains all the test scripts at my time at Sigma Designs.
- These scripts automate testing Sigma chips, using Litepoint as the
primary testing system, with other components integrated in later.
- "WIP" is where the various iterations of my scripts are located.
- If you wish to trace the progress of the script over time, view
the CHANGELOG.md located in the "WIP" folder.
- "Sample-Code" is the starter code provided by Sirius Ding at
Litepoint to help get started working with the Litepoint machine.
-"pyFunctionalTest" contains example code using pySerial to help
me get started using the serial library.

-------------------------------------------------------------------------------
-------------------------------------------------------------------------------
-------------------------------------------------------------------------------

# Setup

- These files are to be run using Python 2.7.13.
Doing otherwise would use the wrong socket library conventions.
(ASCII v Binary)
- Third-Party Python Library Modules Needed for these programs:
        PySerial
        PyVisa
        ftd2xx
- In addition, to PyVisa, you will need to install NI-VISA from 
National Instruments, as well as their drivers for GBIB - USB.
The driver version used for these programs were NI-488.2

### More Detailed Setup 

For more on setup and how to run these programs,
 checkout the 'README.md' located in the
"test MiniUT PCBA ATS" folder. It will show you how to run the latest version
of the testing script, as well as all the installations needed first.


-------------------------------------------------------------------------------
-------------------------------------------------------------------------------
-------------------------------------------------------------------------------

# Documentation for Relevant Scripts

## test_miniUT_v2_shortened.py

    This is the latest version of the testing script. The test sweeps nRB and
gain. miniUT.setup file is the configuration file for this script. The logic
for this script is as follows:
- Find the GPIB port used for the power supply (Agilent 6631B) and set voltage
to 2.5, and the current to low power.
- Find the GPIB port used for the multimeter (Fluke 8845A)
- Find the current at low power mode, communicating with the power supply,
relay, and the multimeter to make the current measurement.
- Setup a connection to Litepoint and the DUT, and perform the sweep
of nRB and gain. The results of each individual test is stored into a .csv
file, generated in the current directory.
- Run the specification check to make sure the results of the sweep match
the desired range.

## MiniUT_GUI_v2_shortened.py

    This is the GUI for the test_miniUT_v2_shortened.py script. The GUI
expects user to enter three key inputs:
- The HOST IP address to establish a connection to Litepoint
- The CABLE LOSS in dB from the cable to properly calculate the average
power level
- The SN (Serial Number) of the board in question.

The SN can be typed in, or scanned in by barcode. Once satisfiable inputs
are entered, the program can be run with the click of a button. In addition
to just key values, there are some features in the menubar the user can use:
- A standard "Exit" option
- A "Set Default Values" option so the user can set what values the default
button will set the key values to
- A "Settings" option that allows the user to customize their output options.
- An "Update Firmware" option that allows the user to update the firmware of
the board.
> NOTE: The "Update Firmware" feature is commented out. It works, but you will
need to uncomment the logic for updating the firmware

## test_miniUT_sweep_five_values.py

> NOTE: While the latest script, test_miniUT_v2_shortened.py has logic to
automatically find the correct ports for the measuring equipment and the COM
for the DUT, this script does not contain that logic, and these connections
must be set using global variables found at the top of the script.
> POWER SUPPLY: This script uses the E3648A power supply, not the 66311B. The
SCPI commands to program E3648A are not the same for 66311B (check out
test_66311B.py and test_3648A.py to see the differences).

    This script is the one used for overnight testing (as it takes upwards of
7 - 8 hours), as it sweeps 5 sets of values: The PA High Power / Low Power mde,
The PA Bias, The PA VCC, nRB, and gain. The script sweeps the values in that 
order, gain being the innermost value swept first.

> NOTE: This script does not take advantage of the configuration file
miniUT.setup. This script uses "input_spec.txt" instead to get the specification
range to compare the results to.

## simple_RB_PA_test.py

- This is a basic script you can use to quickly set up the DUT and the Litepoint
to measure the TX (it does not actually run the test; you do it youself through
Litepoint's provided GUI)
- Use it to do a quick unit test.
- The script DOES NOT set up the CSW (crystal) or automate the power supply
- You can customize the DUT setup with the global variables at the top of the
script.