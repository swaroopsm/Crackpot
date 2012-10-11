#!/usr/bin/python

from flask import Flask, render_template

app=Flask("Crackpot")

@app.route("/")
def index():
	return render_template("home.html",title="Crackpot | Welcome Crackster!")
	
@app.route("/signup")
def signup():
	return render_template("signup.html", title="Crackpot | New Registration")
	
if __name__=="__main__":
	app.debug=True
	app.run()
