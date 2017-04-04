# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azure.cli.core.help_files import helps

# pylint: disable=line-too-long

helps[''] = """
     type: group
     short-summary: Manage Service Fabric clusters and perform cluster operations
"""
helps['cluster'] = """
    type: group
    short-summary: Connect to and manage entire Service Fabric clusters
"""
helps['node'] = """
    type: group
    short-summary: Manage the nodes that form a Service Fabric cluster
"""
helps['application'] = """
    type: group
    short-summary: Manage the applications running in a Service Fabric cluster
"""
