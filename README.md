**:warning: Instead of this package, you should use [hydra](https://hydra.cc/),
which is more general and robust.**

----

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

You may also use this library to configure a set of unit tests. If you're using
PyTest, 

```python
from pyconfigurableml.entry import run_no_parse_args

def custom_setup_logic(config, log):
  # TODO: put your logic here.
  pass

def setup_module(module):
  # You probably don't want to attempt to parse command line arguments
  # inside unit tests.
  run_no_parse_args(custom_setup_logic, __file__)
```

## Configuring this library

In addition to using pyconfigurableml to parse and inject configuration into
your main method, you may also configure the library itself by adding some
information under a `pyconfigurableml` field in your config file.

First, to enable these extras, install them:

```
pip install pyconfigurableml[azure,munch]
```

Then, add subfields following the example below.

```yml
# You may insert your other configuration here as usual.

# This section is for configuration specific to this library.
pyconfigurableml:

  azure:
    # Replace URLs to Azure Key Vault secrets with the secret values. The code
    # must be running in an environment with access to those key vaults.
    resolve_secret_identifiers: True

    # (Optional) Azure Active Directory tenant ID to use when initializing a
    # "default Azure credential" object.
    tenant: 2b9d773f-f2b1-43e7-8a53-bbe28bbb0c6b

  # Ensure files downloaded from the configured URLs exist at these paths
  # (relative to working directory). This library does not (yet) handle
  # authenticating against files stored in enterprise storage accounts (e.g.,
  # Azure blob storage).
  files:
    .data/resnet.tar.gz: https://github.com/onnx/models/raw/master/vision/classification/resnet/model/resnet18-v2-7.tar.gz
    .data/labels.txt: https://raw.githubusercontent.com/onnx/models/master/vision/classification/synset.txt

  # Dictionary mapping logger names to minimum levels. This is convenient for
  # suppressing overly verbose logs from consumed libraries.
  logging:
    azure.core.pipeline.policies.http_logging_policy: WARN

  # If this flag is set to true, the library will convert the configuration
  # object into a "JavaScript-style" object, i.e. a['b'] may be accessed via
  # a.b.
  munch: True
```
