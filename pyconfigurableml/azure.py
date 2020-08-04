'''
TODO: docstring.
'''

import logging
from typing import Dict, Iterable, Tuple


_CREDENTIALS_ = None
_KEY_VAULT_CLIENT_DICT_ = None


def parse_azure_secret_identifier(secret_identifier: str) -> Tuple[str, str]:
    '''
    Returns (key vault name, secret name).
    '''
    parsed = urllib.parse.urlparse(secret_identifier)
    kv_name = parsed.netloc.split('.')[0]
    secret_name = [x for x in parsed.path.split('/') if x][-1]
    return (kv_name, secret_name)


def get_azure_secret(secret_identifier: str) -> str:
    '''
    Obtain SECRET...
    '''

    (kv_name, secret_name) = parse_azure_secret_identifier(secret_identifier)

    global _CREDENTIALS_, _KEY_VAULT_CLIENT_DICT_

    if _KEY_VAULT_CLIENT_DICT_ is None:
        _CREDENTIALS_ = DefaultAzureCredential()
        _KEY_VAULT_CLIENT_DICT_ = {}
    if kv_name in _KEY_VAULT_CLIENT_DICT_:
        client = _KEY_VAULT_CLIENT_DICT_[kv_name]
    else:
        vault_url = f'https://{kv_name}.vault.azure.net/'
        client = SecretClient(vault_url, _CREDENTIALS_)
        _KEY_VAULT_CLIENT_DICT_[kv_name] = client

    print(f'\n\n{secret_name}\n\n')

    return client.get_secret(secret_name).value


from pyconfigurableml._decorators import pass_decorator


def _recurse_resolve_azure_secrets(config: object) -> object:
    if isinstance(config, str):
        try:
            # TODO: handle this better...
            (kv_name, secret_name) = parse_azure_secret_identifier(secret_identifier)
            config = get_azure_secret(config)
        except:
            pass
    elif isinstance(config, Iterable):
        config = list(map(_recurse_resolve_azure_secrets, config))
    elif isinstance(config, Dict[str, object]):
        config = {k: _recurse_resolve_azure_secrets(v) for (k, v) in config.items()}
    
    return config


@pass_decorator('azure')
def resolve_azure_secrets(config: object, az, log: logging.Logger) -> object:

    if az['key_vault']['resolve_identifiers'] == True:
        tenant = az['tenant'] if 'tenant' in az else None
        creds = shared_cache_tenant_id(shared_cache_tenant_id = tenant)
        config = _recurse_resolve_azure_secrets(config)

    return config
