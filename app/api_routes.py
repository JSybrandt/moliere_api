from app import app

import json
import logging
import os
import re
import datetime
from app.cloud_wrapper import *

from flask import request, abort, jsonify

RW_KEY_PATH="keys/datastore-rw.key.json"
client = get_client(RW_KEY_PATH)


# Get results from an existing query
@app.route('/api/result', methods=['GET'])
def api_result():
    if 'query_id' in request.args:
        try:
            entity = get_from_id(client, request.args.get('query_id'))
            if entity:
                return jsonify(entity)
        except:
            pass
    abort(404)


# Submit a new query using POST
@app.route('/api/query',  methods=['POST'])
def api_query():
    keywords = request.form.get('keywords')
    keywords = keywords.strip().split(',')
    num_topics = request.form.get('num_topics')
    cloud_size = request.form.get('cloud_size')
    email = None
    if 'email' in request.form:
        email = request.form.get('email')
    obj = enqueue(client, keywords, num_topics, cloud_size, email)
    return jsonify({"query_id": str(obj.key.id)})
