import argparse
import requests
import sys
import json

def admin_api_register_server(cert, key, id):
    session = requests.Session()
    session.cert = (cert, key)

    # API request
    api_url = 'https://web.skyvr.videoexpertsgroup.com:9000/api/v6/admin/servers/' + id + '/'
    try:
        response = session.delete(url=api_url, verify=False)
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)

    session.close()
    return response.status_code, response.text


# Parsing program call arguments
parser = argparse.ArgumentParser()
parser.add_argument('-cert', '--path_to_cert', help = 'Path to .crt file', required=True)
parser.add_argument('-key', '--path_to_key',  help = 'Path to .key file', required=True)
parser.add_argument('-id', '--server_id',  help = 'ID of server to unregister', required=True)
# Block responsible for checking the entered parameters. In case of an error, the status and description of use are returned
try:
    param = parser.parse_args()
except IOError as msg:
    parser.error(str(msg))


# Function call to send an HTTP request
code, data = admin_api_register_server(param.path_to_cert, param.path_to_key, param.server_id)


# Convertion to json
try:
    data_json = json.loads(data)
except Exception:
    pass


# Output of the status.
print('Request completed. HTTP status code: ' + str(code)+'\n')

# Output if unregistration was successful
if code == 204:
    print('Server was unregistered successfully.\n')
else:
    print('Server was NOT unregistered.\n')
