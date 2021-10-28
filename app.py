from flask import Flask, render_template,request
import sqlite3

conn = sqlite3.connect('test.db')
cursor = conn.cursor()

create_table = "CREATE TABLE users123(id int, username text, password text);"
#cursor.execute(create_table);

user=(1,'asc','qwe')

cursor.execute("insert into users123 values(?,?,?)",user);
conn.close()

app = Flask(__name__)

@app.route("/verifylogin",methods=['POST'])
def verifylogin():
	return 'verifying login credentials'

@app.route("/")
def main():
	return render_template('index.html')



if( __name__ == "__main__"):
	app.run(debug=True)
