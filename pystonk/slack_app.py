from pystonk import get_conf_path
from pystonk.api.PriceHistoryApi import PriceHistoryApi
from pystonk.api.OptionsChainApi import OptionsChainApi
from pystonk.api.QuoteApi import QuoteApi
from pystonk.reports.WeeklyPriceChangeReport import WeeklyPriceChangeReport
from pystonk.reports.WeeklyOptionsReport import WeeklyOptionsReport
from pystonk.view.SlackView import SlackView
from pystonk.utils.LoggerMixin import getLogger

from pyhocon import ConfigFactory
from slack_bolt import App
from slack_bolt.adapter.aws_lambda import SlackRequestHandler
from typing import Tuple

import re


config = ConfigFactory.parse_file(get_conf_path('app.conf'))
app = App(
    token=config['slack']['token'],
    signing_secret=config['slack']['secret'],
    logger=getLogger('pystonk'),
    process_before_response=config['slack']['lambda']
)


def pc_handler(*args) -> Tuple:
    try:
        symbol = args[0].upper()
        api = QuoteApi(config['api_key'])
        price = api.getQuote(symbol)

        return f"{symbol} is currently {round(float(price), 2) if price else 'not found'}", SlackView().showPriceCheck(symbol, price)
    except Exception as e:
        return SlackView().showUnexpectedError(str(e))


def ph_handler(*args) -> Tuple:
    try:
        symbol = args[0].upper()
        percent = abs(round(float(args[1]), 2))
        r = WeeklyPriceChangeReport(
            PriceHistoryApi(config['api_key'])
        )
        r.retrieveData(symbol)

        view = SlackView()
        response = view.showPriceHistory(
            symbol=symbol,
            percent=percent,
            data=r.generate(percent),
            total_weeks=r.totalWeeks(),
            exceeded_weeks=r.thresholdExceededWeeksTotal(percent),
            longest_weeks=r.longestThresholdExceededWeeks(percent)
        )

        return f"price history for {symbol} with {percent} threshold", response
    except Exception as e:
        return SlackView().showUnexpectedError(str(e))


def oc_handler(*args) -> Tuple:
    try:
        symbol = args[0].upper()
        premium = abs(round(float(args[1]), 2))
        r = WeeklyOptionsReport(
            QuoteApi(config['api_key']),
            OptionsChainApi(config['api_key'])
        )
        r.retrieveData(symbol)

        view = SlackView()
        response = view.showOptionsChain(
            symbol=symbol,
            premium=premium,
            current_price=r.getMark(),
            data=r.generate(),
            sell_options=r.getStrikePricesForTargetPremium(premium),
            buy_options=r.getStrikePricesForTargetPremium(premium, is_sell=False)
        )

        return f"option chain for {symbol} with {premium} premium", response
    except Exception as e:
        return SlackView().showUnexpectedError(str(e))


def parse_command(text: str) -> Tuple:
    text = re.sub(r"<.*>", '', text).strip()
    for regex, handler in commands:
        r = regex.search(text)
        if r:
            return handler, r.groups()
    return None, None


def send_ack(body, ack):
    ack("one moment...")


@app.event("app_mention")
def mention(client, event, logger):
    try:
        logger.debug(event)
        view = SlackView()
        handler, args = parse_command(event['text'])
        if not handler:
            text_response = "Invalid command"
            block_response = view.showAvailableCommands()
        else:
            response = handler(*args)
            text_response = response[0]
            block_response = response[1]

        logger.debug(f"channel : {event['channel']}")
        logger.debug(f"block : {block_response}")
        logger.debug(f"block length : {len(str(block_response))}")
        logger.debug(f"text : {len(text_response)}")
        client.chat_postMessage(
            channel=event['channel'],
            blocks=block_response,
            text=text_response
        )
    except Exception as e:
        logger.error(f"Error publishing mention: {e}")


def slash_command(respond, body):
    try:
        logger = getLogger('pystonk')
        logger.debug(body)

        view = SlackView()
        handler, args = parse_command(body['text'] if 'text' in body else '')
        if not handler:
            text_response = "Invalid command"
            block_response = view.showAvailableCommands()
        else:
            response = handler(*args)
            text_response = response[0]
            block_response = response[1]

        logger.debug(f"block : {block_response}")
        logger.debug(f"block length : {len(str(block_response))}")
        logger.debug(f"text : {len(text_response)}")
        respond(
            blocks=block_response,
            text=text_response
        )
    except Exception as e:
        logger.error(f"Error publishing mention: {e}")


app.command("/pystonk")(
    ack=send_ack,
    lazy=[slash_command]
)


def lambda_handler(event, context):
    return SlackRequestHandler(app=app).handle(event, context)


def start():
    app.start(port=int(config['slack']['port']))


commands = (
    (
        re.compile(r"^pc ([a-zA-Z.]+)$", re.IGNORECASE | re.ASCII),
        pc_handler
    ),
    (
        re.compile(r"^ph ([a-zA-Z.]+) (\d*\.?\d*)$", re.IGNORECASE | re.ASCII),
        ph_handler
    ),
    (
        re.compile(r"^oc ([a-zA-Z.]+) (\d*\.?\d*)$", re.IGNORECASE | re.ASCII),
        oc_handler
    )
)


if __name__ == '__main__':
    start()
