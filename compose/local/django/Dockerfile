FROM python:3.9-slim

RUN apt update -yqq \
    && apt install -yqq software-properties-common \
    && apt install -yqq openssh-server openssh-client libpq-dev

RUN apt update -yqq \
    && apt install -yqq gcc \
                        curl \
                        zip \
                        build-essential \
                        libssl-dev \
                        libffi-dev \
                        libxml2-dev \
                        libxslt1-dev \
                        zlib1g-dev \
                        libgdal-dev \
                        gdal-bin

RUN pip install --upgrade pip

ARG APP_HOME=/app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR ${APP_HOME}

RUN pip install -U pip
RUN pip install virtualenv

# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN pip install -U -r /requirements/local.txt

COPY ./compose/local/django/start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start

COPY ./compose/production/django/requirements.sh /requirements.sh
RUN chmod +x /requirements.sh

COPY ./compose/local/django/celery/worker/start /start-celeryworker
RUN sed -i 's/\r//' /start-celeryworker
RUN chmod +x /start-celeryworker

COPY ./compose/local/django/celery/beat/start /start-celerybeat
RUN sed -i 's/\r//' /start-celerybeat
RUN chmod +x /start-celerybeat

COPY ./compose/local/django/celery/flower/start /start-flower
RUN sed -i 's/\r//' /start-flower
RUN chmod +x /start-flower

COPY ./compose/production/django/entrypoint /entrypoint
RUN sed -i 's/\r//' /entrypoint
RUN chmod +x /entrypoint

COPY . ${APP_HOME}

ENTRYPOINT ["/entrypoint"]
