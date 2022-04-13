from enum import Enum

'''
PriceHistory Types
'''
class FrequencyType(Enum):
    MINUTE = 'minute'
    DAILY = 'daily'
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'

class PeriodType(Enum):
    DAY = 'day'
    MONTH = 'month'
    YEAR = 'year'
    YTD = 'ytd'
