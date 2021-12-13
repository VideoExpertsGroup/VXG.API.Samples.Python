import argparse
import requests
import sys
import json
import base64

# Function for executing HTTP request
def cameras_event_processing_events(id, name, token, status):

    # HTTP header. Indicates the MIME document type (json) as well as the authorization key
    headers = {                              
    'accept': 'application/json',
    'Content-Type': 'application/json',
    }

    data = {"record": status, "snapshot": status}    

    params = (                              
    ('token', token),
    )

    address = 'https://web.skyvr.videoexpertsgroup.com/api/v2/cameras/%s/event_processing/events/%s/' % (str(id), name)   # End point
    
    # Exception block.
    try:
        response = requests.put(address, headers=headers, params = params, data=json.dumps(data), timeout=15)     # Method  PUT
    except requests.exceptions.RequestException as e:
        print (e)
        sys.exit(1)
    return response.status_code      # Returns the status of the HTTP request 

# Parsing of the command line
parser = argparse.ArgumentParser()
parser.add_argument('-access_token', '--access_token', help = 'Access token', required=True)
parser.add_argument('-ename', '--ename',  help = 'Event name', required=True)
parser.add_argument('-record_stat', '--record_stat',  help = 'Record off/on', required=True)

try:
    param = parser.parse_args()
except IOError as msg:
    parser.error(str(msg))

# Checking the record_stat parameter. 
if param.record_stat == "on":
    status = True
elif param.record_stat == "off":
    status = False
else:
    print('Specify the parameter "on" or "off"" without quotes')
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
code= cameras_event_processing_events(token_json["camid"], param.ename, token_json['token'], status)

# Status of the HTTP request
print ('Request completed. HTTP status code: ' + str(code)+'\n')
