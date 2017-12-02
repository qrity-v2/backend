# coding: utf-8
""" Методы для работы с Облаком Evotor
"""
from flask import Blueprint
from flask import request


evotor_api = Blueprint('evotor_api', __name__)


@evotor_api.route('/evotor/', methods=['GET'])
def short_link():
    """ Эвотор запрашивает этот метод чтобы отобразить iFrame

        http://78.155.199.101:5000/evotor/?token={token}&uid={uid}
    """
    # идентификатор пользователя в облаке Эвотор
    uid = request.args.get('uid')
    # токен пользователя, для авторизации запросов к REST API Эвотор
    token = request.args.get('token')

    print request.args

    return 'test'
