# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

#pylint: disable=line-too-long

from azure.cli.core.commands import cli_command
from azure.cli.command_modules.sf._factory import cf_sf_client

# Application commands

cli_command(__name__, 'sf application health', 'azure.servicefabric#ServiceFabricClientAPIs.get_application_health', cf_sf_client)
cli_command(__name__, 'sf application manifest', 'azure.servicefabric#ServiceFabricClientAPIs.get_application_type_manifest', cf_sf_client)
cli_command(__name__, 'sf application report-health', 'azure.servicefabric#ServiceFabricClientAPIs.report_application_health', cf_sf_client)
cli_command(__name__, 'sf application provision', 'azure.servicefabric#ServiceFabricClientAPIs.provision_application', cf_sf_client)
cli_command(__name__, 'sf application create', 'azure.cli.command_modules.sf.custom#sf_create_app')
cli_command(__name__, 'sf application delete', 'azure.servicefabric#ServiceFabricClientAPIs.delete_application', cf_sf_client)
cli_command(__name__, 'sf application unprovision', 'azure.servicefabric#ServiceFabricClientAPIs.unprovision_application', cf_sf_client)
cli_command(__name__, 'sf application upgrade', 'azure.cli.command_modules.sf.custom#sf_upgrade_app')


# Service commands

cli_command(__name__, 'sf service list', 'azure.servicefabric#ServiceFabricClientAPIs.get_service_info_list', cf_sf_client)
cli_command(__name__, 'sf service manifest', 'azure.servicefabric#ServiceFabricClientAPIs.get_service_manifest', cf_sf_client)
cli_command(__name__, 'sf service application-name', 'azure.servicefabric#ServiceFabricClientAPIs.get_application_name_info', cf_sf_client)
cli_command(__name__, 'sf service report-health', 'azure.servicefabric#ServiceFabricClientAPIs.report_service_health', cf_sf_client)
cli_command(__name__, 'sf service create', 'azure.cli.command_modules.sf.custom#sf_create_service')
cli_command(__name__, 'sf service description', 'azure.servicefabric#ServiceFabricClientAPIs.get_service_description', cf_sf_client)
cli_command(__name__, 'sf service update', 'azure.cli.command_modules.sf.custom#sf_update_service')

# Partition commands

cli_command(__name__, 'sf partition info', 'azure.servicefabric#ServiceFabricClientAPIs.get_partition_info', cf_sf_client)
cli_command(__name__, 'sf partition service-name', 'azure.servicefabric#ServiceFabricClientAPIs.get_service_name', cf_sf_client)
cli_command(__name__, 'sf partition report-health', 'azure.servicefabric#ServiceFabricClientAPIs.report_partition_health', cf_sf_client)
cli_command(__name__, 'sf partition health', 'azure.servicefabric#ServiceFabricClientAPIs.get_partition_health', cf_sf_client)

# Replica commands

cli_command(__name__, 'sf replica report-health', 'azure.servicefabric#ServiceFabricClientAPIs.report_replica_health', cf_sf_client)
cli_command(__name__, 'sf replica health', 'azure.servicefabric#ServiceFabricClientAPIs.get_replica_health', cf_sf_client)

# Node commands

cli_command(__name__, 'sf node list', 'azure.servicefabric#ServiceFabricClientAPIs.get_node_info_list', cf_sf_client)
cli_command(__name__, 'sf node remove-state', 'azure.servicefabric#ServiceFabricClientAPIs.remove_node_state', cf_sf_client)
cli_command(__name__, 'sf node stop', 'azure.servicefabric#ServiceFabricClientAPIs.stop_node', cf_sf_client)
cli_command(__name__, 'sf node restart', 'azure.servicefabric#ServiceFabricClientAPIs.restart_node', cf_sf_client)
cli_command(__name__, 'sf node start', 'azure.servicefabric#ServiceFabricClientAPIs.start_node', cf_sf_client)
cli_command(__name__, 'sf node replica-list', 'azure.servicefabric#ServiceFabricClientAPIs.get_deployed_service_replica_info_list', cf_sf_client)
cli_command(__name__, 'sf node load', 'azure.servicefabric#ServiceFabricClientAPIs.get_node_load_info', cf_sf_client)
cli_command(__name__, 'sf node health', 'azure.servicefabric#ServiceFabricClientAPIs.get_node_health', cf_sf_client)
cli_command(__name__, 'sf node report-health', 'azure.servicefabric#ServiceFabricClientAPIs.report_node_health', cf_sf_client)

# Cluster commands

cli_command(__name__, 'sf cluster select', 'azure.cli.command_modules.sf.custom#sf_select')
cli_command(__name__, 'sf cluster manifest', 'azure.servicefabric#ServiceFabricClientAPIs.get_cluster_manifest', cf_sf_client)
cli_command(__name__, 'sf cluster code-version', 'azure.servicefabric#ServiceFabricClientAPIs.get_provisioned_fabric_code_version_info_list', cf_sf_client)
cli_command(__name__, 'sf cluster config-version', 'azure.servicefabric#ServiceFabricClientAPIs.get_provisioned_fabric_config_version_info_list', cf_sf_client)
cli_command(__name__, 'sf cluster health', 'azure.servicefabric#ServiceFabricClientAPIs.get_cluster_health', cf_sf_client)
cli_command(__name__, 'sf cluster report-health', 'azure.servicefabric#ServiceFabricClientAPIs.report_cluster_health', cf_sf_client)

# Compose commands

cli_command(__name__, 'sf compose create', 'azure.cli.command_modules.sf.custom#sf_create_compose_application')
cli_command(__name__, 'sf compose status', 'azure.servicefabric#ServiceFabricClientAPIs.get_compose_application_status', cf_sf_client)
cli_command(__name__, 'sf compose list', 'azure.servicefabric#ServiceFabricClientAPIs.get_compose_application_status_list', cf_sf_client)
cli_command(__name__, 'sf compose remove', 'azure.servicefabric#ServiceFabricClientAPIs.remove_compose_application', cf_sf_client)

# Package commands

cli_command(__name__, 'sf application package copy', 'azure.cli.command_modules.sf.custom#sf_copy_app_package')