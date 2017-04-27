# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import os
import sys
import urllib.parse
import requests

import azure.cli.core.azlogging as azlogging

from azure.cli.core._environment import get_config_dir
from azure.cli.core._config import AzConfig
from azure.cli.core.util import CLIError

# Really the CLI should do this for us but I cannot see how to get it to
CONFIG_PATH = os.path.join(get_config_dir(), "config")
az_config = AzConfig()

logger = azlogging.get_az_logger(__name__)

def sf_create_compose_application(application_name, file, repo_user=None,
                                  encrypted=False, repo_pass=None):
    # We need to read from a file which makes this a custom command
    # Encrypted param to indicate a password will be prompted
    """
    Creates a Service Fabric application from a Compose file

    :param str application_name:  The name of application to create from
    Compose file. This is typically the full name of the application
    including "fabric:" URI scheme
    :param str file: Path to the Compose file to use
    :param str repo_user: Container repository user name if needed for
    authentication
    :param bool encrypted: If true, indicate to use an encrypted password rather
    than prompting for a plaintext one
    :param str repo_pass: Encrypted container repository password
    """
    from azure.cli.core.util import read_file_content
    from azure.cli.command_modules.sf._factory import cf_sf_client
    from azure.cli.core.prompting import prompt_pass
    from azure.servicefabric.models.create_compose_application_description \
    import CreateComposeApplicationDescription
    from azure.servicefabric.models.repository_credential import RepositoryCredential

    if any([encrypted, repo_pass]) and not all([encrypted, repo_pass, repo_user]):
        raise CLIError("Invalid arguments: [ --application_name --file | \
        --application_name --file --repo_user | --application_name --file \
        --repo_user --encrypted --repo_pass ])")

    if repo_user:
        plaintext_pass = prompt_pass("Container repository password: ", False,
                                     "Password for container repository\
                                      containing container images")
        repo_pass = plaintext_pass

    repo_cred = RepositoryCredential(repo_user, repo_pass, encrypted)

    file_contents = read_file_content(file)

    model = CreateComposeApplicationDescription(application_name, file_contents, repo_cred)

    sf_client = cf_sf_client(None)
    sf_client.create_compose_application(model)

def sf_select(endpoint, cert=None, key=None, pem=None, ca=None):
    """
    Connects to a Service Fabric cluster endpoint.


    If connecting to secure cluster specify a cert (.crt) and key file (.key)
    or a single file with both (.pem). Do not specify both. Optionally, if
    connecting to a secure cluster, specify also a path to a CA bundle file
    or directory of trusted CA certs.

    :param str endpoint: Cluster endpoint URL, including port and HTTP or HTTPS prefix
    :param str cert: Path to a client certificate file
    :param str key: Path to client certificate key file
    :param str pem: Path to client certificate, as a .pem file
    :param str ca: Path to CA certs directory to treat as valid or CA bundle file
    """
    from azure.cli.core._config import set_global_config_value

    usage = "--endpoint [ [ --key --cert | --pem ] --ca ]"

    if ca and not (pem or all([key, cert])):
        raise CLIError("Invalid syntax: " + usage)

    if any([cert, key]) and not all([cert, key]):
        raise CLIError("Invalid syntax: " + usage)

    if pem and any([cert, key]):
        raise CLIError("Invalid syntax: " + usage)

    if pem:
        set_global_config_value("servicefabric", "pem_path", pem)
        set_global_config_value("servicefabric", "security", "pem")
    elif cert:
        set_global_config_value("servicefabric", "cert_path", cert)
        set_global_config_value("servicefabric", "key_path", key)
        set_global_config_value("servicefabric", "security", "cert")
    else:
        set_global_config_value("servicefabric", "security", "none")

    if ca:
        set_global_config_value("servicefabric", "ca_path", ca)

    set_global_config_value("servicefabric", "endpoint", endpoint)

def sf_get_ca_cert_info():
    az_config.config_parser.read(CONFIG_PATH)
    ca_cert = az_config.get("servicefabric", "ca_path", fallback=None)
    return ca_cert

def sf_get_connection_endpoint():
    az_config.config_parser.read(CONFIG_PATH)
    return az_config.get("servicefabric", "endpoint", fallback=None)

def sf_get_cert_info():
    az_config.config_parser.read(CONFIG_PATH)
    security_type = az_config.get("servicefabric", "security", fallback=None)
    if security_type is "pem":
        pem_path = az_config.get("servicefabric", "pem_path", fallback=None)
        return pem_path
    elif security_type is "cert":
        cert_path = az_config.get("servicefabric", "cert_path", fallback=None)
        key_path = az_config.get("servicefabric", "key_path", fallback=None)
        return cert_path, key_path
    elif security_type is "none":
        return None
    else:
        raise CLIError("Cluster security type not set")

    cert_path = az_config.get('servicefabric', 'cert_path', fallback=None)
    key_path = az_config.get('servicefabric', 'key_path', fallback=None)
    pem_path = az_config.get('servicefabric', 'pem_path', fallback=None)

    return (cert_path, key_path, pem_path)

