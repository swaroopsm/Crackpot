#!/usr/bin/python

from flask import Flask, render_template, request, redirect, url_for
from flask.ext.pymongo import PyMongo
import settings as s

import sys
sys.path.insert(0,"wrappers/")

from Users import Users as u

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
def session():
	if request.method=='GET':
		return redirect(url_for('login'))
	return render_template("login.html", title="Cracpot | Login", error="Invalid...")

@app.route("/new_user", methods=['POST'])
def new_user():
	name=request.form['name']
	email=request.form['email']
	password=request.form['password']
	username=request.form['username']
	a=u.new(mongo,name,email,password,username)
	return a
	
if __name__=="__main__":
	app.debug=True
	app.run()