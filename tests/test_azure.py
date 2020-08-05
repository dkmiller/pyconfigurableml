from pyconfigurableml.azure import parse_azure_secret_identifier, resolve_azure_secrets
import pytest
import sys
from unittest.mock import patch, MagicMock


@pytest.mark.parametrize('secret_identifier, expected', [
    ('https://foo.vault.azure.net/secrets/bar', (True, 'foo', 'bar', None)),
    ('https://foo.vault.azure.net/secrets/bar/', (True, 'foo', 'bar', None)),
    ('https://foo.vault.azure.net/secrets/bar/id', (True, 'foo', 'bar', 'id')),
    ('https://foo.vault.azure.net/secrets/bar/id/', (True, 'foo', 'bar', 'id')),
    ('http://foo.vault.azure.net/secrets/bar/id/', (False, None, None, None)),
    ('https://foo/secrets/bar/id/', (False, None, None, None)),
    ('boz', (False, None, None, None))
])
def test_parse_azure_secret_identifier(secret_identifier, expected):
    result = parse_azure_secret_identifier(secret_identifier)
    assert expected == result


@pytest.mark.parametrize('config, value, expected', [
    ({'a': 1}, None, {'a': 1}),
    (
        {'a': 'https://foo.vault.azure.net/secrets/bar'},
        'baz',
        {'a': 'baz'}
    )
])
def test_resolve_azure_secrets(config, value, expected):
    config['pyconfigurableml'] = {'azure': {'resolve_secret_identifiers': True}}
    expected['pyconfigurableml'] = {'azure': {'resolve_secret_identifiers': True}}

    ret = MagicMock()
    ret.value = value
    secret_client = MagicMock()
    secret_client.get_secret = MagicMock(return_value=ret)
    with patch('azure.keyvault.secrets.SecretClient', return_value=secret_client):
        result = resolve_azure_secrets(config)
    assert expected == result


@pytest.mark.parametrize('config, works', [
    ({'a': 1}, True),
    ({'pyconfigurableml': {'azure': {'resolve_secret_identifiers': False}}}, True),
    (
        {
            'pyconfigurableml': {'azure': {'resolve_secret_identifiers': True}},
            'foo': 'https://foo.vault.azure.net/secrets/bar'
        },
        False
    )
])
def test_resolve_azure_secrets_works_with_disabled_imports(config, works):
    # https://stackoverflow.com/a/1350574
    for namespace in ['azure.identity', 'azure.keyvault.secrets']:
        del sys.modules[namespace]
        sys.modules[namespace] = None

    if works:
        resolve_azure_secrets(config)
    else:
        with pytest.raises(ImportError):
            resolve_azure_secrets(config)
