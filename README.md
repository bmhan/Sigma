### Sigma
### Author: Brian Han
### Date Created: July 10, 2017
### Last Updated: August 10, 2017

# README

-This repo contains all the test scripts at my time at Sigma Designs.
-These scripts automate testing Sigma chips, using Litepoint as the
primary testing system, with other components integrated in later.
-"WIP" is where the various iterations of my scripts are located.
-If you wish to trace the progress of the script over time, view
the CHANGELOG.md located in the "WIP" folder.
-"Sample-Code" is the starter code provided by Sirius Ding at
Litepoint to help get started working with the Litepoint machine.
-"pyFunctionalTest" contains example code using pySerial to help
me get started using the serial library.

-------------------------------------------------------------------------------
-------------------------------------------------------------------------------
-------------------------------------------------------------------------------

# Setup

-These files are to be run using Python 2.7.13.
Doing otherwise would use the wrong socket library conventions.
(ASCII v Binary)
-Third-Party Python Library Modules Needed for these programs:
        PySerial
        PyVisa
        ftd2xx
-In addition, to PyVisa, you will need to install NI-VISA from 
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
