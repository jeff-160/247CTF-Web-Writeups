import requests
import re

url = "https://f959c2eb748a8cec.247ctf.com/"

res = requests.get(url, params={
    'password': 1441592755
})

flag = re.findall(r'(247CTF{.+})', res.text)[0]
print("Flag:", flag)