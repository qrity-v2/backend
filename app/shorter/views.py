# coding: utf-8
from flask import Blueprint
from flask import request
from flask import Response

from app.errors import BadFormException
from app.shorter.functions import save_link
from app.shorter.functions import get_full_link


links_api = Blueprint('links_api', __name__)


@links_api.route('/short/', methods=['POST'])
def short_link():
    url = request.form.get('url')
    if not url:
        raise BadFormException

    key = save_link(url=url)
    return {'result': {'key': key}}


@links_api.route('/s/<url_hash>', methods=['GET'])
def restore_link(url_hash):
    url = get_full_link(url_hash=url_hash)
    if url is not None:
        r = Response(status=302)
        r.headers['Location'] = url
        return r
    return Response(status=404)


# TODO: отдельные пачечные запросы для восстановления работы после восстановления интернета
