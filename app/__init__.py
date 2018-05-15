from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

CORS(app, resources={r'/api/*': {"origins": "*"}})

from app import routes
from app import cloud_wrapper
# READ : https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-ii-templates

