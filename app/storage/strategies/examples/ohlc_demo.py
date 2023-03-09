from components import Strategy, on_step


class OHLCDemo(Strategy):

    @on_step
    def print_ohlc(self):
        timestamp = self.data.dataframe.index[self._loop_index]
        close = self.data.dataframe.iloc[self._loop_index]['close']
