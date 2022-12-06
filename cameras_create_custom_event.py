"""Test for resize images from VXG Server use opencv."""
import io
import os
import sys
import requests
import subprocess
import base64
import json
import shlex
import argparse
from datetime import datetime, timedelta

def create_custom_event(token: str, cam_id: int, custom_event_name: str):
    """Get image URL from VXG Cloud."""
    try:
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Acc %s' % token,
        }
          
        url = "https://web.skyvr.videoexpertsgroup.com/api/v2/cameras/%d/event_processing/events/"%(cam_id)

        data = "{ \"name\": \"%s\", \"notify\": true}"%(custom_event_name);

        print("---\ndata: %s\n---"%(data))  

        resp = requests.post(url=url, headers=headers, data = data, timeout=10).json()
        print(resp)
        return resp.get('urls', [])

    except Exception as e:
        print(e) 
        return []



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--token', help='Access token', required=True)
    parser.add_argument('-e', '--event_name', help='Custom event name', default='motion_detection')

    param = parser.parse_args()

    token_json=''
    try:
       token = base64.b64decode(param.token)
       token_json = json.loads(token) 
    except Exception:
       print("Invalid access token") 
       sys.exit(1)

    cam_id = token_json["camid"]
 
    create_custom_event(param.token, cam_id, param.event_name)

    
if __name__ == '__main__':
    main()