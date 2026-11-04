from pystonk.commands.PriceHistoryCommand import PriceHistoryCommand
from pystonk.models.Quote import Quote
from pystonk.views.ErrorView import ErrorView
from pystonk.views.HelpView import HelpView
from pystonk.views.PriceHistoryView import PriceHistoryView

from io import BytesIO
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

    @patch('pystonk.commands.PriceHistoryCommand.PriceHistoryAnalysis')
    @patch('pystonk.commands.PriceHistoryCommand.ImageWriter')
    def testPriceHistoryCommandResponse(self, image_writer_class_mock, price_history_analysis_class_mock):
        pha_mock = price_history_analysis_class_mock.return_value
        pha_mock.histogram = MagicMock(return_value=BytesIO())
        pha_mock.qq = MagicMock(return_value=BytesIO())
        iw_mock = image_writer_class_mock.return_value
        iw_mock.write = MagicMock(return_value="image_url")

        o = PriceHistoryCommand(self._mock_api, self._mock_api)

        self.assertIsInstance(o.execute('ph abc 10'), PriceHistoryView, "PriceHistoryCommand did not return expected PriceHistoryView when correct parameters are passed")
        self.assertEqual(pha_mock.histogram.call_count, 1, "PriceHistoryCommand did call the PriceHistoryAnalysis.histogram function the expected number of times")
        self.assertEqual(pha_mock.qq.call_count, 0, "PriceHistoryCommand did call the PriceHistoryAnalysis.qq function the expected number of times")

        self.assertIsInstance(o.execute('ph def 10.0'), PriceHistoryView, "PriceHistoryCommand did not return expected PriceHistoryView when correct parameters are passed")
        self.assertIsInstance(o.execute('ph abc -10'), PriceHistoryView, "PriceHistoryCommand did not return expected PriceHistoryView when correct parameters are passed")
        self.assertIsInstance(o.execute('ph def -10.0'), PriceHistoryView, "PriceHistoryCommand did not return expected PriceHistoryView when correct parameters are passed")
        self.assertIsInstance(o.execute('ph def 0.0'), PriceHistoryView, "PriceHistoryCommand did not return expected PriceHistoryView when correct parameters are passed")
        self.assertIsInstance(o.execute('ph def 1 -v'), PriceHistoryView, "PriceHistoryCommand did not return expected PriceHistoryView when correct parameters are passed")
        self.assertEqual(pha_mock.histogram.call_count, 6, "PriceHistoryCommand did call the PriceHistoryAnalysis.histogram function the expected number of times")
        self.assertEqual(pha_mock.qq.call_count, 1, "PriceHistoryCommand did call the PriceHistoryAnalysis.qq function the expected number of times")

        self.assertIsInstance(o.execute('ph def 1 --verbose'), PriceHistoryView, "PriceHistoryCommand did not return expected PriceHistoryView when correct parameters are passed")
        self.assertEqual(pha_mock.histogram.call_count, 7, "PriceHistoryCommand did call the PriceHistoryAnalysis.histogram function the expected number of times")
        self.assertEqual(pha_mock.qq.call_count, 2, "PriceHistoryCommand did call the PriceHistoryAnalysis.qq function the expected number of times")

        self.assertIsInstance(o.execute('ph def 2 -f weekly'), PriceHistoryView, "PriceHistoryCommand did not return expected PriceHistoryView when correct parameters are passed")
        self.assertIsInstance(o.execute('ph def 2 -f monthly'), PriceHistoryView, "PriceHistoryCommand did not return expected PriceHistoryView when correct parameters are passed")
        self.assertIsInstance(o.execute('ph def 2 -f daily'), PriceHistoryView, "PriceHistoryCommand did not return expected PriceHistoryView when correct parameters are passed")
        self.assertIsInstance(o.execute('ph def 3 -p 1'), PriceHistoryView, "PriceHistoryCommand did not return expected PriceHistoryView when correct parameters are passed")
        self.assertIsInstance(o.execute('ph def 3 -p 2'), PriceHistoryView, "PriceHistoryCommand did not return expected PriceHistoryView when correct parameters are passed")
        self.assertIsInstance(o.execute('ph def 3 -p 3'), PriceHistoryView, "PriceHistoryCommand did not return expected PriceHistoryView when correct parameters are passed")
        self.assertIsInstance(o.execute('ph def 3 -p 5'), PriceHistoryView, "PriceHistoryCommand did not return expected PriceHistoryView when correct parameters are passed")
        self.assertEqual(pha_mock.histogram.call_count, 14, "PriceHistoryCommand did call the PriceHistoryAnalysis.histogram function the expected number of times")
        self.assertEqual(pha_mock.qq.call_count, 2, "PriceHistoryCommand did call the PriceHistoryAnalysis.qq function the expected number of times")

    @patch('pystonk.commands.PriceHistoryCommand.PriceHistoryAnalysis')
    @patch('pystonk.commands.PriceHistoryCommand.ImageWriter')
    def testPriceHistoryCommandHelpResponse(self, image_writer_class_mock, price_history_analysis_class_mock):
        pha_mock = price_history_analysis_class_mock.return_value
        pha_mock.histogram = MagicMock(return_value=BytesIO())
        pha_mock.qq = MagicMock(return_value=BytesIO())
        iw_mock = image_writer_class_mock.return_value
        iw_mock.write = MagicMock(return_value="image_url")

        o = PriceHistoryCommand(self._mock_api, self._mock_api)

        self.assertIsInstance(o.execute('ph'), HelpView, "PriceHistoryCommand did not return HelpView when no parameter is passed")
        self.assertIsInstance(o.execute('ph 10 abc'), HelpView, "PriceHistoryCommand did not return HelpView wrong parameter type is passed")
        self.assertIsInstance(o.execute('ph abc 11 xyz'), HelpView, "PriceHistoryCommand did not return HelpView when extra parameter is passed")
        self.assertIsInstance(o.execute('ph -x'), HelpView, "PriceHistoryCommand did not return HelpView when optional parameter is passed")
        self.assertEqual(pha_mock.histogram.call_count, 0, "PriceHistoryCommand did call the PriceHistoryAnalysis.histogram function the expected number of times")
        self.assertEqual(pha_mock.qq.call_count, 0, "PriceHistoryCommand did call the PriceHistoryAnalysis.qq function the expected number of times")

    @patch('pystonk.commands.PriceHistoryCommand.PriceHistoryAnalysis')
    @patch('pystonk.commands.PriceHistoryCommand.ImageWriter')
    def testPriceHistoryCommandErrorResponse(self, image_writer_class_mock, price_history_analysis_class_mock):
        pha_mock = price_history_analysis_class_mock.return_value
        pha_mock.histogram = MagicMock(return_value=BytesIO())
        pha_mock.qq = MagicMock(return_value=BytesIO())
        iw_mock = image_writer_class_mock.return_value
        iw_mock.write = MagicMock(return_value="image_url")

        self._mock_api.get_quote.return_value = None
        o = PriceHistoryCommand(self._mock_api, self._mock_api)

        self.assertIsInstance(o.execute('ph nonexistent 10'), ErrorView, "PriceHistoryCommand did not return expected ErrorView when expected")
        self.assertEqual(pha_mock.histogram.call_count, 0, "PriceHistoryCommand did call the PriceHistoryAnalysis.histogram function the expected number of times")
        self.assertEqual(pha_mock.qq.call_count, 0, "PriceHistoryCommand did call the PriceHistoryAnalysis.qq function the expected number of times")
