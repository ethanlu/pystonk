FROM public.ecr.aws/lambda/python:3.9

COPY . /opt/app
WORKDIR /opt/app

# remove custom app.conf if it exists
RUN rm -rf /opt/app/pystonk/conf/app.conf

RUN pip install --no-cache-dir --upgrade pip \
    && python setup.py develop

CMD [ "pystonk.slack_app.slack_lambda_receiver" ]