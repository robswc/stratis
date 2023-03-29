from components.ohlc import CSVAdapter
from storage.strategies.examples.using_builtins import UsingBuiltins

adapter = CSVAdapter()
ohlc = adapter.get_data(path='../tests/data/AAPL.csv')

strategy = UsingBuiltins()
strategy.run(ohlc)

# 3/29/2023
# first run: 1700ms
# second run: 1400ms
# third run: 1000ms
# fourth run: 800ms
# fifth run: 700ms
# sixth run: sub 700ms
