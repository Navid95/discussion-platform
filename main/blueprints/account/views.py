# print(f'-------------------------------------{__name__}-------------------------------------')

from flask import request, abort, Response, g, jsonify
from main.models import User
from main.schemas import UserSchema, LoginSchema
from main.authentication import basic_http, token_auth
from . import user_blueprint, decorators
from extensions import redis_client


api = user_blueprint
schema = UserSchema()
login_schema = LoginSchema()
auth = basic_http.auth
owner_required = basic_http.user_owner_required
dump_user = decorators.dump_user
load_user = decorators.load_user

"""
CRUD APIs
"""


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


@api.route('/login', methods=['GET'])
@auth.login_required
def login():
    """
    Receives email/pass and if it's validated returns token specific with that user account.

    user can use the token for further access to the system. Consecutive hits replaces the
    token with a new one with a new expiry of 5 hours

    :return: user's authorization token, if token authentication is used returns a message to user (no token is generated)
    """
    if g.token_auth:
        return jsonify({'message': 'you are already using a token, use basic authentication to receive a new token.'})

    return jsonify({'email': g.current_user.email, 'token': token_auth.login(g.current_user)})


@api.route('/logout', methods=['GET'])
@auth.login_required
def logout():
    """
    logs out the user if it is using token authentication (token gets removed and will not be valid anymore)

    :return: result, if token authentication is not used returns a message to user (no token is removed)
    """
    if not g.token_auth:
        return jsonify({'message': 'you are not logged in using a token.'})
    else:
        return jsonify({'result': token_auth.logout(g.current_user.id)})


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

