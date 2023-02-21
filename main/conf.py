import os

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
