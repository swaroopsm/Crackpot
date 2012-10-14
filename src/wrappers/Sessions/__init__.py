#!/usr/bin/python

import sha
import settings as s

class Sessions:
	
	@staticmethod
	def login(m,username,password):
		password=sha.new(s.PASSWORD_SALT).hexdigest()+sha.new(password).hexdigest()
		st=m.db.users.find({"username": username,"password": password}).count()
		if st>0:
			l={}
			z=m.db.users.find({"username": username})
			for i in z:
				del i['_id']
				l.update(i)
			return l['username']
		else:
			return False
