# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import azure.cli.core.azlogging as azlogging
from azure.cli.core._config import az_config, set_global_config_value
from azure.cli.core._util import CLIError

logger = azlogging.get_az_logger(__name__)

def sf_connect(endpoint, cert_path=None, has_password=False):
    """
    Connects to a Service Fabric cluster endpoint

    :param str endpoint: Cluster endpoint URL, including port and HTTP or HTTPS prefix:
    :param str cert_path: Path to a client certificate file
    :param bool has_password: True if the client certificate requires a password

    """

    if has_password and (cert_path is None):
        raise CLIError('--pass-protected must be used with --cert-path')

    set_global_config_value('servicefabric', 'endpoint', endpoint)
    if cert_path is not None:
        set_global_config_value('servicefabric', 'cert_path', cert_path)

    if has_password:
        set_global_config_value('servicefabric', 'cert_password', str(has_password))


def sf_get_connection_endpoint():
    return az_config.get('servicefabric', 'endpoint', fallback=None)

def sf_get_cert_info():
    cert_path = az_config.get('servicefabric', 'cert_path', fallback=None)
    password_protected = az_config.get('servicefabric', 'cert_path', fallback=False)
    # If anything set, assume then password protected
    if password_protected:
        password_protected = bool(password_protected)
    return (cert_path, password_protected)

