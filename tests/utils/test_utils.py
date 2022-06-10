from pystonk.utils import get_friday_of_week, get_third_friday_of_month, get_third_friday_of_quarter, get_third_friday_of_half, is_number, percent_diff, coalesce

from datetime import date
from unittest import TestCase


class UtilsTest(TestCase):
    def testPercentDiff(self):
        r = percent_diff(100, 50)
        self.assertEqual(r, -50.00)

        r = percent_diff(50, 100)
        self.assertEqual(r, 100.00)

    def testGetFridayInSameMonth(self):
        f = get_friday_of_week(date(2020, 2, 3))
        self.assertEqual(f, date(2020, 2, 7))

        f = get_friday_of_week(date(2020, 2, 4))
        self.assertEqual(f, date(2020, 2, 7))

        f = get_friday_of_week(date(2020, 2, 5))
        self.assertEqual(f, date(2020, 2, 7))

        f = get_friday_of_week(date(2020, 2, 6))
        self.assertEqual(f, date(2020, 2, 7))

        f = get_friday_of_week(date(2020, 2, 7))
        self.assertEqual(f, date(2020, 2, 7))

        f = get_friday_of_week(date(2020, 2, 8))
        self.assertEqual(f, date(2020, 2, 7))

        f = get_friday_of_week(date(2020, 2, 9))
        self.assertEqual(f, date(2020, 2, 7))

        f = get_friday_of_week(date(2020, 2, 10))
        self.assertEqual(f, date(2020, 2, 14))

    def testGetFridayInNextMonth(self):
        f = get_friday_of_week(date(2020, 3, 30))
        self.assertEqual(f, date(2020, 4, 3))

        f = get_friday_of_week(date(2020, 3, 31))
        self.assertEqual(f, date(2020, 4, 3))

        f = get_friday_of_week(date(2020, 4, 1))
        self.assertEqual(f, date(2020, 4, 3))

        f = get_friday_of_week(date(2020, 4, 2))
        self.assertEqual(f, date(2020, 4, 3))

        f = get_friday_of_week(date(2020, 4, 3))
        self.assertEqual(f, date(2020, 4, 3))

        f = get_friday_of_week(date(2020, 4, 4))
        self.assertEqual(f, date(2020, 4, 3))

        f = get_friday_of_week(date(2020, 4, 5))
        self.assertEqual(f, date(2020, 4, 3))

        f = get_friday_of_week(date(2020, 4, 6))
        self.assertEqual(f, date(2020, 4, 10))

    def testGetFridayInNextYear(self):
        f = get_friday_of_week(date(2020, 12, 28))
        self.assertEqual(f, date(2021, 1, 1))

        f = get_friday_of_week(date(2020, 12, 29))
        self.assertEqual(f, date(2021, 1, 1))

        f = get_friday_of_week(date(2020, 12, 30))
        self.assertEqual(f, date(2021, 1, 1))

        f = get_friday_of_week(date(2020, 12, 31))
        self.assertEqual(f, date(2021, 1, 1))

        f = get_friday_of_week(date(2021, 1, 1))
        self.assertEqual(f, date(2021, 1, 1))

        f = get_friday_of_week(date(2021, 1, 2))
        self.assertEqual(f, date(2021, 1, 1))

        f = get_friday_of_week(date(2021, 1, 3))
        self.assertEqual(f, date(2021, 1, 1))

        f = get_friday_of_week(date(2021, 1, 4))
        self.assertEqual(f, date(2021, 1, 8))

    def testGetFridayWithLeapYear(self):
        f = get_friday_of_week(date(2024, 2, 26))
        self.assertEqual(f, date(2024, 3, 1))

        f = get_friday_of_week(date(2024, 2, 27))
        self.assertEqual(f, date(2024, 3, 1))

        f = get_friday_of_week(date(2024, 2, 28))
        self.assertEqual(f, date(2024, 3, 1))

        f = get_friday_of_week(date(2024, 2, 29))
        self.assertEqual(f, date(2024, 3, 1))

        f = get_friday_of_week(date(2024, 3, 1))
        self.assertEqual(f, date(2024, 3, 1))

    def testGetThirdFridayWeekStartBeforeFriday(self):
        f = get_third_friday_of_month(date(2022, 6, 1))
        self.assertEqual(f, date(2022, 6, 17))

        f = get_third_friday_of_month(date(2022, 6, 17))
        self.assertEqual(f, date(2022, 6, 17))

        f = get_third_friday_of_month(date(2022, 6, 24))
        self.assertEqual(f, date(2022, 6, 17))

    def testGetThirdFridayWeekStartOnFriday(self):
        f = get_third_friday_of_month(date(2022, 7, 1))
        self.assertEqual(f, date(2022, 7, 15))

        f = get_third_friday_of_month(date(2022, 7, 15))
        self.assertEqual(f, date(2022, 7, 15))

        f = get_third_friday_of_month(date(2022, 7, 24))
        self.assertEqual(f, date(2022, 7, 15))

    def testGetThirdFridayWeekStartAfterFriday(self):
        f = get_third_friday_of_month(date(2022, 10, 1))
        self.assertEqual(f, date(2022, 10, 21))

        f = get_third_friday_of_month(date(2022, 10, 21))
        self.assertEqual(f, date(2022, 10, 21))

        f = get_third_friday_of_month(date(2022, 10, 30))
        self.assertEqual(f, date(2022, 10, 21))

    def testGetthirdFridayOfQuarter(self):
        f = get_third_friday_of_quarter(date(2023, 1, 1))
        self.assertEqual(f, date(2023, 1, 20))

        f = get_third_friday_of_quarter(date(2023, 1, 20))
        self.assertEqual(f, date(2023, 1, 20))

        f = get_third_friday_of_quarter(date(2023, 2, 25))
        self.assertEqual(f, date(2023, 1, 20))

        f = get_third_friday_of_quarter(date(2023, 3, 1))
        self.assertEqual(f, date(2023, 3, 17))

        f = get_third_friday_of_quarter(date(2023, 3, 17))
        self.assertEqual(f, date(2023, 3, 17))

        f = get_third_friday_of_quarter(date(2023, 4, 20))
        self.assertEqual(f, date(2023, 3, 17))

        f = get_third_friday_of_quarter(date(2023, 5, 19))
        self.assertEqual(f, date(2023, 3, 17))

        f = get_third_friday_of_quarter(date(2023, 6, 1))
        self.assertEqual(f, date(2023, 6, 16))

        f = get_third_friday_of_quarter(date(2023, 6, 16))
        self.assertEqual(f, date(2023, 6, 16))

        f = get_third_friday_of_quarter(date(2023, 7, 7))
        self.assertEqual(f, date(2023, 6, 16))

        f = get_third_friday_of_quarter(date(2023, 8, 23))
        self.assertEqual(f, date(2023, 6, 16))

        f = get_third_friday_of_quarter(date(2023, 9, 1))
        self.assertEqual(f, date(2023, 9, 15))

        f = get_third_friday_of_quarter(date(2023, 9, 16))
        self.assertEqual(f, date(2023, 9, 15))

        f = get_third_friday_of_quarter(date(2023, 10, 2))
        self.assertEqual(f, date(2023, 9, 15))

        f = get_third_friday_of_quarter(date(2023, 11, 18))
        self.assertEqual(f, date(2023, 9, 15))

        f = get_third_friday_of_quarter(date(2023, 12, 31))
        self.assertEqual(f, date(2023, 9, 15))

    def testGetthirdFridayOfHalf(self):
        f = get_third_friday_of_half(date(2024, 1, 1))
        self.assertEqual(f, date(2024, 1, 19))

        f = get_third_friday_of_half(date(2024, 1, 19))
        self.assertEqual(f, date(2024, 1, 19))

        f = get_third_friday_of_half(date(2024, 2, 1))
        self.assertEqual(f, date(2024, 1, 19))

        f = get_third_friday_of_half(date(2024, 3, 19))
        self.assertEqual(f, date(2024, 1, 19))

        f = get_third_friday_of_half(date(2024, 4, 24))
        self.assertEqual(f, date(2024, 1, 19))

        f = get_third_friday_of_half(date(2024, 5, 31))
        self.assertEqual(f, date(2024, 1, 19))

        f = get_third_friday_of_half(date(2024, 6, 1))
        self.assertEqual(f, date(2024, 6, 21))

        f = get_third_friday_of_half(date(2024, 6, 21))
        self.assertEqual(f, date(2024, 6, 21))

        f = get_third_friday_of_half(date(2024, 7, 1))
        self.assertEqual(f, date(2024, 6, 21))

        f = get_third_friday_of_half(date(2024, 8, 21))
        self.assertEqual(f, date(2024, 6, 21))

        f = get_third_friday_of_half(date(2024, 9, 30))
        self.assertEqual(f, date(2024, 6, 21))

        f = get_third_friday_of_half(date(2024, 10, 10))
        self.assertEqual(f, date(2024, 6, 21))

        f = get_third_friday_of_half(date(2024, 11, 11))
        self.assertEqual(f, date(2024, 6, 21))

        f = get_third_friday_of_half(date(2024, 12, 31))
        self.assertEqual(f, date(2024, 6, 21))

    def testIsFloat(self):
        self.assertTrue(is_number('1.0'))
        self.assertTrue(is_number('0.1'))
        self.assertTrue(is_number('.1'))
        self.assertTrue(is_number('1.'))

    def testIsNotFloat(self):
        self.assertFalse(is_number('d.1'))
        self.assertFalse(is_number('1.d'))
        self.assertFalse(is_number('d'))
        self.assertFalse(is_number('!@'))

    def testCoalesce(self):
        data = {'a': 1, 'b': 2, 'c': 3}
        self.assertEqual(coalesce(data, ('a', )), 1)
        self.assertEqual(coalesce(data, ('d', 'b', 'a', 'c')), 2)
        self.assertEqual(coalesce(data, ('e', 'f', 'c')), 3)

    def testCoalesceDefault(self):
        data = {'a': 1}
        self.assertIsNone(coalesce(data, ('b', )))
        self.assertEqual(coalesce(data, ('b', ), 5), 5)
