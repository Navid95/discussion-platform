# print(f'-------------------------------------{__name__}-------------------------------------')

from flask import request, abort, Response, g, jsonify
from datetime import datetime
from main.models import User
from main.schemas import UserSchema
import main.authentication.basic_http as basic_http
from . import user_blueprint, decorators

from main.configuration.log_utils import init_logger
import logging

init_logger(__name__)
logger = logging.getLogger(__name__)

api = user_blueprint
schema = UserSchema()
auth = basic_http.auth
owner_required = basic_http.user_owner_required
dump_user = decorators.dump_user
load_user = decorators.load_user

"""
CRUD APIs
"""


# TODO implement marshmallow dump and load as decorators? or hooks?


@api.route('/<id>', methods=['GET'])
@auth.login_required
@owner_required
@dump_user
def get_by_id(id):
    return User.get(id=id)


@api.route('/', methods=['POST'])
@load_user
@dump_user
def create_user():
    json_raw = request.get_json()
    new_user = schema.load(json_raw)
    result = User.persist(new_user)
    if result:
        return new_user
    else:
        abort(400)


@api.route('/<id>', methods=['PUT', 'PATCH'])
@auth.login_required
@owner_required
@dump_user
def update_user(id):
    json_raw = request.get_json()
    new_user = schema.load(json_raw)
    g.current_user.email = new_user.email
    g.current_user.password_hash = new_user.password_hash
    result = User.update(g.current_user)
    if result:
        return g.current_user
    else:
        abort(400)


@api.route('/<id>', methods=['DELETE'])
@auth.login_required
@load_user
def delete_user(id):
    if User.delete(id):
        return jsonify({'status': 200, 'message': 'successful'})


"""
business logic APIs
"""


@api.route('/', methods=['GET'])
def search_user(id):
    """
    Search API with URI string filters
    :param id:
    :return:
    """
    pass


"""
before after hooks
"""


@api.before_request
def before_request():
    request_start = datetime.utcnow()
    g.request_start = request_start
    logger.debug(f'before_request for request: {request}')


@api.after_request
def after_request(response: Response):
    logger.debug(f'after request for response: {response}')
    logger.info(f'[status: {response.status_code}, '
                f'method: {request.method}, '
                f'request: {request.get_data()}, '
                f'response: {response.response}, '
                f'starttime: {g.request_start}, '
                f'endtime: {datetime.utcnow()}]')
    return response
