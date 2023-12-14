import argparse
import requests
import sys
import json

# Replace with your own cloud VMS API endpoint
api_endpoint = 'web.vxgdemo.vxgdemo.cloud-vms.com'

'''
List channels for a License Key
Create group channel
Add channels to a group
Retrieve channels from a group
Retrieve Live URLs for all channels in a group
Record metadata to a channel
'''
def build_url(endpoint, path, param=None):
    if param:
        return f'https://{endpoint}:443/{path}/{param}'
    else:
        return f'https://{endpoint}:443/{path}'

def list_channels_for_lkey(lkey):
    # HTTP header. Indicates the MIME document type (json) as well as the authorization key
    headers = {
    'accept': 'application/json',
    'Authorization': 'LKey ' + lkey,
    }
    path = 'api/v3/channels'
    address = build_url(api_endpoint, path)
    # Exceptions block.
    try:
        response = requests.get(address, headers=headers, timeout=15)
    except requests.exceptions.RequestException as e:
        print (e)
        sys.exit(1)

    code, data = response.status_code, response.text

    # Status of the HTTP request
    print ('Request completed. HTTP status code: ' + str(code)+'\n')

    # Convertion to json
    try:
        data_json = json.loads(data)
    except Exception:
        pass

    try:
        for channel in data_json['objects']:
            print(f'Channel ID: {channel["id"]}')
            print(f'   created: {channel["created"]}')
            print(f'   name: {channel["name"]}')
            print(f'   recording mode: {channel["rec_mode"]}')
            print(f'   created: {channel["created"]}')
            print(f'   storage direct recording: {channel["storage_direct_recording"]}')
            print(f'   streaming: {channel["streaming"]}')
            print(f'   timezone: {channel["timezone"]}')
            print(f'   source url: {channel["source"]["url"]}')
            print(f'   access tokens:')
            print(f'        all: {channel["access_tokens"]["all"]}')
            print(f'        watch: {channel["access_tokens"]["watch"]}\n')
            input('Press any key to continue...\n')
    except Exception:
        print (data)
        input('Press any key to continue...\n')


def create_group_channel(lkey, name):
    # HTTP header. Indicates the MIME document type (json) as well as the authorization key
    headers = {
        'accept': 'application/json',
        'Authorization': 'LKey ' + lkey,
    }
    path = 'api/v3/channel_groups'
    data = {'name': name}
    address = f'https://{api_endpoint}/api/v3/channel_groups/'
    # Exclusion block. If a request error occurs during the sending of the request (for example, the server is not available), the program displays the error status and terminates the execution.
    try:
        response = requests.post(address, headers=headers, json=data)
        # print (response.text)
    except requests.exceptions.RequestException as e:
        print (e)
        sys.exit(1)

    code, data = response.status_code, response.text

    # if code == 201:
    print('Channel group successfully added.')
    # Convertion to json
    try:
        data_json = json.loads(data)
    except Exception:
        pass
    try:
        print(f'Group channel ID: {data_json["id"]}')
        print(f'   name: {data_json["name"]}')
        print(f'   token: {data_json["token"]}')
    except Exception:
        print('Exception')
        print (data)

    input('Press any key to continue...\n')


def add_channel_to_group(lkey, group_id, channel_id):
    # get channels from v5 channels list
    # HTTP header. Indicates the MIME document type (json) as well as the authorization key
    headers = {
    'accept': 'application/json',
    'Authorization': 'LKey ' + lkey,
    }

    # api/v3/channel_groups/
    address = f'https://{api_endpoint}/api/v3/channel_groups/{group_id}/'

    # Exceptions block.
    try:
        response = requests.get(address, headers=headers, timeout=15)
    except requests.exceptions.RequestException as e:
        print (e)
        sys.exit(1)

    code, data = response.status_code, response.text

    if code != 200:
        print(f'Response code: {code}\nResponse message: {data}')
        input('Press any key to continue...\n')
        return
    
    # use json_data['object'] and build list of channel ids
    try:
        data_json = json.loads(data)
    except Exception:
        pass

    if len(data_json['channels']) == 0:
        print('No channels associated with this group token.')
        input('Press any key to continue...\n')
        return

    channel_ids = []
    
    for channel in data_json["channels"]:
        channel_ids.append(channel)

    if channel_id in channel_ids:
        print('Channel ID is already added to group channel.')
        input('Press any key to continue...\n')
        return
    else:
        channel_ids.append(channel_id)

    # use PUT v3 channel_groups/grpid/ and set data to {"channels": [list of channel ids]}
    headers = {
        'accept': 'application/json',
        'Authorization': 'LKey ' + lkey,
    }
    data = {"channels": channel_ids}
    address = f'https://{api_endpoint}/api/v3/channel_groups/{group_id}/'
    # Exclusion block. If a request error occurs during the sending of the request (for example, the server is not available), the program displays the error status and terminates the execution.
    try:
        response = requests.put(address, headers=headers, json=data)
        # print (response.text)
    except requests.exceptions.RequestException as e:
        print (e)
        sys.exit(1)

    code, data = response.status_code, response.text

    if code == 200:
        print(f'Channel {channel_id} was added to group channel {group_id}.')
    else:
        print(f'Response code: {code}\nResponse message: {data}')

    input('Press any key to continue...\n')


