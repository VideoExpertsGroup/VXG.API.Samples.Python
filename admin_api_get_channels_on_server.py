import argparse
import requests
import sys
import json

# Function for executing HTTP request (channel creation)
def get_server_channels(backchannel_address, Lkey):
    # HTTP header. Indicates the MIME document type (json) as well as the authorization key
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'LKey %s' % str(Lkey),
    }


    address = str(backchannel_address) + '/api/v3/channels/' # Server address
    # Exclusion block. If a request error occurs during the sending of the request (for example, the server is not available), the program displays the error status and terminates the execution.
    try:
        response = requests.get(address, headers=headers)
        # print (response.text)
    except requests.exceptions.RequestException as e:
        print (e)
        sys.exit(1)
    return response.status_code, response.text # The function returns the status of the HTTP request sending code


# Parsing program call arguments
parser = argparse.ArgumentParser()
parser.add_argument('-serv_backchannel', '--serv_backchannel', help = 'VXG Server address', required=True)
parser.add_argument('-serv_key', '--vxg_serv_key', help = 'VXG Server key', required=True)
# Block responsible for checking the entered parameters. In case of an error, the status and description of use are returned
try:
    param = parser.parse_args()
except IOError as msg:
    parser.error(str(msg))


# Function call to send an HTTP request
code, data = get_server_channels(param.serv_backchannel, param.vxg_serv_key)


# Convertion to json
try:
    data_json = json.loads(data)
except Exception:
    pass


# Output status of HTTP request.
print ('Request completed. HTTP status code: ' + str(code)+'\n')


# Output response content
try:
    print('Number of cameras on server:' + data['meta']['total_count'] + '\n')
    for channel in data['objects']:
        print('   Camera ID:   ' + str(channel['id']) + '\n')
        print('   Created:   ' + str(channel['created']) + '\n')
        print('   Name:   ' + channel['name'] + '\n')
        print('   Recording Mode:   ' + channel['rec_mode'] + '\n')
        print('   streaming:   ' + str(channel['streaming']) + '\n')
        print('   Time Zone:   ' + channel['timezone'] + '\n')
        print('   ----------------------------------')
except Exception:
    print(data)
