FROM public.ecr.aws/lambda/python:3.9

COPY . /opt/app
WORKDIR /opt/app

RUN pip install --no-cache-dir --upgrade pip \
    && python setup.py develop

CMD [ "pystonk.slack_app.slack_lambda_receiver" ]