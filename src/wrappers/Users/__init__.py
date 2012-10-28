#!/usr/bin/python
import md5, sha, json
import settings as s

class Users:
	
	@staticmethod
	def check_username(m,username):
		c=m.db.users.find({'username': username}).count()
		return c
	
	@staticmethod
	def new(m,name,email,password,username):
		salt=s.PASSWORD_SALT
		password=sha.new(salt).hexdigest()+sha.new(password).hexdigest()
		if(Users.check_username(m,username)>0):
			return json.dumps({'status': 'error', 'message': 'Username already taken..'})
		else:
			try:
				avatar="http://gravatar.com/avatar/"+md5.new(email).hexdigest()
				st=str(m.db.users.save({'name':name,'email':email,'password':password,'username':username, 'avatar': avatar}))
				return json.dumps({'_id':st,'status': 'success', 'message':'Successfully registered. Please wait...'})
			except:
				return json.dumps({'status': 'error', 'message': 'There was an error. Please try again later...'})
	
	@staticmethod
	def update(m,username,name,email,bio,url,location):
		try:
			m.db.users.update({"username": username}, {'$set': {"name": name, "email": email, "bio": bio, "url": url, "location": location }})
			return json.dumps({'status': 'success', 'message': 'Profile information updated successfully'})
		except:
			return json.dumps({'status': 'error', 'message': 'There was an error. Please try again later...'})
	
	@staticmethod
	def view(m,username):
		a=m.db.users.find({'username': username},{'password': 0})
		
		### ToDo: Handle follower/following count issue
		
		c=m.db.jokes.find({'username': username}).count()
		info={}
		for i in a:
			del i['_id']
		 	info.update(i)
		info.update({"jokes": c})
		return info
	
	@staticmethod
	def subscribe(m,username,subscribe,user_name,user_bio,user_avatar, ref_name, ref_bio, ref_avatar):
		try:
			m.db.users.update({"username": username}, {"$push": { "following": {'user': subscribe, 'name': user_name, 'bio': user_bio, 'avatar': user_avatar}}})
			m.db.users.update({"username": subscribe}, {"$push": {"follower": {'user': username, 'name': ref_name, 'bio': ref_bio, 'avatar': ref_avatar}}})
			return json.dumps({"status": "success"})
		except:
			return json.dumps({"status": "error"})
		
	@staticmethod
	def get_userinfo(m, username):
		st=m.db.users.find({'username': username})
		d={}
		for i in st:
			del i['_id']
			d.update(i)
		return d
		
	@staticmethod
	def user_followers(m,username):
		d={}
		a=m.db.users.find({"username": username},{"following": 1})
		for i in a:
			del i['_id']
			d.update(i)
		return d
		
	@staticmethod
	def user_subscribers(m,username):
		d={}
		a=m.db.users.find({"username": username},{"follower": 1})
		for i in a:
			del i['_id']
			d.update(i)
		return d
