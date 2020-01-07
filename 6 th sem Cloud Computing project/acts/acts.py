from flask import Flask, request, jsonify,json
import pymysql
#import mysql.connector
import datetime
import base64
import binascii
import requests

app = Flask(__name__)
con=pymysql.connect(host="mysql-serv", user="root", password="root", db="selfielessacts")
#con=pymysql.connect(host="localhost", user="root", password="king@123", db="selfielessacts")

cur=con.cursor()


count =0
crash=0


@app.route('/api/v1/_health', methods=['GET'])
def health_check():
	global crash
	if(crash == 1):
		response = app.response_class(response=json.dumps({}), status=500, mimetype='application/json')
		return response
		
	response = app.response_class(response=json.dumps({}), status=200, mimetype='application/json')
	return response

@app.route('/api/v1/_crash' , methods=['POST'])
def crash_server():
	global crash
	if(crash == 1):
		response = app.response_class(response=json.dumps({}), status=500, mimetype='application/json')
		return response
	
	crash=1
	response = app.response_class(response=json.dumps({}), status=200, mimetype='application/json')
	return response


	



@app.route('/api/v1/acts/count', methods=['GET'])
def list_no_acts():
	global crash
	if(crash == 1):
		response = app.response_class(response=json.dumps({}), status=500, mimetype='application/json')
		return response
	global count
	count = count + 1
	cur.execute("SELECT COUNT(DISTINCT actId) AS COUNT FROM acts")
	ret=cur.fetchall()
	d=[]
	for i in ret:
		d.append(i[0])
	response = jsonify(d)
	return response




# 3.Function to list number of acts in each category
@app.route('/api/v1/categories', methods=['GET'])
def list_categories():
	global crash
	if(crash == 1):
		response = app.response_class(response=json.dumps({}), status=500, mimetype='application/json')
		return response

	global count
	count = count + 1
	cur.execute("SELECT category, COUNT(DISTINCT actId) AS COUNT FROM acts GROUP BY category")
	ret=cur.fetchall()
	if(len(ret)==0):
		print("this is 8:00 our last try\n\n\n")
		response = app.response_class(response=json.dumps({}), status=204, mimetype='application/json')
	else:
		d=dict()
		for i in ret:
			d[i[0]]=i[1]
		response = jsonify(d)
	return response






# 4.Function to add a category
@app.route('/api/v1/categories', methods=['POST'])
def add_category():
	print("you have entered please type")
	global crash
	if(crash == 1):
		print("crash")
		response = app.response_class(response=json.dumps({}), status=500, mimetype='application/json')
		return response

	global count
	count = count + 1
	data=request.get_json()
	for category in data:
		cur.execute("SELECT COUNT(*) FROM categories WHERE category=%s", category)
		n=cur.fetchone()[0]
		if(n==0):
			print("inside")
			query = ("INSERT INTO categories VALUES (%s)")
			input_data=(category)
			cur.execute(query, input_data)
			con.commit()
			response = app.response_class(response=json.dumps({}), status=201, mimetype='application/json')
		elif(n!=0):
			print("oh no 400 why?")
			response = app.response_class(response=json.dumps({}), status=400, mimetype='application/json')
	
	return response


# 5.Function to remove a category
@app.route('/api/v1/categories/<category>', methods=['DELETE'])
def rem_category(category):
	global crash
	if(crash == 1):
		response = app.response_class(response=json.dumps({}), status=500, mimetype='application/json')
		return response

	global count
	count = count + 1
	cur.execute("SELECT COUNT(*) FROM categories WHERE category=(%s)", category)
	n=cur.fetchone()[0]
	if(n==0):
		response = app.response_class(response=json.dumps({}), status=400, mimetype='application/json')
	else:
		cur.execute("DELETE FROM acts WHERE category=(%s)", category)
		con.commit()
		cur.execute("DELETE FROM categories WHERE category=(%s)", category)
		con.commit()
		response = app.response_class(response=json.dumps({}), status=200, mimetype='application/json')
	return response


