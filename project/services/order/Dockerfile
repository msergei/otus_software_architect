FROM python:alpine
ENV PYTHONUNBUFFERED 1

RUN apk add --update \
  build-base \
  cairo \
  cairo-dev \
  cargo \
  freetype-dev \
  gcc \
  gdk-pixbuf-dev \
  gettext \
  jpeg-dev \
  lcms2-dev \
  libffi-dev \
  musl-dev \
  openjpeg-dev \
  openssl-dev \
  pango-dev \
  poppler-utils \
  postgresql-client \
  postgresql-dev \
  py-cffi \
  python3-dev \
  rust \
  tcl-dev \
  tiff-dev \
  tk-dev \
  zlib-dev &&\
  pip install -U pip

ADD requirements.txt /

RUN pip install -r /requirements.txt
RUN pip install gunicorn

WORKDIR /app

COPY ./order /app/order
COPY ./manage.py /app/manage.py

EXPOSE 8000
