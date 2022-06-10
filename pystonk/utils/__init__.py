from datetime import date, timedelta
from typing import Any, Dict, Tuple

import re


def percent_diff(old: float, new: float) -> float:
    return round(((new - old) / old) * 100, 2)


def get_friday_of_week(d: date) -> date:
    """
    returns the friday date of the week given date is in
    :param d:
    :return:
    """
    return d + timedelta(days=(4 - d.weekday()))


def get_third_friday_of_month(d: date) -> date:
    """
    returns the third friday date of the month given date is in
    :param d:
    :return:
    """
    month_day1 = date(d.year, d.month, 1)
    return month_day1 + timedelta(weeks=(2 if month_day1.weekday() <= 4 else 3), days=(4 - month_day1.weekday()))


def get_third_friday_of_quarter(d: date):
    """
    returns the third friday date of the month given date is in
    :param d:
    :param q:
    :return:
    """
    quarter_day1 = date(d.year, max(((min(d.month, 11) // 3) * 3), 1), 1)
    return quarter_day1 + timedelta(weeks=(2 if quarter_day1.weekday() <= 4 else 3), days=(4 - quarter_day1.weekday()))


def get_third_friday_of_half(d: date):
    """
    returns the third friday date of the month given date is in
    :param d:
    :param q:
    :return:
    """
    half_day1 = date(d.year, max(((min(d.month, 11) // 6) * 6), 1), 1)
    return half_day1 + timedelta(weeks=(2 if half_day1.weekday() <= 4 else 3), days=(4 - half_day1.weekday()))


def is_number(n: Any) -> bool:
    return re.match(r"^\d*\.?\d*$", n) is not None


def coalesce(data: Dict, key: Tuple, default: Any = None) -> Any:
    """
    returns data[k] for first k in key that exists in data
    :param data: key-value paris
    :param key: list of keys
    :param default: value returned if no keys are found in data
    :return:
    """
    return next((data[k] for k in key if k in data), default)
