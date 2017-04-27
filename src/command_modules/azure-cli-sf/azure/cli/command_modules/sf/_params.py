# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

# pylint: disable=line-too-long

from azure.cli.core.commands import register_cli_argument

from azure.cli.core.sdk.util import ParametersContext
from azure.cli.core.util import get_json_object

with ParametersContext(command="sf application create")  as c:
    c.register("parameters", ("--parameters",), type=get_json_object,
               help="JSON encoded application parameters")
