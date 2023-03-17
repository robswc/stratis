from components.backtest.backtest import Backtest
from components.ohlc import CSVAdapter
from storage.strategies.examples.sma_cross_over import SMACrossOver

OHLC = CSVAdapter().get_data('tests/data/AAPL.csv', 'AAPL')
STRATEGY = SMACrossOver(data=OHLC)

class TestBacktest:
    def test_backtest_orders(self):

        # add orders
        STRATEGY.orders.market_order(side='buy', quantity=1)

        backtest = Backtest(strategy=STRATEGY, data=OHLC)
        backtest.test()

        assert backtest.result is not None

    def test_backtest_positions(self):

        QTY = 1

        # add positions
        STRATEGY.positions.open(order_type='market', side='buy', quantity=QTY)
        entry_price, opened_timestamp = STRATEGY.data.close, STRATEGY.data.timestamp
        STRATEGY.data.advance_index(100)
        STRATEGY.positions.close()
        exit_price, closed_timestamp = STRATEGY.data.close, STRATEGY.data.timestamp

        # create and run backtest
        backtest = Backtest(strategy=STRATEGY, data=OHLC)
        backtest.test()

        # grab the newly tested position
        p = STRATEGY.positions.all()[0]

        # calculate expected profit
        expected_profit = (exit_price - entry_price) * QTY

        # check position
        assert p.size == 0
        assert p.pnl == expected_profit
        assert p.unrealized_pnl is None
        assert p.average_entry_price == entry_price
        assert p.average_exit_price == exit_price
        assert p.opened_timestamp == opened_timestamp
        assert p.closed_timestamp == closed_timestamp


        assert backtest.result is not None
