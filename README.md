# School Site

## Table of contents
- [School Site](#school-site)
  - [Table of contents](#table-of-contents)
  - [Setup](#setup)
  - [APP-LOGIC](#app-logic)
    - [Main features](#main-features)
  - [run in dev environment](#run-in-dev-environment)
  - [Run it with docker](#run-it-with-docker)
  - [run test files](#run-test-files)

## Setup
1. install pipenv 
```
pip install pipenv

```
2. install needed packages and activate the venv
```
pipenv install
pipenv shell
```

## APP-LOGIC
Simple school system where a teacher could add/edit/delete a student

### Main features
1. notify student by email after been added to one class
2. teacher is able to login by phone number

## run in dev environment

1. migrate database
```
python manange.py migrate
```
2. run development server
```
python manange.py runserver
```


## Run it with docker
1. docker compose up
```
docker-compose --file docker-compose-local.yml --project-name=school_site up
```
2. docker compose down
```
docker-compose --file docker-compose-local.yml --project-name=school_site down
```

## run test files
1. install dev dependencies
```
pipenv install --dev
```
2. run all test files in the project
```
pytest --cache-clear --capture=no --showlocals --verbose
```