import logging
from jsonformatter import JsonFormatter


"""
logger configs
"""

logger_config = {
    'version': 1,
    'formatters': {
        'normal_formatter': {
            'format': '[%(asctime)s] - %(levelname)s - %(name)s:%(funcName)s - %(message)s',
            "class": 'logging.Formatter'
        }
        , 'api_json_formatter': {
            'format': '''{
                            "Name":            "name",
                            "Levelno":         "levelno",
                            "Levelname":       "levelname",
                            "Pathname":        "pathname",
                            "Filename":        "filename",
                            "Module":          "module",
                            "Lineno":          "lineno",
                            "FuncName":        "funcName",
                            "Created":         "created",
                            "Asctime":         "asctime",
                            "Msecs":           "msecs",
                            "RelativeCreated": "relativeCreated",
                            "Thread":          "thread",
                            "ThreadName":      "threadName",
                            "Process":         "process",
                            "Message":         "message"
                        }'''
            , 'class': 'jsonformatter.JsonFormatter'
        }
    },
    # 'filters': {
    #     'filter_id_1': {
    #         'name': ''
    #     },
    #     'filter_id_2': {}
    # },
    'handlers': {
        'console_handler': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'api_json_formatter',
        }
        , 'api_json_file_handler': {
            'class': 'logging.FileHandler',
            'level': 'DEBUG',
            'formatter': 'api_json_formatter',
            'filename': 'logs/api.json.log',
            'mode': 'a'
            # 'filters': '[filter_id_#, filter_id_#+1, ...]'
        }
        , 'app_file_handler': {
            'class': 'logging.FileHandler',
            'level': 'DEBUG',
            'formatter': 'normal_formatter',
            'filename': 'logs/app.log',
            'mode': 'a'
            # 'filters': '[filter_id_#, filter_id_#+1, ...]'
        }
        , 'app_exception_handler': {
            'class': 'logging.FileHandler',
            'level': 'WARNING',
            'formatter': 'api_json_formatter',
            'filename': 'logs/exception.json.log',
            'mode': 'a'}

    },
    'loggers': {
        'api_logger': {
            'level': 'DEBUG',
            'propagate': True,
            'handlers': ['console_handler', 'api_json_file_handler']
        }
        , 'app_logger': {
            'level': 'DEBUG',
            'propagate': True,
            # 'filters': '[filter_id_#, filter_id_#+1, ...]',
            'handlers': ['console_handler', 'app_file_handler']
        }
        , 'exception_logger': {
            'level': 'DEBUG',
            'propagate': True,
            # 'filters': '[filter_id_#, filter_id_#+1, ...]',
            # 'handlers': ['console_handler', 'app_exception_handler']
            'handlers': ['app_exception_handler']
        }
    },
    'root': {
        'level': 'DEBUG'
    },
    'incremental': False,
    'disable_existing_loggers': True
}
