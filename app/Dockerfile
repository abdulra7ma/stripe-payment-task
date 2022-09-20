FROM python:3.10-alpine

# set work directory
WORKDIR /usr/src/app

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

# Install pipenv and compilation dependencies
RUN pip install pipenv
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# Install python dependencies in /usr/src/app/.venv
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

# copy project
COPY . .

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]