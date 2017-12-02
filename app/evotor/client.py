# coding: utf-8
""" API-клиент для Облака Эвотора
"""
import json

import requests


class EvotorClient(object):
    TEST_UID = '01-000000000544555'
    TEST_TOKEN = 'a705a157-039c-47cc-9515-f93bd24c81a6'

    def __init__(self, token=None, uid=None):
        self.token = token
        self.uid = uid

    def _request(self, method, url, params=None, data=None, verify=True):
        headers = {
            'X-Authorization': self.token or self.TEST_TOKEN,
        }
        res = requests.request(method=method, url=url, params=params, data=data, verify=verify, headers=headers)
        if 200 <= res.status_code <= 300:
            return res
        print 'error: {}'.format(res.status_code)

    def get_employers_list(self):
        url = 'https://api.evotor.ru/api/v1/inventories/employees/search'
        data = self._request(method='GET', url=url)
        if data:
            data = data.json()
            return data
        return []

    def get_shop_list(self):
        url = 'https://api.evotor.ru/api/v1/inventories/stores/search'
        data = self._request(method='GET', url=url)
        if data:
            data = data.json()
            return data
        return []


if __name__ == '__main__':
    cli = EvotorClient()
    print [i['uuid'] for i in cli.get_employers_list()]
    print [i['uuid'] for i in cli.get_shop_list()]

    # https://bot-maxim.com/f/?user_id=01-000000000544555&shop_id=20171202-ED8A-4098-8080-9D2FCCCBFB01
