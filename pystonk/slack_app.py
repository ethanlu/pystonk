from pystonk import configuration, logger
from pystonk.api.OptionsChainApi import OptionsChainApi
from pystonk.api.PriceHistoryApi import PriceHistoryApi
from pystonk.api.QuoteApi import QuoteApi
from pystonk.commands.PriceCheckCommand import PriceCheckCommand
from pystonk.commands.PriceHistoryCommand import PriceHistoryCommand
from pystonk.commands.OptionsChainCommand import OptionsChainCommand
from pystonk.lambda_receiver import acknowledgements
from pystonk.views import View
from pystonk.views.HelpView import HelpView

from random import choice
from slack_bolt import App
from slack_sdk import WebClient
from typing import Type

import re


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
client = WebClient(token=configuration['slack']['token'])


def execute_command(text: str) -> Type[View]:
    text = re.sub(r"<.*>", '', text).strip()
    logger.debug(f"matching command for text : {text}")
    for command in commands:
        if command.command_regex.search(text):
            logger.debug(f"selected command : {command.__class__.__name__}")
            return command.execute(text)

    logger.debug(f"no command match...")
    return HelpView([c.help() for c in commands])


def mention(event):
    logger.debug(f"event : `{event}`")

    try:
        view = execute_command(event['text'])

        text_response = view.show_text()
        block_response = view.show()

        logger.debug(f"block : {block_response}")
        logger.debug(f"block length : {len(str(block_response))}")
        logger.debug(f"text : {len(text_response)}")
        client.chat_postMessage(
            channel=event['channel'],
            blocks=block_response,
            text=text_response
        )
    except:
        logger.exception(f"Unexpected error occurred...")


def slash_command(body):
    logger.debug(f"body : `{body}`")

    try:
        view = execute_command(body['text'])

        text_response = view.show_text()
        block_response = view.show()

        logger.debug(f"block : {block_response}")
        logger.debug(f"block length : {len(str(block_response))}")
        logger.debug(f"text : {len(text_response)}")
        client.chat_postEphemeral(
            channel=body['channel_id'],
            user=body['user_id'],
            blocks=block_response,
            text=text_response
        )
    except Exception as e:
        logger.exception(f"Unexpected error occurred...")


def acknowledge(body, ack):
    logger.debug(f"received : `{body}`")
    ack(choice(acknowledgements))


app.command(re.compile(r"^/pystonk(-dev)?$", re.IGNORECASE | re.ASCII))(ack=acknowledge, lazy=[slash_command])
app.event("app_mention")(ack=acknowledge, lazy=[mention])


def start():
    app.start(port=int(configuration['slack']['port']))

