FROM python:3.10

ADD rest-server.py /

RUN pip install --upgrade pip
RUN pip install redis jsonpickle requests flask minio

CMD mkdir /app
WORKDIR /app

COPY . /app

EXPOSE 5000
CMD cd /app && \
    python3 rest-server.py