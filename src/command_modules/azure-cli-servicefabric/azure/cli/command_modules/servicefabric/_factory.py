# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

def cf_sf_client(_):
    from azure.servicefabric import AzureServiceFabricClientAPIs
    from azure.cli.command_modules.servicefabric.custom import sf_get_connection_endpoint
    return AzureServiceFabricClientAPIs(False, sf_get_connection_endpoint())
    