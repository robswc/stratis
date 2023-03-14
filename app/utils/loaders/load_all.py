import inspect
from pathlib import Path
from importlib import import_module

from loguru import logger

from components.ohlc import DataAdapter
from components.strategy.strategy import BaseStrategy


def import_components(path, component_type):
    logger.debug(f'Importing {component_type.__name__}(s) from {path}...')
    components = []
    app_path = Path(__file__).parent.parent.parent
    paths = app_path.joinpath(path).rglob('*.py')
    for path in paths:
        module_name = path.as_posix().replace('/', '.').replace('.py', '').split('app.')[1]
        module = import_module(module_name)

        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and issubclass(obj, component_type):
                if obj.__name__ != component_type.__name__:
                    components.append(obj)
                    logger.info(f'\t->\t{obj.__name__} ({obj.__module__})')
    return components

# load all components
data_adapters = import_components('components/ohlc/data_adapters', DataAdapter)
strategies = import_components('storage/strategies', BaseStrategy)

# register all components
for adapter in data_adapters:
    adapter.register()

for strategy in strategies:
    strategy.register()