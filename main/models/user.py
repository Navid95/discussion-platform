# print(f'-------------------------------------{__name__}----------------------------------------------')

from extensions import db
from main.models.base_model import BaseModel
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from main.utilities import app_logger as logger, exception_logger
from datetime import datetime, timedelta
from time import time
from flask import current_app
import jwt

# TODO all custom configs should be created at app initialization in json format

TOKEN_EXP_KEY = 'exp'
TOKEN_SENDER_KEY = 'sender'
TOKEN_RECEIVER_KEY = 'receiver'
TOKEN_TOPIC_KEY = 'topic_id'
TOKEN_GEN_TIME = 'gen_time'

user_follows = db.Table('user_follows',
                        db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                        db.Column('topic_id', db.Integer, db.ForeignKey('topic.id'), primary_key=True))

user_waiting_acceptance = db.Table('user_waiting',
                                   db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                                   db.Column('topic_id', db.Integer, db.ForeignKey('topic.id'), primary_key=True))


class User(BaseModel):
    __tablename__ = 'user'

    # id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(100), nullable=False)

    topics = db.relationship('Topic', backref='owner', collection_class=list)
    posts = db.relationship('Post', backref='author')
    follows = db.relationship('Topic', secondary=user_follows, backref='followers')
    waiting_accept = db.relationship('Topic', secondary=user_waiting_acceptance, backref='invites')

    def __init__(self, email, password, **kwargs):
        super(User, self).__init__(**kwargs)
        self.email = email
        self.password = password

    def __repr__(self):
        return {'id': self.id,
                'email': self.email,
                'password_hash': self.password_hash,
                'created': self.created,
                'updated': self.updated
                }.__str__()

    @property
    def password(self):
        logger.warning(f'attempted to read {User} instance {self} password!')
        raise AttributeError('password field not readable')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    """
    CRUD methods
    """

    @staticmethod
    def get_instance(id=None, **kwargs):
        if id is not None:
            return User.query.filter_by(id=id).first()
        elif kwargs.get('email') is not None:
            return User.query.filter_by(email=kwargs['email']).first()
        else:
            return False

    @staticmethod
    def get_all():
        return User.query.all()

    @staticmethod
    def delete_instance(id=None, instance=None, **kwargs):
        if id is not None:
            user = User.get_instance(id=id)
        elif instance is not None and isinstance(instance, User):
            user = instance
        elif kwargs.get('email') is not None:
            user = User.get_instance(email=kwargs['email'])
        else:
            return False
        try:
            db.session.delete(user)
            db.session.commit()
        except BaseException as e:
            logger.exception(e)
            db.session.rollback()
            return False

    @staticmethod
    def persist(instance):
        try:
            if isinstance(instance, User):
                db.session.add(instance)
                db.session.commit()
                return True
            else:
                return False
        except IntegrityError as e:
            logger.warning(e.orig)
            logger.warning(e.orig.args)
            db.session.rollback()
            return False
        except BaseException as e:
            logger.exception(e)
            db.session.rollback()
            return False

    # TODO check why simple python assignment on a field (exp. email) changes the db row (test_models.test_user_crud Update section)
    @staticmethod
    def update_instance(instance):
        pass

    """
    Inherited CRUD methods
    """

    def save(instance):
        try:
            if isinstance(instance, User):
                db.session.add(instance)
                db.session.commit()
                return True
            else:
                return False
        except IntegrityError as e:
            logger.warning(e.orig)
            logger.warning(e.orig.args)
            db.session.rollback()
            return False
        except BaseException as e:
            logger.exception(e)
            db.session.rollback()
            return False

    def get(id):
        return User.query.filter_by(id=id).first()

    # TODO search best practices for update api
    def update(instance):
        return User.save(instance)

    def delete(id):
        try:
            db.session.delete(User.get(id=id))
            db.session.commit()
            return True
        except BaseException as e:
            logger.exception(f'exception in deleting User with id={id}. Trying to rollback')
            db.session.rollback()
            return False

    """
    business logic
    """

    def init_topic(self, topic):
        """
        user initiates a new topic. user will be the owner
        of the topic and also the topic will be added to the users \"follows\" list

        :param topic: topic object to be initiated by user
        :return: boolean
        """
        if not self.owns_topic(topic) and topic.owner_id is None:
            try:
                self.topics.append(topic)
                self.follow_topic(topic=topic)
                db.session.add(self)
                db.session.commit()
                return True
            except BaseException as e:
                logger.exception(e)
                return False
        else:
            return False

    def follow_topic(self, topic):
        """
        user accepts an invitation to follow a topic. topic should not be already
        in user's follows list and should be in user's waiting_accept list.

        :param topic: the topic object to follow
        :return: boolean
        """
        if not self.has_followed(topic) and topic in self.waiting_accept:
            try:
                self.follows.append(topic)
                db.session.add(self)
                db.session.commit()
                return True
            except BaseException as e:
                logger.exception(e)
                return False
        else:
            return False

    def reject_invitation(self, topic):
        """
        this user rejects an invitation to follow a topic. if present the
        topic object will be removed from user's waiting_accpet list.

        :param topic: the topic object to remove
        :return: boolean
        """
        # if not self.has_followed(topic) and topic in self.waiting_accept:
        if topic in self.waiting_accept:
            try:
                self.waiting_accept.remove(topic)
                db.session.add(self)
                db.session.commit()
                return True

            except BaseException as e:
                logger.exception(e)
                return False
        else:
            return False

    def has_followed(self, topic):
        """
        checks if user follows the given topic or not.
        :param topic: the topic object to look for
        :return: boolean
        """
        return topic in self.follows

    def owns_topic(self, topic):
        """
        checks if given topic is in the user's topics list, which means this user is the owner of the topic
        :param topic: the topic object to look for
        :return: boolean
        """
        return topic in self.topics

    def owns_post(self, post):
        """
        checks if given post is in the user's posts list, which means this user is the author of the post
        :param post: the post object to look for
        :return: boolean
        """
        return post in self.posts

    def has_in_waiting_list(self, topic):
        """
        checks if given topic is in users waiting_accept list or not
        :param topic: the topic object to look for
        :return: boolean
        """
        return topic in self.waiting_accept

    def invite_user_to_topic(self, user, topic):
        """
        this user object invites another user to follow the topic given.
        this user should be the owner of te topic and the second user should not have
        the topic in its waiting_accept or follows list.

        :param user: the user object to be invited to topic
        :param topic: the topic object
        :return: boolean
        """
        if self.owns_topic(topic) and not user.has_followed(topic) and not user.has_in_waiting_list(topic):
            try:
                user.waiting_accept.append(topic)
                db.session.add(user)
                db.session.commit()
                return True
            except BaseException as e:
                logger.exception(e)
                return False
        else:
            return False

    def add_post(self, post, topic):
        """

        this user adds given post under the given topic. user is only allowed to
        do so if he/she is the topic owner or has the topic in their follows list

        :param post: the post object to be added
        :param topic: the topic object that post is being added to
        :return: boolean
        """
        if self.owns_topic(topic) or self.has_followed(topic):
            if topic.add_post(post):
                try:
                    self.posts.append(post)
                    db.session.add(self)
                    db.session.commit()

                    return True
                except BaseException as e:
                    exception_logger.exception(e)
                    return False
            else:
                return False
        else:
            return False


    def get_token(self, expiration=None):
        raw_token = dict()
        raw_token[TOKEN_SENDER_KEY] = self.id
        return encode_token(raw_token, expiration)

    def validate_token(self, token):
        raw_token = decode_token(token)
        if raw_token.get(TOKEN_SENDER_KEY) != self.id:
            return False
        else:
            return True


"""
functions
"""


def encode_token(raw_token, expiration=None):
    if expiration:
        raw_token[TOKEN_EXP_KEY] = datetime.now() + timedelta(seconds=expiration)
    raw_token[TOKEN_GEN_TIME] = time()
    return jwt.encode(payload=raw_token, key=current_app.config['SECRET_KEY'],
                      algorithm=current_app.config['CUSTOM_ENCRYPTION_ALGO'])


def decode_token(token):
    return jwt.decode(jwt=token, key=current_app.config['SECRET_KEY'],
                      algorithms=current_app.config['CUSTOM_ENCRYPTION_ALGO'])
