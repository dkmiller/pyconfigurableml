import argparse
import os
from unittest.mock import patch
from pyconfigurableml.entry import run
import pytest
import uuid


@pytest.mark.parametrize('input', [
    1,
    'foo',
    lambda x: x
])
def test_run_type_checking(input) -> None:
    with pytest.raises(TypeError):
        run(input, __file__)


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
            run(main, __file__)
            mock_logger.assert_called_with(called)


def test_if_name_not_main_then_not_called():
    '''
    Call `run` on a method which throws an exception, after patching
    `parse_args` to return None. This verifies no argument parsing is done, and
    that `main` is not called.
    '''
    def main(cfg, log):
        raise Exception('I should not be called')
    # https://stackoverflow.com/a/534847
    file = str(uuid.uuid4())
    with patch('argparse.ArgumentParser.parse_args', return_value=None):
        run(main, file, '__not_main__')


def test_munchify_works():
    def main(cfg, l):
        print(cfg.attr)

    dir_path = os.path.dirname(os.path.realpath(__file__))
    config_path = os.path.join(dir_path, 'config2.yml')

    # https://stackoverflow.com/a/37343818
    with patch(
            'argparse.ArgumentParser.parse_args',
            return_value=argparse.Namespace(config=config_path, level='info')
            ):
        run(main, __file__)


def test_munchify_not_called():
    def main(cfg, l):
        print(cfg.attr)

    dir_path = os.path.dirname(os.path.realpath(__file__))
    config_path = os.path.join(dir_path, 'config1.yml')

    # https://stackoverflow.com/a/37343818
    with pytest.raises(AttributeError):
        with patch(
            'argparse.ArgumentParser.parse_args',
            return_value=argparse.Namespace(config=config_path, level='info')
            ):
            run(main, __file__)
