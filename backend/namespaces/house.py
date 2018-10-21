from app import api, AuthenticationToken
from flask import Flask, request
from flask_restplus import Resource, Api, fields, inputs, reqparse
from itsdangerous import SignatureExpired, JSONWebSignatureSerializer, BadSignature
from util.models import *
from ml.app_predict import *
import random
import json

suburb_collection = {0: "Abbotsford", 1: "Airport West", 2: "Albert Park", 3: "Alphington", 4: "Altona", 5: "Altona North", 6: "Armadale", 7: "Ascot Vale", 8: "Ashburton", 9: "Ashwood", 10: "Avondale Heights", 11: "Balaclava", 12: "Balwyn", 13: "Balwyn North", 14: "Bentleigh", 15: "Bentleigh East", 16: "Box Hill", 17: "Braybrook", 18: "Brighton", 19: "Brighton East", 20: "Brunswick", 21: "Brunswick West", 22: "Bulleen", 23: "Burwood", 24: "Camberwell", 25: "Canterbury", 26: "Carlton North", 27: "Carnegie", 28: "Caulfield", 29: "Caulfield North", 30: "Caulfield South", 31: "Chadstone", 32: "Clifton Hill", 33: "Coburg", 34: "Coburg North", 35: "Collingwood", 36: "Doncaster", 37: "Eaglemont", 38: "Elsternwick", 39: "Elwood", 40: "Essendon", 41: "Essendon North", 42: "Fairfield", 43: "Fitzroy", 44: "Fitzroy North", 45: "Flemington", 46: "Footscray", 47: "Glen Iris", 48: "Glenroy", 49: "Gowanbrae", 50: "Hadfield", 51: "Hampton", 52: "Hampton East", 53: "Hawthorn", 54: "Heidelberg Heights", 55: "Heidelberg West", 56: "Hughesdale", 57: "Ivanhoe", 58: "Kealba", 59: "Keilor East", 60: "Kensington", 61: "Kew", 62: "Kew East", 63: "Kooyong", 64: "Maidstone", 65: "Malvern", 66: "Malvern East", 67: "Maribyrnong", 68: "Melbourne", 69: "Middle Park", 70: "Mont Albert", 71: "Moonee Ponds", 72: "Moorabbin", 73: "Newport", 74: "Niddrie", 75: "North Melbourne", 76: "Northcote", 77: "Oak Park", 78: "Oakleigh South", 79: "Parkville", 80: "Pascoe Vale", 81: "Port Melbourne", 82: "Prahran", 83: "Preston", 84: "Reservoir", 85: "Richmond", 86: "Rosanna", 87: "Seddon", 88: "South Melbourne", 89: "South Yarra", 90: "Southbank", 91: "Spotswood", 92: "St Kilda", 93: "Strathmore", 94: "Sunshine", 95: "Sunshine North", 96: "Sunshine West", 97: "Surrey Hills", 98: "Templestowe Lower", 99: "Thornbury", 100: "Toorak", 101: "Viewbank", 102: "Watsonia", 103: "West Melbourne", 104: "Williamstown", 105: "Williamstown North", 106: "Windsor", 107: "Yallambie", 108: "Yarraville", 109: "Aberfeldie", 110: "Bellfield", 111: "Brunswick East", 112: "Burnley", 113: "Campbellfield", 114: "Carlton", 115: "East Melbourne", 116: "Essendon West", 117: "Fawkner", 118: "Hawthorn East", 119: "Heidelberg", 120: "Ivanhoe East", 121: "Jacana", 122: "Kingsbury", 123: "Kingsville", 124: "Murrumbeena", 125: "Ormond", 126: "West Footscray", 127: "Albion", 128: "Brooklyn", 129: "Glen Huntly", 130: "Oakleigh", 131: "Ripponlea", 132: "Cremorne", 133: "Docklands", 134: "South Kingsville", 135: "Strathmore Heights", 136: "Travancore", 137: "Caulfield East", 138: "Seaholme", 139: "Keilor Park", 140: "Gardenvale", 141: "Princes Hill", 142: "Altona Meadows", 143: "Ardeer", 144: "Attwood", 145: "Bayswater", 146: "Bayswater North", 147: "Beaumaris", 148: "Berwick", 149: "Blackburn", 150: "Blackburn South", 151: "Boronia", 152: "Briar Hill", 153: "Broadmeadows", 154: "Bundoora", 155: "Burnside Heights", 156: "Burwood East", 157: "Cairnlea", 158: "Caroline Springs", 159: "Cheltenham", 160: "Clarinda", 161: "Clayton", 162: "Clyde North", 163: "Craigieburn", 164: "Cranbourne", 165: "Croydon", 166: "Croydon Hills", 167: "Croydon North", 168: "Dandenong", 169: "Dandenong North", 170: "Diamond Creek", 171: "Dingley Village", 172: "Doncaster East", 173: "Donvale", 174: "Doreen", 175: "Edithvale", 176: "Eltham", 177: "Eltham North", 178: "Emerald", 179: "Epping", 180: "Eumemmerring", 181: "Ferntree Gully", 182: "Forest Hill", 183: "Frankston", 184: "Frankston North", 185: "Frankston South", 186: "Gisborne", 187: "Gladstone Park", 188: "Glen Waverley", 189: "Greensborough", 190: "Greenvale", 191: "Hallam", 192: "Healesville", 193: "Heathmont", 194: "Highett", 195: "Hillside", 196: "Hoppers Crossing", 197: "Huntingdale", 198: "Keilor Downs", 199: "Keilor Lodge", 200: "Keysborough", 201: "Kings Park", 202: "Lalor", 203: "Lower Plenty", 204: "Lynbrook", 205: "MacLeod", 206: "Melton", 207: "Melton South", 208: "Melton West", 209: "Mentone", 210: "Mernda", 211: "Mickleham", 212: "Mill Park", 213: "Mitcham", 214: "Montmorency", 215: "Montrose", 216: "Mordialloc", 217: "Mount Waverley", 218: "Mulgrave", 219: "Narre Warren", 220: "Noble Park", 221: "Nunawading", 222: "Oakleigh East", 223: "Parkdale", 224: "Point Cook", 225: "Ringwood", 226: "Ringwood East", 227: "Rockbank", 228: "Rowville", 229: "Roxburgh Park", 230: "Sandringham", 231: "Seabrook", 232: "Seaford", 233: "Skye", 234: "South Morang", 235: "Springvale", 236: "Springvale South", 237: "St Albans", 238: "St Helena", 239: "Sunbury", 240: "Sydenham", 241: "Tarneit", 242: "Taylors Hill", 243: "Taylors Lakes", 244: "Tecoma", 245: "Templestowe", 246: "The Basin", 247: "Thomastown", 248: "Truganina", 249: "Tullamarine", 250: "Vermont", 251: "Vermont South", 252: "Wantirna", 253: "Wantirna South", 254: "Werribee", 255: "Werribee South", 256: "Westmeadows", 257: "Williams Landing", 258: "Wollert", 259: "Wyndham Vale", 260: "Aspendale", 261: "Black Rock", 262: "Blackburn North", 263: "Bonbeach", 264: "Carrum", 265: "Chelsea", 266: "Clayton South", 267: "Dallas", 268: "Delahey", 269: "Doveton", 270: "McKinnon", 271: "Mooroolbark", 272: "Pakenham", 273: "Ringwood North", 274: "Scoresby", 275: "Warrandyte", 276: "Watsonia North", 277: "Wattle Glen", 278: "Wheelers Hill", 279: "Albanvale", 280: "Aspendale Gardens", 281: "Belgrave", 282: "Carrum Downs", 283: "Cranbourne East", 284: "Cranbourne North", 285: "Deer Park", 286: "Heatherton", 287: "Kilsyth", 288: "Langwarrin", 289: "Notting Hill", 290: "Patterson Lakes", 291: "Riddells Creek", 292: "Beaconsfield Upper", 293: "Chelsea Heights", 294: "Chirnside Park", 295: "Coolaroo", 296: "Darley", 297: "Hampton Park", 298: "Keilor", 299: "Meadow Heights", 300: "Mount Evelyn", 301: "North Warrandyte", 302: "Sandhurst", 303: "Silvan", 304: "Wallan", 305: "Croydon South", 306: "Derrimut", 307: "Diggers Rest", 308: "Knoxfield", 309: "Upwey", 310: "Warranwood", 311: "Bacchus Marsh", 312: "Bullengarook", 313: "Deepdene", 314: "Hurstbridge", 315: "Kurunjang", 316: "Laverton", 317: "Lilydale", 318: "Wonga Park", 319: "Endeavour Hills", 320: "Officer", 321: "Olinda", 322: "Waterways", 323: "Beaconsfield", 324: "Yarra Glen", 325: "Brookfield", 326: "Lysterfield", 327: "Plenty", 328: "Whittlesea", 329: "Burnside", 330: "New Gisborne", 331: "Guys Hill", 332: "Plumpton", 333: "Monbulk", 334: "Avonsleigh", 335: "Wildwood", 336: "Gisborne South", 337: "Research", 338: "Botanic Ridge", 339: "Bulla", 340: "Coldstream", 341: "Hopetoun Park", 342: "Cranbourne West", 343: "Eynesbury", 344: "Fawkner Lot", 345: "Ferny Creek", 346: "Wandin North", 347: "Kalkallo", 348: "Menzies Creek"}
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
		suburb_name = suburb_collection[data_array[0]]
		price_result = {
			'suburb': suburb_name,
			'price': result
		}
		return price_result

