from pystonk.utils import get_next_monday_friday, percent_diff

from datetime import date
from unittest import TestCase


class UtilsTest(TestCase):
    def testPercentDiff(self):
        r = percent_diff(100, 50)
        self.assertEqual(r, -50.00)

        r = percent_diff(50, 100)
        self.assertEqual(r, 100.00)

    def testGetNextMondayFridayInSameMonth(self):
        m, f = get_next_monday_friday(date(2020, 2, 2))
        self.assertEqual(m, date(2020, 2, 3))
        self.assertEqual(f, date(2020, 2, 7))

        m, f = get_next_monday_friday(date(2020, 2, 3))
        self.assertEqual(m, date(2020, 2, 10))
        self.assertEqual(f, date(2020, 2, 14))

        m, f = get_next_monday_friday(date(2020, 2, 4))
        self.assertEqual(m, date(2020, 2, 10))
        self.assertEqual(f, date(2020, 2, 14))

        m, f = get_next_monday_friday(date(2020, 2, 5))
        self.assertEqual(m, date(2020, 2, 10))
        self.assertEqual(f, date(2020, 2, 14))

        m, f = get_next_monday_friday(date(2020, 2, 6))
        self.assertEqual(m, date(2020, 2, 10))
        self.assertEqual(f, date(2020, 2, 14))

        m, f = get_next_monday_friday(date(2020, 2, 7))
        self.assertEqual(m, date(2020, 2, 10))
        self.assertEqual(f, date(2020, 2, 14))

        m, f = get_next_monday_friday(date(2020, 2, 8))
        self.assertEqual(m, date(2020, 2, 10))
        self.assertEqual(f, date(2020, 2, 14))

    def testGetNextMondayFridayInTwoMonths(self):
        m, f = get_next_monday_friday(date(2020, 3, 29))
        self.assertEqual(m, date(2020, 3, 30))
        self.assertEqual(f, date(2020, 4, 3))

        m, f = get_next_monday_friday(date(2020, 3, 30))
        self.assertEqual(m, date(2020, 4, 6))
        self.assertEqual(f, date(2020, 4, 10))

        m, f = get_next_monday_friday(date(2020, 3, 31))
        self.assertEqual(m, date(2020, 4, 6))
        self.assertEqual(f, date(2020, 4, 10))

        m, f = get_next_monday_friday(date(2020, 4, 1))
        self.assertEqual(m, date(2020, 4, 6))
        self.assertEqual(f, date(2020, 4, 10))

        m, f = get_next_monday_friday(date(2020, 4, 2))
        self.assertEqual(m, date(2020, 4, 6))
        self.assertEqual(f, date(2020, 4, 10))

        m, f = get_next_monday_friday(date(2020, 4, 3))
        self.assertEqual(m, date(2020, 4, 6))
        self.assertEqual(f, date(2020, 4, 10))

        m, f = get_next_monday_friday(date(2020, 4, 4))
        self.assertEqual(m, date(2020, 4, 6))
        self.assertEqual(f, date(2020, 4, 10))

    def testGetNextMondayFridayInTwoYears(self):
        m, f = get_next_monday_friday(date(2020, 12, 27))
        self.assertEqual(m, date(2020, 12, 28))
        self.assertEqual(f, date(2021, 1, 1))

        m, f = get_next_monday_friday(date(2020, 12, 28))
        self.assertEqual(m, date(2021, 1, 4))
        self.assertEqual(f, date(2021, 1, 8))

        m, f = get_next_monday_friday(date(2020, 12, 29))
        self.assertEqual(m, date(2021, 1, 4))
        self.assertEqual(f, date(2021, 1, 8))

        m, f = get_next_monday_friday(date(2020, 12, 30))
        self.assertEqual(m, date(2021, 1, 4))
        self.assertEqual(f, date(2021, 1, 8))

        m, f = get_next_monday_friday(date(2020, 12, 31))
        self.assertEqual(m, date(2021, 1, 4))
        self.assertEqual(f, date(2021, 1, 8))

        m, f = get_next_monday_friday(date(2021, 1, 1))
        self.assertEqual(m, date(2021, 1, 4))
        self.assertEqual(f, date(2021, 1, 8))

        m, f = get_next_monday_friday(date(2021, 1, 2))
        self.assertEqual(m, date(2021, 1, 4))
        self.assertEqual(f, date(2021, 1, 8))

    def testGetNextMondayFridayWithLeapYear(self):
        m, f = get_next_monday_friday(date(2020, 2, 23))
        self.assertEqual(m, date(2020, 2, 24))
        self.assertEqual(f, date(2020, 2, 28))

        m, f = get_next_monday_friday(date(2020, 2, 24))
        self.assertEqual(m, date(2020, 3, 2))
        self.assertEqual(f, date(2020, 3, 6))

        m, f = get_next_monday_friday(date(2020, 2, 25))
        self.assertEqual(m, date(2020, 3, 2))
        self.assertEqual(f, date(2020, 3, 6))

        m, f = get_next_monday_friday(date(2020, 2, 26))
        self.assertEqual(m, date(2020, 3, 2))
        self.assertEqual(f, date(2020, 3, 6))

        m, f = get_next_monday_friday(date(2020, 2, 27))
        self.assertEqual(m, date(2020, 3, 2))
        self.assertEqual(f, date(2020, 3, 6))

        m, f = get_next_monday_friday(date(2020, 2, 28))
        self.assertEqual(m, date(2020, 3, 2))
        self.assertEqual(f, date(2020, 3, 6))

        m, f = get_next_monday_friday(date(2020, 2, 29))
        self.assertEqual(m, date(2020, 3, 2))
        self.assertEqual(f, date(2020, 3, 6))