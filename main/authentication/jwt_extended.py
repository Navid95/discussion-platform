from main.models import User
from extensions import jwt, redis_client
from datetime import datetime, timedelta

# TODO implement a method for token refreshing

@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()


@jwt.additional_claims_loader
def additional_claims_loader(identity):
    claims = dict()
    claims['exp'] = datetime.utcnow() + timedelta(hours=1)
    claims['app_name'] = 'discussion-platform'
    return claims


@jwt.token_in_blocklist_loader
def token_in_blocklist_loader(_jwt_header, jwt_data: dict):
    jti = jwt_data['jti']
    redis_token = redis_client.get(jti)
    return redis_token is not None


