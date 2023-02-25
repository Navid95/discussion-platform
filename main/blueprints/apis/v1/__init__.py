from flask import Blueprint

apiv1 = Blueprint('api_v1', __name__)

from . import user, topic, post
