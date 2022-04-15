from pystonk import get_conf_path
from pystonk.api.PriceHistoryApi import PriceHistoryApi
from pystonk.api.OptionsChainApi import OptionsChainApi
from pystonk.api.QuoteApi import QuoteApi
from pystonk.reports.WeeklyPriceChangeReport import WeeklyPriceChangeReport
from pystonk.reports.WeeklyOptionsReport import WeeklyOptionsReport
from pystonk.view.TerminalView import TerminalView

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
            symbol = str(input())
            if not symbol:
                raise ValueError("Invalid stock symbol : {args.symbol}")

            print("Enter percent change threshold : ", end='')
            percent = abs(round(float(input()), 2))
            if not percent:
                raise ValueError("Invalid percent change threshold : {args.percent}")

            view = TerminalView()
            view.showPriceHistory(WeeklyPriceChangeReport(PriceHistoryApi(ConfigFactory.parse_file(get_conf_path('app.conf'))['api_key'])), symbol, percent)

        elif report == 2:
            print("Enter stock symbol : ", end='')
            symbol = str(input())
            if not symbol:
                raise ValueError("Invalid stock symbol : {args.symbol}")

            print("Enter target premium : ", end='')
            premium = abs(round(float(input()), 2))

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