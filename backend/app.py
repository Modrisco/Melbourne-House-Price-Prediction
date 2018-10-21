from flask import Flask
from flask_restplus import Api
from flask_cors import CORS
from time import time
from itsdangerous import SignatureExpired, JSONWebSignatureSerializer, BadSignature


class AuthenticationToken:
    def __init__(self, secret_key, expires_in):
        self.secret_key = secret_key
        self.expires_in = expires_in
        self.serializer = JSONWebSignatureSerializer(secret_key)

    def generate_token(self, username):
        info = {
            'username': username,
            'creation_time': time()
        }

        token = self.serializer.dumps(info)
        return token.decode()

    def validate_token(self, token):
        info = self.serializer.loads(token.encode())

        if time() - info['creation_time'] > self.expires_in:
            raise SignatureExpired("The Token has been expired, please get a new token")

        return 1


app = Flask(__name__)
CORS(app)
app.config['ERROR_404_HELP'] = False
api = Api(app,
          title="Melbourne House Market Prediction API",
          description="This is an api designed to connect the service front-end and machine learning model")
api.namespaces.clear()