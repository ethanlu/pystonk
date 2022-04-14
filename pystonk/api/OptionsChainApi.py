from pystonk.api import Api
from pystonk.api.Types import ContractType, OptionType, StrategyType
from pystonk.models.OptionContract import OptionContract
from pystonk.utils import get_next_monday_friday

from datetime import date
from typing import Dict, Tuple

import requests


class OptionsChainApi(Api):
    ENDPOINT = "https://api.tdameritrade.com/v1/marketdata/chains"

    def __init__(self, api_key: str):
        super().__init__(api_key)

    def _buildContractsList(self, friday_date: date, contracts: Dict) -> Dict[str, OptionContract]:
        try:
            date_key = friday_date.strftime('%Y-%m-%d:')
            contract_date_key = next((k for k in contracts.keys() if k.startswith(date_key)))

            return {
                strike_price: OptionContract(
                    put_call=contract[0]['putCall'],
                    symbol=contract[0]['symbol'],
                    description=contract[0]['description'],
                    strike_price=contract[0]['strikePrice'],
                    bid=contract[0]['bid'],
                    ask=contract[0]['ask'],
                    bid_ask_size=contract[0]['bidAskSize'],
                    volatility=contract[0]['volatility'],
                    delta=contract[0]['delta'],
                    gamma=contract[0]['gamma'],
                    theta=contract[0]['theta'],
                    vega=contract[0]['vega'],
                    rho=contract[0]['rho'],
                    open_interest=contract[0]['openInterest'],
                    in_the_money=contract[0]['inTheMoney'],
                    non_standard=contract[0]['nonStandard'],
                    expiration_datetime=contract[0]['expirationDate'],
                    last_trading_datetime=contract[0]['lastTradingDay']
                )
                for strike_price, contract in contracts[contract_date_key].items()
            }
        except StopIteration:
            return {}

    def getWeeklySingleOptionChain(self, symbol: str, week_date: date, strike_count: int = 100) -> Dict[str, Tuple[OptionContract, OptionContract]]:
        symbol = symbol.upper()
        next_monday, next_friday = get_next_monday_friday(week_date)
        params = {
            'apikey': self._api_key,
            'symbol': symbol,
            'contractType': ContractType.ALL.value,
            'strategy': StrategyType.SINGLE.value,
            'optionType': OptionType.STANDARD.value,
            'fromDate': next_monday.strftime('%Y-%m-%d'),
            'toDate': next_friday.strftime('%Y-%m-%d'),
            'strikeCount': strike_count
        }
        self.logger.debug(f"getting weekly single options chain for {symbol} with params : {params}")
        response = requests.get(
            self.ENDPOINT,
            params=params
        )
        self.logger.debug(f"request : {response.url}")
        self.logger.debug(f"response : {response.status_code}")
        response_data = response.json()

        puts = self._buildContractsList(next_friday, response_data['putExpDateMap'])
        calls = self._buildContractsList(next_friday, response_data['callExpDateMap'])

        return {k: (calls[k], puts[k])
            for k in calls.keys()
        }