#!/usr/bin/python
import json
class Jokes:
	@staticmethod
	def new(m,username,joke_title,joke_desc,joke_tags,joke_date):
		try:
			m.db.jokes.save({"username": username, "title": joke_title, "desc": joke_desc, "tags": joke_tags, "date": joke_date})
			return True
		except:
			return False
			
	@staticmethod
	def view(m,username):
		jokes_list=[]
		a=m.db.jokes.find({'username': username}).sort("_id", -1)
		for i in a:
			del i['_id']
			jokes_list.append(i)
		return jokes_list
