from pystonk.models.PriceChangeEstimate import PriceChangeEstimate

from prettytable import PrettyTable
from termcolor import colored
from typing import Any, Iterable, List, NamedTuple, Optional


class TerminalView(object):
    def format_colored_number(self, input: Any, threshold: Any) -> str:
        input = float(input)
        threshold = float(threshold)
        return colored("{:8.2f}".format(input), 'green' if input > threshold else 'red' if input < threshold else 'white')

    def showPriceHistory(self, symbol: str, percent: float, data: Iterable, total_weeks: int, exceeded_weeks: int, longest_weeks: Optional[List], price_change_estimate:PriceChangeEstimate):
        t = PrettyTable()
        t.field_names = (' ', 'Week', 'Open', 'Close', '% Change')

        for (group, candlestick) in data:
            if group == 0:
                t.add_row((
                    ' ',
                    candlestick.startDateTime.strftime('%Y-%m-%d'),
                    '%7.2f' % candlestick.openPrice,
                    '%7.2f' % candlestick.closePrice,
                    '%5.2f' % candlestick.percentChange
                ))
            else:
                t.add_row((
                    colored('*', 'cyan'),
                    colored(candlestick.startDateTime.strftime('%Y-%m-%d'), 'cyan'),
                    colored('%7.2f' % candlestick.openPrice, 'cyan'),
                    colored('%7.2f' % candlestick.closePrice, 'cyan'),
                    self.format_colored_number(candlestick.percentChange, 0)
                ))

        t.align = 'r'
        print()
        print(t)
        print()
        print(f"Symbol : {symbol}")
        print(f"Change Threshold : {percent}")
        print(f"Total Weeks : {total_weeks}")
        print(f"Threshold Exceeded Weeks: {exceeded_weeks}")
        if longest_weeks:
            print(
                f"Longest Consecutive Threshold Exceeded Weeks: {longest_weeks[0][1].startDateTime.strftime('%Y-%m-%d')} to {longest_weeks[-1][1].startDateTime.strftime('%Y-%m-%d')} ({len(longest_weeks)} weeks)"
            )
        print(f"Percent Change Mean: {price_change_estimate.mean()}")
        print(f"Percent Change STD: {price_change_estimate.std()}")
        print(f"Percent Threshold Exceed Probability (Unweighted): {price_change_estimate.percentProbability(percent, weighted=False)}")
        print(f"Percent Threshold Exceed Probability (Weighted)  : {price_change_estimate.percentProbability(percent)}")
        print()

    def showOptionsChain(self, symbol: str, premium: float, current_price: float, data: Iterable, sell_options: Optional[NamedTuple], buy_options: Optional[NamedTuple]):
        t = PrettyTable()
        t.field_names = (' ', 'Call Bid', 'Call Ask', 'Put Bid', 'Put Ask', 'Strike Price', '% Change')

        sell_call = sell_put = buy_call = buy_put = None
        if sell_options:
            sell_call = sell_options.call
            sell_put = sell_options.put
        if buy_options:
            buy_call = buy_options.call
            buy_put = buy_options.put

        for (strike_price, percent_change, call_option, put_option) in data:
            flag = ''
            if call_option == sell_call:
                flag += 'c'
            if call_option == buy_call:
                flag += 'C'
            if put_option == sell_put:
                flag += 'p'
            if put_option == buy_put:
                flag += 'P'

            t.add_row((
                colored(flag, 'cyan' if flag else 'white'),
                colored(call_option.bid, 'cyan' if sell_call == call_option else 'white'),
                colored(call_option.ask, 'cyan' if buy_call == call_option else 'white'),
                colored(put_option.bid, 'cyan' if sell_put == put_option else 'white'),
                colored(put_option.ask, 'cyan' if buy_put == put_option else 'white'),
                self.format_colored_number(float(strike_price), current_price),
                self.format_colored_number(percent_change, 0),
            ))

        t.align = 'r'
        print()
        print(t)
        print(f"Symbol : {symbol}")
        print(f"Target Premium : {premium}")
        print(f"Current Price : {current_price}")

        if sell_options:
            print()
            print(
                f"Closest {sell_options.call.expirationDateTime.strftime('%Y-%m-%d')} Sell Call Strike Price / Change / % Change : {self.format_colored_number(sell_options.call.strikePrice, current_price)} / "
                f"{self.format_colored_number(sell_options.call_diff, 0)} / "
                f"{self.format_colored_number(sell_options.call_diff_percent, 0)}"
            )
            print(
                f"Closest {sell_options.put.expirationDateTime.strftime('%Y-%m-%d')} Sell Put Strike Price / Change / % Change : {self.format_colored_number(sell_options.put.strikePrice, current_price)} / "
                f"{self.format_colored_number(sell_options.put_diff, 0)} / "
                f"{self.format_colored_number(sell_options.put_diff_percent, 0)}"
            )
            print(f"${premium} Sell Option Skew : {self.format_colored_number(sell_options.call_diff + sell_options.put_diff, 0)}")

        if buy_options:
            print()
            print(
                f"Closest {buy_options.call.expirationDateTime.strftime('%Y-%m-%d')} Buy Call Strike Price / Change / % Change : {self.format_colored_number(buy_options.call.strikePrice, current_price)} / "
                f"{self.format_colored_number(buy_options.call_diff, 0)} / "
                f"{self.format_colored_number(buy_options.call_diff_percent, 0)}"
            )
            print(
                f"Closest {buy_options.put.expirationDateTime.strftime('%Y-%m-%d')} Buy Put Strike Price / Change / % Change : {self.format_colored_number(buy_options.put.strikePrice, current_price)} / "
                f"{self.format_colored_number(buy_options.put_diff, 0)} / "
                f"{self.format_colored_number(buy_options.put_diff_percent, 0)}"
            )
            print(f"${premium} Buy Option Skew : {self.format_colored_number(buy_options.call_diff + buy_options.put_diff, 0)}")

        if not sell_options and not buy_options:
            print(f"No Call/Put strike price exist for target premium : {premium}")
        print()
