import argparse
import logging
import os
from unittest.mock import patch
from pyconfigurableml.entry import run
import pytest
from pyconfigurableml.logging import set_logger_levels


@pytest.mark.parametrize('original_levels, configured_levels, new_levels', [
    ({'a': 'INFO'}, {'a': 'WARN'}, {'a': 30}),
    ({'a': 'ERROR'}, {'a': 'INFO'}, {'a': 40}),
    ({'a': 'INFO'}, {'b': 'ERROR'}, {'a': 20, 'b': 40})
])
def test_set_logger_levels(original_levels, configured_levels, new_levels):
    for k, v in original_levels.items():
        l = logging.getLogger(k)
        l.setLevel(v)

    configured_levels = {'pyconfigurableml': {'logging': configured_levels}}

    result = set_logger_levels(configured_levels)
    assert result == configured_levels
    
    for k, v in new_levels.items():
        l = logging.getLogger(k)
        assert v == l.level


@pytest.mark.parametrize('file, levels', [
    ('config2.yml', {'foo': 0}),
    ('config3.yml', {'azure.core.pipeline.policies.http_logging_policy': 30})
])
def test_test_set_logger_levels_from_config_file(file, levels):
    def main(cfg, l):
        pass

    dir_path = os.path.dirname(os.path.realpath(__file__))
    config_path = os.path.join(dir_path, file)

    # https://stackoverflow.com/a/37343818
    with patch(
            'argparse.ArgumentParser.parse_args',
            return_value=argparse.Namespace(config=config_path, level='info')
            ):
        run(main, __file__)

    for k, v in levels.items():
        assert v == logging.getLogger(k).level
