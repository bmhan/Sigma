# -----------------------------------------------------------------------------
# Name:        README
# Purpose:     Contains the following about the miniUT PCBA ATE functionality:
#                       Overview
#                       Installation
#                       How to Run.
# Created:     8/8/2017
# Last Updated: 8/9/2017
#
# -----------------------------------------------------------------------------

-OVERVIEW-

    The program consists of 4 files: miniUT_PCBA_ATE.py,
    miniUT_PCBA_ATE_script.py, socket_interface.py, miniUT.setup
    all located in the test_miniUT_PCBA_ATE folder.
    
    miniUT_PCBA_ATE.py:
        The GUI for the testing script, "miniUT_PCBA_ATE_script.py". Allows the
        user to enter 3 inputs: the HOST of the Litepoint machine in order to
        establish a socket connection, the SN version of the board being
        tested, and the CABLE_LOSS from the cable if attentuation is used.
        The printed stdout output from the testing script is displayed in a
        Text box in the GUI, and will tell the user when the program finishes.
        
        A NOTE about scanning for the SN instead of entering it manually: be
        sure to have the cursor clicked on the entry box for SN before you
        scan, or the SN will not be recorded by the GUI.
        
    miniUT_PCBA_ATE_script.py:
        The actual testing script.  The program does a "shortened" sweep of the
        gain values across 3 nRB presets: 1, 24, 50.  The script performs this
        sweep by forming a connection between 5 devices to the PC:
        Litepoint, the Agilent 66311B power supply, the Fluke 8845A multimeter,
        the "USB Relay Box", and the DUT. Litepoint is connected through the
        Internet (socket connection), the power supply and multimeter through
        GPIB, and the relay and DUT through a serial connection.
   
        The results of this test are stored in a '.csv file' located in the same
        folder where these program files are located.  The naming convention of
        the '.csv' file is "miniUT Rev E8_SN_<SN given by the user>.csv".
        
        A log of the runtime is also produced for debugging purposes.

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

    The installation files are located in a zipped folder included with this folder.
    You can download the files in the links  described below, or use the files from
    the zipped folder (make sure to install Python 2.7 first before installing the
    modules). NOTE: Once you have downloaded the modules, they still must be
    installed and put in the right location for Python to locate them. Directions
    on how to do that can be found here:
    http://www.instructables.com/id/How-to-install-Python-packages-on-Windows-7/
    
    
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
        
    
    In addition to these modules, pyVisa requires the installation of NI-VISA,
    while communication with the GPIB-connected instruments require drivers
    in NI-488.2. Both of these applications can be downloaded from the National
    Instruments website, linked below: (NOTE: Make sure when you download
    NI-488.2, you check the box that mentions 'GPIB' drivers during the
    installation process. Otherwise, drivers for the GPIB instruments will not
    be downloaded)
    http://www.ni.com/download/ni-visa-17.0/6646/en/
    http://www.ni.com/download/ni-488.2-17.0/6627/en/
    
    
    
-HOW TO RUN-
    Before even thinking of running the script, make sure all the equipment
    and devices are connected properly: the multimeter and power supply
    connected through GPIB to the PC, the relay and DUT connected by serial to
    the PC, and  the DUT connected to Litepoint through port 'RF4A' (it must
    be port 'RF4A'; otherwise, you must go into the script code and
    change which port is being set).Also, be sure that the 'Force Awake'
    switch is toggled on the DUT, or else the data will look off.

    1) Make sure all the given files are in the same directory.
    2) Double Click on "miniUT_PCBA_ATE.py" to run the GUI
    3) Input the key values. If you do not satisfy these inputs, the program
       will not allow you to run the test (make sure these values are correct;
       if the wrong host is entered, the test will fail to connect to Litepoint
       and not run. If you enter the wrong cable loss, the average power 
       measurements will all be off)
    4) With the inputs satisfied, run the test
    5) Wait for the test to finish; typically takes ~2 minutes
    6) Repeat steps 3 - 5 as desired
    
    RECOMMENDED: Create a shortcut on the Desktop to run the file.
                 Right click on the "miniUT_PCBA_ATE.py" file.
                 Click "Create Shortcut" (on Windows) or
                 Click "Make Alias" (on Mac) to create the shortcut.
                 Left Click and Drag the Shortcut on to the Desktop. 
