from pystonk.models.PriceHistory import PriceHistory
from pystonk.models.PriceHistoryEstimate import PriceHistoryEstimate
from pystonk.views import View

from quickchart import QuickChart
from prettytable import PrettyTable
from typing import Dict, List

import random


class PriceHistoryView(View):
    def __init__(self, symbol: str, percent: float, price_history: PriceHistory, price_history_estimate: PriceHistoryEstimate):
        super().__init__()

        self._symbol = symbol
        self._percent = percent
        self._price_history = price_history
        self._price_history_estimate = price_history_estimate

        # history table
        self._t = PrettyTable()
        self._t.field_names = (' ', 'Week', 'Open', 'Close', '% Change')

        for candlestick in self._price_history.intervals():
            flag = ''
            if candlestick.percent_change >= percent:
                flag = '*'

            self._t.add_row((
                flag,
                candlestick.start_datetime.strftime('%Y-%m-%d'),
                '%7.2f' % candlestick.open_price,
                '%7.2f' % candlestick.close_price,
                candlestick.percent_change
            ))
        self._t.align = 'r'

        # histogram
        self._hc = QuickChart()
        self._hc.width = self.CHART_WIDTH
        self._hc.height = self.CHART_HEIGHT
        self._hc.device_pixel_ratio = self.CHAR_PIXEL_RATIO
        self._hc.config = {
            "type": "bar",
            "data": {
                "labels": self._price_history_estimate.histogramBins(),
                "datasets": [
                    {
                        "label": "Price Change",
                        "data": self._price_history_estimate.histogram()
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
                        "ticks": {
                            "min": 0
                        },
                        "scaleLabel": {
                            "display": True,
                            "labelString": "Count"
                        }
                    }]
                }
            }
        }

        # probability density
        self._pdc = QuickChart()
        self._pdc.width = self.CHART_WIDTH
        self._pdc.height = self.CHART_HEIGHT
        self._pdc.device_pixel_ratio = self.CHAR_PIXEL_RATIO
        self._pdc.config = {
            "type": "scatter",
            "data": {
                "datasets": [
                    {
                        "label": "Probability Density",
                        "data": [{"x": x, "y": y} for (x, y) in zip(*self._price_history_estimate.pdf())]
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

    def show_text(self) -> str:
        return f"price history for {self._symbol} with {self._percent} threshold cannot be shown in text-only mode"

    def show(self) -> List[Dict]:
        response = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"{random.choice(self.SLACK_OK_EMOJI)} \n Here is the price history details for `{self._symbol}` with intervals where the price change exceeded `{self._percent}%` marked with `*`"
                },
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"```{self._t.get_string()}```"
                },
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"Found `{self._price_history.count_intervals()}` week intervals for this price history"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"Found `{self._price_history.count_intervals_exceed_percent_threshold(self._percent)}` week intervals where the price change exceeded `{self._percent}%`"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"Percent Threshold (`{self._percent}%`) Exceed Rate : `{self._price_history.percent_rate(self._percent)}%`"
                }
            }
        ]

        response += [
            {
                "type": "image",
                "title": {
                    "type": "plain_text",
                    "text": "Weekly Price Change Histogram"
                },
                "image_url": self._hc.get_short_url(),
                "alt_text": "Weekly Price Change Histogram"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"Percent Change Mean : `{self._price_history_estimate.mean()}`"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"Percent Change STD : `{self._price_history_estimate.std()}`"
                }
            },
            {
                "type": "image",
                "title": {
                    "type": "plain_text",
                    "text": "Weekly Price Change Distribution"
                },
                "image_url": self._pdc.get_short_url(),
                "alt_text": "Weekly Price Change Distribution"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"Percent Threshold (`{self._percent}%`) Exceed Probability : `{self._price_history_estimate.percent_probability(self._percent)}%`"
                }
            }
        ]

        return response
