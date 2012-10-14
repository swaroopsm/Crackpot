#!/usr/bin/python

import sha
import settings as s

class Sessions:
	
	@staticmethod
	def login(m,username,password):
		password=sha.new(s.PASSWORD_SALT).hexdigest()+sha.new(password).hexdigest()
		st=m.db.users.find({"username": username,"password": password}).count()
		return st
