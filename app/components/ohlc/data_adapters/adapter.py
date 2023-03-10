from components.ohlc import OHLC

ADAPTER_MAP = {}

class DataAdapter:
    """Base class for data adapters."""
    def __new__(cls, *args, **kwargs):
        if cls not in ADAPTER_MAP:
            ADAPTER_MAP[cls] = super().__new__(cls)
        return ADAPTER_MAP[cls]

    def __init__(self):
        self.name = self.__class__.__name__

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


