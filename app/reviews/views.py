# coding: utf-8
from flask import Blueprint
from flask import current_app
from flask import request
from flask import Response
from telegram.parsemode import ParseMode

from app.errors import BadFormException
from app.reviews.models import ReviewStorage


TELEGRAM_REPORT = [
    50512389,
    202390270,
    91990226,
]


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

    # Сохранить отзыв
    ReviewStorage.add_ratings(
        shop_id=shop_id,
        user_id=user_id,
        rating=rating,
        tags=tags,
        text=text,
    )

    # Если плохо, отправить отчёт в Telegram
    if rating and rating <= 3:
        report_body = u'''
Вам оставили оценку *{}* за *{}*

Посмотреть подробнее на сайте Эвотора:  
https://market.evotor.ru/#/user/apps/7c2ce653-c50a-4ca5-a1af-afae3ce18d1b?tab=0
'''.format(rating, u', '.join(tags))
        for tg_id in TELEGRAM_REPORT:
            try:
                current_app.bot.send_message(
                    chat_id=tg_id,
                    text=report_body,
                    parse_mode=ParseMode.MARKDOWN,
                    disable_web_page_preview=True,
                )
            except Exception as e:
                print 'send report error:', e
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
