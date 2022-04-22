from datetime import date, timedelta
from typing import Any, Tuple

import re


def percent_diff(old: float, new: float) -> float:
    return round(((new - old) / old) * 100, 2)


def get_next_monday_friday(d: date) -> Tuple[date, date]:
    """
    returns tuple of the next week's monday and friday date relative to the given date
    :param d:
    :return:
    """
    next_week = d + timedelta(weeks=1)
    return next_week + timedelta(days=-next_week.weekday()), next_week + timedelta(days=(4 - next_week.weekday()))


def is_number(n: Any) -> bool:
    return re.match(r"^\d*\.?\d*$", n) is not None


def is_stock(n: Any) -> bool:
    return re.match(r"^[a-zA-Z.]+$", n) is not None