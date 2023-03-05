import os
from main.utilities import app_logger as logger
basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    """
    Base Class of flask app configuration consisting of the following parts:

    Environment variables needed by flask extensions

    :SECRET_KEY: encryption key used by various modules

    :SQLALCHEMY_TRACK_MODIFICATIONS: Defaults to False

    """

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'discussion app secret key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CUSTOM_ENCRYPTION_ALGO = os.environ.get('CUSTOM_ENCRYPTION_ALGO') or 'HS256'

#   Redis configurations
    REDIS_DECODE_RESPONSES = True

#   flask-jwt-extended configurations
#     by default if ot set flask SECRET_KEY is used by this extension
    JWT_SECRET_KEY = os.environ.get('SECRET_KEY') or SECRET_KEY
    # by default looks for jwts in headers
    JWT_TOKEN_LOCATION = ['headers']


class Dev(BaseConfig):
    """
    Child class of BaseConfig, representing the development environments' configurations.

    :DEBUG: Defaults to True

    :TESTING: an indicator that the application is running in the test mode

    :SQLALCHEMY_DATABASE_URI: The URI that SQLALCHEMY uses to for connection string
    """
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class Test(BaseConfig):
    """
        Child class of BaseConfig, representing the test environments' configurations.

        :DEBUG: Defaults to True

        :TESTING: an indicator that the application is running in the test mode

        :SQLALCHEMY_DATABASE_URI: The URI that SQLALCHEMY uses for connection string, test environment uses an in-memory DB if no "TEST_DATABASE_URL" is available in environment variables
        """
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
                              'sqlite://'
                              # 'sqlite:///'+ os.path.join(basedir, 'db.sqlite')
                              # 'sqlite:////home/navid/PycharmProjects/discussion-platform/db.sqlite'


class Pro(BaseConfig):
    """
            Child class of BaseConfig, representing the production environments' configurations.

            :DEBUG: Defaults to False

            :TESTING: an indicator that the application is running in the test mode

            :SQLALCHEMY_DATABASE_URI: The URI that SQLALCHEMY uses to for connection string
            """
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('PRO_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data-pro.sqlite')


config = {
    'development': Dev,
    'test': Test,
    'production': Pro,
    'default': Dev
}

logger.debug(f'configuration file imported successfully.')
