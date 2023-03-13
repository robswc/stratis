from components.ohlc import OHLC
from components.strategy import Strategy

CSV_PATH = 'tests/data/AAPL.csv'


class TestStrategy:
    def test_strategy_name(self):
        assert Strategy().name == 'BaseStrategy'

    def test_initializing_examples(self):
        from storage.strategies.examples.sma_cross_over import SMACrossOver
        strategy = SMACrossOver()
        assert strategy.name == 'SMACrossOver'
        assert int(strategy.sma_fast) == 10
        assert int(strategy.sma_slow) == 20

    def test_run_strategy(self):
        from storage.strategies.examples.sma_cross_over import SMACrossOver
        ohlc = OHLC().from_csv(CSV_PATH, 'AAPL')
        strategy = SMACrossOver(data=ohlc)
        strategy.run(
            data=ohlc,
        )

    def test_ohlc_demo(self):
        from storage.strategies.examples.ohlc_demo import OHLCDemo
        strategy = OHLCDemo()
        ohlc = OHLC().from_csv(CSV_PATH, 'AAPL')
        strategy.run(
            data=ohlc,
        )

    def test_load_strategies(self):
        from utils.strategy_loader import import_all_strategies
        strategies = import_all_strategies()
        assert len(strategies) > 0

    def test_strategy_manager(self):
        from utils import strategy_loader
        assert len(Strategy.objects.all()) > 0
        for s in Strategy.objects.all():
            print(s)
        assert Strategy.objects.get('SMACrossOver').name == 'SMACrossOver'