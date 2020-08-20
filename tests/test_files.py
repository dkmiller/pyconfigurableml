import logging
import os.path
import pytest
from pyconfigurableml.files import download_url_to_file, download_url_to_file_if_not_exists, download_urls_to_files_if_not_exist


@pytest.mark.parametrize('url,file_name', [
    ('https://picsum.photos/id/237/200', 'foo.png')
])
def test_download_url_to_file(url, file_name, tmpdir):
    path = str(tmpdir.join(file_name))

    assert not os.path.isfile(path)

    download_url_to_file(url, path)

    assert os.path.isfile(path)


@pytest.mark.parametrize('url,file_name', [
    ('http://foo.bar/baz', 'foo.png')
])
def test_download_url_to_file_if_not_exists__when_file_exists(url, file_name, tmpdir):
    path = tmpdir.join(file_name)
    path.write('content')

    path_str = str(path)

    assert os.path.isfile(path_str)

    download_url_to_file_if_not_exists(url, path_str)

    assert path.read() == 'content'


@pytest.mark.parametrize('url,file_name', [
    ('https://picsum.photos/id/237/200', 'foo.png')
])
def test_download_url_to_file_if_not_exists__when_file_does_not_exist(url, file_name, tmpdir):
    path = str(tmpdir.join(file_name))

    assert not os.path.isfile(path)

    download_url_to_file(url, path)

    assert os.path.isfile(path)


@pytest.mark.parametrize('mapping', [
    {
        'a.png': 'https://picsum.photos/id/237/200'
    },
    {
        'a.png': 'https://picsum.photos/id/237/200',
        'b.gif': 'https://picsum.photos/id/238/200',
        'c.bar': 'https://picsum.photos/id/239/200'
    }
])
def test_download_urls_to_files_if_not_exist(mapping, tmpdir):
    mapping = {str(tmpdir.join(k)): v for k, v in mapping.items()}
    assert len(mapping) > 0
    assert all(not os.path.isfile(path) for path in mapping.keys())

    download_urls_to_files_if_not_exist(mapping)

    assert all(os.path.isfile(path) for path in mapping.keys())


@pytest.mark.parametrize('mapping', [
    {
        'a.png': 'http://foo/bar'
    },
    {
        'a.png': 'https://baz/foo',
        'b.gif': 'https://a.b/c',
        'c.bar': 'https://ax.com/xy'
    }
])
def test_download_urls_to_files_if_not_exist__when_files_not_exist(mapping, tmpdir):
    mapping_new = {}
    for k, v in mapping.items():     
        path = tmpdir.join(k)
        path.write('content')
        mapping_new[str(path)] = v

    download_urls_to_files_if_not_exist(mapping_new)
