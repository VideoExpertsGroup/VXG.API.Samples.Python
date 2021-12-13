import argparse
import requests
import sys
import json
import base64

# Function for executing HTTP request
def cameras_enable_motion_detector(id, token, status):

    # HTTP header. Indicates the MIME document type (json) as well as the authorization key
    headers = {                              
    'accept': 'application/json',
    'Content-Type': 'application/json',
    }
    data = {"objects":[{"enabled": status, "map": "6zEBMDDrMQEwMOsxATAw6zEBMDDrMQEwMOsxATAw6zEBMDDrMQEwMOsxATAw6zEBMDDrMQEwMOsxATAw6zEBMDDrMQEwMOsxATAw"}]}

    params = (                              
    ('token', token),
    )

    address = "https://web.skyvr.videoexpertsgroup.com/api/v2/cameras/%s/motion_detection/regions/" % str(id)   # Адресс запроса

    
    # Exceptions block.
    try:
        response = requests.put(address, headers=headers, params = params, data=json.dumps(data), timeout=15)     # Method PUT
    except requests.exceptions.RequestException as e:
        print (e)
        sys.exit(1)
    return response.status_code      # Returns the status of the HTTP request 

# Parsing of the command line
parser = argparse.ArgumentParser()
parser.add_argument('-access_token', '--access_token', help = 'Access token', required=True)
parser.add_argument('-enabled', '--enabled',  help = 'Enable motion detector (true, false)', required=True)

try:
    param = parser.parse_args()
except IOError as msg:
    parser.error(str(msg))

# Checking the record_stat parameter.
if param.enabled == "true":
    status = True
elif param.enabled == "false":
    status = False
else:
    print('Specify the parameter "true" or "false" without quotes')
    sys.exit(1)

# Parsing of the access token for retrieving of the token and camid.
token_json=''
try:
    token = base64.b64decode(param.access_token)
    token_json = json.loads(token) 
except Exception:
    print("Error access token") 
    sys.exit(1)

# Function call
code= cameras_enable_motion_detector(token_json["camid"], token_json['token'], status)

# Status of the HTTP request
print ('Request completed. HTTP status code: ' + str(code)+'\n')
