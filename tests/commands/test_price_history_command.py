from pystonk.commands.PriceHistoryCommand import PriceHistoryCommand
from pystonk.views.HelpView import HelpView
from pystonk.views.PriceHistoryView import PriceHistoryView

from mock import MagicMock, patch
from unittest import TestCase


class PriceHistoryCommandTest(TestCase):
    def setUp(self) -> None:
        self._mock_api = MagicMock()

    @patch('pystonk.commands.PriceHistoryCommand.PriceHistoryEstimate')
    def testPriceHistoryCommandResponse(self, price_history_estimate_mock):
        o = PriceHistoryCommand(self._mock_api)

        self.assertIsInstance(o.execute('ph abc 10'), PriceHistoryView, "PriceHistoryCommand did not return expected PriceHistoryView when correct parameters are passed")
        self.assertIsInstance(o.execute('ph def 10.0'), PriceHistoryView, "PriceHistoryCommand did not return expected PriceHistoryView when correct parameters are passed")

    @patch('pystonk.commands.PriceHistoryCommand.PriceHistoryEstimate')
    def testPriceHistoryCommandHelpResponse(self, price_history_estimate_mock):
        o = PriceHistoryCommand(self._mock_api)

        self.assertIsInstance(o.execute('ph'), HelpView, "PriceHistoryCommand did not return HelpView when no parameter is passed")
        self.assertIsInstance(o.execute('ph 10 abc'), HelpView, "PriceHistoryCommand did not return HelpView wrong parameter type is passed")
        self.assertIsInstance(o.execute('ph abc 11 xyz'), HelpView, "PriceHistoryCommand did not return HelpView when extra parameter is passed")
        self.assertIsInstance(o.execute('ph -x'), HelpView, "PriceHistoryCommand did not return HelpView when optional parameter is passed")
