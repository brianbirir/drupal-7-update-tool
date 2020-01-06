import os
import sys
import datetime
import zipfile

from src.lib.exceptions import MissingDirectoryException


def get_file_paths(dir_name: str) -> list:
    file_paths = []

    if os.path.exists(dir_name):
        # crawl directory and subdirectories
        for root, directories, files in os.walk(dir_name):
            for file_name in files:
                full_file_path = os.path.join(root, file_name)
                file_paths.append(full_file_path)
        return file_paths
    else:
        raise MissingDirectoryException()


def compress_backup(dir_name: str):
    try:
        if os.path.exists(dir_name):
            print('Folder path exists')
            compressed_file = f'drupalSiteBackup_{datetime.date.today().strftime("%Y%m%d")}.zip'
            compressed_file_path = f'{dir_name}/{compressed_file}'

            file_paths = get_file_paths(dir_name)
            print('The following files will be compressed: ')
            for file_name in file_paths:
                print(file_name)

            print('Writing files to a zip file')
            with zipfile.ZipFile(compressed_file_path, 'w') as z:
                for f in file_paths:
                    z.write(f)
            print('All files have been compressed successfully')
            return True
        else:
            print('Folder path does not exist. Insert correct folder path')
            return False
    except Exception as e:
        print(f'Error: {str(e)}')
        sys.exit()
