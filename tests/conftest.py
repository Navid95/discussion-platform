import pytest
from main.utilities import log_utils
from main import create_flask_app
from extensions import db


@pytest.fixture
def app():
    app = create_flask_app('test')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def cli_runner(app):
    return app.test_cli_runner()



