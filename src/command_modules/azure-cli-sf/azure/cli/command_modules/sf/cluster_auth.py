# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from msrest.authentication import Authentication

class ClientCertAuthentication(Authentication):
    """
    Client certificate authentication for Service Fabric clusters
    """
    def __init__(self, cert=None):
        self.cert = cert

    def signed_session(self):
        """Create requests session with any required auth headers
        applied.

        :rtype: requests.Session.
        """
        session = super(ClientCertAuthentication, self).signed_session()
        if self.cert is not None:
            session.cert = self.cert

        return session
