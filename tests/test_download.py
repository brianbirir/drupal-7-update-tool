import os
import time
import shutil

import pytest

from src.download import get_url, MissingVersion, InaccessibleDownloadLink, download_drupal_update, uncompress_drupal_update

VERSION = '7.69'
DRUPAL_UPDATE_FILE = f'/tmp/drupal_update/drupal-{VERSION}.tar.gz'


@pytest.fixture()
def initialize_folders(request):
    def delete_drupal_update_file():
        os.remove(DRUPAL_UPDATE_FILE)
        shutil.rmtree('/tmp/drupal_update')

    request.addfinalizer(delete_drupal_update_file)


def test_get_url_success():
    assert get_url(
        VERSION
    ) == f'https://ftp.drupal.org/files/projects/drupal-{VERSION}.tar.gz'


def test_missing_version():
    version = ''
    with pytest.raises(MissingVersion):
        get_url(version)


def test_url_response_error():
    version = '1.777'
    with pytest.raises(InaccessibleDownloadLink):
        get_url(version)


def test_download_success(initialize_folders):
    assert download_drupal_update(VERSION)


def test_compressed_file_extraction(initialize_folders):
    download_drupal_update(VERSION)
    time.sleep(3)
    assert uncompress_drupal_update(DRUPAL_UPDATE_FILE, VERSION)
