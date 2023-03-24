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

    def get_data(self, *args, **kwargs) -> OHLC:
        raise NotImplementedError


class CSVAdapter(DataAdapter):
    """CSV Adapter, loads data from a csv file."""

    def get_data(self, path: str, symbol: str = None):
        """
        Loads data from a csv file.
        :param path: path to csv file
        :param symbol: symbol, as a string
        :return: OHLC object
        """
        from components.ohlc import OHLC

        if symbol is None:
            logger.warning('No symbol provided, using filename as symbol.')
            symbol = path.split('/')[-1].split('.')[0]

        return OHLC.from_csv(path, symbol)


