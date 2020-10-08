from tinydb import TinyDB, Query
from time import time

class Db():
	def __init__(self):
		self.db = TinyDB('db.json')


	def set(self,id,passwd,data):
		self.db.insert({'id':id, 'passwd':passwd,'utime': int(time()), 'data':data})

	def get_all(self):
		return self.db.all()

	def get(self,id):
		que = Query()
		try:
			data = self.db.search(que.id == id)[0]
		except IndexError:
			return []
		return data

	def delete(self,id,passwd) -> bool:
		que = Query()
		try:
			group = self.db.search(que.id == id)[0]
			print(group)
			if group["passwd"] == passwd:
				self.db.remove(que.id == id)
				return True
			else:
				return False
		except Exception:
			return False

	def old_data_delete(self):
		que = Query()
		delete_time = int(time()) - 86400
		self.db.remove(que.utime > delete_time)

