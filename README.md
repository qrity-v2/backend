Система сбора отзывов у конечных покупателей на точках продаж. Мы печатаем на чеках короткую ссылку на форму и QR-код.
На форме можно отметить что именно понравилось или не понравилось. Плохие отзывы уйдут нам в базу, после хороших отзывов
мы попросим человека поделиться своим впечатлением в соц сетях. Владелец бизнеса (терминалов Эвотор) получит мгновенные
оповещения в телеграм о плохих оценках. Позже он сможет подробно посмотреть отчёты в админке

Описание системы:
=================

* Терминал с нашим Android-приложением
* Бот в телеграме для мгновенных оповещений
* Веб-форма для сбора отзывов
* Раздел в админке Эвотора с полным отчётом по всем отзывам

Принципы работы системы:
========================

* Терминал оплаты (наше приложние) генерит уникальную ссылку
* * Если у терминала есть интернет, то он запрашивает команду сокращения ссылки
* Терминал кодирует ссылку в QR-код
* Терминал печает чек
* При переходе по ссылке или QR-коду показывается веб-форма для отзыва

Методы публичного API
=====================

Показать форму для создания отзыва
----------------------------------

```
https://bot-maxim.com/f/?user_id=20171202-F4BF-4034-80E2-5E6F50EC75AF&shop_id=20171202-ED8A-4098-8080-9D2FCCCBFB01
```

Показать iFrame для с отчётом для владельца
-------------------------------------------

```
https://bot-maxim.com/evotor/?token=${token}&uid=${uid}
```

Методы клиентского API
======================

Сократить ссылку
----------------

Ссылка будет действительна сутки

```
POST /short/
```

Параметры тела запроса:
* url - str, ссылка, которую надо сократить

Пример запроса:
```
curl -X POST 'http://78.155.199.101/short/' -d 'url=https://vk.com/memes_bot'
```
Пример ответа:
```
{
  "result": {
    "key": "07046"
  }
}
```

Получить полную ссылку
----------------------

```
GET /s/<key>
```

Где key - получен при сокращении ссылки

Ответ - 302-редирект на полную ссылку

Пример:
```
curl -vvv 'http://78.155.199.101/s/07046'

* Hostname was NOT found in DNS cache
*   Trying 78.155.199.101...
* Connected to 78.155.199.101 (78.155.199.101) port 80 (#0)
> GET /s/07046 HTTP/1.1
> User-Agent: curl/7.38.0
> Host: 78.155.199.101
> Accept: */*
>
< HTTP/1.1 302 FOUND
* Server nginx/1.4.6 (Ubuntu) is not blacklisted
< Server: nginx/1.4.6 (Ubuntu)
< Date: Sat, 02 Dec 2017 15:52:46 GMT
< Content-Type: text/html; charset=utf-8
< Content-Length: 255
< Connection: keep-alive
< Location: https://vk.com/memes_bot
< Access-Control-Allow-Origin: *
```

Получить параметры для отображения формы
----------------------------------------

```
GET /review/params/
```

Пример запроса:
```
curl 'http://78.155.199.101/review/params/'
```

Пример ответа:
```
{
  "result": {
    "tags_good": [
      "вкусно",
      "очень красиво",
      "превосходный сервис"
    ],
    "tags_bad": [
      "грубят",
      "грязно",
      "не вкусно",
      "обманули"
    ],
    "shop_name": "Кофейня №1 в Москве"
  }
}
```

Сохранить форму с отзывом
-------------------------

```
POST /review/
```

Параметры тела запроса:

* shop_id - int, ID магазина. Обязательный параметр
* user_id - int, ID кассира. Обязательный параметр
* rating - int, оценка от 1 до 5
* tags - список тегов, выбранных пользователем. Пример: tags=вкусно&tags=отлично
* text - str, отзыв человека

Пример запроса:
```
curl -X POST 'http://78.155.199.101/review/' -d 'shop_id=1&user_id=1&rating=4&tags=хамят&text=ну+ваще&tags=грязно'
```

Ответ в случае успеха:
```
{'result': 'ok'}
```

Интеграция с Evotor
===================

Получить отчёт по отзывам
-------------------------

```
GET /evotor/report/
```

Параметры запроса:

* token - str, токен пользователя Эвотора
* uid - int, ID пользователя Эвотора

Пример ответа:
```
{
  "result": [
    {
      "user_id": "20171202-7A01-4024-80A9-1722C36BCB5C",
      "store_id": "20171202-ED8A-4098-8080-9D2FCCCBFB01",
      "first_name": "Петя",
      "last_name": "Иванов",
      "phone": "8 800 555 35 55",
      "rating": 3,
      "tags": [
        "плохо",
        "не вкусно",
      ],
      "text": "ну пиздец",
      "timestamp": 1512222456,
    },
    {
      "user_id": "20171202-7A01-4024-80A9-1722C36BCB5A",
      "store_id": "20171202-ED8A-4098-8080-9D2FCCCBFB02",
      "first_name": "Василий",
      "last_name": null,
      "phone": null,
      "rating": 5,
      "tags": [
        "круто",
      ],
      "text": null,
      "timestamp": 1512222567,
    }
  ]
}
```
