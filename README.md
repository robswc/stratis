<p align="center">
<img width="480" alt="stratis-full-logo" src="https://user-images.githubusercontent.com/38849824/224750446-a7255083-75eb-474b-b550-198ad21c0da8.png">
<img width="720" alt="stratis-full-logo" src="https://user-images.githubusercontent.com/38849824/227098394-4160f118-a8a9-45d6-a4db-33872aa25043.png">
</p>


# Stratis

[![License](https://img.shields.io/github/license/robswc/stratis?style=for-the-badge)](https://github.com/robswc/stratis/blob/master/LICENSE)
[![Build](https://img.shields.io/github/actions/workflow/status/robswc/stratis/pytest.yml?style=for-the-badge)]()
[![GitHub repo size](https://img.shields.io/github/repo-size/robswc/stratis?style=for-the-badge)](https://github.com/robswc/stratis)
[![Stars](https://img.shields.io/github/stars/robswc/stratis?style=for-the-badge)](https://github.com/robswc/stratis/stargazers)
[![Twitter Follow](https://img.shields.io/twitter/follow/robswc?label=Twitter!&style=for-the-badge)](https://twitter.com/robswc)




Stratis is a python-based framework for developing and testing strategies, inspired by the simplicity 
of tradingview's [Pinescript](https://www.tradingview.com/pine-script-docs/en/v5/Introduction.html).  Currently,
stratis is in the early stages of development, and is not yet ready for production use.  However, it is encouraged
to try it out and provide feedback via [GitHub issues](https://github.com/robswc/stratis/issues/new).

Stratis is a part of [Shenandoah Research's](https://shenandoah.capital/) Open source Trading Software Initiative and developed by Polyad Decision Sciences software engineers!

<span>
<img width="64" alt="sr-logo" src="https://shenandoah.capital/static/media/box_logo_light_v1.7e7ad0f21c75ea8620f0.png">
<a href="https://polyad.ai/"><img width="256" alt="poly-ad-logo" src="https://user-images.githubusercontent.com/38849824/226416451-1e511803-6e0e-4559-9247-c1c4f8bec720.png"></a>
</span>

#### _Please Note Stratis is under active development and is not yet ready for production use._


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
can be difficult to install.  

To install Docker, follow the instructions [here](https://docs.docker.com/get-docker/).

Once Docker is installed, you can run stratis by running the following commands:

```bash
# Clone the repository
git clone https://github.com/robswc/stratis

# Change directory to the repository
cd stratis

# Run the docker-compose file
docker-compose up -d # -d runs the containers in the background
```

For more advanced usage, you can run app with python directly, as it is a FastAPI app under the hood.
I would recommend using a [virtual environment](https://docs.python.org/3/library/venv.html) for this.
You will also have to [install the requirements](https://pip.pypa.io/en/latest/user_guide/#requirements-files).

```bash
cd app  # change directory to the app folder
python python -m uvicorn main:app --reload  # reloads the app on file changes (useful for development)
```
