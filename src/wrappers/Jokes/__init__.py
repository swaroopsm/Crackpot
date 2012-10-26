#!/usr/bin/python
class Jokes:
	@staticmethod
	def new(m,username,joke_title,joke_desc,joke_tags):
		try:
			m.db.jokes.save({"title": joke_title, "desc": joke_desc, "tags": joke_tags})
			return True
		except:
			return False
