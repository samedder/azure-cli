# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import azure.cli.core.azlogging as azlogging
from azure.cli.core._config import az_config, set_global_config_value


logger = azlogging.get_az_logger(__name__)

def sf_update_connection_endpoint(endpoint):
    """
    Updates the current cluster connection endpoint to point to the specified
    url.

    :param endpoint: The new endpoint url of a Service Fabric cluster
    :type endpoint: String
    """

    set_global_config_value('servicefabric', 'endpoint', endpoint)

def sf_get_connection_endpoint():
    return az_config.get('servicefabric', 'endpoint', fallback=None)

def sf_get_cert_info():
    cert_path = az_config.get('servicefabric', 'cert_path', fallback=None)
    password_protected = az_config.get('servicefabric', 'cert_path', fallback=False)
    return (cert_path, password_protected)

def sf_set_cert_info(path, password_protected=False):
    set_global_config_value('servicefabric', 'cert_path', path)
    set_global_config_value('servicefabric', 'cert_password', password_protected)
