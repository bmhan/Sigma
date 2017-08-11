## Sigma
## Author: Brian Han
## Date: 8/10/17

# Changelog

All version changes from file to file is documented here.
Files are listed from newest to oldest order, descending by section

## GUIs

## MiniUT_GUI_Black_wiht_subprocess_old_copy
### Added
- Update of MiniUT_GUI_Black

### Changed
- Use subprocessing to run script without GUI hanging
- Runs script test_miniUT_shortened.py
- Improved regex logic

## test_miniUT_GUI_bad_thread.py
### DOES NOT WORK

## flash_login_miniUT_GUI
### INCOMPLETE; USE "flash_miniUT_GUI" INSTEAD

## flash_miniUT_GUI
### Added
- Flash the DUT using Serial library
- User defines the path to a firmware file with a file dialog
- Update DUT firmware with the press of a button
- Implement threading to prevent GUI from crashing

### Changed
- Different functionality from the previous GUI; not an update

## MiniUT_GUI_Black
### Added 
- Error Message Handling
- Regex logic to make sure user has not entered garbage values

### Changed 
- Runs test_miniUT_RB_PS_66311B_copy_9
- User enters only the Serial Number and the COM for the DUT

## LTE_GUI_Basic
### Added
- First version of the miniUT GUI
- Allow user to enable debugging, set gain range, enter
serial number, set voltage, and set current
- Runs test_miniUT_RB_PS_66311B with the inputed settings
- Note that this version is not multithreaded or multiprocessed,
so program hangs while the script is running
- Not recommended for use

***************************************************************************

## Test Scripts

## modified_test_miniUT_HH_RB_PA_E3648A
### REDACTED SCRIPT; DO NOT USE

## test_miniUT_crystal_rb
### REDACTED SCRIPT; DO NOT USE

### Changed
- Not a direct upgrade over the previous script; serves a different purpose
## test_miniUT_RB_PA_E3648A
### IMPORTANT NOTE
- The 'low power mode' measurement is not implemented correctly
in this version. If you want to use the 5-range sweep, comment out
line #735, and run the script 

### Added
- Sweep 5 sets of values: PA Mode (high or low power), 
PA Bias (0,10,20,30,7f, fe), PA VCC (1 to 3.5 V), nRB, gain
- Measure voltage at 'low power mode' (unimplemented unit testing)
- Logic to communicate with relay and Fluke 8845A multimeter
- Boolean to enable logging of all output to the console
- Logic to retry measurement a few times in case of signal loss

### Changed
- Using power supply E3648A

## test_miniUT_RB_PS_E3648A
### Changed
- Using power supply E3648A
- Go back to creating one .csv file for all nRB and their gain sweep

## test_miniUT_RB_PS_66311B
### Added
- Boolean to enable break-like steps at the end of each measurement
- Error message printing and return values
- Test to compare the output with expected values from input_spec.txt 

### Changed
- Creates separate .csv files for each nRB with their gain values
- Using power supply 66311B
- Integrated test_crystal logic into the main test script

### Removed
- Dependence on test_crystal to find CSW

## test_miniUT_gain_rb_version_with_curr
### Added
- Make call to test_crystal.main() to find CSW

### Changed
- Sweeps gain 0,1,2,3,4,5,10,20...70

### Removed
- Ask user input for gain range to sweep
- No longer in high power mode 

## test_gain_rb_version_with_curr
### Added
- Measuring current and voltage in addition to the other measurements
- Turn off power supply when the test finishes

## test__rb_and_rb_offset_version
### Added
- Sweep nRB, RB offset, and gain
- Asks user for RB offset
- Enable / Disable some print statements with a DEBUG variable
- Turn on Power Supply E3648A to set Voltage and current
- Sweep nRB, RB offset, and gain
- Set fine gain using 'wr 242 4444'

## test_gain_rb_version
### Added
- Sweeps nRB, then gain
- Set gain using 'd 26 X'
- Asks user for gain range to sweep
- Delay between sending Litepoint calculation command and requesting
the result
- Capture ACLR E-UTRA Lower and Upper in the measurements

### Changed
- Measurements are now done for 10 subframes, not 1, taking the average
of these 10 subframes
- 2c0 set to 'a28'

## test_rb_version
### Added 
- Sweeps nRB only

### Removed
- No longer using 'd 27'
- No longer setting bias to 'fe'

## test_gain_outer_rb_inner_version
### Added
- Sweeps gain, then nRB
- Adjust Average Power result to account for Cable Loss (in dB)
- Takes in user input to determine the gain range to sweep

### Changed
- Uses input_rb_hex.csv as the list of nRB values to sweep
- Send PUSCH using 'd 35'
- 2c0 set to 'd28'

## test_5C4_5BC_version & input_5c4_5bc.csv
### Added
- Sweeps gain, set through registers 5C4 and 5BC, for nRB 1
- input_5c4_5bc.csv is the list of values read in to set gain

### Changed
- Bias current set to 'fe', Measured in high power mode, 'd 27' used


## test_rb_version_old
### Changed
- Sweeps nRB values from 1 to 100 using 'd 34'
- Measures a subframe for each gain set
- Writes results to two .csv files, one sorted and another unsorted
- 2c0 set to 128

## test_Power
### Added
- Setups DUT to send PUSCH signal, setups connection to Litepoint, and
makes a measurement for one subframe
- Result is saved in a dictionary (unused) and printed to the console

## getPower
### Changed
- A close version of my_calibration
- Unstable

## my_calibration
### Changed
- Attempt to adapt sample_tx_rx_calibration to Sigma's Litepoint machine
- Incomplete and does not work correctly

## sample_tx_rx_calibration
### Added
- Functionality to connect to Litepoint and make measurements on a DUT
and a generated waveform 
- Does not work on its own; is the basis for future iterations of the
testing script
- Provided by Sirius Ding

***************************************************************************

## Example_05192017 Files provided by Sirius

## sample_tx_rx_calibration
### Added
- Functionality to connect to Litepoint and make measurements on a DUT
and a generated waveform 
- Does not work on its own; is the basis for future iterations of the
testing script
- Provided by Sirius Ding

## lte_load_vsg
### Added
- Functionality to load the waveform generated in lte_waveform_generation
onto Litepoint and play iterations
- Provided by Sirius Ding

### Changed
- Changed the name of the loaded script to account for changes in
lte_waveform_generation
  
## lte_waveform_generation
### Added
- Functionality to create a waveform, ".iqsvg", that can be loaded in
by Litepoint
- Provided by Sirius Ding

### Changed
- Changed the RNTI value for Luc, as well as the name of the generated file.

## socket_interface
### Added
- Functionality to establish connection to Litepoint through a socket
connection
- Provided by Sirius Ding

### Changed
- Added correct local HOST to communciate with Sigma's Litepoint machine
- Added optional debug statements and error return logic

***************************************************************************

## My Personal Short Test Scripts

## test_Visa
### Added
- Sweeps the list of devices connected to the PC through USB, GPIB, etc.
- Determines which connection is the DUT, power supply, multimeter

## test_sweep_0_1f
### Added
- Sweeps for CSW (crystal) from 0 to 1f
- Includes faster test logic that uses frequency error and an assumed
central CSW ('9') to find the CSW in under 5 tests

## simple_RB_PA_test
### Added
- Setup PA Mode, PA Bias, PA VCC, nRB, gain
- Setup Power Supply
- Setup Litepoint
- Not for scripting; just for single setup and test

## test_crystal
### Added
- Looks for the CSW value by looking at the lowest frequency error
and Data EVM