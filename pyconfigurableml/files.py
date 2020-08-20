import concurrent.futures
import logging
import os.path
from typeguard import typechecked
from typing import Dict
import shutil
from pyconfigurableml._core import run_with_specified_config
import requests


@typechecked
def download_url_to_file(url: str, path: str) -> None:
    '''
    https://stackoverflow.com/a/39217788
    '''
    with requests.get(url, stream=True) as req:
        with open(path, 'wb') as file:
            shutil.copyfileobj(req.raw, file)


@typechecked
def download_url_to_file_if_not_exists(url: str, path: str) -> None:
    log = logging.getLogger(__name__)
    if not os.path.isfile(path):
        log.warning(f'Downloading {url} to {path}')
        download_url_to_file(url, path)


@typechecked
def download_urls_to_files_if_not_exist(path_to_url: Dict[str, str]) -> None:
    '''
    https://www.digitalocean.com/community/tutorials/how-to-use-threadpoolexecutor-in-python-3
    '''
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = []
        for k, v in path_to_url.items():
            futures.append(executor.submit(download_url_to_file_if_not_exists, url=v, path=k))

        concurrent.futures.as_completed(futures)


@run_with_specified_config(__name__)
@typechecked
def ensure_files_exist(config, inner_config: Dict[str, str]):
    '''
    TODO: docstring.
    '''
    download_urls_to_files_if_not_exist(inner_config)

    return config
