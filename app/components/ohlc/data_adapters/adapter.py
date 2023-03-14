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
        self.objects.register(self)

        # register
        self.register()

    def get_data(self, *args, **kwargs) -> OHLC:
        raise NotImplementedError


class CSVAdapter(DataAdapter):
    """CSV Adapter, loads data from a csv file."""

    def get_data(self, path: str, symbol: str):
        """
        Loads data from a csv file.
        :param path: path to csv file
        :param symbol: symbol, as a string
        :return: OHLC object
        """
        from components.ohlc import OHLC
        return OHLC().from_csv(path, symbol)


