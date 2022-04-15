FROM python:3.9.12-alpine3.15

COPY . /opt/app
WORKDIR /opt/app

RUN apk update \
    && apk upgrade \
    && apk add bash \
    && apk add git \
    && python setup.py install

CMD ["tail", "-f", "/dev/null"]