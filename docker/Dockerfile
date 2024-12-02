FROM python:3.9-slim

COPY . /opt/app
WORKDIR /opt/app

# remove custom app.conf if it exists
RUN rm -rf /opt/app/pystonk/conf/app.conf

RUN pip install --no-cache-dir --upgrade pip \
    && python -m pip install --editable .[tests]

CMD [ "pystonk.slack_app.start" ]