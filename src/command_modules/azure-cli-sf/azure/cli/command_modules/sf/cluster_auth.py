# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from msrest.authentication import Authentication

class ClientCertAuthentication(Authentication):
    """
    Client certificate authentication for Service Fabric clusters
    """
    def __init__(self, cert=None, key=None, pem=None):
        self.cert_path = cert
        self.key_path = key
        self.pem_path = pem

    def signed_session(self):
        """Create requests session with any required auth headers
        applied.

        :rtype: requests.Session.
        """
        session = super(ClientCertAuthentication, self).signed_session()
        if self.pem_path is not None:
            session.cert = self.pem_path
        else:
            session.cert = (self.cert_path, self.key_path)

        return session
