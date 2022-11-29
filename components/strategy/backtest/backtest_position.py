import datetime

from components.strategy.position import BasicPosition

from loguru import logger


class BacktestPosition:
    def __init__(self):
        self.entry_price = None
        self.take_profit = None
        self.take_loss = None
        self.side = None
        self.quantity = None
        self.timestamp = None
        self.data_index = None
        self.filled_timestamp = None
        self.pnl = 0

    def from_position(self, position: BasicPosition) -> 'BacktestPosition':
        """Creates a backtest position from a position object"""
        self.entry_price = position.price
        self.take_profit = position.take_profit
        self.take_loss = position.take_loss
        self.side = position.side
        self.quantity = position.quantity
        self.timestamp = position.timestamp
        self.data_index = position.data_index
        return self

    def get_timestamp(self, fmt='%Y-%m-%d %H:%M:%S'):
        return datetime.datetime.fromtimestamp(self.timestamp / 1000).strftime(fmt)

    def get_filled_timestamp(self, fmt='%Y-%m-%d %H:%M:%S'):
        return datetime.datetime.fromtimestamp(self.filled_timestamp / 1000).strftime(fmt)

    def test(self, ohlc):
        in_bounds = True
        idx = self.data_index + 1

        upper_bound = max(self.take_loss, self.take_profit)
        lower_bound = min(self.take_loss, self.take_profit)

        while in_bounds:
            candle = ohlc[idx]
            in_bounds = candle['high'] <= upper_bound and candle['low'] >= lower_bound

            # if we reach the end of the data, we are out of bounds
            if idx >= len(ohlc):
                logger.warning(f'Position {self} reached end of data')
                break

            idx += 1

        self.filled_timestamp = ohlc[idx]['datetime']

        if self.side == 'buy':
            exit_price = ohlc[idx]['low'] if self.take_loss < self.take_profit else ohlc[idx]['high']
            self.pnl = (exit_price - self.entry_price) * self.quantity
        else:
            exit_price = ohlc[idx]['high'] if self.take_loss < self.take_profit else ohlc[idx]['low']
            self.pnl = (self.entry_price - exit_price) * self.quantity
