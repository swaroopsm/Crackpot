#!/usr/bin/python
class Jokes:
	@staticmethod
	def new(m,username,joke_title,joke_desc,joke_tags,joke_date):
		try:
			m.db.jokes.save({"username": username, "title": joke_title, "desc": joke_desc, "tags": joke_tags, "date": joke_date})
			return True
		except:
			return False
