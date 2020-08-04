from pyconfigurableml._decorators import pass_decorator
from typeguard import typechecked


@pass_decorator('munchify')
@typechecked
def munchify(config, inner_config: bool):
    '''
    Decide (using `inner_config`) whether to apply `munchify_transform` to
    `config`, and do so if necessary.
    '''
    if inner_config:
        config = munchify_transform(config)

    return config


def munchify_transform(config):
    '''
    Convert a nested dictionary into a JavaScript-style object (Munch).
    '''
    from munch import DefaultMunch
    return DefaultMunch.fromDict(config)
