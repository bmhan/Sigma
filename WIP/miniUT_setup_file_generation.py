# -----------------------------------------------------------------------------
# Name:        miniUT_setup_file_generation.py
# Purpose:     Script that produces the miniUT.setup file 
# Created:     8/10/2017
# Last Updated: 8/10/2017
#
# This quick script produces the JSON miniUT.setup file used by the latest version 
# of the miniUT testing scripts and GUI(newest version at the time of this 
# update:
# MiniUT_GUI_v2_shortened.py and test_miniUT_v2_shortened.py)
# 
# It is not recommended to change any values EXCEPT for the tuples in 
# rb_and_scale, which are transcribed directly from the dictionary
# rb_and_scale_key.
# -----------------------------------------------------------------------------

# This produces the miniUT.setup file in a JSON format. For more information on
# how to read and process this format, checkout Python's documentation of JSON
# online. If you wish to add on to the .setup file to accomodate adjustments to
# the script, check the link below for formatting and the chart :
# http://json.org/example.html
#
# JSON to Python object chart:
#   JSON            Python
#   object          dict
#   array           list
#   string          str
#   number(int)     int
#   number(real)    float
#   true            True
#   false           False
#   null            None


import json


info = {

        "VOLT" : 2.5,
        "HOST" : '10.10.14.202',
        "DEFAULT_HOST":'10.10.14.202',
        "PORT": '24000',
        "CSW_CENTER": "9",
        "DUT": "miniUT Rev 8",
        "SN":"10",
        "DEFAULT_SN": "10",
        "COM": "COM8",
        "PS_ADDRESS": 'GPIB::9::INSTR',
        "CABLE_LOSS_DB": 11,
        "DEFAULT_CABLE_LOSS_DB": 11,
        "EVM_LIMIT": 6,
        "DEBUG": False,
        "STEP_TEST": False,
        "LOGGING": True,
        "SPEC_CHECK": True,
        "rb_and_scale": [
            ['1', '97A0'],
            ["24",'177F'],
            ["50", '1758']
        ],
        "rb_and_scale_key": {
            
            1: '97A0',
            2: '9772',
            3: '57B6',
            4: '579E',
            5: '578D',
            6: '5781',
            8: '5770',
            9: '576A',
            10:'5765',
            12:'17B4',
            15:'17A1',
            16:'179C',
            18:'1793',
            20:'178B',
            24:'177F',
            25:'177D',
            27:'1778',
            30:'1772',
            32:'176E',
            36:'1768',
            40:'1763',
            45:'175D',
            48:'175A',
            50:'1758',
        },
        "specs": {
            "POWER_LOWER_LIMIT" : -60,
            "POWER_UPPER_LIMIT": 30,
            "IQ_OFFSET_LOWER_LIMIT": -50,
            "IQ_OFFSET_UPPER_LIMIT": -20,
            "FREQ_ERROR_LOWER_LIMIT": -3000,
            "FREQ_ERROR_UPPER_LIMIT": 3000,
            "DATA_EVM_LOWER_LIMIT": 0,
            "DATA_EVM_UPPER_LIMIT": 500,
            "PEAK_DATA_EVM_LOWER_LIMIT": 0,
            "PEAK_DATA_EVM_UPPER_LIMIT": 500,
            "RS_EVM_LOWER_LIMIT": 0,
            "RS_EVM_UPPER_LIMIT": 500,
            "PEAK_RS_EVM_LOWER_LIMIT": 0,
            "PEAK_RS_EVM_UPPER_LIMIT": 500,
            "IQ_IMBALANCE_GAIN_LOWER_LIMIT": -5,
            "IQ_IMBALANCE_GAIN_UPPER_LIMIT": 5,
            "IQ_IMBALANCE_PHASE_LOWER_LIMIT": -5,
            "IQ_IMBALANCE_PHASE_UPPER_LIMIT": 5,
            "ACLR_EUTRA_L_LOWER_LIMIT": 0,
            "ACLR_EUTRA_L_UPPER_LIMIT": 70,
            "ACLR_EUTRA_U_LOWER_LIMIT": 0,
            "ACLR_EUTRA_U_UPPER_LIMIT": 70,
            "CURRENT_LOWER_LIMIT": 0,
            "CURRENT_UPPER_LIMIT": 2
        }
    }

with open ("miniUT.setup", 'wb') as file:
    json.dump (info, file) 
    file.close()

"""
#Example of reading data from from a JSON file, printing from it,
#changing data in it and writing the changes back to the files
with open ("miniUT.setup", 'rb') as file:
    data = json.load(file)
    print type(data)
    print data["rb_and_scale"][0][0]
    print data["rb_and_scale_key"]["1"]
    print data["SN"]
    data["SN"] = "foobar"

    if '48' in data["rb_and_scale_key"].keys():
        data["rb_and_scale"].append(['48',data["rb_and_scale_key"]['48']])

    file.close()

with open ("miniUT.setup", 'wb') as file:
    json.dump (data, file)
    file.close()
"""