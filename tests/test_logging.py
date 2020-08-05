import logging
import pytest
from pyconfigurableml.logging import set_logger_levels


@pytest.mark.parametrize('original_levels, configured_levels, new_levels', [
    ({'a': 'INFO'}, {'a': 'WARN'}, {'a': 30}),
    ({'a': 'ERROR'}, {'a': 'INFO'}, {'a': 40}),
    ({'a': 'INFO'}, {'b': 'ERROR'}, {'a': 20, 'b': 40})
])
def test_set_logger_levels(original_levels, configured_levels, new_levels):
    for k, v in original_levels.items():
        logger = logging.getLogger(k)
        logger.setLevel(v)

    configured_levels = {'pyconfigurableml': {'logging': configured_levels}}

    result = set_logger_levels(configured_levels)
    assert result == configured_levels

    for k, v in new_levels.items():
        logger = logging.getLogger(k)
        assert v == logger.level
