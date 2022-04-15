from pystonk import get_conf_path
from pystonk.api.PriceHistoryApi import PriceHistoryApi
from pystonk.api.OptionsChainApi import OptionsChainApi
from pystonk.api.QuoteApi import QuoteApi
from pystonk.reports.WeeklyPriceChangeReport import WeeklyPriceChangeReport
from pystonk.reports.WeeklyOptionsReport import WeeklyOptionsReport
from pystonk.utils import format_colored_number

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
                percent_change = format_colored_number(candlestick.percentChange, candlestick.percentChange)
            else:
                date_color = 'yellow'
                percent_change = format_colored_number(candlestick.percentChange, 0)

            print("\t%10s   %7.2f   %7.2f   %8s" % (
                colored(candlestick.startDateTime.strftime('%Y-%m-%d'), date_color),
                candlestick.openPrice,
                candlestick.closePrice,
                percent_change
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

        c = ocr.retrieveData(args.symbol)
        if c:
            print("\t%8s   %8s   %12s   %8s   %8s   %8s" % ("Call Bid", "Call Ask", "Strike Price", "% Change", "Put Bid", "Put Ask",))
            for (strike_price, percent_change, call_option, put_option) in ocr.generate():
                print("\t%8.2f   %8.2f   %12.2f   %8s   %8.2f   %8.2f" % (
                    call_option.bid,
                    call_option.ask,
                    float(strike_price),
                    format_colored_number(percent_change, 0),
                    put_option.bid,
                    put_option.ask
                ))
            print("\t%8s   %8s   %12s   %8s   %8s   %8s\n" % ("Call Bid", "Call Ask", "Strike Price", "% Change", "Put Bid", "Put Ask",))

            # show results on cli
            print(f"\tSymbol : {args.symbol}")
            print(f"\tTarget premium : {args.premium}")

            targets = ocr.getStrikePricesForTargetPremium(args.premium)
            if targets:
                (target_call, call_diff, call_percent_change), (target_put, put_diff, put_percent_change) = targets
                print(f"\t${args.premium} premium call strike target / change / % change : {format_colored_number(target_call.strikePrice, ocr.getMark())} / {format_colored_number(call_diff, 0)} / {format_colored_number(call_percent_change, 0)}")
                print(f"\t${args.premium} premium put strike target / change / % change  : {format_colored_number(target_put.strikePrice, ocr.getMark())} / {format_colored_number(put_diff, 0)} / {format_colored_number(put_percent_change, 0)}")
                print(f"\t${args.premium} premium call/put strike targets skew : {format_colored_number(call_diff + put_diff, 0)}")
            else:
                print("\tImpossible premium target")
        else:
            print("\tSymbol not found")

    except ValueError as e:
        print(f"Invalid parameter : {str(e)}")
        return
