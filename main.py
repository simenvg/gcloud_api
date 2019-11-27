#!/usr/bin/env python
# -*- coding: utf-8 -*-

import util
from flask import Flask, jsonify, request
from flask_cors import CORS


app = Flask(__name__)
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

if __name__ == '__main__':
	app.run(debug=True)