class FileIter: # pylint: disable=too-few-public-methods
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
    total_files_size = 0
    current_files_size = 0
    for root, _, files in os.walk(abspath):
        total_files_count += len(files)
        total_files_count += 1
        for file in files:
            t = os.stat(os.path.join(root, file))
            total_files_size += t.st_size

    def print_progress(size, rel_file_path):
        nonlocal current_files_size
        current_files_size += size
        sys.stdout.write("\r\033[K")
        print('[{}/{}] files, [{}/{}] bytes, {}'.format(current_files_count,
                                                        total_files_count,
                                                        current_files_size,
                                                        total_files_size,
                                                        rel_file_path),
              end="\r")
    for root, _, files in os.walk(abspath):
        rel_path = os.path.normpath(os.path.relpath(root, abspath))
        for file in files:
            url_path = os.path.normpath(os.path.join('ImageStore', basename,
                                                     rel_path, file)).replace('\\', '/')
            with open(os.path.normpath(os.path.join(root, file)), 'rb') as file_opened:
                url_parsed = list(urllib.parse.urlparse(endpoint))
                url_parsed[2] = url_path
                url_parsed[4] = urllib.parse.urlencode({'api-version': '3.0-preview'})
                url = urllib.parse.urlunparse(url_parsed)
                file_iter = FileIter(file_opened, os.path.normpath(
                    os.path.join(rel_path, file)), print_progress)
                _ = requests.put(url, data=file_iter)
                current_files_count += 1
                print_progress(0, os.path.normpath(os.path.join(rel_path, file)))
        url_path = os.path.normpath(os.path.join('ImageStore', basename,
                                                 rel_path, '_.dir')).replace('\\', '/')
        url_parsed = list(urllib.parse.urlparse(endpoint))
        url_parsed[2] = url_path
        url_parsed[4] = urllib.parse.urlencode({'api-version': '3.0-preview'})
        _ = requests.put(url)
        current_files_count += 1
        print_progress(0, os.path.normpath(os.path.join(rel_path, '_.dir')))
    sys.stdout.write("\r\033[K")
    print('[{}/{}] files, [{}/{}] bytes sent'.format(current_files_count,
                                                     total_files_count,
                                                     current_files_size,
                                                     total_files_size))

def sf_create_app(name, app_type, version, parameters=None, # pylint: disable=too-many-arguments
                  min_node_count=0, max_node_count=0, metrics=None):
    """
    Creates a Service Fabric application using the specified description

    :param str name: Application name
    :param str app_type: Application type
    :param str version: Application version
    :param long min_node_count: The minimum number of nodes where Service Fabric
    will reserve capacity for this application. Note that this does not mean
    that the services of this application will be placed on all of those
    nodes.
    :param long max_node_count: The maximum number of nodes where Service Fabric
    will reserve capacity for this application. Note that this does not mean
    that the services of this application will be placed on all of those
    nodes.
    """
    from azure.servicefabric.models.application_description import ApplicationDescription
    from azure.servicefabric.models.application_parameter import ApplicationParameter
    from azure.servicefabric.models.application_capacity_description \
    import ApplicationCapacityDescription

    if min_node_count > max_node_count:
        raise CLIError("Note, the minimum node reserve capacity count cannot \
        be more than the maximum node count")

    app_params = None
    if parameters is not None:
        app_params = []
        for k in parameters:
            # Create an application parameter for every of these
            p = ApplicationParameter(k, parameters[k])
            app_params.append(p)
    
    app_metrics = None
    if metrics is not None:
        app_metrics = []


def sf_upgrade_app():
    """

    """
    from azure.servicefabric.models.application_description import ApplicationDescription
    from azure.servicefabric.models.application_parameter import ApplicationParameter

    # TODO, waiting on CLI guys to explain best way to handle arbitary user dicts

def sf_create_service(app_name, name, type, singleton_scheme=False, 
                      named_scheme=False, int_scheme=False):
    """
    Creates a Service Fabric application using the specified description

    :param str app_name: Name of the parent application for the service
    :param str name: Name of the service to be created
    :param str type: Name of the service type to be created
    :param bool singleton_scheme: Indicates the service should have a single
    partition, or be not partition. Each service must have only one partition
    scheme
    :param bool named_scheme: Indicates the service should be partitioned by
    using string names as keys. Each service must have only one partition scheme
    :param bool int_scheme: Indicates the service should be partitioned across
    a uniform range of unsigned integers. Each service must have only one
    partition scheme
    """
    from azure.servicefabric.models.service_description import ServiceDescription
    from azure.servicefabric.models.named_partition_scheme_description \
    import NamedPartitionSchemeDescription
    from azure.servicefabric.models.singleton_partition_scheme_description \
    import SingletonPartitionSchemeDescription
    from azure.servicefabric.models.uniform_int64_range_partition_scheme_description \
    import UniformInt64RangePartitionSchemeDescription

    if not sum([singleton_scheme, named_scheme, int_scheme]) is 1:
        raise CLIError("Specify exactly  one partition scheme")
    