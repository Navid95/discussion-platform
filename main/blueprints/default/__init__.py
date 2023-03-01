from flask import Blueprint

default = Blueprint('default', __name__)

from . import api_log_generator, errors