import docker
import os
from flask import Flask, request, jsonify,json
from threading import Thread, Lock
import requests
import time

flag=0
n_cont=0
n_req=0
c=0
container=dict()
app = Flask(__name__)


client = docker.from_env()
container['800'+str(n_cont)]=client.containers.run("acts",ports={80:int('800'+str(n_cont))},network="my-network",detach=True, name="acts"+str(n_cont))
n_cont+=1



def health_check():
	while(1):
		global n_cont
		global container
		global client
		for i in range(n_cont):
			print(i)
			try:
				resp=requests.get("http://0.0.0.0:800"+str(i)+"/api/v1/_health")
				if(resp.status_code==500):
					temp=client.containers.get(str(container['800'+str(i)].id))
					temp.stop()
					temp.remove()
					container['800'+str(i)]=client.containers.run("acts", ports={80:int('800'+str(i))}, network="my-network", detach=True, name="acts"+str(i))
			except:
				print("\n\n you have enterded health exception\n\n")
			print("\nport: ",i,"\n")
		time.sleep(1)


def scale():
	while(1):
		global n_req
		global container
		global n_cont
		global client
		time.sleep(120)
		if(n_req in range(20)):
			for i in range(1,n_cont):
				temp=client.containers.get(str(container['800'+str(i)].id))
				temp.stop()
				temp.remove()
				del container['800'+str(i)]
			n_cont=1

		elif(n_req in range(20,40)):
			if(n_cont<2):
				container['800'+str(n_cont)]=client.containers.run("acts",ports={80:int('800'+str(n_cont))},network="my-network",detach=True,name="acts"+str(n_cont), hostname="0.0.0.0")
				n_cont+=1
				print(container)
			while(n_cont>2):
				temp=client.containers.get(str(container['800'+str(n_cont-1)].id))
				temp.stop()
				temp.remove()
				del container['800'+str(n_cont-1)]
				n_cont-=1

		elif(n_req in range(40,60)):
			while(n_cont<3):
				container['800'+str(n_cont)]=client.containers.run("acts",ports={80:int('800'+str(n_cont))},network="my-network",detach=True,name="acts"+str(n_cont))
				n_cont+=1
			while(n_cont>3):
				temp=client.containers.get(str(container['800'+str(n_cont-1)].id))
				temp.stop()
				temp.remove()
				del container['800'+str(n_cont-1)]
				n_cont-=1

		elif(n_req in range(60,80)):
			while(n_cont<4):
				container['800'+str(n_cont)]=client.containers.run("acts",ports={80:int('800'+str(n_cont))},network="my-network",detach=True,name="acts"+str(n_cont))
				n_cont+=1
			while(n_cont>4):
				temp=client.containers.get(str(container['800'+str(n_cont-1)].id))
				temp.stop()
				temp.remove()
				del container['800'+str(n_cont-1)]
				n_cont-=1

		elif(n_req in range(80,100)):
			while(n_cont<5):
				container['800'+str(n_cont)]=client.containers.run("acts",ports={80:int('800'+str(n_cont))},network="my-network",detach=True,name="acts"+str(n_cont))
				n_cont+=1
			while(n_cont>5):
				temp=client.containers.get(str(container['800'+str(n_cont-1)].id))
				temp.stop()
				temp.remove()
				del container['800'+str(n_cont-1)]
				n_cont-=1

		elif(n_req in range(100,120)):
			while(n_cont<6):
				container['800'+str(n_cont)]=client.containers.run("acts",ports={80:int('800'+str(n_cont))},network="my-network",detach=True,name="acts"+str(n_cont))
				n_cont+=1
			while(n_cont>6):
				temp=client.containers.get(str(container['800'+str(n_cont-1)].id))
				temp.stop()
				temp.remove()
				del container['800'+str(n_cont-1)]
				n_cont-=1

		elif(n_req in range(120,140)):
			while(n_cont<7):
				container['800'+str(n_cont)]=client.containers.run("acts",ports={80:int('800'+str(n_cont))},network="my-network",detach=True,name="acts"+str(n_cont))
				n_cont+=1
			while(n_cont>7):
				temp=client.containers.get(str(container['800'+str(n_cont-1)].id))
				temp.stop()
				temp.remove()
				del container['800'+str(n_cont-1)]
				n_cont-=1
				
		elif(n_req in range(140,160)):
			while(n_cont<8):
				container['800'+str(n_cont)]=client.containers.run("acts",ports={80:int('800'+str(n_cont))},network="my-network",detach=True,name="acts"+str(n_cont))
				n_cont+=1
			while(n_cont>8):
				temp=client.containers.get(str(container['800'+str(n_cont-1)].id))
				temp.stop()
				temp.remove()
				del container['800'+str(n_cont-1)]
				n_cont-=1
				
		elif(n_req in range(160,180)):
			while(n_cont<9):
				container['800'+str(n_cont)]=client.containers.run("acts",ports={80:int('800'+str(n_cont))},network="my-network",detach=True,name="acts"+str(n_cont))
				n_cont+=1
			while(n_cont>9):
				temp=client.containers.get(str(container['800'+str(n_cont-1)].id))
				temp.stop()
				temp.remove()
				del container['800'+str(n_cont-1)]
				n_cont-=1
				
		elif(n_req in range(180,200)):
			for i in range(n_cont,10):
				container['800'+str(i)]=client.containers.run("acts",ports={80:int('800'+str(i))},network="my-network",detach=True, name="acts"+str(n_cont))
			n_cont=10
		n_req=0
