import argparse
import requests
import sys
import json
import base64

# Function for executing HTTP request
def storage_api_get_events(token, start, end, limit):
    # HTTP header. Indicates the MIME document type (json) 
    headers = {
    'accept': 'application/json',
    }

    # Parameters of the HTTP request
    params = (
    ('limit', limit),
    ('order_by', 'time'),
    ('events', 'motion,sound'),
    ('start', start),
    ('end', end),
    ('token', token),
    )

    # Exception block
    try:
        response = requests.get('https://web.skyvr.videoexpertsgroup.com/api/v2/storage/events/', headers=headers, params=params, timeout=15) # Функция выполняющая HTTP запрос. Метод GET
    except requests.exceptions.RequestException as e:
        print (e)
        sys.exit(1)
    return response.status_code, response.text    # The function returns the status of the HTTP request  

# Parser for arguments
parser = argparse.ArgumentParser()
parser.add_argument('-access_token', '--access_token', help = 'Access token', required=True)
parser.add_argument('-start', '--start',  help = 'Start time', required=True)
parser.add_argument('-end', '--end',  help = 'End time', required=True)
parser.add_argument('-limit', '--limit',  help = 'Limit', required=True)

# Checking parameters
try:
    param = parser.parse_args()
except IOError as msg:
    parser.error(str(msg))

# Parsing of access token
token_json=''
try:
    token = base64.b64decode(param.access_token) # Decode access token
    token_json = json.loads(token)
except Exception:
    print("Error access token") 
    sys.exit(1)

# Makes HTTP request
code, data = storage_api_get_events(token_json["token"], str(param.start), str(param.end), str(param.limit))


# Returns the status of the HTTP request.
print ('Request completed. HTTP status code: ' + str(code)+'\n')

# Prints a list of events.
try:
    data_json = json.loads(data)
except Exception:
    pass

print ("Events:")
try:
    for obj in data_json["objects"]:
        print obj
except Exception:
    print ("-------------")
