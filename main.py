#!/usr/bin/env python
# -*- coding: utf-8 -*-


from flask import Flask, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
container = ['Hello World!', 'Google']

@app.route('/mainpage/')
def mainpage():
	return jsonify(container)

@app.route('/get/<number>')
def get(number):
	if int(number) > len(container):
		return 'That number is greater than the size of the container'
	else:
		return jsonify(container[int(number)])

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

