#!/usr/bin/python

from flask import Flask, render_template, request, redirect, url_for, session
from flask.ext.pymongo import PyMongo
from flask_pymongo import ObjectId
import settings as s, md5
import json
import sys
sys.path.insert(0,"wrappers/")

from Users import Users as u
from Sessions import Sessions as se
from Jokes import Jokes as j

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
			return render_template("user.html", title="Crackpot", username=session['username'], avatar_hash=get_userinfo('email_hash'))
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
			info={}
			info.update({'bg_color': get_userinfo('bg_color')})
			info.update({'name': get_userinfo('name')})
			info.update({'email': get_userinfo('email')})
			info.update({'bio': get_userinfo('bio')})
			info.update({'url': get_userinfo('url')})
			info.update({'location': get_userinfo('location')})
			return render_template("profile.html", title="Crackpot | Profile", username=session['username'], avatar_hash=get_userinfo('email_hash'), info=info)
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
	color=request.form['color']
	return u.update(mongo,session['username'],name,email,bio,url,location,color)

@app.route("/subscribe", methods=['POST'])
def subscribe():
	try:
		if session['loggedin'] == True:
			name=request.form['subscribe']
			user_name=request.form['name']
			user_bio=request.form['bio']
			user_avatar=request.form['avatar']
			ref_name=request.form['ref_name']
			ref_bio=request.form['ref_bio']
			ref_avatar=request.form['ref_avatar']
			return u.subscribe(mongo,session['username'],name,user_name,user_bio,user_avatar, ref_name, ref_bio, ref_avatar)
		else:
			return json.dumps({"status": "loggedin_error", "url": "/login"})
	except KeyError:
		return json.dumps({"status": "loggedin_error", "url": "/login"})

@app.route("/<username>")
def public_profile(username):
		a=u.view(mongo,username)
		if a.has_key('username'):	
			a.update({'email_hash': md5.new(a['email']).hexdigest()})
			try:
				ref={}
				ref.update({'ref_name': get_userinfo('name'), 'ref_bio': get_userinfo('bio'), 'ref_avatar': get_userinfo('email_hash')})
				return render_template("public_view.html", title="Crackpot | "+a['name'], info=a, ref=ref)
			except KeyError:
				return render_template("public_view.html", title="Crackpot | "+a['name'], info=a)
		else:
			return "Error! Not found..."

@app.route("/get_followers",methods=['POST'])
def get_followers():
	try:
		if session['loggedin']  == True:
			a=u.user_followers(mongo,request.form['user'])
			a.update({"status":"success"})
			return json.dumps(a)
	except KeyError:
		a=u.user_followers(mongo,request.form['user'])
		a.update({"status":"error"})
		return json.dumps(a)

@app.route("/my_info", methods=['POST'])
def my_info():
	a=u.view(mongo,session['username'])	
	a.update({'email_hash': md5.new(a['email']).hexdigest()})
	return json.dumps(a)

@app.route("/subscriptions", methods=['POST','GET'])
def my_followers():
	try:
		if session['loggedin'] == True:
			return render_template("my_subscriptions.html", title="Crackpot | Subscriptions", username=session['username'], avatar_hash=get_userinfo('email_hash'))
	except KeyError:
		return ""
		
@app.route("/subscribers", methods=['POST','GET'])
def my_subscribers():
	try:
		if session['loggedin'] == True:
			return render_template("my_subscribers.html", title="Cracpot | Subscribers", username=session['username'], avatar_hash=get_userinfo('email_hash'))
	except KeyError:
		return redirect(url_for("login"))
		
@app.route("/get_subscribers", methods=['POST'])
def get_subscribers():
	try:
		if session['loggedin'] == True:
			a=u.user_subscribers(mongo,request.form['user'])
			a.update({"status":"success"})
			return json.dumps(a)
	except KeyError:
		a=u.user_subscribers(mongo,request.form['user'])
		a.update({"status":"error"})
		return json.dumps(a)
		
