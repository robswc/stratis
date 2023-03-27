import os
from datetime import datetime

import pandas as pd
import requests

from components.ohlc import DataAdapter, OHLC
from components.ohlc.symbol import Symbol


class APIDataAdapter(DataAdapter):

    url = os.getenv('DATA_API_URL', None)

    def get_data(
            self,
            start: datetime = None,
            end: datetime = None,
            symbol: str = None,
            **kwargs
    ):

        if self.url is None:
            raise Exception('DATA_API_URL not set')

        # you will have to modify this to get the data from the API, this is just an example
        r = requests.get(f'{self.url}/data/{symbol}/ohlc/5?only_completed=true')
        r.raise_for_status()
        candles = r.json().get('candles', [])

        # strategy a dataframe from the candles
        df = pd.DataFrame.from_records(candles)
        df.set_index('timestamp', inplace=True)

        # strategy a symbol object
        symbol = Symbol(symbol)

        # finally, strategy the OHLC object and return it
        ohlc = OHLC(symbol=symbol, dataframe=df)
        return ohlc

