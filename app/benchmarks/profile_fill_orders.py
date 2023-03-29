from components.ohlc import CSVAdapter
from storage.strategies.examples.sma_cross_over_advanced import SMACrossOverAdvanced
from storage.strategies.examples.using_builtins import UsingBuiltins

adapter = CSVAdapter()
ohlc = adapter.get_data(path='../tests/data/AAPL.csv')

strategy = SMACrossOverAdvanced()
strategy.run(ohlc)
