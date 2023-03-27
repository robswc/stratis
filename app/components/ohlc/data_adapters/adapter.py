from datetime import datetime

import pandas as pd
from loguru import logger

from components.manager.manager import ComponentManager
from components.ohlc import OHLC


class DataAdapterManager(ComponentManager):
    _components = []


class DataAdapter:
    """Base class for data adapters."""

    objects = DataAdapterManager

    @classmethod
    def register(cls):
        cls.objects.register(cls)

    def __init__(self):
        self.name = self.__class__.__name__

        # register
        self.register()

    def get_data(self, start: datetime = None, end: datetime = None, *args, **kwargs) -> OHLC:
        raise NotImplementedError


class CSVAdapter(DataAdapter):
    """CSV Adapter, loads data from a csv file."""

    def get_data(
            self,
            start: datetime = None,
            end: datetime = None,
            path: str = None,
            symbol: str = None,
    ):
        """
        Loads data from a csv file.
        :param path: path to csv file
        :param symbol: symbol, as a string
        :param start: start timestamp
        :param end: end timestamp
        :return: OHLC object
        """
        from components.ohlc import OHLC

        if symbol is None:
            logger.warning('No symbol provided, using filename as symbol.')
            symbol = path.split('/')[-1].split('.')[0]

        ohlc = OHLC.from_csv(path, symbol)

        if start is not None or end is not None:

            # ensure start and end are timestamps
            if start is None:
                start = ohlc.index[0]
            if end is None:
                end = ohlc.index[-1]

            ohlc.trim(start, end)

        return ohlc
