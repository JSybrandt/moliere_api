from app import app

import json
import logging
import os
import re
import datetime
from cloud_wrapper import *

from flask import request, render_template

import urllib


RW_KEY_PATH="keys/datastore-rw.key.json"
client = get_client(RW_KEY_PATH)


@app.route('/')
@app.route('/index')
def main_form():
    return render_template('query_submission_form.html')

@app.route('/result')
def results():
    """
    Returns status object
    Returns N/A if doesn't exist
    args:
        keywords = comma-sep keyword list
        num_topics = positive # of topics
    """
    keywords = request.args.get('keywords')
    keywords = keywords.strip().split(',')
    num_topics = int(request.args.get('num_topics'))

    if exists(client, keywords, num_topics):
        ent = get_entity(client, keywords, num_topics)
        if ent['status'] == QUERY_STATUSES[-1]:
            return ent['result']
        else:
            return ent['status']
    else:
        return "N/A"


@app.route('/query')
def query():

    keywords = request.args.get('keywords')
    keywords = urllib.unquote(keywords).decode('utf8') 
    keywords = keywords.strip().split(',')
    num_topics = request.args.get('num_topics')
    cloud_size = request.args.get('cloud_size')
    email = None
    if 'email' in request.args:
        email = request.args.get('email')

    if exists(client, keywords, num_topics):
        return QUERY_STATUSES[-1]
    else:
        enqueue(client, keywords, num_topics, cloud_size, email)
        return QUERY_STATUSES[0]

@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occured during a request.')
    return """
    An internal error occured: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500
