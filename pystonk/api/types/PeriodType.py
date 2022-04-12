from enum import Enum


class PeriodType(Enum):
    DAY = 'day'
    MONTH = 'month'
    YEAR = 'year'
    YTD = 'ytd'