import os
import shutil
import pytest
import datetime

from src.backup import get_file_paths, compress_backup, MissingDirectoryException

TEMP_DIRECTORY = '/tmp/tempDir'


@pytest.fixture()
def initialize_folders(request):
    os.mkdir(TEMP_DIRECTORY)
    with open(f'{TEMP_DIRECTORY}/test_file.txt', 'w') as f:
        f.write('I am a test file')

    def delete_directory():
        # delete temp directory and its contents
        shutil.rmtree(TEMP_DIRECTORY)

    request.addfinalizer(delete_directory)


def test_get_file_paths_success(initialize_folders):
    assert type(get_file_paths(TEMP_DIRECTORY)) is list


def test_get_file_paths_failure():
    with pytest.raises(MissingDirectoryException):
        get_file_paths('/tmp/fakeDirectory')


def test_compress_backup_success(initialize_folders):
    assert compress_backup(TEMP_DIRECTORY)


def test_compress_backup_failure():
    assert compress_backup('/tmp/fakeDirectory') is False


def test_compressed_file_exists(initialize_folders):
    compress_backup(TEMP_DIRECTORY)
    compressed_file = f'drupalSiteBackup_{datetime.date.today().strftime("%Y%m%d")}.zip'
    assert os.path.exists(f'{TEMP_DIRECTORY}/{compressed_file}')
