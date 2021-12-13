import argparse
import requests
import sys
import json
import base64

# Function for executing HTTP request
def cameras_set_rec_mode(id, token, status):

    # HTTP header. Indicates the MIME document type (json) as well as the authorization key
    headers = {                              
    'accept': 'application/json',
    'Content-Type': 'application/json',
    }
    data = {"rec_mode": status}    # Parameters that shoul be changed in an event

    params = (                              # Parameters of the request.
    ('token', token),
    )

    address = 'https://web.skyvr.videoexpertsgroup.com/api/v2/cameras/%s/' % str(id)   # End point
    
    # Exception block.
    try:
        response = requests.put(address, headers=headers, params = params, data=json.dumps(data), timeout=15)     # Method PUT
    except requests.exceptions.RequestException as e:
        print (e)
        sys.exit(1)
    return response.status_code      # Returns the status of an HTTP request

# Parsing the command line
parser = argparse.ArgumentParser()
parser.add_argument('-access_token', '--access_token', help = 'Access token', required=True)
parser.add_argument('-rec_mode', '--rec_mode',  help = 'Record mode (on, off, by_event)', required=True)

# 
try:
    param = parser.parse_args()
except IOError as msg:
    parser.error(str(msg))

# Checking that the parameter rec_mode is correct. The values should be on, off or by_event.
if param.rec_mode == "on":
    status = "on"
elif param.rec_mode == "off":
    status = "off"
elif param.rec_mode == "by_event":
    status = "by_event"
else:
    print('Specify the parameter "on", "off", "by_event" without quotes')
    sys.exit(1)

# Parsing of the access token for retrieving a token and camid.
token_json=''
try:
    token = base64.b64decode(param.access_token)
    token_json = json.loads(token) 
except Exception:
    print("Error access token") 
    sys.exit(1)

# Function call for sending an HTTP request
code= cameras_set_rec_mode(token_json["camid"], token_json['token'], status)

# Output of the status of the request
print ('Request completed. HTTP status code: ' + str(code)+'\n')
