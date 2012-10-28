#!/usr/bin/python

class Jokes():
	@staticmethod
	def new(m,username,joke_title,joke_desc,joke_tags,joke_date,avatar):
		try:
			m.db.jokes.save({"username": username, "title": joke_title, "desc": joke_desc, "tags": joke_tags, "date": joke_date,"avatar": avatar})
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
		
	@staticmethod
	def my_wall(m,subscribers):
		mywall_list=[]
		a=m.db.jokes.find({'username': { '$in': subscribers }}).sort('_id', -1).limit(8)
		for i in a:
			k=str(i['_id'])
			del i['_id']
			mywall_list.append({"_id": k, "values": i})
		return mywall_list
		
	@staticmethod
	def get_joke(m,oid):
		d={}
		a=m.db.jokes.find({"_id": oid})
		for i in a:
			del i['_id']
			d.update(i)
		return d
		
	@staticmethod
	def view_with_id(m,username):
		jokes_list=[]
		a=m.db.jokes.find({'username': username}).sort("_id", -1)
		for i in a:
			k=str(i['_id'])
			del i['_id']
			jokes_list.append({"_id": k, "values": i})
		return jokes_list
		
	@staticmethod
	def load_more_jokes(m,subscribers,oid):
		jokes_list=[]
		a=m.db.jokes.find({ '$and': [{'username': { '$in': subscribers }},{"_id": {'$lt': oid}} ] } ).sort('_id', -1).limit(4)
		for i in a:
			k=str(i['_id'])
			del i['_id']
			jokes_list.append({"_id": k, "values": i})
		return jokes_list
