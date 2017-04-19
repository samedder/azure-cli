# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azure.cli.core.util import CLIError

def cf_sf_client(_):
    from azure.servicefabric import AzureServiceFabricClientAPIs
    from azure.cli.command_modules.sf.custom import sf_get_connection_endpoint, sf_get_cert_info
    from azure.cli.command_modules.sf.cluster_auth import ClientCertAuthentication

    endpoint = sf_get_connection_endpoint()
    if endpoint is None:
        raise CLIError('Connection endpoint not specified, run `az sf cluster connect` first.')

    cert, key, pem = sf_get_cert_info()
    auth = ClientCertAuthentication(cert=cert, key=key, pem=pem)
    return AzureServiceFabricClientAPIs(auth, base_url=endpoint)
