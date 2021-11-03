from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
import yaml
# import json
# import jyserver.Flask as jsf

app = Flask(__name__)
# Configure db
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

import json
mysql = MySQL(app)
# tablex = []
# @jsf.use(app)
# class App:
#     def __init__(self):
#         self.count=0


#     def createTeams(self):
#         print("in teams")
#         useDetails = []
#         x= 0
#         cur = mysql.connection.cursor()
#         resultValue = cur.execute("SELECT * FROM user")
#         print(cur)
#         if resultValue > 0:
#             userDetails = list(cur.fetchall())
#             print(userDetails)
#             ul = self.js.document.getElementById("list")
#             li = self.js.document.createElement("li")
#             print(li)
#             # li.setAttribute('id',userDetails[0][0])
#             # s = self.js.document.createTextNode(userDetails[0][0])
#             # print(s)
#             # jsonstr1 = json.dumps(s.__dict__)
#             # print(jsonstr1)
#             # s = json.dumps(self.js.document.createTextNode(userDetails[0][0]).__dict__)
#             # print(s)
#             # li.appendChild(str(self.js.document.createTextNode(userDetails[0][0])))
#             # ul.appendChild(str(li))
#             # li = self.js.document.createElement("li")
#             # li.appendChild(str(self.js.document.createTextNode(userDetails[0][1])))
#             # ul.appendChild(str(li))
#             # self.js.document.getElementById("count").innerHTML = userDetails[0][1]
#             # print(x)
#         cur.close()
#     # def increment(self):
#     #     self.count += 1
#     #     self.js.document.getElementById("count").innerHTML = self.count
@app.route('/')
def users():
    return render_template('team.html')


@app.route('/create', methods=["POST"])
def createTeams():
    print("Function called")
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM user")
    if resultValue > 0:
        print(resultValue)
        l = {}
        userDetails = cur.fetchall()
        cur.close()
        i = 0
        for p in userDetails:
           l[i] = p[2]
           i = i+1
        print(type(json.dumps(l)))
        return json.dumps(l)


if __name__ == '__main__':
    app.run(debug=True)