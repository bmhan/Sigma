#Practice place for JSON file interaction
#DictReader/DictWriter v json
#Will need some overhead to switch current data and logic from
#dict to json
#With json, when I read the data from the file, they are 
#automatically formatted into a data structure that I can use.
#Currently, I have to do this step myself, which becomes
#more complicated when I require nested data structures
#e.g. rb_hex
#Should think of switching to json NOW
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
"""
info = {"menu": {
  "id": "file",
  "value": "File",
  "popup": {
    "menuitem": [
      {"value": "New", "onclick": "CreateNewDoc()"},
      {"value": "Open", "onclick": "OpenDoc()"},
      {"value": "Close", "onclick": "CloseDoc()"}
    ]
  }
}} 
with open ("miniUT.setup", 'wb') as file:
    json.dump (info, file) 
    file.close()

with open ("miniUT.setup", 'rb') as file:
    data = json.load(file)
    print type(data)
    print data["menu"]["popup"]["menuitem"][0]["value"]
"""

"""
        SN
        DUT
        CSW_CENTER (e.g. 9 out of 0 - 1f)
        COM, GPIB (? Have logic to make it a dynamic check in test_Visa)
        PS_NAME (important later, maybe if using multiple power supplies)
        HOST
        PORT (maybe not)
"""

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


with open ("miniUT.setup", 'rb') as file:
    data = json.load(file)
    print type(data)
    print data["rb_and_scale"][0][0]
    print data["rb_and_scale_key"]["1"]
    print data["SN"]
    """
    if '48' in data["rb_and_scale_key"].keys():
        data["rb_and_scale"].append(['48',data["rb_and_scale_key"]['48']])
    """
    file.close()

with open ("miniUT.setup", 'wb') as file:
    json.dump (data, file)
    file.close()