from unittest import TestCase
from main import create_flask_app, db
from main.models import User, Topic, Post
from log_utils import init_logger
import logging

init_logger(__name__)
logger = logging.getLogger(__name__)


class test_models(TestCase):

    def setUp(self):
        self.app = create_flask_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.user1 = User(email='self_user1@email.com', password='user1')
        self.topic1 = Topic(title='self_title1')
        self.post1 = Post(content='blah blah blah')

        db.session.add_all([self.user1, self.topic1, self.post1])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        pass

    def test_user_creation(self):
        user = User(email='user1@email.com', password='1234')
        db.session.add(user)
        db.session.commit()
        logger.debug(f'new user persisted: {user}')
        tmp_user = User.query.filter_by(email='user1@email.com').first()
        self.assertIsNotNone(tmp_user)

    def test_topic_creation(self):
        title = 'arbitrary title'
        topic = Topic(title=title)
        db.session.add(topic)
        db.session.commit()
        logger.debug(f'new topic persisted: {topic}')
        self.assertIsNotNone(Topic.query.filter_by(title=title).first())

    def test_user_topic_assignment(self):
        self.user1.topics.append(self.topic1)
        db.session.add(self.user1)
        db.session.commit()
        logger.debug(f'added self.topic1 to self.user1.topics')
        tmp_user = User.query.filter_by(id=self.user1.id).first()
        logger.debug(f'self.topic1: {self.topic1}')
        logger.debug(f'self.user1: {self.user1}')
        logger.debug(f'tmp_user.topics: {tmp_user.topics}')
        self.assertEqual(tmp_user.topics[0], self.user1.topics[0])
        self.assertTrue(len(Topic.query.all())==1)
        self.assertTrue(len(User.query.all())==1)


    def test_topic_user_assignment(self):
        self.topic1.owner_id = self.user1.id
        db.session.add(self.topic1)
        logger.debug(f'assigned self.user1.id to self.topic1.owner_id')
        tmp_user = User.query.filter_by(id=self.topic1.owner_id).first()
        logger.debug(f'self.topic1: {self.topic1}')
        logger.debug(f'self.user1: {self.user1}')
        logger.debug(f'tmp_user: {tmp_user}')
        self.assertTrue(self.user1 == tmp_user)
        self.assertIn(self.topic1, self.user1.topics)
        self.assertTrue(len(User.query.all())==1)
        self.assertTrue(len(Topic.query.all())==1)

    def test_post_creation(self):
        post = Post(content='xxxxxx')
        db.session.add(post)
        db.session.commit()
        logger.debug(f'new post persisted: {post}')
        self.assertIsNotNone(post.id)
        self.assertIsNotNone(Post.query.filter_by(id=post.id).first())

    def test_post_topic_assignment(self):
        self.post1.topic_id = self.topic1.id
        db.session.add(self.post1)
        db.session.commit()
        logger.debug(f'assigned self.topic1.id to self.post1.topic_id')
        tmp_topic = Topic.query.filter_by(id=self.post1.topic_id).first()
        logger.debug(f'self.topic1: {self.topic1}')
        logger.debug(f'self.post1: {self.post1}')
        logger.debug(f'tmp_topic: {tmp_topic}')
        self.assertIsNotNone(self.post1.topic)
        self.assertEqual(self.topic1, tmp_topic)
        self.assertIn(self.post1,self.topic1.posts)
        self.assertTrue(len(Post.query.all())==1)
        self.assertTrue(len(Topic.query.all())==1)

    def test_topic_post_assignment(self):
        self.topic1.posts.append(self.post1)
        db.session.add(self.topic1)
        db.session.commit()
        logger.debug(f'added self.post1 to self.topic1.posts')
        tmp = Post.query.filter_by(id=self.topic1.posts[0].id).first()
        logger.debug(f'self.topic1: {self.topic1}')
        logger.debug(f'self.post1: {self.post1}')
        logger.debug(f'tmp_topic: {tmp}')
        self.assertIsNotNone(tmp)
        self.assertEqual(self.post1, tmp)
        self.assertEqual(tmp.topic_id, self.topic1.id)
        self.assertIn(self.post1,self.topic1.posts)
        self.assertTrue(len(Post.query.all())==1)
        self.assertTrue(len(Topic.query.all())==1)






