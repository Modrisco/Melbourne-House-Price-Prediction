import pymongo
from app import api
from flask import Flask, request
from flask_restplus import Resource, Api, fields, inputs, reqparse
from util.models import *
from ml.app_predict import *


house = api.namespace('house', description='User Information Services')

@house.route('/data', strict_slashes=False)
class House(Resource):
	@house.response(200, 'Success')
	@house.response(400, 'Missing parameters')
	@house.expect(house_details)
	def post(self):
		j = get_request_json()
		(sb,rm,tp,dis,car,ba,y) = unpack(j,'Suburb','Rooms','Type','Distance','Car','Building_Area','Year')
		data_array = [sb,rm,tp,dis,car,ba,y]
		for i in range(len(data_array)):
			data_array[i] = int(data_array[i])
		result = predict(data_array)
		price_result = {'price': result}
		return price_result, 200