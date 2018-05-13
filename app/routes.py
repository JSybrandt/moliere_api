from app import app

import json
import logging
import os
import re
import datetime
from app.cloud_wrapper import *

from flask import request, render_template

import urllib


RW_KEY_PATH="keys/datastore-rw.key.json"
client = get_client(RW_KEY_PATH)


# Show Demo Page For API
@app.route('/')
@app.route('/index')
def main_form():
    return render_template('query_submission_form.html')


# Get results from an existing query
@app.route('/result', methods=['GET'])
def results():

    if 'keywords' in request.args and 'num_topics' in request.args:
        keywords = request.args.get('keywords')
        num_topics = int(request.args.get('num_topics'))
        keywords = keywords.strip().split(',')
        app.logger.warning("Result:", keywords, type(keywords))

        if exists(client, keywords, num_topics):
            ent = get_entity(client, keywords, num_topics)
            return json.dumps(ent, indent=4, sort_keys=True, default=str)
    else:
        return render_template('result_request_form.html')


# Submit a new query using POST
@app.route('/query', methods=['GET', 'POST'])
def query():
    if request.method == 'POST':
        keywords = request.form.get('keywords')
        app.logger.warning("Received: ", keywords)
        # keywords = urllib.unquote(keywords).decode('utf8') 
        keywords = keywords.strip().split(',')
        num_topics = request.form.get('num_topics')
        cloud_size = request.form.get('cloud_size')
        email = None
        if 'email' in request.form:
            email = request.form.get('email')
        if exists(client, keywords, num_topics):
            return QUERY_STATUSES[-1]
        else:
            val = enqueue(client, keywords, num_topics, cloud_size, email)
            return json.dumps(val, default=str)
    else:
        return render_template('query_submission_form.html')

@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occured during a request.')
    return """
    An internal error occured: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500
