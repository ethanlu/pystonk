FROM python:3.9-slim

COPY . /opt/app
WORKDIR /opt/app

RUN apt-get update

RUN pip install --no-cache-dir --upgrade pip \
    && python setup.py develop

ENTRYPOINT ["bin/bash", "docker/entrypoint.sh"]