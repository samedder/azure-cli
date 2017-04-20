# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import azure.cli.core.azlogging as azlogging
from azure.cli.core.util import CLIError

logger = azlogging.get_az_logger(__name__)

def sf_create_compose_application(application_name, file, repo_user=None,
                                  encrypted=False, repo_pass=None):
    # We need to read from a file which makes this a custom command
    # Encrypted param to indicate a password will be prompted
    """
    Creates a Service Fabric application from a Compose file

    :param str application_name:  The name of application to create from
    Compose file. This is typically the full name of the application
    including 'fabric:' URI scheme
    :param str file: Path to the Compose file to use
    :param str repo_user: Container repository user name if needed for
    authentication
    :param bool encrypted: If true, indicate to use an encrypted password rather
    than prompting for a plaintext one
    :param str repo_pass: Encrypted container repository password
    """
    from azure.cli.core.util import read_file_content
    from azure.cli.command_modules.sf._factory import cf_sf_client

    if encrypted and not all([repo_pass, repo_user]):
        CLIError("Invalid arguments: [ --application_name --file | \
        --application_name --file --repo_user | --application_name --file \
        --repo_user --encrypted --repo_pass ])")

    # TODO: Check on password and prompt if un-encrypted

    file_contents = read_file_content(file)
    sf_client = cf_sf_client(None)
    sf_client.create_compose_application(application_name, file_contents,
                                         repo_user, repo_pass, encrypted)


def sf_connect(endpoint, cert=None, key=None, pem=None):
    from azure.cli.core._config import az_config, set_global_config_value

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
        CLIError('Invalid arguments: [ --endpoint | --endpoint --key --cert | --endpoint --pem ]')

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

