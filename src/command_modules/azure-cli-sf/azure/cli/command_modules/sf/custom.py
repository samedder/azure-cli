# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import azure.cli.core.azlogging as azlogging
from azure.cli.core._config import az_config, set_global_config_value
from azure.cli.core._util import CLIError

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
    endpoint_url = az_config.get('servicefabric', 'endpoint', fallback=None)
    if endpoint_url is not None:
        return endpoint_url
    else:
        raise CLIError('Service Fabric cluster endpoint not set, connect to a cluster first')

# Store string inside az_config.set and az_config.get

# Add client argument to custom command

# SF client operation action ->
# Create factory in _factory
# Factory creates client instance
# Uses config to pull down connection string
# Returns client to perform API
