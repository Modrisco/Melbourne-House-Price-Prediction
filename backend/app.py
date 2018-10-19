from flask import Flask
from flask_restplus import Api
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['ERROR_404_HELP'] = False
api = Api(app)