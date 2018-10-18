import pymongo
from app import api
from flask import Flask, request
from flask_restplus import Resource, Api, fields, inputs, reqparse
from util.models import *

house = api.namespace('house', description='User Information Services')

@house.route('/data', strict_slashes=False)
class House(Resource):
	@house.response(200, 'Success')
	@house.response(400, 'Missing parameters')
	@house.expect(house_details)
	def post(self):
		return 200