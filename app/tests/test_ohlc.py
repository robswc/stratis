from components.ohlc import OHLC
from components.ohlc.symbol import Symbol

PATH = 'tests/data/AAPL.csv'


class TestOHLC:

    def test_from_csv(self):
        ohlc = OHLC().from_csv(PATH, 'AAPL')
        assert isinstance(ohlc, OHLC)
        assert isinstance(ohlc.symbol, Symbol)
        assert ohlc.symbol.symbol == 'AAPL'
        assert ohlc.shape == (5001, 5)

    def test_attr_forwarding(self):
        ohlc = OHLC().from_csv(PATH, 'AAPL')
        assert ohlc.shape == (5001, 5)
        assert ohlc.head().shape == (5, 5)
        assert ohlc.tail().shape == (5, 5)
        assert ohlc.describe().shape == (8, 5)

    def test_ohlc_getters(self):
        ohlc = OHLC().from_csv(PATH, 'AAPL')
        assert ohlc.open == 253.91
        assert ohlc.high == 257.33
        assert ohlc.low == 252.32
        assert ohlc.close == 257.33
        ohlc.advance_index()
        assert ohlc.open == 257.17
        assert ohlc.high == 257.67
        assert ohlc.low == 256.48
        assert ohlc.close == 257.07

    def test_index(self):
        ohlc = OHLC().from_csv(PATH, 'AAPL')
        assert ohlc._index == 0
        ohlc.advance_index()
        assert ohlc._index == 1
        ohlc.advance_index(2)
        assert ohlc._index == 3
        ohlc.reset_index()
        assert ohlc._index == 0
