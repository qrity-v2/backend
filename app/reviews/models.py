# coding: utf-8
""" Схемы данных для хранения отзывов
"""
import time

from mongoengine import Document
from mongoengine import SequenceField
from mongoengine import IntField
from mongoengine import StringField
from mongoengine import ListField


def current_timestamp():
    """Получить текущее время, timestamp"""
    return int(time.time())


class ReviewStorage(Document):
    id = SequenceField(
        required=True,
        primary_key=True,
    )
    shop_id = StringField(
        required=True,
    )
    user_id = StringField(
        required=True,
    )
    rating = IntField(
        required=True,
        min_value=1,
        max_value=5,
    )
    tags = ListField(
        StringField(),
    )
    text = StringField(
        required=False,
    )
    added = IntField(
        required=True,
        min_value=0,
        default=current_timestamp,
    )

    meta = {
        'collection': 'review',
        'ordering': ['-id'],
        'indexes': [
            {'fields': ['shop_id', 'user_id']},
            {'fields': ['added']}
        ],
        # TODO: disable after 1M objects
        'auto_create_index': True,
        'index_background': True,
    }

    @classmethod
    def add_ratings(cls, shop_id, user_id, rating, tags, text):
        return cls(shop_id=shop_id, user_id=user_id, rating=rating, tags=tags, text=text).save()
