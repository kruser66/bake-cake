# Проект BakeCake

Продажа тортов на заказ

## Как установить

Python 3 должен быть установлен.

- Скачать проект.
- Создать виртуальное окружение.

```bash
python -m venv venv
```

- Установить зависимости.

```bash
pip install -r requirements.txt
```

- Накатить миграции.

```bash
python manage.py migrate
```

- Создать суперпользователя.

```bash
python manage.py createsuperuser
```

## Запуск проекта

### Установить переменные окружения

- для работы сайта Django:

```python
SECRET_KEY=YOUR_SECRET_KEY
ALLOWED_HOSTS=YOUR_HOST_NAME_OR_ADDRESS
```

### Старт проекта

```bash
python manage.py runserver
```

Сайт будет доступен по адресу: `http://127.0.0.1:8000/`

## Цель проекта

Проект создан в учебных целях на курсе [От новичка до мидл Python/Django разработчика](https://dvmn.org/)
