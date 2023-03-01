# print(f'-------------------------------------{__name__}----------------------------------------------')

from flask import g, jsonify, request
from main.models import User, Topic, Post
from main.authentication import basic_http
from main.schemas import TopicSchema
from . import topic as api


auth = basic_http.auth
schema = TopicSchema()


@api.route('/', methods=['POST'])
@auth.login_required
def init_topic():
    topic = schema.load(request.get_json())
    if g.current_user.init_topic(topic):
        return schema.dumps(topic)
    else:
        return jsonify({'message': 'Something wrong happened'})



def follow_topic():
    pass


def reject_invitation():
    pass


def invite_user_to_topic():
    pass


def add_post():
    pass



"""
CRUD APIs
"""

