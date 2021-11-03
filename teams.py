from flask import Flask, render_template, request, redirect, jsonify
from flask_mysqldb import MySQL
import yaml, json
import random
from random import randrange

app = Flask(__name__)
# Configure db
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def users():
    return render_template('teams.html')


def arrangeRandom(userIds, count):
    r = random.sample(range(len(userIds)), len(userIds))
    print(r)
    users = []
    for i in userIds:
        users.append(i[0])
    i = 0
    c = 0
    d = {}
    v = []
    j = 0
    for id in range(len(users) + 1):
        if (j == len(users)):
            d[i] = v
            break
        if (c == count):
            d[i] = v
            i = i + 1
            c = 0
            v = []
        v.append(users[r[j]])
        c = c + 1
        j = j + 1
    print(d)
    return d


@app.route('/create', methods=["POST"])
def createTeams():
    conn = mysql.connection
    cur = conn.cursor()
    resultValue = cur.execute("SELECT * FROM user")
    userDetails = cur.fetchall()
    resultValu = cur.execute(
        "SELECT reg.userid FROM registration reg WHERE reg.userid IN (SELECT user.userid FROM user WHERE type = 'participant')"
    )
    if resultValue > 0:
        l = {}
        userIds = cur.fetchall()
        d = arrangeRandom(userIds, 2)
        print(userIds)
        # for i in d.keys():
        #     id = i
        #     for j in d[i]:
        #         cur.execute("INSERT INTO `group` (`workshopid`, `userid`, `groupid`) VALUES (%s, %s, %s)",(1,j,id))
        #         conn.commit()
        u = {}
        k = 0
        for x in d.keys():
            u[x] = []
            for y in d[x]:
                res = cur.execute(
                    "SELECT user.name FROM user WHERE user.userid = %s", [y])
                if (res > 0):
                    val = cur.fetchall()
                    u[x].append(val)
        cur.close()
        conn.commit()
        return jsonify(u)


if __name__ == '__main__':
    app.run(debug=True)