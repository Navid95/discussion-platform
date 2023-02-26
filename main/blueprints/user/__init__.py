print(f'-------------------------------------{__name__}----------------------------------------------')

from flask import Blueprint

user = Blueprint('user', __name__)

from . import views


