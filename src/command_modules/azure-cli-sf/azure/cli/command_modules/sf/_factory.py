# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azure.cli.core._util import CLIError

def cf_sf_client(_):
    from azure.servicefabric import AzureServiceFabricClientAPIs
    from azure.cli.command_modules.sf.custom import sf_get_connection_endpoint


    return AzureServiceFabricClientAPIs(False, sf_get_connection_endpoint())

    