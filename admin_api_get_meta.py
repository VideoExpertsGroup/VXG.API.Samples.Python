import argparse
import requests
import sys
import json

# Function for executing HTTP request
def admin_api_get_meta(serv_key, id_channel):
    # HTTP header. Indicates the MIME document type (json) as well as the authorization key
    headers = {
    'accept': 'application/json',
    'Authorization': 'LKey ' + serv_key,
    }
    address = 'https://web.skyvr.videoexpertsgroup.com:443/api/v3/channels/%s/meta/' % id_channel # End point
    # Exceptions block.
    try:
        response = requests.get(address, headers=headers, timeout=15)
    except requests.exceptions.RequestException as e:
        print (e)
        sys.exit(1)
    return response.status_code, response.text    # The function returns the status and the return data

# Parsing of the command line
parser = argparse.ArgumentParser()
parser.add_argument('-serv_key', '--serv_key', help = 'Server key', required=True)
parser.add_argument('-id_channel', '--id_channel',  help = 'Channel id', required=True, type=int)


try:
    param = parser.parse_args()
except IOError as msg:
    parser.error(str(msg))

# Function call
code, data = admin_api_get_meta(param.serv_key, str(param.id_channel))

# Status of the HTTP request
print ('Request completed. HTTP status code: ' + str(code)+'\n')

# Вывод полученных данных
try:
    data_json = json.loads(data)
except Exception:
    pass
print ("Channel meta info:")
try:
    for obj in data_json["objects"]:
        print (obj)
except Exception:
    print ("-------------")