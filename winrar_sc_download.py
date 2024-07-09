#!/usr/bin/env python3
'''
This script finds and downloads the hidden "Ads-Free" version of WinRAR in Simplified Chinese.
It brute-forces through potential release dates to find the correct download link.
Please note that the "Ads-Free" SC version may not be available until a few days after release.
WinRAR Requires a license.
'''

import requests
from datetime import datetime, timedelta
import re
import os

DOWNLOAD_PATH = os.path.join(os.path.expanduser('~'), 'Downloads')
try:
    import platformdirs
    DOWNLOAD_PATH = platformdirs.user_downloads_dir()
except ImportError:
    pass

def get_version_code():
    version_code_input = input('Enter the version code or URL: ')
    if version_code_input.startswith('https://'):
        match = re.search(r'winrar-x(64|32)-(\d+)', version_code_input)
        if match:
            version_code = match.group(2)
            return version_code
        else:
            print('Invalid URL.')
            return get_version_code()
    else:
        try:
            return str(int(version_code_input))
        except ValueError:
            print('Invalid Input.')
            return get_version_code()

def get_release_date():
    print('You can find release dates on https://www.win-rar.com/singlenewsview.html')
    release_date_input = input('Enter the release date (formatted as YYYYMMDD): ')
    try:
        return datetime.strptime(release_date_input, '%Y%m%d')
    except ValueError:
        print('Invalid date format.')
        return get_release_date()

def get_architecture():
    architecture_input = input('Enter the architecture (x64): ')
    if architecture_input == '':
        return 'x64'
    else:
        return architecture_input

def download_file(version_code: str, release_date: str, architecture: str = '64'):
    retry_limit = 30
    retries = 0

    while retries < retry_limit:
        date_str = release_date.strftime('%Y%m%d')
        url = f'https://www.win-rar.com/fileadmin/winrar-versions/sc/sc{date_str}/wrr/winrar-{architecture}-{version_code}sc.exe'
        print(f'Downloading from URL: {url}')
        response = requests.get(url)
        
        if response.status_code == 404:
            print(f'File not found. Retrying with next day...')
            release_date += timedelta(days=1)
            retries += 1
        else:
            file_name = os.path.join(DOWNLOAD_PATH, f'winrar-{architecture}-{version_code}sc.exe')
            with open(file_name, 'wb') as file:
                file.write(response.content)
            print(f'File saved as {file_name}')
            break
    else:
        print('Exceeded retry limit. File could not be found.')

if __name__ == '__main__':
    print(f'Download Directory: {DOWNLOAD_PATH}')
    version_code = get_version_code()
    print(f'Version code: {version_code}')
    release_date = get_release_date()
    print(f'Release date: {release_date.strftime("%Y-%m-%d")}')
    architecture = get_architecture()
    print(f'Architecture: {architecture}')
    download_file(version_code, release_date, architecture)
