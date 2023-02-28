from . import default
from main.utilities import api_logger
from flask import request, Response, g
from time import time

print(f'-----------------------------------{__name__}-----------------------------------')


@default.before_app_request
def before_request():
    g.request_start_time = time()


@default.after_app_request
def after_request(response: Response):
    end_time = time()
    api_logger.info(f'[status: {response.status_code}, '
                    f'method: {request.method}, '
                    f'request: {request.get_data()}, '
                    f'response: {response.response}, '
                    f'starttime: {g.request_start_time}, '
                    f'endtime: {time()}]')
    return response
