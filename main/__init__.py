print(f'-------------------------------------{__name__}----------------------------------------------')

from flask import Flask
import conf
from main.configuration.log_utils import init_logger
import logging
from .extensions import db, marshmallow

config = conf.config

init_logger(__name__)
logger = logging.getLogger(__name__)


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
    marshmallow.init_app(app)

    """
    Registering the Blueprints
    """
    from .blueprints import apis
    app.register_blueprint(blueprint=apis.apiv1,url_prefix='/api/v1')

    from .blueprints import account
    app.register_blueprint(blueprint=account.user_blueprint, url_prefix='/api/v1/user')

    from .blueprints import topic
    app.register_blueprint(blueprint=topic.topic, url_prefix='/api/v1/topic')

    from .blueprints import post
    app.register_blueprint(blueprint=post.post, url_prefix='/api/v1/post')

    logger.debug(f'application instance initialization completed')
    return app
