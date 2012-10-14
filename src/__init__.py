#!/usr/bin/python

from flask import Flask, render_template, request, redirect, url_for, session
from flask.ext.pymongo import PyMongo
import settings as s

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
	return render_template("home.html", title="Crackpot | Welcome Crackster!")

@app.route("/login")
def login():
	return render_template("login.html", title="Cracpot | Login")

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
			return render_template("login.html", title="Crackpot | "+a['username'])
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
	
if __name__=="__main__":
	app.secret_key=s.APP_SECRET_KEY
	app.debug=True
	app.run()
