FROM python:3.9-alpine

WORKDIR /app
ENTRYPOINT ["python"]
EXPOSE 5000

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY start_server.py /app/

CMD ["start_server.py"]
