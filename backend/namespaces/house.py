from app import api, AuthenticationToken
from flask import Flask, request
from flask_restplus import Resource, Api, fields, inputs, reqparse
from itsdangerous import SignatureExpired, JSONWebSignatureSerializer, BadSignature
from util.models import *
from ml.app_predict import *


SECRET_KEY = 'Abracadabra'
expires_in = 600
get_auth = AuthenticationToken(SECRET_KEY, expires_in)

house = api.namespace('house', description='house price prediction')


@house.route('/data', strict_slashes=False)
class House(Resource):
	@house.response(200, 'Success')
	@house.response(400, 'Invalid/Missing parameters')
	@house.response(401, 'Invalid/Missing token')
	@house.expect(house_details)
	@house.doc(description='''
			Use this endpoint to get the prediction of price with the features given by user,
			a valid token should also be provided to keep the stability of the API 
		''')
	def post(self):
		j = get_request_json()
		(tk,sb,rm,tp,dis,car,ba,y) = unpack(j,'Token','Suburb','Rooms','Type','Distance','Car','Building_Area','Year')
		if not tk:
			abort(401, 'token is missing')
		try:
			isValid = get_auth.validate_token(tk)
		except SignatureExpired as e:
			abort(401, e.message)
		except BadSignature as e:
			abort(401, e.message)

		if isValid != 1:
			abort(401, 'token not valid')
		data_array = [sb,rm,tp,dis,car,ba,y]
		for i in range(len(data_array)):
			try:
				int(data_array[i])
			except:
				abort(400, 'Wrong input type')
			data_array[i] = int(data_array[i])
			if data_array[i] < 0:
				abort(400, 'Invalid input')
		result = predict(data_array)
		price_result = {'price': result}
		return price_result