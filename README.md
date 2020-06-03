# Configurable ML

[![python](https://github.com/dkmiller/pyconfigurableml/workflows/python/badge.svg)](https://github.com/dkmiller/pyconfigurableml/actions?query=workflow%3Apython)
[![Coverage Status](https://coveralls.io/repos/github/dkmiller/pyconfigurableml/badge.svg?branch=master)](https://coveralls.io/github/dkmiller/pyconfigurableml?branch=master)

Python utilities for easily configurable machine learning.

This project utilizes the excellent tutorial
[How to Publish an Open-Source Python Package to PyPI](https://realpython.com/pypi-publish-python-package/)

## Usage

```python
from pyconfigurableml.entry import run

def main(config, log):
  # TODO: put your logic here.
  pass

if __name__ == '__main__':
  # The main function will be called with appropriate configuration
  # object and logger.
  run(main)
```

## Roadmap

Create and publish a Python package for handling configuration (via config.yml
or command line args) logging, etc.

Calculate and publish code coverage.

Follow badges at [typeguard](https://github.com/agronholm/typeguard).

- [Coveralls](https://docs.coveralls.io/python)
- [Pypi badge](https://thomas-cokelaer.info/blog/2014/08/1013/), include
  number of downloads.
