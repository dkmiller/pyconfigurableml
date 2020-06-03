import argparse
import os
from unittest.mock import patch
from pyconfigurableml.entry import run
import pytest


@pytest.mark.parametrize('input', [
    1,
    'foo',
    lambda x: x
])
def test_run_type_checking(input) -> None:
    with pytest.raises(TypeError):
        run(input)


@pytest.mark.parametrize('config_name,level,called,main', [
    ('config1.yml', 'info', 'hi', lambda _, l: l.info('hi')),
    ('config1.yml', 'warning', 'bar', lambda c, l: l.warning(c['foo']))
])
def test_run_config(config_name, level, called, main):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    config_path = os.path.join(dir_path, config_name)

    # https://stackoverflow.com/a/37343818
    with patch(
            'argparse.ArgumentParser.parse_args',
            return_value=argparse.Namespace(config=config_path, level='info')
            ):
        # https://stackoverflow.com/a/31756485
        with patch(f'logging.Logger.{level}') as mock_logger:
            run(main)
            mock_logger.assert_called_with(called)
