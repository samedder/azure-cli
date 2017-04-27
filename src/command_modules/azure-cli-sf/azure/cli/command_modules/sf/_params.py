# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azure.cli.core.sdk.util import ParametersContext
from azure.cli.core.util import get_json_object

# For some commands we take JSON strings as possible
with ParametersContext(command="sf application create") as c:
    c.register("parameters", ("--parameters",), type=get_json_object,
               help="JSON encoded list of application parameters.")

with ParametersContext(command="sf application create") as c:
    c.register("metrics", ("--metrics",), type=get_json_object,
               help="JSON encoded list of application metrics and their \
               descriptions.")

with ParametersContext(command="sf application upgrade") as c:
    c.register("parameters", ("--parameters",), type=get_json_object,
               help="JSON encoded list of application parameter overrides to \
               be applied when upgrading an application. Note, when starting \
               an upgrade, be sure to include the existing application \
               parameters, if any.")

with ParametersContext(command="sf application upgrade") as c:
    c.register("default_service_health_policy",
               ("--default_service_health_policy",),
               type=get_json_object, help="JSON encoded specification of the \
               health policy used by default to evaluate the health of a \
               service type.")

with ParametersContext(command="sf application upgrade") as c:
    c.register("service_health_policy", ("--service_health_policy",),
               type=get_json_object, help="JSON encoded map with service type \
               health policy per service type name. The map is empty be \
               default.")
