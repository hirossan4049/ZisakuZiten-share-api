import uuid
import threading
import time
import schedule

from fastapi import Body, FastAPI
from pydantic import BaseModel
from typing import List

try:
	from db import Db
except ImportError:
	from app.db import Db

app = FastAPI()
db = Db()


schedule.every(1).hours.do(db.old_data_delete)

def old_deleter():
	t = threading.currentThread()
	while getattr(t, "do_run", True):
		schedule.run_pending()
		time.sleep(1)

class SuperUser(BaseModel):
	id: str
	passwd: str

class Ziten(BaseModel):
	title: str
	content: str
	updateTime: str

class Group(BaseModel):
    title: str
    updateTime: str
    ziten_updT_List: List[Ziten]

def create_id() -> str:
	return str(uuid.uuid4())

def create_passwd() -> str:
	return str(uuid.uuid4())[:6]

old_data_delete_t = threading.Thread(target=old_deleter)
@app.on_event("startup")
async def startup():
	global old_data_delete_t
	old_data_delete_t.start()

@app.on_event("shutdown")
async def shutdown():
	global old_data_delete_t
	old_data_delete_t.do_run = False
	old_data_delete_t.join()



@app.post("/post/")
async def create_group(group: Group):
	print(group)
	id = create_id()
	passwd = create_passwd()
	db.set(id,passwd,group.json())
	return {"res": "ok", "id": id,"passwd":passwd}


@app.get("/get/{id}")
async def get_group(id: str):
	data = db.get(id)
	if data == []:
		return {"res": "ng","data": ""}
	return {"res": "ok", "data": data["data"]}


@app.post("/delete/")
async def delete_group(su: SuperUser):
	res = db.delete(su.id, su.passwd)
	resstr = "ok" if res else "ng"
	return {"res": resstr}
