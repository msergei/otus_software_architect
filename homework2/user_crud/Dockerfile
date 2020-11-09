FROM python:alpine
ENV PYTHONUNBUFFERED 1

RUN apk update && \
    apk add postgresql-dev gcc python3-dev musl-dev zlib-dev && \
    pip install -U pip

ADD requirements.txt /

RUN pip install -r /requirements.txt

WORKDIR /app

ADD user_crud /app/user_crud/
ADD users /app/users/
ADD manage.py /app/

EXPOSE 8000

CMD ["./manage.py", "runserver", "0.0.0.0:8000"]
