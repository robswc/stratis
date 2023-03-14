from datetime import datetime

from components.orders.order import Order, OrderSide as Side, OrderType


class TestOrders:
    def test_hashing(self):
        ts = datetime.now().timestamp()
        fake_order_1 = Order(
            symbol='BTCUSDT',
            side=Side.BUY,
            type=OrderType.MARKET,
            qty=1,
            timestamp=ts,
        )
        fake_order_2 = Order(
            symbol='BTCUSDT',
            side=Side.BUY,
            type=OrderType.MARKET,
            qty=1,
            timestamp=ts,
        )
        assert fake_order_1 == fake_order_2

        fake_order_3 = Order(
            symbol='BTCUSDT',
            side=Side.BUY,
            type=OrderType.MARKET,
            qty=2,
            datetime=ts,
        )

        assert fake_order_1 != fake_order_3

        # test IDs
        assert fake_order_1.get_id() == fake_order_2.get_id()
        assert fake_order_1.get_id() != fake_order_3.get_id()
