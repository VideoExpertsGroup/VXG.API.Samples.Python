import argparse
import requests
import sys
import json

# Function for executing HTTP request (install key)
def install_key(vxg_address, vxg_serv_key, vxg_cloud_key):
    # HTTP header. Indicates the MIME document type (json) as well as the authorization key
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'LKey %s' % str(vxg_serv_key),
        }
    data = '{ "name": "VXG Cloud", "access_key": "%s", "api_uri": "https://web.skyvr.videoexpertsgroup.com/", "cm_uri": "wss://cam.skyvr.videoexpertsgroup.com:8883/"}' % str(vxg_cloud_key) #Key registration data
    
    address = 'http://'+str(vxg_address)+':83/api/v3/server/relays/' # Server address
    # Exclusion block. If a request error occurs during the sending of the request (for example, the server is not available), the program displays the error status and terminates the execution.
    try:
        response = requests.post(address, headers=headers, data=data, timeout=15)
    except requests.exceptions.RequestException as e:
        print (e)
        sys.exit(1)
    return response.status_code, response.text # The function returns the status of the HTTP request sending code, as well as the received data


# Function for executing HTTP request (check keys)
def get_list_id(vxg_address, vxg_serv_key, vxg_cloud_key):
    # HTTP header. Indicates the MIME document type (json) as well as the authorization key
    headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': 'LKey %s' % str(vxg_serv_key),
    }
    address = 'http://'+str(vxg_address)+':83/api/v3/server/relays/?name=VXG%20Cloud' # Server address
    # Exclusion block. If a request error occurs during the sending of the request (for example, the server is not available), the program displays the error status and terminates the execution.
    try:
        response = requests.get(address, headers=headers, timeout=15)
    except requests.exceptions.RequestException as e:
        print (e)
        sys.exit(1)
    return response.status_code, response.text # The function returns the status of the HTTP request sending code, as well as the received data

# Parsing program call arguments
parser = argparse.ArgumentParser()
parser.add_argument('-vxg_serv_address', '--vxg_serv_address', help = 'VXG Server address', required=True)
parser.add_argument('-vxg_serv_key', '--vxg_serv_key', help = 'VXG Server key', required=True)
parser.add_argument('-vxg_cloud_key', '--vxg_cloud_key',  help = "VXG Cloud key", required=True)

# Block responsible for checking the entered parameters. In case of an error, the status and description of use are returned
try:
    param = parser.parse_args()
except IOError as msg:
    parser.error(str(msg))


status_code, response = get_list_id(param.vxg_serv_address, param.vxg_serv_key, param.vxg_cloud_key) # Function call to send an HTTP request

key_status=False
a=''
# Block for checking the existence of id or key registration
if status_code==200:     #Success Check
    try:
        a = json.loads(response) #Response parsing
    except Exception as e:    #Server returned erroneous data
        print(e)      
        sys.exit(1)
    if a['objects']==[]:     #Checking for the existence of any id
        status_code, response = install_key(param.vxg_serv_address, param.vxg_serv_key, param.vxg_cloud_key) # Function call to send an HTTP request
        if status_code == 201:
            a = json.loads(response)
            print(str(a['name']) + " : id = " + str(a["id"]))
        else:
            print ('Request failed. HTTP status code: ' + str(status_code)+'\n')
    else:
        for i in a['objects']:         #Checking the existence of id on a given key
            if i["access_key"] == str(param.vxg_cloud_key):
                print(str(i['name']) + " : id = " + str(i["id"]))
                key_status=True
        if key_status==False:   #If id with such a key does not exist, set the key 
            status_code, response = install_key(param.vxg_serv_address, param.vxg_serv_key, param.vxg_cloud_key) # Function call to send an HTTP request
            if status_code == 201:
                try:
                    a = json.loads(response)
                    print(str(a['name']) + " : id = " + str(a["id"]))
                except Exception as e:   #Server returned erroneous data
                    print(e)
                    sys.exit(1)
            else:
                print ('Request failed. HTTP status code: ' + str(status_code)+'\n')
else:
    print ('Request failed. HTTP status code: ' + str(status_code)+'\n')