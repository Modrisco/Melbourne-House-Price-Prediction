from flask import Flask
from flask_restplus import Api

app = Flask(__name__)
app.config['ERROR_404_HELP'] = False
api = Api(app)