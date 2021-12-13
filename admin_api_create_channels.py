import argparse
import requests
import sys
import json

# Function for executing HTTP request (channel creation)
def add_channel(vxg_address, Lkey, url, id):
    # HTTP header. Indicates the MIME document type (json) as well as the authorization key
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'LKey %s' % str(Lkey),
    }


    data = '{ "name": "Test_relay", "rec_mode": "on", "relay_to":"%s", "source": { "url": "%s" } }' % (str(id), str(url)) # Data that must be transferred to create a channel
    address = 'http://'+str(vxg_address)+':83/api/v3/channels/' # Server address
    # Exclusion block. If a request error occurs during the sending of the request (for example, the server is not available), the program displays the error status and terminates the execution.
    try:
        response = requests.post(address, headers=headers, data=data)
        print response.text
    except requests.exceptions.RequestException as e:
        print (e)
        sys.exit(1)
    return response.status_code # The function returns the status of the HTTP request sending code

# Parsing program call arguments
parser = argparse.ArgumentParser()
parser.add_argument('-vxg_serv_address', '--vxg_serv_address', help = 'VXG Server address', required=True)
parser.add_argument('-vxg_serv_key', '--vxg_serv_key', help = 'VXG Server key', required=True)
parser.add_argument('-url', '--url',  help = "Camera's URL", required=True)
parser.add_argument('-id', '--id', help = 'ID', required=True, type=int)
# Block responsible for checking the entered parameters. In case of an error, the status and description of use are returned
try:
    param = parser.parse_args()
except IOError as msg:
    parser.error(str(msg))

# Function call to send an HTTP request
code = add_channel(param.vxg_serv_address, param.vxg_serv_key, param.url, param.id)

# Output status of HTTP request.
print ('Request completed. HTTP status code: ' + str(code)+'\n')