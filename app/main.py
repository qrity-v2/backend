# coding: utf-8
import os
import logging
import logging.config
import json

import mongoengine
from flask import Flask
from flask import Response
from flask import jsonify
from werkzeug.exceptions import HTTPException

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

    def load_error_handler(self):
        self.register_error_handler(
            ApiException,
            handle_exception_with_as_dict_method
        )

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
        return super(BaseFlaskApp, self).make_response((rv, status, headers))


def get_app(klass):
    assert issubclass(klass, BaseFlaskApp)
    flask_app = klass(__name__)
    flask_app.load_config()

    flask_app.get_db()
    flask_app.load_error_handler()

    from app.reviews.views import reviews_api
    flask_app.register_blueprint(reviews_api)

    # from app.shorter.views import links_api
    # flask_app.register_blueprint(links_api)

    return flask_app


def uwsgi_app():
    return get_app(klass=BaseFlaskApp)


if __name__ == '__main__':
    uwsgi_app().run(host='0.0.0.0')
