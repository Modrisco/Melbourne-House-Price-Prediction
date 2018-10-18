import pymongo
from app import api
from flask import Flask, request
from flask_restplus import Resource, Api, fields, inputs, reqparse

DB_NAME = 'comp9321'
DB_HOST = 'ds149960.mlab.com'
DB_PORT = 49960
DB_USER = 'admin'
DB_PASS = 'admin1'

# Build connection to the database 
connection = pymongo.MongoClient(DB_HOST, DB_PORT)
db = connection[DB_NAME]
db.authenticate(DB_USER, DB_PASS)

user = api.namespace('user', description='User Information Services')

@user.route('/', strict_slashes=False)
class User(Resource):

	def get(self):
		get_info = 'hello'
		collections = list(db.collection_names())
		return collections[1], 200