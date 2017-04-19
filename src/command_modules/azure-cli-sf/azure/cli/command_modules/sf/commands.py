# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

#pylint: disable=line-too-long

from azure.cli.core.commands import cli_command
from azure.cli.command_modules.sf._factory import cf_sf_client

# Application commands

cli_command(__name__, 'sf application hehalth', 'azure.servicefabric#AzureServiceFabricClientAPIs.get_application_health', cf_sf_client)
cli_command(__name__, 'sf application manifest', 'azure.servicefabric#AzureServiceFabricClientAPIs.get_application_type_manifest', cf_sf_client)
cli_command(__name__, 'sf application report-health', 'azure.servicefabric#AzureServiceFabricClientAPIs.report_application_health', cf_sf_client)

# Service commands

cli_command(__name__, 'sf service list', 'azure.servicefabric#AzureServiceFabricClientAPIs.get_service_info_list', cf_sf_client)
cli_command(__name__, 'sf service manifest', 'azure.servicefabric#AzureServiceFabricClientAPIs.get_service_manifest', cf_sf_client)
cli_command(__name__, 'sf service application-name', 'azure.servicefabric#AzureServiceFabricClientAPIs.get_application_name', cf_sf_client)
cli_command(__name__, 'sf service report-health', 'azure.servicefabric#AzureServiceFabricClientAPIs.report_service_health', cf_sf_client)

# Partition commands

cli_command(__name__, 'sf partition info', 'azure.servicefabric#AzureServiceFabricClientAPIs.get_partition_info', cf_sf_client)
cli_command(__name__, 'sf partition service-name', 'azure.servicefabric#AzureServiceFabricClientAPIs.get_service_name', cf_sf_client)
cli_command(__name__, 'sf partition report-health', 'azure.servicefabric#AzureServiceFabricClientAPIs.report_partition_health', cf_sf_client)
cli_command(__name__, 'sf partition health', 'azure.servicefabric#AzureServiceFabricClientAPIs.get_partition_health', cf_sf_client)

# Replica commands

cli_command(__name__, 'sf replica report-health', 'azure.servicefabric#AzureServiceFabricClientAPIs.report_replica_health', cf_sf_client)
cli_command(__name__, 'sf replica health', 'azure.servicefabric#AzureServiceFabricClientAPIs.get_replica_health', cf_sf_client)

# Node commands

cli_command(__name__, 'sf node list', 'azure.servicefabric#AzureServiceFabricClientAPIs.get_node_info_list', cf_sf_client)
cli_command(__name__, 'sf node remove-state', 'azure.servicefabric#AzureServiceFabricClientAPIs.remove_node_state', cf_sf_client)
cli_command(__name__, 'sf node stop', 'azure.servicefabric#AzureServiceFabricClientAPIs.stop_node', cf_sf_client)
cli_command(__name__, 'sf node restart', 'azure.servicefabric#AzureServiceFabricClientAPIs.restart_node', cf_sf_client)
cli_command(__name__, 'sf node start', 'azure.servicefabric#AzureServiceFabricClientAPIs.start_node', cf_sf_client)
cli_command(__name__, 'sf node replica-list', 'azure.servicefabric#AzureServiceFabricClientAPIs.get_deployed_service_replica_info_list', cf_sf_client)
cli_command(__name__, 'sf node load', 'azure.servicefabric#AzureServiceFabricClientAPIs.get_node_load_info', cf_sf_client)
cli_command(__name__, 'sf node health', 'azure.servicefabric#AzureServiceFabricClientAPIs.get_node_health', cf_sf_client)
cli_command(__name__, 'sf node report-health', 'azure.servicefabric#AzureServiceFabricClientAPIs.report_node_health', cf_sf_client)

# Cluster commands

cli_command(__name__, 'sf cluster connect', 'azure.cli.command_modules.sf.custom#sf_connect')
cli_command(__name__, 'sf cluster manifest', 'azure.servicefabric#AzureServiceFabricClientAPIs.get_cluster_manifest')
cli_command(__name__, 'sf cluster code-version', 'azure.servicefabric#AzureServiceFabricClientAPIs.get_provisioned_fabric_code_version_info_list')
cli_command(__name__, 'sf cluster config-version', 'azure.servicefabric#AzureServiceFabricClientAPIs.get_provisioned_fabric_config_version_info_list')
cli_command(__name__, 'sf cluster health', 'azure.servicefabric#AzureServiceFabricClientAPIs.get_cluster_health')
cli_command(__name__, 'sf cluster report-health', 'azure.servicefabric#AzureServiceFabricClientAPIs.report_cluster_health')
