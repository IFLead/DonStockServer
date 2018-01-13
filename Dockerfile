FROM python:3.6

RUN useradd --system app && \
    mkdir /app && \
    chown app:app /app && \

#COPY web/requirements.txt web/manage.py /app/
COPY web/ /app/

RUN pip install -r /app/web/requirements.txt

RUN ["chmod", "+x", "/app/entrypoint-interface.sh"]
RUN ["chmod", "+x", "/app/entrypoint-worker.sh"]

VOLUME ["/app"]
USER app
WORKDIR /app/web
ENV PYTHONUNBUFFERED 1
