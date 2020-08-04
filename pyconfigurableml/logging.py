import logging
from pyconfigurableml._decorators import pass_decorator
from typeguard import typechecked
from typing import Dict, TypeVar, Union


T = TypeVar('T')


@pass_decorator(__name__)
@typechecked
def set_logger_levels(config: T, inner_config: Dict[str, str]) -> T:
    '''
    Set per-logger minimum levels according to the configuration (mapping
    logger name to string format for level name).

    Inspired by: https://github.com/Azure/azure-sdk-for-python/issues/9422
    '''

    for name, level in inner_config.items():
        logger = logging.getLogger(name)
        # Inspired by: https://stackoverflow.com/a/35689599
        level = max(logger.getEffectiveLevel(), getattr(logging, level))
        logger.setLevel(level)

    return config
