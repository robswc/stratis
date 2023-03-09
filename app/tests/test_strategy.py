from components.ohlc import OHLC
from components.strategy import Strategy


class TestStrategy:
    def test_strategy_name(self):
        assert Strategy().name == 'Strategy'

    def test_initializing_examples(self):
        from storage.strategies.examples.sma_cross_over import SMACrossOver
        strategy = SMACrossOver()
        assert strategy.name == 'SMACrossOver'
        assert int(strategy.sma_fast) == 10
        assert int(strategy.sma_slow) == 20

    def test_run_strategy(self):
        from storage.strategies.examples.sma_cross_over import SMACrossOver
        strategy = SMACrossOver()
        ohlc = OHLC().from_csv('data/AAPL.csv', 'AAPL')
        strategy.run(
            data=ohlc,
        )

    def test_ohlc_demo(self):
        from storage.strategies.examples.ohlc_demo import OHLCDemo
        strategy = OHLCDemo()
        ohlc = OHLC().from_csv('data/AAPL.csv', 'AAPL')
        strategy.run(
            data=ohlc,
        )