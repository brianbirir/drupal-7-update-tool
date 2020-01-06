import os
import tarfile

import requests

DOWNLOAD_TMP = '/tmp/drupal_update'
DRUPAL_DOWNLOAD_BASE_URL = 'https://ftp.drupal.org/files/projects/drupal-'


class MissingDirectoryException(Exception):
    """Raised when directory is missing"""
    def __init__(self):
        Exception.__init__(self, "The directory does not exist!")


class MissingVersion(Exception):
    """Raised when Drupal 7 version is missing"""
    def __init__(self):
        Exception.__init__(self, "The version of Drupal 7 is missing!")


class InaccessibleDownloadLink(Exception):
    """Raised when Download link returns a response code other than 200"""
    def __init__(self):
        Exception.__init__(
            self, "Response error while accessing Drupal download link!")


class UnsuccessfulFileDownload(Exception):
    """Raised when file download fails"""
    def __init__(self):
        Exception.__init__(self, "The download failed!")


class WrongFileFormat(Exception):
    """Raised when downloaded Drupal update file is wrong file format"""
    def __init__(self):
        Exception.__init__(self, "Downloaded file is wrong file format!")


class FileExtractionFailed(Exception):
    """Raised when extracting Drupal zip file fails"""
    def __init__(self):
        Exception.__init__(self, "Extraction of Zip file failed!")


def ping_url(response: int) -> bool:
    """Pings url"""
    if response == 200:
        return True


def get_url(version: str) -> str:
    """Gets and validates url"""
    # check if version is empty
    if not version:
        raise MissingVersion()

    try:
        full_url = ''.join([DRUPAL_DOWNLOAD_BASE_URL, version, '.tar.gz'])
        response_obj = requests.get(full_url)

        if ping_url(response_obj.status_code):
            print('Drupal download link is accessible')
            return full_url
        else:
            raise InaccessibleDownloadLink()
    except requests.exceptions.ConnectionError as e:
        print(str(e))


def check_download_file_type(drupal_file: str) -> bool:
    return tarfile.is_tarfile(drupal_file)


def download_drupal_update(version: str) -> bool:
    """Downloads Drupal zip file via url"""
    os.mkdir('/tmp/drupal_update')
    try:
        url = get_url(version)
        response_obj = requests.get(url, stream=True)
        drupal_update_file = f'{DOWNLOAD_TMP}/drupal-{version}.tar.gz'

        with open(drupal_update_file, 'wb') as f:
            f.write(response_obj.content)

        print(f'Downloaded: {drupal_update_file}')
        # uncompress_drupal_update(drupal_update_file, version)
        if check_download_file_type(drupal_update_file):
            return True
        else:
            print('Not a tar file!')

    except UnsuccessfulFileDownload as e:
        print(str(e))
    except Exception as e:
        print(str(e))


def uncompress_drupal_update(drupal_file: str, drupal_version: str):
    print(drupal_file)
    print(drupal_version)
    """Extracts Drupal update tar file"""
    try:
        if tarfile.is_tarfile(drupal_file):
            print('The file is a tar file, continuing with extraction!')
            drupal_tar_file = tarfile.open(drupal_file, 'r')
            drupal_tar_file.extractall(path=f'{DOWNLOAD_TMP}/')
            drupal_tar_file.close()

            if os.path.exists(f'{DOWNLOAD_TMP}/drupal-{drupal_version}/'):
                print('File extraction successful')
                return True
            else:
                raise MissingDirectoryException()
        else:
            print('Not a tar file!')
    except Exception as e:
        print(str(e))
