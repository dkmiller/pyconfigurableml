import functools


def pass_decorator(param: str):

    def decorator(func):
        @functools.wraps(func)
        def inner_func(config, log):
            try:
                inner_config = config['pyconfigurableml']
                inner_config = inner_config[param]
                return func(config, inner_config, log)
            except KeyError:
                return config
        return inner_func

    return decorator
