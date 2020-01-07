from flask import Flask, request, jsonify,json
import pymysql
import datetime
import base64
import binascii

app = Flask(__name__)
con=pymysql.connect(host="mysql-serv", user="root", password="root", db="selfielessacts",cursorclass=pymysql.cursors.DictCursor)
cur=con.cursor()

count =0



# 1. Function to add user
@app.route('/api/v1/users', methods=['POST'])
def add_user():
    global count
    count = count + 1
    data=request.get_json()
    usn=data['username']
    pwd=data['password']
    def is_sha1(pwd_str):
    	if len(pwd_str) != 40:
    		return False
    	try:
    		sha_int = int(pwd_str, 16)
    	except ValueError:
    		return False
    	return True
    cur.execute("SELECT COUNT(*) FROM users WHERE usn=%s", usn)
    n=cur.fetchone()['COUNT(*)']
    if(is_sha1(pwd) and n==0):
    	query = ("INSERT INTO users VALUES (%s, %s)")
    	input_data=(usn, pwd)
    	cur.execute(query, input_data)
    	con.commit()
    	response = app.response_class(response=json.dumps({}),status=201,mimetype='application/json')
    elif(n!=0 or not(is_sha1(pwd))):
    	response = app.response_class(response=json.dumps({}), status=400, mimetype='application/json')
    return response
     







# 2.Function to remove a user
@app.route('/api/v1/users/<usn>', methods=['DELETE'])
def rem_user(usn):
    global count
    count = count + 1
    cur.execute("SELECT COUNT(*) FROM users WHERE usn=%s", usn)
    n=cur.fetchone()['COUNT(*)']
    if(n==0):
    	response = app.response_class(response=json.dumps({}),status=400,mimetype='application/json')
    else:
    	cur.execute("DELETE FROM users WHERE usn=%s", usn)
    	response = app.response_class(response=json.dumps({}),status=200,mimetype='application/json')
    	con.commit()
    return response


#List all users
@app.route('/api/v1/users', methods=['GET'])
def list_users():
    global count
    count = count + 1
    cur.execute("SELECT COUNT(*) FROM users")
    n=cur.fetchone()['COUNT(*)']
    if(n==0):
        response=app.response_class(response=json.dumps({}), status=204, mimetype='application/json')
        return response
    cur.execute("SELECT usn FROM users")
    ret=list()
    json_list=list()
    ret=cur.fetchall()
    for i in ret:
        json_list.append(i["usn"])
    response=app.response_class(response=json.dumps(json_list), status=200, mimetype='application/json')
    return response




@app.route("/api/v1/_count",methods = ['GET','DELETE'])
def http_count():
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
