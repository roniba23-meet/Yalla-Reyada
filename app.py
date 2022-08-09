from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase
from datetime import datetime

config={
	"apiKey": "AIzaSyCo3ASIp4AAO4A6DY6gdQN2oEHXDW4tGts",
	"authDomain": "yalla-reyada2.firebaseapp.com",
	"databaseURL": "https://yalla-reyada2-default-rtdb.europe-west1.firebasedatabase.app",
	"projectId": "yalla-reyada2",
	"storageBucket": "yalla-reyada2.appspot.com",
	"messagingSenderId": "828299529495",
	"appId": "1:828299529495:web:b8ecc49cba267aeb2bfb52",
	"measurementId": "G-WJPGR7WKXM",
	"databaseURL":"https://yalla-reyada2-default-rtdb.europe-west1.firebasedatabase.app/"
}
firebase=pyrebase.initialize_app(config)
auth=firebase.auth()
db= firebase.database()
app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'
@app.route("/signup", methods=['GET', 'POST'])
def signup():
	error=""
	if (request.method=='POST'):
		email=request.form['email']
		password=request.form['password']
		kind=request.form['kind']
		login_session['user'] = auth.create_user_with_email_and_password(email, password)
		user= {"email":email, "password":password, "type":kind}
		db.child('Users').child(login_session['user']['localId']).set(user)
		try:
			
			return redirect(url_for('start'))
		except:
			error="something"
	return render_template('signup.html')

@app.route("/", methods=["GET", 'POST'])
def signin():
	error=""
	if request.method=='POST':
		print ("pppppppppppppp")
		email = request.form['email']
		password = request.form['password']
		login_session['user'] = auth.sign_in_with_email_and_password(email, password)
		try:
			return render_template('start.html')
		except:
			error = "Authentication failed"
	print("shoot")
	return render_template("signin.html")

@app.route('/start', methods=['POST', 'GET'])
def start():
	login_session['day']=[]
	print("entering start function")
	if 1==1:
		login_session['meal']=[]
		demo=[]
		login_session['meal_day']=[]
		login_session['meal_week']=[]
		login_session['day']=[]
	if request.method=='POST':
		trainee= request.form['trainee']
		title= request.form['title']
		plan_type = request.form.get('plan_type')
		return render_template(str(plan_type)+".html")
	return render_template("start.html")

@app.route('/meal', methods=['POST', 'GET'])
def meal():		
	print("enterting meal function")
	if request.method =='POST':
		item={
		"food": request.form['food'],
		"amount": request.form['amount']
		}
		print("here is the item :")
		print(item)
		print(login_session['meal'])
		login_session['meal'].append(item)
		demo.append(item)
		print(login_session['meal'])
		db.child("all_meals").push(login_session['meal'])
		return render_template('meal.html', list_food=login_session['meal'])
	return render_template('meal.html')


@app.route('/day2', methods=['POST', 'GET'])
def day2():
	if request.method=='POST':
		item={
			"food": request.form['food'],
			"amount": request.form['amount']}
		login_session['meal_day'].append(item)
		return render_template('day.html', list_day=db.child("meal").get().val())
	return render_template('day.html')

@app.route('/day1', methods=['POST', 'GET'])
def day1():

	if request.method=='POST':
		print(login_session['meal_day'])
		login_session['day'].append(login_session['meal_day'])
		db.child("all_days").push(login_session['day'])
		print(login_session['day'])
		return render_template('day.html')
	return render_template('day.html')


if __name__ == '__main__':
	app.run(debug=True)