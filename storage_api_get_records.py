import argparse
import requests
import sys
import json
import base64

# Function performs HTTP request
def storage_api_get_records(token, start, end, limit):
    # HTTP header with MIME type (json)
    headers = {
    'accept': 'application/json',
    }

    # Parameters of HTTP header
    params = (
    ('limit', limit),
    ('start', start),
    ('end', end),
    ('token', token),
    )

    # Exception block. 
    try:
        response = requests.get('https://web.skyvr.videoexpertsgroup.com:443/api/v4/storage/records/', headers=headers, params=params, timeout=15) 
    except requests.exceptions.RequestException as e:
        print (e)
        sys.exit(1)
    return response.status_code, response.text    # Returns status of HTTP request

# Парсинг аргументов вызова программы
parser = argparse.ArgumentParser()
parser.add_argument('-access_token', '--access_token', help = 'Access token', required=True)
parser.add_argument('-start', '--start',  help = 'Start time', required=True)
parser.add_argument('-end', '--end',  help = 'End time', required=True)
parser.add_argument('-limit', '--limit',  help = 'Limit', required=True)

# Блок отвечающий за проверку введенных параметров. В случае ошибки возвращается статус и описание использования
try:
    param = parser.parse_args()
except IOError as msg:
    parser.error(str(msg))

# Парсинг access token для получения token. В случае ошибки программа завершается
token_json=''
try:
    token = base64.b64decode(param.access_token) # Decode access token
    token_json = json.loads(token)
except Exception:
    print("Error access token") 
    sys.exit(1)

# Вызов функции, для отправки HTTP запроса
code, data = storage_api_get_records(token_json["token"], str(param.start), str(param.end), str(param.limit))


# Вывод статуса HTTP запроса.
print ('Request completed. HTTP status code: ' + str(code)+'\n')

# Вывод списка евентов.
try:
    data_json = json.loads(data)
except Exception:
    pass

print ("Events:")
try:
    for obj in data_json["objects"]:
        print obj
except Exception:
    print ("-------------")
