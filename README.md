# Stripe Payment Task

## Table of contents
- [Stripe Payment Task](#stripe-payment-task)
  - [Table of contents](#table-of-contents)
  - [Setup](#setup)
  - [App Logic](#app-logic)
    - [Main Tasks](#main-tasks)
  - [run in dev environment](#run-in-dev-environment)
  - [Run it with docker](#run-it-with-docker)
  - [run test files](#run-test-files)

## Setup
1. install pipenv 
```
pip install pipenv
```
2. установить необходимые пакеты и активировать venv
```
pipenv install
pipenv shell
```

## App Logic
смоделировать магазин электронной коммерции, где покупатель может выбрать товар и купить его с помощью Stripe.

### Main Tasks
- [x] созданы основные views 
- [x] целевая страница для перечисления всех предметов
- [x] целевая страница для перечисления всех предметов
- [x] интегрированный Stripe PaymentIntent
- [x] докеризировал приложение
- [x] используемые переменные окружения
- [x] зарегистрированные модели в админке Django
- [x] созданное приложение «Заказать»
- [x] протестировано большинство компонентов приложения
- [x] отдельный уровень взаимодействия с базой данных на сервисы
- [x] Задокументирована большая часть кода приложения
- [x] загрузил приложение на удаленный сервер

## run in dev environment

1. перенести базу данных
```
python manange.py migrate
```
2. запустить сервер разработки
```
python manange.py runserver 8000
```
3. загрузить предварительно заполненные данные в базу данных
```
python manange.py loaddata fixtures.json
```


## Run it with docker
1. docker compose up
```
docker-compose --file docker-compose-local.yml --project-name=stripe_payment_task up
```
2. docker compose down
```
docker-compose --file docker-compose-local.yml --project-name=stripe_payment_task down
```

## run test files
1. установить зависимости от разработчиков
```
pipenv install --dev
```
2. запустить все тестовые файлы в проекте
```
pytest --cache-clear --capture=no --showlocals --verbose
```