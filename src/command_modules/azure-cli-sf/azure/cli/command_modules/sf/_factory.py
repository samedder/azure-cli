# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azure.cli.core._util import CLIError

def cf_sf_client(_):
    from azure.servicefabric import AzureServiceFabricClientAPIs
    from azure.cli.command_modules.sf.custom import sf_get_connection_endpoint, sf_get_cert_info
    from azure.cli.core.prompting import prompt_pass
    from azure.cli.command_modules.sf.cluster_auth import ClientCertAuthentication

    endpoint = sf_get_connection_endpoint()
    if endpoint is None:
        raise CLIError('Connection endpoint not specified, run `az sf cluster connect` first.')

    cert_path, password_protected = sf_get_cert_info()
    if cert_path is not None:
        # Certificate required for cluster connection
        if password_protected:
            cert_password = prompt_pass('Certificate Password: ', False, 'Enter\
             the password associated with the certificate used to connect to\
             the Service Fabric cluster.')
        else:
            cert_password = None
        auth = ClientCertAuthentication(cert_path, cert_password)
        return AzureServiceFabricClientAPIs(auth, base_url=endpoint)
    else:
        return AzureServiceFabricClientAPIs(False, base_url=endpoint)
