from pystonk.models.PriceChangeEstimate import PriceChangeEstimate
from pystonk.view import View

from quickchart import QuickChart
from prettytable import PrettyTable
from typing import Iterable, List, Optional

import random


class PriceHistoryView(View):
    def __init__(self, symbol: str, percent: float, data: Iterable, total_weeks: int, exceeded_weeks: int, longest_weeks: Optional[List], price_change_estimate: PriceChangeEstimate):
        super().__init__()
        self._symbol = symbol
        self._percent = percent
        self._data = data
        self._total_weeks = total_weeks
        self._exceeded_weeks = exceeded_weeks
        self._longest_weeks = longest_weeks,
        self._price_change_estimate = price_change_estimate

    def show(self) -> List:
        t = PrettyTable()
        t.field_names = (' ', 'Week', 'Open', 'Close', '% Change')

        for (group, candlestick) in self._data:
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
                    "text": f"```{t.get_string()}```"
                },
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"Found `{self._total_weeks}` week intervals for this price history"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"Found `{self._exceeded_weeks}` week intervals where the price change exceeded `{self._percent}%`"
                }
            }
        ]

        if self._longest_weeks:
            response.append(
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"First longest consecutive week of price change exceeding `{self._percent}%` started on `{self._longest_weeks[0][1].startDateTime.strftime('%Y-%m-%d')}` and ended on `{self._longest_weeks[-1][1].startDateTime.strftime('%Y-%m-%d')}` (`{len(self._longest_weeks)}` week intervals)"
                    }
                }
            )

        hc = QuickChart()
        hc.width = self.CHART_WIDTH
        hc.height = self.CHART_HEIGHT
        hc.device_pixel_ratio = self.CHAR_PIXEL_RATIO
        hc.config = {
            "type": "bar",
            "data": {
                "labels": self._price_change_estimate.histogramBins(),
                "datasets": [
                    {
                        "label": "Price Change",
                        "data": self._price_change_estimate.histogram()
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
                        "data": [{"x": x, "y": y} for (x, y) in zip(*self._price_change_estimate.pdf())]
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
                    "text": f"Percent Change Mean : `{self._price_change_estimate.mean()}`"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"Percent Change STD : `{self._price_change_estimate.std()}`"
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
                    "text": f"Percent Threshold (`{self._percent}%`) Exceed Probability : `{self._price_change_estimate.percentProbability(self._percent)}%`"
                }
            }
        ]

        return response
