from pystonk import get_conf_path
from pystonk.api.PriceHistory import PriceHistory, PeriodType, FrequencyType
from pystonk.common.LoggerMixin import LoggerMixin

from pyhocon import ConfigFactory

class PyStonk(LoggerMixin):

    def __init__(self, configuration: dict):
        self._configuration = configuration

    def run(self):
        ph = PriceHistory(self._configuration['api_key'])
        results = ph.getPriceHistory(
            symbol='tsla',
            period_type=PeriodType.YTD,
            period=1,
            frequency_type=FrequencyType.WEEKLY,
            frequency=1
        )
        # api.run(
        #     symbol='tsla',
        #     start=datetime.strptime('2022-01-01', '%Y-%m-%d'),
        #     end=datetime.today()
        # )

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = PyStonk(
        ConfigFactory.parse_file(get_conf_path('app.conf'))
    )
    app.run()