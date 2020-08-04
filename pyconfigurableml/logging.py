import logging
from typeguard import typechecked
from typing import Dict



from pyconfigurableml._decorators import pass_decorator


@pass_decorator('logging')
@typechecked
def set_logger_levels(config: object, l_config: Dict[str, str], log: logging.Logger) -> object:
    '''
    Set per-logger minimum levels according to the configuration.

    Inspired by: https://github.com/Azure/azure-sdk-for-python/issues/9422
    '''

    for name, level in l_config.items():
        logger = logging.getLogger(name)
        # Inspired by: https://stackoverflow.com/a/35689599
        level = max(logger.getEffectiveLevel(), getattr(logging, level))
        log.info(f'Setting log level for {name} to {level}.')
        logger.setLevel(level)
    return config
