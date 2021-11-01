from flask import Flask, render_template,request
from flask_mysqldb import MySQL 
from flask import jsonify
import random
import string
import json


app = Flask(__name__)

app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Sahutronics@123'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_DB'] = 'ssdproject'


mysql = MySQL(app)



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

@app.route("/verifylogin",methods=['POST'])
def verifylogin():
	return 'verifying login credentials'

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


@app.route("/chatbot")
def chatbot():
	
	#print(results);
	
	return render_template('chatbot.html')




@app.route("/")
def main():
	return render_template('index.html')



if( __name__ == "__main__"):
	app.run(debug=True)
