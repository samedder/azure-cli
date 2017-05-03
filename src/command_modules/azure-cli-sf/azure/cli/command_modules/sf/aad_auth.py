# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from msrest.authentication import Authentication

class AdalAuthentication(Authentication):
    """
    Azure Active Directory authentication for Service Fabric clusters
    """
    accessToken = None

    def __init__(self, token):
        self.accessToken = token

    def signed_session(self):
        session = super(AdalAuthentication, self).signed_session()

        header = "{} {}".format("Bearer", self.accessToken)
        session.headers['Authorization'] = header
        return session
