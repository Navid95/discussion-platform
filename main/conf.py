import os
import logging

basedir = os.path.abspath(os.path.dirname(__file__))

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(f'logs/{__name__}.log')
file_handler.setLevel(logging.DEBUG)
file_handler_format = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(name)s:%(funcName)s:: %(message)s')
file_handler.setFormatter(file_handler_format)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.WARNING)
console_handler_format = logging.Formatter(fmt='%(levelname)s:: %(message)s')
console_handler.setFormatter(console_handler_format)

logger.addHandler(file_handler)
logger.addHandler(console_handler)


class BaseConfig:
    """
    Base Class of flask app configuration consisting of the following parts:

    Environment variables needed by flask extensions

    :SECRET_KEY: encryption key used by various modules

    :SQLALCHEMY_TRACK_MODIFICATIONS: Defaults to False

    """

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'discussion app secret key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class Dev(BaseConfig):
    """
    Child class of BaseConfig, representing the development environments' configurations.

    :DEBUG: Defaults to True

    :SQLALCHEMY_DATABASE_URI: The URI that SQLALCHEMY uses to for connection string
    """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class Test(BaseConfig):
    """
        Child class of BaseConfig, representing the test environments' configurations.

        :DEBUG: Defaults to True

        :SQLALCHEMY_DATABASE_URI: The URI that SQLALCHEMY uses for connection string, test environment uses an in-memory DB if no "TEST_DATABASE_URL" is available in environment variables
        """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
                              'sqlite://'


class Pro(BaseConfig):
    """
            Child class of BaseConfig, representing the production environments' configurations.

            :DEBUG: Defaults to False

            :SQLALCHEMY_DATABASE_URI: The URI that SQLALCHEMY uses to for connection string
            """
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('PRO_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data-pro.sqlite')


config = {
    'development': Dev,
    'test': Test,
    'production': Pro,
    'default': Dev
}


logger.debug(f'configuration file imported successfully.')