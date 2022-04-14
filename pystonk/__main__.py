from pystonk import get_conf_path
from pystonk.api.PriceHistoryApi import PriceHistoryApi
from pystonk.api.OptionsChainApi import OptionsChainApi
from pystonk.api.QuoteApi import QuoteApi
from pystonk.reports.WeeklyPriceChangeReport import WeeklyPriceChangeReport
from pystonk.reports.WeeklyOptionsReport import WeeklyOptionsReport

from termcolor import colored
from pyhocon import ConfigFactory

import argparse


def weekly_price_change_report():
    try:
        pcr = WeeklyPriceChangeReport(PriceHistoryApi(ConfigFactory.parse_file(get_conf_path('app.conf'))['api_key']))

        parser = argparse.ArgumentParser()
        parser.add_argument('symbol', type=str, help='stock symbol')
        parser.add_argument('percent', type=float, help='weekly percent change of stock price to exceed')
        args = parser.parse_args()

        if not args.symbol:
            raise ValueError("Invalid stock symbol : {args.symbol}")

        if not args.percent:
            raise ValueError("Invalid percent threshold : {args.percent}")

        pcr.retrieveData(args.symbol)

        # show results on cli
        print("\n")
        print(f"Symbol : {args.symbol}")
        print(f"Change Threshold : {args.percent}")
        print("\t%10s   %7s   %7s   %8s" % ("Week", "Open", "Close", "% Change"))
        for (group, candlestick) in pcr.generate(args.percent):
            if group == 0:
                date_color = 'white'
                change_color = 'white'
            else:
                date_color = 'yellow'
                change_color = 'green' if candlestick.percentChange >= 0 else 'red'

            print("\t%10s   %7.2f   %7.2f   %8s" % (
                colored(candlestick.startDateTime.strftime('%Y-%m-%d'), date_color),
                candlestick.openPrice,
                candlestick.closePrice,
                colored("{:8.2f}".format(candlestick.percentChange), change_color)
            ))
        print(f"Total Weeks : {pcr.totalWeeks()}")
        print(f"Threshold Exceeded Weeks: {pcr.thresholdExceededWeeksTotal(args.percent)}")
        longest = pcr.longestThresholdExceededWeeks(args.percent)
        if longest:
            print(
                f"Longest Consecutive Threshold Exceeded Weeks: {longest[0][1].startDateTime.strftime('%Y-%m-%d')} to {longest[-1][1].startDateTime.strftime('%Y-%m-%d')} ({len(longest)} weeks)")
    except ValueError as e:
        print(f"Invalid parameter : {str(e)}")
        return

def weekly_options_report():
    try:
        ocr = WeeklyOptionsReport(
            QuoteApi(ConfigFactory.parse_file(get_conf_path('app.conf'))['api_key']),
            OptionsChainApi(ConfigFactory.parse_file(get_conf_path('app.conf'))['api_key'])
        )

        parser = argparse.ArgumentParser()
        parser.add_argument('symbol', type=str, help='stock symbol')
        parser.add_argument('premium', type=float, help='target premium price')
        args = parser.parse_args()

        if not args.symbol:
            raise ValueError("Invalid stock symbol : {args.symbol}")

        if not args.premium:
            raise ValueError("Invalid premium : {args.premium}")

        ocr.retrieveData(args.symbol)

        # show results on cli
        print("\n")
        print(f"Symbol : {args.symbol}")
        print(f"Premium : {args.premium}")
        print("\t%8s   %8s   %12s   %8s   %8s   %8s" % ("Call Bid", "Call Ask", "Strike Price", "% Change", "Put Bid", "Put Ask",))
        for (strike_price, percent_change, call_option, put_option) in ocr.generate():
            print("\t%8.2f   %8.2f   %12.2f   %8s   %8.2f   %8.2f" % (
                call_option.bid,
                call_option.ask,
                float(strike_price),
                colored("{:8.2f}".format(percent_change), 'red' if percent_change < 0 else 'green'),
                put_option.bid,
                put_option.ask
            ))
        print("\t%8s   %8s   %12s   %8s   %8s   %8s\n" % ("Call Bid", "Call Ask", "Strike Price", "% Change", "Put Bid", "Put Ask",))

        (target_call, call_diff, call_percent_change), (target_put, put_diff, put_percent_change) = ocr.getStrikePricesForTargetPremium(args.premium)
        print(f"\t${args.premium} premium call/put strike targets : {target_call.strikePrice} / {target_put.strikePrice}")
        print(f"\t${args.premium} premium call/put strike targets difference : +{call_diff} ({call_percent_change}%) / -{put_diff} ({put_percent_change}%) ")
        print(f"\t${args.premium} premium call/put strike targets skew : {round(call_diff - put_diff, 2)}")

    except ValueError as e:
        print(f"Invalid parameter : {str(e)}")
        return
