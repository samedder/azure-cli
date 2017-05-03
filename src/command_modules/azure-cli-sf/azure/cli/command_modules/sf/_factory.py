# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import os

def cf_sf_client(_):
    from azure.cli.core._environment import get_config_dir
    from azure.cli.core._config import AzConfig
    from azure.cli.core.util import CLIError
    from azure.servicefabric import ServiceFabricClientAPIs
    from azure.cli.command_modules.sf.custom import sf_get_connection_endpoint, sf_get_cert_info, sf_get_ca_cert_info
    from azure.cli.command_modules.sf.aad_auth import AdalAuthentication
    from azure.cli.command_modules.sf.cluster_auth import ClientCertAuthentication
    from azure.cli.core.commands.client_factory import configure_common_settings

    endpoint = sf_get_connection_endpoint()
    if endpoint is None:
        raise CLIError('Connection endpoint not specified, run `az sf cluster select` first.')


    CONFIG_PATH = os.path.join(get_config_dir(), "config")
    az_config = AzConfig()
    az_config.config_parser.read(CONFIG_PATH)
    security_type = str(az_config.get("servicefabric", "security", fallback=""))

    if security_type == "aad":
        token = str(az_config.get("servicefabric", "bearer", fallback=""))
        auth = AdalAuthentication(token)
    else:
        cert = sf_get_cert_info()
        ca_cert = sf_get_ca_cert_info()
        auth = ClientCertAuthentication(cert, ca_cert)

    client = ServiceFabricClientAPIs(auth, base_url=endpoint)
    configure_common_settings(client)
    return client
