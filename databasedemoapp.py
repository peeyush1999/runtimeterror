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
    
    return render_template('databaseconnectiondemo.html')
@app.route('/verifylogin', methods=['post'])
def userdeets():
    #message = ''
    cur = mysql.connection.cursor()
    username = request.form.get('Email') 
    print(type(username))
    #userid=[]
    userid = cur.execute("SELECT user.userid,user.name  FROM user where user.username = %s",[username])
    print(userid)
    userDetails = cur.fetchall()
    print(userDetails)
    # print(name)
    # print(type(userid))
    # print(type(name))
    i=1
    j=int(userDetails[0][0])
    cur.execute("INSERT INTO `registration` (`workshopid`, `userid`) VALUES (%s , %s)",[i , j])
    #mysql.commit()
    cur.close()
    d={0:userDetails[0][1]}
    return jsonify(d)

if __name__ == '__main__':
    app.run(debug=True)
