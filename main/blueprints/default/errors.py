from flask import request, jsonify
from main.utilities import app_logger, exception_logger
from main.blueprints.default import default

# TODO add all general http errors
# TODO add custom result code, messages


@default.app_errorhandler(404)
def page_not_found(e):
    response = jsonify({'error': 'not found'})
    response.status_code = 404
    return response, 404


@default.app_errorhandler(500)
def internal_server_error(e):
    response = jsonify({'error': 'internal server error'})
    response.status_code = 500
    return response


def forbidden(message):
    response = jsonify({'error': 'forbidden', 'message': message})
    response.status_code = 403
    return response


@default.app_errorhandler(401)
def unauthorized(e):
    response = jsonify({'error': '401 Unauthorized Access'})
    app_logger.error(e)
    app_logger.error(response)
    # request.status_code = 401
    # response.content_type = "application/json"
    return response


@default.app_errorhandler(400)
def page_not_found(e):
    response = jsonify({'error': 'Bad Request'})
    response.status_code = 400
    return response


def error(status_code, message):
    response = jsonify({"status_code": status_code,"error": message})
    response.status_code = status_code
    return response
