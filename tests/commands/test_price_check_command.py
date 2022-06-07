from pystonk.commands.PriceCheckCommand import PriceCheckCommand
from pystonk.views.HelpView import HelpView
from pystonk.views.PriceCheckView import PriceCheckView

from mock import MagicMock
from unittest import TestCase


class PriceCheckCommandTest(TestCase):
    def setUp(self) -> None:
        self._mock_api = MagicMock()

    def testPriceCheckCommandResponse(self):
        o = PriceCheckCommand(self._mock_api)

        self.assertIsInstance(o.execute('pc abc'), PriceCheckView, "PriceCheckCommand did not return PriceCheckView when correct parameters are passed")

    def testPriceCheckCommandHelpResponse(self):
        o = PriceCheckCommand(self._mock_api)

        self.assertIsInstance(o.execute('pc'), HelpView, "PriceCheckCommand did not return HelpView when no parameter is passed")
        self.assertIsInstance(o.execute('pc abc def'), HelpView, "PriceCheckCommand did not return HelpView when extra parameter is passed")
        self.assertIsInstance(o.execute('pc -x'), HelpView, "PriceCheckCommand did not return HelpView when optional parameter is passed")
