# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

#pylint: disable=line-too-long

from azure.cli.core.commands import cli_command
from azure.cli.command_modules.servicefabric._factory import cf_sf_client

# Application commands

cli_command(__name__, 'sf application health', 'azure.servicefabric#AzureServiceFabricClientAPIs.get_application_health', cf_sf_client)

# Node commands

cli_command(__name__, 'sf node remove-state', 'azure.servicefabric#AzureServiceFabricClientAPIs.remove_node_state', cf_sf_client)

# Cluster commands

cli_command(__name__, 'sf cluster connect', 'azure.cli.command_modules.servicefabric.custom#sf_update_connection_endpoint')
