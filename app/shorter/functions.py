# coding: utf-8
import hashlib

from flask import current_app


PREFIX = 'url_'
KEY_LENGTH = 5


def _generate_hash(url):
    name = hashlib.md5(url).hexdigest()
    return name[:KEY_LENGTH]


def save_link(url):
    key = _generate_hash(url=url)
    if not get_full_link(url_hash=key):
        current_app.redis.set(name=key, value=url, ex=60 * 60 * 24)
    return key


def get_full_link(url_hash):
    return current_app.redis.get(url_hash)
