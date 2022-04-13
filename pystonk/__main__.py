from pystonk import get_conf_path
from pystonk.api.PriceHistory import PriceHistory
from pystonk.reports.WeeklyPriceChangeReport import WeeklyPriceChangeReport

from termcolor import colored
from pyhocon import ConfigFactory
from typing import Dict

import argparse, sys


def weekly_price_change_report():
    pcr = WeeklyPriceChangeReport(PriceHistory(ConfigFactory.parse_file(get_conf_path('app.conf'))['api_key']))

    parser = argparse.ArgumentParser()
    parser.add_argument('symbol', type=str, help='stock symbol')
    parser.add_argument('percent', type=float, help='weekly percent change of stock price to exceed')
    args = parser.parse_args()

    if not args.symbol:
        print("Invalid stock symbol")
        sys.exit(1)

    if not args.percent:
        print("Invalid percent threshold")
        sys.exit(1)

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
        print(f"Longest Consecutive Threshold Exceeded Weeks: {longest[0][1].startDateTime.strftime('%Y-%m-%d')} to {longest[-1][1].startDateTime.strftime('%Y-%m-%d')} ({len(longest)} weeks)")

def weekly_options_report():
    pass
