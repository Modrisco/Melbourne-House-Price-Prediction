import pymongo
from app import api
from flask import Flask, request
from flask_restplus import Resource, Api, fields, inputs, reqparse
from util.models import *

DB_NAME = 'comp9321'
DB_HOST = 'ds149960.mlab.com'
DB_PORT = 49960
DB_USER = 'admin'
DB_PASS = 'admin1'

# Build connection to the database 
connection = pymongo.MongoClient(DB_HOST, DB_PORT)
db = connection[DB_NAME]
db.authenticate(DB_USER, DB_PASS)

auth = api.namespace('auth', description='User Information Services')

@auth.route('/login', strict_slashes=False)
class Login(Resource):
	@auth.response(200, 'Success')
	@auth.response(400, 'Missing Username/Password')
	@auth.response(403, 'Invalid Username/Password')
	@auth.expect(login_details)
	def post(self):
		userlist = db.USERS
		j = get_request_json()
		(un,ps) = unpack(j,'username','password')
		collections = list(db.collection_names())
		for document in userlist.find():
			if document['username'] == un and document['password'] == ps:
				return 'successful', 200
		abort(403,'Invalid Username/Password')

@auth.route('/signup', strict_slashes=False)
class Signup(Resource):
	@auth.response(200, 'Success')
	@auth.response(400, 'Malformed Request')
	@auth.response(409, 'Username Taken')
	@api.expect(signup_details)
	@auth.doc(description='''
        Use this endpoint to create a new account,
        username must be unique and password must be non empty
    ''')
	def post(self):
		userlist = db.USERS
		j = get_request_json()
		(un,ps,em,n) = unpack(j,'username','password','email','name')
		signup_info = {
			'username': un,
			'password': ps,
			'email': em,
			'name': n
		}
		for document in userlist.find():
			if document['username'] == un:
				abort(409, 'Username Taken')
		if ps == '':
			abort(400, 'Password cannot be empty')

		userlist.insert_one(signup_info)
		return 'successful', 200