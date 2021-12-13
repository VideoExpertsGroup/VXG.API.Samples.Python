import argparse
import requests
import sys
import json

# Function for executing HTTP request
def admin_api_set_meta(serv_key, id_channel, tag, data):
    # HTTP header. Indicates the MIME document type (json) as well as the authorization key
    headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': 'LKey ' + serv_key,
    }
    data = '{ "tag": "%s", "data": "%s"}' % (tag, data)      #Input data
    address = 'https://web.skyvr.videoexpertsgroup.com:443/api/v3/channels/%s/meta/' % id_channel
    # Exception block.
    try:
        response = requests.post(address, headers=headers, data=data, timeout=15)
    except requests.exceptions.RequestException as e:
        print (e)
        sys.exit(1)
    return response.status_code        # Function returns the status 

# Parsing of the command line
parser = argparse.ArgumentParser()
parser.add_argument('-serv_key', '--serv_key', help = 'Server key', required=True)
parser.add_argument('-id_channel', '--id_channel',  help = 'Channel id', required=True, type=int)
parser.add_argument('-tag', '--tag', help = 'Tag', required=True)
parser.add_argument('-data', '--data',  help = 'Data', required=True)

try:
    param = parser.parse_args()
except IOError as msg:
    parser.error(str(msg))

# Function call
code = admin_api_set_meta(param.serv_key, str(param.id_channel), param.tag, param.data)

# Output of the status.
print ('Request completed. HTTP status code: ' + str(code)+'\n')