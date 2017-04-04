# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

def cf_sf_client(_):
    from azure.servicefabric import AzureServiceFabricClientAPIs
    return AzureServiceFabricClientAPIs(False,'http://localhost:19080') 