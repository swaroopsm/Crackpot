#!/usr/bin/python

from flask import Flask, render_template, request, redirect, url_for, session
from flask.ext.pymongo import PyMongo
import settings as s, md5

import sys
sys.path.insert(0,"wrappers/")

from Users import Users as u
from Sessions import Sessions as se

app=Flask("Crackpot")

app.config['MONGO_HOST']=s.MONGO_HOST
app.config['MONGO_PORT']=s.MONGO_PORT
app.config['MONGO_USERNAME']=s.MONGO_USERNAME
app.config['MONGO_PASSWORD']=s.MONGO_PASSWORD
app.config['MONGO_DBNAME']=s.MONGO_DBNAME

mongo=PyMongo(app)

@app.route("/")
def index():
	try:
		if session['loggedin'] == True:
			return render_template("user.html", title="Crackpot", username=session['username'])
		return render_template("home.html", title="Crackpot | Welcome Crackster!")
	except KeyError:
		return render_template("home.html", title="Crackpot | Welcome Crackster!")

@app.route("/login")
def login():
	try:
		if session['loggedin'] == True:
			return redirect(url_for("index"))
		else:
			return render_template("login.html", title="Crackpot | Login")
	except KeyError:
		return render_template("login.html", title="Crackpot | Login")

@app.route("/logout")
def logout():
	try:
		if session['loggedin'] == True:
			session.pop('loggedin', None)
			session.pop('username', None)
		return redirect(url_for("index"))
	except KeyError:
		return redirect(url_for("index"))

@app.route("/signup")
def signup():
	return render_template("signup.html", title="Crackpot | New Registration")

@app.route("/session", methods=['POST','GET'])
def login_session():
	if request.method=='GET':
		return redirect(url_for('login'))
	if request.method=='POST':
		loginID=request.form['inputLoginID']
		password=request.form['inputPassword']
		a=se.login(mongo,loginID,password)
		if a['status'] == True:
			session['loggedin'] = True
			session['username'] = a['username']
			session['email_hash'] = md5.new(a['email'].lower()).hexdigest()
			return redirect(url_for("index"))
		else:
			return render_template("login.html", error="Invalid Login	")

@app.route("/new_user", methods=['POST'])
def new_user():
	name=request.form['name']
	email=request.form['email']
	password=request.form['password']
	username=request.form['username']
	a=u.new(mongo,name,email,password,username)
	return a

@app.route("/profile", methods=['GET','POST'])
def profile():
	try:
		if session['loggedin'] == True:
			return render_template("profile.html", title="Crackpot | Profile", username=session['username'])
		else:
			return redirect(url_for("index"))
	except KeyError:
		return redirect(url_for("index"))

def get_userinfo(param):
	a=u.get_userinfo(mongo,session['username'])
	if param in a:
		return a[param]
	elif param=="email_hash":
		return md5.new(a['email']).hexdigest()
	else:
		return ""

@app.route("/update_profile", methods=['POST'])
def update_profile():
	name=request.form['name']
	email=request.form['email']
	bio=request.form['bio']
	url=request.form['url']
	location=request.form['location']
	return u.update(mongo,session['username'],name,email,bio,url,location)

@app.route("/<username>")
def public_profile(username):
	a=u.view(mongo,username)
	a.update({'email_hash': md5.new(a['email']).hexdigest()})
	try:
		return render_template("public_view.html", title="Cracpot | "+a['name'], info=a)
	except:
		return render_template("public_view.html", title="Cracpot | Not Found")

if __name__=="__main__":
	app.secret_key=s.APP_SECRET_KEY
	app.jinja_env.globals.update(get_userinfo=get_userinfo)
	app.debug=True
	app.run()
