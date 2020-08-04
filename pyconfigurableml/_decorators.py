import functools


def pass_decorator(namespace: str):
    '''
    TODO: docstring.
    '''

    def decorator(func):
        @functools.wraps(func)
        def inner_func(config):
            inner_config = config

            try:
                for name in namespace.split('.'):
                    inner_config = inner_config[name]
            except KeyError:
                return config

            return func(config, inner_config)

        return inner_func

    return decorator
