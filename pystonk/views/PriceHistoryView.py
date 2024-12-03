from pystonk.api.Types import FrequencyType
from pystonk.models.PriceHistory import PriceHistory
from pystonk.models.PriceHistoryEstimate import PriceHistoryEstimate
from pystonk.views import View

from quickchart import QuickChart
from prettytable import PrettyTable
from typing import Dict, List

import random


class PriceHistoryView(View):
    INTERVAL_FREQUENCY_TYPE_MAP = {
        FrequencyType.DAILY.value: "days",
        FrequencyType.WEEKLY.value: "weeks",
        FrequencyType.MONTHLY.value: "months"
    }
    TRUNCATED_HISTORY_LIMIT = 10

    def __init__(self, symbol: str, percent: float, frequency_type: FrequencyType, price_history: PriceHistory, price_history_estimate: PriceHistoryEstimate):
        super().__init__()

        self._symbol = symbol
        self._percent = percent
        self._price_history = price_history
        self._price_history_estimate = price_history_estimate

        self._frequency_type = frequency_type
        self._interval_label = self.INTERVAL_FREQUENCY_TYPE_MAP[self._frequency_type.value]

        # history table
        self._t = PrettyTable()

        # histogram
        self._hc = QuickChart()
        self._hc.width = self.CHART_WIDTH
        self._hc.height = self.CHART_HEIGHT
        self._hc.device_pixel_ratio = self.CHAR_PIXEL_RATIO

        # probability density
        self._pdc = QuickChart()
        self._pdc.width = self.CHART_WIDTH
        self._pdc.height = self.CHART_HEIGHT
        self._pdc.device_pixel_ratio = self.CHAR_PIXEL_RATIO

    def _build_history(self) -> List[Dict]:
        self._t.field_names = (' ', self._interval_label.capitalize(), 'Open', 'Close', '% Change')
        self._t.align = 'r'

        rows = []
        for percent_change, candlestick in zip(self._price_history.percent_change_intervals(), self._price_history.intervals()):
            over_threshold = (percent_change >= self._percent) if self._percent >= 0 else (percent_change <= self._percent)
            if self._verbose or over_threshold:
                # show all or only rows over threshold if verbosity is disabled
                rows.append((
                    '*' if over_threshold and self.verbose else '',
                    candlestick.start_datetime.strftime('%Y-%m-%d'),
                    '%7.2f' % candlestick.open_price,
                    '%7.2f' % candlestick.close_price,
                    percent_change
                ))
        # only show last TRUNCATE_HISTORY_LIMIT if verbosity is disabled
        self._t.add_rows(rows if self.verbose else rows[-self.TRUNCATED_HISTORY_LIMIT:])

        response = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"{self._interval_label.capitalize()} where the price change exceeded `{self._percent}%` are marked with `*`" if self.verbose else f"Last {self.TRUNCATED_HISTORY_LIMIT} {self._interval_label} where the price change exceeded `{self._percent}%`"
                },
            }
        ]
        response += self.paginate(self._t)
        response += [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Total {self._interval_label.capitalize()}*: `{self._price_history.count_intervals()}`\n" +
                            f"*{self._interval_label.capitalize()} Exceeding Percent Threshold*: `{self._price_history.count_intervals_exceed_percent_threshold(self._percent)}`"
                }
            }
        ]
        return response

    def _build_statistics(self) -> List[Dict]:
        response = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"Basic statistics from history data"
                },
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Percent Change Min*: `{self._price_history_estimate.min()}` \n" +
                            f"*Percent Change Max*: `{self._price_history_estimate.max()}` \n" +
                            f"*Percent Change Mean*: `{self._price_history_estimate.mean()}` \n" +
                            f"*Percent Change STD*: `{self._price_history_estimate.std()}` \n" +
                            f"*Percent Change Skewness*: `{self._price_history_estimate.skew()}` \n" +
                            f"*Percent Change Kurtosis*: `{self._price_history_estimate.kurtosis()}` \n" +
                            f"*Probability Exceeding Percent Threshold*: `{self._price_history_estimate.percent_probability(self._percent)}%`"
                }
            }
        ]

        if self.verbose:
            self._hc.config = {
                "type": "bar",
                "data": {
                    "labels": self._price_history_estimate.histogram_bins(),
                    "datasets": [
                        {
                            "label": f"{self._frequency_type.value.capitalize()} Price Change (+/-{self._price_history_estimate.histogram_bins_interval()})",
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
                                "labelString": f"Number Of {self._interval_label.capitalize()}"
                            }
                        }]
                    }
                }
            }

            self._pdc.config = {
                "type": "scatter",
                "data": {
                    "datasets": [
                        {
                            "label": f"{self._frequency_type.value.capitalize()} Probability Density",
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

            response += [
                {
                    "type": "image",
                    "title": {
                        "type": "plain_text",
                        "text": f"{self._frequency_type.value.capitalize()} Price Change Histogram"
                    },
                    "image_url": self._hc.get_short_url(),
                    "alt_text": "Price Change Histogram"
                },
                {
                    "type": "image",
                    "title": {
                        "type": "plain_text",
                        "text": f"{self._frequency_type.value.capitalize()} Probability Density"
                    },
                    "image_url": self._pdc.get_short_url(),
                    "alt_text": "Probability Density"
                }
            ]

        return response

    def show_text(self) -> str:
        return f"price history for {self._symbol} with {self._percent} threshold cannot be shown in text-only mode"

    def show(self) -> List[Dict]:
        response = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"{random.choice(self.SLACK_OK_EMOJI)} \n\n Here is the `{self._frequency_type.value}` price history for `{self._symbol}` with `{self._percent}%` percent threshold"
                },
            },
            {
                "type": "divider"
            },
        ]

        response += self._build_history()
        response += [
            {
                "type": "divider"
            },
        ]
        response += self._build_statistics()

        return response
