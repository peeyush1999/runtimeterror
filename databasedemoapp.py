from flask import Flask, render_template, request, redirect,jsonify
from flask_mysqldb import MySQL
import yaml
app = Flask(__name__)

# Configure db
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
mysql = MySQL(app)

@app.route('/')
def users():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def userdetails():
    username = request.form.get('Email')
    conn = mysql.connection
    cur = conn.cursor()
    userid = cur.execute("SELECT user.userid,user.name  FROM user where user.username = %s",[username])
    userDetails = cur.fetchall()
    cur.execute("INSERT INTO `registration` (`workshopid`, `userid`) VALUES (%s , %s)",[0 , userDetails[0][0]])
    cur.close()
    conn.commit()
    return render_template('databaseconnectiondemo.html')


@app.route('/verifylogin', methods=['post'])
def userdeets():
    conn = mysql.connection
    cur = conn.cursor()
    d={}
    count = cur.execute("SELECT user.name FROM user where user.type = 'participant' AND user.userid IN (SELECT reg.userid FROM registration reg)")
    print(count)
    if(count > 0):
        userDetails = cur.fetchall()
        print(userDetails)
        cur.close()
        conn.commit()
        d = {}
        i=0
        for x in userDetails:
            d[i] = x[0]
            i = i+1
    return jsonify(d)

if __name__ == '__main__':
    app.run(threaded=True,debug=True)
