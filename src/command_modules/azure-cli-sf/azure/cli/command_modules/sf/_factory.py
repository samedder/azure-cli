# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

def cf_sf_client(_):
    from azure.cli.core.util import CLIError
    from azure.servicefabric import AzureServiceFabricClientAPIs
    from azure.cli.command_modules.sf.custom import sf_get_connection_endpoint, sf_get_cert_info
    from azure.cli.command_modules.sf.cluster_auth import ClientCertAuthentication
    from azure.cli.core.commands.client_factory import configure_common_settings

    endpoint = sf_get_connection_endpoint()
    if endpoint is None:
        raise CLIError('Connection endpoint not specified, run `az sf cluster select` first.')

    cert = sf_get_cert_info()
    auth = ClientCertAuthentication(cert)
    client = AzureServiceFabricClientAPIs(auth, base_url=endpoint)
    configure_common_settings(client)
    return client
