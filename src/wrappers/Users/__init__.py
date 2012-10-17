#!/usr/bin/python
import sha, json
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
				st=str(m.db.users.save({'name':name,'email':email,'password':password,'username':username}))
				return json.dumps({'_id':st,'status': 'success', 'message':'Successfully registered. Please wait...'})
			except:
				return json.dumps({'status': 'error', 'message': 'There was an error. Please try again later...'})
	
	@staticmethod
	def update(m,username,name,email,bio,url,location):
		try:
			m.db.users.update({"username": username}, {'$set': {"name": name, "email": email, "bio": bio, "url": url, "location": location }})
			return json.dumps({'status': 'success', 'message': 'Updated successfully'})
		except:
			return json.dumps({'status': 'error', 'message': 'There was an error. Please try again later...'})
				
	@staticmethod
	def get_userinfo(m, username):
		st=m.db.users.find({'username': username})
		d={}
		for i in st:
			del i['_id']
			d.update(i)
		return d
