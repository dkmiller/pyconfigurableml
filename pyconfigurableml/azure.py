'''
TODO: docstring.
'''

import logging
from pyconfigurableml._decorators import pass_decorator
import re
from typing import Dict, Iterable, Tuple, Union
from typeguard import typechecked
import urllib.parse


_CREDENTIALS_ = None
_KEY_VAULT_CLIENT_DICT_ = None


@typechecked
def parse_azure_secret_identifier(secret_identifier: str) -> Tuple[bool, Union[None, str], Union[None, str], Union[None, str]]:
    '''
    TODO: docstring.
    '''
    parsed = urllib.parse.urlparse(secret_identifier)

    m1 = re.match(r'([\w\-]+)\.vault\.azure\.net', parsed.netloc)
    if parsed.scheme == 'https' and not parsed.params and not parsed.query and not parsed.fragment and m1:
        kv_name = m1.groups()[0]
        path = [x for x in parsed.path.split('/') if x]
        secret_name = path[1]
        secret_version = path[2] if len(path) == 3 else None
        return (True, kv_name, secret_name, secret_version)
    else:
        return (False, None, None, None)


@typechecked
def get_azure_secret(kv_name: str, secret_name: str, sec_version: Union[None, str]) -> str:
    '''
    TODO: docstring.
    '''

    global _CREDENTIALS_, _KEY_VAULT_CLIENT_DICT_

    if _KEY_VAULT_CLIENT_DICT_ is None:
        _KEY_VAULT_CLIENT_DICT_ = {}
    if kv_name in _KEY_VAULT_CLIENT_DICT_:
        client = _KEY_VAULT_CLIENT_DICT_[kv_name]
    else:
        from azure.keyvault.secrets import SecretClient
        vault_url = f'https://{kv_name}.vault.azure.net/'
        client = SecretClient(vault_url, _CREDENTIALS_)
        _KEY_VAULT_CLIENT_DICT_[kv_name] = client

    return client.get_secret(secret_name, version=sec_version).value


def _recurse_resolve_azure_secrets(config):
    if isinstance(config, str):
        (success, kv_name, secret_name, ver) = parse_azure_secret_identifier(config)
        if success:
            config = get_azure_secret(kv_name, secret_name, ver)
    elif isinstance(config, dict):
        config = {k: _recurse_resolve_azure_secrets(v) for (k, v) in config.items()}
    elif isinstance(config, Iterable):
        config = list(map(_recurse_resolve_azure_secrets, config))
    
    return config


@pass_decorator('azure')
@typechecked
def resolve_azure_secrets(config, inner_config: Dict[str, object]):

    if inner_config['key_vault']['resolve_identifiers'] == True:
        from azure.identity import DefaultAzureCredential
        global _CREDENTIALS_

        tenant = inner_config['tenant'] if 'tenant' in inner_config else None
        _CREDENTIALS_ = DefaultAzureCredential(shared_cache_tenant_id = tenant)
        config = _recurse_resolve_azure_secrets(config)

    return config
