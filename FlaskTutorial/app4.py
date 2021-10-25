from flask import Flask, render_template,request

app = Flask(__name__) 

@app.route("/",methods=['POST','GET'])
def main():
	data={}
	if request.method=='POST':
		
		data['name'] = request.form['name']
		data['pass'] = request.form['pass']
		

	return render_template('index4.html', data=data, data2=data)






if( __name__ == "__main__"):
	app.run(debug=True)