@app.route("/crack", methods=['POST','GET'])
def crack():
	try:
		if session['loggedin'] == True:
			return render_template("new_joke.html", title="Crackpot | Crack a Joke")
	except KeyError:
		return redirect(url_for('login'))

@app.route("/submit_joke", methods=['POST'])
def submit_joke():
	try:
		if session['loggedin']==True:
			joke_title=request.form['joke_title']
			joke_desc=request.form['joke_desc']
			joke_tags_bf=request.form['joke_tags'].split(',')
			joke_tags=[]
			for i in joke_tags_bf:
				joke_tags.append(i.strip())
			joke_date=request.form['joke_date']
			avatar="http://gravatar.com/avatar/"+get_userinfo('email_hash')
			a=j.new(mongo,session['username'],joke_title,joke_desc,joke_tags,joke_date,avatar)
			if a == True:
				return json.dumps({"status": "success", "msg": "Joke added successfully"})
			else:
				return json.dumps({"status": "error", "msg": "There was an error, please try again later"})
	except KeyError:
		return redirect(url_for('login'))

@app.route("/jokes")
def jokes():
	try:
		if session['loggedin']==True:
			return render_template("my_jokes.html", title="Crackpot | My Jokes", username=session['username'], avatar_hash=get_userinfo('email_hash'))
	except KeyError:
		return redirect(url_for('login'))

@app.route("/get_jokes", methods=['POST'])
def get_jokes():
	try:
		if session['loggedin']==True:
			return json.dumps(j.view_with_id(mongo,session['username']))
	except KeyError:
		return redirect(url_for('login'))

@app.route("/subscribed_jokes", methods=['POST'])
def subscribed_jokes():
	try:
		a=u.user_followers(mongo,session['username'])
		d=[]
		for i in a['following']:
			d.append(i['user'])
		return json.dumps(j.my_wall(mongo,d))
	except KeyError:
		return json.dumps({"status": "error"})

@app.route("/complete_joke", methods=['POST'])
def complete_joke():
	try:
		if session['loggedin']==True:
			return json.dumps(j.get_joke(mongo,ObjectId(request.form['oid'])))
	except KeyError:
		return json.dumps({"status": "success"})

@app.route("/public_info", methods=['POST'])
def public_info():
	return json.dumps(u.view(mongo,request.form['username']))

@app.route("/public_jokes", methods=['POST'])
def public_jokes():
	return json.dumps(j.view_with_id(mongo,request.form['username']))

@app.route("/more_jokes", methods=['POST'])
def more_jokes():
	a=u.user_followers(mongo,session['username'])
	d=[]
	for i in a['following']:
		d.append(i['user'])
	return json.dumps(j.load_more_jokes(mongo,d,ObjectId(request.form['oid'])))

@app.route("/<username>/subscribers")
def pub_subscribers(username):
	try:
		a=u.view(mongo,username)	
		a.update({'email_hash': md5.new(a['email']).hexdigest()})
		return render_template("user_subscribers.html", title="Crackpot | "+a['name'], info=a)
	except KeyError:
		return "Error, not found!"

@app.route("/<username>/subscriptions")
def pub_subscriptions(username):
	try:
		a=u.view(mongo,username)	
		a.update({'email_hash': md5.new(a['email']).hexdigest()})
		return render_template("user_subscriptions.html", title="Crackpot | "+a['name'], info=a)
	except KeyError:
		return "Error, not found!"

@app.route("/tags/<tag>")
def tags(tag):
	tag=tag.replace("+"," ")
	a=j.get_tagged(mongo,tag)
	return render_template("tagged.html", info=(a), tagged=tag)

@app.route("/delete_joke", methods=['POST'])
def delete_joke():
	joke_id=request.form['id']
	return json.dumps({"status": j.delete_joke(mongo,ObjectId(joke_id))})


if __name__=="__main__":
	app.secret_key=s.APP_SECRET_KEY
	app.jinja_env.globals.update(get_userinfo=get_userinfo)
	app.debug=True
	app.run()
