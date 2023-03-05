from main.utilities import log_utils
import logging
from logging.config import dictConfig

logger_config = log_utils.logger_config
dictConfig(logger_config)

api_logger = logging.getLogger('api_logger')
app_logger = logging.getLogger('app_logger')
exception_logger = logging.getLogger('exception_logger')

from .exceptions import NoUserFound