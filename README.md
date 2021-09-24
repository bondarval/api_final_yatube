# API для проекта Yatube
### Описание
Представляет собой расширение возможностей проекта Yatube для совершения удаленных операций.   
Благодаря этому проекту зарегистрированные и аутентифицированные пользователи получат возможность опубликовать личные дневники, подписаться на авторов других дневников и комментировать их записи.
Предоставлена возможность делать это без непосредственного входа на сайт с помощью запросов к API сайта.
### Технологии
 - Python 3.7
 - Django 2.2.19
 - REST Framework 3.12.4
 - JWT Djoser 2.1.0
### Установка
- Установить и активировать виртуальное окружение
- Установить зависимости из файла requirements.txt
```
pip install -r requirements.txt
``` 
- В папке с файлом manage.py выполнить команду:
```
python manage.py runserver
```
### Примеры API-запросов
 - Запрос на создание поста:
POST http://127.0.0.1:8000/api/v1/posts/ {
  "text": "string",
  "image": "string",
  "group": 0
}
 - Запрос на получение поста по id: GET http://127.0.0.1:8000/api/v1/posts/{id}/
 - Запрос на получение информации о конкретном сообществе: GET http://127.0.0.1:8000/api/v1/groups/{id}/
### Автор
Валерий А. Бондарь