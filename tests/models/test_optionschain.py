from pystonk.models.OptionContract import OptionContract
from pystonk.models.OptionsChain import OptionsChain


from datetime import datetime
from unittest import TestCase


class WeeklyOptionsReportTest(TestCase):
    def setUp(self) -> None:
        self._latest_price = 100.25
        self._contracts = {
            '90.00': (
                OptionContract('CALL', 'TEST_C90', 'test call 90', 90.00, 9.00, 9.01, '2X4', 10.00, .5, .25, .1, .9, .8, 100, True, False, int(datetime.now().timestamp()*1000), int(datetime.now().timestamp()*1000)),
                OptionContract('PUT', 'TEST_P90', 'test put 90', 90.00, .5, .56, '2X4', 10.00, .5, .25, .1, .9, .8, 100, True, False, int(datetime.now().timestamp()*1000), int(datetime.now().timestamp()*1000))
            ),
            '95.00': (
                OptionContract('CALL', 'TEST_C95', 'test call 95', 95.00, 5.00, 5.05, '2X4', 10.00, .5, .25, .1, .9, .8, 100, True, False, int(datetime.now().timestamp() * 1000), int(datetime.now().timestamp() * 1000)),
                OptionContract('PUT', 'TEST_P95', 'test put 95', 95.00, 1.0, 1.01, '2X4', 10.00, .5, .25, .1, .9, .8, 100, True, False, int(datetime.now().timestamp() * 1000), int(datetime.now().timestamp() * 1000))
            ),
            '100.00': (
                OptionContract('CALL', 'TEST_C100', 'test call 100', 100.00, 1.00, 1.01, '2X4', 10.00, .5, .25, .1, .9, .8, 100, True, False, int(datetime.now().timestamp() * 1000), int(datetime.now().timestamp() * 1000)),
                OptionContract('PUT', 'TEST_P100', 'test put 100', 100.00, 2.25, 2.26, '2X4', 10.00, .5, .25, .1, .9, .8, 100, True, False, int(datetime.now().timestamp() * 1000), int(datetime.now().timestamp() * 1000))
            ),
            '105.00': (
                OptionContract('CALL', 'TEST_C105', 'test call 105', 105.00, .75, .77, '2X4', 10.00, .5, .25, .1, .9, .8, 100, True, False, int(datetime.now().timestamp() * 1000), int(datetime.now().timestamp() * 1000)),
                OptionContract('PUT', 'TEST_P105', 'test put 105', 105.00, 5.00, 5.05, '2X4', 10.00, .5, .25, .1, .9, .8, 100, True, False, int(datetime.now().timestamp() * 1000), int(datetime.now().timestamp() * 1000))
            ),
            '110.00': (
                OptionContract('CALL', 'TEST_C110', 'test call 110', 110.00, .25, .26, '2X4', 10.00, .5, .25, .1, .9, .8, 100, True, False, int(datetime.now().timestamp() * 1000), int(datetime.now().timestamp() * 1000)),
                OptionContract('PUT', 'TEST_P110', 'test put 110', 110.00, 10.00, 10.01, '2X4', 10.00, .5, .25, .1, .9, .8, 100, True, False, int(datetime.now().timestamp() * 1000), int(datetime.now().timestamp() * 1000))
            ),
        }

    def testReport(self):
        o = OptionsChain(self._latest_price, self._contracts)

        self.assertEqual(len(o.matrix()), 5, "OptionsChain did not return expected number of call/put pairs")

        sell_call = o.closestCallOption(.75)
        self.assertEqual(sell_call[0].strikePrice, 105.00, "OptionsChain did not return expected closest sell-call option's strike price")
        self.assertEqual(sell_call[1], 4.75, "OptionsChain did not return expected closest sell-call option's price diff")
        self.assertEqual(sell_call[2], 4.74, "OptionsChain did not return expected closest sell-call option's percent diff")

        buy_call = o.closestCallOption(.25, is_sell=False)
        self.assertEqual(buy_call[0].strikePrice, 110.00, "OptionsChain did not return expected closest buy-call option's strike price")
        self.assertEqual(buy_call[1], 9.75, "OptionsChain did not return expected closest buy-call option's price diff")
        self.assertEqual(buy_call[2], 9.73, "OptionsChain did not return expected closest buy-call option's percent diff")

        sell_put = o.closestPutOption(2.24)
        self.assertEqual(sell_put[0].strikePrice, 100.00, "OptionsChain did not return expected closest sell-put option's strike price")
        self.assertEqual(sell_put[1], -0.25, "OptionsChain did not return expected closest sell-put option's price diff")
        self.assertEqual(sell_put[2], -0.25, "OptionsChain did not return expected closest sell-put option's percent diff")

        buy_put = o.closestPutOption(1.0, is_sell=False)
        self.assertEqual(buy_put[0].strikePrice, 95.00, "OptionsChain did not return expected closest buy-put option's strike price")
        self.assertEqual(buy_put[1], -5.25, "OptionsChain did not return expected closest buy-put option's price diff")
        self.assertEqual(buy_put[2], -5.24, "OptionsChain did not return expected closest buy-put option's percent diff")
