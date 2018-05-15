from app import app

import logging

from flask import render_template, abort


# Show Demo Page For API
@app.route('/')
@app.route('/index')
def main_form():
    return render_template('query_submission_form.html')


# Get results from an existing query
@app.route('/result')
def result():
    return render_template('result_request_form.html')


# Submit a new query using POST
@app.route('/query')
def query():
    return render_template('query_submission_form.html')

@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occured during a request.')
    return """
    An internal error occured: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500
