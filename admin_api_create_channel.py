import argparse
import requests
import sys
import json

# Function for executing HTTP request
def admin_api_create_channel(serv_key, name):
    # HTTP header. Indicates the MIME document type (json) as well as the authorization key
    headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': 'LKey ' + serv_key,
    }
    data = '{ "name": "%s"}' % name # Name of the channel to create

     # Exceptions block.
    try:
        response = requests.post('https://web.skyvr.videoexpertsgroup.com:443/api/v3/channels/', headers=headers, data=data, timeout=15)
    except requests.exceptions.RequestException as e:
        print (e)
        sys.exit(1)
    return response.status_code, response.text # function returns the status of the HTTP request sending code and the returned data (access token, id)

# Parsing program call arguments
parser = argparse.ArgumentParser()
parser.add_argument('-serv_key', '--serv_key', help = 'Server key', required=True)
parser.add_argument('-channel_name', '--channel_name',  help = 'Channel name', required=True)
# Block responsible for checking the entered parameters. In case of an error, the status and description of use are returned
try:
    param = parser.parse_args()
except IOError as msg:
    parser.error(str(msg))


# Function call to send an HTTP request
code, data = admin_api_create_channel(param.serv_key, param.channel_name)

# Convertion to json
try:
    data_json = json.loads(data)
except Exception:
    pass


# Output of the status.
print ('Request completed. HTTP status code: ' + str(code)+'\n')

# Output of the HTTP request (acess token, id)
try:
    print ('Acess_token ALL:   ' + data_json["access_tokens"]["all"]+'\n')
    print ('Acess_token WATCH:   ' + data_json["access_tokens"]["watch"]+'\n')
    print ('Id channel:   ' + str(data_json["id"])+'\n')
except Exception:
    print (data)
    


