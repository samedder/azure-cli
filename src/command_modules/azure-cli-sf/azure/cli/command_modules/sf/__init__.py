# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

def load_params(_):
    import azure.cli.command_modules.sf._params #pylint: disable=redefined-outer-name


def load_commands():
    import azure.cli.command_modules.sf.commands #pylint: disable=redefined-outer-name
