# coding: utf-8
""" Методы для работы с Облаком Evotor
"""
from flask import Blueprint
from flask import current_app
from flask import request
from flask import Response

from app.errors import BadFormException
from app.evotor.client import EvotorClient
from app.evotor.functions import save_user_token
from app.reviews.models import ReviewStorage


evotor_api = Blueprint('evotor_api', __name__)


@evotor_api.route('/evotor/', methods=['GET'])
def evotor_iframe():
    """ Эвотор запрашивает этот метод чтобы отобразить iFrame

        https://bot-maxim.com/evotor/?token=${token}&uid=${uid}
    """
    return Response(current_app.iframe_template, status=200)


@evotor_api.route('/evotor/auth/', methods=['POST'])
def save_new_client():
    """ Облако должно дёрнуть этот метод при установке нового приложения из стора
    """
    data = request.get_json()
    user_id = data.get('userId')
    token = data.get('token')

    if user_id and token:
        save_user_token(user_id=user_id, token=token)
        # спарсить всех работников и сохранить этот токен и им тоже
        # TODO: "в будущем" запускать парсинг регулярно
        try:
            cli = EvotorClient(token=token, uid=user_id)
            employers = cli.get_employers_list()
            for item in employers:
                save_user_token(user_id=item['uuid'], token=token)
        except Exception as e:
            print 'error:', e
        return {'result': 'ok'}
    else:
        raise BadFormException


@evotor_api.route('/evotor/crutch/', methods=['POST'])
def evotor_crutch():
    """ Получить заголовок и отдать его в ответе, потому что SDK не имеет к нему доступа
    """
    shop_id = request.headers.get('X-Evotor-Store-Uuid')
    user_id = request.headers.get('X-Evotor-User-Id')
    return {
        'result': {
            'shop_id': shop_id,
            'user_id': user_id,
        }
    }


@evotor_api.route('/evotor/report/', methods=['GET'])
def load_data():
    """ Отдать данные для отрисовки страницы в админке Эвотора
    """
    # идентификатор пользователя в облаке Эвотор
    uid = request.args.get('uid')
    # токен пользователя, для авторизации запросов к REST API Эвотор
    token = request.args.get('token')
    if not any([uid, token]):
        raise BadFormException

    # Найти все магазины и всех пользователей от этого владельца
    cli = EvotorClient(token=token, uid=uid)
    shops = cli.get_shop_list()
    shops_map = {item['uuid']: item for item in shops}

    employers = cli.get_employers_list()
    employers_map = {item['uuid']: item for item in employers}

    result = []

    query = {
        "$or": [
            {"user_id": {"$in": employers_map.keys()}},
            {"shop_id": {"$in": shops_map.keys()}},
        ],
    }
    print query

    res = ReviewStorage.objects(__raw__=query)
    for item in res:
        user_id = item.user_id
        if user_id not in employers_map:
            # Исключить неправильные ID
            continue
        data = {
            'user_id': user_id,
            'shop_id': item.shop_id,
            'rating': getattr(item, 'rating', None),
            'text': getattr(item, 'text', None),
            'tags': getattr(item, 'tags', []),
            'first_name': employers_map[user_id]['name'],
            'last_name': employers_map[user_id]['lastName'],
            'phone': employers_map[user_id]['phone'],
            'timestamp': int(item.added),
        }
        result.append(data)

    return {'result': result}