@house.route('/random_suburbs', strict_slashes=False)
class House(Resource):
	@house.response(200, 'Success')
	@house.response(400, 'Invalid/Missing parameters')
	@house.response(401, 'Invalid/Missing token')
	@house.expect(house_details)
	@house.doc(description='''
			Choose five random suburbs to see how's the price of house with same conditions in different area 
		''')
	def post(self):
		j = get_request_json()
		(tk, sb, rm, tp, dis, car, ba, y) = unpack(j, 'Token', 'Suburb', 'Rooms', 'Type', 'Distance', 'Car', 'Building_Area', 'Year')
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
		data_array = [sb, rm, tp, dis, car, ba, y]
		random_suburbs = []
		random_prices = {}
		for i in range(len(data_array)):
			try:
				int(data_array[i])
			except:
				abort(400, 'Wrong input type')
			data_array[i] = int(data_array[i])
			if data_array[i] < 0:
				abort(400, 'Invalid input')

		while len(set(random_suburbs)) < 5:
			another_suburb = random.randint(0, 348)
			random_suburbs.append(another_suburb)

		for i in range(len(random_suburbs)):
			data_array[0] = random_suburbs[i]
			price = predict(data_array)
			price_result = {suburb_collection[random_suburbs[i]]: price}
			random_prices.update(price_result)
		return random_prices
