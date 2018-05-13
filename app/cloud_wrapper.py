# This is a lib file

import json
import logging
import os
import re
import datetime
from google.cloud import datastore

QUERY_STATUSES = ['queued', 'running', 'error', 'done']
QUERY_KIND = 'query'

EMAIL_RE = re.compile(r'[^@]+@[^@]+\.[^@]+')


def get_proj_id():
    key = "PROJ_ID"
    if key in os.environ:
        return os.environ[key]
    else:
        raise RuntimeError("Env Var " + key + " not set.")


def get_rw_key_path():
    key = "RW_KEY_PATH"
    if key in os.environ:
        return os.environ[key]
    else:
        raise RuntimeError("Env Var " + key + " not set.")


def iter_query_with_status(client, status):
    "returns an iterator for queries having a given status"
    query = client.query(kind=QUERY_KIND)
    query.add_filter('status', '=', status)
    return query.fetch()


def get_client(cred_path):
    "Gets client from credential"
    return datastore.Client.from_service_account_json(cred_path)


def enqueue(client, query_words, num_topics, cloud_size, email):
    "Posts a query that doesn't already exist"

    # is good query
    if len(query_words) < 2:
        raise ValueError("Must supply at least two keywords.")
    if int(cloud_size) <= 0:
        raise ValueError("Cloud-size must be a positive number")
    if int(num_topics) <= 0:
        raise ValueError("Num-topics must be a positive number")
    if email and not EMAIL_RE.match(email):
        raise ValueError("Invalid Email")
    keyword_string = ','.join(query_words)

    with client.transaction():
        incomplete_key = client.key(QUERY_KIND)
        new_q = datastore.Entity(key=incomplete_key)
        new_q.update({
            'cloud_size': int(cloud_size),
            'keywords': keyword_string,
            'status': QUERY_STATUSES[0],
            'num_topics': int(num_topics),
            'created': datetime.datetime.utcnow(),
            'modified': datetime.datetime.utcnow(),
        })
        if email:
            new_q.update({
                'email': email
            })
        client.put(new_q)

    return new_q


def get_entity(client, query_words, num_topics):
    query = client.query(kind=QUERY_KIND)
    query.add_filter('keywords', '=', ",".join(query_words))
    query.add_filter('num_topics', '=', num_topics)
    res = list(query.fetch())
    if len(res) == 0:
        return None
    return res[0]



def exists(client, query_words, num_topics):
    return get_entity(client, query_words, num_topics) is not None

