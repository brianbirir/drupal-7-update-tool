import sys
import requests


DOWNLOAD_TMP = '/tmp'
DRUPAL_DOWNLOAD_BASE_URL = 'https://ftp.drupal.org/files/projects/drupal-'


class MissingVersion(Exception):
    """Raised when Drupal 7 version is missing"""
    def __init__(self):
        Exception.__init__(self, "The version of Drupal 7 is missing!")


class InaccessibleDownloadLink(Exception):
    """Raised when Download link returns a response code other than 200"""
    def __init__(self):
        Exception.__init__(self, "Response error while accessing Drupal download link!")


def get_url(version: str) -> str:
    # check if version is empty
    if not version:
        raise MissingVersion()

    try:
        full_url = ''.join([DRUPAL_DOWNLOAD_BASE_URL, version, '.zip'])
        ping_response = requests.get(full_url)

        if ping_url(ping_response.status_code):
            print('Drupal download link is accessible')
            return full_url
        else:
            raise InaccessibleDownloadLink()
    except requests.exceptions.ConnectionError as e:
        print(str(e))


def ping_url(response: int) -> bool:
    if response == 200:
        return True


def download_drupal_update():
    pass


def uncompress_drupal_update():
    pass

