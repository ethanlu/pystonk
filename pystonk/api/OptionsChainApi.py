from pystonk.api import Api
from pystonk.api.Types import ContractType, OptionType, StrategyType
from pystonk.models.OptionContract import OptionContract

from datetime import date
from typing import Dict, Tuple


def build_contracts_list(friday_date: date, contracts: Dict) -> Dict[str, OptionContract]:
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


class OptionsChainApi(Api):
    ENDPOINT = "https://api.schwabapi.com/marketdata/v1/chains"

    def __init__(self, app_key: str, app_secret: str):
        super().__init__(app_key, app_secret)

    def get_single_option_chain(self, symbol: str, expire_date: date, strike_count: int = 100) -> Dict[str, Tuple[OptionContract, OptionContract]]:
        symbol = symbol.upper()
        self.logger.debug(f"getting weekly single options chain for {symbol}")
        data = self._get(
            self.ENDPOINT,
            params={
                'symbol': symbol,
                'contractType': ContractType.ALL.value,
                'strategy': StrategyType.SINGLE.value,
                'optionType': OptionType.STANDARD.value,
                'fromDate': expire_date.strftime('%Y-%m-%d'),
                'toDate': expire_date.strftime('%Y-%m-%d'),
                'strikeCount': strike_count
            },
            headers={'Authorization': f"Bearer {self.get_access_token()}"}
        )

        puts = build_contracts_list(expire_date, data['putExpDateMap'])
        calls = build_contracts_list(expire_date, data['callExpDateMap'])

        return {k: (calls[k], puts[k]) for k in calls.keys()}
