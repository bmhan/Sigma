# -----------------------------------------------------------------------------
# Name:        README
# Purpose:     Contains general overview of the programs and the installation
#              instructions to get the program to run, and how to run.
# Created:     8/8/2017
# Last Updated: 8/8/2017
#
# -----------------------------------------------------------------------------

-OVERVIEW-

    The program consists of 4 files: MiniUT_GUI_shortened.py ,
    test_miniUT_shortened.py, socket_interface.py, miniUT.setup.
    
    MiniUT_GUI_shortened.py:
        The GUI for the testing script, test_miniUT_shortened.py. Allows the
        user to enter 3 inputs: the HOST of the Litepoint machine in order to
        establish a socket connection, the SN version of the board being
        tested, and the CABLE_LOSS from the cable if attentuation is used.
        The printed stdout output from the testing script is displayed in a
        Text box in the GUI, and will tell the user when the program finishes.
        
        A NOTE about scanning for the SN instead of entering it manually: be
        sure to have the cursor clicked on the entry box for SN before you
        scan, or the SN will not be recorded by the GUI.
        
    test_miniUT_shortened.py:
        The actual testing script.  The program does a "shortened" sweep of the
        gain values across 3 nRB presets: 1, 24, 50.  The script performs this
        sweep by forming a connection between 5 devices: Litepoint, the Agilent
        66311B power supply, the Fluke 8845A multimeter, the "USB Relay Box",
        and the DUT. Litepoint is connected through the Internet (socket
        connection), the power supply and multimeter through GPIB, and the
        relay and DUT through a serial connection.
   
        The results of this test are stored in a '.csv file' located in the same
        folder where these program files are located.  The naming convention of
        the '.csv' file is "miniUT Rev E8_SN_<SN given by the user>.csv".
        
        NOTE: If you run the same test with the same given inputs, the new .csv
        file generated will erase over the previous file. Be sure to rename your
        .csv file after every test if you want to repeat the same test with the
        same parameters.
        
    socket_interface.py
        Interface used by the testing script test_miniUT_shortened.py to form a 
        socket connection with Litepoint. Important to note that while the
        script runs, there is limited access to the Litepoint GUI, as Litepoint
        automatically restricts GUI access as long as the script has remote 
        access.
        
    miniUT.setup
        A configuration file for the script, written in a JSON format. Important
        variables to note are DEFAULT_HOST, DEFAULT_SN, DEFAULT_CABLE_LOSS_DB,
        which are the default key values for the MiniUT_GUI_shortened.py input.
        Editing this file is not recommended, as the testing script depends on
        the correctness of the data in this file.
        
        
        
        
-INSTALLATION-

    Before you begin the program, make sure you have Python 2.7 installed. The 
    program WILL NOT work with Python 3.
    
    Python 2.7 can be installed on their website here:
    https://www.python.org/downloads/
    
    
    Once Python 2.7 is installed, the program will need a few third-party Python
    modules to work, which will be detailed as follows:
    
        pySerial - Allows Python to communicate through a serial connection.
        pySerial can be downloaded here:
        https://pypi.python.org/pypi/pyserial
        
        
        ftd2xx - Allows Python to communicate with the relay.
        ftd2xx can be downloaded here:
        https://pypi.python.org/pypi/ftd2xx
        
        
        pypiwin32 - Necessary for ftd2xx to work, as ftd2xx builds on top
        of pypiwin32.
        pypiwin32 can be downloaded here:
        https://pypi.python.org/pypi/pypiwin32
        
        
        pyVisa - Allows Python to communicate with the GPIB instruments.
        pyVisa can be downloaded here:
        https://pypi.python.org/pypi/PyVISA
        
    
    Once you have downloaded the modules, they still must be installed and
    put in the right location for Python to locate them. Directions on how
    to do that can be found here:
    http://www.instructables.com/id/How-to-install-Python-packages-on-Windows-7/
    
    In addition to these modules, pyVisa requires the installation of NI-VISA,
    while communication with the GPIB-connected instruments require drivers
    in NI-488.2. Both of these applications can be downloaded from the National
    Instruments website, linked below: (NOTE: Make sure when you download
    NI-488.2, you check the box that mentions 'GPIB' drivers during the
    installation process. Otherwise, drivers for the GPIB instruments will not
    be downloaded)
    http://www.ni.com/download/ni-visa-17.0/6646/en/
    http://www.ni.com/download/ni-488.2-17.0/6627/en/
    