# 6 & 8.Function to list acts in a given category with optional range
@app.route('/api/v1/categories/<category>/acts', methods=['GET'])
def list_acts(category):
	global crash
	if(crash == 1):
		response = app.response_class(response=json.dumps({}), status=500, mimetype='application/json')
		return response

	global count
	count = count + 1
	cur.execute("SELECT COUNT(*) FROM categories WHERE category=(%s)", category)
	n=cur.fetchone()[0]
	if(n==0):
		response = app.response_class(response=json.dumps({}), status=204, mimetype='application/json')
		return response

	if(len(request.args)==0):
		cur.execute("SELECT COUNT(DISTINCT actId) FROM acts WHERE category=(%s)", category)
		n=cur.fetchone()[0]
		if(n>100):
			response = app.response_class(response=json.dumps({}), status=413, mimetype='application/json')
			return response
		else:
			cur.execute("SELECT * FROM acts WHERE category=(%s)",category)
	else:
		start=int(request.args['start'])
		end=int(request.args['end'])
		cur.execute("SELECT COUNT(*) FROM acts WHERE category=(%s)", category)
		n=cur.fetchone()[0]

		if((end-start+1)>100):
			response = app.response_class(response=json.dumps({}), status=413, mimetype='application/json')
			return response
		elif(start<1 or end>n):
			response = app.response_class(response=json.dumps({}), status=400, mimetype='application/json')
			return response
		else:
			cur.execute("SELECT * FROM acts ORDER BY time_stamp DESC LIMIT %s, %s", (start-1, end-start+1))
			
	json_list=list()
	json_array=list()
	json_array=cur.fetchall()
	for i in json_array:
		print(i)
		d=dict()
		d["actId"]=i[0]
		d["username"]=i[1]
		k=str(i[2])
		ss=k[17:19]
		mi=k[14:16]
		hh=k[11:13]
		dd=k[8:10]
		mm=k[5:7]
		yyyy=k[0:4]
		t=dd+"-"+mm+"-"+yyyy+":"+ss+"-"+mi+"-"+hh				

		d["timestamp"]=t
		d["caption"]=i[3]
		d["upvotes"]=i[6]
		d["imgB64"]=i[5]
		json_list.append(d)

	response = app.response_class(response=json.dumps(json_list), status=200, mimetype='application/json')
	return response



# 7.Function to return number of acts in a given category
@app.route('/api/v1/categories/<category>/acts/size', methods=['GET'])
def no_of_acts(category):
	global crash
	if(crash == 1):
		response = app.response_class(response=json.dumps({}), status=500, mimetype='application/json')
		return response

	global count
	count = count + 1
	cur.execute("SELECT COUNT(*) FROM categories WHERE category=(%s)", category)
	n=cur.fetchone()[0]
	if(n==0):
		response = app.response_class(response=json.dumps({}), status=204, mimetype='application/json')
	else:
		cur.execute("SELECT COUNT(*) FROM acts WHERE category=(%s)", category)
		n=cur.fetchone()[0]
		response = app.response_class(response=json.dumps([n]), status=200, mimetype='application/json')
	return response



# 9.Function to upvote
@app.route('/api/v1/acts/upvote', methods=['POST'])
def upvote():
	global crash
	if(crash == 1):
		response = app.response_class(response=json.dumps({}), status=500, mimetype='application/json')
		return response

	global count
	count = count + 1
	data=request.get_json()
	for actId in data:
		cur.execute("SELECT COUNT(*) FROM acts WHERE actId=(%s)", actId)
		n=cur.fetchone()[0]
		if(n==0):
			response = app.response_class(response=json.dumps({}), status=400, mimetype='application/json')
		else:
			cur.execute("UPDATE acts SET likes=likes+1 WHERE actId=(%s)", actId)
			con.commit()
			response = app.response_class(response=json.dumps({}), status=200, mimetype='application/json')
	return response




