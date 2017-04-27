# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azure.cli.core.sdk.util import ParametersContext
from azure.cli.core.util import get_json_object

# For some commands we take JSON strings as possible
with ParametersContext(command="sf application create") as c:
    c.register("parameters", ("--parameters",), type=get_json_object,
               help="JSON encoded list of application parameters")

with ParametersContext(command="sf application create") as c:
    c.register("metrics", ("--metrics",), type=get_json_object,
               help="JSON encoded list of application metrics and their \
               descriptions. These can be generated using `az sf application \
               gen-metrics")
