from pystonk.di import Container
from pystonk.utils.LoggerMixin import getLogger

from slack_bolt import App
from slack_bolt.adapter.aws_lambda import SlackRequestHandler
from typing import Callable, Dict

import boto3
import json
import re

logger = getLogger('pystonk')
app = App(
    token=Container.configuration()['slack']['token'],
    signing_secret=Container.configuration()['slack']['secret'],
    logger=logger,
    process_before_response=Container.configuration()['slack']['lambda']
)
lambda_client = boto3.client('lambda', region_name=Container.configuration()['aws']['region'])


def dispatch_response(ack: Callable, payload: Dict) -> None:
    logger.debug(f"aws lambda arn is `{Container.configuration()['aws']['lambda_arn']}`")
    # call the second lambda to do the processing
    lambda_client.invoke(
        FunctionName=Container.configuration()['aws']['lambda_arn'],
        InvocationType='Event',
        Payload=json.dumps(payload)
    )
    # but respond immediately so that slack does not cancel the request
    ack("one moment...")


@app.event("app_mention")
def receive_mention(ack, event, body):
    logger.debug(f"event : `{event}`")
    logger.debug(f"body : `{body}`")

    dispatch_response(
        ack,
        {
            "f": "respond_mention",
            "p": [event['text'], event['channel']]
        }
    )


@app.command(re.compile(r"^/pystonk(-dev)?$", re.IGNORECASE | re.ASCII))
def receive_slash_command(ack, event, body):
    logger.debug(f"event : `{event}`")
    logger.debug(f"body : `{body}`")

    dispatch_response(
        ack,
        {
            "f": "respond_slash_command",
            "p": [body['text'], body['user_id'], body['channel_id']]
        }
    )


def slack_receiver(event, context):
    logger.debug(f"event : `{event}`")
    logger.debug(f"context : `{context}`")
    return SlackRequestHandler(app=app).handle(event, context)