# 10.Function to remove an act
@app.route('/api/v1/acts/<actId>', methods=['DELETE'])
def rem_act(actId):
	global crash
	if(crash == 1):
		response = app.response_class(response=json.dumps({}), status=500, mimetype='application/json')
		return response

	global count
	count = count + 1
	cur.execute("SELECT COUNT(*) FROM acts WHERE actId=(%s)", actId)
	n=cur.fetchone()[0]
	if(n==0):
		response = app.response_class(response=json.dumps({}), status=400, mimetype='application/json')
	else:
		cur.execute("DELETE FROM acts WHERE actId=(%s)", actId)
		con.commit()
		response = app.response_class(response=json.dumps({}), status=200, mimetype='application/json')
	return response




# 11.Function to upload an act
@app.route('/api/v1/acts', methods=['POST'])
def upload_act():
	global crash
	if(crash == 1):
		response = app.response_class(response=json.dumps({}), status=500, mimetype='application/json')
		return response

	global count
	count = count + 1
	data=request.get_json()
	cur.execute("SELECT COUNT(*) FROM acts WHERE actId=(%s)", data['actId'])
	n=cur.fetchone()[0]
	if(n!=0):
		print("actid not unique")
		response = app.response_class(response=json.dumps({}), status=400, mimetype='application/json')
		return response

	users=requests.get('http://3.214.116.189:80/api/v1/users').json()
	for i in users:
		print(i)
	if data['username'] in users:
		n=1
	else:
		n=0
	# cur.execute("SELECT COUNT(*) FROM users WHERE usn=(%s)", data['username'])
	# n=cur.fetchone()['COUNT(*)']
	if(n==0):
		print("user doesnt exist")
		response = app.response_class(response=json.dumps({}), status=400, mimetype='application/json')
		return response

	def isBase64(s):
		try:
			base64.urlsafe_b64decode(s)
			return True
		except binascii.Error:
			return False

	if(not isBase64(data['imgB64'])):
		print("not b64")
		response = app.response_class(response=json.dumps({}), status=400, mimetype='application/json')
		return response

	if(len(data)!=6):
		print("wrong no of parameters")
		response = app.response_class(response=json.dumps({}), status=400, mimetype='application/json')
		return response

	cur.execute("SELECT COUNT(*) FROM categories WHERE category=(%s)", data['categoryName'])
	n=cur.fetchone()[0]
	if(n==0):
		print("category doesnt exist")
		response = app.response_class(response=json.dumps({}), status=400, mimetype='application/json')
		return response

	d=(data['timestamp'][0:2])
	m=(data['timestamp'][3:5])
	y=(data['timestamp'][6:10])
	s=(data['timestamp'][11:13])
	mi=(data['timestamp'][14:16])
	h=(data['timestamp'][17:19])
	
	try:
		query = ("INSERT INTO acts VALUES (\"%s\",\"%s\",'%s-%s-%s %s:%s:%s',\"%s\",\"%s\",\"%s\",0)"%(data['actId'], data['username'],y,m,d,h,mi,s,data['caption'], data['categoryName'], data['imgB64']))
		cur.execute(query)
		con.commit()
		response = app.response_class(response=json.dumps({}), status=201, mimetype='application/json')
	except:
		print("some other error")
		response = app.response_class(response=json.dumps({}), status=400, mimetype='application/json')
	return response



@app.route("/api/v1/_count",methods = ['GET','DELETE'])
def http_count():
	global crash
	if(crash == 1):
		response = app.response_class(response=json.dumps({}), status=500, mimetype='application/json')
		return response
		
	global count
	print("\n\n\n",count,"\n\n\n")
	if request.method=='GET':
		l=[]
		l.append(count)
		return jsonify(l),200
		
	elif request.method=='DELETE':
		 
		count =0
		return jsonify({}),200
	else:
			return Response("{}",status=405,mimetype='application/json')


if __name__ == '__main__':
	app.run(host="0.0.0.0",port=80)
