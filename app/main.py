# coding: utf-8
import os
import logging
import logging.config
import json

import mongoengine
import redis
from flask import Flask
from flask import Response
from flask import jsonify
from werkzeug.exceptions import HTTPException
from telegram import Bot

from app.errors import ApiException


def handle_exception_with_as_dict_method(error):
    if isinstance(error, ApiException):
        return jsonify(error.jsonify())
    return error


class BaseFlaskApp(Flask):

    def load_config(self):
        self.config.from_pyfile('settings.py')

        # TODO: логирование
        # logging.config.dictConfig(self.config.get('LOGGING', {}))

    def get_db(self):
        self.db = mongoengine.connect(**self.config['MONGO'])
        self.redis_pool = redis.ConnectionPool(**self.config['REDIS'])
        self.redis = redis.Redis(connection_pool=self.redis_pool)
        self.bot = Bot(token=self.config['TELEGRAM_TOKEN'])

    def load_error_handler(self):
        self.register_error_handler(
            ApiException,
            handle_exception_with_as_dict_method
        )

    def load_static_templates(self):
        # Это хуёво, но это MVP
        base_dir = os.path.dirname(__file__)
        with open(os.path.join(base_dir, 'templates/form_template.html')) as f:
            self.form_template = f.read()

        base_dir = os.path.dirname(os.path.dirname(__file__))
        with open(os.path.join(base_dir, 'static/admin/index.html')) as f:
            self.iframe_template = f.read()

    def make_response(self, rv):
        if isinstance(rv, (self.response_class, Response)):
            return rv

        status = headers = None
        if isinstance(rv, tuple):
            rv, status, headers = rv + (None,) * (3 - len(rv))

        if not isinstance(rv, HTTPException):
            try:
                if rv != '':
                    rv = json.dumps(rv, ensure_ascii=False)
            except TypeError:
                pass

        # Access-Control-Allow-Origin=*
        return super(BaseFlaskApp, self).make_response((rv, status, headers))


def get_app(klass):
    assert issubclass(klass, BaseFlaskApp)
    flask_app = klass(__name__)
    flask_app.load_config()

    flask_app.get_db()
    flask_app.load_error_handler()
    flask_app.load_static_templates()

    from app.reviews.views import reviews_api
    flask_app.register_blueprint(reviews_api)

    from app.shorter.views import links_api
    flask_app.register_blueprint(links_api)

    from app.evotor.views import evotor_api
    flask_app.register_blueprint(evotor_api)

    @flask_app.after_request
    def apply_caching(response):
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response

    return flask_app


def uwsgi_app():
    return get_app(klass=BaseFlaskApp)


if __name__ == '__main__':
    uwsgi_app().run(host='127.0.0.1')
