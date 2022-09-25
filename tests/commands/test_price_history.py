from pystonk.commands.PriceHistoryCommand import PriceHistoryCommand
from pystonk.models.Quote import Quote
from pystonk.views.ErrorView import ErrorView
from pystonk.views.HelpView import HelpView
from pystonk.views.PriceHistoryView import PriceHistoryView

from mock import MagicMock, patch
from unittest import TestCase


class PriceHistoryCommandTest(TestCase):
    def setUp(self) -> None:
        self._mock_api = MagicMock()
        self._mock_api.get_quote.return_value = Quote(
            symbol='TEST',
            price=1.23,
            last_price=5.678,
            high_price=5.001,
            low_price=10.002,
            high_price_52=1.03,
            low_price_52=.33,
            bid=10.01,
            ask=.52,
            bid_size=10,
            ask_size=3,
            volume=100
        )

    @patch('pystonk.commands.PriceHistoryCommand.PriceHistoryEstimate')
    def testPriceHistoryCommandResponse(self, price_history_estimate_mock):
        o = PriceHistoryCommand(self._mock_api, self._mock_api)

        self.assertIsInstance(o.execute('ph abc 10'), PriceHistoryView, "PriceHistoryCommand did not return expected PriceHistoryView when correct parameters are passed")
        self.assertIsInstance(o.execute('ph def 10.0'), PriceHistoryView, "PriceHistoryCommand did not return expected PriceHistoryView when correct parameters are passed")
        self.assertIsInstance(o.execute('ph abc -10'), PriceHistoryView, "PriceHistoryCommand did not return expected PriceHistoryView when correct parameters are passed")
        self.assertIsInstance(o.execute('ph def -10.0'), PriceHistoryView, "PriceHistoryCommand did not return expected PriceHistoryView when correct parameters are passed")
        self.assertIsInstance(o.execute('ph def 0.0'), PriceHistoryView, "PriceHistoryCommand did not return expected PriceHistoryView when correct parameters are passed")
        self.assertIsInstance(o.execute('ph def 1 -v'), PriceHistoryView, "PriceHistoryCommand did not return expected PriceHistoryView when correct parameters are passed")
        self.assertIsInstance(o.execute('ph def 1 --verbose'), PriceHistoryView, "PriceHistoryCommand did not return expected PriceHistoryView when correct parameters are passed")
        self.assertIsInstance(o.execute('ph def 2 -f weekly'), PriceHistoryView, "PriceHistoryCommand did not return expected PriceHistoryView when correct parameters are passed")
        self.assertIsInstance(o.execute('ph def 2 -f monthly'), PriceHistoryView, "PriceHistoryCommand did not return expected PriceHistoryView when correct parameters are passed")
        self.assertIsInstance(o.execute('ph def 2 -f daily'), PriceHistoryView, "PriceHistoryCommand did not return expected PriceHistoryView when correct parameters are passed")
        self.assertIsInstance(o.execute('ph def 3 -p 1'), PriceHistoryView, "PriceHistoryCommand did not return expected PriceHistoryView when correct parameters are passed")
        self.assertIsInstance(o.execute('ph def 3 -p 2'), PriceHistoryView, "PriceHistoryCommand did not return expected PriceHistoryView when correct parameters are passed")
        self.assertIsInstance(o.execute('ph def 3 -p 3'), PriceHistoryView, "PriceHistoryCommand did not return expected PriceHistoryView when correct parameters are passed")
        self.assertIsInstance(o.execute('ph def 3 -p 5'), PriceHistoryView, "PriceHistoryCommand did not return expected PriceHistoryView when correct parameters are passed")

    @patch('pystonk.commands.PriceHistoryCommand.PriceHistoryEstimate')
    def testPriceHistoryCommandHelpResponse(self, price_history_estimate_mock):
        o = PriceHistoryCommand(self._mock_api, self._mock_api)

        self.assertIsInstance(o.execute('ph'), HelpView, "PriceHistoryCommand did not return HelpView when no parameter is passed")
        self.assertIsInstance(o.execute('ph 10 abc'), HelpView, "PriceHistoryCommand did not return HelpView wrong parameter type is passed")
        self.assertIsInstance(o.execute('ph abc 11 xyz'), HelpView, "PriceHistoryCommand did not return HelpView when extra parameter is passed")
        self.assertIsInstance(o.execute('ph -x'), HelpView, "PriceHistoryCommand did not return HelpView when optional parameter is passed")

    @patch('pystonk.commands.PriceHistoryCommand.PriceHistoryEstimate')
    def testPriceHistoryCommandErrorResponse(self, price_history_estimate_mock):
        self._mock_api.get_quote.return_value = None
        o = PriceHistoryCommand(self._mock_api, self._mock_api)

        self.assertIsInstance(o.execute('ph nonexistent 10'), ErrorView, "PriceHistoryCommand did not return expected ErrorView when expected")