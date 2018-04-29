import logging
from flask import Flask

# This obj is what the API will call
app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/query')
def query():
    return 'Hey, its a query!'


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occured during a request.')
    return """
    An internal error occured: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500
