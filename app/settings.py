from components.ohlc import CSVAdapter
from components.ohlc.data_adapters.api_adapter import APIDataAdapter

# add any custom data adapters here
DATA_ADAPTERS = [
    CSVAdapter,
    APIDataAdapter
]