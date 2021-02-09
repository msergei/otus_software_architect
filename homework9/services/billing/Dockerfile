FROM python:alpine
ENV PYTHONUNBUFFERED 1

RUN apk update && \
    apk add postgresql-dev gcc python3-dev musl-dev zlib-dev jpeg-dev openssl-dev libffi-dev && \
    pip install -U pip

ADD requirements.txt /

RUN pip install -r /requirements.txt
RUN pip install gunicorn

WORKDIR /app

COPY ./billing /app/billing
COPY ./manage.py /app/manage.py

EXPOSE 8000
