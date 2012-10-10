#!/usr/bin/python

from flask import Flask

app=Flask("Crackpot")

@app.route("/")
def index():
	return "Welcome Crackster!"
	
if __name__=="__main__":
	app.debug=True
	app.run()
