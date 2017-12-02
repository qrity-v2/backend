Принципы работы системы:

* Терминал оплаты (наше приложние) генерит уникальную ссылку
* * Если у терминала есть интернет, то он запрашивает команду сокращения ссылки
* Терминал кодирует ссылку в QR-код
* Терминал печает чек
* При переходе по ссылке или QR-коду дёргается команда "показа формы"

Ограничения
-----------

Доменного имени нет, все запросы делать на IP-адрес `78.155.199.101`

Методы публичного API
=====================

Показать форму для создания отзыва
----------------------------------

...

Показать iFrame для с отчётом для владельца
-------------------------------------------

...

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
curl -X POST 'http://78.155.199.101:5000/short/' -d 'url=https://vk.com/memes_bot'
```
Пример ответа:
```
{
  "result": {
    "key": "07046"
  }
}
```

Получить параметры для отображения формы
----------------------------------------

```
GET /review/params/
```

Пример запроса:
```
curl 'http://78.155.199.101:5000/review/params/'
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

* shop_id - int, ID магазина / пользователя (будет уточнятся). Обязательный параметр
* user_id - int, ID кассира. Обязательный параметр
* rating - int, оценка от 1 до 5
* tags - список тегов, выбранных пользователем. Пример: tags=вкусно&tags=отлично
* text - str, отзыв человека

Пример запроса:
```
curl -X POST 'http://78.155.199.101:5000/review/' -d 'shop_id=1&user_id=1&rating=4&tags=хамят&text=ну+ваще&tags=грязно'
```

Ответ в случае успеха:
```
{'result': 'ok'}
```

...

Интеграция с Evotor
===================

...
