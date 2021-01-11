FROM python:3-alpine

EXPOSE 8080
COPY requirements.txt /requirements.txt
RUN apk update && apk add gcc libc-dev
RUN pip install -U pip && pip install --no-cache-dir -r requirements.txt

COPY app.py /app.py

CMD ["python", "/app.py"]
