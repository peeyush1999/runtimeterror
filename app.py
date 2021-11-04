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
