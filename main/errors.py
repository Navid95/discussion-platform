from discussion import app
from flask import request, jsonify

from main.configuration.log_utils import init_logger
import logging

init_logger(__name__)
logger = logging.getLogger(__name__)


@app.errorhandler(404)
def page_not_found(e):
    response = jsonify({'error': 'not found'})
    response.status_code = 404
    return response


@app.errorhandler(500)
def internal_server_error(e):
    response = jsonify({'error': 'internal server error'})
    response.status_code = 500
    return response


def forbidden(message):
    response = jsonify({'error': 'forbidden', 'message': message})
    response.status_code = 403
    return response


@app.errorhandler(401)
def unauthorized(e):
    logger.debug(f'unauthorized access')
    response = jsonify({'error': 'unauthorized access'})
    request.status_code = 401
    return response


@app.errorhandler(400)
def page_not_found(e):
    response = jsonify({'error': 'Bad Request'})
    response.status_code = 400
    return response
