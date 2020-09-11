import argparse
import logging
import os
from unittest import mock
from pyconfigurableml.entry import run, run_no_parse_args
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
    with mock.patch(
            'argparse.ArgumentParser.parse_args',
            return_value=argparse.Namespace(config=config_path, level='info')
            ):
        # https://stackoverflow.com/a/31756485
        with mock.patch(f'logging.Logger.{level}') as mock_logger:
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
    with mock.patch('argparse.ArgumentParser.parse_args', return_value=None):
        run(main, file, '__not_main__')


def test_munchify_works():
    def main(cfg, _):
        print(cfg.attr)

    dir_path = os.path.dirname(os.path.realpath(__file__))
    config_path = os.path.join(dir_path, 'config2.yml')

    # https://stackoverflow.com/a/37343818
    with mock.patch(
            'argparse.ArgumentParser.parse_args',
            return_value=argparse.Namespace(config=config_path, level='info')
            ):
        run(main, __file__)


def test_munchify_not_called():
    def main(cfg, _):
        print(cfg.attr)

    dir_path = os.path.dirname(os.path.realpath(__file__))
    config_path = os.path.join(dir_path, 'config1.yml')

    # https://stackoverflow.com/a/37343818
    with pytest.raises(AttributeError):
        with mock.patch(
            'argparse.ArgumentParser.parse_args',
            return_value=argparse.Namespace(config=config_path, level='info')
        ):
            run(main, __file__)


@pytest.mark.parametrize('file, levels', [
    ('config2.yml', {'foo': 0}),
    ('config3.yml', {'azure.core.pipeline.policies.http_logging_policy': 30})
])
def test_test_set_logger_levels_from_config_file(file, levels):
    def main(cfg, _):
        pass

    dir_path = os.path.dirname(os.path.realpath(__file__))
    config_path = os.path.join(dir_path, file)

    # https://stackoverflow.com/a/37343818
    with mock.patch(
            'argparse.ArgumentParser.parse_args',
            return_value=argparse.Namespace(config=config_path, level='info')
            ):
        run(main, __file__)

    for k, v in levels.items():
        assert v == logging.getLogger(k).level


@pytest.mark.parametrize('file,level,err,', [
    ('config1.yml', 'INFO', ArithmeticError)
])
def test_run_no_parse_args__doesnt_use_command_line_args(file, level, err):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    config_path = os.path.join(dir_path, file)

    m = mock.Mock()
    m.side_effect = err

    def main(cfg, _):
        print(cfg)

    with mock.patch('sys.argv', m):
        run_no_parse_args(main, __file__, level, config_path)
