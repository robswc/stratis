![stratis_logo](https://user-images.githubusercontent.com/38849824/197833824-384f5821-a4ef-4c68-ac82-91e0a51aaba3.png)

# Currently in beta, not intended for general users (yet) :)

# stratis
a python-based framework for creating and testing trading strategies

### Example Crossover Strategy
```python
class SMACrossOverStrategy(Strategy):
    data = OHLCV().from_csv('storage/data/ohlcv/AAPL.csv')
    sma_slow = []
    sma_fast = []

    @before
    def set_sma(self):
        close_data = self.data.close(as_list=True)
        self.sma_fast = ta.sma(close_data, 10, fill_none=0).round(2)
        self.sma_slow = ta.sma(close_data, 20, fill_none=0).round(2)
        
    @runner
    def run(self, parameters):
        idx = self.get_idx()
        if self.sma_fast[idx] > self.sma_slow[idx] and self.sma_fast[idx - 1] < self.sma_slow[idx - 1]:
            # create a buy order, everytime our fast sma crosses over our slow sma
            self.create_order(order_type='market', side='buy', quantity=1)

```

### Example w/Documentation
```python
class SMACrossOverStrategy(Strategy):
    # import our data, as a csv file
    data = OHLCV().from_csv('storage/data/ohlcv/AAPL.csv')
    
    # set our initial variables
    sma_slow = []
    sma_fast = []

    # use 'before' decorator, to set up constants for your strategy
    @before
    def set_sma(self):
        # get all close values from our data
        close_data = self.data.close(as_list=True)
        # create our sma's
        self.sma_fast = ta.sma(close_data, 10, fill_none=0).round(2)
        self.sma_slow = ta.sma(close_data, 20, fill_none=0).round(2)

    # use 'runner' decorator to define the method that will run on ever 'step' of the strategy.
    @runner
    def run(self, parameters):
        idx = self.get_idx()
        if self.sma_fast[idx] > self.sma_slow[idx] and self.sma_fast[idx - 1] < self.sma_slow[idx - 1]:
            # create a buy order, everytime our fast sma crosses over our slow sma
            self.create_order(order_type='market', side='buy', quantity=1)

    # after the strategy is run, do stuff :)
    @after
    def run_backtest(self):
        # get the results of the strategy, _only_ running the strategy produces orders, but does not test them
        self.backtest.run()

```
