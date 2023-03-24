from loguru import logger


class ComponentManager:

    _components = []

    @classmethod
    def register(cls, component):
        if component in cls._components:
            return
        cls._components.append(component)
        logger.debug(f'Registered component {component} ({component.__module__})')

    @classmethod
    def all(cls):
        return [o() for o in cls._components]

    @classmethod
    def get(cls, name):
        for component in cls._components:
            if component.__name__ == name:
                return component()
        raise ValueError(f'Component "{name}" not found.')