from components.ohlc import OHLC
from components.symbol import Symbol


class TestOHLC:

    def test_from_csv(self):
        ohlc = OHLC().from_csv('data/AAPL.csv', 'AAPL')
        assert isinstance(ohlc, OHLC)
        assert isinstance(ohlc.symbol, Symbol)
        assert ohlc.symbol.symbol == 'AAPL'
        assert ohlc.shape == (5001, 5)

    def test_attr_forwarding(self):
        ohlc = OHLC().from_csv('data/AAPL.csv', 'AAPL')
        assert ohlc.shape == (5001, 5)
        assert ohlc.head().shape == (5, 5)
        assert ohlc.tail().shape == (5, 5)
        assert ohlc.describe().shape == (8, 5)