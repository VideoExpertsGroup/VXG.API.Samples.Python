# VXG.API.Samples.Python

Learn more about our <a href="https://www.videoexpertsgroup.com">Cloud Video Surveillance API</a>

## How to use

1) Create a channel on the Cloud
```
python .\admin_api_create_channel.py -serv_key v3.aaaaaaaaaaaaaaaa -channel_name TestTestTest
```

2) Set metadata
```
python .\admin_api_set_meta.py -serv_key v3.aaaaaaaaaaaaaaaa -id_channel 199415 -tag test -data testtesttest
```

3) Get metadata
```
python .\admin_api_get_meta.py -serv_key v3.aaaaaaaaaaaaaaaa -id_channel 199415
```

4) Get the list of events
```
python .\storage_api_get_events.py -access_token sdafasdfasdfasdfasdfasrwecsdcsdf= -start 2016-06-08T19:59:25 -end 2020-06-08T19:59:25 -limit 10
```

5) Start/Stop record:
```
python .\cameras_event_processing_events.py -access_token sdafasdfasdfasdfasdfasrwecsdcsdf= -ename motion -record_stat on
```
```
python .\cameras_event_processing_events.py -access_token sdafasdfasdfasdfasdfasrwecsdcsdf= -ename motion -record_stat off
```

6) Get records:
```
python .\storage_api_get_records.py -access_token sdafasdfasdfasdfasdfasrwecsdcsdf= -start 2016-06-08T19:59:25 -end 2020-06-08T19:59:25 -limit 10
```

7) Create a channel on the Server:
```
python .\admin_api_create_channels.py -vxg_serv_address 10.10.10.23 -vxg_serv_key srv.aaaaaaaaaaaaaaaa -url rtsp://sadasd:sdasdsd5@10.20.16.58/axis-media/media.amp -id 6
```

8) Install Cloud key on the Server:
```
python .\install_vxg_cloud_key.py -vxg_serv_address 10.10.10.23 -vxg_serv_key srv.aaaaaaaaaaaaaaaa -vxg_cloud_key v3.bbbbbbbbbbbbbbbbb
```

9) Get list of CNVR Servers on the Cloud
```
python .\admin_api_get_servers.py -cert "PATH_TO_CERT" -key "PATH_TO_KEY"
```

10) Register CNVR Server on the Cloud
```
python .\admin_api_register_server.py -cert "PATH_TO_CERT" -key "PATH_TO_KEY" -uuid AAAAAAAA-BBBB-CCCC-DDDD-EEEEEEEEEEEE -owner 12345
```

11) Unregister CNVR Server on the Cloud
```
python .\admin_api_unregister_server.py -cert "PATH_TO_CERT" -key "PATH_TO_KEY" -id 123
```

12) Get list of Server on Cloud
```
python .\servers_get_servers.py -cert "PATH_TO_CERT" -key "PATH_TO_KEY" -vxg_cloud_key v3.bbbbbbbbbbbbbbbbb
```

13) Get info of Server on Cloud
```
python .\servers_get_server_info.py -cert "PATH_TO_CERT" -key "PATH_TO_KEY" -vxg_cloud_key v3.bbbbbbbbbbbbbbbbb -id 123
```

14) Get list of cameras on Server
```
python .\admin_api_get_channels_on_server.py -serv_backchannel https://.../backchannel/... -serv_key srv.aaaaaaaaaaaaaaaa
```


## Overview
The API functions are divided in several sections. Interactive API reference (Swagger) can be found in the Docs & API section on the dashboard in corresponding API sections.

## Admin API
Add/edit/delete cameras.
Manage storage and bandwidth limits.
Retrieve usage statistics.
Store/retrieve meta information.
The API documentaion and an online testing tool can be found here: Admin API
The API authorization is described here

## Admin Server API
Add/delete servers.
Retrieve server list with server info.

## Server API
Retrieve server list with server info.
Retrieve server info for a specific server.

## Channel API
Get live video URLs.
Get recorded video.
Get stored images and clips.
Store new images and clips.
Get recoreded video timeline.
Communication channel (Websocket) for cloud cameras.
The API documentaion and an online testing tool can be found here: Channel API
The API authorization is described here

## Artificial Intelligence (AI) API
Generate images from recorded video.
Generate images from live video.
Create clips.
Get live video.
Get recorded video.
The API documentaion and an online testing tool can be found here: Channel API
The API authorization is described here

## Camera Settings API
Video settings: bitrate, framerate, resolution, etc.
Audio settings.
PTZ.
Apparance.
Motion and audio detectors.
System settings.
The API documentaion and an online testing tool can be found here: Channel API
The API authorization is described here

## Events and Notification API
Put/Get metadata and events.
Send notifications.
The API documentaion and an online testing tool can be found here: Channel API
The API authorization is described here

## Admin API authorization
To authorize your requests to Admin API you need to use your license key that you can find in the VXG dashboard: https://dashboard.videoexpertsgroup.com/?products=

The API Key should be injected to Authorization header of every request to Admin API like this:

Authorization: LKey %license_key%
For example, if the API key is "X9tKpuXq0btatj":

Authorization: LKey X9tKpuXq0btatj
Non-admin API authorization
All function calls require an authorization header.

'Authorization: Acc %channel_access_token%'
The %channel_access_token% can be retrieved in two ways:
a. Using Admin API during creating a channel or updating of a channel access token.
b. Using Cloud/Server Admin UI page.

Example of an authorization header:

'Authorization: Acc eyJhY2Nlc3MiOiAid2F0Y2giLCAidG9rZW4iOiAic2hhcmUuZXlKemFTSTZJRE14T0RoOS41YWEyMjA2N3QxMmNmZjc4MC5GVHpEeUZMYkVLQVNzM2ZJRFZaSDdFMEhhdGMiLCAiY2FtaWQiOiAxMzI0NDUsICJjbW5ncmlkIjogMTMyODUwLCAiYXBpIjogIndlYi5za3l2ci52aWRlb2V4cGVydHNncm91cC5jb20ifQ=='

Learn more about <a href="https://www.videoexpertsgroup.com">Cloud Video Surveillance</a>


