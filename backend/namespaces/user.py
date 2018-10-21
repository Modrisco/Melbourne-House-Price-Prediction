import pymongo
from app import api, AuthenticationToken
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


SECRET_KEY = 'Abracadabra'
expires_in = 600
get_auth = AuthenticationToken(SECRET_KEY, expires_in)


auth = api.namespace('auth', description='User Information Services')


@auth.route('/login', strict_slashes=False)
class Login(Resource):
	@auth.response(200, 'Success')
	@auth.response(400, 'Missing Username/Password')
	@auth.response(403, 'Invalid Username/Password')
	@auth.expect(login_details)
	@auth.doc(description='''
		Use this endpoint to login, username and password must be matched in the database.
		Once login successfully, return a token could be used for 10 minutes for user.
	''')
	def post(self):
		userlist = db.USERS
		j = get_request_json()
		(un, ps) = unpack(j, 'username', 'password')
		for document in userlist.find():
			if document['username'] == un and document['password'] == ps:
				em = document['email']
				n = document['name']
				return {
					"username": un,
					'name': n,
					'email': em,
					"token": get_auth.generate_token(un)
				}
		abort(403, 'Invalid Username/Password')




@auth.route('/signup', strict_slashes=False)
class Signup(Resource):
	@auth.response(200, 'Success')
	@auth.response(400, 'Malformed Request')
	@auth.response(409, 'Username Taken')
	@api.expect(signup_details)
	@auth.doc(description='''
		Use this endpoint to create a new account, 
		username must be unique and password must be non empty. 
		Once signup successfully, return a token could be used for 10 minutes for user.
	''')
	def post(self):
		userlist = db.USERS
		j = get_request_json()
		(un, ps, em, n) = unpack(j, 'username', 'password', 'email', 'name')
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
		return {
			'username': un,
			'name': n,
			'email': em,
			'token': get_auth.generate_token(un)
		}

@auth.route('/update', strict_slashes=False)
class Update(Resource):
	@auth.response(200, 'Success')
	@auth.response(400, 'Malformed Request')
	@auth.response(409, 'No changes')
	@api.expect(user_update_details)
	@auth.doc(description='''
		Use this endpoint to change the password. 
	''')
	def put(self):
		userlist = db.USERS
		j = get_request_json()
		(un, ps, np) = unpack(j, 'username', 'password', 'new_password')
		if ps == np:
			abort(409, 'Password has not be changed')
		if ps == '' or np == '':
			abort(400, 'Password cannot be empty')
		for document in userlist.find():
			if document['username'] == un and document['password'] == ps:
				new_password_item = {'password': np}
				userlist.update_one(document, {'$set': new_password_item})

		return 'password changed successfully'


@auth.route('/destroy', strict_slashes=False)
class Destroy(Resource):
	@auth.response(200, 'Success')
	@auth.response(400, 'Missing Username/Password')
	@auth.response(403, 'Invalid Username/Password')
	@auth.expect(login_details)
	@auth.doc(description='''
		Use this endpoint to destroy the user's information if user doesn't need the service,
		delete the user's information in database
	''')
	def delete(self):
		userlist = db.USERS
		j = get_request_json()
		(un, ps) = unpack(j, 'username', 'password')
		for document in userlist.find():
			if document['username'] == un and document['password'] == ps:
				userlist.delete_one(document)
				return 'account destroyed successfully'
		abort(403, 'Invalid Username/Password')

@auth.route('/token', strict_slashes=False)
@auth.param('username', 'The username when a user signup and login uses')
class GetNewToken(Resource):
	@auth.response(200, 'Success')
	@auth.response(400, 'Malformed Request')
	@auth.doc(description='''
		Use this endpoint to create a new valid token for user after login. 
	''')
	def get(self):
		username = get_request_arg('username', str, required=True)
		userlist = db.USERS
		for document in userlist.find():
			if document['username'] == username:
				return {
					'username': username,
					'token': get_auth.generate_token(username)
				}
		abort(400, 'Invalid username')
