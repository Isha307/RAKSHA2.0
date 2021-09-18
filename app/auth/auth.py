# user authentication (login and sign up)

import pyrebase
import firebase_admin
from flask import *
#auth used for r/w e.g. creating users
from firebase_admin import credentials, auth

# Define the blueprint: 'auth', set its url prefix: auth.url/auth
auth = Blueprint('auth', __name__)

cred = credentials.Certificate('fbAdminConfig.json')
firebase = firebase_admin.initialize_auth(cred)
#used for read-only i.e. signing in
pb = pyrebase.initialize_auth(json.load(open('fbconfig.json')))

@auth.route('/signin', methods=['GET', 'POST'])
def signin():
	unsuccessful = 'Please check your credentials'
	successful = 'Login successful'
	if request.method == 'POST':
		email = request.form['name']
		password = request.form['pass']
		try:
			userRef = pb.auth().sign_in_with_email_and_password(email, password)
			return redirect(url_for('dashboard',user=userRef))
		except Exception as ex:
			print(ex)
			return render_template('auth/signin.html', us=unsuccessful)

	return render_template('auth/signin.html')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
	unsuccessful = 'Please enter a valid email and password'
	successful = 'Signup successful'
	if request.method == 'POST':
		email = request.form['name']
		password = request.form['pass']
		try:
			auth.create_user(email=email, password=password)
			return render_template('auth/signup.html', s=successful)
		except Exception as ex:
			print(ex)
			return render_template('auth/signup.html', us=unsuccessful)

	return render_template('auth/signup.html')

@auth.route('/dashboard/<user>', methods=['GET', 'POST'])
def dashboard(user):
	#for refresh button
	if request.method == 'POST':
		pass
	#get user information
	name = user.identifier
	#pass in relevant info to load custom dashboard
	return render_template('user/dashboard.html', name=name)
