from unittest import TestCase
from main.utilities import app_logger as logger
from extensions import db
from discussion import app
from main import create_flask_app
from main.models import User, Topic, Post


class TestBusiness(TestCase):

    def setUp(self):
        self.app = create_flask_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_init_topic(self):
        user1 = User(email='user1@email.com', password='1234')
        topic1 = Topic(title='title1')
        user1.init_topic(topic=topic1)
        self.assertTrue(topic1 in user1.topics)

        db.session.add(user1)
        db.session.commit()
        self.assertTrue(topic1 in User.get(user1.id).topics)

    def test_user_follow_topic(self):
        user1 = User(email='user1@email.com', password='1234')
        topic1 = Topic(title='title1')
        user1.init_topic(topic=topic1)

        user2 = User(email='user2@email.com', password='1234')
        user2.waiting_accept.append(topic1)
        self.assertTrue(user2.follow_topic(topic1))
        self.assertTrue(topic1 in user2.follows)

        db.session.add_all([user1, user2, topic1])
        db.session.commit()

        self.assertTrue(topic1 in User.get(user2.id).follows)

    def test_user_has_followed(self):
        user1 = User(email='user1@email.com', password='1234')
        topic1 = Topic(title='title1')
        user1.follows.append(topic1)
        self.assertTrue(user1.has_followed(topic1))

        db.session.add_all([user1, topic1])
        db.session.commit()

        self.assertTrue(User.get(user1.id).has_followed(topic1))

    def test_user_owns_topic(self):
        user1 = User(email='user1@email.com', password='1234')
        topic1 = Topic(title='title1')
        user1.topics.append(topic1)
        self.assertTrue(user1.owns_topic(topic1))

        db.session.add_all([user1, topic1])
        db.session.commit()

        self.assertTrue(User.get(user1.id).owns_topic(topic1))

    def test_user_has_in_waiting_list(self):
        user1 = User(email='user1@email.com', password='1234')
        topic1 = Topic(title='title1')
        user1.waiting_accept.append(topic1)
        self.assertTrue(user1.has_in_waiting_list(topic1))

        db.session.add_all([user1, topic1])
        db.session.commit()

        self.assertTrue(User.get(user1.id).has_in_waiting_list(topic1))

    def test_user_invite_user_to_topic(self):
        user1 = User(email='user1@email.com', password='1234')
        topic1 = Topic(title='title1')
        user1.init_topic(topic=topic1)

        user2 = User(email='user2@email.com', password='1234')
        user1.invite_user_to_topic(user=user2, topic=topic1)

        db.session.add(user1, user2)
        db.session.commit()

        self.assertTrue(topic1 in User.get(user2.id).waiting_accept)

    def test_topic_has_post(self):
        topic1 = Topic(title='title1')
        post1 = Post(content='content1')
        topic1.posts.append(post1)

        db.session.add(topic1)
        db.session.commit()

        self.assertTrue(Topic.get(topic1.id).has_post(post1))

    def test_topic_add_post(self):
        topic1 = Topic(title='title1')
        topic2 = Topic(title='title2')
        post1 = Post(content='content1')

        self.assertTrue(topic1.add_post(post1))

        db.session.add_all([topic1, topic2])
        db.session.commit()

        self.assertTrue(Topic.get(topic1.id).has_post(post1))
        self.assertFalse(Topic.get(topic2.id).add_post(post1))