def get_channels_from_group(group_token):
    # HTTP header. Indicates the MIME document type (json) as well as the authorization key
    headers = {
    'accept': 'application/json',
    'Authorization': 'SI ' + group_token,
    }

    address = f'https://{api_endpoint}/api/v5/channels/'

    # Exceptions block.
    try:
        response = requests.get(address, headers=headers, timeout=15)
    except requests.exceptions.RequestException as e:
        print (e)
        sys.exit(1)

    code, data = response.status_code, response.text

    # Status of the HTTP request
    print ('Request completed. HTTP status code: ' + str(code)+'\n')

    # Convertion to json
    try:
        data_json = json.loads(data)
    except Exception:
        pass

    if data_json['meta']["total_count"] == 0:
        print('No channels associated with this group token.')
        input('Press any key to continue...\n')
        return
    
    try:
        for channel in data_json['objects']:
            print(f'Channel ID: {channel["id"]}')
            print(f'   name: {channel["name"]}')
            print(f'   recording: {channel["recording"]}')
            print(f'   status: {channel["status"]}')
            print(f'   token: {channel["token"]}')
            input('Press any key to continue...\n')
    except Exception:
        print (data)
        input('Press any key to continue...\n')

def get_live_urls_for_channels_in_group(group_token):
    # get channel ids
    # get channels from v5 channels list
    # HTTP header. Indicates the MIME document type (json) as well as the authorization key
    headers = {
    'accept': 'application/json',
    'Authorization': 'SI ' + group_token,
    }

    # api/v3/channel_groups/
    address = f'https://{api_endpoint}/api/v5/channels/'

    # Exceptions block.
    try:
        response = requests.get(address, headers=headers, timeout=15)
    except requests.exceptions.RequestException as e:
        print (e)
        sys.exit(1)

    code, data = response.status_code, response.text

    if code != 200:
        print(f'Response code: {code}\nResponse message: {data}')
        input('Press any key to continue...\n')
        return
    
    # use json_data['object'] and build list of channel ids
    try:
        data_json = json.loads(data)
    except Exception:
        pass

    if data_json['meta']["total_count"] == 0:
        print('No channels associated with this group token.')
        input('Press any key to continue...\n')
        return

    channel_info = []
    
    for channel in data_json['objects']:
        channel_info.append((channel["id"], channel["token"]))

    # use v4/live/source and if online return rtmp for each channel
    for channel in channel_info:
        # channel[0] is channel id
        # channel[1] is channel token
        headers = {
        'accept': 'application/json',
        'Authorization': 'Acc ' + channel[1],
        }

        # api/v3/channel_groups/
        address = f'https://{api_endpoint}/api/v4/live/watch/'

        # Exceptions block.
        try:
            response = requests.get(address, headers=headers, timeout=15)
        except requests.exceptions.RequestException as e:
            print (e)
            sys.exit(1)

        code, data = response.status_code, response.text

        # Convertion to json
        try:
            data_json = json.loads(data)
        except Exception:
            pass

        print(f'Channel ID: {channel[0]}\nLive URL: {data_json["rtmp"]}')
        input('Press any key to continue...\n')
        

    input('Press any key to continue...\n')

def record_metadata_to_channel(token, meta):
    input('Press any key to continue...\n')

def main():
    print(f'AI Intergation Menu')

    # print options
    c = 1

    while c != 0:
        print('1. List channels for a License Key')
        print('2. Create group channel')
        print('3. Add channels to a group')
        print('4. List channels in a group')
        print('5. Retrieve Live URLs for a group')
        print('6. Record metadata to a channel')
        print('0. Exit')
        try:
            c = int(input("Choose: "))
        except ValueError:
            raise ValueError('Choice must be integer')
        match c:
            case 1:
                print('Listing channels for license key.')
                lkey = input('Enter LKey: ')
                list_channels_for_lkey(lkey)
            case 2:
                print('Creating group channel.')
                lkey = input('Enter LKey: ')
                name = input('Enter group channel name: ')
                create_group_channel(lkey, name)
            case 3:
                print('Adding channel to group.')
                lkey = input('Enter LKey: ')
                ch_id = int(input('Enter channel id: '))
                gr_id = int(input('Enter group channel id: '))
                add_channel_to_group(lkey, channel_id=ch_id, group_id=gr_id)
            case 4:
                print('Retrieving channels in a group.')
                group_token = input('Enter group access token: ')
                get_channels_from_group(group_token)
            case 5:
                print('Retrieving live URLs for a group.')
                group_token = input('Enter goup access token: ')
                get_live_urls_for_channels_in_group(group_token)
            case 6:
                print('Recording metadata to a channel')
                ch_token = input('Enter channel access token: ')
                meta = input('Enter metadata: ')
                record_metadata_to_channel(ch_token, meta)
            case 0:
                print(f'Goodbye!')
            case _:
                print('Invalid option.')

if __name__ == "__main__":
    main()