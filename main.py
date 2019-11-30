#!/usr/bin/env python
# -*- coding: utf-8 -*-

import util
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_mysqldb import MySQL
import config as cfg
import datetime
import uuid

app = Flask(__name__)


app.config['MYSQL_HOST'] = cfg.mysql['host']
app.config['MYSQL_USER'] = cfg.mysql['user']
app.config['MYSQL_PASSWORD'] = cfg.mysql['passwd']
app.config['MYSQL_DB'] = cfg.mysql['db']

mysql = MySQL(app)

CORS(app)
container = ['Hello World!', 'Google', "SIMEN", "LARS"]

@app.route('/open/')
def openTest():
	return "This is an open endpoint"

@app.route('/closed/')
def closedTest():
	idToken = request.headers.get('idToken')
	decodedToken = util.verifyIdToken(idToken)
	if (decodedToken==None or decodedToken['iss'] != 'https://securetoken.google.com/fluent-webbing-257713'):
		return "NoAccess", 403
	else:
		return "yuhu, " + decodedToken['email'] + " you are logged in", 200
	

@app.route('/post/<word>')
def post(word):
	container.append(word)
	return jsonify(word)

@app.route('/delete/<number>')
def delete(number):
	if int(number) > len(container):
		return 'That number is greater than the size of the container'
	else:
		container.pop(int(number))
		return 'Success'


@app.route('/addthread/<header>')
def addthread(header):
	idToken = request.headers.get('idToken')
	decodedToken = util.verifyIdToken(idToken)
	if (decodedToken==None or decodedToken['iss'] != 'https://securetoken.google.com/fluent-webbing-257713'):
		return "NoAccess", 403
	else:
		now = datetime.datetime.now()
		uid = str(uuid.uuid4())
		str_now = now.date().isoformat()
		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO cloud_app.MessageThreads (uid, header, createdBy, createdAt) VALUES (%s, %s, %s, %s)", (uid, header, decodedToken['email'], str_now))
		mysql.connection.commit()
		cur.close()
		return 'success', 200

@app.route('/getthreads')
def get_threads():
	# idToken = request.headers.get('idToken')
	# decodedToken = util.verifyIdToken(idToken)
	# if (decodedToken==None or decodedToken['iss'] != 'https://securetoken.google.com/fluent-webbing-257713'):
	# 	return "NoAccess", 403
	# else:
	cur = mysql.connection.cursor()
	cur.execute("select * from cloud_app.MessageThreads;")
	row_headers=[x[0] for x in cur.description]
	rv = cur.fetchall()
	json_data=[]
	for result in rv:
		json_data.append(dict(zip(row_headers,result)))
	json = jsonify(json_data)
	print(json)
	cur.close()
	return json, 200




	

if __name__ == '__main__':
	app.run(debug=True)

