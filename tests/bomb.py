

print("""
===========================================
DataBase & fastAPI stress test.
DANGER: A large number of requests are flying in. 	
===========================================
""")
i = input("begin?(y/n) >>")

if i != "y":
	exit()

import requests
from tqdm import tqdm
import time

#baseurl = "http://0.0.0.0:8000/"
baseurl = "http://59.137.252.9:8585/"

ziten = {
	      "title": "string",
	      "content": "string",
	      "updateTime": "string"
	    }

def postest():
	print("=======POST START========")
	postdata = {
	  "title": "string",
	  "updateTime": "string",
	  "ziten_updT_List": [
	  ]
	}
	for i in range(50):
		postdata["ziten_updT_List"].append(ziten)

	resdicts = []
	for i in tqdm(range(100)):
		res = requests.post(baseurl+"post",json=postdata)
		resdicts.append(res.json())

	print("=======POST END========")
	return resdicts

def getest(resdicts):
	print("=======GET START========")
	for item in tqdm(resdicts):
		requests.get(baseurl+"get/"+item["id"])
	print("=======GET END========")

def deletest(resdicts):
	print("=====DELETE START=====")
	for item in tqdm(resdicts):
		json = {"id":item["id"], "passwd":item["passwd"]}
		res = requests.post(baseurl+"delete",json=json)
	print("=====DELETE END=======")

sp = time.time()
res = postest()
ep = time.time()
sg = time.time()
getest(res)
eg = time.time()
sd = time.time()
deletest(res)
ed = time.time()

print("POST  :",ep-sp)
print("GET   :",eg-sg)
print("DELETE:",ed-sd)
