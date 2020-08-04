'''
Utilities around programatic entry point.
'''


import argparse
import logging
import os
from typing import Callable
from typeguard import typechecked
import yaml


from pyconfigurableml.azure import resolve_azure_secrets
from pyconfigurableml.logging import set_logger_levels


from pyconfigurableml._decorators import pass_decorator


@pass_decorator('munchify')
@typechecked
def munchify(config: object, m_config, log: logging.Logger) -> object:
    if m_config == True:
        from munch import DefaultMunch
        config = DefaultMunch.fromDict(config)

    return config


config_actions = [
    set_logger_levels,
    resolve_azure_secrets,
    munchify
]


@typechecked
def run(main: Callable[[object, logging.Logger], None],
        file: str,
        name: str = '__main__') -> None:
    '''
    Handle log levels and parsing a YAML configuration file. The default
    path to the configuration file is `<caller directory>/config.yml`.

        Parameters:
            main: programatic entry point for your program.
            file: should be __file__ in the entry point of your script.
            name: optionally __name__ in your script. This function will only
                  call main if __name__ == '__main__'.
    '''

    if name == '__main__':
        caller_dir = os.path.dirname(os.path.abspath(file))

        parser = argparse.ArgumentParser()

        parser.add_argument('--config', default=os.path.join(caller_dir, 'config.yml'))
        parser.add_argument('--level', default='INFO')
        args = parser.parse_args()

        with open(args.config, 'r') as config_file:
            config = yaml.safe_load(config_file)

        logging.basicConfig(level=args.level)
        logger = logging.getLogger()

        for f in config_actions:
            config = f(config, logger)

        main(config, logger)
