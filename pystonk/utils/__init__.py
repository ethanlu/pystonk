from termcolor import colored
from datetime import date, timedelta
from typing import Any, Tuple


def percent_diff(old: float, new: float) -> float:
    return round(((new - old) / old) * 100, 2)

def get_next_monday_friday(d: date) -> Tuple[date, date]:
    '''
    returns tuple of the next week's monday and friday date relative to the given date
    :param day:
    :return:
    '''
    next_week = d + timedelta(weeks=1)
    return (next_week + timedelta(days=-next_week.weekday()), next_week + timedelta(days=(4 - next_week.weekday())))

def format_colored_number(input, threshold) -> str:
    input = float(input)
    threshold = float(threshold)
    return colored("{:8.2f}".format(input), 'green' if input > threshold else 'red' if input < threshold else 'white')