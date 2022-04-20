from pystonk.reports.WeeklyPriceChangeReport import WeeklyPriceChangeReport
from pystonk.reports.WeeklyOptionsReport import WeeklyOptionsReport

from termcolor import colored
from typing import Any


class TerminalView(object):
    def format_colored_number(self, input: Any, threshold: Any) -> str:
        input = float(input)
        threshold = float(threshold)
        return colored("{:8.2f}".format(input), 'green' if input > threshold else 'red' if input < threshold else 'white')

    def showPriceHistory(self, report: WeeklyPriceChangeReport, symbol: str, percent: float) -> None:
        report.retrieveData(symbol)

        print("\t%10s   %7s   %7s   %8s" % ("Week", "Open", "Close", "% Change"))
        for (group, candlestick) in report.generate(percent):
            if group == 0:
                date_color = 'white'
                percent_change = self.format_colored_number(candlestick.percentChange, candlestick.percentChange)
            else:
                date_color = 'yellow'
                percent_change = self.format_colored_number(candlestick.percentChange, 0)

            print("\t%10s   %7.2f   %7.2f   %8s" % (
                colored(candlestick.startDateTime.strftime('%Y-%m-%d'), date_color),
                candlestick.openPrice,
                candlestick.closePrice,
                percent_change
            ))
        print(f"\tSymbol : {symbol}")
        print(f"\tChange Threshold : {percent}")
        print(f"\tTotal Weeks : {report.totalWeeks()}")
        print(f"\tThreshold Exceeded Weeks: {report.thresholdExceededWeeksTotal(percent)}")
        longest = report.longestThresholdExceededWeeks(percent)
        if longest:
            print(
                f"\tLongest Consecutive Threshold Exceeded Weeks: {longest[0][1].startDateTime.strftime('%Y-%m-%d')} to {longest[-1][1].startDateTime.strftime('%Y-%m-%d')} ({len(longest)} weeks)"
            )

    def showOptionsChain(self, report: WeeklyOptionsReport, symbol: str, premium: float) -> None:
        c = report.retrieveData(symbol)
        if c:
            print("\t%8s   %8s   %12s   %8s   %8s   %8s" % ("Call Bid", "Call Ask", "Strike Price", "% Change", "Put Bid", "Put Ask",))
            for (strike_price, percent_change, call_option, put_option) in report.generate():
                print("\t%8.2f   %8.2f   %12.2f   %8s   %8.2f   %8.2f" % (
                    call_option.bid,
                    call_option.ask,
                    float(strike_price),
                    self.format_colored_number(percent_change, 0),
                    put_option.bid,
                    put_option.ask
                ))
            print("\t%8s   %8s   %12s   %8s   %8s   %8s\n" % ("Call Bid", "Call Ask", "Strike Price", "% Change", "Put Bid", "Put Ask",))

            # show results on cli
            print(f"\tSymbol : {symbol}")
            print(f"\tTarget premium : {premium}")
            print(f"\tMarket price : {report.getMark()}")

            targets = report.getStrikePricesForTargetPremium(premium)
            if targets:
                (target_call, call_diff, call_percent_change), (target_put, put_diff, put_percent_change) = targets
                print(
                    f"\t${premium} premium call strike target / change / % change : {self.format_colored_number(target_call.strikePrice, report.getMark())} / "
                    f"{self.format_colored_number(call_diff, 0)} / "
                    f"{self.format_colored_number(call_percent_change, 0)}"
                )
                print(
                    f"\t${premium} premium put strike target / change / % change  : {self.format_colored_number(target_put.strikePrice, report.getMark())} / "
                    f"{self.format_colored_number(put_diff, 0)} / "
                    f"{self.format_colored_number(put_percent_change, 0)}"
                )
                print(f"\t${premium} premium call/put strike targets skew : {self.format_colored_number(call_diff + put_diff, 0)}")
            else:
                print("\tImpossible premium target")
        else:
            print("\tSymbol not found")