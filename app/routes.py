from app import app
from app import client

import logging

from flask import render_template, abort

from app.cloud_wrapper import get_compute_status

# Put path / name in order here
# All rendered pages need this and an "active_path" to select one.
nav_data = [
    ("/index", "Home"),
    ("/query", "Submit A Query"),
    ("/result", "View Results")
]


def render_base_ext(tempate_file, **args):
    if 'active_path' not in args:
        args['active_path'] = "/" + tempate_file.split('.')[0]
    if 'nav_data' not in args:
        args['nav_data'] = nav_data
    if 'comp_status' not in args:
        args['comp_status'] = get_compute_status(client)
    return render_template(tempate_file, **args)

@app.route('/')
@app.route('/index')
def main_form():
    return render_base_ext('index.html')


# Get results from an existing query
@app.route('/result')
def result():
    return render_base_ext('result_request_form.html', active_path="/result")


# Submit a new query using POST
@app.route('/query')
def query():
    return render_base_ext('query_submission_form.html', active_path='/query')

@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occured during a request.')
    return """
    An internal error occured: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500
