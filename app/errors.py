# coding: utf-8


class ApiException(Exception):
    """Ошибка обращения к серверу"""
    code = 1
    text = u'unknown error'

    def jsonify(self):
        return {
            'error': {
                'code': self.code,
                'text': self.text,
            },
        }


class BadFormException(ApiException):
    code = 2
    text = u'bad form'