"""
@app.route("/api/v1/_health", methods=['GET'])
def testing():
	print("health check entering here")
	resp=requests.get("http://0.0.0.0:800"+str(0)+"/api/v1/_health")
	response = app.response_class(response=json.dumps({}), status=resp.status_code, mimetype='application/json')
	return response
"""

@app.route("/api/v1/<path:url>", methods=['GET','DELETE'])
def load_balance_gd(url):
	print("\n\n you entered  get and delete\n\n")
	global flag
	global c
	global n_cont
	global n_req
	
	if(flag==0):
		flag=1
		
		scaling=Thread(target=scale)
		scaling.start()
		health=Thread(target=health_check)
		health.start()
		
	m=request.method
	p=request.path
	print("\n\n",p,"\n\n")
	if(m=='GET'):
		resp=requests.get("http://0.0.0.0:800"+str(c)+p)
		print("GET")
	elif(m=='DELETE'):
		resp=requests.delete("http://0.0.0.0:800"+str(c)+p)
		print("DELETE")
	else:
		print("INVALID")

	c=(c+1)%n_cont
	if(resp.status_code!=404 and p not in ["/api/v1/_health","/api/v1/_crash"]):
		n_req+=1
	try:
		response=app.response_class(response=json.dumps(resp.json()), status=resp.status_code, mimetype='application/json')
	except ValueError:
		response = app.response_class(response=json.dumps({}), status=resp.status_code, mimetype='application/json')

	return response
	


	
@app.route("/api/v1/<path:url>", methods=['POST'])
def load_balance_p(url):
	print("\n\n you  entered  post\n\n")
	m=request.method
	p=request.path
	global c
	global n_cont
	global n_req
	global flag
	try:
		d=request.get_json()
	except:
		print("no content")
		resp=requests.post("http://0.0.0.0:800"+str(c)+p, json={})
		response = app.response_class(response=json.dumps({}), status=resp.status_code, mimetype='application/json')
		return response

	print("get d is done")
	if(flag==0):
		flag=1
		
		scaling=Thread(target=scale)
		scaling.start()
		health=Thread(target=health_check)
		health.start()
		
		print("threads started")
	m=request.method
	p=request.path
	print("got m and p")
	resp=requests.post("http://0.0.0.0:800"+str(c)+p,json=d)

	print("POST")
	
	c=(c+1)%n_cont
	
	if(resp.status_code!=404 and p not in ["/api/v1/_health","/api/v1/_crash"]):
		n_req+=1
	try:
		response=app.response_class(response=json.dumps(resp.json()), status=resp.status_code, mimetype='application/json')
	except ValueError:
		response = app.response_class(response=json.dumps({}), status=resp.status_code, mimetype='application/json')

	print(resp)
	return response






if __name__ == '__main__':
	app.run(host="0.0.0.0",port=80)




for i in range(n_cont):
	for container in client.containers.list(filters={"name":"acts"+str(i)}):
		print(container)
		temp=client.containers.get(str(container.id))
		temp.remove(force=True)

