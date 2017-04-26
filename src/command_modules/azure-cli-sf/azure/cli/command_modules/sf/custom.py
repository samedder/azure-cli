# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import azure.cli.core.azlogging as azlogging
import os

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

    if not all([cert, key]) and not pem:
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
