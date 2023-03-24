from components.orders.order import Order, StopOrder, LimitOrder
from components.positions.position import Position
from components.orders.signals import Signal, BracketSignal

ROOT_ORDER = Order(
    type='market',
    side='buy',
    qty=100,
    symbol='AAPL',
    filled_avg_price=100,
    timestamp=1000
)


class TestSignals:
    def test_basic_signal(self):
        p = Position(
            orders=[ROOT_ORDER],
        )

        p.test()

        s = Signal().from_position(p)

        assert s.order_type == 'market'
        assert s.side == 'buy'
        assert s.quantity == 100
        assert s.price == 100

    def test_bracket_signal(self):
        stop_order = StopOrder(
            type='stop',
            side='sell',
            qty=100,
            symbol='AAPL',
            stop_price=90,
        )
        limit_order = LimitOrder(
            type='limit',
            side='sell',
            qty=100,
            symbol='AAPL',
            limit_price=110,
        )

        p = Position(
            orders=[ROOT_ORDER, stop_order, limit_order],
        )

        s = BracketSignal().from_position(p)

        assert s.order_type == 'market'
        assert s.side == 'buy'
        assert s.price == 100
        assert s.stop_loss == 90
        assert s.take_profit == 110

        # check that serializing to JSON works as expected
        assert s.json() == ('{"id": "3b8cf71b56751e9e58f69ee2650cf483", "order_type": "market", "side": '
                            '"buy", "quantity": 100, "price": 100.0, "timestamp": 1000, "stop_loss": '
                            '90.0, "take_profit": 110.0}')
