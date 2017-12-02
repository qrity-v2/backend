# coding: utf-8
from flask import Blueprint
from flask import current_app
from flask import request
from flask import Response

from app.errors import BadFormException
from app.reviews.models import ReviewStorage


reviews_api = Blueprint('reviews_api', __name__)


@reviews_api.route('/review/', methods=['POST'])
def save_review():
    """ Сохранить отзыв пользователя
    """
    shop_id = request.form.get('shop_id')
    user_id = request.form.get('user_id')
    rating = request.form.get('rating', type=int)
    tags = request.form.getlist('tags')
    text = request.form.get('text')

    if not all([shop_id, user_id]) or not any([rating, tags, text]):
        raise BadFormException

    ReviewStorage.add_ratings(
        shop_id=shop_id,
        user_id=user_id,
        rating=rating,
        tags=tags,
        text=text,
    )
    return {'result': 'ok'}


@reviews_api.route('/review/params/', methods=['GET'])
def get_form_params():
    return {
        'result': {
            'tags_bad': [
                u'грубят',
                u'грязно',
                u'не вкусно',
                u'обманули',
                u'длительное ожидание',
                u'не соответствует ожиданиям',
            ],
            'tags_good': [
                u'вкусно',
                u'очень красиво',
                u'превосходный сервис',
            ],
        }
    }


@reviews_api.route('/f/', methods=['GET'])
def render_form():
    """ Отдать статическую страницу формочки оценивания
    """
    return Response(current_app.form_template, status=200)
