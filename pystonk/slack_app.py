from pystonk.di import Container
from pystonk.utils.LoggerMixin import getLogger
from pystonk.views import View
from pystonk.views.HelpView import HelpView

from slack_bolt import App
from slack_sdk import WebClient
from typing import Callable, Dict, Type

import re
import sys

logger = getLogger('pystonk')
app = App(
    token=Container.configuration()['slack']['token'],
    signing_secret=Container.configuration()['slack']['secret'],
    logger=logger,
    process_before_response=Container.configuration()['slack']['lambda']
)
slack_web_client = WebClient(token=Container.configuration()['slack']['token'])


def execute_command(text: str) -> Type[View]:
    text = re.sub(r"<.*>", '', text).strip()
    logger.debug(f"matching command for text : {text}")
    for command in Container.available_commands():
        if command.command_regex.search(text):
            logger.debug(f"selected command : {command.__class__.__name__}")
            return command.execute(text)

    logger.debug(f"no command match...")
    return HelpView([c.help() for c in Container.available_commands()])


def dispatch_response(ack: Callable, payload: Dict) -> None:
    ack("one moment...")
    slack_responder(payload, None)


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


def respond_mention(text: str, channel_id: str):
    try:
        view = execute_command(text)

        text_response = view.show_text()
        block_response = view.show()

        logger.debug(f"block : {block_response}")
        logger.debug(f"block length : {len(str(block_response))}")
        logger.debug(f"text : {len(text_response)}")
        slack_web_client.chat_postMessage(
            channel=channel_id,
            blocks=block_response,
            text=text_response
        )
    except:
        logger.error(f"Unexpected error occurred: {sys.exc_info()}")


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


def respond_slash_command(text: str, user_id: str, channel_id: str):
    try:
        view = execute_command(text)

        text_response = view.show_text()
        block_response = view.show()

        logger.debug(f"block : {block_response}")
        logger.debug(f"block length : {len(str(block_response))}")
        logger.debug(f"text : {len(text_response)}")
        slack_web_client.chat_postEphemeral(
            channel=channel_id,
            user=user_id,
            blocks=block_response,
            text=text_response
        )
    except Exception as e:
        logger.error(f"Unexpected error occurred: {sys.exc_info()}")


def slack_responder(event, context):
    logger.debug(event)
    logger.debug(context)

    f = globals()[event['f']]
    f(*event['p'])


def start():
    app.start(port=int(Container.configuration()['slack']['port']))


if __name__ == '__main__':
    start()
