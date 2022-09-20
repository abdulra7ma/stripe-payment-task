# Stripe Payment Task

## Table of contents
- [Stripe Payment Task](#stripe-payment-task)
  - [Table of contents](#table-of-contents)
  - [App Logic](#app-logic)
    - [Main Tasks](#main-tasks)
  - [run in dev environment](#run-in-dev-environment)
  - [Run docker for production](#run-docker-for-production)
  - [run test files](#run-test-files)



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

1. Создайте образ Docker
```
docker-compose build
```
2. запустить образ Docker
```
docker-compose up
```
3. остановить образ Docker
```
docker-compose down
```


## Run docker for production


1. Создайте образ Docker
```
docker-compose --file docker-compose.prod.yml --project-name=stripe_payment_task build
```
2. 
```
docker-compose --file docker-compose.prod.yml --project-name=stripe_payment_task up
```
3. docker compose down
```
docker-compose --file docker-compose.prod.yml --project-name=stripe_payment_task down
```
- для удаления томов при остановке контейнеров
   ```
   docker-compose --file docker-compose.prod.yml --project-name=stripe_payment_task down -v --remove-orphans
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