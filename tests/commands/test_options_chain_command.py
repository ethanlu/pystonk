from pystonk.commands.OptionsChainCommand import OptionsChainCommand
from pystonk.views.HelpView import HelpView
from pystonk.views.OptionsChainView import OptionsChainView

from mock import MagicMock
from unittest import TestCase


class OptionsChainCommandTest(TestCase):
    def setUp(self) -> None:
        self._mock_api = MagicMock()

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
