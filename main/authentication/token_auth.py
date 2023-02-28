"""
expire(name, time, nx=False, xx=False, gt=False, lt=False)
    Set an expire flag on key name for time seconds with given option.
    time can be represented by an integer or a Python timedelta object.

expireat(name, when, nx=False, xx=False, gt=False, lt=False)
    Set an expire flag on key name with given option. when can be represented
    as an integer indicating unix time or a Python datetime object.

expiretime(key)
    Returns the absolute Unix timestamp (since January 1, 1970) in seconds at
    which the given key will expire.

delete(*names)
    Delete one or more keys specified by names

exists(*names)
    Returns the number of names that exist

get(name)
    Return the value at key name, or None if the key does’nt exist

incr(name, amount=1)
    Increments the value of key by amount. If no key exists, the value will be initialized as amount

lastsave(**kwargs)
    Return a Python datetime object representing the last time the Redis database was saved to disk

save(**kwargs)
    Tell the Redis server to save its data to disk, blocking until the save is complete

set(name, value, ex=None, px=None, nx=False, xx=False, keepttl=False, get=False, exat=None, pxat=None)
    Set the value at key name to value
    - ex sets an expire flag on key name for ex seconds.
    - px sets an expire flag on key name for px milliseconds.
    - nx if set to True, set the value at key name to value only
        if it does not exist.
    - xx if set to True, set the value at key name to value only
        if it already exists.
    - keepttl if True, retain the time to live associated with the key.
        (Available since Redis 6.0)
    - get if True, set the value at key name to value and return
        the old value stored at key, or None if the key did not exist. (Available since Redis 6.2)
    - exat sets an expire flag on key name for ex seconds,
        specified in unix time.
    - pxat sets an expire flag on key name for ex milliseconds,
        specified in unix time.

setex(name, time, value)
    Set the value of key name to value that expires in time seconds.
    time can be represented by an integer or a Python timedelta object.

"""

from extensions import redis_client
from main.utilities import app_logger as logger


def check_token(user_id, token):
    """
    checks wetter a token with the specified user id is available and if is equal to the provided token.
    (token expiry is checked implicitly)

    :param user_id: the id of the user to authenticate
    :param token: user token passed to check the validity
    :return: True if token is validated, False otherwise
    """
    logger.debug(f'checking redis db for user.{user_id}')
    redis_token = redis_client.get(f'user.{user_id}')
    if redis_token:
        logger.debug(f'found user.{user_id} on redis, token: {redis_token}')
        if redis_token == token:
            logger.debug('db token equals provided token, authentication successful')
            return True
        else:
            logger.debug('db token does not equal provided token, authentication failed')
            return False
    else:
        logger.debug(f'couldn\'t find user.{user_id} on redis db, authentication failed')
        return False


def login(user):
    """
    generates a new token for the user and inserts the token to the redis db.

    token expiry is set to 5 hours (60*60*5 seconds)

    Token structure:
        -   name: \"user.{id}\"
        -   value: token

    :param user: the user object to be logged in, needs to have a token on redis db
    :return: dict(): the generated token by User
    """
    token = user.get_token()
    redis_client.set(name=f'user.{user.id}', value=token, ex=60*60*5)
    return {'token_string': token, 'exp': 60*60*5}


def logout(user_id):
    """
    removes the user token from redis db

    :param user_id: id of the user that is logging out
    :return: boolean
    """
    redis_client.delete(f'user.{user_id}')
    return True
