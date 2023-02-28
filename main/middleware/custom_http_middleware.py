import typing as t
from flask import Request, jsonify
from flask_http_middleware import BaseHTTPMiddleware, Response, request
from main.utilities import api_logger as logger, app_logger, exception_logger



import time


class HTTPCustomMiddleware(BaseHTTPMiddleware):

    def __init__(self):
        super().__init__()

    def dispatch(self, request: Request, call_next: callable) -> Response:

        start_time = time.time()
        response = call_next(request)
        end_time = time.time()
        log = {"url": request.url,
               "method": request.method,
               "status": response.status,
               "request": request.get_data(),
               "response": response.get_data(),
               "start_time": start_time,
               "end_time": end_time}
        logger.info(log)
        return response

    def error_handler(self, error: t.Any):
        # app_logger.error(error)

        exception_logger.error(error.args)
        return jsonify({"error": str(error.args)})
