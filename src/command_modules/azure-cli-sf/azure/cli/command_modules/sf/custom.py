# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import azure.cli.core.azlogging as azlogging
import requests
import os
import sys
import urllib.parse
from azure.cli.core._config import az_config, set_global_config_value
from azure.cli.core.util import CLIError

logger = azlogging.get_az_logger(__name__)

def sf_connect(endpoint, cert=None, key=None, pem=None):
    """
    Connects to a Service Fabric cluster endpoint.

    If connecting to secure cluster specify a cert (.crt) and key file (.key)
    or a single file with both (.pem). Do not specify both.

    :param str endpoint: Cluster endpoint URL, including port and HTTP or HTTPS prefix:
    :param str cert: Path to a client certificate file
    :param str key: Path to client certificate key file
    :param str pem: Path to client certificate, as a .pem file

    """

    if not all([cert, key]) and not pem:
        CLIError('Invalid syntax: [ --endpoint | --endpoint --key --cert | --endpoint --pem ]')

    if pem and any([cert, key]):
        CLIError('Invalid syntax: [ --endpoint | --endpoint --key --cert | --endpoint --pem ]')

    if pem:
        set_global_config_value('servicefabric', 'pem_path', pem)
    elif cert:
        set_global_config_value('servicefabric', 'cert_path', cert)
        set_global_config_value('servicefabric', 'key_path', key)

    set_global_config_value('servicefabric', 'endpoint', endpoint)


def sf_get_connection_endpoint():
    return az_config.get('servicefabric', 'endpoint', fallback=None)

def sf_get_cert_info():
    cert_path = az_config.get('servicefabric', 'cert_path', fallback=None)
    key_path = az_config.get('servicefabric', 'key_path', fallback=None)
    pem_path = az_config.get('servicefabric', 'pem_path', fallback=None)

    return (cert_path, key_path, pem_path)

class FileIter:
    def __init__(self, file, rel_file_path, print_progress):
        self.file = file
        self.rel_file_path = rel_file_path
        self.print_progress = print_progress

    def __iter__(self):
        return self

    def __next__(self):
        chunk = self.file.read(100000)
        if chunk == b'':
            raise StopIteration
        else:
            self.print_progress(len(chunk), self.rel_file_path)
            return chunk

def sf_copy_app_package(path):
    abspath = os.path.abspath(path)
    basename = os.path.basename(abspath)
    endpoint = sf_get_connection_endpoint()
    total_files_count = 0
    current_files_count = 0
    total_files_size = 0;
    current_files_size = 0;
    for root, dirs, files in os.walk(abspath):
        total_files_count += len(files)
        total_files_count += 1
        for file in files:
            t = os.stat(os.path.join(root, file))
            total_files_size += t.st_size

    def print_progress(size, rel_file_path):
        nonlocal current_files_size
        current_files_size += size
        sys.stdout.write("\r\033[K")
        print('[{}/{}] files, [{}/{}] bytes, {}'.format(current_files_count, total_files_count, current_files_size, total_files_size, rel_file_path), end="\r")
    
    for root, dirs, files in os.walk(abspath):
        rel_path = os.path.normpath(os.path.relpath(root, abspath))
        for file in files:
            url_path = os.path.normpath(os.path.join('ImageStore', basename, rel_path, file)).replace('\\', '/')
            with open(os.path.normpath(os.path.join(root, file)), 'rb') as file_opened:
                url_parsed = list(urllib.parse.urlparse(endpoint))
                url_parsed[2] = url_path
                url_parsed[4] = urllib.parse.urlencode({'api-version': '3.0-preview'})
                url = urllib.parse.urlunparse(url_parsed)
                file_iter = FileIter(file_opened, os.path.normpath(os.path.join(rel_path, file)), print_progress)
                res = requests.put(url, data=file_iter)
                current_files_count += 1
                print_progress(0, os.path.normpath(os.path.join(rel_path, file)))
        
        url_path = os.path.normpath(os.path.join('ImageStore', basename, rel_path, '_.dir')).replace('\\', '/')
        url_parsed = list(urllib.parse.urlparse(endpoint))
        url_parsed[2] = url_path
        url_parsed[4] = urllib.parse.urlencode({'api-version': '3.0-preview'})
        res = requests.put(url)
        current_files_count += 1
        print_progress(0, os.path.normpath(os.path.join(rel_path, '_.dir')))
    sys.stdout.write("\r\033[K")
    print('[{}/{}] files, [{}/{}] bytes sent'.format(current_files_count, total_files_count, current_files_size, total_files_size))
