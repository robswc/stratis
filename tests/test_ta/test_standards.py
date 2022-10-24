from components.data.ohlcv import OHLCV
from components.strategy.strategy import Strategy, runner, after, before
from components.strategy.builtins.standard import TechnicalAnalysis as ta

data = OHLCV().from_csv('fixtures/ohlc_valid.csv')


def test_sma():
    sma = ta.sma(data.close(as_list=True), 10)
    assert sma[0] is None
    assert int(round(sma[-1])) == int(234)
