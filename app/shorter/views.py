# coding: utf-8
from flask import Blueprint
from flask import request

from app.errors import BadFormException
from app.shorter.functions import save_link


links_api = Blueprint('links_api', __name__)


@links_api.route('/short/', methods=['POST'])
def short_link():
    url = request.form.get('url')
    if not url:
        raise BadFormException

    key = save_link(url=url)
    return {'result': {'key': key}}


# TODO: отдельные пачечные запросы
