from components.orders.order import Order
from components.orders.enums import OrderSide as Side
from components.positions.exceptions import PositionClosedException


def add_closing_order_to_position(position, ohlc: 'OHLC'):
    """Adds a calculated closing order to the given position."""
    if position.closed:
        raise PositionClosedException('Position is already closed')

    # create the closing order
    order = Order(
        type='market',
        side=Side.inverse(position.get_side()),
        qty=position.get_size(),
        symbol=position.orders[0].symbol,
        filled_avg_price=ohlc.close,
        timestamp=ohlc.timestamp,
    )

    position.orders.append(order)


def show_details(position: 'Position'):
    """Prints the details of the given position."""
    print('Position:', position)
    for order in position.orders:
        print('\tOrder:', order)
