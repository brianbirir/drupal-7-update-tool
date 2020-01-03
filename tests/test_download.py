import os
import shutil
import pytest
import requests
from src.download import get_url, MissingVersion, InaccessibleDownloadLink

# @pytest.fixture()
# def initialize_folders(request):
#     os.mkdir(TEMP_DIRECTORY)
#     with open(f'{TEMP_DIRECTORY}/test_file.txt', 'w') as f:
#         f.write('I am a test file')
#
#     def delete_directory():
#         # delete temp directory and its contents
#         shutil.rmtree(TEMP_DIRECTORY)
#
#     request.addfinalizer(delete_directory)


def test_get_url_success():
    version = '7.69'
    assert get_url(
        version
    ) == f'https://ftp.drupal.org/files/projects/drupal-{version}.zip'


def test_missing_version():
    version = ''
    with pytest.raises(MissingVersion):
        get_url(version)


def test_url_response_error():
    version = '1.777'
    with pytest.raises(InaccessibleDownloadLink):
        get_url(version)
