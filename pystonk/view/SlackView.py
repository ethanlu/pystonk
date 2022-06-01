from pystonk.models.PriceChangeEstimate import PriceChangeEstimate

from quickchart import QuickChart
from prettytable import PrettyTable
from typing import Dict, Iterable, List, NamedTuple, Optional

import random

class SlackView(object):
    SLACK_BLOCK_LIMIT = 35
    SLACK_OK_EMOJI = (':ro-yup:', ':ro-thumbsup:', ':perfect:', ':meme-yiss:')
    SLACK_FAIL_EMOJI = (':ro-hmm:', ':ro-sob:', ':ro-omg:', ':ro-oops:', ':ro-pff:', ':ro-sorry:', ':ro-sweat:', ':ro-question:', ':ro-exclamation:', ':think-3d:', ':where:', ':poop-animated:', ':blob_think:')
    CHART_WIDTH = 600
    CHART_HEIGHT = 400
    CHAR_PIXEL_RATIO = 2

    def showUnexpectedError(self, e: str):
        return [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"{random.choice(self.SLACK_FAIL_EMOJI)} \n Unexpected error : {e}"
                }
            }
        ]

    def showAvailableCommands(self) -> List:
        return [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"{random.choice(self.SLACK_FAIL_EMOJI)} \n I didn't understand your command"
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Here are the available commands:"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "`pc {stock symbol}` \n\n This command will show the current market price the stock"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "`ph {stock symbol} {percent change threshold (decimal)}` \n\n This command will show the weekly price changes for the stock in the past year. The second parameter will mark any week where the price change exceeded the threshold"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "`oc {stock symbol} {target premium price (decimal)}` \n\n This command shows next week's options chain for the stock and the strike prices for calls and puts that is closest to the given target premium price"
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "The above commands are also available with the `/pystonk` command, but the results will only be visible to you"
                }
            }
        ]

    def showPriceCheck(self, symbol: str, price: Optional[float]) -> List:
        if price:
            msg = f"{random.choice(self.SLACK_OK_EMOJI)} \n `{symbol}` is currently `{round(price, 2)}`"
        else:
            msg = f"{random.choice(self.SLACK_FAIL_EMOJI)} \n `{symbol}` is not found..."
        return [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": msg
                }
            }
        ]

    def showPriceHistory(self, symbol: str, percent: float, data: Iterable, total_weeks: int, exceeded_weeks: int, longest_weeks: Optional[List], price_change_estimate: PriceChangeEstimate) -> List:
        t = PrettyTable()
        t.field_names = (' ', 'Week', 'Open', 'Close', '% Change')

        for (group, candlestick) in data:
            flag = ''
            if group > 0:
                flag = '*'

            t.add_row((
                flag,
                candlestick.startDateTime.strftime('%Y-%m-%d'),
                '%7.2f' % candlestick.openPrice,
                '%7.2f' % candlestick.closePrice,
                candlestick.percentChange
            ))
        t.align = 'r'

        response = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"{random.choice(self.SLACK_OK_EMOJI)} \n Here is the price history details for `{symbol}` with intervals where the price change exceeded `{percent}%` marked with `*`"
                },
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"```{t.get_string()}```"
                },
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"Found `{total_weeks}` week intervals for this price history"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"Found `{exceeded_weeks}` week intervals where the price change exceeded `{percent}%`"
                }
            }
        ]

        if longest_weeks:
            response.append(
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"First longest consecutive week of price change exceeding `{percent}%`  started on `{longest_weeks[0][1].startDateTime.strftime('%Y-%m-%d')}` and ended on `{longest_weeks[-1][1].startDateTime.strftime('%Y-%m-%d')}` (`{len(longest_weeks)}` week intervals)"
                    }
                }
            )

        pdc = QuickChart()
        pdc.width = self.CHART_WIDTH
        pdc.height = self.CHART_HEIGHT
        pdc.device_pixel_ratio = self.CHAR_PIXEL_RATIO
        pdc.config = {
            "type": "scatter",
            "data": {
                "datasets": [
                    {
                        "label": "Probability Density",
                        "data": [{"x": x, "y": y} for (x, y) in zip(*price_change_estimate.pdf())]
                    }
                ]
            },
            "options": {
                "scales": {
                    "xAxes": [{
                        "scaleLabel": {
                            "display": True,
                            "labelString": "Price Change Percent"
                        }
                    }],
                    "yAxes": [{
                        "scaleLabel": {
                            "display": True,
                            "labelString": "Probability"
                        }
                    }]
                }
            }
        }

        hc = QuickChart()
        hc.width = self.CHART_WIDTH
        hc.height = self.CHART_HEIGHT
        hc.device_pixel_ratio = self.CHAR_PIXEL_RATIO
        hc.config = {
            "type": "bar",
            "data": {
                "labels": price_change_estimate.histogramBins(),
                "datasets": [
                    {
                        "label": "Price Change",
                        "data": price_change_estimate.histogram()
                    }
                ]
            },
            "options": {
                "scales": {
                    "y": {
                        "beginAtZero": True
                    },
                    "xAxes": [{
                        "scaleLabel": {
                            "display": True,
                            "labelString": "Price Change Percent"
                        }
                    }],
                    "yAxes": [{
                        "scaleLabel": {
                            "display": True,
                            "labelString": "Count"
                        }
                    }]
                }
            }
        }

        response += [
            {
                "type": "image",
                "title": {
                    "type": "plain_text",
                    "text": "Weekly Price Change Histogram"
                },
                "image_url": hc.get_short_url(),
                "alt_text": "Weekly Price Change Histogram"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"Percent Change Mean : `{price_change_estimate.mean()}`"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"Percent Change STD : `{price_change_estimate.std()}`"
                }
            },
            {
                "type": "image",
                "title": {
                    "type": "plain_text",
                    "text": "Weekly Price Change Distribution"
                },
                "image_url": pdc.get_short_url(),
                "alt_text": "Weekly Price Change Distribution"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"Percent Threshold (`{percent}%`) Exceed Probability : `{price_change_estimate.percentProbability(percent)}%`"
                }
            }
        ]

        return response


    def showOptionsChain(self, symbol: str, premium: float, current_price: float, data: Iterable, sell_options: Optional[NamedTuple], buy_options: Optional[NamedTuple]) -> List:
        t = PrettyTable()
        t.field_names = ('  ', 'Call Bid', 'Call Ask', 'Put Bid', 'Put Ask', 'Strike', '% Change')

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
                flag,
                '%7.2f' % call_option.bid,
                '%7.2f' % call_option.ask,
                '%7.2f' % put_option.bid,
                '%7.2f' % put_option.ask,
                '%7.2f' % float(strike_price),
                '%7.2f' % percent_change,
            ))
        t.align = 'r'

        response = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"{random.choice(self.SLACK_OK_EMOJI)} \n Here is next week's option chain for `{symbol}` with target premium price `{premium}` for buy-call, buy-put, sell-call, and sell-put marked as `C`, `P`, `c`, and `p` respectively:"
                }
            },
            {
                "type": "divider"
            },
        ]

        i = 0
        while i < len(t.rows):
            response.append(
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"```{t.get_string(start=i, end=i + self.SLACK_BLOCK_LIMIT)}```"
                    }
                }
            )
            i += self.SLACK_BLOCK_LIMIT


        if sell_options:
            response.append(
                {
                    "type": "divider"
                }
            )
            response.append(
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"`c` : Closest `{sell_options.call.expirationDateTime.strftime('%Y-%m-%d')}` strike price for sell-call is `{sell_options.call.strikePrice}`\nWhich is `{sell_options.call_diff}` from current price of `{current_price}` (`{sell_options.call_diff_percent}%`)"
                    }
                }
            )
            response.append(
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"`p` : Closest `{sell_options.put.expirationDateTime.strftime('%Y-%m-%d')}` strike price for sell-put is `{sell_options.put.strikePrice}`\nWhich is `{sell_options.put_diff}` from current price of `{current_price}` (`{sell_options.put_diff_percent}%`)"
                    }
                }
            )
            response.append(
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"`{premium}` premium for sell options has a skew of `{round(sell_options.call_diff + sell_options.put_diff, 2)}`"
                    }
                }
            )

        if buy_options:
            response.append(
                {
                    "type": "divider"
                }
            )
            response.append(
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"`C` : Closest `{buy_options.call.expirationDateTime.strftime('%Y-%m-%d')}` strike price for buy-call is `{buy_options.call.strikePrice}`\nWhich is `{buy_options.call_diff}` from current price of `{current_price}` (`{buy_options.call_diff_percent}%`)"
                    }
                }
            )
            response.append(
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"`P` : Closest `{buy_options.put.expirationDateTime.strftime('%Y-%m-%d')}` strike price for buy-put is `{buy_options.put.strikePrice}`\nWhich is `{buy_options.put_diff}` from current price of `{current_price}` (`{buy_options.put_diff_percent}%`)"
                    }
                }
            )
            response.append(
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"`{premium}` premium for buy options has a skew of `{round(buy_options.call_diff + buy_options.put_diff, 2)}`"
                    }
                }
            )

        if not sell_options and not buy_options:
            response.append(
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"No Call/Put strike price exist for target premium : {premium}"
                    }
                }
            )

        return response
