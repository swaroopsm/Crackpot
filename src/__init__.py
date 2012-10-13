#!/usr/bin/python

from flask import Flask, render_template
from flask.ext.pymongo import PyMongo
import settings as s

app=Flask("Crackpot")

app.config['MONGO_HOST']=s.MONGO_HOST
app.config['MONGO_PORT']=s.MONGO_PORT
app.config['MONGO_USERNAME']=s.MONGO_USERNAME
app.config['MONGO_PASSWORD']=s.MONGO_PASSWORD
app.config['MONGO_DBNAME']=s.MONGO_DBNAME

mongo=PyMongo(app)

@app.route("/")
def index():
	return render_template("home.html",title="Crackpot | Welcome Crackster!")
	
@app.route("/signup")
def signup():
	return render_template("signup.html", title="Crackpot | New Registration")

if __name__=="__main__":
	app.debug=True
	app.run()
