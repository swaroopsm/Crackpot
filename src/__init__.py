#!/usr/bin/python

from flask import Flask, render_template

app=Flask("Crackpot")

@app.route("/")
def index():
	return render_template("home.html",title="Crackpot | Welcome Crackster!")
	
if __name__=="__main__":
	app.debug=True
	app.run()
