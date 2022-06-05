from pystonk import get_conf_path
from pystonk.utils.LoggerMixin import getLogger

from pyhocon import ConfigFactory
from slack_bolt import App
from slack_bolt.adapter.aws_lambda import SlackRequestHandler
from typing import Callable, Dict

import boto3
import json
import re

config = ConfigFactory.parse_file(get_conf_path())
logger = getLogger('pystonk')
app = App(
    token=config['slack']['token'],
    signing_secret=config['slack']['secret'],
    logger=logger,
    process_before_response=False
)
lambda_client = boto3.client('lambda', region_name=config['aws']['region'])


def dispatch_reponse(ack: Callable, payload: Dict) -> None:
    logger.debug(f"aws lambda arn is `{config['aws']['lambda_arn']}`")
    lambda_client.invoke(
        FunctionName=config['aws']['lambda_arn'],
        InvocationType='Event',
        Payload=json.dumps(payload)
    )
    ack("one moment...")


@app.event("app_mention")
def receive_mention(ack, event, body):
    logger.debug(f"event : `{event}`")
    logger.debug(f"body : `{body}`")

    dispatch_reponse(
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

    dispatch_reponse(
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
