from flask_mysqldb import MySQL 

app = Flask(__name__)

app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Sahutronics@123'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_DB'] = 'ssdproject'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)
cur = mysql.connection.cursor()


@app.route("/verifylogin",methods=['POST'])
def verifylogin():
	return 'verifying login credentials'

@app.route("/")
def main():

	query="insert into chat values(1,1,2)"

	query1="select * from chat;"
	cur.execute(query1)
	results = cur.fetchall()
	return render_template('index.html')



if( __name__ == "__main__"):
	app.run(debug=True)
