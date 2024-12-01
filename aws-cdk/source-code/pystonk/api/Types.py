from enum import Enum

'''
PriceHistoryApi Types
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

'''
OptionsChainApi Types
'''
class ContractType(Enum):
    ALL = 'ALL'
    CALL = 'CALL'
    PUT = 'PUT'

class OptionType(Enum):
    ALL = 'ALL'
    STANDARD = 'S'
    NONSTANDARD = 'NS'

class RangeType(Enum):
    ALL = 'ALL'
    IN_THE_MONEY = 'ITM'
    NEAR_THE_MONEY = 'NTM'
    OUT_THE_MONEY = 'OTM'
    STRIKE_ABOVE_MARKET = 'SAK'
    STRIKE_BELOW_MARKET = 'SBK'
    STRIKE_NEAR_MARKET = 'SNK'

class StrategyType(Enum):
    ANALYTICAL = 'ANALYTICAL'
    BUTTERFLY = 'BUTTERFLY'
    CALENDAR = 'CALENDAR'
    COLLAR = 'COLLAR'
    CONDOR = 'CONDOR'
    COVERED = 'COVERED'
    DIAGONAL = 'DIAGONAL'
    ROLL = 'ROLL'
    SINGLE = 'SINGLE'
    STRADDLE = 'STRADDLE'
    STRANGLE = 'STRANGLE'
    VERTICAL = 'VERTICAL'