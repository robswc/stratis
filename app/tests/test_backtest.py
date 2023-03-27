from components.backtest.backtest import Backtest
from components.ohlc import CSVAdapter
from components.orders import Order, LimitOrder, StopOrder
from components.orders.enums import OrderSide
from components.positions import Position
from storage.strategies.examples.sma_cross_over import SMACrossOver

OHLC = CSVAdapter().get_data(path='tests/data/AAPL.csv', symbol='AAPL')
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
        entry_price, opened_timestamp = STRATEGY.data.close, (STRATEGY.data.timestamp + 300000)  # add 5 minutes
        # timestamp
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

    def test_bracket_position(self):
        STRATEGY.data.reset_index()
        STRATEGY.data.advance_index(100)
        STRATEGY.orders.orders = []
        root_order = STRATEGY.orders.market_order(side='buy', quantity=1)
        STRATEGY.orders.limit_order(side='sell', quantity=1, price=root_order.price + 2)
        STRATEGY.orders.stop_loss_order(side='sell', quantity=1, price=root_order.price - 10)

        # create position
        p = Position(orders=STRATEGY.orders.all())
        p.test(ohlc=OHLC)

        # check position
        assert p.size == 0
        assert p.pnl == 1.9999999999999716

    def test_stop_loss(self):
        strategy = SMACrossOver(data=OHLC)
        strategy.orders.orders = []
        strategy.data.reset_index()
        strategy.data.advance_index(100)

        # add orders
        root_order = strategy.orders.market_order(side='buy', quantity=1)
        strategy.orders.stop_loss_order(side='sell', quantity=1, price=root_order.price - 5)
        strategy.orders.limit_order(side='sell', quantity=1, price=root_order.price + 100)

        # create position
        p = Position(orders=strategy.orders.all())
        p.test(ohlc=OHLC)

        # check position
        assert p.size == 0
        assert p.pnl == -5

    def test_overview_long_orders(self):
        strategy = SMACrossOver(data=OHLC)
        strategy.orders.orders = []
        strategy.data.reset_index()
        strategy.data.advance_index(100)

        # create positions
        for i in range(3):
            strategy.data.advance_index(5)
            strategy.positions.open(order_type='market', side='buy', quantity=1)
            strategy.data.advance_index(5)
            strategy.positions.close()

        # create backtest
        backtest = Backtest(strategy=strategy, data=OHLC)
        backtest.test()

        # check overview
        assert backtest.result.pnl == -5.170000000000016

    def test_overview_short_orders(self):
        # now do the same with short orders
        strategy = SMACrossOver(data=OHLC)
        strategy.orders.orders = []
        strategy.data.reset_index()
        strategy.data.advance_index(100)

        # create positions
        for i in range(3):
            strategy.data.advance_index(5)
            strategy.positions.open(order_type='market', side='sell', quantity=1)
            strategy.data.advance_index(5)
            strategy.positions.close()

        # create backtest
        backtest = Backtest(strategy=strategy, data=OHLC)
        backtest.test()

        # check overview
        assert backtest.result.pnl == 5.170000000000016

    def test_complex_positions(self):
        b = Backtest(strategy=SMACrossOver(), data=OHLC)

        p1 = Position(
            orders=[
                Order(side='buy', symbol='AAPL', qty=1, order_type='market', filled_avg_price=100, timestamp=1),
                Order(side='sell', symbol='AAPL', qty=1, order_type='limit', filled_avg_price=150, timestamp=2),
            ]
        )

        p2 = Position(
            orders=[
                Order(side='sell', symbol='AAPL', qty=1, order_type='market', filled_avg_price=100, timestamp=10),
                Order(side='buy', symbol='AAPL', qty=1, order_type='stop', filled_avg_price=90, timestamp=20),
            ]
        )

        p3 = Position(
            orders=[
                Order(side='buy', symbol='AAPL', qty=1, order_type='market', filled_avg_price=100, timestamp=100),
                Order(side='sell', symbol='AAPL', qty=1, order_type='stop', filled_avg_price=110, timestamp=200),
            ]
        )

        b.strategy.positions.add(p1)
        b.strategy.positions.add(p2)
        b.strategy.positions.add(p3)
        b.test()

        assert b.result.pnl == 70

    def test_backtest_short_with_order_types(self):

        b = Backtest(strategy=SMACrossOver(), data=OHLC)

        side = OrderSide.SELL
        open_order = Order(
            type='market',
            side=side,
            qty=100,
            symbol='AAPL',
            filled_avg_price=257.33,
            timestamp=1653984000000,
            filled_timestamp=1653984000000,
        )
        take_profit = LimitOrder(
            side=OrderSide.inverse(side),
            qty=100,
            symbol='AAPL',
            limit_price=256,
        )
        stop_loss = StopOrder(
            side=OrderSide.inverse(side),
            qty=100,
            symbol='AAPL',
            stop_price=300
        )

        p = Position(orders=[open_order, take_profit, stop_loss])
        b.strategy.positions.add(p)
        b.test()
        tested_position = b.strategy.positions.all()[0]
        print(tested_position)

        assert tested_position.size == 0
        assert tested_position.closed_timestamp == 1653984600000

    def test_backtest_long_with_order_types(self):
        b = Backtest(strategy=SMACrossOver(), data=OHLC)
        side = OrderSide.BUY
        open_order = Order(
            type='market',
            side=side,
            qty=100,
            symbol='AAPL',
            filled_avg_price=257.33,
            timestamp=1653984000000,
            filled_timestamp=1653984000000,
        )
        take_profit = LimitOrder(
            side=OrderSide.inverse(side),
            qty=100,
            symbol='AAPL',
            limit_price=260,
        )
        stop_loss = StopOrder(
            side=OrderSide.inverse(side),
            qty=100,
            symbol='AAPL',
            stop_price=100
        )

        p = Position(orders=[open_order, take_profit, stop_loss])
        b.strategy.positions.add(p)
        b.test()
        tested_position = b.strategy.positions.all()[0]
        assert tested_position.size == 0
        assert tested_position.closed_timestamp == 1654183500000
