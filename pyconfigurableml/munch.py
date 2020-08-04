from pyconfigurableml._decorators import pass_decorator
from typeguard import typechecked


@pass_decorator('munchify')
@typechecked
def munchify(config, inner_config: bool):
    '''
    TODO: docstring.
    '''
    if inner_config:
        from munch import DefaultMunch
        config = DefaultMunch.fromDict(config)

    return config
