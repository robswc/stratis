import datetime
from components import Strategy, on_step


class OHLCDemo(Strategy):

    @on_step
    def print_ohlc(self):

        # create shorthands for the OHLC data
        timestamp = self.data.timestamp
        close = self.data.close

        # if the timestamp is a multiple of 3600000 (1 hour)
        if timestamp % 3600000 == 0:
            # create a datetime object from the timestamp
            dt = datetime.datetime.fromtimestamp(timestamp / 1000)
            if dt.hour == 10:
                print(f'{dt}: {close}')


