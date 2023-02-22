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
        self.assertTrue(len(Topic.query.all()) == 1)
        self.assertTrue(len(User.query.all()) == 1)

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
        self.assertTrue(len(User.query.all()) == 1)
        self.assertTrue(len(Topic.query.all()) == 1)

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
        self.assertIn(self.post1, self.topic1.posts)
        self.assertTrue(len(Post.query.all()) == 1)
        self.assertTrue(len(Topic.query.all()) == 1)

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
        self.assertIn(self.post1, self.topic1.posts)
        self.assertTrue(len(Post.query.all()) == 1)
        self.assertTrue(len(Topic.query.all()) == 1)

    def test_user_post_on_topic_assignment(self):
        self.topic1.posts.append(self.post1)
        self.user1.posts.append(self.post1)
        user2 = User(email='user2@email.com', password='1234')
        user2.topics.append(self.topic1)

        db.session.add(user2)
        db.session.commit()

        tmp_post1 = Post.query.filter_by(author_id=self.user1.id).first()
        tmp_post2 = Post.query.filter_by(topic_id=self.topic1.id).first()

        db.session.commit()

        self.assertIsNotNone(tmp_post1)
        self.assertIsNotNone(tmp_post2)
        logger.debug(f'tmp_post1: {tmp_post1}')
        logger.debug(f'tmp_post2: {tmp_post2}')

        self.assertEqual(self.post1, tmp_post1)
        self.assertEqual(self.post1, tmp_post2)

        self.assertIn(tmp_post1, self.topic1.posts)
        self.assertIn(tmp_post1, self.user1.posts)

        self.assertIn(self.topic1, User.query.filter_by(id=user2.id).first().topics)

    def test_user_crud(self):
        email = 'crud-user@email.com'
        user = User(email=email, password='crud-user')
        user.topics.append(self.topic1)
        self.topic1.posts.append(self.post1)

        """
        Create
        """
        User.persist(user)
        self.assertIsNotNone(user)
        self.assertIsNotNone(user.id)
        logger.debug(f'Create operations tests passed successfully')

        """
        Read
        """
        self.assertEqual(user, User.get_instance(id=user.id))
        self.assertEqual(user, User.get_instance(email=user.email))
        logger.debug(f'Read operations (get_instance) tests passed successfully')

        user_list = list()
        user_list.append(user)
        user_list.append(self.user1)
        users = User.get_all()
        self.assertEqual(len(user_list), len(users))
        logger.debug(f'user_list type: {type(user_list)}')
        logger.debug(f'users type: {type(users)}')
        self.assertCountEqual(users, user_list)
        logger.debug(f'Read operations (get_all) tests passed successfully')

        logger.debug(f'Read operations tests passed successfully')

        """
        Update
        """
        old_id = user.id
        email2 = 'crud-user-2@email.com'
        logger.debug(f'user with old email: {user}')
        user.email = email2
        User.update(user)
        logger.debug(f'user with updated email: {user}')
        logger.debug(f'db user fetched with id: {User.get_instance(user.id)}')
        self.assertEqual(User.get_instance(id=user.id).email, email2)
        self.assertEqual(User.get_instance(id=user.id), user)
        self.assertEqual(User.get_instance(email=user.email).email, email2)
        self.assertEqual(User.get_instance(id=user.id).id, old_id)

        logger.debug(f'Update operations tests passed successfully')
        logger.debug(f'{User.get_all()}')

        """
        Delete
        """
        user2 = User(email='deletebyid@email', password='1234')
        user3 = User(email='deletebyemail@email', password='1234')
        User.persist(user2)
        User.persist(user3)
        id_2 = user2.id
        id_3 = user3.id
        User.delete_instance(instance=user)
        User.delete_instance(id=user2.id)
        User.delete_instance(email=user3.email)
        self.assertIsNone(User.get_instance(id=old_id))
        self.assertIsNone(User.get_instance(id=id_2))
        self.assertIsNone(User.get_instance(id=id_3))

        logger.debug(f'Delete operations tests passed successfully')

    def test_topic_crud(self):
        title = 'title1'
        topic = Topic(title=title)

        """
        Create
        """
        Topic.persist(topic)
        self.assertIsNotNone(topic.id)

        logger.debug(f'Create operations tests passed successfully')

        """
        Read
        """
        self.assertEqual(topic, Topic.get_instance(id=topic.id))
        self.assertEqual(topic, Topic.get_instance(title=topic.title))
        logger.debug(f'Read operations (get_instance) tests passed successfully')

        topic2 = Topic(title='title2')
        Topic.persist(topic2)
        topic_list = list()
        topic_list.append(topic)
        topic_list.append(topic2)
        topic_list.append(self.topic1)
        self.assertEqual(len(topic_list), len(Topic.get_all()))
        self.assertCountEqual(topic_list, Topic.get_all())
        logger.debug(f'Read operations (get_all) tests passed successfully')

        logger.debug(f'Read operations tests passed successfully')

        """
        Update
        """
        new_title2 = 'new title2'
        topic2.title = new_title2
        Topic.update(topic2)
        self.assertEqual(topic2, Topic.get_instance(id=topic2.id))
        self.assertEqual(topic2.title, Topic.get_instance(id=topic2.id).title)

        logger.debug(f'Update operations tests passed successfully')

        """
        Delete
        """
        id_1 = topic.id
        Topic.delete_instance(id=id_1)
        id_2 = topic2.id
        Topic.delete_instance(instance=topic2)
        title_del = self.topic1.title
        Topic.delete_instance(title=self.topic1.title)

        self.assertIsNone(Topic.get_instance(id=id_1))
        self.assertIsNone(Topic.get_instance(id=id_2))
        self.assertIsNone(Topic.get_instance(title=title_del))

        logger.debug(f'Delete operations tests passed successfully')

    def test_post_crud(self):
        post = Post(content='content')

        """
        Create
        """
        Post.persist(post)
        self.assertIsNotNone(post.id)
        self.assertIsNotNone(post)

        logger.debug(f'Create operations tests passed successfully')

        """
        Read
        """
        self.assertEqual(self.post1, Post.get_instance(id=self.post1.id))
        logger.debug(f'Read operations (get_instance) tests passed successfully')

        post_list = list()
        post_list.append(self.post1)
        post_list.append(post)
        logger.debug(f'Read operations (get_all) tests passed successfully')
        self.assertCountEqual(post_list, Post.get_all())

        logger.debug(f'Read operations tests passed successfully')

        """
        Update
        """
        old_id = post.id
        new_content = 'new post content'
        post.content = new_content
        Post.update(post)
        del post
        self.assertEqual(new_content, Post.get_instance(old_id).content)
        post = Post.get_instance(old_id)
        logger.debug(f'printing fetched post with id {old_id}, :: {post}')
        self.assertTrue(post is not False)

        logger.debug(f'Update operations tests passed successfully')

        """
        Delete
        """
        id_1 = self.post1.id
        id_2 = post.id
        Post.delete_instance(id=id_1)
        Post.delete_instance(instance=post)
        self.assertIsNone(Post.get_instance(id=id_1))
        self.assertIsNone(Post.get_instance(id=id_2))

        logger.debug(f'Delete operations tests passed successfully')