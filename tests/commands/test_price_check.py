from pystonk.commands.PriceCheckCommand import PriceCheckCommand
from pystonk.models.Quote import Quote
from pystonk.views.ErrorView import ErrorView
from pystonk.views.HelpView import HelpView
from pystonk.views.PriceCheckView import PriceCheckView

from mock import MagicMock
from unittest import TestCase


class PriceCheckCommandTest(TestCase):
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

    def testPriceCheckCommandResponse(self):
        o = PriceCheckCommand(self._mock_api)

        self.assertIsInstance(o.execute('pc abc'), PriceCheckView, "PriceCheckCommand did not return PriceCheckView when correct parameters are passed")

    def testPriceCheckCommandHelpResponse(self):
        o = PriceCheckCommand(self._mock_api)

        self.assertIsInstance(o.execute('pc'), HelpView, "PriceCheckCommand did not return HelpView when no parameter is passed")
        self.assertIsInstance(o.execute('pc abc def'), HelpView, "PriceCheckCommand did not return HelpView when extra parameter is passed")
        self.assertIsInstance(o.execute('pc -x'), HelpView, "PriceCheckCommand did not return HelpView when optional parameter is passed")

    def testPriceCheckCommandErrorResponse(self):
        self._mock_api.get_quote.return_value = None
        o = PriceCheckCommand(self._mock_api)

        self.assertIsInstance(o.execute('pc nonexistent'), ErrorView, "PriceCheckCommand did not return ErrorView when expected")
