# Configurable ML

[![python](https://github.com/dkmiller/pyconfigurableml/workflows/python/badge.svg)](https://github.com/dkmiller/pyconfigurableml/actions?query=workflow%3Apython)
[![Coverage Status](https://coveralls.io/repos/github/dkmiller/pyconfigurableml/badge.svg?branch=master)](https://coveralls.io/github/dkmiller/pyconfigurableml?branch=master)
[![PyPI version](https://badge.fury.io/py/pyconfigurableml.svg)](https://badge.fury.io/py/pyconfigurableml)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/pyconfigurableml)](https://pypi.org/project/pyconfigurableml/)

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
  run(main, __file__)

# Alternative approach. Will only load configuration + run main if
# __name__ == '__main__'.
run(main, __file__, __name__)
```
