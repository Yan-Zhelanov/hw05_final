# Yatube
Социальная сеть для публикации блогов.

Разработан по MVT архитектуре. Регистрация реализована с верификацией данных, сменой и восстановлением пароля через почту. Используется пагинация постов и кеширование. Написаны тесты, проверяющие работу сервиса.

## Установка
Создайте виртуальное окружение:
```bash
python -m venv venv
```
Активируйте его:
```bash
source venv/Scripts/activate
```
Используйте [pip](https://pip.pypa.io/en/stable/), чтобы установить зависимости:
```bash
pip install -r requirements.txt
```
После примените все миграции:
```bash
python manage.py migrate
```
И запускайте сервер:
```bash
python manage.py runserver
```

## Стек технологий
Python 3.6+, Django 3.1, SQLite3, unittest.
