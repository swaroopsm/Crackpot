#!/usr/bin/python
import sha, json
import settings as s

class Users:
	
	@staticmethod
	def new(m,name,email,password,username):
		salt=s.PASSWORD_SALT
		password=sha.new(salt).hexdigest()+sha.new(password).hexdigest()
		try:
			st=str(m.db.users.save({'name':name,'email':email,'password':password,'username':username}))
			return json.dumps({'_id':st,'status': 'success', 'message':'Successfully registered. Please wait...'})
		except:
			return json.dumps({'status': 'error', 'message': 'There was an error. Please try again later...'})
			
