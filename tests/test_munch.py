from pyconfigurableml.munch import munchify, munchify_transform
import pytest
import sys
from unittest.mock import patch


@pytest.mark.parametrize('config, inner_config', [
    ({'a': 1}, True),
    ({'a': 1}, False)
])
def test_munchify_called_correctly(config, inner_config):
    if inner_config:
        config['pyconfigurableml'] = {'munch': True}

    with patch('pyconfigurableml.munch.munchify_transform') as mock_transform:
        munchify(config)
        if inner_config:
            mock_transform.assert_called_with(config)
        else:
            mock_transform.assert_not_called()


@pytest.mark.parametrize('input, func, result', [
    ({'a': 1}, lambda x: x.a, 1),
    ({'a': 1}, lambda x: x.b, None)
])
def test_munchify_transform(input, func, result):
    transformed = munchify_transform(input)
    assert result == func(transformed)


@pytest.mark.parametrize('config, namespace, works', [
    ({'a': 1}, 'munch', True),
    ({'pyconfigurableml': {'munch': False}}, 'munch', True),
    ({'pyconfigurableml': {'munch': True}}, 'munch', False)
])
def test_munchify_works_with_disabled_imports(config, namespace, works):
    # https://stackoverflow.com/a/1350574
    del sys.modules[namespace]
    sys.modules[namespace] = None

    if works:
        munchify(config)
    else:
        with pytest.raises(ImportError):
            munchify(config)
