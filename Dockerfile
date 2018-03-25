FROM python:3.6

ENV APP_USER donstock
ENV APP_ROOT /donstock
RUN mkdir /donstock
RUN groupadd -r ${APP_USER} \
    && useradd -r -m \
    --home-dir ${APP_ROOT} \
    -s /usr/sbin/nologin \
    -g ${APP_USER} ${APP_USER}

WORKDIR ${APP_ROOT}

ADD . ${APP_ROOT}

RUN pip install -r requirements.txt

RUN chmod -R 777 media

RUN chmod -R 777 static

RUN python manage.py collectstatic --noinput

USER ${APP_USER}
