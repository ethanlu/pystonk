from pystonk.commands.OptionsChainCommand import OptionsChainCommand
from pystonk.models.Quote import Quote
from pystonk.views.ErrorView import ErrorView
from pystonk.views.HelpView import HelpView
from pystonk.views.OptionsChainView import OptionsChainView

from mock import MagicMock
from unittest import TestCase


class OptionsChainCommandTest(TestCase):
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

    def testOptionsChainCommandResponse(self):
        o = OptionsChainCommand(self._mock_api, self._mock_api)

        self.assertIsInstance(o.execute('oc abc 10'), OptionsChainView, "OptionsChainCommand did not return expected PriceHistoryView when correct parameters are passed")
        self.assertIsInstance(o.execute('oc def 10.0'), OptionsChainView, "OptionsChainCommand did not return expected PriceHistoryView when correct parameters are passed")

    def testOptionsChainCommandHelpResponse(self):
        o = OptionsChainCommand(self._mock_api, self._mock_api)

        self.assertIsInstance(o.execute('oc'), HelpView, "OptionsChainCommand did not return HelpView when no parameter is passed")
        self.assertIsInstance(o.execute('oc 10 abc'), HelpView, "OptionsChainCommand did not return HelpView wrong parameter type is passed")
        self.assertIsInstance(o.execute('oc abc 11 xyz'), HelpView, "OptionsChainCommand did not return HelpView when extra parameter is passed")
        self.assertIsInstance(o.execute('oc -x'), HelpView, "OptionsChainCommand did not return HelpView when optional parameter is passed")

    def testOptionsChainCommandErrorResponse(self):
        self._mock_api.get_quote.return_value = None
        o = OptionsChainCommand(self._mock_api, self._mock_api)

        self.assertIsInstance(o.execute('oc nonexistent 10'), ErrorView, "OptionsChainCommand did not return expected ErrorView when expected")
