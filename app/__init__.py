from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

CORS(app, resources={r'/api/*': {"origins": "*"}})

from app import cloud_wrapper
RW_KEY_PATH="keys/datastore-rw.key.json"
client = cloud_wrapper.get_client(RW_KEY_PATH)

from app import routes
from app import api_routes


# READ : https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-ii-templates

