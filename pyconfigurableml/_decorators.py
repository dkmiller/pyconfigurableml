import functools


def pass_decorator(param: str):

    def decorator(func):
        @functools.wraps(func)
        def inner_func(config):
            try:
                if isinstance(config, list):
                    raise Exception(str(func) + '   ' + str(config))
                inner_config = config['pyconfigurableml']
                inner_config = inner_config[param]
                return func(config, inner_config)
            except KeyError:
                return config
        return inner_func

    return decorator
