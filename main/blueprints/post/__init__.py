# print(f'-------------------------------------{__name__}----------------------------------------------')

from flask import Blueprint

post = Blueprint('post', __name__)

from . import views

