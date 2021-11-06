from flask import Flask, render_template,request
from flask_mysqldb import MySQL 
from flask import jsonify
import random
import string
import json
import time

startTime = int(time.time()) 
phaseTime = 30

app = Flask(__name__)

app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Sahutronics@123'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_DB'] = 'ssdproject'
mysql = MySQL(app)



#================Admin Part=======================================
@app.route('/admin', methods=['GET'])
def admin():
    
    return render_template('admin.html')


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


@app.route('/people', methods=['post'])
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


#=================================================================




@app.route("/updatePhase",methods=['GET'])
def updatephase():
	phase = request.args.get('curphase')
	
	#will fetch this time from DB which contains end time
	global startTime

	currTime = int(time.time()) 
	if(phase == 'EMP'):
		
		print(startTime,phaseTime,currTime,)
		if(startTime+phaseTime < currTime ):
			return "true"
		else:
			return "false"

	if(phase == 'DEF'):
		
		print(startTime,phaseTime,currTime,)
		if(startTime+phaseTime*2 < currTime ):
			return "true"
		else:
			return "false"


	if(phase == 'IDE'):
		
		print(startTime,phaseTime,currTime,)
		if(startTime+phaseTime*3 < currTime ):
			return "true"
		else:
			return "false"

	if(phase == 'PRO'):
		
		print(startTime,phaseTime,currTime,)
		if(startTime+phaseTime*4 < currTime ):
			return "true"
		else:
			return "false"



@app.route("/addMessage",methods=['GET'])
def addMessage():
	cur = mysql.connection.cursor()
	msg = request.args.get('msg')
	userid = request.args.get('userid')
	wid = request.args.get('wid')
	grpid = request.args.get('grpid')
	query="insert into chat(workshopid,groupid,userid,text) values(%s,%s,%s,%s)"
	
	record = [wid,grpid,userid,msg]
	cur.execute(query, record)
	mysql.connection.commit()
	cur.close()
	return 'Added Successfully'

@app.route("/getmsg")
def getmsg():
	cur = mysql.connection.cursor()
	query1="select * from chat order by messageid;"
	cur.execute(query1)
	results = cur.fetchall()
	
	payload = []
	content = {}
	for result in results:
		content = {'uid': result[2], 'text': result[4]}
		payload.append(content)
		content = {}
    

	#print(payload);
	cur.close()
	return jsonify(payload)



@app.route("/verifylogin",methods=['POST'])
def verifylogin():
	return 'verifying login credentials'

@app.route("/")
def main():
	return render_template('index.html')



# functonalities of all participants
@app.route("/emphasize")
def participants():
	global startTime
	startTime = int(time.time()) 
	return render_template('emphasize.html')
	
@app.route("/proto")
def prototype():
	return render_template('prototype.html')


@app.route("/chat")
def chatbox():
	return render_template('chatbox.html')

@app.route("/define")
def define():
	return render_template('define.html')

@app.route("/ideate")
def ideate():
	return render_template('ideate.html')


if( __name__ == "__main__"):
	app.run(debug=True)
	
	startTime = int(time.time()) 

	
	phaseTime = 2
	print(startTime)
