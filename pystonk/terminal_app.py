from pystonk import get_conf_path
from pystonk.api.PriceHistoryApi import PriceHistoryApi
from pystonk.api.OptionsChainApi import OptionsChainApi
from pystonk.api.QuoteApi import QuoteApi
from pystonk.reports.WeeklyPriceChangeReport import WeeklyPriceChangeReport
from pystonk.reports.WeeklyOptionsReport import WeeklyOptionsReport
from pystonk.view.TerminalView import TerminalView
from pystonk.utils import is_float

from pyhocon import ConfigFactory


def terminal():
    try:
        print("Available Reports")
        print("\t1: Weekly Price History")
        print("\t2: Weekly Options Chain")
        print("Choose report : ", end='')
        report = int(input())

        if report == 1:
            print("Enter stock symbol : ", end='')
            symbol = str(input()).upper()
            if not symbol:
                raise ValueError(f"Invalid stock symbol : {symbol}")

            print("Enter percent change threshold : ", end='')
            percent = input()
            if not percent or not is_float(percent):
                raise ValueError(f"Invalid percent change threshold : {percent}")
            percent = abs(round(float(percent), 2))

            view = TerminalView()
            view.showPriceHistory(WeeklyPriceChangeReport(PriceHistoryApi(ConfigFactory.parse_file(get_conf_path('app.conf'))['api_key'])), symbol, percent)

        elif report == 2:
            print("Enter stock symbol : ", end='')
            symbol = str(input()).upper()
            if not symbol:
                raise ValueError(f"Invalid stock symbol : {symbol}")

            print("Enter target premium : ", end='')
            premium = input()
            if not premium or not is_float(premium):
                raise ValueError(f"Invalid target premium : {premium}")
            premium = abs(round(float(premium), 2))

            view = TerminalView()
            view.showOptionsChain(
                WeeklyOptionsReport(QuoteApi(ConfigFactory.parse_file(get_conf_path('app.conf'))['api_key']), OptionsChainApi(ConfigFactory.parse_file(get_conf_path('app.conf'))['api_key'])),
                symbol,
                premium
            )
        else:
            raise ValueError('Invalid report number')
    except ValueError as e:
        print(str(e))