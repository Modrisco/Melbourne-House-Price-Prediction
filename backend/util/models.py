from app import api
from flask_restplus import fields
from flask_restplus import abort
from flask import request

login_details = api.model('login_details', {
  'username': fields.String(required=True, example='xX_greginator_Xx'),
  'password': fields.String(required=True, example='1234'),
})

user_update_details = api.model('user_update_details', {
    'email': fields.String(example='greg@fred.com'),
    'name':  fields.String(example='greg'),
    'password': fields.String(example='1234')
})

signup_details = api.model('signup_details', {
  'username': fields.String(required=True, example='xX_greginator_Xx'),
  'password': fields.String(required=True, example='1234'),
  'email': fields.String(required=True, example='greg@fred.com'),
  'name':  fields.String(required=True, example='greg')
})

# Suburb,Address,Rooms,Type,Price,Method,SellerG,Date,Postcode,Regionname,Propertycount,Distance,CouncilArea
# Abbotsford,49 Lithgow St,3,h,1490000,S,Jellis,1/04/2017,3067,Northern Metropolitan,4019,3,Yarra City Council

house_details = api.model('house_details', {
  'Suburb': fields.String(required=True, example='0'),
  'Rooms': fields.String(required=True, example='3'),
  'Type': fields.String(required=True, example='0'),
  'Distance': fields.String(required=True, example='5'),
  'Car': fields.String(required=True, example='1'),
  'Building_Area': fields.String(required=True, example='100'),
  'Year': fields.String(required=True, example='2018'),
  })

def get_request_json():
    """Get the request body as a JSON object."""
    j = request.json
    if not j:
        abort(400, "Expected a JSON object. Make sure you've set the 'Content-Type' header to 'application/json'.")
    return j

def get_request_arg(arg, type=str, required=False, default=None):
    """Get the value of arg from request.args, converted it using `type`.
    
    - If arg is provided but could not be parsed by `type`, then a 400 error is thrown.
    - If requires is True and the arg is not provided, then a 400 error is thrown.
    - If required is False and the arg is not provided, then default is returned.
    """
    if arg not in request.args:
        if required:
            abort(400, "Expected '{}' query parameter".format(arg))
        else:
            return default
    else:
        try:
            return type(request.args[arg])
        except:
            abort(400, "Query parameter '{}' malformed".format(arg))

def unpack(j,*args,**kargs):
    if kargs.get("required",True):
        not_found = [arg for arg in args if arg not in j]
        if not_found:
            expected = ", ".join(map(str, not_found))
            abort(kargs.get("error",400), "Expected request object to contain: " + expected)
    return [j[arg] for arg in args]