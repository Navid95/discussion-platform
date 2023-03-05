from unittest import TestCase
from main.utilities import NoUserFound
from extensions import db
from main import create_flask_app
from main.models import User, Topic, Post


class TestExceptions(TestCase):

    def setUp(self):
        self.app = create_flask_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):

        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_NoUserFound(self):
        code = 0
        try:
            User.get(1)
        except NoUserFound as e:
            print(e.code)
            print(e.__context__)
            print(e.__cause__)
            print(e.args)
            print(e)
            error = {'error': e.args[0], 'error code': e.code}
            print(error.__repr__())
