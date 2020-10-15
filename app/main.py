import uuid
import threading
import time
import schedule
from pprint import pprint, pformat

from fastapi import Body, FastAPI, Header
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Optional
from user_agents import parse
from starlette.responses import RedirectResponse


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


def debuger():
	print([i.doc_id for i in db.get_all()])

def share_response_html(id, json) -> str:
	html = f"<meta http-equiv='refresh' content=\"0;URL='zisakuziten://{id}'\" /><h1>not installed zisakuziten</h1>"

	html += "<p>" + pformat(json) + "</p>"
	return html




@app.post("/post/")
async def create_group(group: Group):
	# debuger()
	id = create_id()
	passwd = create_passwd()
	db.set(id,passwd,group.json())
	return {"res": "ok", "id": id,"passwd":passwd}


@app.get("/get/{id}")
async def get_group(id: str, user_agent: Optional[str] = Header(None)):
	# debuger()
	ua = parse(user_agent)
	if ua.browser.family == "%E8%87%AA%E4%BD%9C%E8%BE%9E%E5%85%B8":
		print("this get is ZisakuZitenApp")

	data = db.get(id)
	if data == []:
		return {"res": "ng","data": ""}
	return {"res": "ok", "data": data["data"]}


@app.post("/delete/")
async def delete_group(su: SuperUser):
	# debuger()
	res = db.delete(su.id, su.passwd)
	resstr = "ok" if res else "ng"
	return {"res": resstr}

@app.get("/share/{id}")
async def share_group(id, user_agent: Optional[str] = Header(None)):
	ua = parse(user_agent)
	data = db.get(id)
	if ua.browser.family == "%E8%87%AA%E4%BD%9C%E8%BE%9E%E5%85%B8":
		if data == []:
			return {"res": "ng","data": ""}
		return {"res": "ok", "data": data["data"]}
	else:
		if data == []:
			return {"res": "ng","data": ""}
		# response = RedirectResponse(url="zisakuziten://")
		# return respons
		return HTMLResponse(content=share_response_html(id, data["data"]), status_code=200)
		# return "who are you?"
