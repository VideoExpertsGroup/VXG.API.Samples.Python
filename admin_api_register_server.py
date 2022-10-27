import argparse
import requests
import sys
import json

def admin_api_register_server(cert, key, uuid, owner_id):
    session = requests.Session()
    session.cert = (cert, key)

    # API request
    api_url = 'https://web.skyvr.videoexpertsgroup.com:9000/api/v6/admin/servers/'
    data = {'uuid': uuid, 'owner': int(owner_id)}
    try:
        response = session.post(url=api_url, json=data, verify=False)
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)

    session.close()
    return response.status_code, response.text


# Parsing program call arguments
parser = argparse.ArgumentParser()
parser.add_argument('-cert', '--path_to_cert', help = 'Path to .crt file', required=True)
parser.add_argument('-key', '--path_to_key',  help = 'Path to .key file', required=True)
parser.add_argument('-uuid', '--server_uuid',  help = 'Instance UUID of server', required=True)
parser.add_argument('-owner', '--owner_id',  help = 'User ID of user who\'s Cloud Relay Key is register in the server settings', required=True)
# Block responsible for checking the entered parameters. In case of an error, the status and description of use are returned
try:
    param = parser.parse_args()
except IOError as msg:
    parser.error(str(msg))


# Function call to send an HTTP request
code, data = admin_api_register_server(param.path_to_cert, param.path_to_key, param.server_uuid, param.owner_id)


# Convertion to json
try:
    data_json = json.loads(data)
except Exception:
    pass


# Output of the status.
print('Request completed. HTTP status code: ' + str(code)+'\n')

# Output of the HTTP request (acess token, id)
try:
    if data_json['online']:
        print('API Endpoint:   ' + data_json['api_endpoint']+'\n')
        print('Endpoint:   ' + data_json['endpoint']+'\n')
        print('Expired:   ' + data_json['expires']+'\n')
        print('Server ID:   ' + str(data_json['id'])+'\n')
        print('l_key:   ' + data_json['l_key']+'\n')
        print('Server name:   ' + data_json['name']+'\n')
        print('Online:   ' + str(data_json['online'])+'\n')
        print('Owner ID:   ' + str(data_json['owner'])+'\n')
        print('Token:   ' + data_json['token']+'\n')
        print('Server UUID:   ' + data_json['uuid']+'\n')
        print('Server version:   ' + data_json['version']+'\n')
    else:
        print('Server ID:   ' + str(data_json['id'])+'\n')
        print('l_key:   ' + data_json['l_key']+'\n')
        print('Server name:   ' + data_json['name']+'\n')
        print('Online:   ' + str(data_json['online'])+'\n')
        print('Owner ID:   ' + str(data_json['owner'])+'\n')
        print('Server UUID:   ' + data_json['uuid']+'\n')
        print('Server version:   ' + data_json['version']+'\n')
except Exception:
    print(data)