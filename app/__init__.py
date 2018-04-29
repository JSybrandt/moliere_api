from flask import Flask

app = Flask(__name__)

from app import routes
from app import cloud_wrapper
# READ : https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-ii-templates

