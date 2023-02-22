from flask import Flask
from conf import config
from log_utils import init_logger
import logging
from flask_sqlalchemy import SQLAlchemy

init_logger(__name__)
logger = logging.getLogger(__name__)
db = SQLAlchemy()


def create_flask_app(config_name='default'):
    """
    Factory method to create a flask application instance using main.conf classes.
    Functions operates as below:

    First it will initialize the application instance with the config name passed to it.

    Second it will initialize all the flask extensions that are defined in the module with the application instance created in step 1.

    Third it will register the blueprints to the application instance.

    """

    """
    Application initialization
    """
    logger.debug(f'attempting to initialize the app with {config_name} configuration ...')

    app = Flask(__name__)


    logger.info('application initialized successfully.')

    app.config.from_object(config[config_name])


    logger.debug('custom configuration added to the application instance.')

    """
    Initializing the flask extentions
    """
    db.init_app(app)

    """
    Registering the Blueprints
    """

    return app
