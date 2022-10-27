import argparse
import requests
import sys
import json

def admin_api_register_server(cert, key, l_key):
    session = requests.Session()
    session.cert = (cert, key)

    # API request
    api_url = 'https://web.skyvr.videoexpertsgroup.com:9000/api/v6/servers/'
    headers = {'Authorization': l_key}
    try:
        response = session.get(url=api_url, headers=headers, verify=False)
    except requests.exceptions.RequestException as e:
        print (e)
        sys.exit(1)

    session.close()
    return response.status_code, response.text


# Parsing program call arguments
parser = argparse.ArgumentParser()
parser.add_argument('-cert', '--path_to_cert', help = 'Path to .crt file', required=True)
parser.add_argument('-key', '--path_to_key',  help = 'Path to .key file', required=True)
parser.add_argument('-l', '--l_key',  help = 'Cloud relay key applied in server settings', required=True)
#parser.add_argument('-id', '--server_id',  help = 'Server ID number', required=True)
# Block responsible for checking the entered parameters. In case of an error, the status and description of use are returned
try:
    param = parser.parse_args()
except IOError as msg:
    parser.error(str(msg))


# Function call to send an HTTP request
code, data = admin_api_register_server(param.path_to_cert, param.path_to_key, param.l_key)
#code, data = admin_api_register_server(param.path_to_cert, param.path_to_key, param.l_key, param.server_id)



# Convertion to json
try:
    data_json = json.loads(data)
except Exception:
    pass


# Output of the status.
print ('Request completed. HTTP status code: ' + str(code)+'\n')

# Output of the HTTP request (acess token, id)
try:
    print('Meta:')
    print('   limit:   ' + str(data_json['meta']['limit'])+'\n')
    print('   next:   ' + str(data_json['meta']['next'])+'\n')
    print('   offset:   ' + str(data_json['meta']['offset'])+'\n')
    print('   previous:   ' + str(data_json['meta']['previous'])+'\n')
    print('   number of servers:   ' + str(data_json['meta']['total_count'])+'\n')
    print('Servers:')
    for server in data_json['objects']:
        if server['online']:
            print('   API Endpoint:   ' + server['api_endpoint']+'\n')
            print('   Endpoint:   ' + server['endpoint']+'\n')
            print('   Expired:   ' + server['expires']+'\n')
            print('   Server ID:   ' + str(server['id'])+'\n')
            print('   l_key:   ' + server['l_key']+'\n')
            print('   Server name:   ' + server['name']+'\n')
            print('   Online:   ' + str(server['online'])+'\n')
            print('   Token:   ' + server['token']+'\n')
            print('   Server UUID:   ' + server['uuid']+'\n')
            print('   Server version:   ' + server['version']+'\n')
        else:
            print('   Server ID:   ' + str(server['id'])+'\n')
            print('   l_key:   ' + server['l_key']+'\n')
            print('   Server name:   ' + server['name']+'\n')
            print('   Online:   ' + str(server['online'])+'\n')
            print('   Server UUID:   ' + server['uuid']+'\n')
            print('   Server version:   ' + server['version']+'\n')
            print('   ------------------------------------------')
except Exception:
    print (data)