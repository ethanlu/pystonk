from pystonk.models.OptionContract import OptionContract
from pystonk.reports.WeeklyOptionsReport import WeeklyOptionsReport


from datetime import datetime
from mock import MagicMock
from unittest import TestCase


class WeeklyOptionsReportTest(TestCase):
    def setUp(self) -> None:
        self._mock_api = MagicMock()
        self._mock_api.getQuote.return_value = 100.25
        self._mock_api.getWeeklySingleOptionChain.return_value = self.fixtureWeeklyOptionsChainApiResponse()

    def fixtureWeeklyOptionsChainApiResponse(self):
        return {
            '90.00': (
                OptionContract('CALL', 'TEST_C90', 'test call 90', 90.00, 9.00, 9.01, '2X4', 10.00, .5, .25, .1, .9, .8, 100, True, False, int(datetime.now().timestamp()*1000), int(datetime.now().timestamp()*1000)),
                OptionContract('PUT', 'TEST_P90', 'test put 90', 90.00, .5, .56, '2X4', 10.00, .5, .25, .1, .9, .8, 100, True, False, int(datetime.now().timestamp()*1000), int(datetime.now().timestamp()*1000))
            ),
            '95.00': (
                OptionContract('CALL', 'TEST_C95', 'test call 95', 95.00, 5.00, 5.05, '2X4', 10.00, .5, .25, .1, .9, .8, 100, True, False, int(datetime.now().timestamp() * 1000), int(datetime.now().timestamp() * 1000)),
                OptionContract('PUT', 'TEST_P95', 'test put 95', 95.00, 1.0, 1.01, '2X4', 10.00, .5, .25, .1, .9, .8, 100, True, False, int(datetime.now().timestamp() * 1000), int(datetime.now().timestamp() * 1000))
            ),
            '100.00': (
                OptionContract('CALL', 'TEST_C100', 'test call 100', 100.00, .25, .26, '2X4', 10.00, .5, .25, .1, .9, .8, 100, True, False, int(datetime.now().timestamp() * 1000), int(datetime.now().timestamp() * 1000)),
                OptionContract('PUT', 'TEST_P100', 'test put 100', 100.00, 2.25, 2.26, '2X4', 10.00, .5, .25, .1, .9, .8, 100, True, False, int(datetime.now().timestamp() * 1000), int(datetime.now().timestamp() * 1000))
            ),
            '105.00': (
                OptionContract('CALL', 'TEST_C105', 'test call 105', 105.00, .75, .74, '2X4', 10.00, .5, .25, .1, .9, .8, 100, True, False, int(datetime.now().timestamp() * 1000), int(datetime.now().timestamp() * 1000)),
                OptionContract('PUT', 'TEST_P105', 'test put 105', 105.00, 5.00, 5.05, '2X4', 10.00, .5, .25, .1, .9, .8, 100, True, False, int(datetime.now().timestamp() * 1000), int(datetime.now().timestamp() * 1000))
            ),
            '110.00': (
                OptionContract('CALL', 'TEST_C110', 'test call 110', 110.00, 1.00, 1.01, '2X4', 10.00, .5, .25, .1, .9, .8, 100, True, False, int(datetime.now().timestamp() * 1000), int(datetime.now().timestamp() * 1000)),
                OptionContract('PUT', 'TEST_P110', 'test put 110', 110.00, 10.00, 10.01, '2X4', 10.00, .5, .25, .1, .9, .8, 100, True, False, int(datetime.now().timestamp() * 1000), int(datetime.now().timestamp() * 1000))
            ),
        }

    def testRetrieveData(self):
        o = WeeklyOptionsReport(self._mock_api, self._mock_api)
        r = o.retrieveData('test')
        self.assertTrue(r, "WeeklyOptionsReport did not retrieve data successfully")
        self.assertEqual(self._mock_api.getQuote.call_count, 1, "Mocked quote api not called expected amount of times")
        self.assertEqual(self._mock_api.getWeeklySingleOptionChain.call_count, 1, "Mocked options chain api not called expected amount of times")

    def testReport(self):
        premium = 1.0
        o = WeeklyOptionsReport(self._mock_api, self._mock_api)
        o.retrieveData('test')
        r = list(o.generate())

        self.assertEqual(o.getMark(), 100.25, "WeeklyOptionsReport did not return expected mark")
        self.assertEqual(len(r), 5, "WeeklyOptionsReport did not return expected number of call/put pairs")
        ((call_strike, call_diff, call_percent_change), (put_strike, put_diff, put_percent_change)) = o.getStrikePricesForTargetPremium(premium)
        self.assertEqual(call_strike.strikePrice, 110.00, "WeeklyOptionsReport did not return expected target call strike")
        self.assertEqual(call_diff, 9.75, "WeeklyOptionsReport did not return expected target call strike diff")
        self.assertEqual(call_percent_change, 9.73, "WeeklyOptionsReport did not return expected target call strike percent change")
        self.assertEqual(put_strike.strikePrice, 95.00, "WeeklyOptionsReport did not return expected target put strike")
        self.assertEqual(put_diff, -5.25, "WeeklyOptionsReport did not return expected target put strike diff")
        self.assertEqual(put_percent_change, -5.24, "WeeklyOptionsReport did not return expected target put strike percent change")