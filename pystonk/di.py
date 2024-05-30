from pystonk import get_conf_path
from pystonk.api.OptionsChainApi import OptionsChainApi
from pystonk.api.PriceHistoryApi import PriceHistoryApi
from pystonk.api.QuoteApi import QuoteApi
from pystonk.commands.PriceCheckCommand import PriceCheckCommand
from pystonk.commands.PriceHistoryCommand import PriceHistoryCommand
from pystonk.commands.OptionsChainCommand import OptionsChainCommand
from pystonk.commands.SupportResistanceCommand import SupportResistanceCommand

from dependency_injector import containers, providers
from pyhocon import ConfigFactory


class Container(containers.DeclarativeContainer):
    configuration = providers.Singleton(
        ConfigFactory.parse_file,
        get_conf_path()
    )

    options_chain_api = providers.Singleton(
        OptionsChainApi,
        app_key=configuration()['app_key'],
        app_secret=configuration()['app_secret']
    )

    price_history_api = providers.Singleton(
        PriceHistoryApi,
        app_key=configuration()['app_key'],
        app_secret=configuration()['app_secret']
    )

    quote_api = providers.Singleton(
        QuoteApi,
        app_key=configuration()['app_key'],
        app_secret=configuration()['app_secret']
    )

    available_commands = providers.Object(
        [
            providers.Singleton(
                OptionsChainCommand,
                quote_api(),
                options_chain_api()
            )(),
            providers.Singleton(
                PriceCheckCommand,
                quote_api()
            )(),
            providers.Singleton(
                PriceHistoryCommand,
                quote_api(),
                price_history_api()
            )(),
            providers.Singleton(
                SupportResistanceCommand,
                price_history_api()
            )()
        ]
    )
