from pystonk import configuration
from pystonk.api.OptionsChainApi import OptionsChainApi
from pystonk.api.PriceHistoryApi import PriceHistoryApi
from pystonk.api.QuoteApi import QuoteApi
from pystonk.commands.PriceCheckCommand import PriceCheckCommand
from pystonk.commands.PriceHistoryCommand import PriceHistoryCommand
from pystonk.commands.OptionsChainCommand import OptionsChainCommand
from pystonk.utils.LoggerMixin import getLogger
from pystonk.views import View
from pystonk.views.HelpView import HelpView

from slack_bolt import App
from slack_bolt.adapter.aws_lambda import SlackRequestHandler
from slack_sdk import WebClient
from typing import Type

import re

logger = getLogger('pystonk')

apis = {
    'quote': QuoteApi(configuration['app_key'], configuration['app_secret']),
    'price_history': PriceHistoryApi(configuration['app_key'], configuration['app_secret']),
    'options_chain': OptionsChainApi(configuration['app_key'], configuration['app_secret'])
}
commands = (
    PriceCheckCommand(apis['quote']),
    PriceHistoryCommand(apis['quote'], apis['price_history']),
    OptionsChainCommand(apis['quote'], apis['options_chain'])
)

app = App(
    token=configuration['slack']['token'],
    signing_secret=configuration['slack']['secret'],
    logger=logger,
    process_before_response=configuration['slack']['lambda']
)
slack_web_client = WebClient(token=configuration['slack']['token'])


def execute_command(text: str) -> Type[View]:
    text = re.sub(r"<.*>", '', text).strip()
    logger.debug(f"matching command for text : {text}")
    for command in commands:
        if command.command_regex.search(text):
            logger.debug(f"selected command : {command.__class__.__name__}")
            return command.execute(text)

    logger.debug(f"no command match...")
    return HelpView([c.help() for c in commands])


@app.event("app_mention")
def receive_mention(ack, event, body):
    logger.debug(f"event : `{event}`")
    logger.debug(f"body : `{body}`")

    ack("one moment...")

    try:
        view = execute_command(event['text'])

        text_response = view.show_text()
        block_response = view.show()

        logger.debug(f"block : {block_response}")
        logger.debug(f"block length : {len(str(block_response))}")
        logger.debug(f"text : {len(text_response)}")
        slack_web_client.chat_postMessage(
            channel=event['channel'],
            blocks=block_response,
            text=text_response
        )
    except:
        logger.exception(f"Unexpected error occurred...")


@app.command(re.compile(r"^/pystonk(-dev)?$", re.IGNORECASE | re.ASCII))
def receive_slash_command(ack, event, body):
    logger.debug(f"event : `{event}`")
    logger.debug(f"body : `{body}`")

    ack("one moment...")

    try:
        view = execute_command(body['text'])

        text_response = view.show_text()
        block_response = view.show()

        logger.debug(f"block : {block_response}")
        logger.debug(f"block length : {len(str(block_response))}")
        logger.debug(f"text : {len(text_response)}")
        slack_web_client.chat_postEphemeral(
            channel=body['channel_id'],
            user=body['user_id'],
            blocks=block_response,
            text=text_response
        )
    except Exception as e:
        logger.exception(f"Unexpected error occurred...")


def start():
    app.start(port=int(configuration['slack']['port']))


def start_lambda(event, context):
    logger.debug(f"event : `{event}`")
    logger.debug(f"context : `{context}`")
    return SlackRequestHandler(app=app).handle(event, context)


if __name__ == '__main__':
    start()
