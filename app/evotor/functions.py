# coding: utf-8
from flask import current_app


PREFIX = 'user_'


def _get_key(user_id):
    return u'{}_{}'.format(PREFIX, user_id)


def save_user_token(user_id, token):
    key = _get_key(user_id=user_id)
    current_app.redis.set(name=key, value=token)
    return True


def get_user_token(user_id):
    key = _get_key(user_id=user_id)
    return current_app.redis.get(name=key)
