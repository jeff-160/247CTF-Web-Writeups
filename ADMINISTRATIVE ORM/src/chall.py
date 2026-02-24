import pymysql.cursors
import pymysql, os, bcrypt, debug
from flask import Flask, request
from secret import flag, secret_key, sql_user, sql_password, sql_database, sql_host

class ORM():
    def __init__(self):
        self.connection = pymysql.connect(host=sql_host, user=sql_user, password=sql_password, db=sql_database, cursorclass=pymysql.cursors.DictCursor)

    def update(self, sql, parameters):
        with self.connection.cursor() as cursor:
          cursor.execute(sql, parameters)
          self.connection.commit()

    def query(self, sql, parameters):
        with self.connection.cursor() as cursor:
          cursor.execute(sql, parameters)
          result = cursor.fetchone()
        return result

    def get_by_name(self, user):
        return self.query('select * from users where username=%s', user)

    def get_by_reset_code(self, reset_code):
        return self.query('select * from users where reset_code=%s', reset_code)

    def set_password(self, user, password):
        password_hash = bcrypt.hashpw(password, bcrypt.gensalt())
        self.update('update users set password=%s where username=%s', (password_hash, user))

    def set_reset_code(self, user):
        self.update('update users set reset_code=uuid() where username=%s', user)

app = Flask(__name__)
app.config['DEBUG'] = False
app.config['SECRET_KEY'] = secret_key
app.config['USER'] = 'admin'

@app.route("/get_flag")
def get_flag():
    user_row = app.config['ORM'].get_by_name(app.config['USER'])
    if bcrypt.checkpw(request.args.get('password','').encode('utf8'), user_row['password'].encode('utf8')):
        return flag
    return "Invalid password for %s!" % app.config['USER']

@app.route("/update_password")
def update_password():
    user_row = app.config['ORM'].get_by_reset_code(request.args.get('reset_code',''))
    if user_row:
        app.config['ORM'].set_password(app.config['USER'], request.args.get('password','').encode('utf8'))
        return "Password reset for %s!" % app.config['USER']
    app.config['ORM'].set_reset_code(app.config['USER'])
    return "Invalid reset code for %s!" % app.config['USER']

@app.route("/statistics") # TODO: remove statistics
def statistics():
    return debug.statistics()

@app.route('/')
def source():
    return "%s" % open(__file__).read()

@app.before_first_request
def before_first():
    app.config['ORM'] = ORM()
    app.config['ORM'].set_password(app.config['USER'], os.urandom(32).hex())

@app.errorhandler(Exception)
def error(error):
    return "Something went wrong!"

if __name__ == "__main__":
    app.run()