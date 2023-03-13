<img width="667" alt="stratis-full-logo" src="https://user-images.githubusercontent.com/38849824/224750446-a7255083-75eb-474b-b550-198ad21c0da8.png">

# Stratis

Stratis is a python-based framework for developing and testing strategies, inspired by the simplicity 
of tradingview's [Pinescript](https://www.tradingview.com/pine-script-docs/en/v5/Introduction.html).  Currently,
stratis is in the early stages of development, and is not yet ready for production use.  However, it is encouraged
to try it out and provide feedback via [GitHub issues](https://github.com/robswc/stratis/issues/new).

Stratis is a part of [Shenandoah Research's](https://shenandoah.capital/) Open source Trading Software Initiative.

<img width="256" alt="stratis-full-logo" src="https://user-images.githubusercontent.com/38849824/224753683-4cb3decb-4232-42e4-8bce-fca2f7f23998.png">

## Basic Example

The following code demonstrates how to create a strategy that prints the timestamp and close price of the 
OHLC data every hour.  The `on_step` decorator is used to run the function on every step of the OHLC data.  You can find
more info about how to create strategies [here](https://github.com/robswc/stratis/wiki/Strategies).

Using the `Strategy`
class, along with the `on_step` decorator, you can create strategies that are as simple or as complex as you want, with
the full power of python at your disposal.

```python
class OHLCDemo(Strategy):

    @on_step  # the on_step decorator runs the function on every "step" of the OHLC data
    def print_ohlc(self):

        # strategy shorthands for the OHLC data
        timestamp = self.data.timestamp
        close = self.data.close

        # if the timestamp is a multiple of 3600000 (1 hour), print the timestamp and close price
        if timestamp % 3600000 == 0:
            print(f'{timestamp}: {close}')
                
```
```python
data = CSVAdapter('data/AAPL.csv')
strategy = OHLCDemo().run(data)
```


## Table of Contents

- [Installation](#Installation)
- [Features](#features)

## Installation

It is heavily recommended to use Docker to run stratis.  This is because stratis requires a number of dependencies that
can be difficult to install.  To install Docker, follow the instructions [here](https://docs.docker.com/get-docker/).

Once Docker is installed, you can run stratis by running the following command:

```bash
# Clone the repository
git clone https://github.com/robswc/stratis

# Change directory to the repository
cd stratis

# Run the docker-compose file
docker-compose up -d # -d runs the container in the background
```