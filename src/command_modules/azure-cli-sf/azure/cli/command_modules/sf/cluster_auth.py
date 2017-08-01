# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from msrest.authentication import Authentication

class ClientCertAuthentication(Authentication):
    """
    Client certificate authentication for Service Fabric clusters
    """
    def __init__(self, cert=None, ca_cert=None):
        self.cert = cert
        self.ca_cert = ca_cert

    def signed_session(self):
        """Create requests session with any required auth headers
        applied.

        :rtype: requests.Session.
        """
        session = super(ClientCertAuthentication, self).signed_session()
        if self.cert is not None:
            session.cert = self.cert
        if self.ca_cert is not None:
            session.verify = self.ca_cert

        return session

class AadAuthentication(Authentication):
    """
    Azure Active Directory authentication for Service Fabric clusters
    """
    accessToken = None

    def __init__(self, token):
        self.accessToken = token

    def signed_session(self):
        session = super(AdalAuthentication, self).signed_session()

        header = "{} {}".format("bearer", token)
        session.headers['Authorization'] = header
        return session
