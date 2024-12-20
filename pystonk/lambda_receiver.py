from pystonk import configuration, logger

from random import choice
from slack_bolt import App
from slack_bolt.adapter.aws_lambda import SlackRequestHandler
from slack_sdk import WebClient

import boto3
import json
import re


acknowledgements = (
    "Absolutely!", "Acknowledged HQ.", "Affirmative, sir!", "Affirmative.", "All right!", "As you will.", "Commencing!", "Commencing.", "Confirmed.",
    "Delighted to, sir!", "Excellent!", "Excellent.", "Haha! At last!", "Honor guide me!", "I copy that.", "I dig.", "I hear that.", "I'm all over it.",
    "I'm goin!", "I'm gone.", "I'm on the job.", "Immediately!", "In the pipe, five by five.", "In transit HQ.", "Initiating.", "It shall be done.",
    "It will be done.", "It's show time!", "Let's roll.", "Locus acknowledged.", "Make it happen.", "Move it!", "My path is set.", "Naturally.",
    "Navcom locked.", "No problem.", "No sweat!", "Of course, mein Herr!", "Of course.", "Oh, is that it?", "On my way!", "Orders received.",
    "Outstanding!", "Perfect!", "Proceedin'", "Right away, sir.", "Right away.", "Rock and roll", "Roger that.", "Roger.", "Set a course.", "Slammin'!",
    "So be it.", "Stat!", "Sure thing!", "Target designated.", "Thus I serve!", "Vector locked in.", "Very well.", "We move.", "Yeah, I'm goin'!",
    "Yep!", "You got it.", "You think as I do."
)

app = App(
    token=configuration['slack']['token'],
    signing_secret=configuration['slack']['secret'],
    logger=logger,
    process_before_response=configuration['slack']['lambda']
)
client = WebClient(token=configuration['slack']['token'])
lambda_client = boto3.client('lambda', region_name=configuration['aws']['region'])


@app.event("app_mention")
def receive_mention(ack, event):
    logger.debug(f"event : `{event}`")

    logger.debug(f"passing request to aws lambda arn : `{configuration['aws']['lambda_arn']}`")
    # pass payload to the second lambda to do the processing
    lambda_client.invoke(
        FunctionName=configuration['aws']['lambda_arn'],
        InvocationType='Event',
        Payload=json.dumps({'f': 'mention', 'p': event})
    )

    # but respond immediately so that slack does not cancel the request
    response = choice(acknowledgements)
    ack(response)
    client.chat_postMessage(
        channel=event['channel'],
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": response
                }
            }
        ],
        text=response
    )


@app.command(re.compile(r"^/pystonk(-dev)?$", re.IGNORECASE | re.ASCII))
def receive_slash_command(ack, body):
    logger.debug(f"body : `{body}`")

    logger.debug(f"passing request to aws lambda arn : `{configuration['aws']['lambda_arn']}`")
    # call the second lambda to do the processing
    lambda_client.invoke(
        FunctionName=configuration['aws']['lambda_arn'],
        InvocationType='Event',
        Payload=json.dumps({'f': 'slash_command', 'p': body})
    )

    # but respond immediately so that slack does not cancel the request
    ack(choice(acknowledgements))


def start(event, context):
    logger.debug(f"event : `{event}`")
    logger.debug(f"context : `{context}`")
    return SlackRequestHandler(app=app).handle(event, context)
