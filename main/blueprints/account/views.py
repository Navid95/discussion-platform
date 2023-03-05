
from flask import request, abort, Response, g, jsonify
from datetime import datetime, timedelta
from main.utilities import NoUserFound
from extensions import redis_client
from main.models import User
from main.schemas import UserSchema, LoginSchema
from main.authentication import jwt, load_login_data, validate_login_credentials_post, user_owner_required
from flask_jwt_extended import jwt_required, create_access_token, get_jwt, get_current_user, current_user
from main.blueprints.default.errors import error

from . import user_blueprint, decorators


api = user_blueprint
schema = UserSchema()
login_schema = LoginSchema()
owner_required = user_owner_required
dump_user = decorators.dump_user
load_user = decorators.load_user

ACCESS_EXPIRES = timedelta(hours=1)

"""
CRUD APIs
"""


@api.route('/<id>', methods=['GET'])
@jwt_required()
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
        return jsonify({'error': 'failed'})


@api.route('/<id>', methods=['PATCH'])
@jwt_required()
@owner_required
@dump_user
def update_user(id):
    json_raw = request.get_json()
    new_user = schema.load(json_raw)
    current_user.email = new_user.email
    current_user.password_hash = new_user.password_hash
    result = User.update(current_user)
    if result:
        return current_user
    else:
        abort(400)


@api.route('/<id>', methods=['DELETE'])
@jwt_required()
@owner_required
@load_user
def delete_user(id):
    if User.delete(id):
        return jsonify({'status': 200, 'message': 'successful'})

    return jsonify({'status': 400, 'message': 'failed'})


"""
business logic APIs
"""


@api.route('/login', methods=['POST'])
@load_login_data
def login():
    """
    Receives email/pass and if it's validated returns jwt-token specific with that user account.

    user can use the token for further access to the system.

    :return: user's authorization token
    """
    user_credentials = dict()
    user_credentials.update(g.input_data)
    try:
        if validate_login_credentials_post(user_credentials['email'], user_credentials['password']):
            token = create_access_token(identity=g.current_user)
            return jsonify(access_token=token)
    except NoUserFound as e:
        abort(401)
    except BaseException as e:
        abort(500)


@api.route('/logout', methods=['DELETE'])
@jwt_required()
def logout():
    """
    logs out the user if it is using token authentication (token gets removed and will not be valid anymore)

    :return: result, if token authentication is not used returns a message to user (no token is removed)
    """
    if get_jwt():
        jti = get_jwt()['jti']
        redis_client.set(name=jti,value='',ex=ACCESS_EXPIRES)
        return jsonify(message='token revoked successfully')
    else:
        return jsonify({'message': 'no token provided'})


@api.route('/test', methods=['GET'])
def test():
    return jsonify(message='hara kiri?')

